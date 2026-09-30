"""Deterministic NoöPunk mechanics exposed to Concordia orchestration."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from rules import (
    AttributeSet,
    CheckResult,
    OpposedResult,
    SkillAccess,
    compare_opposed,
    difficulty_meaning,
    difficulty_target,
    resolve_check,
)


def resolve_named_check(
    *,
    attributes: AttributeSet,
    attribute_id: str,
    difficulty: str,
    extra_modifiers: Iterable[int] = (),
    skill_access: SkillAccess = SkillAccess.UNSKILLED_ALLOWED,
    has_skill: bool = True,
    dice_total: int | None = None,
) -> dict[str, object]:
    """Resolve a check from a difficulty NAME, in code (issue #11).

    A GM or LLM agent chooses *which* difficulty applies; this function decides
    what that difficulty is. Selection is allowed to be conversational, the
    target is not: neither the agent nor the model may supply the number, because
    "Hard" moved from 12 to 15 and a hallucinated target would be a silent
    rules fork.

    The returned payload carries the resolved difficulty name, its canonical
    target and its canonical meaning alongside the arithmetic, so a description
    of the outcome can be checked against what the engine actually did.
    """
    target = difficulty_target(difficulty)
    result = resolve_structured_check(
        attributes=attributes,
        attribute_id=attribute_id,
        target=target,
        extra_modifiers=extra_modifiers,
        skill_access=skill_access,
        has_skill=has_skill,
        dice_total=dice_total,
    )
    return {
        **result,
        "difficulty": difficulty,
        "difficulty_meaning": difficulty_meaning(difficulty),
    }


def resolve_structured_check(
    *,
    attributes: AttributeSet,
    attribute_id: str,
    target: int,
    extra_modifiers: Iterable[int] = (),
    skill_access: SkillAccess = SkillAccess.UNSKILLED_ALLOWED,
    has_skill: bool = True,
    dice_total: int | None = None,
) -> dict[str, object]:
    """Return deterministic structured mechanics for GM/agent context.

    Numeric resolution is performed in code. LLMs may describe or reason about
    this result, but must not replace these values with invented outcomes.
    """
    result: CheckResult = resolve_check(
        attribute_modifier=attributes[attribute_id],
        target=target,
        extra_modifiers=extra_modifiers,
        skill_access=skill_access,
        has_skill=has_skill,
        dice_total=dice_total,
    )
    return asdict(result)


def resolve_structured_opposed(left_total: int, right_total: int) -> dict[str, object]:
    result: OpposedResult = compare_opposed(left_total, right_total)
    return asdict(result)
