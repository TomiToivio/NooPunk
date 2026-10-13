"""Run the RPG layer's worked scene: ``python -m strategy_game.rpg``.

Prints the layer's demonstration as JSON by default — the Fate checks, the dice as they fell, the
outcome of each, what the table keeps, and what this layer excludes. ``--text`` prints the same report
as reading text.

This is the RPG layer's **own** entry point. The pinned key set of ``python -m strategy_game`` and the
pinned ``strategy_game.__all__`` are untouched by it: the package declares its own ``__all__``, and
nothing here is added to the scaffold's surface (#282 / #347 / #389).

    python -m strategy_game.rpg
    python -m strategy_game.rpg --text
    python -m strategy_game.rpg --seed 7
"""
from __future__ import annotations

import argparse
import json

from .run import DEFAULT_SEED, render_report, scene_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m strategy_game.rpg",
        description=(
            "The NoöPunk crossover RPG layer's worked scene: a cyber check and a PSI check through one "
            "seeded Fate engine, plus the two BCI netrunning examples. Noncanonical and illustrative; "
            "no strategy or political mechanic is computed."
        ),
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help=f"seeded RNG for every check (default {DEFAULT_SEED}); same seed, same scene")
    parser.add_argument("--text", action="store_true", help="print the report as text, not JSON")
    args = parser.parse_args(argv)

    report = scene_report(args.seed)
    if args.text:
        print(render_report(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
