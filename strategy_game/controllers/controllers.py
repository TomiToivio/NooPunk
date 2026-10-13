"""Controllers and their authority: the real protocol, two model-free providers, and the adapter seam.

Issue #304 asks for a controller that "may control several faction leaders", for a human/scripted
controller to work "**before** adding Ollama", and for the LLM and human cases to be
indistinguishable to the rules engine. It also asks that no Ollama, network connection or paid API be
needed "to load a scenario, run a scripted turn or replay a save".

:mod:`strategy_game.ports` already reserves ``AgentProvider``/``AgentRunner`` as **signature-only**
seams (``describe(state)``, no behaviour). This module is the *real* protocol those seams stand in
for, and it is deliberately behavioural but rule-free:

* :class:`Controller` -- identity plus two questions: *do you command this leader?* and *what, if
  anything, do you propose for it?* An LLM controller and a human controller answer the same two
  questions, so the recorder cannot tell them apart;
* :class:`ControllerRegistry` -- which controller commands which leader. A leader has **at most one**
  authoritative controller, enforced here rather than documented;
* :class:`NullAgentProvider` -- the default controller: proposes **nothing**. The game plays, loads
  and replays with this and no model provider present at all;
* :class:`ScriptedAgentProvider` -- a **deterministic** controller replaying a fixed script: same
  calls, same output, byte for byte. No RNG and no model;
* :func:`controller_from_adapter` -- the **capability-gated optional loading seam**. It consults
  :mod:`strategy_game.capabilities` and never imports an optional adapter itself. An absent adapter
  yields ``None`` (the caller keeps its Null provider, so the game stays complete -- VISION §7a); a
  present one is refused explicitly, because building the Ollama/Concordia adapters is a later,
  author-gated step and this unit implements none of them.

Nothing here decides what a proposal *means*, what it costs, whether it succeeds, or whose turn it
is. ``strategy_game/RULEBOOK.md`` still says **NO RULES APPROVED**.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, cast, runtime_checkable

from .. import capabilities
from ..core import WorldState
from ..provenance import Provenance, ProvenanceKind
from .proposals import (
    AssignmentConflict,
    MoveProposal,
    ProposalError,
    UnauthorizedProposalError,
)


@runtime_checkable
class Controller(Protocol):
    """The one controller protocol a human, a script and (later) an LLM all conform to.

    Deliberately minimal, and deliberately *behavioural* rather than the signature-only seams in
    :mod:`strategy_game.ports`: a controller has an identity, knows whether it commands a given
    leader, and may declare at most one proposal for that leader. It returns a
    :class:`~strategy_game.controllers.proposals.MoveProposal` or nothing -- never a result, never a
    mutated state.
    """

    @property
    def controller_id(self) -> str:
        """Stable identity of this controller (never of the leaders it commands)."""
        ...

    def controls(self, leader_id: str) -> bool:
        """True when this controller is authorised to command ``leader_id``."""
        ...

    def propose(self, state: WorldState, *, leader_id: str) -> MoveProposal | None:
        """Declare a move for ``leader_id``, or ``None`` for no proposal."""
        ...


@dataclass(frozen=True)
class Assignment:
    """A controller and the leaders it commands. Data, not a rule."""

    controller_id: str
    leader_ids: tuple[str, ...] = ()


class ControllerRegistry:
    """Which controller commands which leader. Enforces *at most one* authoritative controller.

    This is the authorisation source the recorder consults. It is a boundary map, not a rulebook:
    it says who may speak for a piece, not what a piece may do.
    """

    def __init__(self) -> None:
        self._by_leader: dict[str, str] = {}

    def assign(self, controller_id: str, leader_id: str) -> None:
        """Assign ``leader_id`` to ``controller_id``. Re-assigning the same pair is a no-op."""
        controller_id = str(controller_id).strip()
        leader_id = str(leader_id).strip()
        if not controller_id:
            raise ProposalError("an assignment requires a controller_id")
        if not leader_id:
            raise ProposalError("an assignment requires a leader_id")
        existing = self._by_leader.get(leader_id)
        if existing is not None and existing != controller_id:
            raise AssignmentConflict(
                f"leader {leader_id!r} already has authoritative controller {existing!r}; "
                f"a leader has at most one"
            )
        self._by_leader[leader_id] = controller_id

    def controller_of(self, leader_id: str) -> str | None:
        return self._by_leader.get(str(leader_id).strip())

    def leaders_of(self, controller_id: str) -> tuple[str, ...]:
        return tuple(
            leader for leader, controller in self._by_leader.items() if controller == controller_id
        )

    def authorizes(self, controller_id: str, leader_id: str) -> bool:
        """True only when this exact controller owns this exact leader."""
        return self._by_leader.get(str(leader_id).strip()) == str(controller_id).strip()

    def authorize(self, controller_id: str, leader_id: str) -> None:
        """Raise :class:`UnauthorizedProposalError` unless ``controller_id`` commands ``leader_id``."""
        if not self.authorizes(controller_id, leader_id):
            owner = self.controller_of(leader_id)
            raise UnauthorizedProposalError(
                f"controller {controller_id!r} is not authorised for leader {leader_id!r} "
                f"(authoritative controller: {owner!r})"
            )

    @classmethod
    def from_assignments(cls, assignments: Iterable[Assignment]) -> "ControllerRegistry":
        registry = cls()
        for assignment in assignments:
            for leader_id in assignment.leader_ids:
                registry.assign(assignment.controller_id, leader_id)
        return registry

    def to_dict(self) -> dict[str, str]:
        return {leader: controller for leader, controller in sorted(self._by_leader.items())}


class NullAgentProvider:
    """The default controller: proposes nothing, commands nothing, needs no model.

    Its purpose is that the game is complete without it doing anything. Loading a scenario, taking a
    scripted turn and replaying a save all work with this as the only controller present.
    """

    def __init__(self, controller_id: str = "null") -> None:
        self._controller_id = str(controller_id)

    @property
    def controller_id(self) -> str:
        return self._controller_id

    def controls(self, leader_id: str) -> bool:
        return False

    def propose(self, state: WorldState, *, leader_id: str) -> MoveProposal | None:
        return None


@dataclass(frozen=True)
class ScriptedMove:
    """One line of a deterministic script: a declaration without identity or provenance.

    ``action_code`` is an open string here too: a script is free to say anything, because no action
    set is approved.
    """

    leader_id: str
    action_code: str = ""
    target_id: str = ""
    resources: tuple[str, ...] = ()
    rationale: str = ""


class ScriptedAgentProvider:
    """A deterministic, rule-free controller replaying a fixed script. No RNG, no model.

    Determinism is the whole point: two fresh instances driven through the same call sequence emit
    equal proposals, because the only mutable state is a per-leader cursor into the script. When a
    leader's lines are exhausted it proposes nothing.
    """

    def __init__(
        self,
        controller_id: str,
        script: Iterable[ScriptedMove] = (),
        *,
        default_action_code: str = "unspecified",
    ) -> None:
        self._controller_id = str(controller_id)
        self._script = tuple(script)
        self._default_action_code = str(default_action_code)
        self._cursor: dict[str, int] = {}

    @property
    def controller_id(self) -> str:
        return self._controller_id

    @property
    def script(self) -> tuple[ScriptedMove, ...]:
        return self._script

    def leaders(self) -> tuple[str, ...]:
        """The leaders this script writes orders for, in first-appearance order."""
        seen: list[str] = []
        for move in self._script:
            if move.leader_id not in seen:
                seen.append(move.leader_id)
        return tuple(seen)

    def controls(self, leader_id: str) -> bool:
        return str(leader_id) in self.leaders()

    def propose(self, state: WorldState, *, leader_id: str) -> MoveProposal | None:
        """The next scripted line for ``leader_id``, or ``None`` once the script is exhausted.

        ``state`` is accepted so a scripted controller is interchangeable with a human or an LLM one,
        and is deliberately unused: a scripted declaration does not depend on world state.
        """
        lines = [move for move in self._script if move.leader_id == str(leader_id)]
        index = self._cursor.get(str(leader_id), 0)
        if index >= len(lines):
            return None
        self._cursor[str(leader_id)] = index + 1
        move = lines[index]
        return MoveProposal(
            controller_id=self._controller_id,
            leader_id=move.leader_id,
            action_code=move.action_code or self._default_action_code,
            target_id=move.target_id,
            resources=move.resources,
            rationale=move.rationale,
            # A script is template-generated text, so its origin is stated rather than left unknown.
            provenance=Provenance(
                kind=ProvenanceKind.GENERATED, source=f"scripted:{self._controller_id}"
            ),
        )


#: The declared optional adapters a controller *could* one day be built from. A subset of
#: :data:`strategy_game.capabilities.OPTIONAL_ADAPTERS` -- the adapter seam is optional, so it must
#: never add a name to that set, only read from it.
CONTROLLER_ADAPTERS: tuple[str, ...] = ("ollama", "concordia")


class AdapterNotImplementedError(NotImplementedError):
    """Raised when an adapter-backed controller is asked for and the adapter is actually present.

    Present-but-unimplemented is refused on purpose: silently importing an adapter here would be how
    an unapproved runtime dependency enters the game.
    """


def available_controller_adapters() -> dict[str, bool]:
    """Availability of the adapters a controller may be built from, as data. Imports nothing."""
    return {name: capabilities.is_available(name) for name in CONTROLLER_ADAPTERS}


def controller_from_adapter(name: str, *, controller_id: str = "") -> Controller | None:
    """The capability-gated optional-loading seam: never a hard import.

    Returns ``None`` when the named adapter is **absent**, so the caller keeps its
    :class:`NullAgentProvider` and the game stays complete (VISION §7a: switching optional LLM
    support off must leave a *complete* game). Raises :class:`AdapterNotImplementedError` when the
    adapter is **present**, because this unit implements no Ollama/Concordia adapter -- that is a
    later, author-gated step. Raises :class:`ValueError` for an undeclared name, mirroring
    :func:`strategy_game.capabilities.require`.

    This function calls neither :func:`capabilities.require` nor any import: the adapter seam is
    *declared* here and *constructed* later.
    """
    if name not in capabilities.OPTIONAL_ADAPTERS:
        raise ValueError(f"{name!r} is not a declared optional adapter")
    if not capabilities.is_available(name):
        return None
    raise AdapterNotImplementedError(
        f"the {name!r} controller adapter is not implemented yet; building it is a later, "
        f"author-gated step and is not part of this unit"
    )


def default_controllers() -> tuple[Controller, ...]:
    """The controllers a model-free game starts with: one null provider, nothing else.

    A caller adds a scripted or (later) adapter-backed controller explicitly; the default must never
    require a model.
    """
    return (NullAgentProvider(),)


def registry_for(controllers: Iterable[Controller]) -> ControllerRegistry:
    """Build a registry from controllers that already know their own leaders.

    A :class:`ScriptedAgentProvider` declares its leaders from its script; a controller that cannot
    answer is skipped, so the caller stays in control of who commands whom.
    """
    registry = ControllerRegistry()
    for controller in controllers:
        declared = getattr(controller, "leaders", None)
        if not callable(declared):
            continue
        for leader_id in cast(Iterable[str], declared()):
            registry.assign(controller.controller_id, leader_id)
    return registry
