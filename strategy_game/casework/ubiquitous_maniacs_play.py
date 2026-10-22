"""Terminal runner for the optional Ubiquitous Maniacs NoöPunk case.

Run: python -m strategy_game.casework.ubiquitous_maniacs_play
Only public CaseSession methods are used; this is not a second rules engine.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from .session import CaseworkError, load_session
from .ubiquitous_maniacs import CASE, build_session


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=CASE.title)
    parser.add_argument("--seed", type=int, default=502)
    parser.add_argument("--save", type=Path, default=Path("ubiquitous-maniacs-save.json"))
    parser.add_argument("--new", action="store_true")
    args = parser.parse_args(argv)
    if args.save.exists() and not args.new:
        try:
            session = load_session(args.save, CASE)
        except (ValueError, CaseworkError) as exc:
            parser.error(f"cannot resume saved case: {exc}")
    else:
        session = build_session(seed=args.seed)
    print(CASE.title)
    print(CASE.hook)
    print("Commands: help, status, act SEAT ACTION, next, assemble, resolve ID, save, quit")
    while not session.finished:
        scene = session.scene_spec
        print(f"\n{scene.title} | {scene.location}\n{scene.prose}")
        print("Actions:")
        for action in scene.actions:
            print(f"  {action.id}: {action.label}")
        try:
            command = input("> ").strip().split()
        except EOFError:
            command = ["quit"]
        if not command:
            continue
        try:
            if command[0] == "quit":
                session.save(args.save)
                print(f"Saved to {args.save}")
                return 0
            if command[0] == "save":
                session.save(args.save)
                print(f"Saved to {args.save}")
            elif command[0] == "help":
                print("Use one seat once per scene: pc_leader, laura_falk, "
                      "harri_romppainen, sebastian_virtanen, laura_univaara.")
                print("Resolve with closed_by_evidence or closed_by_withdrawal.")
            elif command[0] == "status":
                print(session.report())
            elif command[0] == "act" and len(command) == 3:
                result = session.act(command[1], command[2])
                print(result)
            elif command[0] == "next":
                print("Next scene:", session.end_scene())
            elif command[0] == "assemble":
                print(session.assemble("finding-ward"))
            elif command[0] == "resolve" and len(command) == 2:
                print(session.resolve(command[1]))
                session.save(args.save)
            else:
                print("Unknown command; type help.")
        except (CaseworkError, ValueError) as exc:
            print("Cannot do that:", exc)
    print("Case closed; campaign record saved to", args.save)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
