"""Cities Without Number: Foci (SRD 1.6.0-1.6.2, 2.7.1.6).

This module implements the **Foci engine**, not the catalogue text: how many picks a character has,
which of the 26 Foci have a second level, when a new pick is earned, and the gear budgets that three
Foci grant. The benefit prose for each Focus stays in the SRD (and in the rulebook's own wording);
duplicating it here would create a second copy that must be kept in sync with the first.

Transcribed from the **Cities Without Number SRD** (CC0, verified 2026-10-10 in
``data/sources/game_system_rights.json``). Section numbers are cited throughout.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

__all__ = [
    "FOCI",
    "GEAR_BUDGET",
    "PICK_LEVELS",
    "Focus",
    "FocusError",
    "advancement_picks",
    "can_take_level",
    "focused_edge",
    "gear_budget",
    "GEAR_BUDGET_FOCI",
    "max_level",
    "new_character_picks",
    "take_level",
    "total_picks",
]

#: SRD 2.7.1.6: "At levels 2, 5, 7, and 10 a PC can add a level to an existing Focus or pick up the
#: first level in a new Focus."
PICK_LEVELS: tuple[int, ...] = (2, 5, 7, 10)

#: SRD 1.6.2: the gear budgets granted by the three Foci that carry one, by character level.
#: ``(vehicle, drone)`` -- Ace Driver and Roamer use the vehicle column, Drone Pilot the drone column.
GEAR_BUDGET: dict[int, tuple[int, int]] = {
    1: (5_000, 1_000),
    2: (10_000, 5_000),
    3: (15_000, 10_000),
    4: (20_000, 15_000),
    5: (30_000, 20_000),
    6: (40_000, 25_000),
    7: (60_000, 35_000),
    8: (80_000, 45_000),
    9: (100_000, 60_000),
    10: (200_000, 80_000),
}

#: The Foci that grant a gear budget (SRD 1.6.2 names them explicitly).
GEAR_BUDGET_FOCI: dict[str, Literal["vehicle", "drone"]] = {
    "Ace Driver": "vehicle",
    "Roamer": "vehicle",
    "Drone Pilot": "drone",
}

FocusError = ValueError


@dataclass(frozen=True)
class Focus:
    """A Focus and how many levels it has.

    SRD 1.6.0: "Foci usually come in two levels, though some have only one." The first pick grants
    level 1; the second pick grants level 2 **in addition to** level 1.
    """

    name: str
    levels: Literal[1, 2]

    @property
    def has_second_level(self) -> bool:
        return self.levels == 2


#: SRD 1.6.1. Twenty-two Foci have two levels; four have one.
FOCI: dict[str, Focus] = {
    "Ace Driver": Focus("Ace Driver", 2),
    "Alert": Focus("Alert", 2),
    "All Natural": Focus("All Natural", 1),
    "Armsmaster": Focus("Armsmaster", 2),
    "Assassin": Focus("Assassin", 2),
    "Authority": Focus("Authority", 2),
    "Close Combatant": Focus("Close Combatant", 2),
    "Cyberdoc": Focus("Cyberdoc", 2),
    "Deadeye": Focus("Deadeye", 2),
    "Diplomat": Focus("Diplomat", 2),
    "Drone Pilot": Focus("Drone Pilot", 2),
    "Expert Programmer": Focus("Expert Programmer", 2),
    "Healer": Focus("Healer", 2),
    "Henchkeeper": Focus("Henchkeeper", 2),
    "Many Faces": Focus("Many Faces", 1),
    "Pop Idol": Focus("Pop Idol", 2),
    "Roamer": Focus("Roamer", 2),
    "Safe Haven": Focus("Safe Haven", 2),
    "Shocking Assault": Focus("Shocking Assault", 2),
    "Sniper's Eye": Focus("Sniper's Eye", 2),   # the SRD prints a typographic apostrophe
    "Specialist": Focus("Specialist", 2),
    "Tinker": Focus("Tinker", 2),
    "Unarmed Combatant": Focus("Unarmed Combatant", 2),
    "Unique Gift": Focus("Unique Gift", 1),
    "Unregistered": Focus("Unregistered", 1),
    "Whirlwind Assault": Focus("Whirlwind Assault", 2),
}


def focused_edge(*, has_focused_edge: bool) -> int:
    """SRD 1.6.0: "A new character may choose one Focus, plus one more if they have the Focused Edge"."""
    return 1 if has_focused_edge else 0


def new_character_picks(*, has_focused_edge: bool = False) -> int:
    return 1 + focused_edge(has_focused_edge=has_focused_edge)


def advancement_picks(character_level: int) -> int:
    """How many Focus picks the character has earned from levelling (SRD 2.7.1.6)."""
    if character_level < 1:
        raise FocusError("character level starts at 1")
    return sum(1 for level in PICK_LEVELS if level <= character_level)


def total_picks(character_level: int, *, has_focused_edge: bool = False) -> int:
    """Creation pick(s) plus every advancement pick earned so far."""
    return new_character_picks(has_focused_edge=has_focused_edge) + advancement_picks(character_level)


def max_level(focus: str) -> int:
    if focus not in FOCI:
        raise FocusError(f"unknown Focus {focus!r}")
    return FOCI[focus].levels


def can_take_level(focus: str, *, current_level: int) -> bool:
    """Whether the next pick in this Focus is legal.

    A level cannot be skipped: level 2 requires level 1 first, and a one-level Focus refuses a
    second pick rather than silently capping it.
    """
    if current_level < 0:
        raise FocusError("current level cannot be negative")
    return current_level < max_level(focus)


def take_level(focus: str, *, current_level: int) -> int:
    """Return the Focus's new level after spending a pick, or raise if the pick is illegal."""
    if not can_take_level(focus, current_level=current_level):
        raise FocusError(
            f"{focus} is at level {current_level} of {max_level(focus)}; no further levels exist"
        )
    return current_level + 1


def gear_budget(character_level: int, *, kind: Literal["vehicle", "drone"]) -> int:
    """SRD 1.6.2: the free-gear budget for Ace Driver/Roamer (vehicle) or Drone Pilot (drone)."""
    if kind not in ("vehicle", "drone"):
        raise FocusError("kind must be 'vehicle' or 'drone'")
    if character_level not in GEAR_BUDGET:
        raise FocusError("the SRD table covers character levels 1-10")
    vehicle, drone = GEAR_BUDGET[character_level]
    return vehicle if kind == "vehicle" else drone
