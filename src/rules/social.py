"""Social procedures — the executable half of issue #220.

`rulebook/4_SOCIAL.md` states the procedure; this module is the arithmetic, so the
properties the chapter asserts can be **proved rather than read**.

**Status: PROVISIONAL, not canonical.** `IS_CANONICAL = False`.

The properties worth executing:

* **One arithmetic across realms.** The margin->band function is *imported* from the
  physical module rather than re-implemented. Physical and social differ in what a band
  *means*, never in how it is computed -- so the two realms cannot drift apart.
* **A social result cannot overwrite a Motivation.** There is deliberately no function
  here that mutates a character's US/FRONTIER or Motivation edges. The module can compute
  a consequence; it cannot rewrite a person, because the capability does not exist.
* **Relationship status is derived, never stored.** Statuses are computed from Affect
  edges, so a status field and the graph can never disagree.
* **Bounded group modifiers.** Support is capped at the same +2 the resolution pass
  recorded, so a crowd cannot become an unbounded bonus.
"""
from __future__ import annotations

from dataclasses import dataclass

#: Reused deliberately: ONE margin->band function for every realm.
from .physical_combat import band_for_margin

#: PROVISIONAL. The author owns calibration.
IS_CANONICAL = False

# --------------------------------------------------------------------------- #
# Consequence vocabulary: the same bands, different meaning
# --------------------------------------------------------------------------- #

#: Social meaning per effect band. Order: least to most consequential.
SOCIAL_CONSEQUENCE: dict[str, str] = {
    "glancing": "Heard",
    "solid": "Leaning",
    "severe": "Convinced",
    "brutal": "Committed",
}

#: Returned when the actor does not beat the resistance at all.
UNMOVED = "Unmoved"

#: The canonical consequence of coercion: a bounded negative aspect.
GRIEVANCE_ASPECT = "Grievance"

#: Methods that move behaviour under threat rather than belief.
COERCIVE_METHODS: frozenset[str] = frozenset({"Provoke", "coerce", "coercion"})

#: The one-step ceiling a witnessed public exchange may move a Reputation edge.
REPUTATION_STEP = 1

#: The bounded group-support cap, matching the recorded +-2 situational cap (#217).
MAX_GROUP_SUPPORT = 2


class SocialError(ValueError):
    """A social-procedure invariant was violated."""


# --------------------------------------------------------------------------- #
# Contests
# --------------------------------------------------------------------------- #

def social_consequence(actor_total: int, resistance_total: int) -> str:
    """Read a social contest's outcome.

    Shares `band_for_margin` with physical conflict, so the arithmetic is identical and
    only the vocabulary differs. A margin below zero is `Unmoved`: in social play, not
    beating resistance means nothing changed -- there is no "graze". A margin of exactly
    zero is the band's bottom edge and means they listened.

    The band function treats every negative margin as "glancing", so the sign check must
    happen here rather than being inferred from the band.
    """
    value = actor_total - resistance_total
    if value < 0:
        return UNMOVED
    return SOCIAL_CONSEQUENCE[band_for_margin(value)]


def is_coercive(method: str) -> bool:
    return method in COERCIVE_METHODS


@dataclass(slots=True)
class SocialOutcome:
    """A resolved social result. Note what it does NOT carry: a belief."""

    consequence: str
    coercive: bool
    grievance: str | None = None
    reputation_step: int = 0

    def __post_init__(self) -> None:
        if self.consequence not in (*SOCIAL_CONSEQUENCE.values(), UNMOVED):
            raise SocialError(f"unknown consequence: {self.consequence!r}")
        if not self.coercive and self.grievance is not None:
            raise SocialError("a Grievance can only follow a coercive method")
        if abs(self.reputation_step) > REPUTATION_STEP:
            raise SocialError(
                f"a witnessed exchange may move Reputation by at most {REPUTATION_STEP} step"
            )


def resolve_social(
    actor_total: int,
    resistance_total: int,
    *,
    method: str,
    witnessed: bool = False,
) -> SocialOutcome:
    """Resolve a social exchange into a bounded consequence.

    Coercion always attaches a Grievance; a witnessed exchange may move Reputation one
    step. Nothing else is created, and nothing existing is overwritten.
    """
    consequence = social_consequence(actor_total, resistance_total)
    coercive = is_coercive(method)
    grievance = GRIEVANCE_ASPECT if coercive else None
    step = 0
    if witnessed and consequence != UNMOVED:
        step = REPUTATION_STEP
    return SocialOutcome(
        consequence=consequence,
        coercive=coercive,
        grievance=grievance,
        reputation_step=step,
    )


# --------------------------------------------------------------------------- #
# Hard limits, as callable assertions
# --------------------------------------------------------------------------- #

def detects_lie(*, kinesics_succeeded: bool, contradicting_evidence: bool) -> bool:
    """Whether a lie is DETECTED. Cues alone never detect a lie.

    Only independent evidence does. This is the executable form of "Kinesics reads cues,
    not truth", and it is a function precisely so no caller can pass a good Kinesics
    result and receive certainty about another mind.
    """
    return bool(contradicting_evidence)


def rewrites_motivation(consequence: str) -> bool:
    """Whether this consequence may rewrite a target's Motivation. Never, at any band."""
    if consequence not in (*SOCIAL_CONSEQUENCE.values(), UNMOVED):
        raise SocialError(f"unknown consequence: {consequence!r}")
    return False


# --------------------------------------------------------------------------- #
# Relationship status: DERIVED from Affect edges, never stored
# --------------------------------------------------------------------------- #

UNKNOWN = "Unknown"
ACQUAINTED = "Acquainted"
TRUSTED = "Trusted"
INDEBTED = "Indebted"
ESTRANGED = "Estranged"
HOSTILE = "Hostile"

STATUSES: tuple[str, ...] = (UNKNOWN, ACQUAINTED, TRUSTED, INDEBTED, ESTRANGED, HOSTILE)

#: PROVISIONAL thresholds.
TRUST_THRESHOLD = 5
HOSTILE_THRESHOLD = -5


@dataclass(frozen=True, slots=True)
class AffectEdgeView:
    """The minimal shape of an Affect edge this module needs. Mirrors `src/simulation/affect.py`."""

    label: str
    score: int


def relationship_status(edges: list[AffectEdgeView] | tuple[AffectEdgeView, ...]) -> str:
    """Compute a relationship status from the Affect edges between two nodes.

    No edges means `Unknown` -- explicitly NOT a stored zero. A status is a read-out, so
    changing a relationship means changing an edge (with provenance), never editing a
    status field beside the graph.
    """
    if not edges:
        return UNKNOWN
    labels = {e.label.lower() for e in edges}
    scores = [e.score for e in edges]
    if "owes" in labels or "indebted" in labels:
        return INDEBTED
    if max(scores) >= TRUST_THRESHOLD:
        return TRUSTED
    if min(scores) <= HOSTILE_THRESHOLD:
        return HOSTILE
    if "distrusts" in labels or "hates" in labels or "opposes" in labels:
        return ESTRANGED
    return ACQUAINTED


def status_is_derived() -> bool:
    """Pinned so an implementation cannot quietly add a stored status field."""
    return True


# --------------------------------------------------------------------------- #
# Groups
# --------------------------------------------------------------------------- #

def group_support(supporting_members: int) -> int:
    """Bounded support: one per member, capped at the recorded +-2 situational cap."""
    if supporting_members < 0:
        raise SocialError("supporting members cannot be negative")
    return min(supporting_members, MAX_GROUP_SUPPORT)


def group_total(leader_stat: int, leader_skill: int, roll: int, supporting_members: int) -> int:
    return leader_stat + leader_skill + roll + group_support(supporting_members)
