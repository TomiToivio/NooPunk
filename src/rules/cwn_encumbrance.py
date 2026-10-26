"""Cities Without Number: encumbrance.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``), ``rules-of-the-game/encumbrance/``.

## The rules, as the SRD states them

Gear has an encumbrance value in points and is either **Stowed** (packed away; takes a Main Action to
retrieve) or **Readied** (in hands or quick-access places; usable as part of an action).

* A character carries **Stowed points equal to their Strength score** and **Readied points equal to
  half their Strength, rounded down**.
* They may push past that: **+2 Readied and +4 Stowed** for a longer term, at a **30 %** cut to Move
  speed (10 m → 7 m); a **second** such push is a **50 %** cut (10 m → 5 m); beyond that it cannot be
  hauled over a significant distance.
* Three small items may be **bundled** into one point, at the cost of a Main Action to break the
  bundle open.
* When bulk goods are measured in kilograms, **25 kg ≈ 10 points** for a character carrying a pack.

## What this module does not decide

It does not track items, and it does not decide whether a particular object is 0, 1, 2 or 5+ points —
the SRD leaves ambiguous objects to the GM. It answers the questions a runtime asks: what fits, what
tier the load is in, and what that tier does to movement.
"""
from __future__ import annotations

from dataclasses import dataclass

#: SRD: Readied points are half Strength, rounded down.
READIED_DIVISOR = 2

#: SRD: one overload step is +2 Readied and +4 Stowed.
OVERLOAD_READIED_BONUS = 2
OVERLOAD_STOWED_BONUS = 4

#: SRD: first overload cuts Move by 30 %, the second by 50 %.
HEAVY_LOAD_SPEED_FACTOR = 0.70
OVERLOADED_SPEED_FACTOR = 0.50

#: SRD: base Move speed is 10 m; the two overloaded speeds are 7 m and 5 m.
BASE_MOVE_METRES = 10.0

#: SRD: three small items can be bundled into one point.
BUNDLE_SIZE = 3

#: SRD: 25 kg is about 10 points when carried on the back.
KILOGRAMS_PER_TEN_POINTS = 25.0


class EncumbranceError(ValueError):
    """A constraint from the SRD was about to be violated."""


@dataclass(frozen=True)
class Load:
    """A character's carried load, split the way the SRD splits it."""

    stowed: float = 0.0
    readied: float = 0.0

    def __post_init__(self) -> None:
        if self.stowed < 0 or self.readied < 0:
            raise EncumbranceError("encumbrance cannot be negative")


def stowed_capacity(strength: int) -> int:
    """Stowed points a character can carry without penalty: their Strength."""
    if strength < 0:
        raise EncumbranceError("Strength cannot be negative")
    return strength


def readied_capacity(strength: int) -> int:
    """Readied points without penalty: half Strength, rounded down."""
    if strength < 0:
        raise EncumbranceError("Strength cannot be negative")
    return strength // READIED_DIVISOR


def tier_for(strength: int, load: Load) -> str:
    """``normal``, ``heavy`` (first push), ``overloaded`` (second push) or ``immobile``."""
    stowed_limit = stowed_capacity(strength)
    readied_limit = readied_capacity(strength)
    if load.stowed <= stowed_limit and load.readied <= readied_limit:
        return "normal"
    if (
        load.stowed <= stowed_limit + OVERLOAD_STOWED_BONUS
        and load.readied <= readied_limit + OVERLOAD_READIED_BONUS
    ):
        return "heavy"
    if (
        load.stowed <= stowed_limit + 2 * OVERLOAD_STOWED_BONUS
        and load.readied <= readied_limit + 2 * OVERLOAD_READIED_BONUS
    ):
        return "overloaded"
    return "immobile"


def move_speed(strength: int, load: Load, *, base: float = BASE_MOVE_METRES) -> float:
    """The character's Move speed in metres for this load."""
    if base <= 0:
        raise EncumbranceError("base speed must be positive")
    tier = tier_for(strength, load)
    if tier == "normal":
        return base
    if tier == "heavy":
        return base * HEAVY_LOAD_SPEED_FACTOR
    if tier == "overloaded":
        return base * OVERLOADED_SPEED_FACTOR
    return 0.0


def can_haul(strength: int, load: Load) -> bool:
    """Whether the load can be carried over a significant distance at all."""
    return tier_for(strength, load) != "immobile"


def bundled_points(item_count: int) -> int:
    """Points for small identical items tied into bundles of three."""
    if item_count < 0:
        raise EncumbranceError("item count cannot be negative")
    return (item_count + BUNDLE_SIZE - 1) // BUNDLE_SIZE


def kilograms_to_points(kilograms: float) -> float:
    """Convert bulk weight to encumbrance points (25 kg ≈ 10 points)."""
    if kilograms < 0:
        raise EncumbranceError("weight cannot be negative")
    return kilograms / KILOGRAMS_PER_TEN_POINTS * 10.0
