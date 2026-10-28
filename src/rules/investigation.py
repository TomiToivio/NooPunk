"""The GUMSHOE-inspired investigation procedure (#704).

This module is the executable half of `docs/design/ISSUE_704_GUMSHOE_INVESTIGATION.md`. It enforces the
two rules that are easy to state and easy to violate, and it deliberately does **not** roll dice.

**Rule 1 — no dead ends.** Every core clue must be reachable by at least two independent paths. A case
that violates this is refused at validation time, because the failure is an authoring defect that a
table discovers only by stalling.

**Rule 2 — finding is free, interpretation costs a check.** `seek()` returns the *fact* whenever the
three conditions hold (access, competency, declaration). It never returns a *reading*. `interpret()`
never returns truth: it returns a reading flagged as requiring a check, which the CWN engine resolves
elsewhere. There is no code path in this module that rolls, and none that concludes.

Nothing here defines an attribute, a skill rating scale, or a die. Methods are plain strings so the
module works with whichever skill list the migration settles on.

Source basis: GUMSHOE SRD (CC BY 3.0), p. 50 "Gathering Clues" and the core-clue rules. No SRD text is
reproduced.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from enum import Enum


class InvestigationError(ValueError):
    """A case, clue or ledger operation that violates the procedure."""


class DeadEndError(InvestigationError):
    """A core clue with fewer than two independent paths — an authoring defect."""


class Grade(str, Enum):
    CORE = "core"          # guaranteed once the three conditions hold
    OPTIONAL = "optional"  # bought with a spend
    COLOUR = "colour"      # free on arrival, no mechanical weight


class ReadingKind(str, Enum):
    MUNDANE = "mundane"
    ANOMALOUS = "anomalous"


class Outcome(str, Enum):
    GUARANTEED = "guaranteed"      # core fact, conditions met, no roll
    REQUIRES_SPEND = "requires_spend"  # optional clue: pay, then receive
    REQUIRES_CHECK = "requires_check"  # competency missing: ordinary check, failure possible
    COLOUR = "colour"              # free texture
    UNKNOWN = "unknown"            # the method does not reach this clue; alternatives listed


@dataclass(frozen=True)
class Clue:
    """One clue, written twice: a fact and two readings, plus the test that separates them."""

    id: str
    scene: str
    grade: Grade
    fact: str
    mundane_reading: str
    anomalous_reading: str
    discriminator: str
    methods: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.fact.strip():
            raise InvestigationError(f"clue {self.id}: a fact is required")
        if not self.methods:
            raise InvestigationError(f"clue {self.id}: at least one method is required")
        if self.grade is Grade.CORE and not self.discriminator.strip():
            raise InvestigationError(
                f"core clue {self.id}: a discriminator must be named in advance — "
                "otherwise the anomaly gate can never be honoured"
            )


@dataclass(frozen=True)
class SeekResult:
    """What `seek()` is allowed to return: a fact, or a reason it is not free."""

    outcome: Outcome
    fact: str | None
    clue_id: str | None = None
    alternatives: tuple[str, ...] = ()
    reason: str = ""

    @property
    def is_fact(self) -> bool:
        return self.outcome in (Outcome.GUARANTEED, Outcome.COLOUR, Outcome.REQUIRES_SPEND)


@dataclass(frozen=True)
class Reading:
    """An interpretation. Never truth: always flagged as needing the engine's check."""

    clue_id: str
    kind: ReadingKind
    statement: str
    requires_check: bool = True


@dataclass
class Case:
    """A case model: scenes, clues, and what has been established."""

    id: str
    scenes: tuple[str, ...]
    clues: tuple[Clue, ...]
    discovered: set[str] = field(default_factory=set)
    discriminators_attempted: set[str] = field(default_factory=set)
    discriminators_resolved: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        unknown = {c.scene for c in self.clues} - set(self.scenes)
        if unknown:
            raise InvestigationError(f"case {self.id}: clues in unknown scenes {sorted(unknown)}")
        ids = [c.id for c in self.clues]
        if len(ids) != len(set(ids)):
            raise InvestigationError(f"case {self.id}: duplicate clue ids")

    # -- authoring lint ---------------------------------------------------

    def clue(self, clue_id: str) -> Clue:
        for c in self.clues:
            if c.id == clue_id:
                return c
        raise InvestigationError(f"case {self.id}: no clue {clue_id}")

    def core_clues(self) -> tuple[Clue, ...]:
        return tuple(c for c in self.clues if c.grade is Grade.CORE)

    def dead_ends(self) -> tuple[Clue, ...]:
        """Core clues with fewer than two independent paths through distinct methods."""
        return tuple(c for c in self.core_clues() if len(set(c.methods)) < 2)

    def validate(self) -> None:
        """Refuse a case that can dead-end. Call this on load, not on play."""
        dead = self.dead_ends()
        if dead:
            names = ", ".join(f"{c.id} (methods: {', '.join(c.methods)})" for c in dead)
            raise DeadEndError(
                f"case {self.id}: core clues reachable one way only: {names}. "
                "Give each a second method, a second scene, or an institutional route."
            )

    # -- play -------------------------------------------------------------

    def seek(self, clue_id: str, method: str, *, trained: bool) -> SeekResult:
        """Look for a clue. Never rolls; never interprets."""
        clue = self.clue(clue_id)

        if clue.grade is Grade.COLOUR:
            self.discovered.add(clue.id)
            return SeekResult(Outcome.COLOUR, clue.fact, clue.id, reason="colour: free on arrival")

        if method not in clue.methods:
            return SeekResult(
                Outcome.UNKNOWN,
                None,
                clue.id,
                alternatives=tuple(clue.methods),
                reason=f"method {method!r} does not reach this clue",
            )

        if not trained:
            # The guarantee requires competency. An untrained attempt is an ordinary check.
            return SeekResult(
                Outcome.REQUIRES_CHECK,
                None,
                clue.id,
                reason="untrained: the guarantee does not apply; resolve as a normal check",
            )

        if clue.grade is Grade.CORE:
            self.discovered.add(clue.id)
            return SeekResult(Outcome.GUARANTEED, clue.fact, clue.id, reason="core clue: no roll")

        return SeekResult(
            Outcome.REQUIRES_SPEND,
            None,
            clue.id,
            reason="optional clue: pay time, resource, risk or credibility",
        )

    def pay_and_take(self, clue_id: str, *, spent: str) -> SeekResult:
        """Complete a spend for an optional clue."""
        clue = self.clue(clue_id)
        if clue.grade is not Grade.OPTIONAL:
            raise InvestigationError(f"clue {clue.id} is {clue.grade.value}, not optional")
        if not spent.strip():
            raise InvestigationError("a spend must name what it costs")
        self.discovered.add(clue.id)
        return SeekResult(Outcome.GUARANTEED, clue.fact, clue.id, reason=f"paid with {spent}")

    def interpret(self, clue_id: str, kind: ReadingKind) -> Reading:
        """Return a reading, flagged for the engine. This method cannot conclude anything."""
        clue = self.clue(clue_id)
        if clue.id not in self.discovered:
            raise InvestigationError(
                f"clue {clue.id} has not been established; a reading needs its fact first"
            )
        statement = (
            clue.mundane_reading if kind is ReadingKind.MUNDANE else clue.anomalous_reading
        )
        return Reading(clue.id, kind, statement)

    # -- the anomaly gate -------------------------------------------------

    def attempt_discriminator(self, clue_id: str) -> str:
        clue = self.clue(clue_id)
        self.discriminators_attempted.add(clue.id)
        return clue.discriminator

    def resolve_discriminator(self, clue_id: str, *, supports: ReadingKind) -> None:
        if clue_id not in self.discriminators_attempted:
            raise InvestigationError(
                f"clue {clue_id}: a discriminator must be attempted before it can resolve"
            )
        self.discriminators_resolved.add(f"{clue_id}:{supports.value}")

    def anomaly_gate_open(self) -> bool:
        """True only when every core clue's discriminator has been attempted."""
        return all(c.id in self.discriminators_attempted for c in self.core_clues())

    def require_anomaly_gate(self) -> None:
        if not self.anomaly_gate_open():
            missing = [
                c.id for c in self.core_clues() if c.id not in self.discriminators_attempted
            ]
            raise InvestigationError(
                "cannot resolve the case as anomalous: discriminators not attempted for "
                + ", ".join(missing)
            )


@dataclass(frozen=True)
class Hypothesis:
    id: str
    kind: ReadingKind
    statement: str
    support: tuple[str, ...] = ()       # clue ids
    contradict: tuple[str, ...] = ()    # clue ids


def actionable(hypothesis: Hypothesis, case: Case) -> bool:
    """Two *independent* supports and no unaddressed contradiction.

    Independence is by scene: two facts from one document are one fact wearing two hats.
    """
    if hypothesis.contradict:
        return False
    scenes = set()
    for clue_id in hypothesis.support:
        clue = case.clue(clue_id)
        if clue.id not in case.discovered:
            continue
        scenes.add(clue.scene)
    return len(scenes) >= 2


def support_report(hypotheses: Iterable[Hypothesis], case: Case) -> Mapping[str, bool]:
    return {h.id: actionable(h, case) for h in hypotheses}
