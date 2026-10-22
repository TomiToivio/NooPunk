"""Run the packaged case: ``python -m strategy_game.casework``.

Default output is reading text; ``--json`` prints the same run as one JSON object. The command plays
the case, prints what happened and what persisted, and writes a save file — no renderer, no engine
and no network are involved.

``--play`` is the same case, played by a human: an interactive prompt over the same ``CaseSession``
(see :mod:`strategy_game.casework.play`). The headless path is unchanged and stays the default.
"""
from __future__ import annotations

import argparse
import json
import sys

from .demo import APPROACHES, ROUTES, render_text, run_demo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m strategy_game.casework",
        description=(
            "Play the packaged, non-canonical investigation case and print what it changed "
            "(issue #502's RPG-first vertical slice). Headless by default; --play for a human."
        ),
    )
    parser.add_argument(
        "--route",
        choices=ROUTES,
        default="investigate",
        help="how to close the case headless: on the record, in the loading bay, or by referral",
    )
    parser.add_argument(
        "--approach",
        choices=APPROACHES,
        default="pressure",
        help="the confrontation's method: words or force (only used by --route confront)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="dice seed for the run (default: the route's own seed)"
    )
    parser.add_argument(
        "--save", default=None, help="where to write the save file (default: a temporary path)"
    )
    parser.add_argument("--json", action="store_true", help="print the run as JSON")
    parser.add_argument(
        "--play",
        action="store_true",
        help="play the case yourself at a prompt instead of running it headless",
    )
    parser.add_argument(
        "--new",
        action="store_true",
        help="with --play and --save: start a fresh morning even if the save file exists",
    )
    args = parser.parse_args(argv)

    if args.play:
        from .play import play

        if args.json:
            print(
                "case refused: --play writes a transcript, so it cannot also print one JSON "
                "document; drop --json, or read the record from casework.play.play() instead",
                file=sys.stderr,
            )
            return 2
        played = play(
            seed=args.seed,
            save_to=args.save,
            resume=not args.new,
        )
        return 2 if played.exit_reason == "refused" else 0

    try:
        result = run_demo(args.route, seed=args.seed, approach=args.approach, save_to=args.save)
    except ValueError as exc:
        print(f"case refused: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
