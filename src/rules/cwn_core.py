"""Cities Without Number: saving throws, Shock and Trauma.

The companion to :mod:`src.rules.wn_core`. That module carries the shared Without Number kernel
(attributes, modifier bands, `2d6` skill checks, difficulties, opposed checks). This one carries the
two CWN mechanics the kernel does not cover, and nothing else.

Everything below is transcribed from the **Cities Without Number SRD** (CC0, verified 2026-10-10 in
``data/sources/game_system_rights.json``). Section numbers are cited so a reader can check the
implementation against the source rather than against my memory of it.

## Saving throws (SRD 2.2.0, 1.7.3)

A save is ``1d20 >= target``. A **natural 1 always fails** and a **natural 20 always succeeds**,
whatever the target.

Targets are ``16 - character level - best relevant attribute modifier``::

    Physical : 16 - level - best(Strength, Constitution)
    Evasion  : 16 - level - best(Dexterity, Intelligence)
    Mental   : 16 - level - best(Wisdom, Charisma)
    Luck     : 16 - level                     (no attribute applies)

The character-creation summary (1.7.3) says a *new character's* target is "15 minus the better
modifier", which is the same formula read at **level 1** — ``16 - 1 = 15``. The two sections agree;
they are not two rules, and this module implements the general one.

## Trauma (SRD 2.4.6.3)

On a **hit** with a lethal weapon, roll the weapon's Trauma Die. If it is ``>=`` the victim's Trauma
Target (usually **6** for an unarmoured human) the hit is **Traumatic**, and it multiplies the
**total** damage by the weapon's Trauma Rating (a ``x3`` rating turns 9 damage into 27).

Non-lethal attacks do not roll the Trauma Die at all (2.4.6.1).

## Shock (SRD 2.4.6.4)

Some melee weapons inflict Shock **on a miss**: if the target's Melee AC is ``<=`` the weapon's Shock
AC rating, the target takes the Shock value anyway. A rating of ``None`` means ``Shock n/-`` — it
applies regardless of AC.

Three invariants are enforced here rather than left to the caller:

* **Shock can never cause a Traumatic Hit.**
* **A hit never deals less than the Shock that would have applied on a miss** (:func:`damage_floor`).
* Only the wielder's attribute modifier and bonuses that *explicitly* say they add to Shock count;
  a generic +2 damage mod does not.
"""
from __future__ import annotations

import random
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from . import wn_core
from .cwn_major_injury import (
    INJURY_MAX,
    INJURY_MIN,
    MAJOR_INJURY_TABLE,
    MajorInjury,
    clamp_injury_roll,
    injury_for_roll,
)

#: The four saves, in SRD order.
SAVE_KINDS: tuple[str, ...] = ("Physical", "Evasion", "Mental", "Luck")

#: ``16 - level - modifier``; 1.7.3's "15" is this value at level 1.
SAVE_BASE = 16

#: The attribute pair each save draws its modifier from. ``Luck`` has none.
SAVE_ATTRIBUTES: dict[str, tuple[str, ...]] = {
    "Physical": ("Strength", "Constitution"),
    "Evasion": ("Dexterity", "Intelligence"),
    "Mental": ("Wisdom", "Charisma"),
    "Luck": (),
}

#: SRD 2.4.6.3: usually 6 for an unarmoured human. Edges, armour and cyberware may raise it.
DEFAULT_TRAUMA_TARGET = 6

SAVE_DIE_FACES = 20


class CwnError(ValueError):
    """A constraint from the SRD was about to be violated."""


@dataclass(frozen=True)
class Save:
    """One resolved saving throw."""

    kind: str
    die: int
    bonus: int
    target: int

    @property
    def natural(self) -> bool:
        """True on a natural 1 or natural 20 — the two results the die decides alone."""
        return self.die in (1, SAVE_DIE_FACES)

    @property
    def total(self) -> int:
        return self.die + self.bonus

    @property
    def success(self) -> bool:
        if self.die == 1:
            return False
        if self.die == SAVE_DIE_FACES:
            return True
        return self.total >= self.target


def _modifier(stat: str, attributes: Mapping[str, int]) -> int:
    if stat not in attributes:
        raise CwnError(f"attribute {stat!r} is missing from the sheet")
    return wn_core.attribute_modifier(int(attributes[stat]))


def save_target(kind: str, *, level: int, attributes: Mapping[str, int]) -> int:
    """The d20 target for ``kind``, from SRD 2.2.0.

    ``Luck`` ignores attributes entirely — a new character's Luck target is 15, i.e. 16 minus level 1.
    """
    if kind not in SAVE_ATTRIBUTES:
        raise CwnError(f"unknown save {kind!r}; expected one of {SAVE_KINDS}")
    if level < 1:
        raise CwnError(f"character level starts at 1, got {level}")
    pair = SAVE_ATTRIBUTES[kind]
    best = max((_modifier(stat, attributes) for stat in pair), default=0)
    return SAVE_BASE - level - best


def saving_throw(
    kind: str,
    *,
    level: int,
    attributes: Mapping[str, int],
    bonus: int = 0,
    rng: Any = None,
    die: int | None = None,
) -> Save:
    """Roll ``1d20`` against the save target.

    The die may be supplied directly for a table that rolled a real d20; otherwise pass a seeded
    ``rng`` so a replay is reproducible.
    """
    target = save_target(kind, level=level, attributes=attributes)
    rolled: int
    if die is None:
        source = rng if rng is not None else random.Random()
        rolled = int(source.randint(1, SAVE_DIE_FACES))
    else:
        if not 1 <= die <= SAVE_DIE_FACES:
            raise CwnError(f"a d20 shows 1..{SAVE_DIE_FACES}, got {die}")
        rolled = die
    return Save(kind=kind, die=rolled, bonus=int(bonus), target=target)


# --------------------------------------------------------------------------- #
# Trauma
# --------------------------------------------------------------------------- #

def is_traumatic_hit(trauma_die: int, trauma_target: int = DEFAULT_TRAUMA_TARGET) -> bool:
    """SRD 2.4.6.3: the Trauma Die meeting or exceeding the Trauma Target.

    Non-lethal attacks must not call this at all — they do not roll the Trauma Die (2.4.6.1).
    """
    if trauma_die < 1:
        raise CwnError(f"trauma die must be positive, got {trauma_die}")
    return trauma_die >= trauma_target


def trauma_damage(total_damage: int, trauma_rating: int, *, traumatic: bool) -> int:
    """Multiply the **total** damage by the weapon's Trauma Rating on a Traumatic Hit.

    The SRD multiplies total damage, not the weapon's die: 9 damage at ``x3`` becomes 27.
    """
    if trauma_rating < 1:
        raise CwnError(f"trauma rating must be at least x1, got x{trauma_rating}")
    if total_damage < 0:
        raise CwnError(f"damage cannot be negative, got {total_damage}")
    return total_damage * trauma_rating if traumatic else total_damage


# --------------------------------------------------------------------------- #
# Shock
# --------------------------------------------------------------------------- #

def shock_applies(*, hit: bool, shock_ac: int | None, target_melee_ac: int) -> bool:
    """Whether Shock lands: **only on a miss**, and only if the target's AC is within the rating.

    ``shock_ac=None`` models ``Shock n/-``, which applies regardless of Armor Class (2.4.6.4).
    """
    if hit:
        return False
    if shock_ac is None:
        return True
    return target_melee_ac <= shock_ac


def shock_damage(
    *,
    hit: bool,
    shock_value: int,
    shock_ac: int | None,
    target_melee_ac: int,
    attribute_modifier: int = 0,
    explicit_bonus: int = 0,
) -> int:
    """Shock inflicted on a miss, or ``0``.

    ``explicit_bonus`` is only for bonuses that *say* they add to Shock (the Killing Blow Edge, for
    example). A generic "+2 damage" weapon mod does not qualify, so it has no parameter here.
    """
    if shock_value < 0:
        raise CwnError(f"shock value cannot be negative, got {shock_value}")
    if not shock_applies(hit=hit, shock_ac=shock_ac, target_melee_ac=target_melee_ac):
        return 0
    return shock_value + attribute_modifier + explicit_bonus


def damage_floor(hit_damage: int, shock_that_would_have_applied: int) -> int:
    """SRD 2.4.6.4: a hit never deals less than the Shock that a miss would have dealt."""
    if hit_damage < 0 or shock_that_would_have_applied < 0:
        raise CwnError("damage cannot be negative")
    return max(hit_damage, shock_that_would_have_applied)


def shock_can_cause_trauma() -> bool:
    """False by SRD 2.4.6.4 — exposed as a function so a caller cannot forget the invariant."""
    return False


def resolve_attack(
    *,
    hit: bool,
    total_damage: int = 0,
    trauma_die: int | None = None,
    trauma_rating: int = 1,
    trauma_target: int = DEFAULT_TRAUMA_TARGET,
    shock_value: int = 0,
    shock_ac: int | None = None,
    target_melee_ac: int = 10,
    attribute_modifier: int = 0,
    explicit_shock_bonus: int = 0,
) -> dict[str, Any]:
    """One attack's damage, with the SRD's three Shock invariants enforced in order.

    Returns a dictionary rather than a bare number so a table can show *why* a number appeared:
    ``damage``, ``shock``, ``trauma`` (bool), ``trauma_die``.
    """
    # The floor is a COUNTERFACTUAL: "a hit can never do less damage than the Shock that would have
    # been inflicted on a miss". It must therefore be computed with hit=False even when the attack
    # hit, or the floor can never engage. Getting this wrong is invisible whenever damage exceeds
    # the Shock value, which is almost always.
    would_be_shock = shock_damage(
        hit=False,
        shock_value=shock_value,
        shock_ac=shock_ac,
        target_melee_ac=target_melee_ac,
        attribute_modifier=attribute_modifier,
        explicit_bonus=explicit_shock_bonus,
    )
    if not hit:
        return {"damage": would_be_shock, "shock": would_be_shock,
                "shock_floor": would_be_shock, "trauma": False, "trauma_die": None}

    trauma = False
    if trauma_die is not None:
        trauma = is_traumatic_hit(trauma_die, trauma_target)
    damage = trauma_damage(total_damage, trauma_rating, traumatic=trauma)
    damage = damage_floor(damage, would_be_shock)
    return {"damage": damage, "shock": 0, "shock_floor": would_be_shock,
            "trauma": trauma, "trauma_die": trauma_die}

# --------------------------------------------------------------------------- #
# Major Injuries (SRD 2.5.6)
# --------------------------------------------------------------------------- #
# The trigger is narrow and easy to get wrong: it is not "reduced to zero", it is "reduced to zero by
# LETHAL damage during the same scene in which the subject suffered a Traumatic Hit". The damage that
# brings them down need not be the Traumatic Hit itself -- they stay vulnerable until the scene ends.

# The Major Injury table lives in one module only. `cwn_major_injury` owns the rows and their
# consequences; this module keeps the public names (`Injury`, `injury_for_roll`, `clamp_injury_roll`)
# that earlier callers used, so the consolidation is invisible to them.
Injury = MajorInjury


def major_injury_risk(*, lethal: bool, hit_points: int, traumatic_this_scene: bool) -> bool:
    """SRD 2.5.6: lethal damage to zero HP, in a scene where a Traumatic Hit already landed.

    All three conditions are required. Zero HP from a non-lethal beating, or from lethal damage in a
    scene with no Traumatic Hit, does **not** put the subject on this table.
    """
    return lethal and hit_points <= 0 and traumatic_this_scene


def resolve_downed(
    *,
    lethal: bool,
    hit_points: int,
    traumatic_this_scene: bool,
    level: int,
    attributes: Mapping[str, int],
    save_bonus: int = 0,
    save_die: int | None = None,
    injury_roll: int | None = None,
    rng: Any = None,
) -> dict[str, Any]:
    """What happens when a subject reaches zero hit points.

    Returns ``{"at_risk", "mortally_wounded", "saved", "injury"}``. A subject at risk who passes the
    **Physical** save is still *Mortally Wounded* — they may be stabilized and recover normally — but
    takes no Major Injury. A subject not at risk is simply down.
    """
    at_risk = major_injury_risk(lethal=lethal, hit_points=hit_points,
                                traumatic_this_scene=traumatic_this_scene)
    if not at_risk:
        return {"at_risk": False, "mortally_wounded": hit_points <= 0,
                "saved": None, "injury": None, "injury_roll": None}

    save = saving_throw("Physical", level=level, attributes=attributes,
                        bonus=save_bonus, rng=rng, die=save_die)
    if save.success:
        return {"at_risk": True, "mortally_wounded": True, "saved": True,
                "injury": None, "injury_roll": None}

    if injury_roll is None:
        source = rng if rng is not None else random.Random()
        injury_roll = source.randint(INJURY_MIN, INJURY_MAX)
    roll = clamp_injury_roll(int(injury_roll))
    return {"at_risk": True, "mortally_wounded": True, "saved": False,
            "injury": injury_for_roll(roll), "injury_roll": roll}

# --------------------------------------------------------------------------- #
# System Strain and cyberware (SRD 3.6.x)
# --------------------------------------------------------------------------- #
# Capacity: "A healthy character normally starts at zero System Strain and has their Constitution
# score as their allowed maximum." Cyberware adds PERMANENT strain (which may be fractional); healing
# and chems add ordinary strain that recovers. The two are the same counter -- permanent strain simply
# never comes back while the implant is in.

#: Lifestyle modifies the maximum (SRD 3.5.2 cost-of-living table). The $1,000 "ordinary" life is +0.
LIFESTYLE_STRAIN: dict[str, int] = {
    "squatter": -2,   # abandoned building
    "slum": -1,       # dirty shared apartment
    "ordinary": 0,
    "fine": 1,        # clean, secure building
    "luxury": 2,
}


def strain_maximum(constitution: int, *, lifestyle: str = "ordinary") -> int:
    """Allowed maximum System Strain = Constitution score, adjusted by lifestyle.

    Never below zero: a squatter with Con 3 has a maximum of 1, not -1.
    """
    if lifestyle not in LIFESTYLE_STRAIN:
        raise CwnError(f"unknown lifestyle {lifestyle!r}; expected one of {sorted(LIFESTYLE_STRAIN)}")
    if not 3 <= constitution <= 18:
        raise CwnError("Constitution must be within the Without Number range 3-18")
    return max(0, constitution + LIFESTYLE_STRAIN[lifestyle])


#: SRD 3.6.1 installation table: (upper bound of the strain band, cost, recovery, difficulty).
#: The bands are inclusive at the upper bound; 3.1 or more is the open-ended last band.
INSTALL_BANDS: tuple[tuple[float | None, int, str, int], ...] = (
    (0.0, 100, "1 hour", 7),
    (0.5, 500, "1 day", 8),
    (1.0, 2500, "4 days", 10),
    (3.0, 12500, "2 weeks", 11),
    (None, 50000, "1 month", 12),
)


def installation_terms(strain: float) -> dict[str, Any]:
    """Cost, recovery time and surgery difficulty for an implant of a given strain cost (SRD 3.6.1)."""
    if strain < 0:
        raise CwnError("System Strain cost cannot be negative")
    for upper, cost, recovery, difficulty in INSTALL_BANDS:
        if upper is None or strain <= upper:
            return {"strain": strain, "cost": cost, "recovery": recovery, "difficulty": difficulty}
    raise AssertionError("unreachable: the last band is open-ended")


def can_accept_implant(*, current_strain: float, implant_strain: float, maximum: int) -> bool:
    """SRD 3.6.1: "A subject cannot accept cyber if it would put their System Strain above their maximum"."""
    return current_strain + implant_strain <= maximum


def resolve_implant_surgery(
    *,
    strain: float,
    current_strain: float,
    maximum: int,
    check_total: int,
    difficulty: int | None = None,
) -> dict[str, Any]:
    """The outcome of implant surgery.

    Three outcomes, and the third is the one that is easy to forget:

    * the implant is refused outright if the strain would exceed the maximum -- no roll happens;
    * the check succeeds at or above the difficulty -> implanted, strain becomes permanent;
    * the check fails by **two or less** -> the surgery simply fails;
    * the check fails by **more than two** -> "the surgery is unsuccessful, the target's System Strain
      is maximized, and the target is reduced to 1 hit point" (SRD 3.6.1).
    """
    if not can_accept_implant(current_strain=current_strain, implant_strain=strain, maximum=maximum):
        return {"outcome": "refused", "strain_after": current_strain, "hit_points": None,
                "detail": "implant would exceed the subject's maximum System Strain"}

    need = installation_terms(strain)["difficulty"] if difficulty is None else difficulty
    if check_total >= need:
        return {"outcome": "installed", "strain_after": current_strain + strain,
                "hit_points": None, "detail": f"check {check_total} vs difficulty {need}"}

    shortfall = need - check_total
    if shortfall > 2:
        return {"outcome": "catastrophic", "strain_after": maximum, "hit_points": 1,
                "detail": f"failed by {shortfall}; System Strain maximized, reduced to 1 hit point"}
    return {"outcome": "failed", "strain_after": current_strain, "hit_points": None,
            "detail": f"failed by {shortfall}; implant not installed"}


def maintenance_minutes(strain: float) -> int:
    """SRD 3.6.4: upkeep takes hours equal to the system's System Strain, minimum fifteen minutes."""
    if strain < 0:
        raise CwnError("System Strain cost cannot be negative")
    return max(15, round(strain * 60))


def maintenance_overdue(months_since_upkeep: float) -> bool:
    """SRD 3.6.4: "If a system goes more than a month without upkeep, it starts to malfunction"."""
    return months_since_upkeep > 1


def first_aid(*, heal_skill: int = 0, die: int | None = None, rng: Any = None) -> dict[str, Any]:
    """SRD 2.5.1: a medkit patch-up restores ``1d6 + Heal``, or ``1d6 - 1`` with no Heal skill at all.

    Every application adds one System Strain to the target -- the cost the SRD makes easy to skip.
    """
    if heal_skill < 0:
        raise CwnError("Heal skill cannot be negative")
    roll: int
    if die is None:
        roll = (rng if rng is not None else random.Random()).randint(1, 6)
    else:
        if not 1 <= die <= 6:
            raise CwnError("first aid uses a d6")
        roll = die
    healed = max(0, roll + heal_skill if heal_skill > 0 else roll - 1)
    return {"roll": roll, "healed": healed, "strain_cost": 1}
