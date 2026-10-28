#!/usr/bin/env python3
"""Exact 2d6 calibration for the optional narrative layer (#689, #229).

The aspect layer's two safety rules - *one ladder step per aspect* and *one invoke per
roll* - were justified by arithmetic measured on **4dF**, and that kernel has been
retired in favour of the Without Number `2d6` check (ruling 2026-10-26). The rules may
still be right; the derivation no longer applies. This script measures the same
quantities on the real kernel, by exact enumeration rather than simulation, so the
numbers are stable and reviewable.

It computes nothing about play - only the probability that a check succeeds at a given
difficulty with 0..+4 of aspect bonus, and what each step of bonus is worth.

Usage:
    python tools/narrative_layer_2d6_calibration.py [--json OUT]
"""
from __future__ import annotations

import argparse
import json
from itertools import product

DIFFICULTIES = (6, 8, 10, 12, 14)


def distribution() -> dict[int, float]:
    """The exact 2d6 distribution: 36 equiprobable outcomes, summed."""
    counts: dict[int, int] = {}
    for first, second in product(range(1, 7), repeat=2):
        total = first + second
        counts[total] = counts.get(total, 0) + 1
    return {total: count / 36 for total, count in sorted(counts.items())}


def success_probability(bonus: int, difficulty: int, dist: dict[int, float]) -> float:
    """P(2d6 + bonus >= difficulty). A check succeeds on meeting the difficulty."""
    return sum(p for total, p in dist.items() if total + bonus >= difficulty)


def table() -> dict[int, dict[str, float]]:
    dist = distribution()
    out: dict[int, dict[str, float]] = {}
    for difficulty in DIFFICULTIES:
        base = success_probability(0, difficulty, dist)
        row: dict[str, float] = {"base": round(base * 100, 1)}
        for bonus in (1, 2, 3, 4):
            probability = success_probability(bonus, difficulty, dist)
            row[f"plus{bonus}"] = round(probability * 100, 1)
            row[f"shift{bonus}"] = round((probability - base) * 100, 1)
        out[difficulty] = row
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=str, default=None)
    args = parser.parse_args(argv)

    data = table()
    header = "DV |  +0    +1    +2    +3    +4   | shift at +1 / +2 / +4 (pp)"
    print("Exact 2d6 aspect-bonus calibration")
    print(header)
    print("-" * len(header))
    for difficulty, row in data.items():
        print(f"{difficulty:2} | {row['base']:5.1f} {row['plus1']:5.1f} {row['plus2']:5.1f} "
              f"{row['plus3']:5.1f} {row['plus4']:5.1f}   | "
              f"{row['shift1']:+5.1f} {row['shift2']:+5.1f} {row['shift4']:+5.1f}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
