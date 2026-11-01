#!/usr/bin/env python3
"""Render the CWN Free Edition parity matrix (#1025, milestone 1).

Every section of the book's own table of contents is mapped to the Python module that implements it, the test
that exercises it, and a status. Nothing is inferred from a filename: a section is `complete` only when a module
exists **and** a test references it, `partial` when the module exists without test evidence, `missing` when
there is no module at all, and `setting` only where the book's own section is prose/advice rather than a
procedure, with the reason stated.

The point is to make the epic tractable and to stop "file exists" from standing in for "rule works". The matrix
is generated, so it cannot quietly drift from the code the way a hand-maintained table does.

Usage:
    python3 tools/cwn_fe_parity.py --render docs/rules/CWN_FE_PARITY_MATRIX.md
    python3 tools/cwn_fe_parity.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOC = ROOT / "data" / "rules" / "cwn_fe_toc.json"
COVERAGE = ROOT / "data" / "rules" / "cwn_coverage.json"
RULES = ROOT / "src" / "rules"
TESTS = ROOT / "tests"

#: ToC section -> implementing modules (stems), or "setting" with the reason it is not mechanical.
#: A section not named here is reported as `missing`: silence is never read as done.
MAPPING: dict[str, object] = {
    "A Slow Chrome Apocalypse": ("setting", "what the game is about; no procedure"),
    "Character Creation": ["cwn_character", "cwn_backgrounds", "cwn_edges_foci", "cwn_foci"],
    "Attributes": ["cwn_character"],
    "Skills": ["wn_core", "cwn_character"],
    "Choosing a Background": ["cwn_backgrounds"],
    "Contacts": ["cwn_backgrounds"],
    "One-Roll Contact Tables": ["cwn_backgrounds"],
    "Edges": ["cwn_edges_foci"],
    "Foci": ["cwn_foci", "cwn_edges_foci"],
    "Hit Points, Attack Bonus, and Saves": ["cwn_character", "cwn_core", "cwn_advancement"],
    "Starting Gear": ["cwn_equipment"],
    "Fi n a l To u c h e s": ["cwn_character"],
    "The Rules of the Game": ("setting", "chapter divider"),
    "Scenes, Rounds, and Mission Time": ["cwn_mission_time"],
    "Saving Throws": ["cwn_core"],
    "Skill Checks": ["wn_core"],
    "Combat": ["cwn_combat", "cwn_core"],
    "The Combat Round": ["cwn_initiative", "cwn_combat_actions"],
    "Actions in Combat": ["cwn_combat_actions"],
    "Combat Maneuvers and Definitions": ["cwn_combat_actions", "cwn_attack_modifiers"],
    "Injury, Healing, and System Strain": ["cwn_core", "cwn_strain", "cwn_healing"],
    "Major Injuries and Damaging Cyberware": ["cwn_major_injury", "cwn_injury_procedure"],
    "Vehicle Combat": ["cwn_vehicles"],
    "Chases and Pursuit": ["cwn_vehicles"],
    "Character Advancement": ["cwn_advancement"],
    "Crafting and Modifying Gear": ["cwn_gear_mods"],
    "The Tools of the Trade": ("setting", "chapter divider"),
    "Encumbrance": ["cwn_encumbrance"],
    "Acquiring Gear": ["cwn_equipment"],
    "Gear, Lifestyles, and Services": ["cwn_equipment"],
    "Armor": ["cwn_equipment", "cwn_gear_mods"],
    "Weapons": ["cwn_equipment"],
    "Armor and Weapon Mods": ["cwn_gear_mods"],
    "Pharmaceuticals and Street Drugs": [],
    "Cyberware": ["cwn_cyberware"],
    "Cyberware Mods": ["cwn_cyberware"],
    "Cyberdecks": [],
    "Drones": ["cwn_drones"],
    "Drone Fittings": ["cwn_drones"],
    "Drone Operation": ["cwn_drones"],
    "Vehicles": ["cwn_vehicles"],
    "Vehicle Fittings": ["cwn_vehicles"],
    "Vehicle-Mounted Weaponry": ["cwn_vehicles"],
    "Vehicle Mods": ["cwn_vehicles"],
    "Example Vehicles": ["cwn_vehicles"],
    "Hacking": ["cwn_hacking", "cwn_program_catalogue"],
    "Cyberspace, Nodes, and Access": ["cwn_hacking"],
    "Hacking Mechanics": ["cwn_hacking"],
    "Programs": ["cwn_program_catalogue"],
    "Cyberspace Actions": ["cwn_hacking"],
    "Demons and Watchdogs": [],
    "Network Servers and Architecture": [],
    "reating Your Dystopia": ("setting", "GM guidance chapter; generators still in scope"),
    "Cyberpunk Themes": ("setting", "thematic guidance, no procedure"),
    "Creating The World": [],
    "Creating The City": [],
    "Building Your Districts": [],
    "Creating Megacorps": [],
    "Creating Gangs": [],
    "Creating NPCs": [],
    "reating and Running Missions": [],
    "Creating Schemes": [],
    "NPC Operator Teams": [],
    "NPC Scheme Results": [],
    "How To Create a Mission": [],
    "Mission Tags": [],
    "Mission Types": [],
    "Creating an Intrusion Mission": [],
    "Playing the Mission": [],
    "Mission Rewards and Experience": [],
    "Heat": ["cwn_heat"],
    "aces On the Street": ("setting", "NPC chapter divider"),
    "Reaction Rolls and Morale": ["cwn_npcs"],
    "Morale and Morale Checks": ["cwn_npcs"],
    "Beasts and Guard Animals": [],
    "Corp Guards and Law Enforcement": [],
    "Gangers and Criminals": [],
    "Hackers and Pilots": [],
    "NPC Cyber Descriptions": [],
    "he City": ("setting", "example city; explicitly not NooPunk canon"),
    "A Timeline of Collapse": ("setting", "setting lore, no procedure"),
    "The Megacorps": ("setting", "setting lore"),
    "Other Groups and Organizations": ("setting", "setting lore"),
    "The Ethos of the City": ("setting", "setting lore"),
    "The City Government": ("setting", "setting lore"),
    "Crime and Punishment": ("setting", "setting lore"),
    "Social Relationships in the City": ("setting", "setting lore"),
    "Gender and Identity": ("setting", "setting lore"),
    "The Districts of the City": ("setting", "example districts"),
    "The Citadel": ("setting", "example district"),
    "The Flats": ("setting", "example district"),
    "Fogtown": ("setting", "example district"),
    "Gannett": ("setting", "example district"),
    "Portside": ("setting", "example district"),
    "Rachowski": ("setting", "example district"),
    "ixing Sine Nomine Games Together": ("setting", "cross-game guidance"),
    "ndex": ("setting", "index"),
    "unificent Kickstarter Backers": ("setting", "credits"),
}


def load() -> tuple[list[dict], dict]:
    return (json.loads(TOC.read_text(encoding="utf-8")),
            json.loads(COVERAGE.read_text(encoding="utf-8")))


def tests_by_module() -> dict[str, list[str]]:
    """Test files that name a module, so evidence is a real reference rather than a guess."""
    found: dict[str, list[str]] = {}
    for path in sorted(TESTS.glob("test_*.py")):
        body = path.read_text(encoding="utf-8", errors="replace")
        for name in re.findall(r"\b(cwn_[a-z_]+|wn_core|swn_[a-z_]+)\b", body):
            found.setdefault(name, [])
            if path.name not in found[name]:
                found[name].append(path.name)
    return found


def build() -> list[dict]:
    toc, coverage = load()
    procedures = {m["module"].removesuffix(".py"): len(m["procedures"]) for m in coverage["modules"]}
    evidence = tests_by_module()
    rows = []
    for entry in toc:
        title = entry["title"]
        spec = MAPPING.get(title)
        if isinstance(spec, tuple):
            status, note = "setting", spec[1]
            modules, tests, count = [], [], 0
        elif isinstance(spec, list):
            modules = [m for m in spec if m in procedures]
            absent = [m for m in spec if m not in procedures]
            tests = sorted({t for m in modules for t in evidence.get(m, [])})
            count = sum(procedures.get(m, 0) for m in modules)
            if not modules:
                status = "missing"
                note = "no module implements this section"
            elif tests:
                # "tested" means a module exists and a test references it. It is evidence of implementation,
                # NOT proof that every subprocedure on the page is covered - that needs the per-procedure audit.
                status = "tested"
                note = ""
            else:
                status = "untested"
                note = "module exists but no test references it"
            if absent:
                note = (note + "; " if note else "") + "declared but absent: " + ", ".join(absent)
        else:
            modules, tests, count = [], [], 0
            status, note = "missing", "not mapped yet"
        rows.append({"title": title, "pdf_page": entry["pdf_page"], "modules": modules,
                     "procedures": count, "tests": tests, "status": status, "note": note})
    return rows


def summary(rows: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        out[row["status"]] = out.get(row["status"], 0) + 1
    return out


def render(rows: list[dict]) -> str:
    counts = summary(rows)
    lines = [
        "# CWN Free Edition parity matrix (#1025, milestone 1)",
        "",
        "**Generated by `tools/cwn_fe_parity.py`; do not edit by hand.**",
        "",
        "Table of contents captured from the CWN Free Edition PDF (081123, 231 pages) at",
        "`data/rules/cwn_fe_toc.json`. The SRD at <https://cwn.quadrifons.com/> is a cross-check only: it omits",
        "optional sections and the Antagonists & NPCs material, so several Free Edition sections below have no",
        "SRD counterpart.",
        "",
        "Every section of the Free Edition's own table of contents, in book order, mapped to the module that",
        "implemented it and the test that exercises it.",
        "",
        "| Status | Means |",
        "|---|---|",
        ("| `tested` | a module implements it **and** a test references it. Evidence of implementation, "
         "**not** proof that every subprocedure on those pages is covered — that is the per-procedure audit. |"),
        "| `untested` | a module exists but no test references it. |",
        "| `missing` | nothing implements it. |",
        "| `setting` | the book's section is prose or advice rather than a procedure, with the reason given. |",
        "",
        "Silence is never read as done.",
        "",
        "| Status | Sections |",
        "|---|---:|",
    ]
    for key in ("tested", "untested", "missing", "setting"):
        lines.append(f"| {key} | {counts.get(key, 0)} |")
    lines += [f"| **total** | **{len(rows)}** |", "", "## Matrix", "",
              "| Section | PDF p. | Modules | Procedures | Tests | Status | Note |",
              "|---|---:|---|---:|---|---|---|"]
    for row in rows:
        mods = ", ".join(f"`{m}`" for m in row["modules"]) or "—"
        tests = ", ".join(f"`{t}`" for t in row["tests"][:2]) or "—"
        note = (row["note"] or "—").replace("|", "\\|")
        lines.append(f"| {row['title']} | {row['pdf_page']} | {mods} | {row['procedures']} | {tests} "
                     f"| {row['status']} | {note} |")
    missing = [f"{row['title']} (p{row['pdf_page']})" for row in rows if row["status"] == "missing"]
    lines += ["", "## The gaps, generated", ""]
    if missing:
        lines.append(f"**{len(missing)} sections have no implementing module.** This list is generated from the "
                     "matrix, so it cannot go stale the way a hand-written summary would:")
        lines.append("")
        for entry in missing:
            lines.append(f"- {entry}")
    else:
        lines.append("Every mechanical section has an implementing module.")
    lines += [
        "",
        "No section is marked `tested` on the strength of a data file or a filename, and `tested` is not a claim",
        "that every subprocedure on those pages is covered.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--render", metavar="PATH")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    rows = build()
    counts = summary(rows)
    unmapped = [r["title"] for r in rows if r["note"] == "not mapped yet"]
    if unmapped:
        print(f"{len(unmapped)} section(s) with no mapping entry: {', '.join(unmapped[:5])}", file=sys.stderr)
        return 1

    if args.render:
        target = Path(args.render)
        text = render(rows)
        if target.exists() and target.read_text(encoding="utf-8") == text:
            print(f"{target}: already up to date")
        else:
            target.write_text(text, encoding="utf-8")
            print(f"{target}: written")

    print(f"{len(rows)} Free Edition sections: " +
          ", ".join(f"{counts.get(k, 0)} {k}" for k in ("tested", "untested", "missing", "setting")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
