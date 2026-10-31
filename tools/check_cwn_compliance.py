#!/usr/bin/env python3
"""Validate and render the CWN compliance matrix (#950).

The matrix is only worth having if a false claim fails somewhere. This checks that:

* every referenced file actually exists;
* a row claiming `implemented` lists at least one test that exists — a module without a test is `partial`;
* every row names an SRD section, and every status is one of the declared values;
* a row whose SRD section is not in the linked SRD is marked `missing`, never `implemented`.

It also renders `docs/rules/CWN_COMPLIANCE_MATRIX_950.md` from the JSON, so the document cannot drift from the
data it describes.

Usage:
    python3 tools/check_cwn_compliance.py            # validate
    python3 tools/check_cwn_compliance.py --render   # rewrite the markdown
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "rules" / "cwn_compliance_matrix.json"
DOC = ROOT / "docs" / "rules" / "CWN_COMPLIANCE_MATRIX_950.md"

REQUIRED = ("id", "system", "srd", "godot", "python", "mud", "coverage", "tests")
#: Sections the linked hosted SRD does not include. A claim of coverage there is a false claim.
OMITTED_BY_SOURCE = ("Antagonists",)


def validate(matrix: dict, root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    statuses = set(matrix.get("statuses", []))
    rows = matrix.get("rows")
    if not isinstance(rows, list) or not rows:
        return ["matrix has no rows"]

    seen: set[str] = set()
    omitted = " ".join(matrix.get("srd", {}).get("scope_note", "").split())
    for index, row in enumerate(rows):
        label = str(row.get("id") or f"rows[{index}]")
        missing = [key for key in REQUIRED if key not in row]
        if missing:
            problems.append(f"{label}: missing {', '.join(missing)}")
            continue
        if label in seen:
            problems.append(f"{label}: duplicate id")
        seen.add(label)

        if row["coverage"] not in statuses:
            problems.append(f"{label}: unknown coverage {row['coverage']!r}")

        for key in ("godot", "python", "mud", "tests"):
            for path in row.get(key) or []:
                if not (root / str(path)).exists():
                    problems.append(f"{label}: {key} path does not exist: {path}")

        if row["coverage"] == "implemented":
            tests = [p for p in (row.get("tests") or []) if (root / str(p)).exists()]
            if not tests:
                problems.append(
                    f"{label}: claims implemented but lists no existing test — a module without a test is partial")

        section = str(row.get("srd", ""))
        if any(token in section for token in OMITTED_BY_SOURCE) and row["coverage"] == "implemented":
            problems.append(
                f"{label}: {section!r} is not in the linked SRD; it cannot be marked implemented")
        if any(token in section for token in OMITTED_BY_SOURCE) and not str(
                row.get("divergence", "")).strip():
            problems.append(f"{label}: an omitted section needs a note saying so")

    if "omits" not in omitted:
        problems.append("scope_note must state what the linked SRD omits")
    return problems


def render(matrix: dict) -> str:
    lines = [
        "# CWN compliance matrix (#950)",
        "",
        "Generated from `data/rules/cwn_compliance_matrix.json` by `tools/check_cwn_compliance.py --render`.",
        "Do not edit by hand: edit the JSON and regenerate, or the matrix and its evidence disagree.",
        "",
        f"**Source:** {matrix['srd']['source']}",
        "",
        f"> {matrix['srd']['scope_note']}",
        "",
        "Status is deliberately conservative: **implemented** requires an existing test; a module without a test",
        "is **partial**. A section the linked SRD omits is **missing**, however much code mentions it.",
        "",
        "| System | SRD | Godot | Python | MUD | Coverage | Tests | Divergence |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in matrix["rows"]:
        def cell(key: str) -> str:
            values = row.get(key) or []
            if not values:
                return "—"
            return "<br>".join(f"`{Path(str(v)).name}`" for v in values)
        lines.append(
            f"| **{row['system']}** | {row['srd']} | {cell('godot')} | {cell('python')} | "
            f"{cell('mud')} | `{row['coverage']}` | {cell('tests')} | {row.get('divergence') or '—'} |")
    counts: dict[str, int] = {}
    for row in matrix["rows"]:
        counts[row["coverage"]] = counts.get(row["coverage"], 0) + 1
    lines += ["", "## Totals", "",
              " · ".join(f"**{k}**: {v}" for k, v in sorted(counts.items())), "",
              "## Notes", "",
              "- The MUD column is empty wherever only the Godot or Python layer implements the rule; that is a",
              "  port target, not a contradiction.",
              "- Tabletop references point at the rulebook segment that owns the same rule, so a mechanic change",
              "  has one place to update besides the code and this matrix.",
              ]
    return "\n".join(lines) + chr(10)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()

    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    problems = validate(matrix)
    if problems:
        for problem in problems:
            print(f"FAIL {problem}")
        print(f"{len(problems)} problem(s)")
        return 1

    if args.render:
        DOC.parent.mkdir(parents=True, exist_ok=True)
        DOC.write_text(render(matrix), encoding="utf-8")
        print(f"rendered {DOC.relative_to(ROOT)}")
    print(f"CWN compliance matrix OK — {len(matrix['rows'])} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
