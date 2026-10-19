"""Run the tactical mission spike headless: ``python -m strategy_game.tactical``.

Default output is reading text; ``--json`` prints the same run as one JSON object. Neither output
contains a drawing instruction — this command exists to show that the mission layer needs no renderer
to be played, tested and written into persistent state.
"""
from __future__ import annotations

import argparse
import json
import sys

from .demo import DEMO_SEED, render_text, run_demo
from .mission import MissionError, load_mission


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m strategy_game.tactical",
        description=(
            "Play the packaged, non-canonical spike mission headless and print what it changed. "
            "No renderer is imported and no engine is required (issue #515, technical spike)."
        ),
    )
    parser.add_argument("--seed", type=int, default=DEMO_SEED, help="dice seed for the run")
    parser.add_argument(
        "--mission", default=None, help="path to a mission JSON document (default: the packaged fixture)"
    )
    parser.add_argument("--json", action="store_true", help="print the run as JSON")
    args = parser.parse_args(argv)

    try:
        spec = load_mission(args.mission)
    except MissionError as exc:
        print(f"mission refused: {exc}", file=sys.stderr)
        return 2
    result = run_demo(spec, seed=args.seed)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(render_text(result))
    return 0 if result["mission"]["complete"] else 1


if __name__ == "__main__":  # pragma: no cover - exercised through ``main``
    raise SystemExit(main())
