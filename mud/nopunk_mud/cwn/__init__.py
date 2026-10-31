"""CWN core for the MUD (#950).

A clean, dependency-free port of the published Without Number procedures the Evennia commands need: attribute
modifiers, skill checks, saving throws, hit points and System Strain. It is **not** a homebrew resolution
system — every function here implements a rule that already exists in `src/rules/` (Python) and `godot/core/`
(GDScript), and `tests/test_mud_cwn_parity_950.py` at the repository root compares the three where they overlap.

Why a port rather than an import: the MUD ships as its own package with its own environment (ADR #946). A
runtime import of `src/rules` would couple two deployment units; a parity test keeps them honest without
coupling them.

Source of truth: the linked CWN SRD (https://cwn.quadrifons.com/). Coverage and gaps are recorded in
`data/rules/cwn_compliance_matrix.json` and `docs/rules/CWN_COMPLIANCE_MATRIX_950.md`.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

ATTRIBUTES = ("Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma")
ATTRIBUTE_MIN = 3
ATTRIBUTE_MAX = 18
SKILL_RANK_MIN = -1
SKILL_RANK_MAX = 4
UNTRAINED_MODIFIER = -1

SAVE_DIE_FACES = 20
SAVE_BASE = 16
SAVE_ATTRIBUTES: dict[str, tuple[str, ...]] = {
    "Physical": ("Strength", "Constitution"),
    "Evasion": ("Dexterity", "Intelligence"),
    "Mental": ("Wisdom", "Charisma"),
    "Luck": (),
}

HIT_DIE_FACES = 6
HARD_TO_KILL_BONUS = 2
MIN_LEVEL = 1
MAX_LEVEL = 10

LIFESTYLE_STRAIN: dict[str, int] = {
    "squatter": -2, "slum": -1, "ordinary": 0, "fine": 1, "luxury": 2,
}

#: 2d6 difficulty bands.
DIFFICULTIES: dict[str, int] = {"easy": 6, "routine": 8, "hard": 10, "very_hard": 12, "heroic": 14}


class CwnError(ValueError):
    """An illegal CWN input. The message names the rule that refused it."""


# ---- attributes -----------------------------------------------------------------------------------

def attribute_modifier(score: int) -> int:
    """3 -> -2, 4-7 -> -1, 8-13 -> 0, 14-17 -> +1, 18 -> +2 (SRD 1.1.2)."""
    if not ATTRIBUTE_MIN <= score <= ATTRIBUTE_MAX:
        raise CwnError(f"attribute score must be {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX}, got {score}")
    if score <= 3:
        return -2
    if score <= 7:
        return -1
    if score <= 13:
        return 0
    if score <= 17:
        return 1
    return 2


def validate_sheet(attributes: Mapping[str, int]) -> list[str]:
    """Problems with an attribute block. Empty means it may be used."""
    problems: list[str] = []
    for name in ATTRIBUTES:
        if name not in attributes:
            problems.append(f"missing attribute: {name}")
            continue
        score = int(attributes[name])
        if not ATTRIBUTE_MIN <= score <= ATTRIBUTE_MAX:
            problems.append(f"{name} {score} outside {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX}")
    return problems


# ---- checks ---------------------------------------------------------------------------------------

@dataclass(frozen=True)
class CheckResult:
    total: int
    target: int
    dice: tuple[int, int]
    success: bool


def skill_modifier(rank: int) -> int:
    """Rank 0 is trained; only -1 is untrained."""
    if not SKILL_RANK_MIN <= rank <= SKILL_RANK_MAX:
        raise CwnError(f"skill rank must be {SKILL_RANK_MIN}..{SKILL_RANK_MAX}, got {rank}")
    return UNTRAINED_MODIFIER if rank < 0 else rank


def skill_check(*, rank: int, attribute: int, difficulty: int, dice: Sequence[int],
                circumstances: int = 0, aid: int = 0) -> CheckResult:
    """2d6 + rank + attribute modifier + circumstances + aid against a difficulty band."""
    if len(dice) != 2:
        raise CwnError(f"a skill check rolls 2d6, got {len(dice)} dice")
    if any(not 1 <= int(face) <= 6 for face in dice):
        raise CwnError("each die shows 1..6")
    if difficulty not in DIFFICULTIES.values():
        raise CwnError(f"difficulty {difficulty} is not a published band")
    if not -2 <= circumstances <= 2:
        raise CwnError("circumstances cap at +/-2")
    if not 0 <= aid <= 1:
        raise CwnError("assistance is capped at +1")
    total = (int(dice[0]) + int(dice[1]) + skill_modifier(rank)
             + attribute_modifier(attribute) + circumstances + aid)
    return CheckResult(total=total, target=difficulty, dice=(int(dice[0]), int(dice[1])),
                       success=total >= difficulty)


# ---- saves ----------------------------------------------------------------------------------------

def save_target(kind: str, *, level: int, attributes: Mapping[str, int]) -> int:
    """16 - level - best attribute modifier of the save's pair. Luck ignores attributes."""
    if kind not in SAVE_ATTRIBUTES:
        raise CwnError(f"unknown save {kind!r}; expected one of {tuple(SAVE_ATTRIBUTES)}")
    if not MIN_LEVEL <= level <= MAX_LEVEL:
        raise CwnError(f"character level must be {MIN_LEVEL}..{MAX_LEVEL}, got {level}")
    pair = SAVE_ATTRIBUTES[kind]
    best = max((attribute_modifier(int(attributes[name])) for name in pair if name in attributes),
               default=0)
    return SAVE_BASE - level - best


def saving_throw(kind: str, *, level: int, attributes: Mapping[str, int], die: int,
                 bonus: int = 0) -> dict[str, object]:
    """A d20 save: natural 1 fails, natural 20 succeeds, otherwise total >= target."""
    if not 1 <= die <= SAVE_DIE_FACES:
        raise CwnError(f"a d20 shows 1..{SAVE_DIE_FACES}, got {die}")
    target = save_target(kind, level=level, attributes=attributes)
    total = die + bonus
    if die == 1:
        success = False
    elif die == SAVE_DIE_FACES:
        success = True
    else:
        success = total >= target
    return {"kind": kind, "die": die, "bonus": bonus, "target": target,
            "total": total, "success": success, "natural": die in (1, SAVE_DIE_FACES)}


# ---- hit points and strain ------------------------------------------------------------------------

def hit_points(level: int, constitution_modifier: int, *, dice: Iterable[int] | None = None,
               hard_to_kill: bool = False) -> int:
    """Total of the level's hit dice, each with the Constitution modifier, floored at 1."""
    if not MIN_LEVEL <= level <= MAX_LEVEL:
        raise CwnError(f"character level must be {MIN_LEVEL}..{MAX_LEVEL}, got {level}")
    bonus = HARD_TO_KILL_BONUS if hard_to_kill else 0
    if dice is None:
        rolls = [random.randint(1, HIT_DIE_FACES) for _ in range(level)]
    else:
        rolls = [int(face) for face in dice]
        if len(rolls) != level:
            raise CwnError(f"expected {level} hit dice, got {len(rolls)}")
        if any(not 1 <= face <= HIT_DIE_FACES for face in rolls):
            raise CwnError(f"hit dice must be 1..{HIT_DIE_FACES}")
    return sum(max(1, face + bonus + constitution_modifier) for face in rolls)


def strain_maximum(constitution: int, *, lifestyle: str = "ordinary") -> int:
    """Constitution adjusted by lifestyle, never below zero."""
    if lifestyle not in LIFESTYLE_STRAIN:
        raise CwnError(f"unknown lifestyle {lifestyle!r}")
    if not ATTRIBUTE_MIN <= constitution <= ATTRIBUTE_MAX:
        raise CwnError("Constitution must be within 3-18")
    return max(0, constitution + LIFESTYLE_STRAIN[lifestyle])


# ---- character sheet ------------------------------------------------------------------------------

@dataclass(frozen=True)
class Character:
    """The minimum a MUD command needs to resolve a check or a save."""

    name: str
    attributes: dict[str, int]
    skills: dict[str, int]
    level: int = 1
    background: str = ""

    def modifier(self, attribute: str) -> int:
        return attribute_modifier(self.attributes[attribute])

    def saves(self) -> dict[str, int]:
        return {kind: save_target(kind, level=self.level, attributes=self.attributes)
                for kind in SAVE_ATTRIBUTES}

    def max_hit_points(self, dice: Iterable[int] | None = None) -> int:
        return hit_points(self.level, self.modifier("Constitution"), dice=dice)

    def strain_capacity(self, *, lifestyle: str = "ordinary") -> int:
        return strain_maximum(self.attributes["Constitution"], lifestyle=lifestyle)

    def check(self, skill: str, *, difficulty: int, dice: Sequence[int],
              circumstances: int = 0) -> CheckResult:
        rank = self.skills.get(skill, UNTRAINED_MODIFIER)
        return skill_check(rank=rank, attribute=self.attributes["Intelligence"],
                           difficulty=difficulty, dice=dice, circumstances=circumstances)


def create_character(name: str, *, attributes: Mapping[str, int], skills: Mapping[str, int] | None = None,
                     level: int = 1, background: str = "") -> Character:
    """Build a character, refusing an illegal sheet instead of repairing it silently."""
    if not str(name).strip():
        raise CwnError("a character needs a name")
    problems = validate_sheet(attributes)
    if problems:
        raise CwnError("; ".join(problems))
    for skill, rank in dict(skills or {}).items():
        if not SKILL_RANK_MIN <= int(rank) <= SKILL_RANK_MAX:
            raise CwnError(f"skill {skill!r} rank {rank} outside {SKILL_RANK_MIN}..{SKILL_RANK_MAX}")
    return Character(name=str(name), attributes={k: int(v) for k, v in attributes.items()},
                     skills={k: int(v) for k, v in dict(skills or {}).items()},
                     level=int(level), background=str(background))

# ---- combat ---------------------------------------------------------------------------------------
# Ported from the same procedures as the rest of this module: no second resolution system.

ATTACK_DIE_FACES = 20


@dataclass(frozen=True)
class Attack:
    die: int
    total: int
    armor_class: int
    hit: bool


def attack_roll(*, attack_bonus: int, attribute: int, combat_rank: int, armor_class: int,
                die: int) -> Attack:
    """d20 + attack bonus + attribute modifier + combat rank versus AC."""
    if not SKILL_RANK_MIN <= combat_rank <= SKILL_RANK_MAX:
        raise CwnError("combat rank outside -1..4")
    if armor_class < 1:
        raise CwnError("armour class must be positive")
    if not 1 <= die <= ATTACK_DIE_FACES:
        raise CwnError(f"attack die must be 1..{ATTACK_DIE_FACES}")
    total = die + attack_bonus + attribute_modifier(attribute) + combat_rank
    return Attack(die=die, total=total, armor_class=armor_class, hit=total >= armor_class)


def damage_roll(*, weapon_die: int, roll: int, attribute: int) -> int:
    """One weapon die plus the attribute modifier, never below zero."""
    if weapon_die not in (4, 6, 8, 10, 12):
        raise CwnError("unsupported weapon die")
    if not 1 <= roll <= weapon_die:
        raise CwnError(f"damage roll must be 1..{weapon_die}")
    return max(0, roll + attribute_modifier(attribute))


def strain_absorb(current: int, amount: int, constitution: int) -> dict[str, object]:
    """Absorb strain up to capacity; overflow is refused, never silently clamped."""
    if amount < 0 or current < 0:
        raise CwnError("strain values cannot be negative")
    capacity = strain_maximum(constitution)
    if current + amount > capacity:
        return {"ok": False, "current": current, "capacity": capacity,
                "overflow": current + amount - capacity}
    return {"ok": True, "current": current + amount, "capacity": capacity, "overflow": 0}
