"""Character creation on the CWN chassis: attributes and the skill pool.

Original implementation of the procedures in the Cities Without Number SRD,
character creation sections on Attributes and Skills. The prose here is ours;
no SRD text is reproduced.

Two things this layer settles that earlier design notes left open:

* **How attribute scores come to exist.** Either six 3d6 rolls taken in order -
  with one optional substitution of a 14 - or the fixed array, which forfeits
  that substitution. The two routes are exclusive on purpose, and the module
  enforces the exclusivity rather than trusting the caller to remember it.
* **What a starting skill level means.** The first time a skill is picked it
  becomes level-0, the second time level-1, and a third pick is not a third
  level: it must become some *other* skill that is not already level-1. No
  character begins play above level-1.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

from .wn_core import attribute_modifier

ATTRIBUTES = ("Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma")
ATTRIBUTE_MIN = 3
ATTRIBUTE_MAX = 18
DICE_PER_ATTRIBUTE = 3
ARRAY = (14, 12, 11, 10, 9, 7)
SUBSTITUTE_SCORE = 14
MAX_CREATION_SKILL_LEVEL = 1
MODIFIER_FLOOR = -2
MODIFIER_CEILING = 2


class CharacterRulesError(ValueError):
    """Raised when a call is outside the creation procedure."""


def roll_attributes(dice: Sequence[int]) -> dict[str, int]:
    """Six 3d6 rolls taken in order, one per attribute.

    Dice enter as values so a table roll and a replay agree; this function never
    rolls anything itself.
    """
    if len(dice) != len(ATTRIBUTES) * DICE_PER_ATTRIBUTE:
        raise CharacterRulesError(
            f"expected {len(ATTRIBUTES) * DICE_PER_ATTRIBUTE} dice, got {len(dice)}"
        )
    scores: dict[str, int] = {}
    for index, attribute in enumerate(ATTRIBUTES):
        chunk = dice[index * DICE_PER_ATTRIBUTE:(index + 1) * DICE_PER_ATTRIBUTE]
        for die in chunk:
            if not 1 <= die <= 6:
                raise CharacterRulesError(f"a d6 shows 1..6, got {die}")
        scores[attribute] = sum(chunk)
    return scores


def substitute_fourteen(
    scores: Mapping[str, int],
    attribute: str,
    *,
    already_substituted: bool = False,
    array_used: bool = False,
) -> dict[str, int]:
    """Replace one rolled score with 14.

    Available once, and never when the fixed array was used - the array is
    itself the concession, so taking both would be a better character than the
    rules offer.
    """
    if attribute not in ATTRIBUTES:
        raise CharacterRulesError(f"unknown attribute {attribute!r}")
    if array_used:
        raise CharacterRulesError("the array forfeits the substitute-fourteen option")
    if already_substituted:
        raise CharacterRulesError("only one score may be substituted")
    result = dict(scores)
    if set(result) != set(ATTRIBUTES):
        raise CharacterRulesError("all six attributes are required")
    result[attribute] = SUBSTITUTE_SCORE
    return result


def assign_array(assignment: Mapping[str, int]) -> dict[str, int]:
    """Assign the fixed array across the attributes.

    The assignment must be a permutation of the array: no inventing a better
    spread, and no dropping the low score.
    """
    if set(assignment) != set(ATTRIBUTES):
        raise CharacterRulesError("all six attributes are required")
    if sorted(assignment.values()) != sorted(ARRAY):
        raise CharacterRulesError(f"attributes must be a permutation of {ARRAY}")
    return {attribute: assignment[attribute] for attribute in ATTRIBUTES}


def effective_modifier(base_score: int, bonus: int = 0, *, uncapped: bool = False) -> int:
    """The attribute modifier, plus any Focus or cyberware bonus.

    Such bonuses cannot push the modifier past +2 or below -2 unless the source
    says explicitly that it may.
    """
    modifier = attribute_modifier(base_score) + bonus
    if uncapped:
        return modifier
    return max(MODIFIER_FLOOR, min(MODIFIER_CEILING, modifier))


class SkillPool:
    """The skill picks a character makes during creation.

    The third and later pick of a skill is not a level: it must be spent on a
    different skill that is not yet level-1. Tracking that here stops a caller
    from quietly handing out level-2 at creation.
    """

    def __init__(self) -> None:
        self.levels: dict[str, int] = {}

    def can_pick(self, skill: str) -> bool:
        if skill not in self.levels:
            return True
        if self.levels[skill] < MAX_CREATION_SKILL_LEVEL:
            return True
        return any(
            level < MAX_CREATION_SKILL_LEVEL
            for name, level in self.levels.items()
            if name != skill
        )

    def pick(self, skill: str) -> int:
        """Spend one pick; returns the resulting level.

        A skill already at level-1 cannot be picked again during creation - the
        pick has to go somewhere else, which is the caller's job to choose.
        """
        if not skill:
            raise CharacterRulesError("a skill needs a name")
        current = self.levels.get(skill)
        if current is None:
            self.levels[skill] = 0
            return 0
        if current < MAX_CREATION_SKILL_LEVEL:
            self.levels[skill] = current + 1
            return self.levels[skill]
        raise CharacterRulesError(
            f"{skill} is already level-{MAX_CREATION_SKILL_LEVEL}; pick another skill"
        )

    def open_skills(self) -> tuple[str, ...]:
        """Skills a surplus pick may legally be spent on."""
        return tuple(
            name for name, level in self.levels.items()
            if level < MAX_CREATION_SKILL_LEVEL
        )
