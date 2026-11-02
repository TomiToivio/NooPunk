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
from nopunk_mud.cli_console import MudConsole
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
    # Mission time is state, so the smoke proves it survives the same save/load as everything else.
    state.apply({"id": "time-1", "type": "advance_time", "minutes": 12})

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
        "minute": restored.clock().minute,
        "scene": restored.scene,
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
    parser.add_argument("--seed", type=int, default=7,
                        help="deterministic campaign seed (the same seed and commands replay exactly)")
    parser.add_argument("--load", type=Path, default=None,
                        help="resume a saved campaign; the case continues where it stopped")
    args = parser.parse_args()
    if args.campaign:
        # One console loop for both entry points: `nopunk_mud.cli_console` owns the shell, this reuses it
        # rather than keeping a second copy of the same read-print-persist cycle.
        console = MudConsole(seed=args.seed)
        if args.load:
            console.engine = CampaignEngine.from_dict(json.loads(args.load.read_text(encoding="utf-8")))
        save_file = args.save or args.load

        def persist() -> None:
            """Write after every command: a case closed by Ctrl-C is still resumable."""
            if save_file is not None:
                save_file.parent.mkdir(parents=True, exist_ok=True)
                save_file.write_text(json.dumps(console.engine.to_dict(), indent=2), encoding="utf-8")

        commands = ([part.strip() for part in args.script.split(",") if part.strip()]
                    if args.script else None)
        if commands is None:
            print(console.engine.command("look"))
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                if line in {"quit", "exit"}:
                    break
                console.handle(line)
                persist()
                if console.engine.state.ending:
                    break
        else:
            for line in commands:
                print("> " + line)
                console.handle(line)
                persist()
        persist()
        print(json.dumps({"ending": console.engine.state.ending, "clues": console.engine.state.clues,
                          "hp": console.engine.state.hp, "turns": console.engine.state.turns,
                          "seed": console.engine.state.seed,
                          "save": str(save_file) if save_file else None}, indent=2))
        return 0 if console.engine.state.ending else 1
    if not args.demo:
        parser.print_help()
        return 2
    print(json.dumps(demo(args.save), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
