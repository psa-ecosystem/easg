"""Markdown YAML rule block extraction."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc


YAML_BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


def extract_rules(baseline_path: Path) -> list[dict[str, Any]]:
    """Extract rule dictionaries from YAML code blocks in a Markdown file.

    Only blocks whose parsed content is a mapping with a top-level ``rules:``
    key that maps to a list of rule dictionaries are kept. Scalar, mapping, or
    metadata-only ``rules:`` values are ignored.
    """
    text = baseline_path.read_text(encoding="utf-8")
    blocks = YAML_BLOCK_RE.findall(text)
    rules: list[dict[str, Any]] = []
    for block in blocks:
        data = yaml.safe_load(block)
        if isinstance(data, dict) and isinstance(data.get("rules"), list):
            rules.extend(data["rules"])
    return rules
