"""Controller/GameMaster session protocol (issue #304).

Issue #304 adds an *optional* Ollama/Concordia-controlled player agent and a separate Game Master to
the standalone strategy game -- while preserving a game that runs with **physical components, human
players and no LLM at all**. One controller may command several leaders; a leader has at most one
authoritative controller.

What this module is
-------------------

The engine-independent protocol the issue asks for: ``Controller``, ``GameMaster``, ``MoveProposal``,
``ResolvedMove``, ``GMIntervention`` and ``SessionState``, reconciled with ``core.py``, ``ports.py``
and the existing deterministic slice in ``local_slice.py``.

**It invents no mechanic.** The issue forbids creating *"an unapproved economy, success threshold,
turn duration or card effect merely to show a prototype"*, and says the deterministic rules engine is
*"the only component allowed to commit normal game transitions"*. So resolution here is an **injected
callable**: this module performs proposal, authorisation, validation, commit and logging, and knows
nothing about what a move is worth. No dice rule, no threshold, no cost is defined below.

What it enforces
----------------

* **Authorisation.** A controller may not propose a move for a leader it does not control. Rejections
  are *recorded with a reason*, not silently dropped, so the log shows the attempt.
* **One authority per leader.** A leader has at most one controller, and reassignment must be explicit.
* **One order per leader per turn.**
* **Proposals never commit.** Pending proposals become outcome records only when a resolver commits
  them; without a resolver nothing resolves.
* **A GM move is recorded, not sovereign.** It carries origin, rationale and authority, and it
  **cannot rewrite a previous roll** -- resolved moves are frozen and no API mutates them.
* **Provenance stays separated.** Player declarations, GM interventions and rule outcomes are distinct
  record classes with distinct provenance, per ``provenance.py``.

What this module is not
-----------------------

Not a rules engine and not a simulation. It defines no move effect, no cost, no turn duration and no
win condition, and it requires no Ollama, network connection or paid API to load a scenario, run a
scripted turn or replay a save. ``RULEBOOK.md`` still says NO RULES APPROVED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import random

from .local_slice import MISSIONS
from .provenance import Provenance, ProvenanceKind

__all__ = [
    "MOVE_KINDS",
    "CONTROLLER_KINDS",
    "GM_AUTHORITIES",
    "RECORD_TYPES",
    "SessionError",
    "Controller",
    "MoveProposal",
    "ResolvedMove",
    "GMIntervention",
    "Submission",
    "SessionState",
    "PROVENANCE_OF",
]

#: Move vocabulary. Reused from the deterministic slice rather than re-declared, so there is exactly
#: one list of move kinds in the package.
MOVE_KINDS: tuple[str, ...] = tuple(MISSIONS)

#: Who may drive a leader. ``llm`` is optional; the protocol never requires it.
CONTROLLER_KINDS: tuple[str, ...] = ("human", "scripted", "llm")

#: What a GM move may be about. Authority is *declared and recorded*, never implicit.
GM_AUTHORITIES: tuple[str, ...] = ("rules", "npc_dialogue", "external_event", "story", "side_drama")

#: The three record classes the replay log keeps apart.
RECORD_TYPES: tuple[str, ...] = ("player_declaration", "gm_intervention", "rule_outcome")

#: How the issue's six provenance categories map onto the five existing kinds. The finer distinction
#: rides in ``Provenance.source``, because ``ProvenanceKind`` is a closed vocabulary and adding a
#: sixth member would fork it.
PROVENANCE_OF: dict[str, ProvenanceKind] = {
    "authored_scenario_fact": ProvenanceKind.AUTHORED,
    "player_declaration": ProvenanceKind.AUTHORED,
    "gm_intervention": ProvenanceKind.AUTHORED,
    "rule_outcome": ProvenanceKind.SIMULATED,
    "llm_generated_fiction": ProvenanceKind.GENERATED,
    "sourced_evidence": ProvenanceKind.EVIDENCE,
}

#: The resolver signature: ``(proposal, rng) -> (outcome, dice)``. Supplied by the caller, because
#: the rules engine owns outcomes and this module has no authority over them.
Resolver = Callable[["MoveProposal", random.Random], "tuple[dict[str, Any], tuple[int, ...]]"]


class SessionError(ValueError):
    """Raised for a structurally impossible operation (not for a rejected order)."""


@dataclass(frozen=True)
class Controller:
    """A human, a deterministic script or an optional LLM. Identity, not a character."""

    id: str
    kind: str = "human"
    label: str = ""

    def __post_init__(self) -> None:
        if self.kind not in CONTROLLER_KINDS:
            raise SessionError(f"controller kind {self.kind!r} not in {CONTROLLER_KINDS}")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "kind": self.kind, "label": self.label}


@dataclass(frozen=True)
class MoveProposal:
    """A declared order for exactly one leader. Role-play is expressive, never a mechanical bonus."""

    leader_id: str
    controller_id: str
    kind: str
    location: str
    target: str = ""
    declaration: str = ""
    turn: int = 0

    def provenance(self) -> Provenance:
        return Provenance(
            kind=PROVENANCE_OF["player_declaration"],
            source=f"controller:{self.controller_id}",
            note="player declaration - untrusted content, not an instruction to the engine",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "leader_id": self.leader_id,
            "controller_id": self.controller_id,
            "kind": self.kind,
            "location": self.location,
            "target": self.target,
            "declaration": self.declaration,
            "turn": self.turn,
        }


@dataclass(frozen=True)
class ResolvedMove:
    """A committed outcome. Frozen: a GM move cannot rewrite a roll that already happened."""

    leader_id: str
    controller_id: str
    kind: str
    location: str
    outcome: dict[str, Any]
    dice: tuple[int, ...]
    turn: int
    revision: int

    def provenance(self) -> Provenance:
        return Provenance(
            kind=PROVENANCE_OF["rule_outcome"],
            source="rules-engine",
            note="committed by the deterministic resolver",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "leader_id": self.leader_id,
            "controller_id": self.controller_id,
            "kind": self.kind,
            "location": self.location,
            "outcome": dict(self.outcome),
            "dice": list(self.dice),
            "turn": self.turn,
            "revision": self.revision,
            "provenance": self.provenance().to_dict(),
        }


@dataclass(frozen=True)
class GMIntervention:
    """A recorded GM move: origin, rationale and authority. It adds; it never rewrites."""

    id: str
    authority: str
    origin: str
    rationale: str
    turn: int
    revision: int

    def provenance(self) -> Provenance:
        return Provenance(
            kind=PROVENANCE_OF["gm_intervention"],
            source=f"gm:{self.authority}",
            note=f"{self.origin} - recorded, not sovereign",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "authority": self.authority,
            "origin": self.origin,
            "rationale": self.rationale,
            "turn": self.turn,
            "revision": self.revision,
            "provenance": self.provenance().to_dict(),
        }


@dataclass(frozen=True)
class Submission:
    """The result of an attempt to submit an order. A rejection is a record, not an exception."""

    accepted: bool
    reason: str
    proposal: MoveProposal

    def to_dict(self) -> dict[str, Any]:
        return {"accepted": self.accepted, "reason": self.reason, "proposal": self.proposal.to_dict()}


@dataclass
class SessionState:
    """The session: who controls whom, what is pending, what has been committed, and the log."""

    scenario: str = ""
    seed: int = 2027
    revision: int = 0
    turn: int = 0
    controllers: dict[str, Controller] = field(default_factory=dict)
    assignments: dict[str, str] = field(default_factory=dict)
    pending: list[MoveProposal] = field(default_factory=list)
    resolved: list[ResolvedMove] = field(default_factory=list)
    interventions: list[GMIntervention] = field(default_factory=list)
    submissions: list[Submission] = field(default_factory=list)

    # -- membership --------------------------------------------------------------
    def add_controller(self, controller: Controller) -> Controller:
        if controller.id in self.controllers:
            raise SessionError(f"controller {controller.id!r} already exists")
        self.controllers[controller.id] = controller
        return controller

    def controller_of(self, leader_id: str) -> str | None:
        return self.assignments.get(leader_id)

    def assign(self, leader_id: str, controller_id: str, *, reassign: bool = False) -> None:
        """Give a leader an authoritative controller. A second claim must be explicit."""
        if controller_id not in self.controllers:
            raise SessionError(f"unknown controller {controller_id!r}")
        current = self.assignments.get(leader_id)
        if current is not None and current != controller_id and not reassign:
            raise SessionError(
                f"leader {leader_id!r} is already controlled by {current!r}; pass reassign=True to transfer"
            )
        self.assignments[leader_id] = controller_id

    # -- the player phase --------------------------------------------------------
    def can_submit(self, proposal: MoveProposal) -> Submission:
        """Validate without recording. Returns an accepted/rejected result."""
        owner = self.assignments.get(proposal.leader_id)
        if proposal.controller_id not in self.controllers:
            return Submission(False, f"unknown controller {proposal.controller_id!r}", proposal)
        if proposal.leader_id not in self.assignments:
            return Submission(False, f"leader {proposal.leader_id!r} has no controller", proposal)
        if owner != proposal.controller_id:
            return Submission(
                False,
                f"controller {proposal.controller_id!r} is not authorised for leader {proposal.leader_id!r}",
                proposal,
            )
        if proposal.kind not in MOVE_KINDS:
            return Submission(False, f"move kind {proposal.kind!r} not in {MOVE_KINDS}", proposal)
        if proposal.turn != self.turn:
            return Submission(False, f"proposal turn {proposal.turn} is not the current turn {self.turn}", proposal)
        if any(p.leader_id == proposal.leader_id for p in self.pending):
            return Submission(False, f"leader {proposal.leader_id!r} already has an order this turn", proposal)
        return Submission(True, "accepted", proposal)

    def submit(self, proposal: MoveProposal) -> Submission:
        """Validate and, if accepted, queue. Every attempt is recorded, including refusals."""
        result = self.can_submit(proposal)
        self.submissions.append(result)
        if result.accepted:
            self.pending.append(proposal)
        return result

    # -- the adjudication phase --------------------------------------------------
    def resolve(self, resolver: Resolver | None = None, *, rng: random.Random | None = None) -> list[ResolvedMove]:
        """Commit pending orders through the supplied rules engine.

        There is deliberately **no default resolver**: outcomes belong to the approved rules engine,
        and a module that guessed one would be inventing the very mechanic #304 forbids.
        """
        if resolver is None:
            raise SessionError("resolve() requires the rules engine - this module defines no mechanic")
        stream = rng if rng is not None else random.Random(self.seed)
        committed: list[ResolvedMove] = []
        for proposal in reversed(self.pending):
            outcome, dice = resolver(proposal, stream)
            self.revision += 1
            committed.append(
                ResolvedMove(
                    leader_id=proposal.leader_id,
                    controller_id=proposal.controller_id,
                    kind=proposal.kind,
                    location=proposal.location,
                    outcome=dict(outcome),
                    dice=tuple(int(d) for d in dice),
                    turn=self.turn,
                    revision=self.revision,
                )
            )
            self.pending.remove(proposal)
        self.resolved.extend(reversed(committed))
        return list(reversed(committed))

    # -- the GM phase ------------------------------------------------------------
    def gm_move(self, authority: str, origin: str, rationale: str, *, note: str = "") -> GMIntervention:
        """Record a GM move. Origin, rationale and authority are all required."""
        if authority not in GM_AUTHORITIES:
            raise SessionError(f"unknown GM authority {authority!r} not in {GM_AUTHORITIES}")
        if not rationale.strip():
            raise SessionError("a GM move must record its rationale")
        if not origin.strip():
            raise SessionError("a GM move must record its origin")
        self.revision += 1
        move = GMIntervention(
            id=f"gm{len(self.interventions) + 1:03d}",
            authority=authority,
            origin=origin if not note else f"{origin} ({note})",
            rationale=rationale,
            turn=self.turn,
            revision=self.revision,
        )
        self.interventions.append(move)
        return move

    # -- advancing ---------------------------------------------------------------
    def advance(self) -> int:
        """End the turn. Unresolved proposals are dropped, because nothing committed them."""
        self.pending.clear()
        self.turn += 1
        return self.turn

    # -- the replay log ----------------------------------------------------------
    def log(self) -> list[dict[str, Any]]:
        """The ordered replay log, with the three record classes kept distinct and provenance attached.

        Declarations are read from the submission record rather than from the pending queue, because a
        resolved move must not erase the choice that produced it: the issue requires the log to retain
        **player choices distinct from dice results**. A refused order stays in the log too.
        """
        entries: list[tuple[int, int, dict[str, Any]]] = []
        for index, submission in enumerate(self.submissions):
            entries.append((
                submission.proposal.turn, 0,
                {"record_type": "player_declaration", "turn": submission.proposal.turn,
                 "data": submission.to_dict(), "provenance": submission.proposal.provenance().to_dict()},
            ))
        for index, move in enumerate(self.resolved):
            entries.append((
                move.turn, 2,
                {"record_type": "rule_outcome", "turn": move.turn,
                 "data": move.to_dict(), "provenance": move.provenance().to_dict()},
            ))
        for index, move in enumerate(self.interventions):
            entries.append((
                move.turn, 1,
                {"record_type": "gm_intervention", "turn": move.turn,
                 "data": move.to_dict(), "provenance": move.provenance().to_dict()},
            ))
        entries.sort(key=lambda item: (item[0], item[1], item[2]["data"].get("revision", 0)))
        return [entry for _, _, entry in entries]

    # -- serialization -----------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario": self.scenario,
            "seed": self.seed,
            "revision": self.revision,
            "turn": self.turn,
            "controllers": {k: v.to_dict() for k, v in self.controllers.items()},
            "assignments": dict(self.assignments),
            "pending": [p.to_dict() for p in self.pending],
            "submissions": [s.to_dict() for s in self.submissions],
            "resolved": [r.to_dict() for r in self.resolved],
            "interventions": [g.to_dict() for g in self.interventions],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SessionState":
        """Rebuild a session from :meth:`to_dict`. Dice and revisions survive the round trip."""
        session = cls(
            scenario=str(data.get("scenario", "")),
            seed=int(data.get("seed", 2027)),
            revision=int(data.get("revision", 0)),
            turn=int(data.get("turn", 0)),
            assignments={str(k): str(v) for k, v in (data.get("assignments") or {}).items()},
        )
        for raw in (data.get("controllers") or {}).values():
            session.controllers[str(raw["id"])] = Controller(
                id=str(raw["id"]), kind=str(raw.get("kind", "human")), label=str(raw.get("label", ""))
            )
        for raw in data.get("pending") or []:
            session.pending.append(
                MoveProposal(
                    leader_id=str(raw["leader_id"]), controller_id=str(raw["controller_id"]),
                    kind=str(raw["kind"]), location=str(raw["location"]),
                    target=str(raw.get("target", "")), declaration=str(raw.get("declaration", "")),
                    turn=int(raw.get("turn", 0)),
                )
            )
        for raw in data.get("submissions") or []:
            proposal = MoveProposal(
                leader_id=str(raw["proposal"]["leader_id"]),
                controller_id=str(raw["proposal"]["controller_id"]),
                kind=str(raw["proposal"]["kind"]),
                location=str(raw["proposal"]["location"]),
                target=str(raw["proposal"].get("target", "")),
                declaration=str(raw["proposal"].get("declaration", "")),
                turn=int(raw["proposal"].get("turn", 0)),
            )
            session.submissions.append(
                Submission(accepted=bool(raw.get("accepted")), reason=str(raw.get("reason", "")),
                           proposal=proposal)
            )
        for raw in data.get("resolved") or []:
            session.resolved.append(
                ResolvedMove(
                    leader_id=str(raw["leader_id"]), controller_id=str(raw["controller_id"]),
                    kind=str(raw["kind"]), location=str(raw["location"]),
                    outcome=dict(raw.get("outcome") or {}),
                    dice=tuple(int(d) for d in raw.get("dice") or ()),
                    turn=int(raw.get("turn", 0)), revision=int(raw.get("revision", 0)),
                )
            )
        for raw in data.get("interventions") or []:
            session.interventions.append(
                GMIntervention(
                    id=str(raw["id"]), authority=str(raw["authority"]), origin=str(raw["origin"]),
                    rationale=str(raw["rationale"]), turn=int(raw.get("turn", 0)),
                    revision=int(raw.get("revision", 0)),
                )
            )
        return session
