"""Vanilla CWN Heat track (Free Edition p. 178).

Heat is one team-wide reputation score. The book prints consequences by band but no generic
acquisition formula: mission tags and specific offences are what add Heat. This module therefore
stores and reports the score, and refuses to invent a formula the book does not give.
"""
from __future__ import annotations

from dataclasses import dataclass

HEAT_SOURCE = "CWN Free Edition p. 178"

HEAT_BANDS = (
    (0, "avoided", "The corps actively avoid bothering the team; smooth operators are an asset."),
    (1, "low", "Stay out of victims' offices and away from their security crews."),
    (4, "significant", "Vigorous pursuit during missions; captured operators are likely killed."),
    (6, "hunted", "Enemies actively seek the team's death; at least one hit team is tracking them."),
    (8, "overwhelmed", "Several stronger teams hunt the team; only a bloody rebuff deters them."),
    (10, "megacorp_enemy", "A megacorp or city government is personally enraged; survival is unlikely."),
)


class HeatError(ValueError):
    """Invalid Heat operation."""


def heat_band(score: int) -> tuple[str, str]:
    if not isinstance(score, int) or score < 0:
        raise HeatError("Heat is a non-negative integer")
    name, text = HEAT_BANDS[0][1], HEAT_BANDS[0][2]
    for threshold, band, description in HEAT_BANDS:
        if score >= threshold:
            name, text = band, description
    return name, text


@dataclass
class HeatTrack:
    score: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.score, int) or self.score < 0:
            raise HeatError("Heat is a non-negative integer")

    def add(self, amount: int) -> int:
        if not isinstance(amount, int) or amount < 0:
            raise HeatError("Heat changes are non-negative integers")
        self.score += amount
        return self.score

    def reduce(self, amount: int) -> int:
        if not isinstance(amount, int) or amount < 0:
            raise HeatError("Heat changes are non-negative integers")
        self.score = max(0, self.score - amount)
        return self.score

    @property
    def band(self) -> str:
        return heat_band(self.score)[0]

    @property
    def consequence(self) -> str:
        return heat_band(self.score)[1]
