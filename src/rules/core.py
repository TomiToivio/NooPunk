"""Canonical engine-independent NoöPunk core rules.

Issue #111 makes NoöPunk an independent system. The canonical check is:

    STAT + Skill + 1d10 >= Difficulty Value

Both STAT and trained Skill ratings are 1..10. Issue #131 (2026-10-05) locks the
six universal base STATs — FIT / REF / INT / SOC / CYB / PSY — recorded in
``data/rules/core.json``. Cybernetic hardware statistics (COMPUTE / INTERFACE /
NETWORK and similar) are properties of decks, implants, devices and agents, not
character STATs. Issue #159 locks the 40-item universal Skill vocabulary recorded
in ``data/rules/skills.json`` and ``data/rules/core.json``. Ties, criticals, and
the situational-modifier procedure remain deliberately unresolved rather than inherited
from another game.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import random
from typing import Mapping, Protocol


class DiceSource(Protocol):
    def randint(self, a: int, b: int) -> int: ...


_CANON_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "core.json"
_CANON = json.loads(_CANON_PATH.read_text(encoding="utf-8"))

CHECK_DICE = _CANON["skill_check"]["dice"]
CHECK_DICE_COUNT = int(_CANON["skill_check"]["dice_count"])
CHECK_DICE_SIDES = int(_CANON["skill_check"]["dice_sides"])
STAT_MIN = int(_CANON["stats"]["min"])
STAT_MAX = int(_CANON["stats"]["max"])
SKILL_LEVEL_MIN = int(_CANON["skills"]["min"])
SKILL_LEVEL_MAX = int(_CANON["skills"]["max"])
DIFFICULTIES = {int(k): str(v) for k, v in _CANON["difficulties"].items()}
DIFFICULTY_LADDER = tuple(sorted(DIFFICULTIES))
TOP_DIFFICULTY = max(DIFFICULTY_LADDER)

#: The six universal base STATs, locked by issue #131. Order is canonical.
STAT_LIST: tuple[str, ...] = tuple(_CANON["stats"]["final_list"])
#: Canonical display names, keyed by STAT code.
STAT_NAMES: dict[str, str] = dict(_CANON["stats"]["names"])
#: The four-layer ontology each base STAT belongs to.
STAT_LAYER: dict[str, str] = dict(_CANON["stats"]["layer"])


@dataclass(frozen=True, slots=True)
class AttributeSet:
    """A set of named 1..10 STAT ratings.

    The class name is retained as a compatibility surface for runtimes, while the
    canonical rules terminology is STAT. Issue #111 intentionally does not lock a
    final list of STAT names.
    """

    values: Mapping[str, int]

    def __post_init__(self) -> None:
        values = dict(self.values)
        if not values:
            raise ValueError("At least one STAT is required.")
        if any(not isinstance(name, str) or not name.strip() for name in values):
            raise ValueError("STAT names must be non-empty strings.")
        for value in values.values():
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError("STAT ratings must be integers.")
            if not STAT_MIN <= value <= STAT_MAX:
                raise ValueError(f"STAT ratings must be {STAT_MIN}..{STAT_MAX}.")
        object.__setattr__(self, "values", values)

    def __getitem__(self, stat_id: str) -> int:
        return self.values[stat_id]

    def as_dict(self) -> dict[str, int]:
        return dict(self.values)


@dataclass(frozen=True, slots=True)
class CheckResult:
    stat: int
    skill: int
    die: int
    target: int
    total: int
    success: bool


@dataclass(frozen=True, slots=True)
class OpposedResult:
    left_total: int
    right_total: int
    winner: str | None
    unresolved_tie: bool


def roll_d10(rng: DiceSource | None = None) -> int:
    source = rng if rng is not None else random
    return source.randint(1, CHECK_DICE_SIDES)


def roll_check_dice(rng: DiceSource | None = None) -> int:
    return roll_d10(rng)


def _validate_rating(label: str, value: int, minimum: int, maximum: int) -> int:
    value = int(value)
    if not minimum <= value <= maximum:
        raise ValueError(f"{label} must be {minimum}..{maximum}.")
    return value


def resolve_check(
    *,
    stat: int | None = None,
    skill: int | None = None,
    target: int,
    rng: DiceSource | None = None,
    die: int | None = None,
    # Compatibility names for callers during the migration. They are interpreted
    # as the new ratings, not as old modifier scales.
    attribute_modifier: int | None = None,
    skill_level: int | None = None,
    dice_total: int | None = None,
    **_legacy_ignored: object,
) -> CheckResult:
    """Resolve STAT + Skill + 1d10 vs DV.

    The compatibility parameter names exist only to ease runtime migration.
    They do not preserve the retired 2d6 or EP2 mechanics.
    """
    if stat is None:
        stat = attribute_modifier
    if skill is None:
        skill = skill_level
    if die is None:
        die = dice_total
    if stat is None or skill is None:
        raise ValueError("A canonical check requires both STAT and Skill ratings.")

    stat_value = _validate_rating("STAT", stat, STAT_MIN, STAT_MAX)
    skill_value = _validate_rating("Skill", skill, SKILL_LEVEL_MIN, SKILL_LEVEL_MAX)
    rolled = roll_d10(rng) if die is None else int(die)
    if not 1 <= rolled <= CHECK_DICE_SIDES:
        raise ValueError("A 1d10 check roll must be in 1..10.")

    total = stat_value + skill_value + rolled
    return CheckResult(
        stat=stat_value,
        skill=skill_value,
        die=rolled,
        target=int(target),
        total=total,
        success=total >= int(target),
    )


def compare_opposed(left_total: int, right_total: int, **_ignored: object) -> OpposedResult:
    """Higher total wins. A tie remains unresolved by design."""
    if left_total > right_total:
        return OpposedResult(left_total, right_total, "left", False)
    if right_total > left_total:
        return OpposedResult(left_total, right_total, "right", False)
    return OpposedResult(left_total, right_total, None, True)


def difficulty_for(target: int) -> str:
    target = int(target)
    return DIFFICULTIES.get(target, "Unlisted difficulty; use an authored DV deliberately.")


__all__ = [
    "AttributeSet",
    "CHECK_DICE",
    "CHECK_DICE_COUNT",
    "CHECK_DICE_SIDES",
    "CheckResult",
    "DIFFICULTIES",
    "DIFFICULTY_LADDER",
    "OpposedResult",
    "SKILL_LEVEL_MAX",
    "SKILL_LEVEL_MIN",
    "STAT_LAYER",
    "STAT_LIST",
    "STAT_MAX",
    "STAT_MIN",
    "STAT_NAMES",
    "TOP_DIFFICULTY",
    "compare_opposed",
    "difficulty_for",
    "resolve_check",
    "roll_check_dice",
    "roll_d10",
]
