"""psa-validator command line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from psa_validator.parser import extract_rules
from psa_validator.report import report_to_json, run_compliance, self_check


def _baseline_default() -> Path:
    return Path("docs/governance/PSA-Engineering-Baseline-v0.1.md")


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--baseline",
        type=Path,
        default=_baseline_default(),
        help="Baseline Markdown file",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Output report path",
    )
    parser.add_argument(
        "--report-id",
        type=str,
        default=None,
        help="Deterministic report ID",
    )
    parser.add_argument(
        "--generated-at",
        type=str,
        default=None,
        help="Deterministic ISO-8601 timestamp",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON instead of human-readable text",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="psa-validator",
        description="PSA Engineering Baseline compliance validator",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Validate a repository")
    check.add_argument(
        "repo",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Repository root to validate (default: .)",
    )
    check.add_argument(
        "--scope",
        type=str,
        default=None,
        help="Filter by rule scope",
    )
    _add_common_args(check)

    self_check = subparsers.add_parser("self-check", help="Validate the baseline document itself")
    _add_common_args(self_check)

    return parser


def _render(report: dict[str, Any], use_json: bool) -> str:
    if use_json:
        return report_to_json(report)
    from psa_validator.report import format_human
    return format_human(report)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        baseline_path = args.baseline.resolve()

        if args.command == "self-check":
            report = self_check(
                baseline_path,
                report_id=args.report_id,
                generated_at=args.generated_at,
            )
        else:
            repo_root = args.repo.resolve()
            rules = extract_rules(baseline_path)
            if args.scope:
                rules = [r for r in rules if r.get("scope") == args.scope]
            report = run_compliance(
                repo_root,
                rules,
                "0.1.0",
                report_id=args.report_id,
                generated_at=args.generated_at,
            )

        output = _render(report, args.json)
        if args.report:
            args.report.write_text(output, encoding="utf-8")
        else:
            print(output)

        return 0 if report["summary"]["overall_status"] != "failed" else 1
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
