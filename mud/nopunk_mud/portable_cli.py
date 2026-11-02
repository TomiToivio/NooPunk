"""Offline text reference adapter; run: python -m nopunk_mud.portable_cli."""
from __future__ import annotations

import argparse
from pathlib import Path

from .portable import Command, PortableSession

LOCATIONS = {
    "hq": "UNSA safehouse",
    "kurvi": "Kurvi",
    "university": "University of Helsinki",
}


def run(commands: list[str] | None = None, save: Path | None = None) -> PortableSession:
    session = PortableSession.restore(save) if save and save.exists() else PortableSession()
    print(session.describe())
    iterator = iter(commands) if commands is not None else None
    while True:
        try:
            raw = next(iterator) if iterator is not None else input("UNSA> ")
        except (EOFError, StopIteration):
            break
        text = raw.strip().lower()
        if text in {"quit", "exit"}:
            break
        if text == "help":
            print("Commands: accept hq, interview kurvi, records university, "
                  "report hq, submit hq, status hq, quit")
            continue
        parts = text.split(maxsplit=1)
        if len(parts) != 2 or parts[1] not in LOCATIONS:
            print("Use: <action> <hq|kurvi|university> (or help)")
            continue
        result = session.execute(Command(parts[0], LOCATIONS[parts[1]]))
        print(result.message)
        if save:
            session.save(save)
        if result.finished:
            break
    return session


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", type=Path)
    parser.add_argument("--script", help="semicolon-delimited commands")
    args = parser.parse_args()
    run(args.script.split(";") if args.script is not None else None, args.save)


if __name__ == "__main__":
    main()
