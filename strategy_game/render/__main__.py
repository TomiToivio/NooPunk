"""Draw the board as text.

    python -m strategy_game.render            # the Ukweli local slice (the only complete local content)
    python -m strategy_game.render --empty    # the empty scaffold, like `python -m strategy_game`
    python -m strategy_game.render --world w.json
    python -m strategy_game.render --cards    # append the character-card roster faces
    python -m strategy_game.render --json     # the MapProvider payload, for another renderer to draw

Standard library only and deterministic: no model client, no service, no account, and no rule is
read or applied. This is a *view* of declared state, so it can change without a gate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..characters import load_character_cards
from ..core import WorldState
from .redaction import emit, redact
from .text import LOCAL_SLICE_DATA, TextMapProvider, render_board_text, render_roster_text, state_from_local_slice


def build_state(args: argparse.Namespace) -> WorldState:
    """The state to draw: a file, the empty scaffold, or the local slice."""
    if args.world:
        # WorldState exposes from_json (core.py), not from_dict.
        return WorldState.from_json(Path(args.world).read_text(encoding="utf-8"))
    if args.empty:
        return WorldState()
    if LOCAL_SLICE_DATA.exists():
        return state_from_local_slice()
    return WorldState()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render the NoöPunk strategy board as text (a view, not a rule).")
    parser.add_argument("--world", help="a WorldState-shaped JSON file to draw")
    parser.add_argument("--empty", action="store_true", help="draw the empty scaffold state instead")
    parser.add_argument("--cards", action="store_true", help="append the character-card roster faces")
    parser.add_argument("--json", action="store_true", help="print the MapProvider payload instead of text")
    args = parser.parse_args(argv)

    state = build_state(args)
    if args.json:
        emit(json.dumps(TextMapProvider().describe(state), ensure_ascii=False, indent=2))
        return 0
    emit(render_board_text(state))
    if args.cards:
        print()
        emit(render_roster_text(load_character_cards()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
