"""CWN attack-roll arithmetic for the NoöPunk detective RPG.

Implements only the shared d20 attack-versus-Armor-Class calculation.
Damage, Shock, Trauma, cover, initiative, weapons, special attacks and
situational exceptions remain separate CWN procedures. Do not substitute
this for the complete combat chapter.

The attacker's skill is a trained rank 0..4, or None if untrained.
Unlike general 2d6 skill checks, untrained attacks take a -2 penalty.
Both melee and ranged AC are passed explicitly by the caller; this
module never guesses which one a target has.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from .wn_core import WnError, attribute_modifier

UNTRAINED_ATTACK_PENALTY = -2
ATTACK_DIE_SIDES = 20


@dataclass(frozen=True)
class AttackResult:
    die: int
    attack_bonus: int
    attribute_modifier: int
    skill_modifier: int
    other_modifier: int
    armor_class: int

    @property
    def total(self) -> int:
        return (self.die + self.attack_bonus + self.attribute_modifier
                + self.skill_modifier + self.other_modifier)

    @property
    def hit(self) -> bool:
        return self.total >= self.armor_class

    @property
    def margin(self) -> int:
        return self.total - self.armor_class


def attack_roll(
    *,
    attribute_score: int,
    skill_level: int | None,
    attack_bonus: int,
    armor_class: int,
    other_modifier: int = 0,
    rng: Any = None,
    die: int | None = None,
) -> AttackResult:
    """Roll an attack or resolve an already supplied d20 result.

    `other_modifier` is supplied by the caller after consulting the
    relevant CWN equipment, maneuver, cover and situational rules.
    No automatic critical-hit, natural-1 or trauma behavior is assumed.
    """
    modifier = attribute_modifier(attribute_score)
    if skill_level is not None and (not isinstance(skill_level, int) or not 0 <= skill_level <= 4):
        raise WnError("attack skill must be None (untrained) or trained rank 0..4")
    if armor_class < 1:
        raise WnError("armor class must be positive")
    if die is None:
        roller = rng if rng is not None else random.Random()
        face = roller.randint(1, ATTACK_DIE_SIDES)
    else:
        face = int(die)
    if not 1 <= face <= ATTACK_DIE_SIDES:
        raise WnError("attack d20 face must be 1..20")
    return AttackResult(
        die=face, attack_bonus=int(attack_bonus), attribute_modifier=modifier,
        skill_modifier=UNTRAINED_ATTACK_PENALTY if skill_level is None else skill_level,
        other_modifier=int(other_modifier), armor_class=int(armor_class),
    )
