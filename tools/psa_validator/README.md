# psa_validator

PSA Engineering Baseline compliance validator package.

## Module map

| Module | Responsibility |
|---|---|
| `parser.py` | Extract YAML rule blocks from the baseline Markdown document. |
| `schema.py` | Rule schema constants, category-to-prefix mapping, and validation. |
| `checks.py` | Individual rule check execution (`file_exists`, `regex_match`, etc.). |
| `report.py` | Compliance level computation, report assembly, and formatting. |
| `cli.py` | Subcommand CLI (`check`, `self-check`). |

## Usage

From the repository root:

```bash
# Validate the current repository
./tools/psa-validator check .

# Validate the baseline document itself
./tools/psa-validator self-check

# Machine-readable JSON output
./tools/psa-validator check . --json

# Deterministic report for CI
./tools/psa-validator check . --json --report report.json --report-id my-run --generated-at 2026-07-14T00:00:00+00:00
```

The legacy entry point remains available:

```bash
python3 tools/psa_compliance_validator.py
python3 tools/psa_compliance_validator.py --self-check
```
