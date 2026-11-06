"""Command-line demonstration for the standalone social-science simulator (#1286).

Run:

    python -m social_science --seed 7 --turns 8 --out /tmp/social-science-run.json
    python -m social_science --seed 7 --intervention

No CWN, Evennia, NoöPunk RPG data or LLM is required.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .export import write_run
from .metrics import simulation_metrics
from .scenario import build_synthetic_scenario


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the synthetic NoöPunk social-science simulator."
    )
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--turns", type=int, default=8)
    parser.add_argument(
        "--intervention", action="store_true", help="run the intervention fixture"
    )
    parser.add_argument(
        "--out", type=Path, default=None, help="write the full run JSON here"
    )
    args = parser.parse_args(argv)

    simulation = build_synthetic_scenario(
        seed=args.seed, turns=args.turns, intervention=args.intervention
    )
    simulation.run()
    metrics = simulation_metrics(simulation)
    summary = {
        "seed": args.seed,
        "turns": simulation.turn,
        "intervention": bool(args.intervention),
        "events": metrics["events"]["total"],
        "event_kinds": metrics["events"]["by_kind"],
        "social_edges": metrics["graphs"]["social"]["edges"],
        "communication_edges": metrics["graphs"]["communication"]["edges"],
        "synthetic": True,
    }
    if args.out:
        write_run(args.out, simulation)
        summary["output"] = str(args.out)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
