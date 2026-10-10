"""Prototype: a Fudge/Fate-inspired kernel for issue #200. **NOT CANONICAL.**

Issue #200 replaces NoöPunk's closed-system design framing with a fully Creative
Commons direction built around a Fudge / Psi-Punk / Fate / Transhumanity's Fate
synthesis, and insists the numerical migration be **tested before it is locked**.
This module is that test rig, and nothing more.

Deliberate boundaries:

* :mod:`src.rules.core` and ``data/rules/core.json`` remain the authored, canonical
  ``STAT + Skill + 1d10`` check. Nothing here changes, replaces or bypasses them;
  the legacy path below *delegates* to the canonical engine rather than
  reimplementing it, so the migration benchmark cannot drift from the real thing.
* Nothing here may be wired into a runtime until the author records a decision.
  ``AGENTS.md`` §13.9 and §15.2 fix the current 1–10 + 1d10 baseline as active, and
  §13.8 forbids silently redesigning the balances. A prototype is not a migration.
* **Separate Attributes and Skills are mandatory** (#200). Every candidate keeps the
  six STATs and a separate Skill rating; they differ only in how the two combine.
  That difference is the entire question the issue asks us to measure.

The four things #200 says to test, and where each is measured:

======================  =====================================================
additive Stat+Skill     ``CANDIDATES`` spread, :func:`edge_curve`
modifier stacking       :data:`MAX_SITUATIONAL_STEPS`, :func:`resolve_ladder`
opposed checks          :func:`opposed_ladder`, :func:`opposed_legacy`
combat lethality,       :func:`hits_to_takedown`, :func:`disparity`
high-end PSI/cyber
======================  =====================================================

Wording note: the ladder's *steps* are inspired by Fudge's trait ladder, but its
labels here are NoöPunk's own. A ladder of named steps is a procedure, not a
protected expression, and independently worded labels keep this prototype inside the
CC-compatible boundary the rights ledger records.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

from .core import (
    DIFFICULTIES,
    DIFFICULTY_LADDER,
    SKILL_LEVEL_MAX,
    SKILL_LEVEL_MIN,
    STAT_MAX,
    STAT_MIN,
    CheckResult,
    DiceSource,
    resolve_check,
)

#: This module is a prototype. If this ever becomes True, the migration happened.
IS_CANONICAL = False

#: Ladder step range, inclusive. Seven steps, centred on 0.
LADDER_MIN = -3
LADDER_MAX = 3

#: NoöPunk's own step labels. Deliberately NOT Fudge's names: the ladder shape is a
#: procedure we implement independently, the wording is ours.
LADDER_LABELS: dict[int, str] = {
    -3: "Abysmal",
    -2: "Poor",
    -1: "Weak",
    0: "Unremarkable",
    1: "Capable",
    2: "Strong",
    3: "Peak",
}

#: Fudge-style dice: four dice, each −1 / 0 / +1. Range −4..+4.
FDF_COUNT = 4
FDF_SIDES = 3

#: DRAFT cap on stacked situational modifiers, in ladder steps. Fate's own practice is
#: ±2 per invoke; #200 asks us to bound *stacking*, which is the pathology. This is a
#: prototype value awaiting playtest, not a canon number.
MAX_SITUATIONAL_STEPS = 2

#: DRAFT divisor mapping a 1–10 rating onto a ladder step. A step is ~1.5 rating
#: points, so 1 and 10 land exactly on ±3 and the middle two ratings share step 0.
LADDER_RATING_PIVOT = 5.5
LADDER_RATING_WIDTH = 1.5

#: DRAFT divisor converting a canonical Difficulty Value onto the ladder scale, for
#: migration comparison only. Derived from the median legacy total: an average
#: STAT 5 + Skill 5 + 1d10 has a median of 15.5, so DV 15.5 is ladder 0. Recorded as a
#: prototype calibration; it is NOT authored canon and the DVs above Heroic clamp.
LEGACY_DV_PIVOT = 15.5
LEGACY_DV_WIDTH = 2.0


def clamp_step(step: int) -> int:
    """Clamp any integer onto the seven-step ladder."""
    return max(LADDER_MIN, min(LADDER_MAX, int(step)))


def ladder_label(step: int) -> str:
    return LADDER_LABELS[clamp_step(step)]


# --------------------------------------------------------------------------------------
# Candidate combination rules. All three keep Attributes and Skills separate.
# --------------------------------------------------------------------------------------


def rating_step(rating: int, *, label: str = "rating") -> int:
    """Map a 1..10 STAT or Skill rating onto a ladder step."""
    value = int(rating)
    if not STAT_MIN <= value <= STAT_MAX:
        raise ValueError(f"{label} must be {STAT_MIN}..{STAT_MAX}.")
    raw = (value - LADDER_RATING_PIVOT) / LADDER_RATING_WIDTH
    return clamp_step(round(raw))


def combine_additive(stat: int, skill: int) -> int:
    """CANDIDATE A — add both steps. Widest spread; the one #200 warns about."""
    return clamp_step(rating_step(stat, label="STAT") + rating_step(skill, label="Skill"))


def combine_averaged(stat: int, skill: int) -> int:
    """CANDIDATE B — average the ratings, then map. Narrowest spread.

    The half-point case is resolved **half-up** by explicit integer arithmetic rather
    than left to :func:`round`, whose banker's rounding would make the mapping depend on
    a language detail instead of a design decision.
    """
    stat_value = int(stat)
    skill_value = int(skill)
    if not STAT_MIN <= stat_value <= STAT_MAX:
        raise ValueError(f"STAT must be {STAT_MIN}..{STAT_MAX}.")
    if not SKILL_LEVEL_MIN <= skill_value <= SKILL_LEVEL_MAX:
        raise ValueError(f"Skill must be {SKILL_LEVEL_MIN}..{SKILL_LEVEL_MAX}.")
    averaged = (stat_value + skill_value + 1) // 2  # round half up
    return rating_step(averaged, label="averaged rating")


def combine_skill_primary(stat: int, skill: int) -> int:
    """CANDIDATE C — the Skill carries the step; the STAT nudges by at most ±1.

    This is the Fate-shaped option: competence lives in the trained Skill, while the
    underlying Attribute still matters mechanically without doubling the numbers.
    """
    skill_step = rating_step(skill, label="Skill")
    stat_step = rating_step(stat, label="STAT")
    nudge = max(-1, min(1, stat_step))
    return clamp_step(skill_step + nudge)


#: The three candidates #200 asks to compare, by name.
CANDIDATES: dict[str, Callable[[int, int], int]] = {
    "A_additive": combine_additive,
    "B_averaged": combine_averaged,
    "C_skill_primary": combine_skill_primary,
}


# --------------------------------------------------------------------------------------
# Dice
# --------------------------------------------------------------------------------------


def roll_fudge_die(rng: DiceSource) -> int:
    """One Fudge die: −1, 0 or +1, uniformly."""
    return rng.randint(0, FDF_SIDES - 1) - 1


def roll_4df(rng: DiceSource | None = None) -> int:
    """Four Fudge dice summed. Mean 0, range −4..+4, triangular."""
    source = rng if rng is not None else random
    return sum(roll_fudge_die(source) for _ in range(FDF_COUNT))


@dataclass(frozen=True, slots=True)
class LadderResult:
    candidate: str
    step: int
    dice: int
    situational: int
    total: int
    difficulty: int
    margin: int
    outcome: str


#: Fate-flavoured success bands, keyed off the margin. Prototype naming.
SUCCESS_WITH_STYLE_MARGIN = 3


def resolve_ladder(
    *,
    candidate: str,
    stat: int,
    skill: int,
    difficulty: int = 0,
    situational: int = 0,
    rng: DiceSource | None = None,
    dice: int | None = None,
    cap_situational: bool = True,
) -> LadderResult:
    """Resolve a ladder check: combine(STAT, Skill) + 4dF + situational vs difficulty.

    Situational modifiers are capped at ±:data:`MAX_SITUATIONAL_STEPS` by default,
    because unbounded stacking is the failure mode #200 asks us to bound. Passing
    ``cap_situational=False`` is allowed so a test can measure *why* the cap exists.
    """
    if candidate not in CANDIDATES:
        raise ValueError(f"Unknown candidate {candidate!r}; expected one of {sorted(CANDIDATES)}.")
    combined = CANDIDATES[candidate](stat, skill)
    applied = int(situational)
    if cap_situational:
        applied = max(-MAX_SITUATIONAL_STEPS, min(MAX_SITUATIONAL_STEPS, applied))
    rolled = roll_4df(rng) if dice is None else int(dice)
    if not -FDF_COUNT <= rolled <= FDF_COUNT:
        raise ValueError(f"A 4dF roll must be in {-FDF_COUNT}..{FDF_COUNT}.")
    target = clamp_step(difficulty)
    total = combined + rolled + applied
    margin = total - target
    if margin < 0:
        outcome = "failure"
    elif margin < SUCCESS_WITH_STYLE_MARGIN:
        outcome = "success"
    else:
        outcome = "success_with_style"
    return LadderResult(
        candidate=candidate,
        step=combined,
        dice=rolled,
        situational=applied,
        total=total,
        difficulty=target,
        margin=margin,
        outcome=outcome,
    )


def opposed_ladder(
    *,
    candidate: str,
    left: tuple[int, int],
    right: tuple[int, int],
    rng: DiceSource | None = None,
    left_dice: int | None = None,
    right_dice: int | None = None,
) -> tuple[LadderResult, LadderResult, str | None]:
    """Both sides roll. Higher total wins; equal totals stay an unresolved tie."""
    left_result = resolve_ladder(
        candidate=candidate, stat=left[0], skill=left[1], difficulty=0, rng=rng, dice=left_dice
    )
    right_result = resolve_ladder(
        candidate=candidate, stat=right[0], skill=right[1], difficulty=0, rng=rng, dice=right_dice
    )
    if left_result.total > right_result.total:
        winner: str | None = "left"
    elif right_result.total > left_result.total:
        winner = "right"
    else:
        winner = None
    return left_result, right_result, winner


# --------------------------------------------------------------------------------------
# The migration benchmark: the canonical 1d10 path, delegated not duplicated.
# --------------------------------------------------------------------------------------


def resolve_legacy(
    *, stat: int, skill: int, target: int, rng: DiceSource | None = None, die: int | None = None
) -> CheckResult:
    """The canonical ``STAT + Skill + 1d10`` check, via :func:`src.rules.core.resolve_check`.

    Deliberately a delegation: if this prototype ever disagreed with the shipped engine
    about the benchmark, the comparison below would be worthless.
    """
    return resolve_check(stat=stat, skill=skill, target=target, rng=rng, die=die)


def legacy_dv_to_step(dv: int) -> int:
    """Map a canonical Difficulty Value onto a ladder step, for comparison only.

    A prototype calibration (see :data:`LEGACY_DV_PIVOT`), not authored canon. Values
    above Heroic clamp to the top step, which is a real limitation of a seven-step
    ladder and is reported as such rather than hidden.
    """
    return clamp_step(round((int(dv) - LEGACY_DV_PIVOT) / LEGACY_DV_WIDTH))


def legacy_dv_ladder() -> dict[str, int]:
    """The authored DVs, each with the ladder step this prototype maps it onto."""
    return {f"{dv} {DIFFICULTIES[dv]}": legacy_dv_to_step(dv) for dv in DIFFICULTY_LADDER}


# --------------------------------------------------------------------------------------
# Measurement helpers. Everything below returns real counts, never assertions.
# --------------------------------------------------------------------------------------


def p_success_ladder(
    *, candidate: str, stat: int, skill: int, difficulty: int, trials: int, seed: int
) -> float:
    rng = random.Random(seed)
    hits = sum(
        1
        for _ in range(trials)
        if resolve_ladder(
            candidate=candidate, stat=stat, skill=skill, difficulty=difficulty, rng=rng
        ).outcome
        != "failure"
    )
    return hits / trials


def p_success_legacy(*, stat: int, skill: int, target: int, trials: int, seed: int) -> float:
    rng = random.Random(seed)
    hits = sum(
        1 for _ in range(trials) if resolve_legacy(stat=stat, skill=skill, target=target, rng=rng).success
    )
    return hits / trials


def edge_curve(
    *, candidate: str, levels: Sequence[tuple[int, int]], difficulty: int, trials: int, seed: int
) -> list[tuple[int, int, float]]:
    """P(success) per (STAT, Skill) profile, at a fixed difficulty."""
    return [
        (stat, skill, p_success_ladder(
            candidate=candidate, stat=stat, skill=skill, difficulty=difficulty,
            trials=trials, seed=seed + i,
        ))
        for i, (stat, skill) in enumerate(levels)
    ]


def disparity(*, candidate: str, trials: int, seed: int) -> dict[str, float]:
    """The high-end spread #200 asks about: top-tier vs competent, at the same difficulty.

    A wide spread means a specialist trivialises what a competent character struggles
    with; a narrow one means competence stops mattering at the top. Both are design
    consequences, and this measures which one each candidate buys.
    """
    top = p_success_ladder(candidate=candidate, stat=STAT_MAX, skill=SKILL_LEVEL_MAX,
                           difficulty=0, trials=trials, seed=seed)
    competent = p_success_ladder(candidate=candidate, stat=5, skill=5,
                                 difficulty=0, trials=trials, seed=seed + 1)
    weak = p_success_ladder(candidate=candidate, stat=2, skill=1,
                            difficulty=0, trials=trials, seed=seed + 2)
    return {
        "top_10_10": top,
        "competent_5_5": competent,
        "weak_2_1": weak,
        "top_minus_competent": top - competent,
        "competent_minus_weak": competent - weak,
    }


def hits_to_takedown(
    *, candidate: str, stat: int, skill: int, defence: int, stress: int, trials: int, seed: int
) -> float:
    """Expected exchanges to fill a stress track, as a lethality proxy.

    A deliberately simple model: each success removes one stress box, success-with-style
    removes two. It compares *pace*, not a final combat system -- #200 explicitly leaves
    the light wound ladder in place until it is reconciled.
    """
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        remaining = stress
        exchanges = 0
        while remaining > 0 and exchanges < 200:
            exchanges += 1
            result = resolve_ladder(
                candidate=candidate, stat=stat, skill=skill,
                difficulty=legacy_dv_to_step(defence), rng=rng,
            )
            if result.outcome == "success":
                remaining -= 1
            elif result.outcome == "success_with_style":
                remaining -= 2
        total += exchanges
    return total / trials


def expected_4df_distribution() -> Mapping[int, float]:
    """The exact 4dF distribution, for validating the sampled one."""
    counts: dict[int, int] = {v: 0 for v in range(-FDF_COUNT, FDF_COUNT + 1)}
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            for c in (-1, 0, 1):
                for d in (-1, 0, 1):
                    counts[a + b + c + d] += 1
    total = 3 ** FDF_COUNT
    return {k: v / total for k, v in sorted(counts.items())}


__all__ = [
    "CANDIDATES",
    "FDF_COUNT",
    "FDF_SIDES",
    "IS_CANONICAL",
    "LADDER_LABELS",
    "LADDER_MAX",
    "LADDER_MIN",
    "LEGACY_DV_PIVOT",
    "LEGACY_DV_WIDTH",
    "MAX_SITUATIONAL_STEPS",
    "SUCCESS_WITH_STYLE_MARGIN",
    "LadderResult",
    "clamp_step",
    "combine_additive",
    "combine_averaged",
    "combine_skill_primary",
    "disparity",
    "edge_curve",
    "expected_4df_distribution",
    "hits_to_takedown",
    "ladder_label",
    "legacy_dv_ladder",
    "legacy_dv_to_step",
    "opposed_ladder",
    "p_success_ladder",
    "p_success_legacy",
    "rating_step",
    "resolve_ladder",
    "resolve_legacy",
    "roll_4df",
    "roll_fudge_die",
]
