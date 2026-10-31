"""Headless solo smoke: character, check, save — no LLM, no Mesa, no other players (#950).

This is the smallest thing that proves the pivot is real: a UNSA recruit is created from the CWN core, resolves
a check, and the world persists across a restart — using only the standard library.

    cd mud && python -m nopunk_mud.cli --demo
    cd mud && python -m nopunk_mud.cli --demo --save /tmp/nopunk-world.json
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from nopunk_mud import cwn
from nopunk_mud.campaign import CampaignEngine
from nopunk_mud.world_state import WorldState

#: A legal UNSA recruit: Academy graduate, middling in everything, trained where it matters.
RECRUIT = {
    "name": "rookie",
    "attributes": {"Strength": 10, "Dexterity": 12, "Constitution": 11,
                   "Intelligence": 13, "Wisdom": 10, "Charisma": 9},
    "skills": {"Administer": 1, "Notice": 1, "Talk": 0},
}


def demo(save_path: Path | None = None) -> dict:
    """Run the smoke. Returns a report so a test can assert on it rather than on stdout."""
    character = cwn.create_character(RECRUIT["name"], attributes=RECRUIT["attributes"],
                                     skills=RECRUIT["skills"], background="UNSA Academy")

    state = WorldState.helsinki_opening()
    state.apply({"id": "join-1", "type": "join", "character": character.name, "room": "street"})
    state.apply({"id": "faction-1", "type": "faction_join", "character": character.name,
                 "faction": "unsa"})

    # A published check: Notice, routine difficulty, fixed dice so the smoke is reproducible.
    check = character.check("Notice", difficulty=cwn.DIFFICULTIES["routine"], dice=(3, 4))

    path = save_path or Path(tempfile.mkdtemp()) / "world.json"
    state.save(path)
    restored = WorldState.load(path)

    return {
        "character": character.name,
        "saves": character.saves(),
        "hp": character.max_hit_points(dice=(4,)),
        "strain": character.strain_capacity(),
        "check": {"total": check.total, "target": check.target, "success": check.success},
        "room": restored.room_of(character.name),
        "faction": restored.characters[character.name]["faction"],
        "persisted": path.exists(),
        "llm_calls": 0,
        "other_players": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="NoöPunk MUD headless smoke")
    parser.add_argument("--demo", action="store_true", help="run the solo smoke")
    parser.add_argument("--save", type=Path, default=None)
    parser.add_argument("--campaign", action="store_true",
                        help="play the solo UNSA case (interactive; stdin is a command per line)")
    parser.add_argument("--script", default="",
                        help="run a comma-separated script instead of reading stdin")
    args = parser.parse_args()
    if args.campaign:
        engine = CampaignEngine()
        commands = ([part.strip() for part in args.script.split(",") if part.strip()]
                    if args.script else None)
        if commands is None:
            print(engine.command("look"))
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                if line in {"quit", "exit"}:
                    break
                print("\n" + engine.command(line))
                if engine.state.ending:
                    break
        else:
            for line in commands:
                print("> " + line)
                print(engine.command(line))
        print(json.dumps({"ending": engine.state.ending, "clues": engine.state.clues,
                          "hp": engine.state.hp, "turns": engine.state.turns}, indent=2))
        return 0 if engine.state.ending else 1
    if not args.demo:
        parser.print_help()
        return 2
    print(json.dumps(demo(args.save), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
