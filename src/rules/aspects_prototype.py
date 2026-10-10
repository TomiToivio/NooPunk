"""Prototype: the aspects / resource / consequence layer for issue #200. **NOT CANONICAL.**

#200 asks for "Fate-like Aspects, player choices, relationships, compels, stress/consequences,
limited narrative resources and scene-level stakes" -- and constrains them hard:

    "Tags/Aspects affect fictional permissions, bounded modifiers or meaningful consequences;
     avoid uncapped numerical exploits."

and

    "rolls, skill/gear calculations, state transitions, injury, resources, AP, investigations and
     objective permissions must be deterministic and auditable."

That pair is the whole design problem, and it is why this module measures rather than declares:

* On 4dF, **a +2 is not a modifier, it is most of the roll.** 4dF ranges -4..+4 but sits within
  +/-2 about 94% of the time, so +2 all but decides a contest. "Bounded" therefore has to mean
  something narrower than Fate's +2 default, and :func:`value_of_bonus` puts a number on it.
* A *numeric* stress track is in tension with NooPunk's existing harm vocabulary, which
  `RULEBOOK.md` section 51 calls "a fiction-first consequence vocabulary, not a hidden damage
  engine". :func:`attrition` measures both so the difference is visible instead of assumed.

Like the kernel prototype, nothing here is wired into canon:

* ``data/rules/core.json`` and ``src/rules/core.py`` are untouched. The six STATs and the
  separate Skill taxonomy stay exactly where they are.
* Every numeric value is **DRAFT pending calibration**, per #200.
* :data:`IS_CANONICAL` is False and :data:`CONSEQUENCE_STATES` is asserted against the rulebook by
  the tests, so this file cannot silently drift from the authored vocabulary.

The prototype's answers, so the reasoning is auditable:

* Invoking an aspect grants :data:`ASPECT_INVOKE_BONUS` of **one step**, and at most
  :data:`MAX_INVOCATIONS_PER_ROLL` invocation per roll. Two would be an uncapped exploit in
  miniature; one is a nudge that respects the 4dF spread.
* An aspect's *permission* use costs nothing and rolls nothing -- it establishes what is
  fictionally possible, which is what #200 asks tags to do first.
* Consequences use the authored four states and are recorded by the fiction, not by arithmetic.
  A numeric track is measured only as the counterfactual it is.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from fractions import Fraction

from .kernel_prototype import LADDER_MAX, LADDER_MIN, fdf_outcome_counts

#: Prototype marker. Nothing here is canon and nothing here may be imported by a runtime yet.
IS_CANONICAL = False

# ---------------------------------------------------------------------------------------
# DRAFT parameters. #200 requires every new number to be flagged pending calibration.
# ---------------------------------------------------------------------------------------

#: DRAFT. Steps granted by invoking one aspect. Deliberately 1, not Fate's usual 2 -- see
#: :func:`value_of_bonus` for the measurement that forces the choice.
ASPECT_INVOKE_BONUS = 1

#: DRAFT. Invocations allowed on a single roll. The bound #200's "avoid uncapped numerical
#: exploits" requires: without it, aspects stack past the whole 4dF range.
MAX_INVOCATIONS_PER_ROLL = 1

#: DRAFT. Narrative resource (name deliberately generic; #200 does not name it yet).
NARRATIVE_POOL_START = 3

#: DRAFT. Tokens granted for accepting a compel, and spent to invoke.
TOKENS_PER_COMPEL = 1
TOKENS_PER_INVOCATION = 1

#: DRAFT. Steps a consequence may impose, and how many consequences a character can carry.
CONSEQUENCE_PENALTY_STEPS = 1
MAX_CONSEQUENCES = 3

#: The authored harm vocabulary, `RULEBOOK.md` section 51. The tests assert this against the
#: rulebook text, so it cannot drift. Order is the ladder: least to most severe.
CONSEQUENCE_STATES = ("Scratched", "Wounded", "Critical", "Down")


# ---------------------------------------------------------------------------------------
# Aspects
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Aspect:
    """A tag with a fictional meaning and at most a bounded mechanical effect.

    #200 puts permission first, so :meth:`permits` is free and deterministic. The modifier path
    is the bounded one, and :meth:`invoke` refuses to exceed the cap rather than trusting callers.
    """

    name: str
    #: What the tag fictionally establishes. Descriptive only; the GM reads it.
    permits: str = ""
    #: A compel is the narrativist price: accept a complication, gain a token.
    compellable: bool = True

    def permits_action(self, action: str) -> bool:
        """Aspect-as-permission: deterministic, costs nothing, grants no number."""
        return bool(self.permits) and action.strip().lower() in self.permits.lower()


@dataclass
class NarrativePool:
    """The DRAFT narrative resource. Tokens are the only thing aspects cost."""

    tokens: int = NARRATIVE_POOL_START
    spent: int = 0
    gained: int = 0

    def invoke(self, count: int = 1) -> int:
        """Pay for `count` invocations. Returns the granted steps, never exceeding the cap."""
        wanted = min(count, MAX_INVOCATIONS_PER_ROLL)
        affordable = min(wanted, self.tokens // TOKENS_PER_INVOCATION)
        if affordable <= 0:
            return 0
        self.tokens -= affordable * TOKENS_PER_INVOCATION
        self.spent += affordable * TOKENS_PER_INVOCATION
        return affordable * ASPECT_INVOKE_BONUS

    def compel(self, count: int = 1) -> None:
        """Accept a complication, gain tokens."""
        self.tokens += count * TOKENS_PER_COMPEL
        self.gained += count * TOKENS_PER_COMPEL


# ---------------------------------------------------------------------------------------
# Measuring the roll, exactly
# ---------------------------------------------------------------------------------------

_COUNTS = fdf_outcome_counts()
_TOTAL = sum(_COUNTS.values())


def success_probability(bonus: int = 0, difficulty: int = 0) -> Fraction:
    """Exact P(4dF + bonus + base >= difficulty), the base being the ladder step 0.

    Exact rather than sampled, following the sibling resolution lab (#207): a design number
    should not be blamable on a seed.
    """
    needed = difficulty - bonus
    hits = sum(count for roll, count in _COUNTS.items() if roll >= needed)
    return Fraction(hits, _TOTAL)


def value_of_bonus(bonus: int, difficulty: int = 0) -> Fraction:
    """How much a +`bonus` invocation is worth, in percentage points of success.

    This is the measurement that decides :data:`ASPECT_INVOKE_BONUS`. If a single +2 moves the
    odds by more than the entire typical spread of the roll, then #200's "bounded modifiers"
    cannot mean Fate's default +2.
    """
    return success_probability(bonus, difficulty) - success_probability(0, difficulty)


def spread_of_the_roll() -> Fraction:
    """The share of 4dF outcomes that fall inside +/-1 -- the roll's own typical spread."""
    inside = sum(count for roll, count in _COUNTS.items() if abs(roll) <= 1)
    return Fraction(inside, _TOTAL)


def stacked_success_probability(*, invocations: int, difficulty: int = 0, cap: bool = True) -> Fraction:
    """P(success) with `invocations` aspects stacked, optionally respecting the cap.

    The uncapped branch exists only to SHOW the exploit #200 forbids; nothing may call it in a
    resolver.
    """
    applied = min(invocations, MAX_INVOCATIONS_PER_ROLL) if cap else invocations
    return success_probability(applied * ASPECT_INVOKE_BONUS, difficulty)


def tokens_per_scene(invocations_per_scene: int) -> Fraction:
    """Scenes a starting pool sustains at a given invocation rate."""
    cost = invocations_per_scene * TOKENS_PER_INVOCATION
    return Fraction(NARRATIVE_POOL_START, cost) if cost else Fraction(0)


def compel_break_even(invocations_per_scene: int) -> Fraction:
    """Compels needed per scene to fund a given rate of invocation."""
    return Fraction(invocations_per_scene * TOKENS_PER_INVOCATION, TOKENS_PER_COMPEL)


# ---------------------------------------------------------------------------------------
# Consequences: the authored ladder, and the numeric counterfactual
# ---------------------------------------------------------------------------------------


@dataclass
class HarmState:
    """A character's harm, recorded in the AUTHORED vocabulary rather than arithmetic.

    `RULEBOOK.md` section 51 is explicit that a successful attack does not automatically advance
    this and repeated harm does not automatically step it along -- the GM records what the
    fiction established. So this type records states; it does not compute them.
    """

    states: list[str] = field(default_factory=list)
    consequences: int = 0

    def record(self, state: str) -> None:
        if state not in CONSEQUENCE_STATES:
            raise ValueError(f"{state!r} is not an authored harm state: {CONSEQUENCE_STATES}")
        self.states.append(state)

    @property
    def worst(self) -> str | None:
        if not self.states:
            return None
        return max(self.states, key=CONSEQUENCE_STATES.index)

    @property
    def taken_out(self) -> bool:
        return self.worst in ("Critical", "Down")

    def penalty_steps(self) -> int:
        """Bounded: consequences never accumulate past :data:`MAX_CONSEQUENCES`."""
        return min(self.consequences, MAX_CONSEQUENCES) * CONSEQUENCE_PENALTY_STEPS


def attrition(*, boxes: int, attacker_bonus: int = 0, defender_bonus: int = 0) -> Fraction:
    """Expected exchanges to fill a NUMERIC stress track of `boxes`.

    Presented only as the counterfactual to the authored ladder. A numeric track answers "how
    many hits", which is precisely the question section 51 declines to make automatic -- so this
    number is a design observation, never a rule.
    """
    p = success_probability(attacker_bonus - defender_bonus)
    return Fraction(boxes, 1) / p if p else Fraction(0)


def ladder_progression_is_automatic() -> bool:
    """Whether harm advances the ladder by arithmetic. Section 51 says it must not."""
    return False


# ---------------------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------------------


def bonus_table(difficulty: int = 0) -> Mapping[int, tuple[Fraction, Fraction]]:
    """bonus -> (P(success), percentage-point gain) at a given difficulty."""
    return {b: (success_probability(b, difficulty), value_of_bonus(b, difficulty))
            for b in range(LADDER_MAX - LADDER_MIN)}


def count_states(states: Iterable[str]) -> Mapping[str, int]:
    return dict(Counter(states))


__all__ = [
    "ASPECT_INVOKE_BONUS",
    "CONSEQUENCE_PENALTY_STEPS",
    "CONSEQUENCE_STATES",
    "IS_CANONICAL",
    "LADDER_MAX",
    "LADDER_MIN",
    "MAX_CONSEQUENCES",
    "MAX_INVOCATIONS_PER_ROLL",
    "NARRATIVE_POOL_START",
    "TOKENS_PER_COMPEL",
    "TOKENS_PER_INVOCATION",
    "Aspect",
    "HarmState",
    "NarrativePool",
    "attrition",
    "bonus_table",
    "compel_break_even",
    "count_states",
    "ladder_progression_is_automatic",
    "spread_of_the_roll",
    "stacked_success_probability",
    "success_probability",
    "tokens_per_scene",
    "value_of_bonus",
]
