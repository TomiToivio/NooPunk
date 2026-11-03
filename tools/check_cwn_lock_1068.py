#!/usr/bin/env python3
"""Issue #1068: conservative CWN foundation and tabletop/Python parity guard.

Checks repository structure and the evidence inventory. This is NOT a claim
of semantic conformity to the published CWN rules.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/rules/cwn_fe_toc.json"
TABLETOP = ROOT / "RULEBOOK.md"
PYTHON = ROOT / "src/rules"
POLICY = ROOT / "docs/rules/CWN_IMMUTABLE_CORE_1068.md"
MATRIX = ROOT / "docs/rules/CWN_COVERAGE_1068.md"  # the single coverage document; the old matrix path is a pointer


def audit() -> list[str]:
    failures: list[str] = []
    for file in (SOURCE, TABLETOP, POLICY, MATRIX):
        if not file.is_file() or not file.read_text(encoding="utf-8").strip():
            failures.append(f"Required nonempty file missing: {file.relative_to(ROOT)}")
    if not PYTHON.is_dir() or not list(PYTHON.glob("cwn_*.py")):
        failures.append("Python CWN rule modules missing")
    if SOURCE.is_file():
        try:
            entries = json.loads(SOURCE.read_text(encoding="utf-8"))
            if not isinstance(entries, list) or not entries:
                failures.append("Free Edition table of contents must be a nonempty list")
            else:
                for i, item in enumerate(entries):
                    if not isinstance(item, dict) or not isinstance(item.get("title"), str) or not isinstance(item.get("pdf_page"), int):
                        failures.append(f"Invalid TOC row: {i}")
        except (ValueError, TypeError) as exc:
            failures.append(f"Invalid Free Edition TOC: {exc}")
    if POLICY.is_file():
        content = POLICY.read_text(encoding="utf-8")
        for marker in ("https://cwn.quadrifons.com/", "CWN_Free_Version_081123.pdf", "RULEBOOK.md", "src/rules"):
            if marker not in content:
                failures.append(f"Policy missing reference: {marker}")
    return failures


if __name__ == "__main__":
    errors = audit()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print("CWN #1068 structural guard passed (NOT a rules-fidelity certification).")
