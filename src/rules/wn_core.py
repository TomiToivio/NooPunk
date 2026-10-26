"""The Without Number kernel, adopted as NoöPunk's baseline.

**Author ruling, 2026-10-26:** *"use CWN/SWN/AWN/WWN system for everything. Make the stats,
skills, all rules based on them. We will modify later."* This module is the arithmetic of that
decision, and it supersedes the earlier "`1d10` stays" ruling (#566 / D40) for the tabletop layer.

What is implemented here is what was **verified against the SRD**, not what seemed plausible:

* six attributes on a 3-18 scale (``1.1.1``), and the modifier bands from ``1.1.2``;
* the skill check as ``2d6 + attribute modifier + skill level`` against a difficulty;
* the difficulty bands ``6 / 8 / 10 / 12 / 14`` (``2.3.1``);
* situational circumstances bounded at ``-2..+2``, aid capped at ``+1``, opposed checks won by the
  higher roll (``2.3.3``/``2.3.4``);
* combat: attack rolls, Shock, Trauma, Damage Soak, mortal injury and stabilization, the Major
  Injury table (``2.4``, ``2.5.1``, ``2.5.2``);
* injury and recovery: System Strain, first aid, natural healing, Frailty (``2.5.3`` - ``2.5.5``);
* cyberware: installation bands, maintenance, the optional alienation rule (``3.6``);
* hacking: Access, security levels, connection penalties, cyberware and drone difficulty, the
  alert counter (``4.x``);
* encumbrance, advancement, and the NPC stat-line conventions.

**Deliberately absent:** Edges, Foci, the equipment catalogue as data, drones, vehicles, faction
turns and the magic options. Each needs its own verified reading, and inventing any of them would
put a number in the repo that no source supports. The equipment catalogue, drones and vehicles are
data work tracked in ``docs/rules/CWN_CONVERSION.md``; Edges and Foci are content the author owns.

Provenance: mechanics taken from the *Cities Without Number* SRD, which is CC0 (verified
2026-10-25 in ``data/sources/game_system_rights.json``), with the Effort pool shape from the
*Worlds Without Number* SRD, also CC0. *Stars Without Number* and *Ashes Without Number* have no
verified SRD and remain ``blocked-unverified`` — the psionic mechanics in ``src/rules/psionics.py``
are an independent expression of their shape and cite neither source's text. No SRD prose is
reproduced; the expression here is original.
"""
from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

#: The six attribute names, in the SRD's order. These replace NooPunk's earlier
#: FIT/REF/INT/SOC/CYB/PSY set for the tabletop layer, by author ruling 2026-10-26.
ATTRIBUTES: tuple[str, ...] = (
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma",
)

#: Short codes for the same six attributes, used by saves and by the migration map.
ATTRIBUTE_CODES: tuple[str, ...] = tuple(name[:3].upper() for name in ATTRIBUTES)

#: The CWN skill list. A skill never carries a fixed attribute: the attribute is chosen for the
#: action being attempted, which is why this tuple has no bindings attached to it.
SKILLS: tuple[str, ...] = (
    "Administer",
    "Connect",
    "Drive",
    "Exert",
    "Fix",
    "Heal",
    "Know",
    "Lead",
    "Notice",
    "Perform",
    "Program",
    "Punch",
    "Shoot",
    "Sneak",
    "Stab",
    "Survive",
    "Talk",
    "Trade",
    "Work",
)

#: The psionic disciplines, which are specialist skills rather than an ordinary free pick.
PSIONIC_SKILLS: tuple[str, ...] = (
    "Biopsionics",
    "Metapsionics",
    "Precognition",
    "Telekinesis",
    "Telepathy",
    "Teleportation",
)

ATTRIBUTE_MIN = 3
ATTRIBUTE_MAX = 18
MODIFIER_CAP = 2

#: Difficulty bands, verified from SRD 2.3.1. Names paraphrase the SRD's own descriptions.
DIFFICULTY_SIMPLE = 6        # still more than the PC's background would cover
DIFFICULTY_SIGNIFICANT = 8   # a competent professional, succeeding more often than not
DIFFICULTY_EXPERT = 10       # beyond anyone but a skilled expert
DIFFICULTY_MASTER = 12       # only a true master, reliably
DIFFICULTY_EXTREME = 14      # only a true master, and probably failing

SITUATIONAL_MIN = -2
SITUATIONAL_MAX = 2
AID_BONUS_MAX = 1

SKILL_CHECK_DICE = 2
SKILL_CHECK_FACES = 6

#: No level-0 in the skill: the SRD applies -1. Level-0 itself is basic competence, not a penalty.
UNSKILLED_PENALTY = -1

#: Trained skill levels run 0..4. A character with no level-0 at all is *untrained*, recorded as
#: ``UNTRAINED``; the two states are different and the kernel never conflates them.
SKILL_MIN_LEVEL = 0
MAX_SKILL_LEVEL = 4
UNTRAINED = UNSKILLED_PENALTY


class WnError(ValueError):
    """A constraint from the SRD was about to be violated."""


def attribute_modifier(score: int) -> int:
    """The modifier for an attribute score (SRD 1.1.2).

    3 -> -2, 4-7 -> -1, 8-13 -> +0, 14-17 -> +1, 18 -> +2.

    The +/-2 bound is the *base* modifier cap; abilities may raise it, which is why the
    cap is applied here as a band rather than clamped on the result.
    """
    if not ATTRIBUTE_MIN <= score <= ATTRIBUTE_MAX:
        raise WnError(f"attribute score must be {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX}, got {score}")
    if score <= 3:
        return -2
    if score <= 7:
        return -1
    if score <= 13:
        return 0
    if score <= 17:
        return 1
    return 2


def clamp_situational(value: int) -> int:
    """Circumstances adjust a check by at most -2..+2 (SRD 2.3.1).

    Gear mods, magic items and aid are explicitly outside this bound, so only caller-supplied
    circumstance lives here. Clamping rather than raising keeps a referee's table moving.
    """
    return max(SITUATIONAL_MIN, min(SITUATIONAL_MAX, value))


def clamp_aid(value: int) -> int:
    """Aid tops out at +1 however many allies help (SRD 2.3.3)."""
    return max(0, min(AID_BONUS_MAX, value))


@dataclass(frozen=True)
class Check:
    """One resolved skill check."""

    dice: tuple[int, int]
    attribute_modifier: int
    skill_level: int
    situational: int
    aid: int
    difficulty: int
    #: True when the character does not even have level-0 in the skill: the SRD's -1 applies.
    untrained: bool = False
    #: Flat modifiers that are *not* circumstances: a hacking Verb's own modifier, and the
    #: connection penalties for a wireless link or a VR crown. The SRD's -2..+2 bound covers
    #: circumstances, not gear or connection quality, so folding these into `situational` would
    #: silently swallow the third point of a wireless-plus-crown penalty.
    misc: int = 0

    @property
    def total(self) -> int:
        return (sum(self.dice) + self.attribute_modifier + self.skill_level
                + self.situational + self.aid + self.misc
                + (UNSKILLED_PENALTY if self.untrained else 0))

    @property
    def success(self) -> bool:
        return self.total >= self.difficulty

    @property
    def margin(self) -> int:
        return self.total - self.difficulty


def _roll(rng: Any = None, dice: Sequence[int] | None = None) -> tuple[int, int]:
    if dice is not None:
        pair = tuple(int(d) for d in dice)
        if len(pair) != 2 or any(not 1 <= d <= SKILL_CHECK_FACES for d in pair):
            raise WnError(f"each die must be 1..{SKILL_CHECK_FACES}, got {dice}")
        return pair  # type: ignore[return-value]
    source = rng if rng is not None else random.Random()
    return (source.randint(1, SKILL_CHECK_FACES), source.randint(1, SKILL_CHECK_FACES))


def skill_check(
    *,
    attribute_score: int,
    skill_level: int | None,
    difficulty: int,
    situational: int = 0,
    aid: int = 0,
    misc: int = 0,
    rng: Any = None,
    dice: Sequence[int] | None = None,
) -> Check:
    """`2d6 + attribute modifier + skill level` against a difficulty.

    The dice may be supplied directly (`dice=(3, 5)`) for a table that rolled real dice, or a
    seeded `rng` may be passed for a replayable digital resolution. `misc` carries flat modifiers
    that are not circumstances (gear, connection quality, a Verb's own modifier) and is deliberately
    not clamped to the situational bound.
    """
    if skill_level is None:
        untrained = True
        level = 0
    else:
        untrained = False
        if skill_level < 0:
            raise WnError(f"skill level cannot be negative, got {skill_level}")
        level = int(skill_level)
    return Check(
        dice=_roll(rng, dice),
        attribute_modifier=attribute_modifier(attribute_score),
        skill_level=level,
        untrained=untrained,
        situational=clamp_situational(situational),
        aid=clamp_aid(aid),
        misc=int(misc),
        difficulty=difficulty,
    )


def opposed_check(
    *,
    a: Sequence[int],
    b: Sequence[int],
) -> str | None:
    """Opposed checks: the higher roll wins (SRD 2.3.4).

    Returns "a", "b", or **None on a tie** — the SRD states the winner is the one who rolls
    higher and does not say what a tie means, so this reports the ambiguity instead of inventing
    a tie-break. A caller that needs one must supply its own procedure.
    """
    ta, tb = sum(a), sum(b)
    if ta == tb:
        return None
    return "a" if ta > tb else "b"


# --------------------------------------------------------------------------- #
# Saving throws (CWN SRD 2.02)
# --------------------------------------------------------------------------- #

SAVE_DIE = 20
SAVE_TARGET_BASE = 16
SAVE_TYPES: tuple[str, ...] = ("physical", "evasion", "mental", "luck")


@dataclass(frozen=True)
class Save:
    """One resolved saving throw."""

    kind: str
    target: int
    die: int
    natural: bool

    @property
    def success(self) -> bool:
        return (self.die >= self.target) if not self.natural else self.die == SAVE_DIE


def save_target(
    kind: str,
    *,
    level: int = 1,
    modifiers: dict[str, int] | None = None,
) -> int:
    """``16 - level - the higher of the two listed attribute modifiers``; Luck has none.

    The SRD subtracts *character level*, which is why an unlevelled character (level 1 here) has a
    harder target than a veteran. The two modifiers are the category's own pair — Physical uses
    Strength or Constitution, Evasion Dexterity or Intelligence, Mental Wisdom or Charisma.
    """
    key = _require_save(kind)
    attrs = SAVE_ATTRIBUTES[key]
    mods = modifiers or {}
    best = max((int(mods.get(attr, 0)) for attr in attrs), default=0) if attrs else 0
    return SAVE_TARGET_BASE - int(level) - best


def roll_save(
    kind: str,
    *,
    level: int = 1,
    modifiers: dict[str, int] | None = None,
    rng: Any = None,
    die: int | None = None,
) -> Save:
    """Roll a save: a natural 1 always fails and a natural 20 always succeeds."""
    key = _require_save(kind)
    target = save_target(key, level=level, modifiers=modifiers)
    source = rng if rng is not None else random.Random()
    rolled = source.randint(1, SAVE_DIE) if die is None else int(die)
    if not 1 <= rolled <= SAVE_DIE:
        raise WnError(f"a save roll must be 1..{SAVE_DIE}, got {rolled}")
    return Save(kind=key, target=target, die=rolled, natural=rolled in (1, SAVE_DIE))


SAVE_ATTRIBUTES: dict[str, tuple[str, ...]] = {
    "physical": ("STR", "CON"),
    "evasion": ("DEX", "INT"),
    "mental": ("WIS", "CHA"),
    "luck": (),
}


def _require_save(kind: str) -> str:
    key = str(kind).lower()
    if key not in SAVE_TYPES:
        raise WnError(f"unknown save type {kind!r}; expected one of {SAVE_TYPES}")
    return key


# --------------------------------------------------------------------------- #
# Combat (CWN SRD 2.4)
# --------------------------------------------------------------------------- #

ATTACK_DIE = 20
ATTACK_MOVEMENT_METERS = 10
#: No level-0 in the weapon's combat skill: the SRD applies -2 to the attack, not -1.
UNSKILLED_ATTACK_PENALTY = -2
#: A normal unarmored human is hit traumatically on a Trauma Die of 6 or more.
DEFAULT_TRAUMA_TARGET = 6
#: Rounds a mortally wounded character survives without stabilization.
MORTAL_ROUNDS = 6


@dataclass(frozen=True)
class Attack:
    """One resolved attack roll (CWN SRD 2.4.1)."""

    die: int
    attack_bonus: int
    attribute_modifier: int
    skill_level: int
    situational: int
    target_ac: int
    untrained: bool = False

    @property
    def total(self) -> int:
        return (self.die + self.attack_bonus + self.attribute_modifier
                + self.skill_level + self.situational
                + (UNSKILLED_ATTACK_PENALTY if self.untrained else 0))

    @property
    def natural(self) -> bool:
        return self.die in (1, ATTACK_DIE)

    @property
    def success(self) -> bool:
        """A natural 1 always misses, a natural 20 always hits, otherwise total >= AC."""
        if self.die == 1:
            return False
        if self.die == ATTACK_DIE:
            return True
        return self.total >= self.target_ac


def attack_roll(
    *,
    attack_bonus: int,
    target_ac: int,
    attribute_modifier: int = 0,
    skill_level: int = 0,
    untrained: bool = False,
    situational: int = 0,
    rng: Any = None,
    die: int | None = None,
) -> Attack:
    """``d20 + attack bonus + attribute modifier + combat skill`` against Melee or Ranged AC."""
    if not untrained and skill_level < 0:
        raise WnError(f"combat skill level cannot be negative, got {skill_level}")
    source = rng if rng is not None else random.Random()
    rolled = source.randint(1, ATTACK_DIE) if die is None else int(die)
    if not 1 <= rolled <= ATTACK_DIE:
        raise WnError(f"an attack roll must be 1..{ATTACK_DIE}, got {rolled}")
    return Attack(
        die=rolled,
        attack_bonus=int(attack_bonus),
        attribute_modifier=int(attribute_modifier),
        skill_level=0 if untrained else int(skill_level),
        untrained=untrained,
        situational=clamp_situational(situational),
        target_ac=int(target_ac),
    )


@dataclass(frozen=True)
class Weapon:
    """The part of a weapon's stat line the resolution needs.

    ``shock_ac=None`` means the weapon's Shock applies regardless of the target's Armor Class,
    which the source records as ``Shock N/-``. ``trauma_die=None`` means the weapon rolls no Trauma
    Die at all (non-lethal attacks and unarmed strikes).
    """

    name: str
    damage_count: int = 1
    damage_sides: int = 6
    damage_bonus: int = 0
    attribute: str = "DEX"
    shock: int = 0
    shock_ac: int | None = None
    trauma_die: int | None = None
    trauma_rating: int = 1

    def shock_applies(self, target_melee_ac: int) -> bool:
        """Shock lands on a miss only if the target's melee AC is low enough (or unlimited)."""
        if self.shock <= 0:
            return False
        if self.shock_ac is None:
            return True
        return target_melee_ac <= self.shock_ac


@dataclass(frozen=True)
class Hit:
    """The outcome of one attack, including what happened on a miss."""

    hit: bool
    damage: int
    traumatic: bool
    shock_damage: int
    trauma_roll: int | None
    trauma_target: int

    @property
    def total_damage(self) -> int:
        return self.damage if self.hit else self.shock_damage


def resolve_attack(
    attack: Attack,
    weapon: Weapon,
    *,
    attribute_modifier: int = 0,
    target_melee_ac: int | None = None,
    trauma_target: int = DEFAULT_TRAUMA_TARGET,
    non_lethal: bool = False,
    rng: Any = None,
    damage_dice: Sequence[int] | None = None,
    trauma_roll: int | None = None,
) -> Hit:
    """Apply CWN's damage, Shock and Trauma procedures to a resolved attack roll.

    * A hit does ``weapon damage + attribute modifier``, multiplied by the Trauma Rating on a
      Traumatic Hit, and can never do less than the Shock the weapon would have inflicted on a miss.
    * A miss still does the weapon's Shock if the target's melee AC is within the Shock rating.
    * Non-lethal attacks never roll the Trauma Die.
    """
    melee_ac = int(target_melee_ac if target_melee_ac is not None
                   else attack.target_ac)
    shock_applies = weapon.shock_applies(melee_ac)
    shock_damage = weapon.shock + attribute_modifier if shock_applies else 0
    shock_damage = max(0, shock_damage)

    if not attack.success:
        return Hit(hit=False, damage=0, traumatic=False, shock_damage=shock_damage,
                   trauma_roll=None, trauma_target=trauma_target)

    source = rng if rng is not None else random.Random()
    if damage_dice is not None:
        faces = tuple(int(f) for f in damage_dice)
        if len(faces) != weapon.damage_count or any(not 1 <= f <= weapon.damage_sides for f in faces):
            raise WnError(f"{weapon.name} rolls {weapon.damage_count}d{weapon.damage_sides}, got {damage_dice}")
    else:
        faces = tuple(source.randint(1, weapon.damage_sides) for _ in range(weapon.damage_count))
    damage = sum(faces) + attribute_modifier + weapon.damage_bonus
    damage = max(damage, shock_damage)

    rolled_trauma: int | None = None
    traumatic = False
    trauma_sides = weapon.trauma_die
    if trauma_sides is not None and not non_lethal:
        if trauma_roll is None:
            rolled_trauma = source.randint(1, trauma_sides)
        else:
            rolled_trauma = int(trauma_roll)
            if not 1 <= rolled_trauma <= trauma_sides:
                raise WnError(f"a Trauma Die for {weapon.name} is 1..{trauma_sides}, got {rolled_trauma}")
        traumatic = rolled_trauma >= trauma_target
        if traumatic:
            damage *= max(1, weapon.trauma_rating)

    return Hit(hit=True, damage=damage, traumatic=traumatic, shock_damage=shock_damage,
               trauma_roll=rolled_trauma, trauma_target=trauma_target)


class DamageSoak:
    """Armor's Damage Soak: it absorbs damage first and ablates for the rest of the fight."""

    def __init__(self, amount: int) -> None:
        if amount < 0:
            raise WnError(f"Damage Soak cannot be negative, got {amount}")
        self.initial = int(amount)
        self.remaining = int(amount)

    def take(self, damage: int) -> int:
        """Absorb what it can and return the damage that reaches the wearer."""
        if damage < 0:
            raise WnError(f"damage cannot be negative, got {damage}")
        absorbed = min(self.remaining, damage)
        self.remaining -= absorbed
        return damage - absorbed

    def refresh(self) -> None:
        """Refreshes after combat is over."""
        self.remaining = self.initial

    @property
    def depleted(self) -> bool:
        return self.remaining == 0


def stabilize_difficulty(rounds_since_fall: int, *, has_tools: bool = True) -> int:
    """``8 + full rounds since the target fell``; +2 without a medkit (CWN SRD 2.5.2)."""
    if rounds_since_fall < 0:
        raise WnError(f"rounds since the fall cannot be negative, got {rounds_since_fall}")
    return 8 + int(rounds_since_fall) + (0 if has_tools else 2)


@dataclass
class MortalWound:
    """A character at zero hit points from lethal damage (CWN SRD 2.5.2)."""

    rounds_since_fall: int = 0
    stabilized: bool = False
    frail: bool = False

    def tick(self) -> bool:
        """Advance one round. Returns True if the character dies now."""
        if not self.stabilized:
            self.rounds_since_fall += 1
        return self.dead

    @property
    def dead(self) -> bool:
        return not self.stabilized and self.rounds_since_fall > MORTAL_ROUNDS

    def stabilize(self) -> None:
        self.stabilized = True

    def recover(self) -> int:
        """Stabilized characters recover after ten minutes with 1 hit point and the Frail condition."""
        if not self.stabilized:
            raise WnError("a character cannot recover from a mortal wound before being stabilized")
        self.frail = True
        return 1


#: The Major Injury table (CWN SRD 2.5.1). Rolled only after a failed Physical save.
MAJOR_INJURIES: dict[int, str] = {
    1: "instant_death",
    2: "internal_damage",
    3: "brain_damage",
    4: "eye_damage",
    5: "gut_wound",
    6: "right_leg_ruined",
    7: "left_leg_ruined",
    8: "right_arm_ruined",
    9: "left_arm_ruined",
    10: "system_damage",
    11: "flesh_wound",
    12: "flesh_wound",
}


def major_injury(die: int) -> str:
    """Roll 1d12 on the Major Injury table, clamped to 1..12 as the source requires."""
    clamped = max(1, min(12, int(die)))
    return MAJOR_INJURIES[clamped]


def major_injury_risked(*, traumatic_hit_this_scene: bool, lethal_zero_hp: bool) -> bool:
    """A Major Injury is risked only when lethal damage drops a traumatically-hit character to zero."""
    return bool(traumatic_hit_this_scene and lethal_zero_hp)


# --------------------------------------------------------------------------- #
# System Strain and healing (CWN SRD 2.5.3 - 2.5.5)
# --------------------------------------------------------------------------- #

STRAIN_PER_REST_NIGHT = 1
FIRST_AID_STRAIN_COST = 1
FRAIL_FIELD_DIFFICULTY = 10


@dataclass
class SystemStrain:
    """System Strain: maximum is CON, cyberware occupies part of it permanently."""

    constitution: int
    permanent: float = 0.0
    current: float = 0.0

    def __post_init__(self) -> None:
        if not ATTRIBUTE_MIN <= self.constitution <= ATTRIBUTE_MAX:
            raise WnError(f"constitution must be {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX}, got {self.constitution}")
        if self.permanent < 0 or self.current < 0:
            raise WnError("System Strain cannot be negative")
        if self.permanent > self.maximum:
            raise WnError("permanent System Strain cannot exceed the maximum")

    @property
    def maximum(self) -> float:
        return float(self.constitution)

    @property
    def available(self) -> float:
        return self.maximum - self.current

    def can_accept(self, amount: float) -> bool:
        """Cyberware, drugs and powers that would cross the maximum cannot be used at all."""
        if amount < 0:
            raise WnError("System Strain cannot be negative")
        return self.current + amount <= self.maximum

    def add(self, amount: float) -> bool:
        """Add Strain. Returns True if it was accepted; False means the effect is unusable."""
        if amount < 0:
            raise WnError("System Strain cannot be negative")
        if not self.can_accept(amount):
            return False
        self.current += amount
        return True

    def forced(self, amount: float) -> bool:
        """An unavoidable effect: returning True means the character is unconscious for an hour."""
        if amount < 0:
            raise WnError("System Strain cannot be negative")
        self.current += amount
        return self.current > self.maximum

    def rest_night(self) -> None:
        self.current = max(0.0, self.current - STRAIN_PER_REST_NIGHT)


def first_aid_healing(*, heal_skill: int | None, rng: Any = None, die: int | None = None) -> int:
    """``1d6 + Heal``, or ``1d6 - 1`` with no Heal skill at all (CWN SRD 2.5.5)."""
    source = rng if rng is not None else random.Random()
    rolled = source.randint(1, 6) if die is None else int(die)
    if not 1 <= rolled <= 6:
        raise WnError(f"a first-aid die is 1..6, got {rolled}")
    if heal_skill is None:
        return rolled - 1
    if heal_skill < 0:
        raise WnError(f"Heal skill cannot be negative, got {heal_skill}")
    return rolled + heal_skill


def natural_healing(*, level: int, is_npc: bool = False, hit_dice: int | None = None, frail: bool = False) -> int:
    """Per night: the character's level (NPCs: hit dice). Frail characters heal nothing."""
    if frail:
        return 0
    if is_npc:
        if hit_dice is None:
            raise WnError("an NPC needs hit dice to heal naturally")
        return max(0, int(hit_dice))
    if level < 1:
        raise WnError(f"level must be positive, got {level}")
    return int(level)


def frail_field_removal_difficulty(*, has_medkit: bool = True) -> int:
    """A physician's single attempt to remove Frailty: difficulty 10 with a medkit and an hour."""
    return FRAIL_FIELD_DIFFICULTY + (0 if has_medkit else 2)


# --------------------------------------------------------------------------- #
# Cyberware installation, maintenance and alienation (CWN SRD 3.6)
# --------------------------------------------------------------------------- #

#: (maximum System Strain in the band, installation difficulty, cost in dollars, recovery time)
CYBERWARE_INSTALLATION: tuple[tuple[float | None, int, int, str], ...] = (
    (0.0, 7, 100, "1 hour"),
    (0.5, 8, 500, "1 day"),
    (1.0, 10, 2500, "4 days"),
    (3.0, 11, 12500, "2 weeks"),
    (None, 12, 50000, "1 month"),
)

CYBERWARE_MAINTENANCE_FRACTION = 0.05


def cyberware_installation(strain: float) -> dict[str, Any]:
    """The installation row a system of this System Strain falls into."""
    if strain < 0:
        raise WnError(f"System Strain cannot be negative, got {strain}")
    for max_strain, difficulty, cost, recovery in CYBERWARE_INSTALLATION:
        if max_strain is None or strain <= max_strain:
            return {"difficulty": difficulty, "cost": cost, "recovery": recovery}
    raise WnError(f"no installation band for System Strain {strain}")  # pragma: no cover


def installation_outcome(*, check_total: int, difficulty: int) -> str:
    """``success``, ``success_with_complication``, or ``failure`` per the SRD's margin rule."""
    margin = int(check_total) - int(difficulty)
    if margin >= 0:
        return "success"
    if margin >= -2:
        return "success_with_complication"
    return "failure"


def cyberware_maintenance_cost(base_cost: int) -> float:
    """Monthly upkeep is 5% of the system's base cost."""
    if base_cost < 0:
        raise WnError(f"a cost cannot be negative, got {base_cost}")
    return base_cost * CYBERWARE_MAINTENANCE_FRACTION


def alienation_exceeded(*, alienation: float, wisdom: int, syndrome_allowance: float = 0.0) -> bool:
    """The optional alienation rule: past WIS (plus syndromes) the character becomes an NPC."""
    return alienation > wisdom + syndrome_allowance


# --------------------------------------------------------------------------- #
# Hacking (CWN SRD 4.x)
# --------------------------------------------------------------------------- #

HACK_SECURITY_LEVELS: dict[int, str] = {
    7: "private home network",
    8: "small business, minor gang or minor government office",
    9: "corp branch office, major gang or important government facility",
    10: "corp high-security network",
    12: "corp or government black site",
}

WIRELESS_PENALTY = -2
VR_CROWN_PENALTY = -1
HACK_FAILURES_PER_ALERT = 2
ALERTS_TO_ALERT_NETWORK = 2


def access_pool(*, intelligence_modifier: int, program_skill: int, deck_bonus: int = 0) -> int:
    """``INT modifier + Program + the deck's bonus Access``, never negative."""
    if program_skill < 0:
        raise WnError(f"Program skill cannot be negative, got {program_skill}")
    return max(0, int(intelligence_modifier) + int(program_skill) + int(deck_bonus))


def cyber_hack_difficulty(*, level_or_hit_dice: int, has_operator: bool = True) -> int:
    """``7 + ceil(HD or level / 3)``; a drone with no operator is difficulty 8."""
    if not has_operator:
        return 8
    if level_or_hit_dice < 1:
        raise WnError(f"level or hit dice must be positive, got {level_or_hit_dice}")
    return 7 + (int(level_or_hit_dice) + 2) // 3


def hacking_difficulty(
    security: int,
    *,
    alerted: bool = False,
    important_device: bool = False,
    tech_quality: int = 0,
    inside_info: int = 0,
) -> int:
    """The network's security level plus the source's situation modifiers."""
    if security not in HACK_SECURITY_LEVELS:
        raise WnError(f"{security} is not a recorded security level; expected {sorted(HACK_SECURITY_LEVELS)}")
    difficulty = int(security)
    if alerted:
        difficulty += 1
    if important_device:
        difficulty += 1
    difficulty += int(tech_quality)
    difficulty -= int(inside_info)
    return difficulty


def hacking_check(
    *,
    intelligence_score: int,
    program_skill: int | None,
    difficulty: int,
    wireless: bool = False,
    vr_crown: bool = False,
    verb_modifier: int = 0,
    situational: int = 0,
    rng: Any = None,
    dice: Sequence[int] | None = None,
) -> Check:
    """The Int/Program check behind a Verb, with the connection penalties the source requires."""
    penalty = (WIRELESS_PENALTY if wireless else 0) + (VR_CROWN_PENALTY if vr_crown else 0)
    return skill_check(
        attribute_score=intelligence_score,
        skill_level=program_skill,
        difficulty=difficulty,
        situational=situational,
        misc=penalty + int(verb_modifier),
        rng=rng,
        dice=dice,
    )


@dataclass
class AlertCounter:
    """Every two failed checks count as one Alert action; two Alerts alert the network."""

    failures: int = 0
    alerts: int = 0

    def record_failure(self) -> bool:
        """Returns True when this failure completed a network alert."""
        self.failures += 1
        if self.failures % HACK_FAILURES_PER_ALERT == 0:
            self.alerts += 1
        return self.alerted

    @property
    def alerted(self) -> bool:
        return self.alerts >= ALERTS_TO_ALERT_NETWORK


# --------------------------------------------------------------------------- #
# Encumbrance (CWN SRD 2.3.x)
# --------------------------------------------------------------------------- #


def stowed_capacity(strength: int) -> int:
    """Stowed encumbrance points equal the Strength score."""
    if not ATTRIBUTE_MIN <= strength <= ATTRIBUTE_MAX:
        raise WnError(f"strength must be {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX}, got {strength}")
    return int(strength)


def readied_capacity(strength: int) -> int:
    """Readied points equal half the Strength score, rounded down."""
    return stowed_capacity(strength) // 2


def overload_stage(*, readied: int, stowed: int, strength: int) -> int:
    """0 = unencumbered, 1 = first overload (70% movement), 2 = second (50%), 3 = cannot haul.

    Overload is cumulative: the first push adds two Ready and four Stowed points, the second push
    adds another two and four on top of that. Anything beyond the second push cannot be hauled.
    """
    if readied < 0 or stowed < 0:
        raise WnError("encumbrance cannot be negative")
    readied_limit = readied_capacity(strength)
    stowed_limit = stowed_capacity(strength)
    if readied <= readied_limit and stowed <= stowed_limit:
        return 0
    for stage in (1, 2):
        if readied <= readied_limit + 2 * stage and stowed <= stowed_limit + 4 * stage:
            return stage
    return 3


def movement_for_stage(stage: int) -> int:
    """Movement in metres for an overload stage, from the base 10 metres."""
    multipliers = {0: 1.0, 1: 0.7, 2: 0.5}
    if stage not in multipliers:
        return 0
    return int(ATTACK_MOVEMENT_METERS * multipliers[stage])


# --------------------------------------------------------------------------- #
# Advancement (CWN SRD 1.9)
# --------------------------------------------------------------------------- #

MAX_LEVEL = 10
XP_FAST: tuple[int, ...] = (0, 3, 6, 12, 18, 27, 39, 54, 72, 93)
XP_SLOW: tuple[int, ...] = (0, 6, 15, 24, 36, 51, 69, 87, 105, 139)
SKILL_POINTS_PER_LEVEL = 3
EDUCATED_BONUS_POINT = 1
#: Points to buy each skill level, and the character level needed to buy it.
SKILL_COSTS: tuple[tuple[int, int, int], ...] = (
    (0, 1, 1),
    (1, 2, 1),
    (2, 3, 3),
    (3, 4, 6),
    (4, 5, 9),
)
ATTRIBUTE_IMPROVEMENT_COSTS: tuple[int, ...] = (1, 2, 3, 4, 5)
ATTRIBUTE_IMPROVEMENT_MIN_LEVELS: tuple[int, ...] = (1, 1, 3, 6, 9)
FOCUS_LEVELS: tuple[int, ...] = (2, 5, 7, 10)
THIRD_EDGE_LEVEL = 5


def level_for_xp(xp: int, *, track: str = "fast") -> int:
    """The highest level whose threshold the accumulated XP has reached."""
    if xp < 0:
        raise WnError(f"experience cannot be negative, got {xp}")
    table = XP_FAST if track == "fast" else XP_SLOW
    if track not in ("fast", "slow"):
        raise WnError(f"unknown XP track {track!r}; expected 'fast' or 'slow'")
    level = 1
    for index, threshold in enumerate(table):
        if xp >= threshold:
            level = index + 1
    return level


def attack_bonus(*, level: int, on_target_edge: bool = False) -> int:
    """Half the character level, rounded down; the On Target Edge makes it the full level."""
    if level < 1:
        raise WnError(f"level must be positive, got {level}")
    return int(level) if on_target_edge else int(level) // 2


def skill_point_cost(skill_level: int) -> int:
    for level, points, _minimum in SKILL_COSTS:
        if level == skill_level:
            return points
    raise WnError(f"no skill level {skill_level}; levels are 0..4")


def minimum_level_for_skill(skill_level: int) -> int:
    for level, _points, minimum in SKILL_COSTS:
        if level == skill_level:
            return minimum
    raise WnError(f"no skill level {skill_level}; levels are 0..4")


def hit_points_gain(
    *,
    level: int,
    constitution_modifier: int,
    hard_to_kill: bool = False,
    current_maximum: int | None = None,
    rng: Any = None,
    dice: Sequence[int] | None = None,
) -> int:
    """Roll ``1d6 + CON`` per character level; a roll that does not beat the old maximum adds 1.

    Each die is floored at 1 after the modifier is applied, which is why a CON penalty cannot
    produce a zero-point level.
    """
    if level < 1:
        raise WnError(f"level must be positive, got {level}")
    sides = 8 if hard_to_kill else 6
    bonus = 2 if hard_to_kill else 0
    source = rng if rng is not None else random.Random()
    if dice is not None:
        faces = tuple(int(d) for d in dice)
        if len(faces) != level or any(not 1 <= f <= sides for f in faces):
            raise WnError(f"expected {level} dice of 1..{sides}, got {dice}")
    else:
        faces = tuple(source.randint(1, sides) for _ in range(level))
    total = sum(max(1, face + bonus + constitution_modifier) for face in faces)
    if current_maximum is None:
        return total
    return total if total > current_maximum else 1


# --------------------------------------------------------------------------- #
# Migration from the transitional 1d10 layer
# --------------------------------------------------------------------------- #

#: The six legacy STATs folded onto the family's six attributes. CYB and PSY have no attribute of
#: their own: cybernetic and psychic capacity become skills, Edges and permissions (migration step M4).
LEGACY_STAT_MAP: dict[str, str] = {
    "FIT": "STR",
    "REF": "DEX",
    "INT": "INT",
    "SOC": "CHA",
    "CYB": "INT",
    "PSY": "WIS",
}


def from_legacy_stat(value: int) -> int:
    """Map a legacy 1..10 STAT onto a 3..18 attribute, preserving rank order (1 -> 3, 10 -> 18)."""
    value = int(value)
    if not 1 <= value <= 10:
        raise WnError(f"a legacy STAT is 1..10, got {value}")
    return ATTRIBUTE_MIN + round((value - 1) * (ATTRIBUTE_MAX - ATTRIBUTE_MIN) / 9)


def from_legacy_skill(value: int) -> int:
    """Map a legacy 1..10 skill rating onto a level 0..4 (1..2 -> 0, 3..4 -> 1, ... 9..10 -> 4)."""
    value = int(value)
    if not 1 <= value <= 10:
        raise WnError(f"a legacy skill rating is 1..10, got {value}")
    return min(4, (value - 1) // 2)
