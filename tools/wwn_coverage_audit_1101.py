#!/usr/bin/env python3
"""Audit Worlds Without Number coverage for #1101 and render the register.

This is a *traceability* tool, not a rules engine and not a prose gate. It joins
three layers that are allowed to disagree:

  1. the curated register (`data/rules/wwn_traceability.json`) — what the source
     says and which procedure claims to implement it;
  2. the Python tree — does the module/procedure named in the register exist?
  3. the tests — is an `implemented` row actually exercised?

`--check` fails if a claim is stale or the rendered report has drifted. It never
rules on whether a mechanic is *correct*; that needs the page-cited verification
queue in the report.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/rules/wwn_traceability.json"
REPORT = ROOT / "docs/rules/WWN_COVERAGE_1101.md"

STATUS_ORDER = ("implemented", "verified_reuse", "partial", "missing", "blocked", "not_applicable")
STATUS_LABEL = {
    "implemented": "implemented",
    "verified_reuse": "verified reuse",
    "partial": "partial",
    "missing": "missing",
    "blocked": "blocked",
    "not_applicable": "n/a",
}


def load_register(path: Path = DATA) -> dict:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("format") != "wwn-traceability-1":
        raise SystemExit(f"{path}: unexpected format {data.get('format')!r}")
    return data


def defined_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    rows = data.get("rows") or []
    ids = [row.get("id") for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate row ids")
    if not rows:
        errors.append("register has no rows")
        return errors

    for row in rows:
        rid = row.get("id", "<no id>")
        status = row.get("status")
        if status not in STATUS_LABEL:
            errors.append(f"{rid}: unknown status {status!r}")
            continue
        modules = row.get("modules") or []
        tests = row.get("tests") or []
        if row.get("edition") == "free_srd" and not str(row.get("srd") or "").startswith(
            "https://wwn.quadrifons.com/"
        ):
            errors.append(f"{rid}: free-SRD row without an SRD citation")

        for path_text in [m.get("path") for m in modules]:
            path = ROOT / str(path_text)
            if not path.is_file():
                errors.append(f"{rid}: module missing: {path_text}")
                continue
            names = defined_names(path)
            for module in modules:
                if module.get("path") != path_text:
                    continue
                for procedure in module.get("procedures") or []:
                    if procedure not in names:
                        errors.append(f"{rid}: {path_text} has no `{procedure}`")

        for test_text in tests:
            if not (ROOT / str(test_text)).is_file():
                errors.append(f"{rid}: test missing: {test_text}")

        if status == "implemented":
            if not modules or not tests:
                errors.append(f"{rid}: implemented needs modules and tests")
            else:
                stems = [Path(m["path"]).stem for m in modules]
                body = "\n".join((ROOT / t).read_text(encoding="utf-8", errors="ignore")
                                 for t in tests if (ROOT / t).is_file())
                if not any(stem in body for stem in stems):
                    errors.append(f"{rid}: tests never refer to {stems}")
        elif status == "verified_reuse":
            if not modules or not tests:
                errors.append(f"{rid}: verified_reuse needs modules and tests")
        elif status == "blocked":
            if row.get("edition") not in {"deluxe", "free_book"}:
                errors.append(f"{rid}: blocked row must be Deluxe or free-book-only")
            if modules:
                errors.append(f"{rid}: a blocked row must not claim an implementation")
        elif status == "missing" and modules:
            errors.append(f"{rid}: a missing row must not claim a module")

    compat = data.get("compatibility") or []
    for entry in compat:
        if entry.get("status") not in STATUS_LABEL:
            errors.append(f"compat {entry.get('id')}: unknown status")
        for path_text in entry.get("modules") or []:
            if not (ROOT / str(path_text)).is_file():
                errors.append(f"compat {entry.get('id')}: module missing: {path_text}")
    return errors


def counts(rows: list[dict]) -> Counter:
    return Counter(row["status"] for row in rows)


def code_cell(row: dict) -> str:
    modules = row.get("modules") or []
    if not modules:
        return "—"
    cells = []
    for module in modules:
        name = Path(module["path"]).name
        procedures = module.get("procedures") or []
        if procedures:
            cells.append(f"`{name}` ({', '.join(procedures[:3])}{'…' if len(procedures) > 3 else ''})")
        else:
            cells.append(f"`{name}`")
    return "<br>".join(cells)


def tests_cell(row: dict) -> str:
    tests = row.get("tests") or []
    if not tests:
        return "—"
    return "<br>".join(f"`{Path(test).name}`" for test in tests)


def render(data: dict) -> str:
    rows = data["rows"]
    tallies = counts(rows)
    total = len(rows)
    srd_rows = [row for row in rows if row.get("edition") == "free_srd"]
    compat = data.get("compatibility") or []
    lines = [
        "# Worlds Without Number — coverage register (#1101)",
        "",
        (f"**{total} rows** across the free SRD, the free-book-only material and Deluxe. "
        f"Source: the [WWN SRD]({data['source']['srd']}) (CC0; system text only)."),
        "",
        ("This is an **audit**, not a claim that NoöPunk runs Worlds Without Number. The "
        "tabletop rulebook remains CWN; WWN rows are the code-level supplement the issue asks "
        "for. A row is `verified reuse` only where the procedure is the shared Without Number "
        "chassis and a CWN test exercises it."),
        "",
        ("Citations are **section anchors**, not page numbers: the CC0 SRD is unpaginated and the "
        "free-book PDF was unavailable (HTTP 403), so no page is invented. Deluxe rows carry the "
        "issue's printed page because those are the only pages we can state without the text."),
        "",
        "## What the audit found",
        "",
        "| Status | Rows | Meaning |",
        "| --- | ---: | --- |",
    ]
    for status in STATUS_ORDER:
        lines.append(f"| {STATUS_LABEL[status]} | {tallies.get(status, 0)} | "
                     f"{data['status_legend'][status]} |")
    lines += [
        "",
        (f"- **{tallies.get('implemented', 0) + tallies.get('verified_reuse', 0)} of {total}** rows "
        "are implemented or verified reuse; the rest are named gaps, not silently missing."),
        (f"- **{tallies.get('blocked', 0)} blocked** rows are Deluxe or free-book-only procedures "
        "whose lawful text is not on this host. They are not synthesised."),
        (f"- Of the {len(srd_rows)} free-SRD rows, **{sum(1 for r in srd_rows if r['status'] in ('implemented', 'verified_reuse'))} "
        "are implemented or reused**, so the SRD is not the bottleneck; the unimplemented "
        "systems are (classes, factions, equipment, bestiary, travel)."),
        "",
        "## Register",
        "",
        "| § | Procedure | Status | Code | Tests | Tabletop | Note |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for chapter in dict.fromkeys(row["chapter"] for row in rows):
        lines.append(f"| | **{chapter}** | | | | | |")
        for row in (r for r in rows if r["chapter"] == chapter):
            note = row.get("note") or (
                "Shared Without Number chassis; no WWN-specific code."
                if row["status"] == "verified_reuse"
                else "Not implemented." if row["status"] == "missing" else ""
            )
            note = note.replace("|", "\\|")
            page = f" p.{row['page']}" if row.get("page") else ""
            lines.append(
                f"| {row['section']} | {row['title']}{page} | {STATUS_LABEL[row['status']]} | "
                f"{code_cell(row)} | {tests_cell(row)} | {row.get('tabletop_status', '—')} | {note} |"
            )
    lines += [
        "",
        "## Cross-game compatibility",
        "",
        ("The issue asks for a CWN↔WWN↔SWN↔AWN matrix. This is the part that can be stated "
        "without inventing conversions; each row names what exists and what does not."),
        "",
        "| Area | Status | Code | Note |",
        "| --- | --- | --- | --- |",
    ]
    for entry in compat:
        mods = ", ".join(f"`{Path(p).name}`" for p in entry.get("modules") or []) or "—"
        lines.append(f"| {entry['area']} | {STATUS_LABEL[entry['status']]} | {mods} | "
                     f"{entry.get('note', '').replace('|', chr(92) + '|')} |")
    lines += [
        "",
        "## Blocked sources",
        "",
        ("- **Deluxe (G–K)**: *The Legates*, Iterums/Gyre, the Latter Earth, Ruins and Relics, "
        "Sciences of the Latter Earth. The Deluxe PDF is not on this host; the CC0 SRD does not "
        "cover it. Nine rows are blocked, not guessed."),
        ("- **Free-book-only world/campaign tools (pp. 94–279)**: not in the CC0 SRD; the free-book "
        "mirror cited by #1101 returned HTTP 403 on 2026-11-03. Four rows are blocked."),
        ("- Rights: `data/sources/game_system_rights.json#worlds-without-number-srd` records "
        "`verified-public-domain` for the **SRD**, not the commercial book or its protected "
        "setting. Do not copy setting text from either edition."),
        "",
        "## Next queue (Phase 2, by dependency)",
        "",
        ("1. **Classes**: 15 of 19 absent, 3 partial (Adventurer, Elementalist, Necromancer); "
        "start with Warrior/Expert/Mage and the Adventurer "
        "combination engine, then Foci. High Mage is the only implemented class."),
        ("2. **Factions**: the WWN faction turn is wholly absent. The SWN engine is a different "
        "system — reuse its dice/state utilities only after a named parity check."),
        ("3. **Equipment and bestiary**: no WWN catalogues; the CWN lists govern the tabletop, so "
        "this is a conversion decision, not a transcription sprint."),
        "4. **Travel/wilderness/dungeon/hazards**: unported; AWN survival exists but is not WWN.",
        "5. **Spell effects**: 13 of 83 transcribed (#1085); do not duplicate its queue.",
        "6. **Deluxe G–K**: blocked until a lawful copy exists.",
        "",
        "## Verification",
        "",
        "```bash",
        "python3.11 tools/wwn_coverage_audit_1101.py --check",
        "```",
        "",
        ("The check verifies every claimed module/procedure via AST, every test path, the "
        "implemented/test link, and that this report is byte-identical to a fresh render."),
        "",
        ("Generated by `tools/wwn_coverage_audit_1101.py` from "
        "`data/rules/wwn_traceability.json`; do not edit by hand."),
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if stale or if any claim is broken")
    parser.add_argument("--write", action="store_true", help="write the rendered report")
    args = parser.parse_args(argv)

    data = load_register()
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    rendered = render(data)
    if args.write:
        REPORT.write_text(rendered, encoding="utf-8")
        print(f"wrote {REPORT.relative_to(ROOT)}")
        return 0
    if args.check:
        if not REPORT.is_file():
            print(f"ERROR: {REPORT.relative_to(ROOT)} is missing; run --write", file=sys.stderr)
            return 1
        if REPORT.read_text(encoding="utf-8") != rendered:
            print("ERROR: report is stale; run tools/wwn_coverage_audit_1101.py --write",
                  file=sys.stderr)
            return 1

    tallies = counts(data["rows"])
    print(f"WWN coverage OK — {len(data['rows'])} rows: " +
          ", ".join(f"{STATUS_LABEL[s]}={tallies.get(s, 0)}" for s in STATUS_ORDER))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
