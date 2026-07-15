"""psa_validator CLI entry point for `python3 -m psa_validator`."""

from __future__ import annotations

import sys

from psa_validator.cli import main

if __name__ == "__main__":
    sys.exit(main())
