"""Individual rule check execution."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc

MAX_READ_BYTES = 10 * 1024 * 1024


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _resolve_path(base_path: Path, target: str) -> Path:
    target_path = Path(target)
    if target_path.is_absolute():
        raise ValueError(f"absolute target paths are not allowed: {target}")
    base = base_path.resolve()
    resolved = (base / target_path).resolve()
    if resolved != base and base not in resolved.parents:
        raise ValueError(f"target escapes base_path: {target}")
    return resolved


def _safe_read_text(path: Path) -> str:
    size = path.stat().st_size
    if size > MAX_READ_BYTES:
        raise ValueError(f"file too large to read: {path} ({size} bytes)")
    return path.read_text(encoding="utf-8")


def _get_nested(data: Any, dotted_path: str) -> Any:
    current = data
    for part in dotted_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise KeyError(dotted_path)
    return current


def _failure_status(severity: str) -> str:
    return severity if severity in ("warning", "info") else "failed"


def _set_result(result: dict[str, Any], status: str, summary: str, evidence: dict[str, Any]) -> None:
    result["status"] = status
    result["summary"] = summary
    result["evidence"] = evidence


def _fail(result: dict[str, Any], severity: str, summary: str, evidence: dict[str, Any]) -> None:
    _set_result(result, _failure_status(severity), summary, evidence)


def _ensure_file(resolved: Path, target: str, result: dict[str, Any], severity: str) -> bool:
    if resolved.is_file():
        return True
    _fail(result, severity, f"File missing: {target}", {"path": str(resolved)})
    return False


def run_check(base_path: Path, rule: dict[str, Any]) -> dict[str, Any]:
    """Execute a single rule's check method against a repository."""
    rule_id = rule.get("rule_id", "UNKNOWN")
    method = rule.get("check_method")
    severity = rule.get("severity", "blocking")
    target = rule.get("target")

    result: dict[str, Any] = {
        "rule_id": rule_id,
        "status": "passed",
        "summary": "",
        "evidence": {},
    }

    try:
        if method == "manual":
            _set_result(result, "manual", "Manual review required", {})
            return result

        if target is None:
            raise ValueError("target is required for automated checks")

        resolved = _resolve_path(base_path, target)

        if method == "file_exists":
            if resolved.is_file():
                _set_result(result, "passed", f"File exists: {target}", {"path": str(resolved)})
            else:
                _fail(result, severity, f"File missing: {target}", {"path": str(resolved)})

        elif method == "dir_exists":
            if resolved.is_dir():
                _set_result(result, "passed", f"Directory exists: {target}", {"path": str(resolved)})
            else:
                _fail(result, severity, f"Directory missing: {target}", {"path": str(resolved)})

        elif method == "dir_not_empty":
            if resolved.is_dir():
                if any(resolved.iterdir()):
                    _set_result(result, "passed", f"Directory not empty: {target}", {"path": str(resolved)})
                else:
                    _fail(result, severity, f"Directory empty: {target}", {"path": str(resolved)})
            else:
                _fail(result, severity, f"Directory missing: {target}", {"path": str(resolved)})

        elif method == "regex_match":
            if _ensure_file(resolved, target, result, severity):
                content = _safe_read_text(resolved)
                pattern = rule.get("pattern", "")
                if re.search(pattern, content):
                    _set_result(result, "passed", f"Pattern matched in {target}", {"path": str(resolved), "pattern": pattern})
                else:
                    _fail(result, severity, f"Pattern not found in {target}", {"path": str(resolved), "pattern": pattern})

        elif method == "yaml_path":
            if _ensure_file(resolved, target, result, severity):
                data = load_yaml(resolved)
                path_expr = rule.get("path", "")
                try:
                    value = _get_nested(data, path_expr)
                    _set_result(result, "passed", f"YAML path found in {target}", {
                        "path": str(resolved),
                        "yaml_path": path_expr,
                        "value": value,
                    })
                except KeyError:
                    _fail(result, severity, f"YAML path not found in {target}", {"path": str(resolved), "yaml_path": path_expr})

        else:
            _set_result(result, "failed", f"Unknown check method: {method}", {"method": method})

    except Exception as exc:
        _set_result(result, "failed", f"Check raised {type(exc).__name__}: {exc}", {"error": str(exc)})

    return result
