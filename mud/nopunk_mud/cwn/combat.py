"""CWN combat: the action economy, Trauma and Shock (#950 item 3).

Source: Cities Without Number SRD, *Combat Actions* and *Damage, Trauma, and Shock*.

The action economy, as written:

* one **Main** action per round;
* one **Move** action per round, and a second by spending the Main action;
* **On Turn** actions, as many as the GM finds plausible;
* **Instant** actions, as many as the GM finds plausible, usable off-turn and after a roll.

Trauma: on a lethal hit, roll the weapon's Trauma Die; if it is equal to or greater than the victim's
Trauma Target (usually 6 for an unarmoured human) the hit is Traumatic and the total damage is
multiplied by the weapon's Trauma Rating. A non-lethal attack does not roll the Trauma Die.

Shock: a melee weapon records Shock as a value and an Armour Class, e.g. ``Shock 2/15``. When the
wielder *misses* a target whose Melee Armour Class is equal to or less than that rating, the target
suffers the Shock value.

Determinism: every roll is passed in. Nothing here rolls dice, so a caller can replay a fight.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import CwnError

TRAUMA_DIE_SIDES = (4, 6, 8, 10, 12)
DEFAULT_TRAUMA_TARGET = 6
MAIN = "main"
MOVE = "move"
ON_TURN = "on_turn"
INSTANT = "instant"


@dataclass
class CombatTurn:
    """One combatant's action budget for one round."""

    main_used: bool = False
    moves_used: int = 0
    on_turn_used: int = 0
    instant_used: int = 0
    used: list[str] = field(default_factory=list)

    def spend_main(self) -> None:
        if self.main_used:
            raise CwnError("the main action is already spent this round")
        self.main_used = True
        self.used.append(MAIN)

    def spend_move(self) -> None:
        if self.moves_used >= 2:
            raise CwnError("no move action left this round")
        if self.moves_used == 1:
            # The second move action costs the main action.
            if self.main_used:
                raise CwnError("a second move action requires the main action, which is spent")
            self.main_used = True
            self.used.append(MAIN)
        self.moves_used += 1
        self.used.append(MOVE)

    def spend_on_turn(self) -> None:
        """Unbounded by rule; the GM decides plausibility. Counted so a log can show it."""
        self.on_turn_used += 1
        self.used.append(ON_TURN)

    def spend_instant(self) -> None:
        """Usable off-turn, even after the dice are rolled."""
        self.instant_used += 1
        self.used.append(INSTANT)

    @property
    def main_available(self) -> bool:
        return not self.main_used

    @property
    def moves_available(self) -> int:
        if self.moves_used >= 2:
            return 0
        if self.moves_used == 1 and self.main_used:
            return 0
        return 2 - self.moves_used

    def reset(self) -> None:
        self.main_used = False
        self.moves_used = 0
        self.on_turn_used = 0
        self.instant_used = 0
        self.used.clear()


def trauma_hit(
    *,
    damage: int,
    trauma_die: int,
    die_roll: int,
    trauma_rating: int,
    trauma_target: int = DEFAULT_TRAUMA_TARGET,
    lethal: bool = True,
) -> dict[str, object]:
    """Apply the Trauma Die to an already-resolved hit.

    Returns ``{"traumatic": bool, "damage": int, "die": int | None}``.
    """
    if trauma_die not in TRAUMA_DIE_SIDES:
        raise CwnError(f"unsupported trauma die d{trauma_die}")
    if not 1 <= die_roll <= trauma_die:
        raise CwnError(f"trauma die roll must be 1..{trauma_die}")
    if trauma_rating < 2:
        raise CwnError("a trauma rating is a damage multiplier of at least 2")
    if trauma_target < 1:
        raise CwnError("trauma target must be positive")
    if damage < 0:
        raise CwnError("damage cannot be negative")

    if not lethal:
        # "If so, do not roll the Trauma Die." The die is not consulted at all.
        return {"traumatic": False, "damage": damage, "die": None}

    traumatic = die_roll >= trauma_target
    return {
        "traumatic": traumatic,
        "damage": damage * trauma_rating if traumatic else damage,
        "die": die_roll,
    }


def shock_damage(*, shock: int, shock_ac: int, missed: bool, target_melee_ac: int) -> int:
    """Shock applies only on a miss, and only to targets at or below the weapon's Shock AC."""
    if shock < 0:
        raise CwnError("shock cannot be negative")
    if not missed:
        return 0
    return shock if target_melee_ac <= shock_ac else 0
