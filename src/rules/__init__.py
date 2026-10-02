"""Engine-independent NoöPunk RPG rules.

RULEBOOK.md is the source of truth. The existing core module still carries the
legacy six-attribute digital specification as explicit porting debt; issue #51 adds
the new generic four-system typed-tag model in rules.tags without inventing the
final attribute list.
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


# Issue #51 typed-tag API. Imported after the legacy core exports so callers can
# migrate incrementally without pretending the old AttributeSet is final canon.
from .tags import (
    EntityState,
    SystemDomain,
    SystemState,
    Tag,
    TagCategory,
    TagStack,
    absent_system,
    present_system,
    stack_relevant_tags,
)

__all__ += [
    "EntityState",
    "SystemDomain",
    "SystemState",
    "Tag",
    "TagCategory",
    "TagStack",
    "absent_system",
    "present_system",
    "stack_relevant_tags",
]
