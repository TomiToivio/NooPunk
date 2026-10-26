"""Cities Without Number: character advancement.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``), section ``rules-of-the-game/character-advancement/``.

The SRD gives two progression tracks — "fast" and "slow" — both totalling *accumulated* experience,
not experience since the last level. It then lists what a level grants: hit points, saving throws,
attack bonus, skill points (with per-rank costs and level prerequisites), optional attribute boosts,
and Focus/Edge picks at levels 2, 5, 7 and 10.

This module owns the arithmetic of those grants. It does not own a character's stored level or spent
points: a campaign or a save file does, because those are bookkeeping, not rules.

## Deliberate omissions

* **Edge and Focus text** is content, not arithmetic; only the *levels* at which a pick is available
  and the *retroactivity* of the fifth-level Edge are represented.
* The Underdog Rule and other optional character-creation variants are not modelled.
"""
from __future__ import annotations

import random
from collections.abc import Iterable

#: SRD: new characters begin at first level and can rise to tenth under the default rules.
MIN_LEVEL = 1
MAX_LEVEL = 10

#: SRD: "PCs gain three experience points for an average successful mission".
DEFAULT_XP_PER_MISSION = 3

#: Accumulated XP thresholds (SRD table).
XP_FOR_LEVEL: dict[str, dict[int, int]] = {
    "fast": {
        1: 0,
        2: 3,
        3: 6,
        4: 12,
        5: 18,
        6: 27,
        7: 39,
        8: 54,
        9: 72,
        10: 93,
    },
    "slow": {
        1: 0,
        2: 6,
        3: 15,
        4: 24,
        5: 36,
        6: 51,
        7: 69,
        8: 87,
        9: 105,
        10: 139,
    },
}

#: SRD: a level grants three skill points; the Educated Edge grants a fourth.
SKILL_POINTS_PER_LEVEL = 3
EDUCATED_BONUS_POINTS = 1

#: SRD table: point cost and minimum character level for each skill rank.
SKILL_POINT_COST: dict[int, int] = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}
SKILL_MIN_CHARACTER_LEVEL: dict[int, int] = {0: 1, 1: 1, 2: 3, 3: 6, 4: 9}
MAX_SKILL_RANK = 4

#: SRD: the nth attribute boost costs n points; five total, gated by character level.
ATTRIBUTE_BOOST_LIMIT = 5
ATTRIBUTE_BOOST_MIN_CHARACTER_LEVEL: dict[int, int] = {1: 1, 2: 1, 3: 3, 4: 6, 5: 9}

#: SRD: "At levels 2, 5, 7, and 10 a PC can add a level to an existing Focus or pick up a new one."
FOCUS_LEVELS: tuple[int, ...] = (2, 5, 7, 10)

#: SRD: "upon reaching fifth level, an operator can pick a third Edge".
THIRD_EDGE_LEVEL = 5

#: SRD: hit points are rolled with 1d6 per level, +2 per die with the Hard to Kill Edge.
HIT_DIE_FACES = 6
HARD_TO_KILL_BONUS = 2


class AdvancementError(ValueError):
    """A constraint from the SRD was about to be violated."""


def level_for_xp(xp: int, *, track: str = "fast") -> int:
    """The highest level whose accumulated-XP threshold has been reached."""
    if xp < 0:
        raise AdvancementError("experience cannot be negative")
    table = _xp_table(track)
    level = MIN_LEVEL
    for candidate, threshold in sorted(table.items()):
        if xp >= threshold:
            level = candidate
        else:
            break
    return level


def xp_for_next_level(level: int, *, track: str = "fast") -> int | None:
    """The accumulated XP needed for the next level, or ``None`` at the cap."""
    table = _xp_table(track)
    if level >= MAX_LEVEL:
        return None
    return table[level + 1]


def _xp_table(track: str) -> dict[int, int]:
    try:
        return XP_FOR_LEVEL[track]
    except KeyError as exc:  # pragma: no cover - defensive
        raise AdvancementError(f"unknown advancement track {track!r}") from exc


def attack_bonus(level: int, *, on_target: bool = False) -> int:
    """Half the character's level, rounded down — full level with the On Target Edge."""
    _check_level(level)
    return level if on_target else level // 2


def save_target(level: int) -> int:
    """``16 - level`` before attribute modifiers; 15 at first level, as the SRD notes."""
    _check_level(level)
    return 16 - level


def skill_points_for_level(*, educated: bool = False) -> int:
    """Three points per level, plus one with the Educated Edge."""
    return SKILL_POINTS_PER_LEVEL + (EDUCATED_BONUS_POINTS if educated else 0)


def skill_point_cost(rank: int) -> int:
    """Point cost of the *next* rank: every rank is bought in order."""
    if rank not in SKILL_POINT_COST:
        raise AdvancementError(f"skill rank must be 0..{MAX_SKILL_RANK}, got {rank}")
    return SKILL_POINT_COST[rank]


def skill_rank_allowed(rank: int, character_level: int) -> bool:
    """Whether a character is high enough level to hold this rank."""
    _check_level(character_level)
    if rank not in SKILL_MIN_CHARACTER_LEVEL:
        raise AdvancementError(f"skill rank must be 0..{MAX_SKILL_RANK}, got {rank}")
    return character_level >= SKILL_MIN_CHARACTER_LEVEL[rank]


def total_skill_cost(target_rank: int) -> int:
    """Points required to reach ``target_rank`` from untrained, buying each rank in order."""
    if target_rank < 0 or target_rank > MAX_SKILL_RANK:
        raise AdvancementError(f"target rank must be 0..{MAX_SKILL_RANK}")
    return sum(SKILL_POINT_COST[rank] for rank in range(target_rank + 1))


def attribute_boost_cost(nth: int) -> int:
    """The nth attribute boost costs n points (first 1, second 2, ... fifth 5)."""
    if nth < 1 or nth > ATTRIBUTE_BOOST_LIMIT:
        raise AdvancementError(f"attribute boosts are numbered 1..{ATTRIBUTE_BOOST_LIMIT}")
    return nth


def attribute_boost_allowed(nth: int, character_level: int) -> bool:
    """Whether the character is high enough level for that boost."""
    _check_level(character_level)
    return character_level >= ATTRIBUTE_BOOST_MIN_CHARACTER_LEVEL[attribute_boost_cost(nth)]


def focus_picks_at(level: int) -> int:
    """How many Focus picks a character of this level has had (levels 2, 5, 7, 10)."""
    _check_level(level)
    return sum(1 for focus_level in FOCUS_LEVELS if level >= focus_level)


def has_third_edge(level: int) -> bool:
    """The third Edge becomes selectable at fifth level."""
    _check_level(level)
    return level >= THIRD_EDGE_LEVEL


def hit_points_rolled(
    level: int,
    constitution_modifier: int,
    *,
    hard_to_kill: bool = False,
    dice: Iterable[int] | None = None,
) -> int:
    """The total of the level's hit dice, each with the Constitution modifier, floored at 1."""
    _check_level(level)
    bonus = HARD_TO_KILL_BONUS if hard_to_kill else 0
    if dice is None:
        rolls = [random.randint(1, HIT_DIE_FACES) for _ in range(level)]
    else:
        rolls = list(dice)
        if len(rolls) != level:
            raise AdvancementError(
                f"expected {level} hit dice, got {len(rolls)}"
            )
        if any(face < 1 or face > HIT_DIE_FACES for face in rolls):
            raise AdvancementError(f"hit dice must be 1..{HIT_DIE_FACES}")
    return sum(max(1, face + bonus + constitution_modifier) for face in rolls)


def new_maximum_hit_points(current_maximum: int, rolled: int) -> int:
    """Take the roll if it beats the current maximum, otherwise gain one point."""
    if current_maximum < 1:
        raise AdvancementError("current maximum hit points must be at least 1")
    if rolled < 1:
        raise AdvancementError("a hit point roll must be at least 1")
    return rolled if rolled > current_maximum else current_maximum + 1


def _check_level(level: int) -> None:
    if level < MIN_LEVEL or level > MAX_LEVEL:
        raise AdvancementError(f"character level must be {MIN_LEVEL}..{MAX_LEVEL}, got {level}")
