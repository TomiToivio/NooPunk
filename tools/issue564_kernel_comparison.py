"""Kernel comparison for issue #564 — measure the three candidate core checks, do not pick one.

Queue row **D40 / issue #566** asks which kernel NoöPunk's playable rules should use. That question
has only ever been argued from familiarity. This module makes it measurable: it enumerates the exact
distribution of each candidate and reports the four quantities a ruling actually turns on —

* **what one point of competence is worth** (percentage points of success, and how that varies),
* **how wide the uncertain band is** (the number of difficulty steps where success is neither
  certain nor hopeless),
* **how often an extreme happens** (the tails that decide whether a master can fail and a novice can
  luck out),
* and **where the same feel lands** on each kernel's own ladder.

The three kernels, each taken from its published source:

**A — layer A, legacy NoöPunk.** `STAT + Skill + 1d10 ≥ DV`, both ratings 1..10
(`src/rules/core.py`, `data/rules/core.json`); DV ladder 9 / 13 / 15 / 17 / 21 / 24 / 29.

**W — the Without Number family.** `2d6 + attribute modifier + skill level ≥ difficulty`, attribute
modifier −2..+2, skill level 0..4, difficulty 6 / 8 / 10 / 12 / 14+
(<https://cwn.quadrifons.com/rules-of-the-game/skill-checks/>; identical in WWN and AWN).

**F — layer B, the crossover.** `4dF + skill` against opposition, four outcome bands
(`strategy_game/rpg/fate.py`; success with style at +3, success at +1, tie at 0, failure below).

Everything is exact enumeration over `fractions.Fraction`: no sampling, no seed, no run-to-run
variation. Nothing here approves a kernel — `IS_CANONICAL = False`, and D40 stays the author's.

Usage::

    python3 tools/issue564_kernel_comparison.py
    python3 tools/issue564_kernel_comparison.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Mapping

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.rules import core as layer_a_core  # noqa: E402  (path set above)

#: Not canon, not a proposal. A measurement.
IS_CANONICAL = False

#: Layer A's authored DV ladder, read from the canonical core (never re-declared here).
LAYER_A_LADDER: tuple[int, ...] = tuple(layer_a_core.DIFFICULTY_LADDER)

#: The Without Number ladder, read from the CWN SRD's "Difficulty Levels" table.
WN_LADDER: tuple[int, ...] = (6, 8, 10, 12, 14)

#: Fate's four bands, as `strategy_game/rpg/fate.py` applies them (shifts, most severe first).
FATE_BANDS: tuple[tuple[int, str], ...] = (
    (3, "success with style"),
    (1, "success"),
    (0, "tie — succeed at a minor cost"),
)


# --------------------------------------------------------------------------- #
# Dice: exact distributions
# --------------------------------------------------------------------------- #

def d_sums(count: int, sides: int) -> Counter[int]:
    """Exact distribution of `count`d`sides`, by enumeration."""
    sums: Counter[int] = Counter({0: 1})
    for _ in range(count):
        nxt: Counter[int] = Counter()
        for total, n in sums.items():
            for face in range(1, sides + 1):
                nxt[total + face] += n
        sums = nxt
    return sums


def fate_sums() -> Counter[int]:
    """4dF: each die is −1 / 0 / +1, so the totals run −4..+4 with a triangular bell."""
    return Counter({-4: 1, -3: 4, -2: 10, -1: 16, 0: 19, 1: 16, 2: 10, 3: 4, 4: 1})


#: The three candidates. `ladder` is None for Fate, whose difficulty is the opposition itself.
KERNELS: dict[str, dict] = {
    "layer_a_1d10": {
        "label": "layer A — STAT + Skill + 1d10 vs DV",
        "dice": d_sums(1, layer_a_core.CHECK_DICE_SIDES),
        "ladder": list(LAYER_A_LADDER),
        "bonus_label": "STAT + Skill",
        "bonus_typical": 10,  # 5 + 5: a competent professional on the 1..10 scales
        "bonus_range": (2, 20),
    },
    "wn_2d6": {
        "label": "Without Number — 2d6 + attribute modifier + skill level vs difficulty",
        "dice": d_sums(2, 6),
        "ladder": list(WN_LADDER),
        "bonus_label": "attribute modifier + skill level",
        "bonus_typical": 2,  # +1 attribute, skill-1
        "bonus_range": (-2, 6),
    },
    "fate_4dF": {
        "label": "layer B — 4dF + skill vs opposition",
        "dice": fate_sums(),
        "ladder": None,
        "bonus_label": "Fate skill rating",
        "bonus_typical": 3,  # a Fate "Good" skill
        "bonus_range": (-1, 8),
    },
}


# --------------------------------------------------------------------------- #
# The quantities a ruling turns on
# --------------------------------------------------------------------------- #

def success_probability(kernel: str, bonus: int, target: int) -> Fraction:
    """P(success) for `bonus` against `target`, exactly.

    Fate counts a tie as a success at a minor cost, because that is what its band table says; the
    strict-success figure is reported separately by `fate_bands_at`.
    """
    dice = KERNELS[kernel]["dice"]
    need = target - bonus
    total = sum(dice.values())
    hits = sum(n for value, n in dice.items() if value >= need)
    return Fraction(hits, total)


def delta_curve(kernel: str, deltas: Iterable[int] | None = None) -> dict[int, Fraction]:
    """P(success) as a function of `bonus − target`, the kernel's intrinsic shape.

    This is the only fair cross-kernel comparison: the ladders and scales differ, but the *shape* of
    "how much better am I than the task" is comparable. Note the axis is shifted per kernel by the
    die's own minimum: with `1d10` a character whose bonus equals the target succeeds on every roll,
    so the contested region is `delta ≤ −2`, not `delta = 0`.
    """
    if deltas is None:
        deltas = range(-14, 3)
    dice = KERNELS[kernel]["dice"]
    total = sum(dice.values())
    out: dict[int, Fraction] = {}
    for delta in deltas:
        hits = sum(n for value, n in dice.items() if value >= -delta)
        out[delta] = Fraction(hits, total)
    return out


def uncertain_window(kernel: str) -> tuple[int, int]:
    """The first and last `delta` at which success is neither impossible nor certain."""
    curve = delta_curve(kernel, range(-20, 4))
    contested = [delta for delta, p in curve.items() if 0 < p < 1]
    if not contested:
        raise ValueError(f"{kernel} has no contested region")
    return min(contested), max(contested)


def marginal_gain(kernel: str, delta: int) -> Fraction:
    """What one point of competence buys at `delta` — the number that decides the game's feel."""
    curve = delta_curve(kernel, (delta, delta + 1))
    return curve[delta + 1] - curve[delta]


def uncertain_width(kernel: str, *, low: Fraction = Fraction(1, 20), high: Fraction = Fraction(19, 20)) -> int:
    """How many consecutive `delta` steps are neither hopeless nor certain."""
    curve = delta_curve(kernel, range(-12, 13))
    return sum(1 for p in curve.values() if low < p < high)


def tail_probabilities(kernel: str, bonus: int, target: int) -> dict[str, Fraction]:
    """The extremes: the best outcome, and how often the worst one happens."""
    dice = KERNELS[kernel]["dice"]
    need = target - bonus
    total = sum(dice.values())
    best, worst = max(dice), min(dice)
    return {
        "best_outcome": Fraction(dice[best], total),
        "worst_outcome": Fraction(dice[worst], total),
        "certain": Fraction(1) if worst >= need else Fraction(0),
        "impossible": Fraction(1) if best < need else Fraction(0),
    }


def fate_bands_at(skill: int, opposition: int) -> dict[str, Fraction]:
    """Fate's four bands for `4dF + skill` vs `opposition`."""
    dice = fate_sums()
    total = sum(dice.values())
    counts: Counter[str] = Counter()
    for shift, n in dice.items():
        margin = skill + shift - opposition
        band = "failure"
        for threshold, name in FATE_BANDS:
            if margin >= threshold:
                band = name
                break
        counts[band] += n
    return {band: Fraction(n, total) for band, n in counts.items()}


def success_curve(kernel: str, bonus: int) -> list[dict]:
    """P(success) at every rung of the kernel's own ladder."""
    ladder = KERNELS[kernel]["ladder"]
    if ladder is None:  # Fate: the "ladder" is the opposition, sampled across a plausible spread
        ladder = list(range(0, 9))
    return [{
        "target": target,
        "probability": float(success_probability(kernel, bonus, target)),
        "certain": success_probability(kernel, bonus, target) == 1,
        "impossible": success_probability(kernel, bonus, target) == 0,
    } for target in ladder]


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def build_report() -> dict:
    kernels = {}
    for name, spec in KERNELS.items():
        typical = spec["bonus_typical"]
        low, high = uncertain_window(name)
        curve = delta_curve(name, range(low - 1, high + 2))
        gains = {delta: float(marginal_gain(name, delta)) for delta in range(low, high)}
        midpoint = (low + high) // 2
        kernels[name] = {
            "label": spec["label"],
            "bonus_typical": typical,
            "bonus_range": list(spec["bonus_range"]),
            "ladder": spec["ladder"],
            "ladder_curve": success_curve(name, typical),
            "contested_window": [low, high],
            "delta_curve": {delta: float(p) for delta, p in curve.items()},
            "marginal_gain": gains,
            "gain_at_midpoint": float(marginal_gain(name, midpoint)),
            "best_gain": max(gains.values()),
            "worst_gain": min(gains.values()),
            "uncertain_width": uncertain_width(name),
            "tails_typical": {k: float(v) for k, v in
                              tail_probabilities(name, typical,
                                                 (spec["ladder"] or [0])[1] if spec["ladder"] else 2).items()},
        }
    return {
        "format": "noopunk.issue564.kernel_comparison",
        "version": 1,
        "issue": [564, 566],
        "is_canonical": False,
        "method": "exact enumeration over fractions.Fraction; no sampling",
        "kernels": kernels,
        "fate_bands_typical": {k: float(v) for k, v in
                               fate_bands_at(KERNELS["fate_4dF"]["bonus_typical"], 2).items()},
    }


def format_report(report: Mapping) -> str:
    lines = ["Kernel comparison — issue #564 / D40 (exact enumeration; not canon)\n"]
    for name, k in report["kernels"].items():
        lines.append(f"{k['label']}")
        low, high = k["contested_window"]
        lines.append(
            f"  typical bonus {k['bonus_typical']} (range {k['bonus_range'][0]}..{k['bonus_range'][1]}), "
            f"ladder {k['ladder']}, contested deltas {low}..{high}"
        )
        lines.append("  P(success) by 'bonus − target' across the contested band:")
        row = "  ".join(f"{d:+d}:{p * 100:4.0f}%" for d, p in k["delta_curve"].items())
        lines.append("   " + row)
        lines.append(
            f"  one point of competence buys {k['worst_gain'] * 100:.1f}–{k['best_gain'] * 100:.1f} "
            f"points (at the midpoint {k['gain_at_midpoint'] * 100:.1f}); "
            f"5–95% band = {k['uncertain_width']} steps"
        )
        if k["ladder"]:
            curve = "  ".join(f"{c['target']}:{c['probability'] * 100:4.0f}%" for c in k["ladder_curve"])
            lines.append(f"  at its own ladder: {curve}")
        lines.append("")
    bands = report["fate_bands_typical"]
    lines.append("Layer B's four bands at a typical contest (4dF + 3 vs 2):")
    lines.append("   " + ", ".join(f"{b} {p * 100:.1f}%" for b, p in bands.items()))
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="emit the report as JSON")
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = build_report()
    print(json.dumps(report, indent=2) if args.json else format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
