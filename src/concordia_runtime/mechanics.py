"""Deterministic NoöPunk mechanics exposed to Concordia.

Concordia executes the shared NoöPunk rules; it does not define them. The current
canonical check is STAT + Skill + 1d10 vs Difficulty Value.
"""

from __future__ import annotations

from dataclasses import asdict

from rules import AttributeSet, CheckResult, OpposedResult, compare_opposed, resolve_check


def resolve_structured_check(
    *,
    attributes: AttributeSet,
    attribute_id: str,
    target: int,
    skill_level: int,
    dice_total: int | None = None,
    **_compat: object,
) -> dict[str, object]:
    """Resolve a structured NoöPunk check through the shared kernel.

    attribute_id and skill_level remain as adapter names while callers are
    migrated; semantically they are a STAT name and a 1..10 Skill rating.
    """
    result: CheckResult = resolve_check(
        stat=attributes[attribute_id],
        skill=skill_level,
        target=target,
        die=dice_total,
    )
    return asdict(result)


def resolve_structured_opposed(
    left_total: int,
    right_total: int,
    **_compat: object,
) -> dict[str, object]:
    """Higher total wins; ties remain unresolved pending an explicit rule."""
    result: OpposedResult = compare_opposed(left_total, right_total)
    return asdict(result)
