"""Attribute check -mekaniikka: yksinkertainen d6 + attribute vs difficulty."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .state import ReceptionGame


@dataclass(frozen=True)
class CheckResult:
    success: bool
    roll: int
    total: int
    difficulty: int


def perform_check(
    game: ReceptionGame,
    attribute: str,
    difficulty: int,
    dice_sides: int = 6,
) -> CheckResult:
    """Heitä d6, lisää attribute, vertaa difficultyyn.

    Palauttaa CheckResultin. Ei muuta game-tilaa suoraan —
    kutsuja päättää mitä lopputuloksesta seuraa.
    """
    roll = random.randint(1, dice_sides)
    total = roll + game.player.get_attribute(attribute)
    success = total >= difficulty
    return CheckResult(
        success=success,
        roll=roll,
        total=total,
        difficulty=difficulty,
    )
