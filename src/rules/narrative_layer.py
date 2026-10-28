"""Narrative layer — the executable half of issue #229, re-anchored on 2d6 by #689.

`rulebook/19_NARRATIVE_LAYER.md` states the layer; this module enforces its two safety
rules in code, because both are the kind of promise prose cannot keep:

* **One ladder step, once per roll.** `invoke_step()` has no parameter that could increase
  it, and `can_invoke()` refuses a second invocation in the same roll. Without the cap the
  prototype measured four stacked aspects reaching **100%** -- auto-success.
* **An aspect never produces a rating.** There is no code path from an `Aspect` to a STAT
  or Skill value, and none is exposed.

Since #689 the bands and the step are read on the Without Number die (`2d6 + attribute
modifier + skill rank`), not on the retired d10 ladder. The boundary arithmetic is
measured, not inherited: `band_distribution()` enumerates all 36 outcomes.

**Status: PROVISIONAL, not canonical.** `IS_CANONICAL = False`; nothing in the shipped
`src/rules/core.py` path imports it.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

#: PROVISIONAL. The author owns calibration.
IS_CANONICAL = False

#: PROVISIONAL: the bounded narrative pool.
POOL_MIN = 0
POOL_MAX = 3

#: The cap that prevents the measured auto-success exploit. One invocation per roll.
MAX_INVOCATIONS_PER_ROLL = 1

#: The bound, expressed as a ladder STEP rather than a number, so it survives the pending
#: scale migration unchanged. Never incremented by spending more points.
INVOKE_STEPS = 1


class NarrativeError(ValueError):
    """A narrative-layer invariant was violated."""


class EffectClass(str, Enum):
    """What an aspect is allowed to do. Note what is absent: no RATING member."""

    PERMISSION = "permission"
    MODIFIER = "modifier"
    CONSEQUENCE = "consequence"


#: Every GM move is a description of what the fiction does next -- never a modifier.
GM_MOVES: dict[str, str] = {
    "reward": "they get it cleanly",
    "reward_and_aspect": "they get it cleanly, and an aspect goes in their favour",
    "cost": "they get it, but something is spent, owed or noticed",
    "escalate": "the situation worsens, an aspect turns against them, or a new threat appears",
}

#: Play styles that must all resolve through ONE core.
PLAY_STYLES: tuple[str, ...] = ("narrativist", "simulationist", "gamist")


@dataclass(frozen=True, slots=True)
class Aspect:
    """A bounded, cancellable tag. Every part is required; a missing part is invalid."""

    statement: str
    scope: str
    duration: str
    effect_class: EffectClass
    cancellation: str

    def __post_init__(self) -> None:
        if not isinstance(self.effect_class, EffectClass):
            raise NarrativeError(f"effect_class must be an EffectClass, got {self.effect_class!r}")
        for name in ("statement", "scope", "duration", "cancellation"):
            value = getattr(self, name)
            if not str(value).strip():
                raise NarrativeError(f"an aspect requires a non-empty {name}")


def validate_aspect(aspect: Aspect) -> Aspect:
    """Re-validation entry point, so a caller holding a mutated object can re-check it."""
    return Aspect(
        statement=aspect.statement,
        scope=aspect.scope,
        duration=aspect.duration,
        effect_class=aspect.effect_class,
        cancellation=aspect.cancellation,
    )


def effect_class_may_produce_a_rating(effect_class: EffectClass) -> bool:
    """Never, for any class. Pinned so the capability cannot be added silently."""
    if not isinstance(effect_class, EffectClass):
        raise NarrativeError(f"unknown effect class: {effect_class!r}")
    return False


# --------------------------------------------------------------------------- #
# The bound: one step, once per roll
# --------------------------------------------------------------------------- #

def can_invoke(invocations_this_roll: int) -> bool:
    """The load-bearing cap. Measured: without it, stacked aspects reach 100%."""
    if invocations_this_roll < 0:
        raise NarrativeError("invocation count cannot be negative")
    return invocations_this_roll < MAX_INVOCATIONS_PER_ROLL


def invoke_step(*_ignored: object, **_kw: object) -> int:
    """The modifier an invocation grants: one ladder step, and nothing can change that.

    Takes and ignores arguments so a caller cannot pass a "bigger" invocation; a future
    edit that tried to honour such a parameter would have to change this signature, which
    the guard pins.
    """
    return INVOKE_STEPS


def assert_can_invoke(invocations_this_roll: int) -> None:
    if not can_invoke(invocations_this_roll):
        raise NarrativeError(
            f"only {MAX_INVOCATIONS_PER_ROLL} aspect invocation is allowed per roll"
        )


# --------------------------------------------------------------------------- #
# The pool
# --------------------------------------------------------------------------- #

@dataclass
class ResourcePool:
    """A per-character narrative pool. Spending more never buys a bigger modifier."""

    current: int = 0
    owner: str = ""

    def __post_init__(self) -> None:
        if self.current < POOL_MIN or self.current > POOL_MAX:
            raise NarrativeError(
                f"pool must start within {POOL_MIN}..{POOL_MAX}, got {self.current}"
            )

    def spend(self, amount: int = 1) -> None:
        if amount <= 0:
            raise NarrativeError("cannot spend a non-positive amount")
        if amount > self.current:
            raise NarrativeError("not enough points")
        self.current -= amount

    def earn(self, amount: int = 1) -> None:
        """Gained by accepting a compel -- the only mid-scene source."""
        if amount <= 0:
            raise NarrativeError("cannot earn a non-positive amount")
        self.current = min(POOL_MAX, self.current + amount)

    def invoke(self, invocations_this_roll: int) -> int:
        """Spend a point and take one step. The step does not depend on the spend."""
        assert_can_invoke(invocations_this_roll)
        self.spend(1)
        return invoke_step()


# --------------------------------------------------------------------------- #
# Outcome bands: the 2d6 reading (#689)
# --------------------------------------------------------------------------- #

#: The four outcomes, ascending. A roll's band is read off its margin, never re-rolled.
OUTCOME_BANDS: tuple[str, ...] = ("miss", "cost", "clean", "style")

#: Lowest margin that earns each band; everything below zero is a miss.
#:
#: The boundaries are PROVISIONAL, and they are *measured*: at the standard difficulty
#: (DV 8, modifier 0) the 36 outcomes split 21 miss / 9 cost / 6 clean / 0 style, and one
#: step moves mass from miss into cost. `band_distribution()` recomputes that.
BAND_MIN_MARGIN: dict[str, int] = {"cost": 0, "clean": 2, "style": 5}


def band_for(margin: int) -> str:
    """Read a margin into its band. Deterministic, and never a second roll."""
    if not isinstance(margin, int) or isinstance(margin, bool):
        raise NarrativeError(f"margin must be an integer, got {margin!r}")
    for band in reversed(OUTCOME_BANDS):
        if band != "miss" and margin >= BAND_MIN_MARGIN[band]:
            return band
    return "miss"


def outcome_band(total: int, difficulty: int) -> str:
    """The single entry point a resolver needs: a core total and its difficulty."""
    return band_for(total - difficulty)


def band_distribution(*, modifier: int = 0, difficulty: int = 8) -> dict[str, Fraction]:
    """Exact share of the 36 two-die outcomes in each band.

    Exists so the boundaries can be re-derived instead of inherited. It is calibration,
    not resolution: nothing at the table calls it.
    """
    counts = dict.fromkeys(OUTCOME_BANDS, 0)
    for first in range(1, 7):
        for second in range(1, 7):
            counts[band_for(first + second + modifier - difficulty)] += 1
    return {band: Fraction(counts[band], 36) for band in OUTCOME_BANDS}


#: Band -> GM move. The move describes the fiction; it never alters the number rolled.
BAND_TO_MOVE: dict[str, str] = {
    "miss": "escalate",
    "cost": "cost",
    "clean": "reward",
    "style": "reward_and_aspect",
}


def gm_move(*, band: str) -> str:
    """Choose the GM move from the band the core already produced. Adds no randomness."""
    try:
        return BAND_TO_MOVE[band]
    except KeyError:
        raise NarrativeError(
            f"unknown band: {band!r} (expected one of {', '.join(OUTCOME_BANDS)})"
        ) from None


@dataclass(slots=True)
class LLMProposal:
    """What an LLM may hand back to the engine: narration plus a suggestion."""

    narration: str
    proposed_aspect: Aspect | None = None
    proposed_modifier: int | None = None


@dataclass(slots=True)
class Validation:
    accepted: bool
    reason: str = ""
    aspect: Aspect | None = None


def validate_proposal(proposal: LLMProposal) -> Validation:
    """The engine's gate. Rejects anything that would take the numeric loop from the core.

    An LLM may narrate and may propose a well-formed aspect. It may not propose a
    modifier of its own choosing, and a malformed aspect is rejected rather than narrated
    into existence.
    """
    if proposal.proposed_modifier is not None:
        return Validation(False, "the LLM may not propose a numeric modifier")
    if proposal.proposed_aspect is None:
        return Validation(True, "narration only")
    try:
        validated = validate_aspect(proposal.proposed_aspect)
    except NarrativeError as exc:
        return Validation(False, f"malformed aspect: {exc}")
    return Validation(True, "aspect accepted", aspect=validated)


# --------------------------------------------------------------------------- #
# GNS parity
# --------------------------------------------------------------------------- #

def core_for_style(style: str) -> str:
    """Every play style resolves on the SAME core. Parity is structural, not stylistic."""
    if style not in PLAY_STYLES:
        raise NarrativeError(f"unknown play style: {style!r} (expected one of {PLAY_STYLES})")
    return "core_check"


def styles_share_one_core() -> bool:
    return len({core_for_style(s) for s in PLAY_STYLES}) == 1
