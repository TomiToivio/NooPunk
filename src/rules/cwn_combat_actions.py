"""Cities Without Number: the combat action economy.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``), ``rules-of-the-game/combat/combat-actions``.

## What the SRD fixes and what it leaves to the table

Fixed: a combatant gets **one Main** action and **one Move** action per round, and may **spend the Main
action for a second Move**; **On Turn** and **Instant** actions are as many as the GM finds plausible.
Several named actions modify or consume that budget in specific ways:

* **Snap Attack** (Instant): give up the Main action for an attack at **−4**, usable off-turn, only if
  the Main action is still unspent.
* **Swarm Attack** (Main): **+2 to hit and +1 damage per other assailant**, to a maximum of **+6 / +3**
  (four attackers in total). The bonus damage does not add to Shock and cannot exceed the weapon's
  normal maximum; any Shock is always applicable.
* **Charge** (Main + Move): move up to twice normal speed in a straight line, **at least 3 metres**, and
  attack at **+2** to hit, with **−2 AC** until the end of the round.
* **Total Defense** (Instant): give up the Main action for **+2 AC** and immunity to Shock until the
  start of the next turn; not available if the Main action is already spent.

Left to the table: *which* circumstances are plausible ("as many On Turn actions as the GM finds
plausible"), and the adjudication of simultaneous Instant actions. This module returns the numbers and
enforces the action-budget constraints, and refuses to invent the plausible ones.
"""
from __future__ import annotations

from dataclasses import dataclass, field

MAIN_ACTIONS_PER_ROUND = 1
MOVE_ACTIONS_PER_ROUND = 1

#: SRD: "as many On Turn actions ... as the GM finds plausible" — not a number, so not enforced.
ON_TURN_LIMITED = False
INSTANT_LIMITED = False

SNAP_ATTACK_PENALTY = -4

SWARM_PER_OTHER_HIT = 2
SWARM_PER_OTHER_DAMAGE = 1
#: Four assailants in total, so at most three "other" attackers count.
SWARM_MAX_OTHER_ASSAILANTS = 3

CHARGE_TO_HIT_BONUS = 2
CHARGE_AC_PENALTY = -2
CHARGE_MIN_DISTANCE_METRES = 3.0
CHARGE_SPEED_MULTIPLIER = 2

TOTAL_DEFENSE_AC_BONUS = 2


class ActionError(ValueError):
    """An action-budget rule from the SRD was about to be broken."""


@dataclass
class TurnBudget:
    """Main/Move bookkeeping for one combatant in one round."""

    main_used: bool = False
    moves_used: int = 0
    extra_moves: int = 0

    @property
    def main_available(self) -> bool:
        return not self.main_used

    @property
    def moves_available(self) -> int:
        return max(0, MOVE_ACTIONS_PER_ROUND + self.extra_moves - self.moves_used)

    def take_main(self) -> None:
        if not self.main_available:
            raise ActionError("the Main action has already been spent this round")
        self.main_used = True

    def take_move(self) -> None:
        if self.moves_available <= 0:
            raise ActionError(
                "no Move action left; spend the Main action for a second Move instead"
            )
        self.moves_used += 1

    def convert_main_to_move(self) -> None:
        """Spend the Main action to gain a second Move action."""
        self.take_main()
        self.extra_moves += 1


@dataclass(frozen=True)
class SwarmBonus:
    to_hit: int
    damage: int


@dataclass(frozen=True)
class Charge:
    to_hit_bonus: int
    ac_penalty: int
    speed_multiplier: int


@dataclass(frozen=True)
class DefenseStance:
    ac_bonus: int
    shock_immune: bool = True


def snap_attack_penalty(*, main_used: bool) -> int:
    """The Snap Attack penalty, or an error when the Main action is already spent."""
    if main_used:
        raise ActionError("a Snap Attack gives up a Main action that must still be unspent")
    return SNAP_ATTACK_PENALTY


def swarm_bonus(other_assailants: int) -> SwarmBonus:
    """Bonuses for a Swarm Attack by one of up to four attackers on the same target."""
    if other_assailants < 0:
        raise ActionError("the number of other assailants cannot be negative")
    counted = min(other_assailants, SWARM_MAX_OTHER_ASSAILANTS)
    return SwarmBonus(
        to_hit=SWARM_PER_OTHER_HIT * counted,
        damage=SWARM_PER_OTHER_DAMAGE * counted,
    )


def charge(
    distance_metres: float, *, budget: TurnBudget | None = None
) -> Charge:
    """Validate a Charge and return its modifiers.

    The charge costs both the Main and the Move action, so it is refused when either is unavailable.
    """
    if distance_metres < CHARGE_MIN_DISTANCE_METRES:
        raise ActionError(
            f"a Charge needs at least {CHARGE_MIN_DISTANCE_METRES:g} metres to build momentum"
        )
    if budget is not None:
        if not budget.main_available:
            raise ActionError("a Charge costs the Main action, which is already spent")
        if budget.moves_available <= 0:
            raise ActionError("a Charge costs a Move action, and none is left this round")
    return Charge(
        to_hit_bonus=CHARGE_TO_HIT_BONUS,
        ac_penalty=CHARGE_AC_PENALTY,
        speed_multiplier=CHARGE_SPEED_MULTIPLIER,
    )


def total_defense(*, main_used: bool) -> DefenseStance:
    """The Total Defense stance, or an error when the Main action is already spent."""
    if main_used:
        raise ActionError("Total Defense cannot be taken after spending the Main action")
    return DefenseStance(ac_bonus=TOTAL_DEFENSE_AC_BONUS)


#: The SRD's common actions, with the action each costs. ``main+move`` is a Charge.
COMMON_ACTIONS: dict[str, str] = {
    "make_melee_attack": "main",
    "make_ranged_attack": "main",
    "make_snap_attack": "instant",
    "make_swarm_attack": "main",
    "charge": "main+move",
    "screen_ally": "move",
    "total_defense": "instant",
    "run": "move",
    "fighting_withdrawal": "main",
    "use_skill": "main",
    "ready_or_stow_item": "main",
    "reload_weapon": "main",
    "drop_item": "instant",
    "pick_up_item": "move",
    "stand_up": "move",
}
