"""Controller / MoveProposal boundary for the NoöPunk × LaclauGPT crossover (issue #304, step 1).

This subpackage is the **proposal-side structure** of the #304 turn architecture and nothing more.
It gives the game an engine-independent way to *declare* moves and *record* them, so a scripted round
is playable and loadable with **no model provider present at all** -- while never resolving anything.

Read this first, because it is the whole boundary:

* A :class:`MoveProposal` is a **declaration** by a controller for one leader. It carries identity,
  an open-string action code, a declared target, declared resource names and free text -- and it
  carries **no result**. ``leader_id`` is required; ``provenance`` defaults to ``UNKNOWN``.
* A :class:`ProposalRecorder` **stores proposals as data only**. It is never given a
  :class:`~strategy_game.core.WorldState`, so recording cannot change authoritative state -- the
  recorder has no handle on it. Reading and replaying the log imports nothing optional.
* The :class:`Controller` protocol is the *real* boundary behind the signature-only
  ``ports.AgentProvider``/``AgentRunner`` seams. :class:`NullAgentProvider` proposes nothing;
  :class:`ScriptedAgentProvider` is deterministic; an LLM controller and a human controller answer
  the same two questions, so the recorder cannot prefer either.
* :func:`controller_from_adapter` is the only optional-loading seam, and it consults
  :mod:`strategy_game.capabilities` -- it never hard-imports ollama or concordia.

Deliberately **absent**: resolution, thresholds, an approved action set, a GM intervention menu,
hidden-information rules and multiplayer transport. See
:data:`strategy_game.controllers.proposals.PENDING_AUTHOR_RULINGS` for the list and the reason each
one needs an author ruling rather than an agent's choice.

The public API of this subpackage is its own: :attr:`strategy_game.__all__` and the CI-pinned key set
of ``python -m strategy_game`` are **untouched** (the same pattern ``tabletop/`` used for #282/#347).
"""
from .controllers import (
    AdapterNotImplementedError,
    Assignment,
    CONTROLLER_ADAPTERS,
    Controller,
    ControllerRegistry,
    NullAgentProvider,
    ScriptedAgentProvider,
    ScriptedMove,
    available_controller_adapters,
    controller_from_adapter,
    default_controllers,
    registry_for,
)
from .proposals import (
    APPROVED_ACTION_CODES,
    PENDING_AUTHOR_RULINGS,
    AssignmentConflict,
    MoveProposal,
    ProposalError,
    ProposalLog,
    ProposalRecorder,
    UnauthorizedProposalError,
)

__all__ = [
    # proposals
    "APPROVED_ACTION_CODES",
    "PENDING_AUTHOR_RULINGS",
    "AssignmentConflict",
    "MoveProposal",
    "ProposalError",
    "ProposalLog",
    "ProposalRecorder",
    "UnauthorizedProposalError",
    # controllers
    "AdapterNotImplementedError",
    "Assignment",
    "CONTROLLER_ADAPTERS",
    "Controller",
    "ControllerRegistry",
    "NullAgentProvider",
    "ScriptedAgentProvider",
    "ScriptedMove",
    "available_controller_adapters",
    "controller_from_adapter",
    "default_controllers",
    "registry_for",
]
