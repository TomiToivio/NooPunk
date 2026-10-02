"""Canonical, engine-independent NoöPunk RPG rules.

The numeric canon lives in ``data/rules/core.json`` so every runtime consumes the
same authored values instead of keeping its own copy.

**Engine: 2d6 skill checks.** RULEBOOK.md §4 is the source of truth:
``total = 2d6 + relevant skill level + relevant attribute modifier``, success at
``total >= difficulty`` on the 6 / 8 / 10 / 12 / 14 ladder. The earlier 3d6
skill-check engine and its 3/6/9/12/15/18 ladder are **withdrawn**; RULEBOOK §17.1
recorded the digital runtimes as carrying that as port debt, and this module is the
port that retires it.

Two things the port deliberately does **not** change, because RULEBOOK §17.1 says
they were never part of the superseded engine:

* attribute **generation** stays 3d6 per attribute (§5.2) — that is the generation
  roll, not the skill-check engine;
* the six attribute ids, the -3..+3 ordinary-human modifier range, the unskilled
  penalty, and the trained-only representation are unchanged.

Nothing here invents a rule. Difficulty above 14 is expressed as an explicit
``difficulty_floor`` rather than as an extra ladder rung, because RULEBOOK §4 writes
the top rung as "14+" and adding a sixth named rung would be inventing canon.
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
_HUMAN_MODIFIERS = {
    int(k): int(v) for k, v in _CANON["human_3d6_generation"]["modifier_table"].items()
}

#: The skill-check dice. Read from the canon file so a runtime cannot drift from it.
CHECK_DICE_COUNT = int(_CANON["skill_check"]["dice_count"])
CHECK_DICE_SIDES = int(_CANON["skill_check"]["dice_sides"])
CHECK_DICE = _CANON["skill_check"]["dice"]

UNSKILLED_PENALTY = int(_CANON["unskilled_penalty"])
SKILL_LEVEL_MIN = int(_CANON["skill_levels"]["min"])
SKILL_LEVEL_MAX = int(_CANON["skill_levels"]["max"])

#: The five named difficulty rungs in ascending order. `14` is the top rung; the
#: rulebook writes it "14+", so a harder task uses a higher *target*, not a new rung.
DIFFICULTY_LADDER = tuple(sorted(int(key) for key in DIFFICULTIES))
TOP_DIFFICULTY = max(DIFFICULTY_LADDER)

#: Situational modifier band from RULEBOOK §4.
SITUATIONAL_MODIFIER_MIN = -2
SITUATIONAL_MODIFIER_MAX = 2

#: Aid bonus cap from RULEBOOK §4.3.
AID_BONUS_CAP = int(_CANON["aiding"]["cap"])


class SkillAccess(str, Enum):
    """Whether an action can be attempted without the relevant skill."""

    UNSKILLED_ALLOWED = "unskilled_allowed"
    TRAINED_ONLY = "trained_only"


@dataclass(frozen=True, slots=True)
class AttributeSet:
    """The six canonical attribute modifiers.

    Values are intentionally not clamped to -3..+3. Ordinary humans are generated
    in that range, while transhuman, AI, NHI or injured entities may use explicit
    values outside it when author-defined rules permit.
    """

    values: Mapping[str, int]

    def __post_init__(self) -> None:
        values = dict(self.values)
        if set(values) != set(ATTRIBUTE_IDS):
            raise ValueError(f"Attributes must be exactly: {', '.join(ATTRIBUTE_IDS)}")
        if not all(isinstance(value, int) and not isinstance(value, bool)
                   for value in values.values()):
            raise TypeError("Attribute modifiers must be integers.")
        object.__setattr__(self, "values", values)

    def __getitem__(self, attribute_id: str) -> int:
        return self.values[attribute_id]

    def as_dict(self) -> dict[str, int]:
        return dict(self.values)


@dataclass(frozen=True, slots=True)
class HumanAttributes:
    """A generated ordinary-human attribute set: raw 3d6 rolls plus modifiers."""

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
    """Outcome of one skill check.

    ``attempted=False`` means the check was **blocked** (trained-only without the
    skill) and no dice were rolled — RULEBOOK §4.2 calls this a blocked attempt,
    not a failed roll. ``success`` stays ``None`` in that case so a caller cannot
    mistake "blocked" for "failed".
    """

    attempted: bool
    dice_total: int | None
    attribute_modifier: int
    skill_level: int
    extra_modifiers: tuple[int, ...]
    unskilled_modifier: int
    total: int | None
    target: int
    success: bool | None
    blocked_reason: str | None = None

    @property
    def difficulty(self) -> int:
        """Alias for ``target``; the rulebook's word for it is 'difficulty'."""
        return self.target


@dataclass(frozen=True, slots=True)
class OpposedResult:
    """Outcome of an opposed skill check.

    ``unresolved_tie`` is True only when no player character was involved on either
    side. RULEBOOK §4.1 defines the player-character tie rule and deliberately does
    **not** define a general tie procedure, so a no-PC tie stays unresolved rather
    than being decided here.
    """

    left_total: int
    right_total: int
    winner: str | None
    unresolved_tie: bool
    decided_by: str = ""


def human_modifier(raw_3d6: int) -> int:
    """Map a 3d6 attribute *generation* roll to its modifier (RULEBOOK §5.2)."""
    try:
        return _HUMAN_MODIFIERS[raw_3d6]
    except KeyError as exc:
        raise ValueError("Human attribute generation requires a 3d6 total in 3..18.") from exc


def roll_3d6(rng: DiceSource | None = None) -> int:
    """Roll 3d6. Used for attribute **generation**, not for skill checks."""
    source = rng if rng is not None else random
    return sum(source.randint(1, 6) for _ in range(3))


def roll_2d6(rng: DiceSource | None = None) -> int:
    """Roll the skill-check dice (2d6). The LLM never supplies this."""
    source = rng if rng is not None else random
    return sum(source.randint(1, CHECK_DICE_SIDES) for _ in range(CHECK_DICE_COUNT))


#: Historical alias. `roll_check_dice` is the name new code should use; the
#: generation roll has its own name (`roll_3d6`) and they must not be confused.
def roll_check_dice(rng: DiceSource | None = None) -> int:
    return roll_2d6(rng)


def generate_human_attributes(rng: DiceSource | None = None) -> HumanAttributes:
    """Generate ordinary-human attributes (§5.2): 3d6 per attribute, then the table."""
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
    skill_level: int = 0,
    has_skill: bool = True,
    extra_modifiers: Iterable[int] = (),
    skill_access: SkillAccess = SkillAccess.UNSKILLED_ALLOWED,
    rng: DiceSource | None = None,
    dice_total: int | None = None,
    aid_bonus: int = 0,
) -> CheckResult:
    """Resolve one skill check: 2d6 + skill level + attribute modifier vs difficulty.

    ``dice_total`` is injectable for deterministic tests and for orchestration that
    has already rolled. When omitted, code rolls 2d6. **The LLM never supplies
    dice**, and it may not supply ``dice_total`` either — that parameter exists for
    deterministic callers, not for model output.

    ``skill_level`` is the trained level 0..4. A character who does not possess the
    skill passes ``has_skill=False``; unskilled is not level 0 (§5.3), which is why
    the two are separate parameters rather than one overloaded integer.
    """
    extras = tuple(int(value) for value in extra_modifiers)

    if not has_skill and skill_access is SkillAccess.TRAINED_ONLY:
        return CheckResult(
            attempted=False,
            dice_total=None,
            attribute_modifier=int(attribute_modifier),
            skill_level=0,
            extra_modifiers=extras,
            unskilled_modifier=0,
            total=None,
            target=int(target),
            success=None,
            blocked_reason="trained_only_without_skill",
        )

    level = 0
    if has_skill:
        level = int(skill_level)
        if not SKILL_LEVEL_MIN <= level <= SKILL_LEVEL_MAX:
            raise ValueError(
                f"Skill level must be {SKILL_LEVEL_MIN}..{SKILL_LEVEL_MAX}; "
                "unskilled is expressed with has_skill=False, not as level 0."
            )

    unskilled = UNSKILLED_PENALTY if not has_skill else 0
    rolled = roll_2d6(rng) if dice_total is None else int(dice_total)
    if not 2 * 1 <= rolled <= 2 * CHECK_DICE_SIDES:
        raise ValueError(
            f"A {CHECK_DICE} check roll must be in {2}..{2 * CHECK_DICE_SIDES}."
        )

    aid = min(int(aid_bonus), AID_BONUS_CAP)
    total = rolled + level + int(attribute_modifier) + sum(extras) + unskilled + aid
    return CheckResult(
        attempted=True,
        dice_total=rolled,
        attribute_modifier=int(attribute_modifier),
        skill_level=level,
        extra_modifiers=extras,
        unskilled_modifier=unskilled,
        total=total,
        target=int(target),
        success=total >= target,
    )


def compare_opposed(
    left_total: int,
    right_total: int,
    *,
    left_is_player_character: bool = False,
    right_is_player_character: bool = False,
) -> OpposedResult:
    """Compare two opposed totals under RULEBOOK §4.1.

    The higher total wins. On a tie, if a player character is involved on either
    side the player character wins. A tie with no player character involved is left
    **unresolved**: §4.1 defines the PC tie and explicitly declines to define a
    general one, so deciding it here would be inventing canon.
    """
    if left_total > right_total:
        return OpposedResult(left_total, right_total, "left", False, "higher_total")
    if right_total > left_total:
        return OpposedResult(left_total, right_total, "right", False, "higher_total")
    if left_is_player_character and not right_is_player_character:
        return OpposedResult(left_total, right_total, "left", False, "player_character_tie")
    if right_is_player_character and not left_is_player_character:
        return OpposedResult(left_total, right_total, "right", False, "player_character_tie")
    return OpposedResult(left_total, right_total, None, True, "unresolved_tie")


def difficulty_for(target: int) -> str:
    """Return the ladder meaning for a target, or a floor note above the ladder.

    Above the top rung the rulebook writes "14+", so this reports the top rung's
    meaning with an explicit floor marker instead of inventing a sixth rung.
    """
    ladder = DIFFICULTIES.get(str(int(target)))
    if ladder:
        return ladder
    if int(target) > TOP_DIFFICULTY:
        return f"{DIFFICULTIES[str(TOP_DIFFICULTY)]} (above the {TOP_DIFFICULTY} rung)"
    return "easier than the lowest named rung; generally not worth a roll"


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
