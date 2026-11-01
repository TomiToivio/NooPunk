"""Vanilla CWN reaction rolls and NPC morale (Free Edition pp. 182-184).

Source: CWN Free Edition 081123, "Reaction Rolls and Morale" and "Morale and Morale Checks".
The dice are supplied by the caller so the result is deterministic and testable; this module does
not hide a random source inside a rule calculation.
"""
from __future__ import annotations

from dataclasses import dataclass

REACTION_SOURCE = "CWN Free Edition p. 182"
MORALE_SOURCE = "CWN Free Edition pp. 183-184"

REACTION_BANDS = (
    (2, "violent_hostile", "As hostile and violent as is plausible"),
    (3, "hostile", "Hostile and unfriendly to the PCs"),
    (6, "neutral", "A neutral or expected reaction from them"),
    (9, "friendly", "Unusually friendly or cooperative"),
    (12, "helpful", "As friendly and helpful as is plausible"),
)


class NpcRuleError(ValueError):
    """Invalid dice or NPC values; refuse rather than silently clamp."""


def _d6(value: int, name: str) -> int:
    if not isinstance(value, int) or not 1 <= value <= 6:
        raise NpcRuleError(f"{name} must be a d6 result (1..6)")
    return value


def reaction_band(total: int) -> str:
    """Map a modified 2d6 reaction total to its printed band."""
    if not 2 <= total <= 12:
        raise NpcRuleError("reaction total must be 2..12 after modifiers")
    key = REACTION_BANDS[0][1]
    for threshold, name, _ in REACTION_BANDS:
        if total >= threshold:
            key = name
    return key


@dataclass(frozen=True)
class Reaction:
    total: int
    band: str
    description: str
    source: str = REACTION_SOURCE


def reaction_roll(die_a: int, die_b: int, charisma_modifier: int = 0) -> Reaction:
    """2d6 + the spokesman's Charisma modifier, using the printed reaction table."""
    if not -2 <= charisma_modifier <= 2:
        raise NpcRuleError("Charisma modifier must be -2..+2 under CWN")
    total = _d6(die_a, "die_a") + _d6(die_b, "die_b") + charisma_modifier
    total = min(12, max(2, total))
    band = reaction_band(total)
    description = next(text for _, name, text in REACTION_BANDS if name == band)
    return Reaction(total=total, band=band, description=description)


@dataclass(frozen=True)
class MoraleCheck:
    total: int
    morale: int
    broken: bool
    source: str = MORALE_SOURCE


def morale_check(die_a: int, die_b: int, morale: int) -> MoraleCheck:
    """2d6 against Morale; equal or higher breaks, exactly as printed on p. 183."""
    if not 2 <= morale <= 12:
        raise NpcRuleError("NPC Morale must be 2..12")
    total = _d6(die_a, "die_a") + _d6(die_b, "die_b")
    return MoraleCheck(total=total, morale=morale, broken=total >= morale)
