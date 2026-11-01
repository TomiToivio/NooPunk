"""Subprocedure-level CWN → Evennia implementation backlog for epic #1025.

This is a *candidate* procedure inventory, not a book-complete TOC transcription.
A reviewer must confirm each reference against the Free Edition PDF before marking
source_verified. Source pages are intentionally null rather than guessed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Ordered by implementation dependency. Each entry is a reviewable procedure,
# not a claim that the existing Python code matches the copyrighted rulebook.
GROUPS = (
    ("01-character", "Character creation", (
        "Attribute generation and allocation", "Attribute modifiers",
        "Background choice and free skills", "Skill levels and initial skills",
        "Contacts and one-roll character tables", "Edge selection",
        "Focus selection and levels", "Focus gear budget", "Initial equipment",
        "Hit points and derived statistics", "Saving throws", "Final character sheet")),
    ("02-advancement", "Advancement", (
        "Experience awards", "Level thresholds and bonuses", "Skill point spending",
        "Focus progression", "Edge progression", "Character rebuild restrictions")),
    ("03-resolution", "Fundamental rules and time", (
        "Skill checks and difficulty", "Assistance and opposed checks",
        "Saving throw resolution", "Scene and mission time", "Combat round timing")),
    ("04-combat", "Combat", (
        "Initiative and combat order", "Combat action economy", "Movement and positioning",
        "Melee attacks", "Ranged and unarmed attacks", "Cover and range",
        "Ammunition and reloading", "Shock damage", "Trauma checks",
        "Special attacks and maneuvers", "Suppression", "Damage and armor",
        "Mortal injury and stabilization", "Healing and first aid",
        "Poisons and System Strain", "Major injuries")),
    ("05-gear", "Equipment and economy", (
        "Encumbrance and inventory", "Gear acquisition and availability",
        "Lifestyle and living costs", "Wages, bribes and services",
        "Weapon and armor item definitions", "Weapon and armor accessories",
        "Pharmaceuticals and drugs", "Crafting and modification",
        "Factory modifications and maintenance")),
    ("06-cyberware", "Cyberware", (
        "Cyberware installation and costs", "Installation risk and complications",
        "Cyberware System Strain", "Maintenance and removal",
        "Detection and concealment", "Skillplugs", "Cyberware modifications",
        "Alienation and consequences")),
    ("07-vehicles", "Vehicles and drones", (
        "Vehicle catalog and fittings", "Vehicle damage and combat",
        "Vehicle action economy", "Chases and pursuit",
        "Drone catalog and fittings", "Drone control and commands",
        "Drone damage and consequences")),
    ("08-hacking", "Hacking", (
        "Cyberdecks and capacity", "Cyberspace network structure",
        "Access permissions", "Cyberspace movement and time",
        "Hacking actions and costs", "Program acquisition and writing",
        "Subjects and verbs", "Program execution and limits",
        "Security countermeasures", "Demons and watchdogs",
        "Security escalation", "Persistent intrusion state")),
    ("09-npcs", "NPC and antagonist procedures", (
        "NPC stat blocks", "NPC templates and combatants",
        "Hackers and vehicle operators", "Cybered opponents and creatures",
        "Reaction rolls", "Morale checks", "Security response")),
    ("10-gm", "Missions and GM tools", (
        "Mission creation", "Mission types and tags", "Intrusion missions",
        "Mission reward and XP", "Heat", "Schemes and operators",
        "Megacorporation generators", "Gang generators",
        "District and city generators", "Faces on the Street generators",
        "Creating Your Dystopia generators", "The City procedures")),
    ("11-evennia", "MUD acceptance and persistence", (
        "Command wiring", "Character persistence", "Inventory persistence",
        "Combat reconnect and resume", "Hacking reconnect and resume",
        "Atomic state mutations", "Solo UNSA campaign integration",
        "Overlay-disabled vanilla rules tests")),
)

# Optional file hints are discovery leads, never evidence of correctness.
HINTS = {
    "01-character": ["src/rules/cwn_character.py", "mud/nopunk_mud/cwn_core.py"],
    "02-advancement": ["src/rules/cwn_advancement.py"],
    "03-resolution": ["src/rules/cwn_core.py", "src/rules/cwn_mission_time.py"],
    "04-combat": ["src/rules/cwn_combat.py", "mud/nopunk_mud/cwn/combat.py"],
    "05-gear": ["src/rules/cwn_equipment.py", "src/rules/cwn_encumbrance.py"],
    "06-cyberware": ["src/rules/cwn_strain.py"],
    "07-vehicles": ["src/rules/cwn_vehicles.py", "src/rules/cwn_drones.py"],
    "08-hacking": ["src/rules/cwn_hacking.py", "src/rules/cwn_program_catalogue.py"],
    "09-npcs": [],
    "10-gm": [],
    "11-evennia": ["mud/commands/default_cmdsets.py"],
}

def build(root: Path = ROOT) -> dict:
    rows = []
    for group, section, procedures in GROUPS:
        for position, procedure in enumerate(procedures, 1):
            rows.append({
                "id": f"{group}-{position:02d}",
                "section_candidate": section,
                "procedure_candidate": procedure,
                "pdf_page": None,
                "srd_url": None,
                "swnr_path": None,
                "source_verified": False,
                "rules_candidates": [path for path in HINTS[group] if (root / path).is_file()],
                "evennia_command": None,
                "tests": [],
                "implemented_verified": False,
                "command_wired_verified": False,
                "persistence_verified": False,
                "book_example_verified": False,
                "playtested": False,
                "status": "unverified",
                "disposition": "review source, then implement or document non-mechanical rationale",
            })
    return {
        "schema": "noopunk.cwn.procedure-backlog.v1",
        "scope": "Provisional issue-checklist breakdown; NOT an exhaustive verified Free Edition TOC",
        "issue": 1025,
        "source": "https://tesera.ru/images/items/2301450/CWN_Free_Version_081123.pdf",
        "srd": "https://cwn.quadrifons.com/",
        "swnr_reference": "https://github.com/wintersleepAI/swnr",
        "verified_complete": 0,
        "procedures": rows,
    }

def validate(report: dict, root: Path = ROOT) -> list[str]:
    errors = []
    seen = set()
    for row in report["procedures"]:
        key = row["id"]
        if key in seen:
            errors.append(f"{key}: duplicate identifier")
        seen.add(key)
        if row["status"] not in {"unverified", "partial", "complete", "missing", "not_applicable"}:
            errors.append(f"{key}: invalid status")
        for path in row["rules_candidates"] + row["tests"]:
            if not (root / path).is_file():
                errors.append(f"{key}: missing evidence file: {path}")
        if row["source_verified"] and not isinstance(row["pdf_page"], int):
            errors.append(f"{key}: verified source lacks PDF page")
        if row["status"] == "complete":
            required = ("source_verified", "implemented_verified", "command_wired_verified",
                        "persistence_verified", "book_example_verified", "playtested")
            if not all(row[field] for field in required) or not row["tests"] or not row["evennia_command"]:
                errors.append(f"{key}: unsupported complete claim")
        if row["status"] == "not_applicable" and not row["disposition"].strip():
            errors.append(f"{key}: non-mechanical exclusion requires justification")
    if report["verified_complete"] != sum(row["status"] == "complete" for row in report["procedures"]):
        errors.append("verified_complete count disagrees with rows")
    return errors

def markdown(report: dict) -> str:
    lines = [
        "# CWN Free Edition → Evennia procedure backlog (#1025)", "",
        "**Provisional checklist, not a verified transcription of the complete book.**",
        "PDF pages, SRD anchors, SWNR equivalents and command/test evidence remain",
        "unknown until individually checked. A filename is not a parity claim.", "",
        "| ID | Procedure candidate | PDF page | Evidence leads | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["procedures"]:
        leads = ", ".join(row["rules_candidates"]) or "none"
        lines.append(f'| {row["id"]} | {row["procedure_candidate"]} | '
                     f'{row["pdf_page"] or "unverified"} | {leads} | {row["status"]} |')
    lines.extend(["", "Verify the entire PDF table of contents and *all* subprocedures before",
                  "claiming exhaustive coverage. For each row, supply book page, SRD/SWNR",
                  "cross-checks, code, Evennia command, unit/golden tests, persistence",
                  "and playtest evidence. Do not close #1025 on this inventory alone."])
    return "\n".join(lines) + "\n"

def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args(argv)
    result = build()
    errors = validate(result)
    if errors:
        parser.error("; ".join(errors))
    print(markdown(result) if args.markdown else json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
