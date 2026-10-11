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
