"""Reserved adapters: signatures only. No rules, actions or transitions."""
from __future__ import annotations

from typing import Protocol

from .core import WorldState


class LeaderRPG(Protocol):
    def describe(self, state: WorldState) -> object: ...


class PoliticalSimulation(Protocol):
    def describe(self, state: WorldState) -> object: ...


class FactionStrategy(Protocol):
    def describe(self, state: WorldState) -> object: ...


class AgentProvider(Protocol):
    def describe(self, state: WorldState) -> object: ...


class MapProvider(Protocol):
    """Reserved map/board port (see ``docs/INTEGRATION_BOUNDARIES.md``).

    Signature only. A map provider returns a portable visualization representation and must not
    infer borders, travel, control or ownership.
    """

    def describe(self, state: WorldState) -> object: ...


class AgentRunner(Protocol):
    """Reserved agent-runner port: runs an actor against a state (see #282).

    Named separately from ``AgentProvider`` because the issue lists "agent runners" as its own
    adapter boundary: a provider supplies an actor, a runner advances it. Signature only -- which
    layer uses one, and whether it is an LLM at all, stays open, and the scaffold never requires
    an LLM to load or view world state.
    """

    def describe(self, state: WorldState) -> object: ...
