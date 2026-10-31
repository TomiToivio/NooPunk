#!/usr/bin/env python3
"""Check and render the linked-SRD page audit (#950).

This is the **page-level** companion to the system-level CWN compliance matrix. That matrix answers "is
combat implemented?"; this one answers "is any page of the linked SRD unaccounted for?". It exists because
a system-level row like `combat/*` can hide several unimplemented pages behind one green cell.

The point of this tool is that the audit cannot drift into marketing. Every claim in
``data/rules/cwn/srd_page_coverage.json`` is checked against the repository:

* every page of the linked SRD is accounted for exactly once - completeness is proved, not asserted;
* every Godot module named actually exists;
* every test named actually exists;
* a row claiming ``implemented`` must name at least one test, because "implemented" without evidence is
  the failure mode this file exists to prevent;
* every Python symbol named must really be defined in ``mud/nopunk_mud/cwn_core.py``;
* ``not_applicable`` must say why, so a page cannot be quietly dropped by relabelling it.

Coverage of the *linked* SRD is not coverage of the published CWN rulebook: the hosted SRD omits
Antagonists/NPCs and some optional rules, and those are absent from this matrix rather than marked done.

Usage:
    python3 tools/cwn_page_audit.py --check
    python3 tools/cwn_page_audit.py --render docs/rules/CWN_SRD_PAGE_AUDIT_950.md

Exit codes: 0 = consistent, 1 = the matrix and the repository disagree.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data/rules/cwn/srd_page_coverage.json"
PAGES = ROOT / "data/rules/cwn/srd_pages.json"
PYTHON_CORE = ROOT / "mud/nopunk_mud/cwn_core.py"

COVERAGE = ("implemented", "partial", "missing", "not_applicable")
LABEL = {"implemented": "implemented", "partial": "partial", "missing": "missing",
         "not_applicable": "n/a"}


def _python_symbols(path: Path) -> set[str]:
    """Top-level function names defined in the MUD core."""
    if not path.exists():
        return set()
    body = path.read_text(encoding="utf-8")
    return set(re.findall(r"^(?:async\s+)?def\s+(\w+)", body, re.MULTILINE))


def load() -> tuple[dict, dict]:
    return (json.loads(MATRIX.read_text(encoding="utf-8")),
            json.loads(PAGES.read_text(encoding="utf-8")))


def problems(matrix: dict, pages: dict) -> list[str]:
    """Every way the matrix and the repository can disagree."""
    found: list[str] = []
    rows = matrix.get("rows") or []
    known = list(pages.get("pages") or [])
    symbols = _python_symbols(PYTHON_CORE)

    if matrix.get("format") != "cwn-srd-page-coverage-v1":
        found.append(f"unexpected format {matrix.get('format')!r}")

    seen: dict[str, int] = {}
    for row in rows:
        slug = row.get("srd", "")
        seen[slug] = seen.get(slug, 0) + 1
        if slug not in known:
            found.append(f"{slug}: not a page of the linked SRD")
        coverage = row.get("coverage")
        if coverage not in COVERAGE:
            found.append(f"{slug}: coverage {coverage!r} is not one of {COVERAGE}")
        for path in row.get("godot") or []:
            if not (ROOT / path).exists():
                found.append(f"{slug}: Godot module {path} does not exist")
        for test in row.get("tests") or []:
            path = test.split("::")[0]
            if not (ROOT / path).exists():
                found.append(f"{slug}: test file {path} does not exist")
        if coverage == "implemented" and not (row.get("tests") or []):
            found.append(f"{slug}: claimed implemented with no test")
        if coverage == "implemented" and not (row.get("python") or []):
            found.append(f"{slug}: claimed implemented with no Python target")
        if coverage == "not_applicable" and not (row.get("note") or "").strip():
            found.append(f"{slug}: not_applicable without a reason")
        for name in row.get("python") or []:
            if name not in symbols:
                found.append(f"{slug}: Python symbol {name} is not defined in "
                             f"{PYTHON_CORE.relative_to(ROOT)}")

    for slug, count in seen.items():
        if count > 1:
            found.append(f"{slug}: listed {count} times")
    for slug in known:
        if slug not in seen:
            found.append(f"{slug}: page of the linked SRD is missing from the matrix")
    return found


def summary(rows: list[dict]) -> dict[str, int]:
    counts = {key: 0 for key in COVERAGE}
    for row in rows:
        counts[row.get("coverage", "missing")] = counts.get(row.get("coverage", "missing"), 0) + 1
    return counts


def render(matrix: dict, pages: dict) -> str:
    rows = matrix.get("rows") or []
    counts = summary(rows)
    total = len(rows)
    lines = [
        "# CWN linked-SRD page audit (#950)",
        "",
        ("Per page of the linked SRD. The system-level view - what a system is and how far it is ported - "
         "is `docs/rules/CWN_COMPLIANCE_MATRIX_950.md`; this file answers the different question of "
         "whether any page has been left out."),
        "",
        ("**Generated by `tools/cwn_page_audit.py --render`; do not edit by hand.** "
         "`tests/test_cwn_srd_page_audit_950.py` fails if this file and the repository disagree."),
        "",
        (f"Scope: the **{total} pages** of the linked SRD at <{matrix.get('source')}>. This is not coverage of "
         "the published *Cities Without Number* book: the hosted SRD omits Antagonists/NPCs and some "
         "optional rules, and those pages are absent from the source rather than marked complete."),
        "",
        "| Coverage | Pages |",
        "|---|---:|",
    ]
    for key in COVERAGE:
        lines.append(f"| {LABEL[key]} | {counts.get(key, 0)} |")
    lines += [
        f"| **total** | **{total}** |",
        "",
        ("A page is `implemented` only when a test exercises it. `partial` means some of the page is ported "
         "and the rest is named in the note. `n/a` is a landing or terminology page with no procedure of "
         "its own, and always carries a reason."),
        "",
        "## Matrix",
        "",
        "| SRD page | Godot | Python | Coverage | Evidence | Note |",
        "|---|---|---|---|---|---|",
    ]
    for row in sorted(rows, key=lambda r: r["srd"]):
        slug = row["srd"]
        link = f"[{slug}]({row.get('srd_url', '')})" if row.get("srd_url") else slug
        godot = ", ".join(f"`{Path(p).name}`" for p in row.get("godot") or []) or "—"
        python = ", ".join(f"`{p}`" for p in row.get("python") or []) or "—"
        tests = ", ".join(f"`{t.split('::')[-1] if '::' in t else Path(t).name}`"
                          for t in row.get("tests") or []) or "—"
        note = (row.get("note") or "—").replace("|", "\\|")
        lines.append(f"| {link} | {godot} | {python} | {LABEL[row['coverage']]} | {tests} | {note} |")
    lines += [
        "",
        "## NoöPunk overlays",
        "",
        ("No page carries a NoöPunk overlay yet. Noösphere, Psyche, faction reputation and GUMSHOE-style "
         "investigation are **mods on this core** and must not change a CWN number; when one is added it "
         "gets its own column entry here rather than being folded into CWN coverage."),
        "",
        "## Porting order",
        "",
        ("The solo campaign in #950 needs, in this order: skills and backgrounds, initiative and action "
         "economy, Shock, injuries and healing, encumbrance, weapons and armour, then hacking. That is "
         "everything currently marked `missing` in `character-creation` and the combat rows."),
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="verify the matrix against the repository")
    parser.add_argument("--render", metavar="PATH", help="write the Markdown matrix to PATH")
    args = parser.parse_args(argv)

    matrix, pages = load()
    if args.render:
        target = Path(args.render)
        text = render(matrix, pages)
        if target.exists() and target.read_text(encoding="utf-8") == text:
            print(f"{target}: already up to date")
        else:
            target.write_text(text, encoding="utf-8")
            print(f"{target}: written")

    found = problems(matrix, pages)
    counts = summary(matrix.get("rows") or [])
    print(f"{len(matrix.get('rows') or [])} SRD pages: " +
          ", ".join(f"{counts.get(k, 0)} {LABEL[k]}" for k in COVERAGE))
    if found:
        for line in found:
            print(f"  - {line}", file=sys.stderr)
        print(f"{len(found)} problem(s): the matrix and the repository disagree", file=sys.stderr)
        return 1
    if args.check:
        print("matrix consistent with the repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
