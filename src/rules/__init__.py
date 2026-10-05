"""Shared NoöPunk rules.

NoöPunk is an independent system. Core resolution is STAT + Skill + 1d10 vs DV.
"""

from .core import (
    AttributeSet,
    CHECK_DICE,
    CHECK_DICE_COUNT,
    CHECK_DICE_SIDES,
    CheckResult,
    DIFFICULTIES,
    DIFFICULTY_LADDER,
    OpposedResult,
    SKILL_LEVEL_MAX,
    SKILL_LEVEL_MIN,
    STAT_MAX,
    STAT_MIN,
    TOP_DIFFICULTY,
    compare_opposed,
    difficulty_for,
    resolve_check,
    roll_check_dice,
    roll_d10,
)

__all__ = [
    "AttributeSet",
    "CHECK_DICE",
    "CHECK_DICE_COUNT",
    "CHECK_DICE_SIDES",
    "CheckResult",
    "DIFFICULTIES",
    "DIFFICULTY_LADDER",
    "OpposedResult",
    "SKILL_LEVEL_MAX",
    "SKILL_LEVEL_MIN",
    "STAT_MAX",
    "STAT_MIN",
    "TOP_DIFFICULTY",
    "compare_opposed",
    "difficulty_for",
    "resolve_check",
    "roll_check_dice",
    "roll_d10",
]
