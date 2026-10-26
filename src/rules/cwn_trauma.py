"""Damage, Trauma and Shock on the CWN chassis.

Original implementation of the numerical mechanics described in the Cities
Without Number SRD, "Damage, Trauma, and Shock". The prose here is our own; no
SRD text is reproduced. The SRD omits the antagonists chapter, so NPC stat
blocks are out of scope at this layer.

The three ideas that make CWN violence feel different from a hit-point slugfest:

* **Trauma** - a lethal hit rolls a Trauma Die against the victim's Trauma
  Target. Beating it multiplies the whole hit, so a high Trauma Rating weapon
  is swingy rather than merely strong.
* **Shock** - an armed melee miss still hurts an insufficiently armoured
  target. Combat is dangerous even when you lose the roll.
* **Damage Soak** - armour can absorb a finite amount per fight and then stops
  helping, which models luck running out rather than ablative plating.

All dice enter as explicit values. Nothing here rolls anything, so a table roll
and a replay produce identical results.
"""
from __future__ import annotations

from dataclasses import dataclass

DEFAULT_TRAUMA_TARGET = 6


class TraumaRulesError(ValueError):
    """Raised when a call is outside the rules rather than merely unlucky."""


@dataclass(frozen=True)
class Shock:
    """Shock is recorded as a value and the highest Melee AC it reaches.

    ``max_ac=None`` is the SRD's ``Shock N/-`` form: it applies against any
    Armour Class. It is not "no shock"; it is shock without an AC ceiling.
    """

    value: int
    max_ac: int | None = None

    def __post_init__(self) -> None:
        if self.value < 0:
            raise TraumaRulesError("Shock value cannot be negative")

    def applies_to(self, melee_ac: int, *, immune: bool = False) -> bool:
        if immune:
            return False
        if self.max_ac is None:
            return True
        return melee_ac <= self.max_ac


@dataclass(frozen=True)
class Weapon:
    """The weapon facts the damage layer needs, and no more."""

    damage_die: str
    trauma_rating: int = 1
    shock: Shock | None = None
    lethal: bool = True
    unarmed: bool = False

    def __post_init__(self) -> None:
        if self.trauma_rating < 1:
            raise TraumaRulesError("Trauma Rating is at least x1")


@dataclass(frozen=True)
class AttackResult:
    """What a resolved hit did, itemised so a UI can explain the number."""

    base_damage: int
    total_damage: int
    soak_absorbed: int
    damage_to_hit_points: int
    traumatic: bool
    shock_floor_applied: bool
    major_injury_risk: bool


def absorb_with_soak(damage: int, soak: int) -> tuple[int, int]:
    """Return (damage that reaches hit points, soak remaining).

    Soak is spent down within a fight and does not regenerate until the fight
    ends, so callers must carry the remainder forward rather than re-reading a
    static armour value each hit.
    """
    if damage < 0 or soak < 0:
        raise TraumaRulesError("damage and soak cannot be negative")
    absorbed = min(damage, soak)
    return damage - absorbed, soak - absorbed


def is_traumatic(trauma_die_roll: int, trauma_target: int = DEFAULT_TRAUMA_TARGET) -> bool:
    """A Traumatic Hit is a Trauma Die that reaches the Trauma Target.

    Equalling the target counts: the SRD says "equals or exceeds".
    """
    if trauma_die_roll < 1:
        raise TraumaRulesError("a Trauma Die roll is at least 1")
    if trauma_target < 1:
        raise TraumaRulesError("a Trauma Target is at least 1")
    return trauma_die_roll >= trauma_target


def shock_on_miss(
    shock: Shock | None,
    melee_ac: int,
    attribute_modifier: int = 0,
    *,
    immune: bool = False,
    barrier_spent: bool = False,
) -> int:
    """Shock inflicted by a missed attack, or 0.

    ``barrier_spent`` models a riot shield or similar: it negates the first
    source of Shock in a round. Only the wielder's attribute modifier adds to
    Shock; generic damage bonuses do not.
    """
    if shock is None or barrier_spent:
        return 0
    if not shock.applies_to(melee_ac, immune=immune):
        return 0
    return max(0, shock.value + attribute_modifier)


def major_injury_risk(hit_points_after: int, *, traumatic_in_fight: bool) -> bool:
    """Zero hit points only threaten a Major Injury once trauma has landed.

    Being knocked to zero by ordinary damage is a knockout; being knocked to
    zero after a Traumatic Hit in the same fight is a wound that persists.
    """
    return hit_points_after <= 0 and traumatic_in_fight


def resolve_hit(
    weapon: Weapon,
    *,
    damage_roll: int,
    attribute_modifier: int = 0,
    skill_bonus: int = 0,
    trauma_die_roll: int | None = None,
    trauma_target: int = DEFAULT_TRAUMA_TARGET,
    target_melee_ac: int = 10,
    soak: int = 0,
    lethal: bool | None = None,
    shock_immune: bool = False,
    barrier_spent: bool = False,
    traumatic_damage_earlier_in_fight: bool = False,
    current_hit_points: int | None = None,
) -> AttackResult:
    """Resolve a hit that has already landed.

    ``lethal=False`` suppresses the Trauma Die entirely, which is how non-lethal
    attacks stay survivable. ``skill_bonus`` only applies to a purely unarmed
    attack; artificial weapons that merely use the Punch skill do not receive it,
    so the caller passes it only for ``weapon.unarmed``.
    """
    if damage_roll < 1:
        raise TraumaRulesError("a damage roll is at least 1")
    is_lethal = weapon.lethal if lethal is None else lethal

    base = damage_roll + attribute_modifier
    if weapon.unarmed:
        base += skill_bonus

    traumatic = False
    if is_lethal:
        if trauma_die_roll is None:
            raise TraumaRulesError("a lethal hit needs its Trauma Die roll")
        traumatic = is_traumatic(trauma_die_roll, trauma_target)

    total = base * weapon.trauma_rating if traumatic else base

    # A hit can never do less than the Shock it would have inflicted on a miss.
    floor = shock_on_miss(
        weapon.shock, target_melee_ac, attribute_modifier,
        immune=shock_immune, barrier_spent=barrier_spent,
    )
    floor_applied = total < floor
    if floor_applied:
        total = floor

    through, _remaining = absorb_with_soak(total, soak)

    # A Major Injury is only in play once a Traumatic Hit has landed in this
    # fight and the victim is at zero: trauma is what makes zero dangerous.
    # The caller supplies the victim's hit points, because damage dealt and hit
    # points remaining are different quantities and conflating them is how this
    # layer produced a false negative on its own first test run.
    major = False
    if current_hit_points is not None:
        major = major_injury_risk(
            current_hit_points - through,
            traumatic_in_fight=traumatic or traumatic_damage_earlier_in_fight,
        )

    return AttackResult(
        base_damage=base,
        total_damage=total,
        soak_absorbed=total - through,
        damage_to_hit_points=through,
        traumatic=traumatic,
        shock_floor_applied=floor_applied,
        major_injury_risk=major,
    )
