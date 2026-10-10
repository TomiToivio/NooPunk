"""Issue #217 AC2 — the resolution semantics that were still open. NOT canonical.

`IS_CANONICAL = False`. This consumes `src/rules/kernel_prototype.py` and the author-directed
scale in `data/rules/fudge_scale_migration.json`; it re-implements neither, and it changes no
shipped behaviour (`src/rules/core.py` is untouched).

## What was already done, and is therefore NOT here

Three of AC2's five named items already existed before this module, and re-stating them would
have created a second definition of the same rule:

===========================  ==========================================================
tie / opposed checks         ``kernel_prototype.opposed_ladder`` — equal totals stay an
                             unresolved tie; ``core.compare_opposed`` pins the same rule
                             for the shipped engine.
bounded modifiers            ``kernel_prototype.resolve_ladder(cap_situational=True)``
                             caps situational steps at ``MAX_SITUATIONAL_STEPS`` (±2).
action points                Cross-domain; owned by #225, not this issue.
===========================  ==========================================================

## What is implemented here

**1. Trained / untrained −1.** The issue names the rule ("trained/untrained -1") but nothing
implemented it: :func:`rating_step` maps a Skill rating straight onto the ladder with no notion
of training. An untrained Skill now applies :data:`UNTRAINED_STEP_PENALTY` to the combined
step, **after** the candidate has combined STAT and Skill, so it composes with all three
candidates instead of being baked into one.

**2. An explicit partial-success band, OFF by default.** The prototype's bands are
``failure`` (margin < 0), ``success`` (0 ≤ margin < :data:`SUCCESS_WITH_STYLE_MARGIN`) and
``success_with_style``. There is no partial success, and where one *should* sit is a design
decision, not an implementation detail — so this module **measures** the readings rather than
silently picking one:

- ``PARTIAL_AT_MINUS_ONE`` — a one-step miss is a partial with a cost. Costs the failure rate
  directly (it converts every margin −1 result).
- ``PARTIAL_AT_ZERO`` — a bare success becomes partial-with-cost and full success needs +1.
  This makes full success strictly harder, which is a balance change, not a vocabulary change.
- ``PARTIAL_OFF`` — today's behaviour, preserved as the default.

The recommendation is ``PARTIAL_AT_MINUS_ONE``, because it adds a band without moving the
boundary of success; but the author owns it, and passing ``partial=PARTIAL_OFF`` reproduces the
current bands exactly.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
from typing import Literal

from .kernel_prototype import (
    CANDIDATES,
    LADDER_MAX,
    LADDER_MIN,
    SUCCESS_WITH_STYLE_MARGIN,
    clamp_step,
    combine_skill_primary,
    rating_step,
)

IS_CANONICAL = False

#: An untrained Skill's penalty, in ladder steps. Named by #217's AC2.
UNTRAINED_STEP_PENALTY = -1

PartialPolicy = Literal["off", "at_minus_one", "at_zero"]
PARTIAL_OFF: PartialPolicy = "off"
PARTIAL_AT_MINUS_ONE: PartialPolicy = "at_minus_one"
PARTIAL_AT_ZERO: PartialPolicy = "at_zero"

#: Exact 4dF distribution over its 81 equally likely outcomes (mean 0, range −4..+4).
FDF_DISTRIBUTION: dict[int, Fraction] = {
    total: Fraction(count, 81)
    for total, count in sorted(Counter(map(sum, product((-1, 0, 1), repeat=4))).items())
}

OUTCOMES = ("failure", "partial", "success", "success_with_style")


def apply_training(step: int, *, trained: bool) -> int:
    """Apply the untrained penalty to an already-combined step, then clamp to the ladder."""
    return clamp_step(int(step) + (0 if trained else UNTRAINED_STEP_PENALTY))


def combined_step(candidate: str, stat: int, skill: int, *, trained: bool = True) -> int:
    """Candidate combination, then training, in that order.

    Order matters and is stated rather than implied: training is a property of the *character*,
    not of the combination rule, so it must compose with A, B and C identically and must not be
    folded into one of them.
    """
    if candidate not in CANDIDATES:
        raise ValueError(f"Unknown candidate {candidate!r}; expected one of {sorted(CANDIDATES)}.")
    return apply_training(CANDIDATES[candidate](stat, skill), trained=trained)


def outcome_for(margin: int, *, partial: PartialPolicy = PARTIAL_OFF) -> str:
    """Map a margin onto an outcome band under the chosen partial-success policy."""
    if partial not in (PARTIAL_OFF, PARTIAL_AT_MINUS_ONE, PARTIAL_AT_ZERO):
        raise ValueError(f"Unknown partial-success policy {partial!r}.")
    if margin < 0:
        if partial == PARTIAL_AT_MINUS_ONE and margin == -1:
            return "partial"
        return "failure"
    if partial == PARTIAL_AT_ZERO and margin == 0:
        return "partial"
    if margin < SUCCESS_WITH_STYLE_MARGIN:
        return "success"
    return "success_with_style"


def outcome_distribution(
    *,
    candidate: str,
    stat: int,
    skill: int,
    difficulty: int,
    trained: bool = True,
    situational: int = 0,
    partial: PartialPolicy = PARTIAL_OFF,
) -> dict[str, Fraction]:
    """Exact probability of each outcome band. No simulation, no seed.

    Margins outside the reachable range contribute nothing, so the four bands always sum to 1
    for any input — which the guard asserts rather than assumes.
    """
    step = combined_step(candidate, stat, skill, trained=trained)
    target = clamp_step(int(difficulty))
    base = step + int(situational) - target
    tally: dict[str, Fraction] = {name: Fraction(0) for name in OUTCOMES}
    for dice, chance in FDF_DISTRIBUTION.items():
        tally[outcome_for(base + dice, partial=partial)] += chance
    return tally


def p_success_at_least(
    *,
    candidate: str,
    stat: int,
    skill: int,
    difficulty: int,
    trained: bool = True,
    situational: int = 0,
) -> Fraction:
    """Exact chance of ``success`` or better — the quantity a trained/untrained comparison needs."""
    step = combined_step(candidate, stat, skill, trained=trained)
    base = step + int(situational) - clamp_step(int(difficulty))
    return sum(
        (chance for dice, chance in FDF_DISTRIBUTION.items() if base + dice >= 0),
        Fraction(0),
    )


def untrained_cost(
    *,
    candidate: str = "C_skill_primary",
    stat: int = 5,
    skill: int = 5,
    difficulty: int = 0,
    situational: int = 0,
) -> Fraction:
    """How much competence the untrained penalty removes, as an exact probability drop."""
    return (
        p_success_at_least(
            candidate=candidate, stat=stat, skill=skill, difficulty=difficulty,
            trained=True, situational=situational,
        )
        - p_success_at_least(
            candidate=candidate, stat=stat, skill=skill, difficulty=difficulty,
            trained=False, situational=situational,
        )
    )


def ladder_bounds() -> tuple[int, int]:
    """The reachable step range, exposed so a guard can test the clamp without importing it."""
    return LADDER_MIN, LADDER_MAX


def default_candidate() -> str:
    """The candidate the prototype recommends, named once rather than repeated as a literal."""
    return "C_skill_primary"


__all__ = [
    "FDF_DISTRIBUTION",
    "IS_CANONICAL",
    "OUTCOMES",
    "PARTIAL_AT_MINUS_ONE",
    "PARTIAL_AT_ZERO",
    "PARTIAL_OFF",
    "UNTRAINED_STEP_PENALTY",
    "apply_training",
    "combine_skill_primary",
    "combined_step",
    "default_candidate",
    "ladder_bounds",
    "outcome_distribution",
    "outcome_for",
    "p_success_at_least",
    "rating_step",
    "untrained_cost",
]
