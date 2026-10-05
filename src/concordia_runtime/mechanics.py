"""Deterministic NoöPunk mechanics exposed to Concordia orchestration.

Canonical engine: STAT + Skill + 1d10 vs DV (issue #111).
"""
from __future__ import annotations

from dataclasses import asdict
from rules import AttributeSet, CheckResult, OpposedResult, compare_opposed, resolve_check


def resolve_structured_check(
    *,
    attributes: AttributeSet,
    attribute_id: str,
    skill: int,
    target: int,
    die: int | None = None,
) -> dict[str, object]:
    """Resolve one canonical check in code, never in model prose."""
    result: CheckResult = resolve_check(
        stat=attributes[attribute_id],
        skill=skill,
        target=target,
        die=die,
    )
    return asdict(result)


def resolve_structured_opposed(left_total: int, right_total: int) -> dict[str, object]:
    """Higher total wins; ties remain unresolved pending playtest."""
    result: OpposedResult = compare_opposed(left_total, right_total)
    return asdict(result)
