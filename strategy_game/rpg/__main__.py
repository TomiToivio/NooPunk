"""Run the shared NoöPunk RPG engine or its integrated scenarios."""
from __future__ import annotations

import argparse
import json
from .run import DEFAULT_SEED, render_report, scene_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m strategy_game.rpg",
        description="NoöPunk RPG: Fate engine demos or an integrated playable scenario")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--text", action="store_true")
    parser.add_argument("--scenario", choices=("ubiquitous-maniacs",),
                        help="play a scenario with the same RPG Fate engine")
    parser.add_argument("--save", help="scenario save JSON path")
    parser.add_argument("--new", action="store_true", help="ignore an existing scenario save")
    args = parser.parse_args(argv)
    if args.scenario:
        from strategy_game.scenarios.ubiquitous_maniacs_cli import main as scenario_main
        forwarded = []
        if args.save:
            forwarded += ["--save", args.save]
        if args.new:
            forwarded.append("--new")
        return scenario_main(forwarded)
    if args.save or args.new:
        parser.error("--save and --new require --scenario")
    report = scene_report(args.seed)
    if args.text:
        print(render_report(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
