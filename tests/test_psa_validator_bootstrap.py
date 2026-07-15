from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE = Path("/Users/nexlume/codex/projects/PSA/docs/governance/PSA-Engineering-Baseline-v0.1.md")


def test_validator_runs():
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "psa-validator"),
            "check",
            ".",
            "--baseline",
            str(BASELINE),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode in (0, 1)
    assert "Compliance Level" in result.stdout or "Compliance Level" in result.stderr


def test_validator_package_imports():
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from psa_validator import __version__  # type: ignore[import]

    assert __version__ == "0.1.0"
