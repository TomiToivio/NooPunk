"""NoöPunk core on the Without Number chassis (#615).

Author direction (2026-10-26): *"For beginning, use CWN/SWN/AWN/WWN system for everything. Make the stats,
skills, all rules based on them. We will modify later."*

This module implements the contract in `data/rules/wn_core.json` and nothing else. It is deliberately
**additive**: `src/rules/core.py` remains the legacy `STAT + Skill + 1d10 ≥ DV` kernel until its migration
lands, because a chassis swap that breaks every scenario in one commit is the destructive rewrite the
conversion epic forbids. Two kernels coexist during the migration and exactly one of them is named
canonical here.

Design rules, so a result from this module can be trusted:

* **Every roll takes an injected RNG.** No module-level `random`. A seeded `random.Random` and an explicit
  dice value both work, so a replay is reproducible and a test is exact.
* **Dice are validated, never clamped.** A `d6` of 7 is an error, not a 6 — silent clamping is how a
  distribution test passes while the distribution is wrong.
* **The arithmetic is the contract.** Nothing here decides difficulty, adds situational modifiers or
  invents a stat; callers pass those in.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Final, Protocol

#: Attribute score -> modifier, per the Without Number band.
_MODIFIER_BY_SCORE: Final[dict[int, int]] = {
    3: -2,
    4: -1, 5: -1, 6: -1, 7: -1,
    8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
    14: 1, 15: 1, 16: 1, 17: 1,
    18: 2,
}

STAT_MIN: Final = 3
STAT_MAX: Final = 18
UNSKILLED_CHECK_PENALTY: Final = -1
UNSKILLED_ATTACK_PENALTY: Final = -2
SAVE_BASE_TARGET: Final = 15
SAVE_CATEGORIES: Final = ("Physical", "Evasion", "Mental", "Luck")

#: Which attributes a save may draw its modifier from; the better one applies.
_SAVE_STATS: Final[dict[str, tuple[str, ...]]] = {
    "Physical": ("STR", "CON"),
    "Evasion": ("INT", "DEX"),
    "Mental": ("WIS", "CHA"),
    "Luck": (),
}


class Dice(Protocol):
    """Anything that can produce a die result, so tests can inject one."""

    def randint(self, a: int, b: int) -> int:  # pragma: no cover - protocol
        ...


def attribute_modifier(score: int) -> int:
    """The Without Number modifier for an attribute score of 3..18."""
    if not isinstance(score, int) or isinstance(score, bool):
        raise TypeError(f"attribute score must be an int, got {type(score).__name__}")
    if score < STAT_MIN or score > STAT_MAX:
        raise ValueError(
            f"attribute score {score} is outside {STAT_MIN}..{STAT_MAX}; "
            "scores are not clamped, because a silent clamp hides a generation bug"
        )
    return _MODIFIER_BY_SCORE[score]


def _roll(rng: Dice, sides: int, count: int = 1) -> list[int]:
    return [rng.randint(1, sides) for _ in range(count)]


@dataclass(frozen=True)
class CheckResult:
    """The outcome of one skill check, with the arithmetic that produced it."""

    dice: tuple[int, ...]
    modifier: int
    skill_level: int
    total: int
    difficulty: int
    untrained: bool

    @property
    def success(self) -> bool:
        return self.total >= self.difficulty


def skill_check(
    *,
    attribute_score: int,
    skill_level: int | None,
    difficulty: int,
    rng: Dice | None = None,
    dice: tuple[int, int] | None = None,
) -> CheckResult:
    """`2d6 + attribute modifier + skill level >= difficulty`.

    ``skill_level=None`` means untrained: the attempt is at **-1**, and untrained is not a numbered level.
    Blocking an untrained attempt where training is required is the caller's decision, not a -1 here.
    """
    if skill_level is not None and not 0 <= skill_level <= 4:
        raise ValueError(f"skill level must be 0..4 or None (untrained), got {skill_level}")
    if difficulty <= 0:
        raise ValueError(f"difficulty must be positive, got {difficulty}")

    if dice is not None:
        if len(dice) != 2:
            raise ValueError(f"a 2d6 check needs exactly two dice, got {len(dice)}")
        rolled = tuple(int(d) for d in dice)
        for face in rolled:
            if not 1 <= face <= 6:
                raise ValueError(f"a d6 shows 1..6, got {face}")
    else:
        rolled = tuple(_roll(rng or random.Random(), 6, 2))

    untrained = skill_level is None
    level = UNSKILLED_CHECK_PENALTY if untrained else int(skill_level)
    modifier = attribute_modifier(attribute_score)
    total = sum(rolled) + modifier + level
    return CheckResult(
        dice=rolled,
        modifier=modifier,
        skill_level=level,
        total=total,
        difficulty=difficulty,
        untrained=untrained,
    )


@dataclass(frozen=True)
class SaveResult:
    die: int
    target: int
    category: str

    @property
    def success(self) -> bool:
        return self.die >= self.target


def saving_throw(
    *,
    category: str,
    scores: dict[str, int],
    rng: Dice | None = None,
    die: int | None = None,
) -> SaveResult:
    """`d20 >= 15 - best relevant attribute modifier`; Luck is a flat 15."""
    if category not in SAVE_CATEGORIES:
        raise ValueError(f"save category must be one of {SAVE_CATEGORIES}, got {category!r}")

    relevant = _SAVE_STATS[category]
    target = SAVE_BASE_TARGET
    if relevant:
        missing = [stat for stat in relevant if stat not in scores]
        if missing:
            raise ValueError(f"a {category} save needs {relevant}; missing {missing}")
        target = SAVE_BASE_TARGET - max(attribute_modifier(scores[stat]) for stat in relevant)

    if die is None:
        rolled = _roll(rng or random.Random(), 20)[0]
    else:
        rolled = int(die)
        if not 1 <= rolled <= 20:
            raise ValueError(f"a d20 shows 1..20, got {rolled}")
    return SaveResult(die=rolled, target=target, category=category)


@dataclass(frozen=True)
class AttackResult:
    die: int
    total: int
    ac: int

    @property
    def hit(self) -> bool:
        return self.total >= self.ac


def attack_roll(
    *,
    attack_bonus: int,
    ac: int,
    rng: Dice | None = None,
    die: int | None = None,
) -> AttackResult:
    """`d20 + attack bonus vs AC`. The unskilled -2 belongs in ``attack_bonus``; it is not applied twice."""
    if die is None:
        rolled = _roll(rng or random.Random(), 20)[0]
    else:
        rolled = int(die)
        if not 1 <= rolled <= 20:
            raise ValueError(f"a d20 shows 1..20, got {rolled}")
    total = rolled + int(attack_bonus)
    return AttackResult(die=rolled, total=total, ac=int(ac))


def roll_attributes(rng: Dice | None = None) -> dict[str, int]:
    """Roll six attributes in order on 3d6.

    The contract also offers the array ``14/12/11/10/9/7`` and one free score of 14; those are assignment
    choices made by the table, so they live in the JSON contract rather than in a generator.
    """
    source = rng or random.Random()
    order = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
    return {stat: sum(_roll(source, 6, 3)) for stat in order}
