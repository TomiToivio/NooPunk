"""Conservative, reproducible MUD CWN implementation audit (#1025).

Presence of a Python module is evidence of code, NEVER proof of source parity,
command wiring, persistence or playtest. More rows are required to exhaust the
Free Edition PDF; until individually reviewed, they stay unverified.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    "character_creation": {
        "rules": ["src/rules/cwn_character.py", "src/rules/cwn_backgrounds.py",
                  "src/rules/cwn_edges_foci.py"],
        "mud": ["mud/nopunk_mud/cwn_core.py"],
        "test": ["tests/test_cwn_character.py", "mud/tests/test_cwn_character.py"],
        "command": [],
    },
    "advancement": {
        "rules": ["src/rules/cwn_advancement.py"],
        "mud": [], "test": ["tests/test_cwn_advancement.py"], "command": [],
    },
    "skill_checks_saves": {
        "rules": ["src/rules/cwn_core.py"],
        "mud": ["mud/nopunk_mud/cwn_core.py"],
        "test": ["mud/tests/test_cwn_core.py"], "command": ["mud/commands/default_cmdsets.py"],
    },
    "combat_trauma_shock": {
        "rules": ["src/rules/cwn_combat.py", "src/rules/cwn_trauma.py"],
        "mud": ["mud/nopunk_mud/cwn/combat.py"],
        "test": ["mud/tests/test_cwn_combat.py"], "command": [],
    },
    "initiative_actions": {
        "rules": ["src/rules/cwn_initiative.py", "src/rules/cwn_combat_actions.py"],
        "mud": ["mud/nopunk_mud/cwn/initiative.py"],
        "test": ["mud/tests/test_cwn_initiative_950.py"], "command": [],
    },
    "injuries_healing_strain": {
        "rules": ["src/rules/cwn_injury_procedure.py", "src/rules/cwn_healing.py",
                  "src/rules/cwn_strain.py"],
        "mud": [], "test": ["tests/test_cwn_healing.py"], "command": [],
    },
    "equipment_encumbrance_crafting": {
        "rules": ["src/rules/cwn_equipment.py", "src/rules/cwn_encumbrance.py",
                  "src/rules/cwn_gear_mods.py"],
        "mud": [], "test": ["tests/test_cwn_equipment.py"], "command": [],
    },
    "cyberware_installation_alienation": {
        "rules": [], "mud": [], "test": [], "command": [],
    },
    "hacking_programs_security": {
        "rules": ["src/rules/cwn_hacking.py", "src/rules/cwn_program_catalogue.py"],
        "mud": [], "test": ["tests/test_cwn_hacking.py"], "command": [],
    },
    "drones_vehicles_chases": {
        "rules": ["src/rules/cwn_drones.py", "src/rules/cwn_vehicles.py"],
        "mud": [], "test": ["tests/test_cwn_drones.py"], "command": [],
    },
    "npc_morale_reactions": {
        "rules": [], "mud": [], "test": [], "command": [],
    },
    "heat_missions_gm_generation": {
        "rules": [], "mud": [], "test": [], "command": [],
    },
}

def build(root: Path = ROOT) -> dict:
    rows = []
    for family, evidence in FAMILIES.items():
        present = {key: [path for path in paths if (root / path).is_file()]
                   for key, paths in evidence.items()}
        # This classification is an inventory, NOT a parity claim.
        rows.append({
            "family": family,
            "source_pdf_reviewed": False,
            "source_srd_reviewed": False,
            "book_page": None,
            "rules_code_paths": present["rules"],
            "mud_code_paths": present["mud"],
            "test_paths": present["test"],
            "command_candidates": present["command"],
            "in_game_command_verified": False,
            "persisted_state_verified": False,
            "book_example_verified": False,
            "playtest_verified": False,
            "status": "unverified",
            "missing_candidate_paths": {
                k: [p for p in v if p not in present[k]] for k, v in evidence.items()
            },
        })
    return {
        "schema": "noopunk.cwn.mud-parity-audit",
        "issue": 1025,
        "scope": "Free Edition PDF + SRD; this is a family-level bootstrap, not chapter parity",
        "total_families": len(rows),
        "verified_complete": 0,
        "families": rows,
    }

def markdown(report: dict) -> str:
    lines = [
        "# CWN Free Edition → Evennia MUD parity audit (#1025)",
        "",
        "**This is a preliminary inventory, not full book parity.** File existence",
        "and repository tests do not demonstrate rules accuracy, a usable command,",
        "persistent state, or gameplay. Source page references must be filled only",
        "after a human/agent checks the Free Edition PDF and SRD.",
        "",
        "| Area | Rules code found | MUD code found | Tests found | Book verified | Playable verified |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in report["families"]:
        lines.append(f'| `{row["family"]}` | {len(row["rules_code_paths"])} | '
                     f'{len(row["mud_code_paths"])} | {len(row["test_paths"])} | No | No |')
    lines += ["", "Generate the current inventory: `python3 tools/cwn_mud_parity_1025.py --markdown`.",
              "Machine-readable audit: `python3 tools/cwn_mud_parity_1025.py`.",
              "The complete PDF chapter/procedure mapping, book examples and real Evennia",
              "end-to-end checks remain **open**. No checked-off family until all evidence exists.",
              "", "References: #1025, #950, #1006; `data/rules/overlay_registry.json`."]
    return "\n".join(lines) + "\n"

def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args(argv)
    result = build()
    print(markdown(result) if args.markdown else json.dumps(result, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
