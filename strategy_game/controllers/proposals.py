"""Move proposals: the data a controller may *declare*, never a move that has happened.

Issue #304 asks for optional human/scripted/Ollama-controlled player agents and a separate Game
Master, while keeping the deterministic rules engine "the only component allowed to commit normal
game transitions". Its own milestone list draws the line this module implements:

    "Design an engine-independent `Controller / GameMaster / MoveProposal / ResolvedMove /
     GMIntervention / SessionState` conceptual interface ... ; avoid competing state engines."

The design comment already recorded on #304 settled the boundary and named the reusable seams
(`ports.py`, `capabilities.py`, `provenance.py`, `tabletop/dice.py`, `tabletop/serialization.py`).
This module is the *structure* that boundary asks for and nothing beyond it.

What a proposal is
------------------

A :class:`MoveProposal` is a **declaration**, not a resolution:

* ``controller_id`` -- which controller is speaking (identity, not authority to act alone);
* ``leader_id`` -- **required**; an unnamed faction action is not a proposal;
* ``action_code`` -- an **open string**. No action set is approved, so none is assumed. The module
  declares :data:`APPROVED_ACTION_CODES` as an empty tuple precisely so that "nothing approved yet"
  is visible in code rather than smuggled in as a default verb;
* ``target_id`` -- what the declared action is aimed at (a declared reference, not a lookup);
* ``resources`` -- declared resource *names* only. There is deliberately no quantity anywhere: an
  amount would be an economy, and this project has approved no economy;
* ``rationale`` -- free text, i.e. fiction. It is stored as untrusted content and is never read as
  an instruction or a transition;
* ``provenance`` -- defaults to :attr:`strategy_game.provenance.ProvenanceKind.UNKNOWN`, so an
  unclassified origin stays visibly unknown instead of reading as fact.

What this module never does
---------------------------

No resolution, no thresholds, no success/failure, no action set, no GM menu, no mechanics. A
*container* is not a rule. :class:`ProposalRecorder` stores proposals **as data only** and takes
**no world or table state argument at all** -- so it has no handle with which to mutate authoritative
state, which is a stronger guarantee than a promise not to. Reading and replaying a recorded log
imports nothing from :data:`strategy_game.capabilities.OPTIONAL_ADAPTERS`.

Reserved to the author (see :data:`PENDING_AUTHOR_RULINGS`): the approved action set, the resolution
core, the GM's closed menu of intervention types, hidden-information rules for multiplayer, the
online transport, and every Tarot meaning or effect.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Any

from ..provenance import Provenance

if TYPE_CHECKING:  # pragma: no cover - typing only; no import at runtime, so no cycle
    from .controllers import ControllerRegistry


class ProposalError(ValueError):
    """Raised for a malformed proposal."""


class UnauthorizedProposalError(ProposalError):
    """Raised when a controller proposes for a leader it is not authorised to command."""


class AssignmentConflict(ProposalError):
    """Raised when a leader is assigned a second, different authoritative controller."""


#: The action codes the author has approved. **Empty**: no action set is approved, so this module
#: assumes none. It is declared (rather than omitted) so that "nothing is approved yet" is a visible
#: value a caller can read, and so that a future approval changes exactly one constant.
APPROVED_ACTION_CODES: tuple[str, ...] = ()

#: What this unit deliberately did **not** invent, each with the reason it needs an author ruling.
#: Carried as data so a later reader can see the boundary in code instead of having to trust prose.
PENDING_AUTHOR_RULINGS: tuple[str, ...] = (
    "the approved action set: MoveProposal.action_code stays an open string until the author names one",
    "the resolution core: no ResolvedMove, no threshold, no success/failure is implemented here",
    "the Game Master's closed menu of intervention types: no GMIntervention record is invented",
    "hidden-information rules (what a controller may read, and when): needed at a physical table, "
    "not a networking problem, and undecided",
    "online multiplayer transport: an offline open-source game may not assume a server, and the "
    "hidden-information rule it depends on is undecided",
    "every NoöPunk Tarot meaning, composition and mechanical effect: reserved to the author by #304",
)


@dataclass
class MoveProposal:
    """One controller's declared move for one leader. A record, not an outcome.

    The fields are all declarative. Nothing here is compared, spent, rolled or applied, and no
    numeric field is declared at all -- see the module docstring for why each field is shaped this
    way. ``leader_id`` is required: constructing a proposal without it is refused, because "an
    unnamed faction action is invalid" is a structural fact the container can enforce without
    deciding any rule.
    """

    controller_id: str
    leader_id: str
    action_code: str = ""
    target_id: str = ""
    resources: tuple[str, ...] = ()
    rationale: str = ""
    #: Where this declaration came from. Defaults to UNKNOWN: an unclassified origin stays visible.
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.controller_id = str(self.controller_id).strip()
        leader_id = self.leader_id
        self.action_code = str(self.action_code)
        self.target_id = str(self.target_id)
        self.resources = tuple(str(item) for item in (self.resources or ()))
        self.rationale = str(self.rationale)
        # ``None`` is not a leader either: ``str(None)`` would quietly become the word "None".
        if leader_id is None or not str(leader_id).strip():
            raise ProposalError(
                "a MoveProposal requires a leader_id; a declaration with no leader is invalid"
            )
        self.leader_id = str(leader_id).strip()
        # Accept a legacy bare string or a raw dict the way core.Event does, so a recorded snapshot
        # is never rejected for carrying an unclassified origin.
        if not isinstance(self.provenance, Provenance):
            self.provenance = Provenance.from_dict(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        """Plain-JSON scalars; keys match the dataclass fields."""
        return {
            "controller_id": self.controller_id,
            "leader_id": self.leader_id,
            "action_code": self.action_code,
            "target_id": self.target_id,
            "resources": list(self.resources),
            "rationale": self.rationale,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MoveProposal":
        return cls(
            controller_id=data.get("controller_id", ""),
            leader_id=data.get("leader_id", ""),
            action_code=data.get("action_code", ""),
            target_id=data.get("target_id", ""),
            resources=tuple(data.get("resources") or ()),
            rationale=data.get("rationale", ""),
            provenance=Provenance.from_dict(data.get("provenance")),
        )

    @property
    def field_names(self) -> tuple[str, ...]:
        return tuple(item.name for item in fields(self))


@dataclass
class ProposalLog:
    """An append-only list of recorded proposals. The record, not the result."""

    entries: list[MoveProposal] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.entries)

    def append(self, proposal: MoveProposal) -> MoveProposal:
        """Append a proposal and return it, so ``log.append(recorder.record(p))`` reads in one line."""
        self.entries.append(proposal)
        return proposal

    def replay(self) -> tuple[MoveProposal, ...]:
        """Rebuild every proposal from the stored data.

        No RNG, no model and no optional adapter is consulted -- a recorded declaration is an
        exogenous input the replay consumes, exactly like a recorded die face. This is what makes a
        run reproducible *given its recorded inputs* even when an LLM produced some of them.
        """
        return tuple(MoveProposal.from_dict(entry.to_dict()) for entry in self.entries)

    def to_dict(self) -> dict[str, Any]:
        return {"entries": [entry.to_dict() for entry in self.entries]}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProposalLog":
        return cls(entries=[MoveProposal.from_dict(item) for item in (data.get("entries") or ())])


class ProposalRecorder:
    """Records a proposal after checking identity, and stores it as data only.

    The recorder deliberately has **no** ``WorldState`` or ``TableState`` parameter. It cannot apply
    a proposal because it is never handed anything to apply it to; the only state it owns is the
    :class:`ProposalLog`. Committing a normal game transition is the deterministic rules engine's
    job and is out of scope for this unit (#304: "the only component allowed to commit normal game
    transitions").

    The authorisation check is a **boundary check, not a game rule**: it refuses a proposal whose
    ``leader_id`` is not commanded by the stated controller, exactly as an LLM controller and a human
    controller must be indistinguishable to it.
    """

    def __init__(self, registry: "ControllerRegistry") -> None:
        # Duck-typed on purpose: the authority only has to be able to answer `authorize`. This keeps
        # this module importable on its own (no runtime import of the registry, hence no cycle).
        if not callable(getattr(registry, "authorize", None)):
            raise ProposalError("a ProposalRecorder needs an authority exposing authorize(...)")
        self._registry = registry
        self.log = ProposalLog()

    @property
    def entries(self) -> tuple[MoveProposal, ...]:
        return tuple(self.log.entries)

    def record(self, proposal: MoveProposal) -> MoveProposal:
        """Authorise and store a proposal. Mutates only this recorder's own log."""
        self._registry.authorize(proposal.controller_id, proposal.leader_id)
        return self.log.append(proposal)

    def replay(self) -> tuple[MoveProposal, ...]:
        return self.log.replay()

    def to_dict(self) -> dict[str, Any]:
        return self.log.to_dict()

    @classmethod
    def from_dict(cls, data: dict[str, Any], registry: "ControllerRegistry") -> "ProposalRecorder":
        recorder = cls(registry)
        recorder.log = ProposalLog.from_dict(data)
        return recorder
