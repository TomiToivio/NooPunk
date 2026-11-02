#!/usr/bin/env python3
"""Verify the CWN traceability inventory against the tree (#1068).

The inventory (`data/rules/cwn_rule_inventory.json`) is the claim; this tool is the check. It refuses the
two ways a coverage matrix usually lies:

* a row that claims `implemented` while naming no Python test — untested is not implemented;
* a row that names a module or a test file that does not exist, or a module that does not import.

It also reports the counts, so the honest number is printed rather than described.

    python3 tools/cwn_rule_inventory_audit.py            # human-readable
    python3 tools/cwn_rule_inventory_audit.py --check    # exit 1 on any violation
    python3 tools/cwn_rule_inventory_audit.py --markdown > docs/rules/CWN_RULE_INVENTORY.md
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "data" / "rules" / "cwn_rule_inventory.json"
STATUSES = ("implemented", "partial", "unverified", "missing", "not_applicable")


def load(path: Path = INVENTORY) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != "noopunk.rules.cwn_rule_inventory":
        raise SystemExit(f"{path} is not a CWN rule inventory")
    return data


def _module_imports(rel: str) -> tuple[bool, str]:
    """Import the module as a package member so its relative imports resolve.

    Loading it by file location fails on every ``from .cwn_core import ...`` and would report a healthy
    module as missing — the check must not lie in the other direction either.
    """
    if not (ROOT / rel).exists():
        return False, "file does not exist"
    dotted = rel.removesuffix(".py").replace("/", ".")
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    try:
        importlib.import_module(dotted)
    except Exception as exc:  # noqa: BLE001 - any import failure means the claim is false
        return False, f"import failed: {type(exc).__name__}: {exc}"
    return True, ""


def audit(data: dict) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for row in data["rows"]:
        identifier = row["id"]
        if identifier in seen:
            problems.append(f"{identifier}: duplicate row")
        seen.add(identifier)
        if row["status"] not in STATUSES:
            problems.append(f"{identifier}: unknown status {row['status']!r}")
        if not isinstance(row.get("printed_page"), int) or row["printed_page"] < 1:
            problems.append(f"{identifier}: needs the printed page it came from")
        for module_path in row.get("python", []):
            if not module_path.endswith(".py"):
                continue
            ok, why = _module_imports(module_path)
            if not ok:
                problems.append(f"{identifier}: {module_path} {why}")
        for test_path in row.get("tests", []):
            if not (ROOT / test_path).exists():
                problems.append(f"{identifier}: test {test_path} does not exist")
        if row["status"] == "implemented" and not row.get("tests"):
            problems.append(f"{identifier}: claims implemented without a Python test")
        if row["status"] == "implemented" and not row.get("python"):
            problems.append(f"{identifier}: claims implemented without a module")
        if row["status"] != "not_applicable" and not row.get("evidence"):
            problems.append(f"{identifier}: needs an evidence note saying what was checked")
    return problems


def totals(data: dict) -> Counter:
    return Counter(row["status"] for row in data["rows"])


def markdown(data: dict) -> str:
    counts = totals(data)
    total = len(data["rows"])
    lines = [
        "# CWN rule inventory — every Deluxe chapter and section",
        "",
        (f"Source: *{data['source']['book']}*, printed pages as they appear in the book "
         f"(PDF page = printed + {data['source']['pdf_page_offset']}). Generated from "
         "`data/rules/cwn_rule_inventory.json` by `tools/cwn_rule_inventory_audit.py --markdown`; "
         "do not edit this table by hand."),
        "",
        f"**{total} rows** — " + ", ".join(f"{counts[s]} {s}" for s in STATUSES if counts[s]),
        "",
        "| printed p. | section | status | python | tests | evidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in data["rows"]:
        modules = "<br>".join(f"`{m}`" for m in row["python"]) or "—"
        tests = "<br>".join(f"`{t}`" for t in row["tests"]) or "—"
        lines.append(f"| {row['printed_page']} | {row['chapter']} — {row['section']} | "
                     f"{row['status']} | {modules} | {tests} | {row['evidence']} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="exit 1 on any violation")
    parser.add_argument("--markdown", action="store_true", help="render the document from the data")
    args = parser.parse_args(argv)

    data = load()
    if args.markdown:
        sys.stdout.write(markdown(data))
        return 0

    problems = audit(data)
    counts = totals(data)
    print(f"rows: {len(data['rows'])}")
    for status in STATUSES:
        print(f"  {status:15} {counts[status]}")
    if args.check:
        if problems:
            for problem in problems:
                print(problem)
            print(f"\n{len(problems)} problem(s) in the CWN inventory")
            return 1
        print("\nOK: every claimed module imports, every named test exists, no untested claim")
        return 0
    for problem in problems:
        print(f"  ! {problem}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
