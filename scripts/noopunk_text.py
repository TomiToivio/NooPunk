#!/usr/bin/env python3
"""Run the local NoöPunk text RPG/Simulation.

The default scenario is the small canonical pre-Fall issue #60 vertical slice.
The earlier fixture scenario remains available with --scenario fixture for
regression testing. LLM use is optional.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simulation.sqlite_store import connect
from text_game.actions import parse_command
from text_game.actors import PatrolController, build_ollama_controller_from_env
from text_game.engine import GameEngine
from text_game.model import FIXTURE_PREFIX, fixture_world
from text_game.issue74 import (
    ANALYST_ID as ISSUE74_ANALYST_ID,
    HUMAN_ID as ISSUE74_HUMAN_ID,
    issue74_world,
)
from text_game.prefall import (
    HUMAN_ID as PREFALL_HUMAN_ID,
    MARS_ARCHIVE_ID,
    STARGATE_ANALYST_ID,
    prefall_world,
)
from text_game.persistence import load_game, save_game


FIXTURE_HUMAN_ID = FIXTURE_PREFIX + "human"
WANDERER_ID = FIXTURE_PREFIX + "wanderer"
LLM_CONTACT_ID = FIXTURE_PREFIX + "llm-contact"
LLM_PLAYER_ID = FIXTURE_PREFIX + "llm-player"


def _admin(engine: GameEngine, raw: str) -> str:
    command = raw.strip().casefold()
    if command == "gm state":
        return str(engine.world.to_dict())
    if command == "gm events":
        return "\n".join(event.to_json() for event in engine.events) or "(no events)"
    if command == "gm actors":
        return "\n".join(
            f"{actor.actor_id}: room={actor.room_id} controller={actor.controller}"
            for actor in sorted(engine.world.actors.values(), key=lambda a: a.actor_id)
        )
    return "GM commands: gm state | gm events | gm actors"


def _build_engine(args: argparse.Namespace) -> tuple[GameEngine, object | None, str]:
    connection = connect(args.db) if args.db else connect(":memory:")
    llm = build_ollama_controller_from_env() if args.ollama else None

    if args.scenario == "fixture":
        human_id = FIXTURE_HUMAN_ID
        world = fixture_world()
        controllers = {
            WANDERER_ID: PatrolController(
                route={
                    FIXTURE_PREFIX + "hub": "east",
                    FIXTURE_PREFIX + "side": "west",
                }
            )
        }
        if llm is not None:
            controllers[LLM_CONTACT_ID] = llm
            controllers[LLM_PLAYER_ID] = llm
    elif args.scenario == "issue74":
        human_id = ISSUE74_HUMAN_ID
        world = issue74_world()
        controllers = {}
        if llm is not None:
            controllers[ISSUE74_ANALYST_ID] = llm
    else:
        human_id = PREFALL_HUMAN_ID
        world = prefall_world()
        controllers = {}
        if llm is not None:
            controllers[STARGATE_ANALYST_ID] = llm
            controllers[MARS_ARCHIVE_ID] = llm

    if args.load:
        engine = load_game(
            args.load,
            connection=connection,
            controllers=controllers,
            gm_controller=llm if args.llm_gm else None,
        )
    else:
        engine = GameEngine(
            world=world,
            connection=connection,
            controllers=controllers,
            gm_controller=llm if args.llm_gm else None,
        )
    return engine, llm, human_id


def main() -> int:
    parser = argparse.ArgumentParser(description="NoöPunk local text RPG/Simulation")
    parser.add_argument(
        "--scenario",
        choices=("prefall", "issue74", "fixture"),
        default="prefall",
        help="Scenario to run (issue74 is the tiny Concordia/EP2 proof of concept)",
    )
    parser.add_argument("--db", default="", help="SQLite event-log path (default: in-memory)")
    parser.add_argument("--load", default="", help="Load JSON save")
    parser.add_argument("--save", default="noopunk-save.json", help="Default JSON save path")
    parser.add_argument("--ollama", action="store_true", help="Enable optional Ollama/Concordia actors")
    parser.add_argument("--llm-gm", action="store_true", help="Use the Ollama controller for brief GM narration")
    args = parser.parse_args()

    if args.llm_gm and not args.ollama:
        parser.error("--llm-gm requires --ollama")

    engine, llm, human_id = _build_engine(args)

    print("NoöPunk local text RPG/Simulation")
    if args.scenario == "prefall":
        print("Scenario: alternate Eclipse Phase timeline, pre-Fall, 20XX, Earth intact.")
    elif args.scenario == "issue74":
        print("Scenario: issue #74 Concordia + EP2 proof of concept, 20XX.")
    else:
        print("Scenario: non-canonical regression fixture.")
    print(
        "Commands: look, go <direction>, n/s/e/w, inventory, take, drop, talk, say, "
        "use, stats, sheet, test skill|social|mesh|combat ..."
    )
    print("Meta: save [path], load <path>, gm state|events|actors, quit")
    if not args.ollama:
        print("LLM disabled. Scripted contacts remain active; optional LLM contacts are inert.")
    print()
    print(engine.describe_room(human_id))

    while True:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue

        lowered = raw.casefold()
        if lowered in {"quit", "exit"}:
            break
        if lowered.startswith("gm "):
            print(_admin(engine, raw))
            continue
        if lowered == "save" or lowered.startswith("save "):
            path = raw[5:].strip() or args.save
            save_game(engine, path)
            print(f"Saved: {path}")
            continue
        if lowered.startswith("load "):
            path = raw[5:].strip()
            if not path:
                print("load requires a path")
                continue
            engine = load_game(
                path,
                connection=engine.connection,
                controllers=engine.controllers,
                gm_controller=engine.gm_controller,
            )
            print(f"Loaded: {path}")
            print(engine.describe_room(human_id))
            continue

        try:
            action = parse_command(human_id, raw, source="system")
            result = engine.execute(action)
        except ValueError as exc:
            if llm is None:
                print(f"Error: {exc}")
                continue
            try:
                action = llm.interpret_intent(
                    actor_id=human_id,
                    intent=raw,
                    context=engine.context_for(human_id),
                )
                print(f"[intent → {action.raw}]")
                result = engine.execute(action)
            except Exception as llm_exc:
                print(f"Error: {exc}; intent parser also failed: {llm_exc}")
                continue

        print(result.text)

        narration = engine.gm_narration(result)
        if narration:
            print(f"GM: {narration}")

        for actor_id, background_result in engine.run_background_once():
            actor = engine.world.actors[actor_id]
            print(f"[{actor.label}] {background_result.text.splitlines()[0]}")

        if args.save:
            save_game(engine, args.save)

        if result.completed:
            print("Scenario objective completed. You may keep exploring or type quit.")

    if args.save:
        save_game(engine, args.save)
        print(f"Saved: {args.save}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
