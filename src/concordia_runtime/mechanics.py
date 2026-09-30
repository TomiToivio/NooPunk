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
    resolve_check,
)


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
