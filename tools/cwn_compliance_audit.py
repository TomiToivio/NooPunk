#!/usr/bin/env python3
"""Audit the CWN compliance matrix, and render the document from it (#950).

The matrix exists because the issue forbids claiming coverage "based on filenames alone".
So the matrix is **data** (`data/mud/cwn_compliance.json`), each row names the Python module
and the test files that are supposed to own its rule, and this tool resolves those claims
against the tree:

* every `python` path must exist and must actually import;
* every path in `tests` must exist;
* a row that claims `implemented` must name at least one **Python** test (a `.gd` test does
  not prove a Python module works);
* the totals are printed, so a reader sees how much of the linked SRD is real.

`--markdown` renders `docs/mud/CWN_COMPLIANCE_MATRIX.md`, so the document and the data can
never drift: regenerate it instead of editing the table.

    python3 tools/cwn_compliance_audit.py            # audit, human-readable
    python3 tools/cwn_compliance_audit.py --check    # audit, exit 1 on any violation
    python3 tools/cwn_compliance_audit.py --markdown > docs/mud/CWN_COMPLIANCE_MATRIX.md

This is a documentation/data audit, not a CI gate: it is not wired into `.github/workflows/`,
per the executable-code-only testing policy (#271).
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATRIX = ROOT / "data" / "mud" / "cwn_compliance.json"
SRC = ROOT / "src"


def load() -> dict:
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def _imports(path: str) -> tuple[bool, str]:
    """Import a module through its package, so a row cannot point at a file that does not run.

    The modules are imported as ``rules.<name>`` with ``src`` on the path rather than loaded
    by file path: they use relative imports, and loading a file directly reports a false
    ``ImportError`` on a module that is perfectly healthy.
    """
    full = ROOT / path
    if not full.exists():
        return False, "missing"
    try:
        dotted = full.relative_to(SRC).with_suffix("").as_posix().replace("/", ".")
    except ValueError:
        return False, "not under src/"
    sys.path.insert(0, str(SRC))
    try:
        importlib.import_module(dotted)
    except Exception as exc:  # a broken module is exactly what this audit is for
        return False, f"{type(exc).__name__}: {exc}"
    finally:
        sys.path.remove(str(SRC))
    return True, ""


def audit(data: dict, *, run_tests: bool = False) -> list[str]:
    violations: list[str] = []
    for row in data["rows"]:
        coverage = row["coverage"]
        python_target = row.get("python")
        tests = row.get("tests", [])

        if python_target and not (ROOT / python_target).exists():
            violations.append(f"{row['id']}: python target missing: {python_target}")
        if python_target and (ROOT / python_target).exists():
            ok, why = _imports(python_target)
            if not ok:
                violations.append(f"{row['id']}: {python_target} does not import ({why})")
        for test in tests:
            if not (ROOT / test).exists():
                violations.append(f"{row['id']}: test path missing: {test}")
        if coverage == "implemented" and not any(t.endswith(".py") for t in tests):
            violations.append(
                f"{row['id']}: claims 'implemented' but names no Python test — "
                "a GDScript test does not prove the Python module"
            )
        if coverage == "implemented" and not python_target:
            violations.append(f"{row['id']}: claims 'implemented' with no python target")
    return violations


def totals(data: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in data["rows"]:
        counts[row["coverage"]] = counts.get(row["coverage"], 0) + 1
    return counts


def markdown(data: dict) -> str:
    counts = totals(data)
    order = ["implemented", "partial", "godot-only", "missing", "omitted-by-srd"]
    summary = " · ".join(f"**{counts.get(name, 0)}** {name}" for name in order)
    lines = [
        "# CWN rules compliance matrix (NoöPunk MUD)",
        "",
        "**Generated** by `python3 tools/cwn_compliance_audit.py --markdown`. Do not edit this",
        "file by hand: edit `data/mud/cwn_compliance.json` and regenerate, so the table and the",
        "audit can never disagree.",
        "",
        f"**Issue:** {data['issue']} · **Rules source:** the linked SRD, <{data['srd_source']}>",
        f"· **Full book:** {data['full_book_reference']}",
        "",
        f"**Rows:** {len(data['rows'])} — {summary}",
        "",
        "| # | SRD section | Python target | Godot status | Coverage | Tests | Note |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, row in enumerate(data["rows"], start=1):
        srd = f"[{row['srd']}]({data['srd_source'].rstrip('/')}{row['srd_path']})" if row.get("srd_path") else row["srd"]
        python_target = f"`{row['python']}`" if row.get("python") else "—"
        godot = f"`{row['godot']}`" if row.get("godot") else "—"
        tests = ", ".join(f"`{Path(t).name}`" for t in row.get("tests", [])) or "—"
        lines.append(
            f"| {index} | {srd} | {python_target} | {godot} | **{row['coverage']}** | {tests} | {row['note'] or ''} |"
        )
    lines += [
        "",
        "## What this matrix does and does not claim",
        "",
        "* A row is **implemented** only when a Python module owns the procedure and a Python test",
        "  exercises it. The audit fails a row that claims implemented with only a GDScript test.",
        "* **godot-only** rows are migration targets, not coverage. They are the first work for the",
        "  MUD-era port: `-` focus gear budget, mission time, chases, wages and bribes,",
        "  pharmaceuticals, cyberware mods/systems, cyberware alienation.",
        "* **omitted-by-srd** rows record the linked SRD's own stated gaps (antagonists and optional",
        "  rules). Coverage of the full published book is **not** claimed anywhere.",
        "* Overlays (GUMSHOE investigation, Noösphere/Psychic modules, ideology) are NoöPunk modules",
        "  layered on this baseline and are deliberately absent from this table.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit non-zero on any violation")
    parser.add_argument("--markdown", action="store_true", help="print the generated document")
    args = parser.parse_args()

    data = load()
    if args.markdown:
        print(markdown(data))
        return 0

    violations = audit(data)
    counts = totals(data)
    print(f"rows: {len(data['rows'])}")
    for name in ("implemented", "partial", "godot-only", "missing", "omitted-by-srd"):
        print(f"  {name:<16}{counts.get(name, 0)}")
    if violations:
        print("\nviolations:", file=sys.stderr)
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)
        return 1 if args.check else 0
    print("\nOK: every named module imports and every named test file exists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
