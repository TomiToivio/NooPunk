"""Experimental #200 probability lab. NOT the canonical rule resolver.

Independent mathematics only; no third-party rulebook expression is copied.
A trial compares existing flat 1d10 with four independently uniform {-1,0,+1}
dice (often called 4dF). Both use separate Attribute and Skill ratings.
The default Attribute+Skill mapping here is for comparative analysis only.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Literal, Mapping

from .core import STAT_LIST

Mode = Literal["d10", "four_fudge"]

DICE: dict[str, Mapping[int, Fraction]] = {
    "d10": {face: Fraction(1, 10) for face in range(1, 11)},
    "four_fudge": {
        total: Fraction(count, 81)
        for total, count in sorted(
            Counter(map(sum, product((-1, 0, 1), repeat=4))).items()
        )
    },
}


@dataclass(frozen=True)
class Trial:
    """Noncanonical check specification: rating bounds mirror the current core."""
    attribute: str
    stat: int
    skill: int
    target: int
    mode: Mode
    situational: int = 0

    def __post_init__(self) -> None:
        if self.attribute not in STAT_LIST:
            raise ValueError("Unknown canonical attribute")
        for name, value in (("stat", self.stat), ("skill", self.skill)):
            if type(value) is not int or not 1 <= value <= 10:
                raise ValueError(f"{name} must be an integer from 1 to 10")
        if type(self.target) is not int or type(self.situational) is not int:
            raise ValueError("target and situational must be integers")
        if self.mode not in DICE:
            raise ValueError("Unsupported experimental die mode")


def success_probability(trial: Trial) -> Fraction:
    """Exact, seed-free chance total >= target; no automatic critical rule."""
    base = trial.stat + trial.skill + trial.situational
    return sum(
        (chance for outcome, chance in DICE[trial.mode].items()
         if base + outcome >= trial.target),
        Fraction(0),
    )


def curve(mode: Mode, stat: int, skill: int, targets: range, attribute: str = "INT") -> tuple[Fraction, ...]:
    """Deterministic list for charts/tabletop comparison, no runtime mutation."""
    return tuple(success_probability(Trial(attribute, stat, skill, target, mode))
                 for target in targets)
