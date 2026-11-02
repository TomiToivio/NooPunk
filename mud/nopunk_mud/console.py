"""Plain-text console for the first UNSA investigation (#1053, Priority 0).

No Evennia, no Concordia, no Pygame, no LLM, no network. This is the interface the issue asks to exist *first*,
because a rules engine that can only run inside a MUD has not been separated from the MUD — it has been buried
in it.

    python -m nopunk_mud.console                 # interactive
    python -m nopunk_mud.console --script s.txt  # non-interactive, for tests and for CI
    python -m nopunk_mud.console --seed 7 --script s.txt

The console owns no rules. It reads a line, hands it to the campaign engine, prints what comes back, and knows
exactly four things the engine does not: how to read input, how to quit, and how to save or load a game to a
path the player names.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, TextIO

from nopunk_mud.campaign import CampaignEngine

BANNER = "NooPunk — UNSA Helsinki. Type 'help' for commands, 'quit' to leave."


class Console:
    """A thin shell over CampaignEngine. Deliberately thin: any rule here would be a rule in two places."""

    def __init__(self, *, seed: int = 7, out: TextIO | None = None) -> None:
        self.engine = CampaignEngine(seed=seed)
        self.out = out or sys.stdout
        self.quit = False

    def _print(self, text: str) -> None:
        print(text, file=self.out)

    def handle(self, line: str) -> None:
        command, _, argument = line.strip().partition(" ")
        command = command.casefold()

        if command in ("quit", "exit"):
            self.quit = True
            return
        if command == "save":
            if not argument.strip():
                self._print("Usage: save <path>")
                return
            self.engine.command(f"save {argument.strip()}")
            self._print(f"Saved to {argument.strip()}")
            return
        if command == "load":
            if not argument.strip():
                self._print("Usage: load <path>")
                return
            path = Path(argument.strip())
            if not path.is_file():
                self._print(f"No save at {path}")
                return
            import json
            self.engine = CampaignEngine.from_dict(json.loads(path.read_text(encoding="utf-8")))
            self._print(f"Loaded {path}")
            return
        if not command:
            return
        self._print(self.engine.command(line.strip()))

    def run(self, lines: Iterable[str]) -> None:
        for line in lines:
            if self.quit:
                return
            self.handle(line)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    seed = 7
    script: Path | None = None

    if "--seed" in argv:
        i = argv.index("--seed")
        try:
            seed = int(argv[i + 1])
        except (IndexError, ValueError):
            print("--seed needs an integer", file=sys.stderr)
            return 2
        del argv[i:i + 2]
    if "--script" in argv:
        i = argv.index("--script")
        try:
            script = Path(argv[i + 1])
        except IndexError:
            print("--script needs a path", file=sys.stderr)
            return 2
        del argv[i:i + 2]
    if argv:
        print(f"Unknown argument(s): {' '.join(argv)}", file=sys.stderr)
        return 2

    console = Console(seed=seed)
    console._print(BANNER)

    if script is not None:
        if not script.is_file():
            print(f"No such script: {script}", file=sys.stderr)
            return 2
        console.run(script.read_text(encoding="utf-8").splitlines())
        return 0

    try:
        while not console.quit:
            console._print("")
            line = input("> ")
            console.handle(line)
    except (EOFError, KeyboardInterrupt):
        console._print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
