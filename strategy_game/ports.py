"""Reserved adapters: signatures only. No rules, actions or transitions.

Each layer of the strategy game is independently swappable, and every protocol here is
`runtime_checkable` so a stub can be verified against it in a test without importing any
optional package. A protocol says *what a layer receives and returns*, never what it
decides — that is a rule, and rules need the author's gate (#282).

`describe` is deliberately the only method: the scaffold lets a layer read a
`WorldState` and hand back whatever representation it likes, while the scaffold itself
commits to no schema for that representation.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from .core import WorldState


@runtime_checkable
class LeaderRPG(Protocol):
    """Layer I: the faction leader's identity, traits and narrative."""

    def describe(self, state: WorldState) -> object: ...


@runtime_checkable
class PoliticalSimulation(Protocol):
    """Layer II: articulation, signifiers, frontiers, networks."""

    def describe(self, state: WorldState) -> object: ...


@runtime_checkable
class FactionStrategy(Protocol):
    """Layer III: assets, organisation, presence and strategic choice."""

    def describe(self, state: WorldState) -> object: ...


@runtime_checkable
class AgentProvider(Protocol):
    """An agent source for a layer (may be non-LLM)."""

    def describe(self, state: WorldState) -> object: ...


@runtime_checkable
class AgentRunner(Protocol):
    """Runs an agent against a state. Optional: no LLM is required to load or view state.

    Named separately from :class:`AgentProvider` because #282 asks for "agent runners"
    as an adapter boundary: a provider supplies an actor, a runner advances it. Which
    one a layer uses, and whether it is an LLM at all, stays open.
    """

    def describe(self, state: WorldState) -> object: ...


@runtime_checkable
class MapProvider(Protocol):
    """Supplies abstract board geometry — point locations and overlays.

    #282 asks for protocols covering "map providers" as well as the three layers. This
    one returns geometry only: the scaffold's view model stays map/network-neutral and
    no rendering engine is selected.
    """

    def describe(self, state: WorldState) -> object: ...
