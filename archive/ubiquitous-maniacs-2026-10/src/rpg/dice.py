"""Fate dice helpers shared by random play and deterministic tests."""

from __future__ import annotations

import random
from collections.abc import Callable


FateDie = Callable[[], int]


def roll_4df(fate_die: FateDie | None = None) -> tuple[int, int, int, int]:
    die = fate_die or (lambda: random.choice((-1, 0, 1)))
    dice = tuple(die() for _ in range(4))
    if any(value not in (-1, 0, 1) for value in dice):
        raise ValueError("Fate dice must return -1, 0, or 1")
    return dice  # type: ignore[return-value]


def fixed_4df(total: int) -> tuple[int, int, int, int]:
    """Return one valid deterministic 4dF tuple with the requested total."""
    if total < -4 or total > 4:
        raise ValueError("A 4dF total must be between -4 and +4")
    sign = 1 if total >= 0 else -1
    values = [sign] * abs(total) + [0] * (4 - abs(total))
    return tuple(values)  # type: ignore[return-value]
