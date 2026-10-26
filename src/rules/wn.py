"""The NoöPunk base system: the *Without Number* shape, as the author directed on 2026-10-26.

Author instruction, quoted in `data/rules/wn_core.json`: *"For beginning, use CWN/SWN/AWN/WWN system
for everything. Make the stats, skills, all rules based on them. We will modify later."*

So this module is the base rules layer, and `rules.core` (STAT + Skill + 1d10) becomes **transitional**:
it still runs the legacy game while the layers that consume it are migrated. Nothing here is a hybrid —
the arithmetic below is the family's own:

    skill check   2d6 + attribute modifier + skill level  >=  difficulty
    attributes    3..18, modifier -2..+2 by band
    skills        level 0..4, -1 when untrained
    saves         1d20 >= 16 - level - highest of two attribute modifiers

The values live in `data/rules/wn_core.json` (canon), so a house rule is a data edit rather than a code
edit. The implementation is original expression over the CWN SRD's CC0 facts; no SRD sentence is
reproduced here, and no SWN or AWN text is used at all (neither has an established SRD licence — see
`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`).
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, Sequence

_CANON_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "wn_core.json"
CANON: dict[str, Any] = json.loads(_CANON_PATH.read_text(encoding="utf-8"))

REVISION: str = CANON["_canon_revision"]

#: The six attributes, in the family's order. NoöPunk adds nothing here yet: a setting-specific
#: seventh attribute would be a *later* modification, not a base-system decision.
ATTRIBUTES: tuple[str, ...] = tuple(CANON["attributes"]["list"])
ATTRIBUTE_NAMES: dict[str, str] = dict(CANON["attributes"]["names"])

ATTRIBUTE_MIN: int = int(CANON["attributes"]["min"])
ATTRIBUTE_MAX: int = int(CANON["attributes"]["max"])
MODIFIER_FLOOR: int = int(CANON["attributes"]["modifier_floor"])
MODIFIER_CEILING: int = int(CANON["attributes"]["modifier_ceiling"])

SKILL_MIN: int = int(CANON["skills"]["min"])
SKILL_MAX: int = int(CANON["skills"]["max"])
UNSKILLED_PENALTY: int = int(CANON["skills"]["untrained_penalty"])

CHECK_DICE_COUNT: int = int(CANON["skill_check"]["dice_count"])
CHECK_DICE_SIDES: int = int(CANON["skill_check"]["dice_sides"])
CHECK_DICE: str = CANON["skill_check"]["dice"]

DIFFICULTIES: dict[int, str] = {int(k): str(v) for k, v in CANON["difficulties"].items()}
DIFFICULTY_LADDER: tuple[int, ...] = tuple(sorted(DIFFICULTIES))
TOP_DIFFICULTY: int = max(DIFFICULTY_LADDER)

SITUATIONAL_MIN: int = int(CANON["situational_modifier_band"]["min"])
SITUATIONAL_MAX: int = int(CANON["situational_modifier_band"]["max"])
AID_BONUS_MAX: int = int(CANON["aid_bonus"]["max"])

SAVE_DIE: int = int(CANON["saves"]["die"].removeprefix("1d"))
SAVE_TARGET_BASE: int = int(CANON["saves"]["target_base"])
SAVE_TYPES: tuple[str, ...] = tuple(CANON["saves"]["types"])

GENERATION_ARRAY: tuple[int, ...] = tuple(int(x) for x in CANON["attributes"]["generation"]["array"])


class WNError(ValueError):
    """A base-system input outside its canon range, or a save type that does not exist."""


class DiceSource(Protocol):
    def randint(self, a: int, b: int) -> int: ...


# --------------------------------------------------------------------------- #
# Attributes
# --------------------------------------------------------------------------- #


def attribute_modifier(score: int) -> int:
    """The modifier a 3..18 score carries, from the canon band table.

    The bands are contiguous and closed, which is why this is a lookup and not arithmetic: a house
    rule that moves one band edge must not silently move the others.
    """
    score = int(score)
    if not ATTRIBUTE_MIN <= score <= ATTRIBUTE_MAX:
        raise WNError(f"attribute score must be {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX}, got {score}")
    for band in CANON["attributes"]["modifier_bands"]:
        if int(band["low"]) <= score <= int(band["high"]):
            return int(band["modifier"])
    raise WNError(f"no modifier band covers {score}")  # pragma: no cover - the table is total


def clamp_modifier(value: int) -> int:
    """Attribute *bonus* modifiers from gear may not leave -2..+2 unless a rule says so."""
    return max(MODIFIER_FLOOR, min(MODIFIER_CEILING, int(value)))


def attribute_total(*modifiers: int) -> int:
    """Stack the highest modifier plus any named bonuses, then clamp to the canon band."""
    return clamp_modifier(sum(int(m) for m in modifiers))


# --------------------------------------------------------------------------- #
# Skill checks
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class SkillCheck:
    attribute: str
    attribute_score: int
    attribute_modifier: int
    skill_level: int | None
    dice: tuple[int, ...]
    situational: int
    difficulty: int
    total: int
    success: bool

    @property
    def margin(self) -> int:
        return self.total - self.difficulty

    @property
    def untrained(self) -> bool:
        return self.skill_level is None


def roll_check_dice(rng: DiceSource | None = None) -> tuple[int, ...]:
    source = rng if rng is not None else random
    return tuple(source.randint(1, CHECK_DICE_SIDES) for _ in range(CHECK_DICE_COUNT))


def resolve_skill_check(
    *,
    attribute: str,
    score: int,
    skill_level: int | None,
    difficulty: int,
    rng: DiceSource | None = None,
    dice: Sequence[int] | None = None,
    situational: int = 0,
) -> SkillCheck:
    """One skill check: ``2d6 + attribute modifier + skill level >= difficulty``.

    ``skill_level=None`` means *untrained*: the character does not even have level-0, and the canon's
    -1 penalty applies. That is deliberately distinct from level-0, which is basic competence.

    ``situational`` is the canon's -2..+2 band; it is validated rather than clamped so a caller cannot
    silently exceed what the rules permit.
    """
    code = _require_attribute(attribute)
    level = None if skill_level is None else _validate_skill_level(skill_level)
    if not SITUATIONAL_MIN <= int(situational) <= SITUATIONAL_MAX:
        raise WNError(
            f"situational modifier must be {SITUATIONAL_MIN}..{SITUATIONAL_MAX}, got {situational}"
        )
    modifier = attribute_modifier(score)

    if dice is None:
        rolled = roll_check_dice(rng)
    else:
        rolled = tuple(int(d) for d in dice)
        if len(rolled) != CHECK_DICE_COUNT:
            raise WNError(f"a {CHECK_DICE} check needs exactly {CHECK_DICE_COUNT} dice, got {len(rolled)}")
        if not all(1 <= d <= CHECK_DICE_SIDES for d in rolled):
            raise WNError(f"each die must be 1..{CHECK_DICE_SIDES}, got {rolled}")

    penalty = UNSKILLED_PENALTY if level is None else 0
    total = sum(rolled) + modifier + (level or 0) + penalty + int(situational)
    return SkillCheck(
        attribute=code,
        attribute_score=int(score),
        attribute_modifier=modifier,
        skill_level=level,
        dice=rolled,
        situational=int(situational),
        difficulty=int(difficulty),
        total=total,
        success=total >= int(difficulty),
    )


def _require_attribute(code: str) -> str:
    key = str(code).upper()
    if key not in ATTRIBUTES:
        raise WNError(f"unknown attribute {code!r}; expected one of {ATTRIBUTES}")
    return key


def _validate_skill_level(level: int) -> int:
    level = int(level)
    if not SKILL_MIN <= level <= SKILL_MAX:
        raise WNError(f"skill level must be {SKILL_MIN}..{SKILL_MAX}, got {level}")
    return level


def difficulty_for(target: int, *, nearest: bool = False) -> str:
    """The ladder's name for a difficulty, or a refusal that says so."""
    target = int(target)
    if target in DIFFICULTIES:
        return DIFFICULTIES[target]
    if nearest and DIFFICULTY_LADDER:
        closest = min(DIFFICULTY_LADDER, key=lambda step: (abs(step - target), step))
        return f"{DIFFICULTIES[closest]} (nearest rung to {target}; the ladder is {list(DIFFICULTY_LADDER)})"
    return f"No ladder rung at {target}; the ladder is {list(DIFFICULTY_LADDER)}."


# --------------------------------------------------------------------------- #
# Saving throws
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class SaveResult:
    kind: str
    target: int
    die: int
    success: bool
    natural: bool

    @property
    def margin(self) -> int:
        return self.die - self.target


def save_target(kind: str, *, level: int = 1, modifiers: dict[str, int] | None = None) -> int:
    """``16 - level - highest listed attribute modifier``; Luck has no attribute modifiers."""
    key = _require_save(kind)
    entry = CANON["saves"]["types"][key]
    attrs = tuple(entry["attributes"])
    mods = modifiers or {}
    best = max((int(mods.get(attr, 0)) for attr in attrs), default=0) if attrs else 0
    return SAVE_TARGET_BASE - int(level) - best


def roll_save(
    kind: str,
    *,
    level: int = 1,
    modifiers: dict[str, int] | None = None,
    rng: DiceSource | None = None,
    die: int | None = None,
) -> SaveResult:
    """A saving throw: a natural 1 always fails and a natural 20 always succeeds."""
    target = save_target(kind, level=level, modifiers=modifiers)
    source = rng if rng is not None else random
    rolled = source.randint(1, SAVE_DIE) if die is None else int(die)
    if not 1 <= rolled <= SAVE_DIE:
        raise WNError(f"a save roll must be 1..{SAVE_DIE}, got {rolled}")
    natural = rolled in (1, SAVE_DIE)
    success = (rolled >= target) if not natural else rolled == SAVE_DIE
    return SaveResult(kind=_require_save(kind), target=target, die=rolled, success=success, natural=natural)


def _require_save(kind: str) -> str:
    key = str(kind).lower()
    if key not in SAVE_TYPES:
        raise WNError(f"unknown save type {kind!r}; expected one of {SAVE_TYPES}")
    return key


# --------------------------------------------------------------------------- #
# Migration from the transitional 1d10 layer
# --------------------------------------------------------------------------- #

#: How the legacy six STATs fold into the family's six attributes. Two legacy STATs have no
#: counterpart — CYB and PSY — and are carried by skills and Edges instead of by an attribute.
LEGACY_STAT_MAP: dict[str, str] = {
    "FIT": "STR",
    "REF": "DEX",
    "INT": "INT",
    "SOC": "CHA",
    "CYB": "INT",
    "PSY": "WIS",
}


def from_legacy_stat(value: int) -> int:
    """Map a legacy 1..10 STAT to a 3..18 attribute, preserving rank order.

    The two scales are both linear, so the mapping is a linear stretch: 1 -> 3, 10 -> 18.
    """
    value = int(value)
    if not 1 <= value <= 10:
        raise WNError(f"a legacy STAT is 1..10, got {value}")
    return ATTRIBUTE_MIN + round((value - 1) * (ATTRIBUTE_MAX - ATTRIBUTE_MIN) / 9)


def from_legacy_skill(value: int) -> int:
    """Map a legacy 1..10 skill rating to a family level 0..4 (1..2 -> 0, 3..4 -> 1, ... 9..10 -> 4)."""
    value = int(value)
    if not 1 <= value <= 10:
        raise WNError(f"a legacy skill rating is 1..10, got {value}")
    return min(SKILL_MAX, (value - 1) // 2)


def from_legacy_check_total(total: int, *, stat: int, skill: int, die: int) -> int:
    """Re-base an old check's total onto the new arithmetic, for log/record conversion only."""
    return int(total) - int(stat) - int(skill) - int(die)
