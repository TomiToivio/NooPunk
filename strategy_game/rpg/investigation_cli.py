"""Run the noncanonical #502 investigative RPG vertical slice."""
from __future__ import annotations

import argparse
from pathlib import Path
from .investigation import Investigation, InvestigationError, STAGES


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NoöPunk RPG-first example case (#502)")
    parser.add_argument("--save", type=Path, default=Path("noopunk_case.json"))
    args = parser.parse_args(argv)
    case = Investigation.load(args.save) if args.save.exists() else Investigation()
    print("NoöPunk / example case. PC: faction leader; party: faction agents.")
    while not case.finished:
        print("\n" + STAGES[case.stage]["prompt"])
        print("Available choices:", ", ".join(case.available()))
        print("Commands: party <ids>, check <id> <COG|INT|REF|SAV|SOM|WIL> <difficulty> <seed>, quit")
        try:
            raw = input("> ").strip()
        except EOFError:
            case.save(args.save)
            return 0
        if raw == "quit":
            case.save(args.save)
            return 0
        try:
            parts = raw.split()
            if parts and parts[0] == "party":
                case.party(parts[1:])
                print("Party:", ", ".join(case.participants))
            elif parts and parts[0] == "check" and len(parts) == 5:
                print(case.attempt(parts[1], parts[2], int(parts[3]), int(parts[4])))
            else:
                case.choose(raw)
                case.save(args.save)
        except (InvestigationError, ValueError) as exc:
            print("Not available:", exc)
    case.save(args.save)
    print("\nCase complete. The saved event ledger can feed later strategic adapters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
