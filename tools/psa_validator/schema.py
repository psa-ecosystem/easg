"""Rule schema validation."""

from __future__ import annotations

import re
from typing import Any

RULE_ID_RE = re.compile(r"^EB-([A-Z]{2,})-\d{3}$")

ALLOWED_CATEGORIES = {
    "baseline",
    "governance",
    "repository",
    "project",
    "contract",
    "version",
    "documentation",
    "testing",
    "release",
    "agent",
    "compliance",
}
ALLOWED_STATUSES = {"active", "draft", "deprecated"}
ALLOWED_METHODS = {
    "file_exists",
    "dir_exists",
    "dir_not_empty",
    "regex_match",
    "yaml_path",
    "manual",
}
ALLOWED_SEVERITIES = {"blocking", "warning", "info"}
ALLOWED_LEVELS = {1, 2, 3}

CATEGORY_PREFIXES: dict[str, set[str]] = {
    "baseline": {"STATUS", "SCOPE", "BASELINE"},
    "governance": {"GOV"},
    "repository": {"RG"},
    "project": {"PC"},
    "contract": {"IC"},
    "version": {"VS"},
    "documentation": {"DOC"},
    "testing": {"TEST"},
    "release": {"REL"},
    "agent": {"AGENT"},
    "compliance": {"COMP"},
}

REQUIRED_FIELDS = [
    "rule_id",
    "category",
    "scope",
    "status",
    "compliance_level",
    "owner",
    "title",
    "requirement",
    "rationale",
    "check_method",
    "severity",
]


def validate_rule_schema(rule: dict[str, Any]) -> list[str]:
    """Validate a single rule against the PSA Engineering Baseline Rule Schema."""
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in rule:
            errors.append(f"missing field: {field}")

    rule_id = rule.get("rule_id")
    match = RULE_ID_RE.match(str(rule_id or ""))
    if not match:
        errors.append(f"invalid rule_id: {rule_id}")
    else:
        prefix = match.group(1)
        category = rule.get("category")
        allowed_prefixes = CATEGORY_PREFIXES.get(category) if isinstance(category, str) else None
        if allowed_prefixes is not None and prefix not in allowed_prefixes:
            errors.append(
                f"rule_id prefix '{prefix}' is not allowed for category '{category}'"
            )

    if rule.get("category") not in ALLOWED_CATEGORIES:
        errors.append(f"invalid category: {rule.get('category')}")
    if rule.get("status") not in ALLOWED_STATUSES:
        errors.append(f"invalid status: {rule.get('status')}")
    if rule.get("compliance_level") not in ALLOWED_LEVELS:
        errors.append(f"invalid compliance_level: {rule.get('compliance_level')}")
    if rule.get("check_method") not in ALLOWED_METHODS:
        errors.append(f"invalid check_method: {rule.get('check_method')}")
    if rule.get("severity") not in ALLOWED_SEVERITIES:
        errors.append(f"invalid severity: {rule.get('severity')}")

    method = rule.get("check_method")
    if method in ("file_exists", "dir_exists", "dir_not_empty", "regex_match", "yaml_path"):
        if "target" not in rule:
            errors.append(f"{rule_id}: target is required for {method}")
    if method == "regex_match" and "pattern" not in rule:
        errors.append(f"{rule_id}: pattern is required for regex_match")
    if method == "yaml_path" and "path" not in rule:
        errors.append(f"{rule_id}: path is required for yaml_path")

    return errors
