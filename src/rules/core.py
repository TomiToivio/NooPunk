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
#: Why each difficulty carries its name. Data, not prose, so the three runtimes
#: cannot describe the same target differently (issue #11).
DIFFICULTY_MEANINGS = dict(_CANON.get("difficulty_meanings", {}))
#: The author's reading of modifier values outside the ordinary-human range.
HUMAN_ATTRIBUTE_INTERPRETATION = dict(_CANON.get("human_attribute_interpretation", {}))
UNSKILLED_PENALTY = int(_CANON["unskilled_penalty"])
#: Sentinel for "the attempt could not be made", distinct from a failed roll.
BLOCKED_TRAINED_ONLY = str(_CANON.get("trained_only_without_skill", "blocked"))
_HUMAN_MODIFIERS = {int(k): int(v) for k, v in _CANON["human_3d6_modifier"].items()}


class UnknownDifficulty(KeyError):
    """A difficulty name that is not in the canonical table (issue #11).

    Raised instead of a bare KeyError or a silent default, because the label
    'Hard' changed meaning (12 -> 15) and silently falling back to a number
    would reinterpret old data without telling anyone.
    """


def difficulty_target(name: str) -> int:
    """The canonical target for a named difficulty.

    This is the single lookup the runtimes share. It exists so that no runtime
    re-declares the name-to-target mapping (the Godot adapter previously read the
    JSON inline, which allowed a rename to be applied in one runtime only).
    """
    try:
        return int(DIFFICULTIES[name])
    except KeyError as exc:
        raise UnknownDifficulty(
            f"unknown difficulty {name!r}; canonical difficulties are "
            f"{', '.join(DIFFICULTIES)}"
        ) from exc


def difficulty_meaning(name: str) -> str:
    """The canonical one-line meaning for a named difficulty."""
    difficulty_target(name)  # validates the name, raising UnknownDifficulty
    return DIFFICULTY_MEANINGS.get(name, "")


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
