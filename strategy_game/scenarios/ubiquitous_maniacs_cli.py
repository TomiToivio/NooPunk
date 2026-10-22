"""Play Ubiquitous Maniacs through the shared NoöPunk Fate RPG kernel."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ubiquitous_maniacs import UbiquitousManiacs, ScenarioError, cast


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NoöPunk RPG: Ubiquitous Maniacs")
    parser.add_argument("--save", type=Path, default=Path("ubiquitous_maniacs_save.json"))
    parser.add_argument("--new", action="store_true", help="start a new scenario instead of loading a save")
    args = parser.parse_args(argv)
    try:
        session = (UbiquitousManiacs.from_dict(json.loads(args.save.read_text(encoding="utf-8")))
                   if args.save.exists() and not args.new else UbiquitousManiacs())
    except (OSError, json.JSONDecodeError, ScenarioError, KeyError, TypeError) as exc:
        parser.error(f"cannot load save: {exc}")

    def save() -> None:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        temp = args.save.with_name(args.save.name + ".tmp")
        temp.write_text(json.dumps(session.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(args.save)

    print("NoöPunk RPG / Ubiquitous Maniacs")
    print("Cast:", ", ".join(f"{actor.id} ({actor.name})" for actor in cast().values()))
    while not session.finished:
        scene = session.view()
        print(f"\nDay {scene['day']} / {scene['stage']}\n{scene['text']}")
        print("Choices:", ", ".join(scene["choices"]))
        print("Commands: check <actor> <skill> <difficulty> <seed>, quit")
        try:
            raw = input("> ").strip()
        except EOFError:
            save()
            return 0
        if raw in {"quit", "exit"}:
            save()
            return 0
        try:
            parts = raw.split()
            if len(parts) == 5 and parts[0] == "check":
                print(session.attempt(parts[1], parts[2], int(parts[3]), int(parts[4])))
            else:
                session.choose(raw)
            save()
        except (ScenarioError, ValueError) as exc:
            print("Not available:", exc)
    save()
    print("\nScenario complete. Record saved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
