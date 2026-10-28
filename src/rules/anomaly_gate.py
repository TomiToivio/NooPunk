"""The anomaly gate (#704): uncertainty has to survive contact with play.

`src/rules/investigation.py` guarantees the *fact* and refuses to conclude anything. This module adds the
one discipline that guarantee still needs: a case may not be resolved as **anomalous** until every
discriminator has been attempted and recorded — including the ones that failed.

Why it exists. The investigative layer makes clues free, so the risk it introduces is not a stalled plot
but the opposite: a table that collects every fact and then treats the strangest reading as established
because it is the most memorable. The gate names, in advance, the test that would separate the ordinary
explanation from the weird one, and refuses resolution while any of those tests is still unrun.

What it does **not** do: it does not judge which reading is true, it does not score confidence, and it
cannot conclude a case. It records attempts and resolutions; the players and the referee do the believing.

Design note (recorded, not enforced): the discriminating test should be *possible* and *cost something*.
A discriminator that no character can run is a wall, not a test, and a discriminator that costs nothing
is a formality.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.rules.investigation import Case, ClueKind, InvestigationError


class GateError(InvestigationError):
    """A dossier or gate operation that breaks the resolution discipline."""


@dataclass
class Readings:
    """The two readings of one clue, and the test that would separate them."""

    clue_id: str
    mundane: str
    anomalous: str
    discriminator: str

    def __post_init__(self) -> None:
        for name in ("mundane", "anomalous", "discriminator"):
            if not getattr(self, name).strip():
                raise GateError(f"clue {self.clue_id}: {name} must be stated, not left blank")
        if self.mundane.strip() == self.anomalous.strip():
            raise GateError(
                f"clue {self.clue_id}: the ordinary and anomalous readings are identical — "
                "that is one reading, and it cannot preserve uncertainty"
            )


@dataclass
class Dossier:
    """A case plus the readings declared for its clues, and the record of what has been tested."""

    case: Case
    readings: dict[str, Readings] = field(default_factory=dict)
    attempted: set[str] = field(default_factory=set)
    resolved: dict[str, str] = field(default_factory=dict)  # clue_id -> "mundane" | "anomalous"

    # -- declaration ------------------------------------------------------

    def declare(self, clue_id: str, *, mundane: str, anomalous: str, discriminator: str) -> Readings:
        """Attach the two readings and the distinguishing test to a clue in this case."""
        # Raises InvestigationError if the clue is not in the case.
        for scene in self.case.scenes:
            for clue in scene.clues:
                if clue.id == clue_id:
                    readings = Readings(clue_id, mundane, anomalous, discriminator)
                    self.readings[clue_id] = readings
                    return readings
        raise GateError(f"case {self.case.id!r} has no clue {clue_id!r}")

    def core_clue_ids(self) -> tuple[str, ...]:
        return tuple(
            clue.id
            for scene in self.case.scenes
            for clue in scene.clues
            if clue.kind is ClueKind.CORE
        )

    def undeclared_core(self) -> tuple[str, ...]:
        return tuple(cid for cid in self.core_clue_ids() if cid not in self.readings)

    def validate(self) -> None:
        """Every core clue must carry a named discriminator before play starts."""
        missing = self.undeclared_core()
        if missing:
            raise GateError(
                "core clues without a declared discriminator: "
                + ", ".join(missing)
                + ". Name the test in advance, or the gate can never be honoured."
            )

    # -- testing ----------------------------------------------------------

    def attempt(self, clue_id: str) -> str:
        """Record that a discriminating test was tried; return the test for the referee to run."""
        if clue_id not in self.readings:
            raise GateError(f"clue {clue_id!r} has no declared readings")
        self.attempted.add(clue_id)
        return self.readings[clue_id].discriminator

    def resolve(self, clue_id: str, *, anomalous: bool | None) -> None:
        """Record what a completed test showed.

        ``anomalous=None`` means **inconclusive**, which is a real result and a common one: the
        test was run and settled nothing. An attempted discriminator is not a conclusive result,
        and a model that can only say yes/no quietly rewards the first test anybody runs (#709).
        """
        if clue_id not in self.attempted:
            raise GateError(
                f"clue {clue_id!r}: a discriminator cannot resolve a question it never asked"
            )
        self.resolved[clue_id] = (
            "inconclusive" if anomalous is None else "anomalous" if anomalous else "mundane"
        )

    # -- the gate ---------------------------------------------------------

    def untested_core(self) -> tuple[str, ...]:
        return tuple(cid for cid in self.core_clue_ids() if cid not in self.attempted)

    def gate_open(self) -> bool:
        return not self.untested_core()

    def may_conclude_anomalous(self) -> bool:
        """The whole point: no anomalous conclusion while a core test is unrun."""
        return self.gate_open()

    def require_open(self) -> None:
        if not self.gate_open():
            raise GateError(
                "cannot resolve as anomalous: discriminators not attempted for "
                + ", ".join(self.untested_core())
            )

    def provisional_referral(self, reason: str) -> dict[str, object]:
        """Refer a case upward without proving an ontology.

        An investigator can say "this needs the anomaly desk" on one strange fact and an
        inconclusive test; requiring the gate to be fully open before a *referral* would make the
        procedure demand proof of the thing under investigation (#709). A referral is explicitly
        provisional and is not a conclusion.
        """
        if not reason.strip():
            raise GateError("a referral must give a reason")
        return {
            "provisional": True,
            "reason": reason,
            "gate_open": self.gate_open(),
            "outstanding": self.untested_core(),
        }

    def tally(self) -> dict[str, int]:
        """Counts only. This is a record, not a verdict."""
        return {
            "attempted": len(self.attempted),
            "resolved_mundane": sum(1 for v in self.resolved.values() if v == "mundane"),
            "resolved_anomalous": sum(1 for v in self.resolved.values() if v == "anomalous"),
            "inconclusive": sum(1 for v in self.resolved.values() if v == "inconclusive"),
            "outstanding": len(self.untested_core()),
        }


@dataclass
class HypothesisLedger:
    """An arbitrary number of live hypotheses, none of which the model may retire.

    Two readings per clue is how a *clue* is written; it is not a claim that a case has only two
    explanations. A table may hold a template artifact, a clerk, a precognition and a deception at
    once, and resolving one discriminator must not delete the others (#709).
    """

    entries: dict[str, str] = field(default_factory=dict)   # id -> statement
    withdrawn: set[str] = field(default_factory=set)

    def add(self, hypothesis_id: str, statement: str) -> None:
        if not hypothesis_id.strip() or not statement.strip():
            raise GateError("a hypothesis needs an id and a statement")
        if hypothesis_id in self.entries:
            raise GateError(f"hypothesis {hypothesis_id!r} already exists")
        self.entries[hypothesis_id] = statement

    def withdraw(self, hypothesis_id: str, *, reason: str) -> None:
        """Only a player or referee retires a hypothesis, and only for a stated reason."""
        if hypothesis_id not in self.entries:
            raise GateError(f"no hypothesis {hypothesis_id!r}")
        if not reason.strip():
            raise GateError("a hypothesis is withdrawn for a reason, not silently")
        self.withdrawn.add(hypothesis_id)

    def live(self) -> tuple[str, ...]:
        return tuple(h for h in self.entries if h not in self.withdrawn)

    def count(self) -> int:
        return len(self.live())
