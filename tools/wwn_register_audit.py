#!/usr/bin/env python3
"""WWN rule register (#1101) — thin wrapper around `tools/rules_register_audit.py`.

The validator is shared with the SWN register (#1105). A second copy of it would be the same duplicate-tool
mistake this repository has already paid for twice, so this file only says where the WWN register lives.

Usage:
    python3 tools/wwn_register_audit.py --render docs/rules/WWN_COVERAGE_1101.md
    python3 tools/wwn_register_audit.py --check --render docs/rules/WWN_COVERAGE_1101.md
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rules_register_audit import (  # noqa: F401
    BLOCKED_ALLOWED,
    CLAIMS_CODE,
    audit,
    counts,
    fidelity_counts,
    render,
    run,
)
from rules_register_audit import (
    load as _load,
)

REGISTER = "data/rules/wwn_register.json"


def load(register_path: str | None = None):
    return _load(register_path or REGISTER)


def main(argv: list[str] | None = None) -> int:
    return run(argv, default_register=REGISTER)


if __name__ == "__main__":
    raise SystemExit(main())
