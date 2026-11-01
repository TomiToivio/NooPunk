#!/usr/bin/env python3
"""Render the CWN Free Edition parity matrix (#1025) from its JSON authority."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "rules" / "cwn_free_edition_parity_1025.json"
OUT = ROOT / "docs" / "rules" / "CWN_FREE_EDITION_PARITY_1025.md"

BACKLOG = (
    ("1", "Parity matrix, validator and baseline audit", "this PR", "No dependency"),
    ("2", "Character creation end-to-end: contacts/one-roll tables, starting gear, final sheet, save/load", "tests/test_cwn_*", "1"),
    ("3", "MUD combat loop: initiative, actions, maneuvers, turn/save-resume, command wiring", "cwn_combat* + cwn/*", "2"),
    ("4", "Chases, vehicle combat actions, drone operation, cyberdecks", "cwn_vehicles, cwn_drones", "3"),
    ("5", "Pharmaceuticals, cyberware surgery/mods/maintenance/alienation, gear economy", "cwn_core, cwn_gear_mods", "2"),
    ("6", "Hacking simulator: node graph, cyberspace actions, programs, demons/watchdogs, servers", "cwn_hacking, cwn_program_catalogue", "3"),
    ("7", "NPC stat blocks/bestiary, NPC cyber summaries, reaction/morale commands", "cwn_npcs", "3"),
    ("8", "Mission/scheme/city/megacorp/gang generators, mission tags/types, Heat accrual", "cwn_heat + new generator modules", "7"),
    ("9", "Solo campaign integration and full book-example acceptance audit", "mud/solo_campaign", "2-8"),
)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    rows = data["rows"]
    counts = Counter(row["status"] for row in rows)
    lines = [
        "# CWN Free Edition parity matrix (#1025)",
        "",
        "**Generated** by `python3 tools/render_cwn_1025_matrix.py --write` from",
        "`data/rules/cwn_free_edition_parity_1025.json`. Do not hand-edit this file; edit the JSON and",
        "regenerate so the audit and its evidence cannot disagree.",
        "",
        f"**Source:** CWN Free Edition 081123, 231 pages. Book page numbers are used; the PDF page is the",
        f"book page + {data['pdf_page_offset']} in this printing. SRD cross-check: <https://cwn.quadrifons.com/>.",
        "The SRD omits optional sections and the Antagonists/NPC material, so the PDF governs.",
        "",
        "**Constitution:** `docs/rules/RULES_CONSTITUTION.md` (#1006). Vanilla CWN is locked; NoöPunk,",
        "GUMSHOE, Noösphere, faction and stress layers are separate overlays and are never counted here.",
        "",
        "## Honest status legend",
        "",
        "- `complete` — Python rule exists, has an executable test, and is reachable from the MUD/campaign",
        "  where the procedure is player-facing. A module without a test is not complete.",
        "- `partial` — some rule logic or data exists, but a printed procedure, MUD surface, persistence",
        "  proof or book-example test is missing. The gap column names it.",
        "- `missing` — no Python implementation of the procedure.",
        "- `not_applicable` — setting fiction, advice or reference matter with no mechanical procedure.",
        "",
        "Command-wired, persistent-save-safe and playtested are **not** implied by `complete` unless the",
        "gap column says so. The baseline is deliberately conservative: no 100% claim from file existence.",
        "",
        f"**Rows:** {len(rows)} — " + " · ".join(f"**{key}** {counts[key]}" for key in
                                                ("complete", "partial", "missing", "not_applicable")),
        "",
        "| Section | Book pp. | Status | Python | MUD | Tests | Gap / evidence |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        cells = [row["section"], str(row["page"]), row["status"], row["python"] or "—",
                 row["mud"] or "—", row["tests"] or "—", row["note"] or "—"]
        lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in cells) + " |")
    lines += [
        "",
        "## Coverage by chapter",
        "",
        "The table above follows the Free Edition table of contents. Character creation, the core rules,",
        "equipment basics, injuries and advancement are substantially implemented. The largest genuine",
        "gaps are GM-facing: chases, drugs, cyberdecks/drone operation, the full hacking simulator, NPC",
        "stat blocks, and the entire mission/scheme/city generation chapter. Those are named as missing",
        "rather than hidden behind data files.",
        "",
        "## Implementation backlog (dependency order)",
        "",
        "| # | Slice | Evidence | Depends on |",
        "| --- | --- | --- | --- |",
    ]
    for number, title, evidence, dep in BACKLOG:
        lines.append(f"| {number} | {title} | {evidence} | {dep} |")
    lines += [
        "",
        "Each slice lands as its own PR linked to #1025 and updates this matrix. The issue stays open",
        "until the final acceptance audit has no unexplained `partial`/`missing` mechanical row.",
    ]
    text = "\n".join(lines) + "\n"
    if "--write" in __import__("sys").argv:
        OUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows)")
    else:
        import sys
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
