"""The RPG layer's reserved adapters: the seam between the RPG and the strategy/simulation layer.

Issue #389 asks for *"a clean future adapter boundary to separate faction strategy/simulation, without
inventing that layer's mechanics"*. This module is that boundary and nothing more: **signatures only,
no rules, no actions, no transitions, no state**. It mirrors the convention of ``strategy_game/ports.py``
-- ``def name(...) -> ...: ...`` -- and it deliberately imports no strategy module, so the two layers
stay independent.

What this boundary is
---------------------

The RPG layer resolves *scenes*: a character acts, dice are rolled, an outcome is produced. The strategy
layer owns *factions, turns, leaders and political rules*. They meet at exactly four points, and only
these:

===========================================  ==========================================================
:class:`CharacterPort`                       the strategy layer asks for a character by id -- read-only
:class:`StrategyContextPort`                 the strategy layer supplies context for a leader -- read-only
:class:`ScenePort`                           the RPG layer runs one scene for a request and returns it
:class:`SceneConsumerPort`                   the strategy layer consumes the outcome as *declared* data
===========================================  ==========================================================

What may cross the boundary
---------------------------

Identifiers, declared read-only context, and outcome records. Nothing else.

What may not
------------

* **No strategy mechanic is defined here** -- not a turn economy, not a statistic, not a threshold, not
  a leader mission, not a win condition. #389 approves the Fate basis **for the RPG layer only**, and
  the strategy and political layers' mechanics remain pending. Declaring one here to make the seam look
  complete would be exactly the overreach the issue forbids.
* **No mutation.** A consumer reads an outcome; it does not write RPG state, and the RPG layer does not
  write strategy state. A scene outcome is a *declaration* until the owning layer decides what to do
  with it.
* **No hard dependency.** An implementation may be absent: the absence of an adapter is never a broken
  game, only a missing optional extension.

Adopting an adapter
-------------------

An implementation must satisfy the protocol structurally; nothing here registers, loads or imports one,
and no optional dependency is required to use this package.
"""

from __future__ import annotations

from typing import Protocol

__all__ = [
    "CharacterPort",
    "StrategyContextPort",
    "ScenePort",
    "SceneConsumerPort",
    "BOUNDARY_RULES",
]

#: The rules an adapter must respect. Declared as data so the contracts can assert them rather than
#: trusting that the docstring above was read.
BOUNDARY_RULES: tuple[str, ...] = (
    "the boundary defines no strategy, political or simulation mechanic",
    "data crossing the boundary is declared and read-only",
    "an adapter may be absent, and its absence is not a broken game",
    "an adapter never mutates the other layer's state",
    "no optional dependency is required to import this module",
)


class CharacterPort(Protocol):
    """Read-only access to one character sheet, by id. Owned by the RPG layer."""

    def sheet(self, character_id: str) -> object: ...


class StrategyContextPort(Protocol):
    """Read-only context the strategy layer supplies for a leader, by id.

    The strategy layer decides what is in a context and when a scene happens; this boundary only
    carries it. Which political facts exist is deliberately not specified here.
    """

    def context_for(self, leader_id: str) -> object: ...


class ScenePort(Protocol):
    """The seam the strategy layer calls: run one RPG scene and return its outcome record."""

    def run_scene(self, request: object) -> object: ...


class SceneConsumerPort(Protocol):
    """How the strategy layer takes an outcome: as declared data, never as a mutation."""

    def consume(self, outcome: object) -> object: ...
