"""Canonical, engine-independent NoöPunk RPG rules."""

from .core import (
    ATTRIBUTE_DEFINITIONS,
    ATTRIBUTE_IDS,
    DIFFICULTIES,
    UNSKILLED_PENALTY,
    AttributeSet,
    CheckResult,
    HumanAttributes,
    OpposedResult,
    SkillAccess,
    compare_opposed,
    generate_human_attributes,
    human_modifier,
    roll_3d6,
    resolve_check,
)

__all__ = [
    "ATTRIBUTE_DEFINITIONS",
    "ATTRIBUTE_IDS",
    "DIFFICULTIES",
    "UNSKILLED_PENALTY",
    "AttributeSet",
    "CheckResult",
    "HumanAttributes",
    "OpposedResult",
    "SkillAccess",
    "compare_opposed",
    "generate_human_attributes",
    "human_modifier",
    "roll_3d6",
    "resolve_check",
]
