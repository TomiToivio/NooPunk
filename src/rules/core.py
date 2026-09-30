"""Canonical NoöPunk attribute and 3d6 resolution mechanics.

The numeric canon is stored in data/rules/core.json so runtimes can consume the
same authored values without maintaining separate tables.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
import random
from typing import Iterable, Mapping, Protocol


class DiceSource(Protocol):
    def randint(self, a: int, b: int) -> int: ...


_CANON_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "core.json"
_CANON = json.loads(_CANON_PATH.read_text(encoding="utf-8"))

ATTRIBUTE_DEFINITIONS = tuple(_CANON["attributes"])
ATTRIBUTE_IDS = tuple(item["id"] for item in ATTRIBUTE_DEFINITIONS)
DIFFICULTIES = dict(_CANON["difficulties"])
UNSKILLED_PENALTY = int(_CANON["unskilled_penalty"])
_HUMAN_MODIFIERS = {int(k): int(v) for k, v in _CANON["human_3d6_modifier"].items()}


class SkillAccess(str, Enum):
    """Whether an action can be attempted without its future skill."""

    UNSKILLED_ALLOWED = "unskilled_allowed"
    TRAINED_ONLY = "trained_only"


@dataclass(frozen=True, slots=True)
class AttributeSet:
    """The six canonical attribute modifiers.

    Values are intentionally not clamped to -3..+3. Ordinary humans are
    generated in that range, while future entities may use explicit values
    outside it when author-defined rules permit.
    """

    values: Mapping[str, int]

    def __post_init__(self) -> None:
        values = dict(self.values)
        if set(values) != set(ATTRIBUTE_IDS):
            raise ValueError(f"Attributes must be exactly: {', '.join(ATTRIBUTE_IDS)}")
        if not all(isinstance(value, int) for value in values.values()):
            raise TypeError("Attribute modifiers must be integers.")
        object.__setattr__(self, "values", values)

    def __getitem__(self, attribute_id: str) -> int:
        return self.values[attribute_id]

    def as_dict(self) -> dict[str, int]:
        return dict(self.values)


@dataclass(frozen=True, slots=True)
class HumanAttributes:
    raw_rolls: Mapping[str, int]
    modifiers: AttributeSet

    def __post_init__(self) -> None:
        raw = dict(self.raw_rolls)
        if set(raw) != set(ATTRIBUTE_IDS):
            raise ValueError(f"Raw rolls must be exactly: {', '.join(ATTRIBUTE_IDS)}")
        if any(roll < 3 or roll > 18 for roll in raw.values()):
            raise ValueError("Human 3d6 attribute rolls must be in 3..18.")
        object.__setattr__(self, "raw_rolls", raw)


@dataclass(frozen=True, slots=True)
class CheckResult:
    attempted: bool
    dice_total: int | None
    attribute_modifier: int
    extra_modifiers: tuple[int, ...]
    unskilled_modifier: int
    total: int | None
    target: int
    success: bool | None
    blocked_reason: str | None = None


@dataclass(frozen=True, slots=True)
class OpposedResult:
    left_total: int
    right_total: int
    winner: str | None
    unresolved_tie: bool


def human_modifier(raw_3d6: int) -> int:
    try:
        return _HUMAN_MODIFIERS[raw_3d6]
    except KeyError as exc:
        raise ValueError("Human attribute generation requires a 3d6 total in 3..18.") from exc


def roll_3d6(rng: DiceSource | None = None) -> int:
    source = rng if rng is not None else random
    return sum(source.randint(1, 6) for _ in range(3))


def generate_human_attributes(rng: DiceSource | None = None) -> HumanAttributes:
    raw = {attribute_id: roll_3d6(rng) for attribute_id in ATTRIBUTE_IDS}
    return HumanAttributes(
        raw_rolls=raw,
        modifiers=AttributeSet(
            {attribute_id: human_modifier(roll) for attribute_id, roll in raw.items()}
        ),
    )


def resolve_check(
    *,
    attribute_modifier: int,
    target: int,
    extra_modifiers: Iterable[int] = (),
    skill_access: SkillAccess = SkillAccess.UNSKILLED_ALLOWED,
    has_skill: bool = True,
    rng: DiceSource | None = None,
    dice_total: int | None = None,
) -> CheckResult:
    """Resolve 3d6 + attribute + modifiers against a target.

    dice_total is injectable for deterministic tests and external deterministic
    orchestration. When omitted, code rolls 3d6. The LLM never supplies dice.
    """
    extras = tuple(int(value) for value in extra_modifiers)

    if not has_skill and skill_access is SkillAccess.TRAINED_ONLY:
        return CheckResult(
            attempted=False,
            dice_total=None,
            attribute_modifier=attribute_modifier,
            extra_modifiers=extras,
            unskilled_modifier=0,
            total=None,
            target=target,
            success=None,
            blocked_reason="trained_only_without_skill",
        )

    unskilled = UNSKILLED_PENALTY if not has_skill else 0
    rolled = roll_3d6(rng) if dice_total is None else int(dice_total)
    if rolled < 3 or rolled > 18:
        raise ValueError("A 3d6 check roll must be in 3..18.")

    total = rolled + int(attribute_modifier) + sum(extras) + unskilled
    return CheckResult(
        attempted=True,
        dice_total=rolled,
        attribute_modifier=int(attribute_modifier),
        extra_modifiers=extras,
        unskilled_modifier=unskilled,
        total=total,
        target=int(target),
        success=total >= target,
    )


def compare_opposed(left_total: int, right_total: int) -> OpposedResult:
    if left_total > right_total:
        return OpposedResult(left_total, right_total, "left", False)
    if right_total > left_total:
        return OpposedResult(left_total, right_total, "right", False)
    return OpposedResult(left_total, right_total, None, True)
