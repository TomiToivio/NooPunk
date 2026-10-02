"""Deterministic NoöPunk mechanics exposed to Concordia orchestration.

Concordia executes NoöPunk rules; it does not replace them. Numeric resolution
happens in code, through the shared rules layer, so a runtime cannot redefine a
canonical rule (AGENTS.md §13: a rules difference between runtimes is a defect).

Engine: 2d6 + skill level + attribute modifier against 6/8/10/12/14+ (RULEBOOK §4).
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from rules import (
    AttributeSet,
    CheckResult,
    OpposedResult,
    SkillAccess,
    compare_opposed,
    resolve_check,
)


def resolve_structured_check(
    *,
    attributes: AttributeSet,
    attribute_id: str,
    target: int,
    skill_level: int = 0,
    has_skill: bool = True,
    extra_modifiers: Iterable[int] = (),
    skill_access: SkillAccess = SkillAccess.UNSKILLED_ALLOWED,
    dice_total: int | None = None,
    aid_bonus: int = 0,
) -> dict[str, object]:
    """Return deterministic structured mechanics for GM/agent context.

    Numeric resolution is performed in code. LLMs may describe or reason about this
    result but must not replace these values with invented outcomes; `dice_total` is
    for deterministic callers (replay, tests), never for model output.
    """
    result: CheckResult = resolve_check(
        attribute_modifier=attributes[attribute_id],
        target=target,
        skill_level=skill_level,
        has_skill=has_skill,
        extra_modifiers=extra_modifiers,
        skill_access=skill_access,
        dice_total=dice_total,
        aid_bonus=aid_bonus,
    )
    return asdict(result)


def resolve_structured_opposed(
    left_total: int,
    right_total: int,
    *,
    left_is_player_character: bool = False,
    right_is_player_character: bool = False,
) -> dict[str, object]:
    """Compare two opposed totals under RULEBOOK §4.1."""
    result: OpposedResult = compare_opposed(
        left_total,
        right_total,
        left_is_player_character=left_is_player_character,
        right_is_player_character=right_is_player_character,
    )
    return asdict(result)
