"""The Without Number kernel, adopted as NoöPunk's baseline.

**Author ruling, 2026-10-26:** *"use CWN/SWN/AWN/WWN system for everything. Make the stats,
skills, all rules based on them. We will modify later."* This module is the arithmetic of that
decision, and it supersedes the earlier "`1d10` stays" ruling (#566 / D40) for the tabletop layer.

What is implemented here is what was **verified against the SRD**, not what seemed plausible:

* six attributes on a 3-18 scale (``1.1.1``), and the modifier bands from ``1.1.2``;
* the skill check as ``2d6 + attribute modifier + skill level`` against a difficulty;
* the difficulty bands ``6 / 8 / 10 / 12 / 14`` (``2.3.1``);
* situational circumstances bounded at ``-2..+2``, aid capped at ``+1``, opposed checks won by the
  higher roll (``2.3.3``/``2.3.4``).

**Deliberately absent:** saving throws, classes and Edges, Foci, Effort, Shock/Trauma and
progression. Each needs its own verified reading, and inventing any of them would put a number in
the repo that no source supports. They are the next slices, not omissions by accident.

Provenance: mechanics taken from the *Worlds Without Number* SRD, which is CC0 (verified
2026-10-25 in ``data/sources/game_system_rights.json``). *Cities Without Number* shares this engine
and is also CC0. *Stars Without Number* and *Ashes Without Number* have no verified SRD and remain
``blocked-unverified`` — this module therefore cites neither, and their material stays a design
reference. No SRD prose is reproduced; the expression here is original.
"""
from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

#: The six attribute names, in the SRD's order. These replace NooPunk's earlier
#: FIT/REF/INT/SOC/CYB/PSY set for the tabletop layer, by author ruling 2026-10-26.
ATTRIBUTES: tuple[str, ...] = (
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma",
)

ATTRIBUTE_MIN = 3
ATTRIBUTE_MAX = 18
MODIFIER_CAP = 2

#: Difficulty bands, verified from SRD 2.3.1. Names paraphrase the SRD's own descriptions.
DIFFICULTY_SIMPLE = 6        # still more than the PC's background would cover
DIFFICULTY_SIGNIFICANT = 8   # a competent professional, succeeding more often than not
DIFFICULTY_EXPERT = 10       # beyond anyone but a skilled expert
DIFFICULTY_MASTER = 12       # only a true master, reliably
DIFFICULTY_EXTREME = 14      # only a true master, and probably failing

SITUATIONAL_MIN = -2
SITUATIONAL_MAX = 2
AID_BONUS_MAX = 1

SKILL_CHECK_DICE = 2
SKILL_CHECK_FACES = 6


class WnError(ValueError):
    """A constraint from the SRD was about to be violated."""


def attribute_modifier(score: int) -> int:
    """The modifier for an attribute score (SRD 1.1.2).

    3 -> -2, 4-7 -> -1, 8-13 -> +0, 14-17 -> +1, 18 -> +2.

    The +/-2 bound is the *base* modifier cap; abilities may raise it, which is why the
    cap is applied here as a band rather than clamped on the result.
    """
    if not ATTRIBUTE_MIN <= score <= ATTRIBUTE_MAX:
        raise WnError(f"attribute score must be {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX}, got {score}")
    if score <= 3:
        return -2
    if score <= 7:
        return -1
    if score <= 13:
        return 0
    if score <= 17:
        return 1
    return 2


def clamp_situational(value: int) -> int:
    """Circumstances adjust a check by at most -2..+2 (SRD 2.3.1).

    Gear mods, magic items and aid are explicitly outside this bound, so only caller-supplied
    circumstance lives here. Clamping rather than raising keeps a referee's table moving.
    """
    return max(SITUATIONAL_MIN, min(SITUATIONAL_MAX, value))


def clamp_aid(value: int) -> int:
    """Aid tops out at +1 however many allies help (SRD 2.3.3)."""
    return max(0, min(AID_BONUS_MAX, value))


@dataclass(frozen=True)
class Check:
    """One resolved skill check."""

    dice: tuple[int, int]
    attribute_modifier: int
    skill_level: int
    situational: int
    aid: int
    difficulty: int

    @property
    def total(self) -> int:
        return (sum(self.dice) + self.attribute_modifier + self.skill_level
                + self.situational + self.aid)

    @property
    def success(self) -> bool:
        return self.total >= self.difficulty

    @property
    def margin(self) -> int:
        return self.total - self.difficulty


def _roll(rng: Any = None, dice: Sequence[int] | None = None) -> tuple[int, int]:
    if dice is not None:
        pair = tuple(int(d) for d in dice)
        if len(pair) != 2 or any(not 1 <= d <= SKILL_CHECK_FACES for d in pair):
            raise WnError(f"each die must be 1..{SKILL_CHECK_FACES}, got {dice}")
        return pair  # type: ignore[return-value]
    source = rng if rng is not None else random.Random()
    return (source.randint(1, SKILL_CHECK_FACES), source.randint(1, SKILL_CHECK_FACES))


def skill_check(
    *,
    attribute_score: int,
    skill_level: int,
    difficulty: int,
    situational: int = 0,
    aid: int = 0,
    rng: Any = None,
    dice: Sequence[int] | None = None,
) -> Check:
    """`2d6 + attribute modifier + skill level` against a difficulty.

    The dice may be supplied directly (`dice=(3, 5)`) for a table that rolled real dice, or a
    seeded `rng` may be passed for a replayable digital resolution.
    """
    if skill_level < 0:
        raise WnError(f"skill level cannot be negative, got {skill_level}")
    return Check(
        dice=_roll(rng, dice),
        attribute_modifier=attribute_modifier(attribute_score),
        skill_level=skill_level,
        situational=clamp_situational(situational),
        aid=clamp_aid(aid),
        difficulty=difficulty,
    )


def opposed_check(
    *,
    a: Sequence[int],
    b: Sequence[int],
) -> str | None:
    """Opposed checks: the higher roll wins (SRD 2.3.4).

    Returns "a", "b", or **None on a tie** — the SRD states the winner is the one who rolls
    higher and does not say what a tie means, so this reports the ambiguity instead of inventing
    a tie-break. A caller that needs one must supply its own procedure.
    """
    ta, tb = sum(a), sum(b)
    if ta == tb:
        return None
    return "a" if ta > tb else "b"
