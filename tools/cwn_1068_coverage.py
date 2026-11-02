#!/usr/bin/env python3
"""Render the CWN coverage audit for issue #1068.

This is an **audit**, not a rules engine and not a documentation gate. It joins two
curated sources:

* ``data/rules/cwn_compliance_matrix.json`` — what the Python/MUD/Godot layers implement
  and which tests exist (the existing #950 source of truth);
* ``data/rules/cwn_tabletop_audit_1068.json`` — which tabletop reference covers each CWN
  surface, and whether the reader-facing ``RULEBOOK.md`` still teaches a superseded
  mechanic for it.

Checks are limited to data-about-code: every matrix row has exactly one audit row, and
every referenced Python/test path exists. It does **not** match prose against a frozen
copy — the repository's AGENTS.md forbids that class of gate, and the rulebook is reviewed
editorially and by playtesting.

Usage:
    python3 tools/cwn_1068_coverage.py            # check + write the report
    python3 tools/cwn_1068_coverage.py --check    # check only
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "rules" / "cwn_compliance_matrix.json"
AUDIT = ROOT / "data" / "rules" / "cwn_tabletop_audit_1068.json"
DOC = ROOT / "docs" / "rules" / "CWN_COVERAGE_AUDIT_1068.md"

CHAPTER_TITLES = {
    "character-creation": "Character creation",
    "rules-of-the-game": "Rules of the game",
    "gear-vehicles-cyberware": "Gear, vehicles and cyberware",
    "hacking": "Hacking",
    "antagonists": "Antagonists",
}


def load() -> tuple[dict, dict]:
    return (json.loads(MATRIX.read_text(encoding="utf-8")),
            json.loads(AUDIT.read_text(encoding="utf-8")))


def check(matrix: dict, audit: dict) -> list[str]:
    """Data-about-code checks only. Returns human-readable problems."""
    problems: list[str] = []
    matrix_rows = {row["id"]: row for row in matrix.get("rows", [])}
    audit_rows = {row["id"]: row for row in audit.get("rows", [])}
    if set(matrix_rows) != set(audit_rows):
        only_matrix = sorted(set(matrix_rows) - set(audit_rows))
        only_audit = sorted(set(audit_rows) - set(matrix_rows))
        problems.append(f"matrix/audit id mismatch: only-matrix={only_matrix} only-audit={only_audit}")
    for row_id, row in audit_rows.items():
        if row["baseline_status"] not in audit["status_vocabulary"]["baseline_status"]:
            problems.append(f"{row_id}: unknown baseline_status {row['baseline_status']!r}")
        if row["rulebook_status"] not in audit["status_vocabulary"]["rulebook_status"]:
            problems.append(f"{row_id}: unknown rulebook_status {row['rulebook_status']!r}")
        if row["baseline_status"] == "exact" and not row["baseline"]:
            problems.append(f"{row_id}: exact baseline status with no reference")
        if row["rulebook_status"] not in ("missing", "not_applicable") and not row["rulebook"]:
            problems.append(f"{row_id}: non-missing rulebook status with no reference")
    for row_id, row in matrix_rows.items():
        for key in ("python", "mud", "tests", "godot"):
            for path in row.get(key) or []:
                if not (ROOT / str(path)).exists():
                    problems.append(f"{row_id}: {key} path does not exist: {path}")
        if row["coverage"] == "implemented" and not any(
                (ROOT / t).exists() for t in (row.get("tests") or [])):
            problems.append(f"{row_id}: implemented but no existing test")
    return problems


def counts(matrix: dict, audit: dict) -> dict:
    python = Counter(row["coverage"] for row in matrix["rows"])
    baseline = Counter(row["baseline_status"] for row in audit["rows"])
    rulebook = Counter(row["rulebook_status"] for row in audit["rows"])
    return {"python": python, "baseline": baseline, "rulebook": rulebook}


def _join(matrix: dict, audit: dict) -> list[dict]:
    code = {row["id"]: row for row in matrix["rows"]}
    rows = []
    for row in audit["rows"]:
        source = code[row["id"]]
        rows.append({**row, "coverage": source["coverage"], "python": source.get("python") or [],
                     "mud": source.get("mud") or [], "tests": source.get("tests") or []})
    return rows


def _table(rows: list[dict]) -> list[str]:
    lines = [
        "| System | SRD | Tabletop baseline | RULEBOOK.md | Tabletop | Python | Tests | Note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        unique_tests = list(dict.fromkeys(row["tests"]))
        tests = ("—" if row["coverage"] == "not_applicable"
                 else ", ".join(f"`{Path(t).name}`" for t in unique_tests[:2]) or "—")
        note = row["note"].replace("|", "\\|") or "—"
        lines.append(
            f"| **{row['system']}** | {row['srd'].replace('https://cwn.quadrifons.com/', 'SRD: ')} | "
            f"{row['baseline'] or '—'} | {row['rulebook'] or '—'} | "
            f"{row['baseline_status']} / {row['rulebook_status']} | {row['coverage']} | {tests} | {note} |"
        )
    return lines


def render(matrix: dict, audit: dict) -> str:
    c = counts(matrix, audit)
    rows = _join(matrix, audit)
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_chapter[row["chapter"]].append(row)

    py = c["python"]
    base = c["baseline"]
    book = c["rulebook"]
    total = len(rows)
    lines = [
        "# CWN rule coverage audit (#1068)",
        "",
        ("Generated by `tools/cwn_1068_coverage.py` from "
         "`data/rules/cwn_compliance_matrix.json` (#950) and "
         "`data/rules/cwn_tabletop_audit_1068.json` (#1068). **Audit, not a rules change.**"),
        "",
        (f"**{total} CWN SRD surfaces.** Source: <https://cwn.quadrifons.com/>. "
         "The linked hosted SRD omits the Antagonists chapter; that is recorded as a source "
         "limitation, not as coverage."),
        "",
        "## Counts",
        "",
        "| layer | state | count |",
        "| --- | --- | ---: |",
    ]
    for key, label in (("implemented", "implemented"), ("unverified", "unverified"),
                       ("missing", "missing"), ("not_applicable", "not applicable")):
        lines.append(f"| Python / MUD / Godot | {label} | {py.get(key, 0)} |")
    for key, label in (("exact", "baseline names the procedure and source chapter"),
                       ("category", "baseline names only the category"),
                       ("not_applicable", "chapter overview")):
        lines.append(f"| Tabletop baseline | {label} | {base.get(key, 0)} |")
    for key, label in (("legacy_conflict", "RULEBOOK.md teaches a superseded mechanic"),
                       ("partial", "RULEBOOK.md has related material only"),
                       ("missing", "RULEBOOK.md does not document it"),
                       ("not_applicable", "chapter overview")):
        lines.append(f"| Reader rulebook | {label} | {book.get(key, 0)} |")

    lines += [
        "",
        "## What the numbers mean",
        "",
        (f"- **Tabletop:** the baseline covers **{base.get('exact', 0)}** surfaces exactly and "
         f"**{base.get('category', 0)}** at category level; it is a source-dependent baseline, so the "
         "CWN book/SRD is still required at the table. This is the intended, licensed arrangement."),
        (f"- **Reader rulebook:** **{book.get('legacy_conflict', 0)}** surfaces still have a chapter "
         f"that teaches a superseded mechanic, **{book.get('partial', 0)}** have related material only, "
         f"and **{book.get('missing', 0)}** are absent. The banner at the top of RULEBOOK.md is correct, "
         "but the chapters below it are not rewritten. That is the largest documentation gap in this "
         "audit."),
        (f"- **Python:** **{py.get('implemented', 0)}** surfaces have a module and a test, "
         f"**{py.get('unverified', 0)}** have code without a test that names the rule, and "
         f"**{py.get('missing', 0)}** are missing. `implemented` is not the same claim as "
         "`verified against the book`."),
        "",
        "## Relation to the #1068 policy",
        "",
        ("This matrix is the tabletop-side companion to `docs/rules/CWN_IMMUTABLE_CORE_1068.md`. That "
         "document requires a source reference, Python symbol/test, exact tabletop heading, integration "
         "note and independent status for every procedure. Here, `baseline` means the baseline names the "
         "procedure and its governing source chapter; it is **not** a `verified` claim, and the CWN "
         "book/SRD is still required at the table. Nothing in this report certifies semantic conformance; "
         "the structural guard in `tools/check_cwn_lock_1068.py` is likewise structural only."),
        "",
        "## Traceability matrix",
        "",
    ]
    for chapter in ("character-creation", "rules-of-the-game", "gear-vehicles-cyberware",
                    "hacking", "antagonists"):
        lines += [f"### {CHAPTER_TITLES.get(chapter, chapter)}", ""]
        lines += _table(by_chapter.get(chapter, []))
        lines.append("")

    legacy = [r for r in rows if r["rulebook_status"] == "legacy_conflict"]
    missing_doc = [r for r in rows if r["rulebook_status"] == "missing"
                   and r["baseline_status"] != "not_applicable"]
    py_gaps = [r for r in rows if r["coverage"] in {"unverified", "missing"}]
    both = [r for r in py_gaps if r["rulebook_status"] in {"legacy_conflict", "partial", "missing"}]
    lines += [
        "## Gaps, in the order they should be worked",
        "",
        "### 1. Reader rulebook still contradicts the baseline",
        "",
        ("These chapters must either be rewritten as CWN procedures or clearly marked historical in "
         "place. They are the pages a tabletop reader will follow by mistake."),
        "",
        *[f"- **{r['system']}** — `{r['rulebook']}` ({r['coverage']} in Python)" for r in legacy],
        "",
        "### 2. Python code without a test that names the rule",
        "",
        *[(f"- **{r['system']}** — {r['coverage']}; modules: "
           f"{', '.join(Path(p).name for p in r['python'][:3]) or '—'}") for r in py_gaps],
        "",
        "### 3. Both layers thin or absent",
        "",
        *[(f"- **{r['system']}** — Python `{r['coverage']}`, rulebook `{r['rulebook_status']}`"
           + (f": {r['note']}" if r["note"] else "")) for r in both],
        "",
        "### 4. Documentation absent but the baseline covers it",
        "",
        *[f"- **{r['system']}** — baseline: {r['baseline']}" for r in missing_doc[:20]],
        f"- …and {max(0, len(missing_doc) - 20)} more; see the matrix above." if len(missing_doc) > 20 else "",
        "",
        "## Source limitations",
        "",
        ("- The hosted SRD omits **Antagonists/NPC statistics**; the free rulebook may contain it, but "
         "no page-cited transcription exists in this repository. It is not claimed as covered."),
        ("- Deluxe-only material (some cyberware, vehicle and hacking options) is out of scope until a "
         "licence review and legally available text exist. Do not fill these from memory."),
        "- SWN/AWN are licence-constrained in this repository; their rows are not part of this CWN count.",
        "",
        "## No CWN rule was changed",
        "",
        ("This audit adds data and a report. It does not edit `src/rules/`, `mud/nopunk_mud/`, the CWN "
         "SRD tables, or any published procedure. The only rulebook edit in this change is the authority "
         "statement at the top of `RULEBOOK.md`, which now names CWN as the mechanical core and marks "
         "the conflicting chapters historical — a statement of the existing baseline decision, not a "
         "new rule."),
        "",
        "## Maintenance workflow (same-PR gate)",
        "",
        ("Per AGENTS.md, prose is not a CI test target, so the correspondence is enforced by a review "
         "checklist rather than a text matcher:"),
        "",
        ("1. A rule or mod change updates its **CWN source reference**, **tabletop procedure**, "
         "**Python module**, **test**, and **this audit row** in the same pull request."),
        "2. A new or changed Python rule that cannot name a tabletop reference is not finished.",
        ("3. A rulebook chapter that conflicts with the baseline is either rewritten or marked "
         "historical; it may not stay silently authoritative."),
        "4. `python3 tools/cwn_1068_coverage.py --check` must pass (ids and code paths only).",
        "5. `python3 tools/check_cwn_compliance.py` and the engine-boundary check run in CI as before.",
        "",
        "## How to reproduce",
        "",
        "```bash",
        "python3.11 tools/check_cwn_compliance.py        # validate the #950 code matrix",
        "python3.11 tools/cwn_1068_coverage.py --check   # join tabletop audit + code matrix",
        "python3.11 tools/cwn_1068_coverage.py           # rewrite this report",
        "```",
        "",
    ]
    return "\n".join(line for line in lines if line is not None) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render the CWN coverage audit (#1068).")
    parser.add_argument("--check", action="store_true", help="validate only; do not write the report")
    args = parser.parse_args(argv)

    matrix, audit = load()
    problems = check(matrix, audit)
    if problems:
        print("cwn coverage audit: FAILED")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("cwn coverage audit: data and code paths consistent")
    if not args.check:
        DOC.write_text(render(matrix, audit), encoding="utf-8")
        print(f"report -> {DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
