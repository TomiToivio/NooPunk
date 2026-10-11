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
