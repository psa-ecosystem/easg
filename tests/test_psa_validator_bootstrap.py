"""Bootstrap sanity tests for the PSA validator migrated into EASG."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
BASELINE = Path("/Users/nexlume/codex/projects/PSA/docs/governance/PSA-Engineering-Baseline-v0.1.md")

sys.path.insert(0, str(TOOLS_DIR))

from psa_validator import __version__  # type: ignore[import]
from psa_validator.parser import extract_rules  # type: ignore[import]
from psa_validator.report import run_compliance  # type: ignore[import]


def test_package_imports_and_version():
    """The copied package must be importable and expose the expected version."""
    assert __version__ == "0.1.0"


def test_baseline_rules_are_extractable():
    """The PSA Engineering Baseline must be parseable by the validator."""
    rules = extract_rules(BASELINE)
    assert rules
    assert all("rule_id" in rule for rule in rules)


def test_cli_help_runs():
    """The CLI entry point must be invocable via the executable wrapper."""
    result = subprocess.run(
        [sys.executable, str(TOOLS_DIR / "psa-validator"), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "psa-validator" in result.stdout


def test_compliance_report_produced_for_empty_easg():
    """Running against the bare EASG repo must produce a structured report.

    At this bootstrap stage EASG is missing governance files, so the report
    should indicate failure and a compliance level below 3.
    """
    rules = extract_rules(BASELINE)
    report = run_compliance(REPO_ROOT, rules, "0.1.0")

    assert "summary" in report
    assert "results" in report
    assert report["summary"]["max_compliance_level"] == 3
    # EASG is intentionally not yet Level 3 compliant.
    assert report["summary"]["achieved_compliance_level"] < 3
    assert report["summary"]["overall_status"] == "failed"
    assert any(r["status"] == "failed" for r in report["results"])


def test_cli_check_returns_failure_for_empty_easg():
    """The CLI must return non-zero and emit a compliance report in JSON form."""
    result = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "psa-validator"),
            "check",
            str(REPO_ROOT),
            "--baseline",
            str(BASELINE),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1, result.stderr
    report = json.loads(result.stdout)
    assert report["summary"]["overall_status"] == "failed"
