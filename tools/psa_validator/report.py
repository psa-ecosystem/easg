"""Compliance report generation and formatting."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from psa_validator.checks import run_check
from psa_validator.parser import extract_rules
from psa_validator.schema import validate_rule_schema


def compute_compliance_level(results: list[dict[str, Any]]) -> int:
    """Compute the achieved compliance level.

    A blocking failure at compliance level N caps achievement at N-1.
    """
    blocking_failures = set()
    for r in results:
        if r.get("status") == "failed" and r.get("severity") == "blocking":
            blocking_failures.add(r.get("compliance_level", 1))

    for level in range(3, 0, -1):
        if all(failure_level > level for failure_level in blocking_failures):
            return level
    return 0


def _enrich_result(result: dict[str, Any], rule: dict[str, Any]) -> dict[str, Any]:
    """Add rule metadata fields required in every report result."""
    result["category"] = rule.get("category")
    result["severity"] = rule.get("severity", "blocking")
    result["compliance_level"] = rule.get("compliance_level", 1)
    return result


def run_compliance(
    repo_root: Path,
    rules: list[dict[str, Any]],
    baseline_version: str,
    report_id: str | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Run all active rules against a repository and produce a compliance report."""
    results: list[dict[str, Any]] = []
    counts = {"passed": 0, "failed": 0, "warnings": 0, "info": 0, "manual": 0, "skipped": 0}

    for rule in rules:
        rule_id = rule.get("rule_id")
        if rule.get("status") == "deprecated":
            results.append(_enrich_result({
                "rule_id": rule_id,
                "status": "skipped",
                "summary": "deprecated rule skipped",
                "evidence": {},
            }, rule))
            counts["skipped"] += 1
            continue
        if rule.get("status") == "draft":
            results.append(_enrich_result({
                "rule_id": rule_id,
                "status": "skipped",
                "summary": "draft rule skipped",
                "evidence": {},
            }, rule))
            counts["skipped"] += 1
            continue

        result = run_check(repo_root, rule)
        _enrich_result(result, rule)
        results.append(result)

        status = result["status"]
        if status == "passed":
            counts["passed"] += 1
        elif status == "failed":
            counts["failed"] += 1
        elif status == "warning":
            counts["warnings"] += 1
        elif status == "info":
            counts["info"] += 1
        elif status == "manual":
            counts["manual"] += 1
        else:
            counts["skipped"] += 1

    achieved = compute_compliance_level(results)
    any_blocking_failed = any(
        r.get("status") == "failed" and r.get("severity") == "blocking" for r in results
    )
    overall = "failed" if any_blocking_failed else "passed_with_warnings" if counts["warnings"] else "passed"

    return {
        "report_id": report_id or f"psa-eb-check-{repo_root.name}-{datetime.now(timezone.utc).isoformat()}",
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "baseline_version": baseline_version,
        "target": str(repo_root),
        "summary": {
            "overall_status": overall,
            **counts,
            "max_compliance_level": 3,
            "achieved_compliance_level": achieved,
        },
        "results": results,
    }


def self_check(
    baseline_path: Path,
    report_id: str | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Validate the baseline document itself."""
    rules = extract_rules(baseline_path)
    results: list[dict[str, Any]] = []

    ids = [str(r["rule_id"]) for r in rules if r.get("rule_id")]
    duplicates = {rid for rid in ids if ids.count(rid) > 1}

    baseline_rule = {
        "rule_id": "EB-BASELINE-001",
        "category": "baseline",
        "scope": "baseline_validation",
        "status": "active",
        "compliance_level": 3,
        "owner": "PSA Governance",
        "title": "Baseline rule IDs must be unique",
        "requirement": "Every rule_id defined in PSA Engineering Baseline MUST appear exactly once across all YAML rule blocks.",
        "rationale": "Prevents duplicate or conflicting rules.",
        "check_method": "manual",
        "severity": "blocking",
    }
    results.append(_enrich_result({
        "rule_id": "EB-BASELINE-001",
        "status": "failed" if duplicates else "passed",
        "summary": f"duplicate rule ids: {sorted(duplicates)}" if duplicates else "all rule ids unique",
        "evidence": {"duplicates": sorted(duplicates)},
    }, baseline_rule))

    text = baseline_path.read_text(encoding="utf-8")
    appendix_section = text.split("## Appendix A: Rule Registry")[1] if "## Appendix A: Rule Registry" in text else ""
    registry_ids = set(re.findall(r"\|\s*(EB-[A-Z]{2,}-\d{3})\s*\|", appendix_section))
    body_ids = set(ids)
    missing_in_registry = body_ids - registry_ids
    missing_in_body = registry_ids - body_ids
    registry_ok = not missing_in_registry and not missing_in_body
    results.append(_enrich_result({
        "rule_id": "EB-BASELINE-002",
        "status": "passed" if registry_ok else "failed",
        "summary": "registry matches rule blocks" if registry_ok else "registry mismatch",
        "evidence": {
            "missing_in_registry": sorted(missing_in_registry),
            "missing_in_body": sorted(missing_in_body),
        },
    }, baseline_rule))

    schema_errors: list[str] = []
    for rule in rules:
        schema_errors.extend(validate_rule_schema(rule))
    results.append(_enrich_result({
        "rule_id": "EB-BASELINE-003",
        "status": "failed" if schema_errors else "passed",
        "summary": f"{len(schema_errors)} schema errors" if schema_errors else "all rules match schema",
        "evidence": {"errors": schema_errors[:20]},
    }, baseline_rule))

    any_failed = any(r["status"] == "failed" for r in results)
    return {
        "report_id": report_id or f"psa-eb-self-check-{datetime.now(timezone.utc).isoformat()}",
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "baseline_version": "0.1.0",
        "target": str(baseline_path),
        "summary": {
            "overall_status": "failed" if any_failed else "passed",
            "passed": sum(1 for r in results if r["status"] == "passed"),
            "failed": sum(1 for r in results if r["status"] == "failed"),
            "warnings": 0,
            "info": 0,
            "manual": 0,
            "skipped": 0,
            "max_compliance_level": 3,
            "achieved_compliance_level": 3 if not any_failed else 0,
        },
        "results": results,
    }


def format_human(report: dict[str, Any]) -> str:
    """Render a compliance report in human-readable text."""
    summary = report.get("summary", {})
    lines: list[str] = []
    lines.append("PSA Compliance Report")
    lines.append("")
    lines.append(f"Target:    {report.get('target')}")
    lines.append(f"Baseline:  {report.get('baseline_version')}")
    lines.append(f"Report ID: {report.get('report_id')}")
    lines.append("")
    lines.append(f"Compliance Level: {summary.get('achieved_compliance_level')} / {summary.get('max_compliance_level')}")
    lines.append(f"Overall Status:   {summary.get('overall_status')}")
    lines.append("")
    lines.append(
        f"Passed: {summary.get('passed', 0)}  "
        f"Failed: {summary.get('failed', 0)}  "
        f"Warnings: {summary.get('warnings', 0)}  "
        f"Info: {summary.get('info', 0)}  "
        f"Manual: {summary.get('manual', 0)}  "
        f"Skipped: {summary.get('skipped', 0)}"
    )
    lines.append("")

    results = report.get("results", [])
    if results:
        lines.append("Results:")
        for r in results:
            status = r.get("status", "unknown")
            symbol = {
                "passed": "✓",
                "failed": "✗",
                "warning": "⚠",
                "info": "ℹ",
                "manual": "?",
                "skipped": "⊘",
            }.get(status, "•")
            lines.append(f"  {symbol} {r.get('rule_id')} [{r.get('category')}] {r.get('summary')}")

    return "\n".join(lines)


def report_to_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False)
