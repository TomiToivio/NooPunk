"""Mental load as conditions, not a track (#698; decisions D46–D48).

Three rules shape this module, and they are enforced in the types rather than left to reviewers:

**D46 — no second harm economy.** There is no pool, no bar and no number to deplete. A condition
constrains *choices*: it says what the character cannot attempt and what lifts it. There is nothing
here for Trauma, Frail or System Strain to compete with, because there is nothing numeric at all.

**D47 — four layers.** Exposure is recorded in four distinct places, and conflating them is what makes
"sanity" rules mushy:

    observable_event  →  acute_response  →  persistent_condition  →  worldview_state

What happened, what it did at the time, what it left behind, and what the character now believes. A
condition is layer 3 only; a belief is layer 4 and is *never* written by layer 2.

**D48 — a world view changes by decision, never by a failed save.** `resolve_shock()` cannot be called
without naming a `Choice`. No function in this module takes a die, a seed or a random number generator,
so there is no code path that could let a roll overwrite a conviction. `tests/test_issue698_mental_load.py`
asserts that by inspecting every public signature.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

__all__ = [
    "Choice",
    "Condition",
    "ConditionError",
    "ExposureLayer",
    "ParadigmShock",
    "ShockRecord",
    "WorldviewState",
    "apply_choice",
    "offer_choices",
    "resolve_shock",
    "worldview_transition",
]

#: Any name that would let a caller smuggle randomness into a world-view change.
_FORBIDDEN_PARAMETERS = ("rng", "random", "die", "dice", "roll", "seed")


class ConditionError(ValueError):
    """A condition or shock was constructed in a way the rules do not allow."""


class ExposureLayer(str, Enum):
    """D47's four layers. A world view is layer four and is not a condition."""

    OBSERVABLE_EVENT = "observable_event"
    ACUTE_RESPONSE = "acute_response"
    PERSISTENT_CONDITION = "persistent_condition"
    WORLDVIEW_STATE = "worldview_state"


class WorldviewState(str, Enum):
    """D48's reachable states for one belief.

    ``received`` is the default: the belief was given, not examined. A shock can move it to
    ``cracked``; only a *choice* moves it to ``reframed``, ``integrated`` or ``fractured``.
    """

    RECEIVED = "received"
    CRACKED = "cracked"
    REFRAMED = "reframed"
    INTEGRATED = "integrated"
    FRACTURED = "fractured"


#: States reachable only through an explicit choice (never through an event alone).
CHOICE_ONLY_STATES: frozenset[WorldviewState] = frozenset(
    {WorldviewState.REFRAMED, WorldviewState.INTEGRATED, WorldviewState.FRACTURED}
)


@dataclass(frozen=True, slots=True)
class Condition:
    """One persistent condition (layer 3).

    ``severity`` and ``clears_when`` are **author-supplied**. This module deliberately does not
    enumerate severities or invent recovery rules: the decision record leaves both open, and a
    guessed severity would be indistinguishable from a ruled one downstream.
    """

    id: str
    layer: ExposureLayer
    statement: str
    severity: str
    constrains: tuple[str, ...]
    clears_when: str

    def __post_init__(self) -> None:
        if self.layer is ExposureLayer.WORLDVIEW_STATE:
            raise ConditionError(
                "a world view is not a condition (D47); use a ParadigmShock for layer four"
            )
        if not self.statement.strip():
            raise ConditionError("a condition needs a statement")
        if not self.severity.strip():
            raise ConditionError(
                "severity is author-supplied; pass a named severity rather than inventing a number"
            )
        if not self.clears_when.strip():
            raise ConditionError("a condition must say what clears it")
        if not self.constrains:
            raise ConditionError("a condition must constrain at least one choice")


@dataclass(frozen=True, slots=True)
class Choice:
    """One branch of a shock, with the cost that branch carries (D48).

    A shock offers *two different costs*, never a right and a wrong answer.
    """

    id: str
    label: str
    cost: str
    resulting_state: WorldviewState

    def __post_init__(self) -> None:
        if self.resulting_state not in CHOICE_ONLY_STATES:
            raise ConditionError(
                f"{self.resulting_state.value!r} is not a choice outcome; a choice produces "
                "reframed, integrated or fractured"
            )
        if not self.cost.strip():
            raise ConditionError("every branch of a shock must carry a cost")


@dataclass(frozen=True, slots=True)
class ParadigmShock:
    """A held belief meeting evidence that contradicts it."""

    belief: str
    evidence: str
    choices: tuple[Choice, Choice]

    def __post_init__(self) -> None:
        if len(self.choices) != 2:
            raise ConditionError("a paradigm shock offers exactly two branches")
        if self.choices[0].id == self.choices[1].id:
            raise ConditionError("the two branches must be distinct")


@dataclass(slots=True)
class ShockRecord:
    """The journal entry for one shock: what happened and what the player decided."""

    belief: str
    evidence: str
    state_before: WorldviewState
    state_after: WorldviewState
    chosen: str
    cost: str
    events: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "belief": self.belief,
            "evidence": self.evidence,
            "state_before": self.state_before.value,
            "state_after": self.state_after.value,
            "chosen": self.chosen,
            "cost": self.cost,
            "events": list(self.events),
        }


def offer_choices(shock: ParadigmShock) -> tuple[Choice, Choice]:
    """The two branches, in a stable order. Presenting them is what a shock *does*."""
    return shock.choices


def worldview_transition(before: WorldviewState, chosen: Choice) -> WorldviewState:
    """The state a choice produces. Total, deterministic, and independent of any die."""
    if chosen.resulting_state in CHOICE_ONLY_STATES:
        return chosen.resulting_state
    raise ConditionError(f"choice {chosen.id!r} does not name a reachable outcome")


def resolve_shock(shock: ParadigmShock, *, choice_id: str,
                  state: WorldviewState = WorldviewState.RECEIVED) -> ShockRecord:
    """Apply an **explicit** choice to a belief and return the journal entry.

    There is deliberately no overload that resolves a shock without a ``choice_id``: that absence is
    D48 in code. A caller cannot ask this function to decide for the player.
    """
    matching = [c for c in shock.choices if c.id == choice_id]
    if not matching:
        raise ConditionError(
            f"unknown choice {choice_id!r}; a shock is resolved by naming one of its branches"
        )
    chosen = matching[0]
    after = worldview_transition(state, chosen)
    return ShockRecord(
        belief=shock.belief,
        evidence=shock.evidence,
        state_before=state,
        state_after=after,
        chosen=chosen.id,
        cost=chosen.cost,
        events=[
            f"layer 1 observable_event: {shock.evidence}",
            f"layer 4 worldview_state: {state.value} -> {after.value} (choice {chosen.id})",
        ],
    )


def apply_choice(record: ShockRecord, chosen: Choice) -> ShockRecord:
    """Re-resolve a journal entry with a different branch (used by the #699 case)."""
    after = worldview_transition(record.state_before, chosen)
    return ShockRecord(
        belief=record.belief, evidence=record.evidence, state_before=record.state_before,
        state_after=after, chosen=chosen.id, cost=chosen.cost,
        events=[*record.events, f"re-resolved: {chosen.id}"],
    )


def _assert_no_randomness() -> None:
    """Fail at import if any public entry point could accept randomness (D48)."""
    for name, function in sorted(globals().items()):
        if not inspect.isfunction(function) or name.startswith("_"):
            continue
        parameters = inspect.signature(function).parameters
        smuggled = [p for p in parameters if p.lower() in _FORBIDDEN_PARAMETERS]
        if smuggled:
            raise ConditionError(
                f"{name}() accepts {smuggled}; no world-view change may depend on a roll (D48)"
            )


_assert_no_randomness()
