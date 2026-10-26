"""Injury consequences on the CWN chassis: Damage Soak and Major Injury.

``src/rules/cwn_core.py`` is the single source of truth for the resolution
primitives - the Trauma Die against the Trauma Target, the Trauma Rating
multiplication, Shock applicability and its value, and the "a hit is never
weaker than the Shock it avoided" floor. This module does not restate any of
them; it delegates.

What lives here is what the core does not model: **Damage Soak** as a per-fight
pool that spends down rather than a static armour value, and the **Major Injury**
condition, which is only possible once a Traumatic Hit has landed in that fight
and the victim reaches zero hit points. Both are consequences of a resolved
attack rather than parts of resolving one.

All dice enter as explicit values, so a table roll and a replay agree.
"""
from __future__ import annotations

from dataclasses import dataclass

from .cwn_core import (
    DEFAULT_TRAUMA_TARGET,
    CwnError,
    damage_floor,
    is_traumatic_hit,
    shock_applies,
    shock_damage,
    trauma_damage,
)

# The name this module used before the core existed. Keeping the alias means a
# caller catching either name catches the same class, rather than silently
# missing an error because two modules defined their own.
TraumaRulesError = CwnError

__all__ = [
    "DEFAULT_TRAUMA_TARGET",
    "AttackResult",
    "Shock",
    "TraumaRulesError",
    "Weapon",
    "absorb_with_soak",
    "is_traumatic",
    "major_injury_risk",
    "resolve_hit",
    "shock_on_miss",
]


@dataclass(frozen=True)
class Shock:
    """A Shock rating: its value and the highest Melee AC it reaches.

    ``max_ac=None`` is the SRD's ``Shock n/-`` form - no Armour Class ceiling.
    That is not the same as no Shock, and confusing the two is easy.
    """

    value: int
    max_ac: int | None = None

    def __post_init__(self) -> None:
        if self.value < 0:
            raise TraumaRulesError("Shock value cannot be negative")

    def applies_to(self, melee_ac: int, *, immune: bool = False) -> bool:
        """Whether a miss would reach a target at this Armour Class."""
        if immune:
            return False
        return shock_applies(hit=False, shock_ac=self.max_ac, target_melee_ac=melee_ac)


@dataclass(frozen=True)
class Weapon:
    """The weapon facts the injury layer needs, and no more."""

    damage_die: str
    trauma_rating: int = 1
    shock: Shock | None = None
    lethal: bool = True
    unarmed: bool = False


@dataclass(frozen=True)
class AttackResult:
    """A resolved hit, itemised so a UI can explain the number."""

    base_damage: int
    total_damage: int
    soak_absorbed: int
    damage_to_hit_points: int
    traumatic: bool
    shock_floor_applied: bool
    major_injury_risk: bool


def absorb_with_soak(damage: int, soak: int) -> tuple[int, int]:
    """Return (damage reaching hit points, soak remaining).

    Soak is spent down inside a fight and refreshes only after it ends, so the
    remainder has to be carried forward instead of re-reading a static value.
    """
    if damage < 0 or soak < 0:
        raise TraumaRulesError("damage and soak cannot be negative")
    absorbed = min(damage, soak)
    return damage - absorbed, soak - absorbed


def is_traumatic(trauma_die_roll: int, trauma_target: int = DEFAULT_TRAUMA_TARGET) -> bool:
    """Delegate to the core: the Trauma Die meeting or exceeding the target."""
    return is_traumatic_hit(trauma_die_roll, trauma_target)


def shock_on_miss(
    shock: Shock | None,
    melee_ac: int,
    attribute_modifier: int = 0,
    *,
    immune: bool = False,
    barrier_spent: bool = False,
) -> int:
    """Shock from a missed attack, or 0.

    Immunity and a spent barrier are NoöPunk-side effects with no field in the
    core signature, so they are decided here and only the surviving case is
    delegated.
    """
    if shock is None or immune or barrier_spent:
        return 0
    value = shock_damage(
        hit=False,
        shock_value=shock.value,
        shock_ac=shock.max_ac,
        target_melee_ac=melee_ac,
        attribute_modifier=attribute_modifier,
    )
    return max(0, value)


def major_injury_risk(hit_points_after: int, *, traumatic_in_fight: bool) -> bool:
    """Zero hit points only threaten a Major Injury once trauma has landed.

    Being knocked out by ordinary damage is a knockout. Being knocked to zero
    after a Traumatic Hit in the same fight is a wound that persists.
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

    ``lethal=False`` suppresses the Trauma Die entirely, which is what keeps a
    non-lethal attack survivable. ``skill_bonus`` belongs to a purely unarmed
    attack only, so the caller passes it only for ``weapon.unarmed``.
    """
    if damage_roll < 1:
        raise TraumaRulesError("a damage roll is at least 1")

    is_lethal = weapon.lethal if lethal is None else lethal
    base = damage_roll + attribute_modifier + (skill_bonus if weapon.unarmed else 0)

    traumatic = False
    if is_lethal:
        if trauma_die_roll is None:
            raise TraumaRulesError("a lethal hit needs its Trauma Die roll")
        traumatic = is_traumatic(trauma_die_roll, trauma_target)

    total = trauma_damage(base, weapon.trauma_rating, traumatic=traumatic)

    floor = shock_on_miss(
        weapon.shock, target_melee_ac, attribute_modifier,
        immune=shock_immune, barrier_spent=barrier_spent,
    )
    floored = damage_floor(total, floor)
    floor_applied = floored > total
    total = floored

    through, _remaining = absorb_with_soak(total, soak)

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
