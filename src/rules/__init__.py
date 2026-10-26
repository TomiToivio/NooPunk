"""Shared NoöPunk rules.

The **base system** is the *Without Number* shape (author direction 2026-10-26): six attributes 3..18,
skills level 0..4, `2d6 + attribute modifier + skill level >= difficulty`, 1d20 saves. It lives in
:mod:`rules.wn`, driven by `data/rules/wn_core.json`.

:mod:`rules.core` (`STAT + Skill + 1d10`) is the **transitional** legacy layer: it still runs the
legacy game while the layers that consume it are migrated. New play should use :mod:`rules.wn`.
"""

from . import wn

# Retired compatibility surface (see the module docstring). Kept only so callers
# mid-migration keep importing; it is not canonical mechanics.
from ._retired import (
    AID_BONUS_CAP,
    ATTRIBUTE_DEFINITIONS,
    ATTRIBUTE_IDS,
    SITUATIONAL_MODIFIER_MAX,
    SITUATIONAL_MODIFIER_MIN,
    UNSKILLED_PENALTY,
    HumanAttributes,
    SkillAccess,
    generate_human_attributes,
    human_modifier,
)
from .core import (
    CHECK_DICE,
    CHECK_DICE_COUNT,
    CHECK_DICE_SIDES,
    DIFFICULTIES,
    DIFFICULTY_LADDER,
    SKILL_LEVEL_MAX,
    SKILL_LEVEL_MIN,
    STAT_LAYER,
    STAT_LIST,
    STAT_MAX,
    STAT_MIN,
    STAT_NAMES,
    TOP_DIFFICULTY,
    AttributeSet,
    CheckResult,
    OpposedResult,
    compare_opposed,
    difficulty_for,
    resolve_check,
    roll_check_dice,
    roll_d10,
)

# The unified tag prototype (issue #51). `tags` does not import this package at
# module scope, so there is no circular import and the canonical core stays
# independent of the prototype. Issue #111 replaced the *check* the core performs;
# it did not retire the tag layer, whose re-exports were dropped here by accident,
# breaking test modules at import time and silently removing tests from the suite.
from .tags import (
    ATTRIBUTE_CATEGORY,
    FOUR_SYSTEMS,
    HUMAN_ATTRIBUTE_MAX,
    HUMAN_ATTRIBUTE_MIN,
    PROTOTYPE_ATTRIBUTE_SYSTEMS,
    PROTOTYPE_ATTRIBUTE_TAGS,
    PROTOTYPE_MAX_CONTRIBUTING_TAGS,
    RESOLVED,
    TAG_RATING_MAX,
    TAG_RATING_MIN,
    UNRESOLVED_ABSENT_SYSTEM,
    AbsentSystemResult,
    SystemPresence,
    Tag,
    TagCheckInput,
    TagError,
    TagStack,
    TranshumanTag,
    build_stack,
    compose_check,
    resolve_tag_check,
    stat_rating,
    transhuman_attribute,
)

__all__ = [
    "AID_BONUS_CAP",
    "ATTRIBUTE_CATEGORY",
    "ATTRIBUTE_DEFINITIONS",
    "ATTRIBUTE_IDS",
    "CHECK_DICE",
    "CHECK_DICE_COUNT",
    "CHECK_DICE_SIDES",
    "DIFFICULTIES",
    "DIFFICULTY_LADDER",
    "FOUR_SYSTEMS",
    "HUMAN_ATTRIBUTE_MAX",
    "HUMAN_ATTRIBUTE_MIN",
    "PROTOTYPE_ATTRIBUTE_SYSTEMS",
    "PROTOTYPE_ATTRIBUTE_TAGS",
    "PROTOTYPE_MAX_CONTRIBUTING_TAGS",
    "RESOLVED",
    "SITUATIONAL_MODIFIER_MAX",
    "SITUATIONAL_MODIFIER_MIN",
    "SKILL_LEVEL_MAX",
    "SKILL_LEVEL_MIN",
    "STAT_LAYER",
    "STAT_LIST",
    "STAT_MAX",
    "STAT_MIN",
    "STAT_NAMES",
    "TAG_RATING_MAX",
    "TAG_RATING_MIN",
    "TOP_DIFFICULTY",
    "UNRESOLVED_ABSENT_SYSTEM",
    "UNSKILLED_PENALTY",
    "AbsentSystemResult",
    "AttributeSet",
    "CheckResult",
    "HumanAttributes",
    "OpposedResult",
    "SkillAccess",
    "SystemPresence",
    "Tag",
    "TagCheckInput",
    "TagError",
    "TagStack",
    "TranshumanTag",
    "build_stack",
    "compare_opposed",
    "compose_check",
    "difficulty_for",
    "generate_human_attributes",
    "human_modifier",
    "resolve_check",
    "resolve_tag_check",
    "roll_check_dice",
    "roll_d10",
    "stat_rating",
    "transhuman_attribute",
]
