"""Canonical, engine-independent NoöPunk RPG rules.

RULEBOOK.md is the source of truth; this package consumes the authored values from
``data/rules/core.json`` rather than re-declaring them.

The skill-check engine is **2d6 + skill level + attribute modifier** against
6/8/10/12/14+ (RULEBOOK §4). The earlier 3d6 skill-check engine is withdrawn.
"""

from .core import (
    AID_BONUS_CAP,
    ATTRIBUTE_DEFINITIONS,
    ATTRIBUTE_IDS,
    AttributeSet,
    CHECK_DICE,
    CHECK_DICE_COUNT,
    CHECK_DICE_SIDES,
    CheckResult,
    DIFFICULTIES,
    DIFFICULTY_LADDER,
    HumanAttributes,
    OpposedResult,
    SITUATIONAL_MODIFIER_MAX,
    SITUATIONAL_MODIFIER_MIN,
    SKILL_LEVEL_MAX,
    SKILL_LEVEL_MIN,
    SkillAccess,
    TOP_DIFFICULTY,
    UNSKILLED_PENALTY,
    compare_opposed,
    difficulty_for,
    generate_human_attributes,
    human_modifier,
    resolve_check,
    roll_2d6,
    roll_3d6,
    roll_check_dice,
)

__all__ = [
    "AID_BONUS_CAP",
    "ATTRIBUTE_DEFINITIONS",
    "ATTRIBUTE_IDS",
    "AttributeSet",
    "CHECK_DICE",
    "CHECK_DICE_COUNT",
    "CHECK_DICE_SIDES",
    "CheckResult",
    "DIFFICULTIES",
    "DIFFICULTY_LADDER",
    "HumanAttributes",
    "OpposedResult",
    "SITUATIONAL_MODIFIER_MAX",
    "SITUATIONAL_MODIFIER_MIN",
    "SKILL_LEVEL_MAX",
    "SKILL_LEVEL_MIN",
    "SkillAccess",
    "TOP_DIFFICULTY",
    "UNSKILLED_PENALTY",
    "compare_opposed",
    "difficulty_for",
    "generate_human_attributes",
    "human_modifier",
    "resolve_check",
    "roll_2d6",
    "roll_3d6",
    "roll_check_dice",
]
