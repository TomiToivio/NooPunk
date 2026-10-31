"""The simulation bridge: Mesa summarises, the world decides (#946).

A population simulation is a good way to discover that a district is running out of food. It is a bad way to
decide that a player's character is dead. This module keeps that line: the simulation emits `SimEvent`s, and
`reconcile()` turns them into ordinary, clamped world events that the authoritative state applies (or
refuses) like any other.

Mesa is optional. `LocalSimulation` is a small, dependency-free population loop so the pipeline can be tested
and played before the Mesa dependency exists — and if Mesa is installed later, it only has to produce the same
`SimEvent`s.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Protocol, runtime_checkable


@dataclass(frozen=True)
class SimEvent:
    """One summary line from the simulation. Deliberately narrow: no player state, only world pressure."""

    actor: str            # faction id
    resource: str
    delta: int
    reason: str = ""
    tick: int = 0


@runtime_checkable
class Simulation(Protocol):
    def step(self) -> list[SimEvent]:  # pragma: no cover - protocol
        ...


class LocalSimulation:
    """A tiny scarcity loop: rations shrink, population pressure pushes back.

    No randomness, so a test can assert exact numbers; the Mesa version may randomise, and that is fine because
    it only produces SimEvents.
    """

    def __init__(self, population: int = 12, consumption_per_tick: int = 1) -> None:
        self.population = population
        self.consumption_per_tick = consumption_per_tick
        self.tick = 0

    def step(self) -> list[SimEvent]:
        self.tick += 1
        return [SimEvent(actor="unsa", resource="rations",
                         delta=-self.consumption_per_tick,
                         reason=f"{self.population} people ate", tick=self.tick)]


def reconcile(events: Iterable[SimEvent], apply_event) -> dict[str, Any]:
    """Turn simulation events into world events, one per event, capped and attributed.

    Returns a summary rather than a mutation: the caller can log how much the simulation actually changed, and
    a refused event is reported instead of being retried until it works.
    """
    applied: list[dict[str, Any]] = []
    refused: list[dict[str, Any]] = []
    for index, sim in enumerate(events):
        if not -3 <= sim.delta <= 3:
            refused.append({"actor": sim.actor, "resource": sim.resource, "delta": sim.delta,
                            "reason": "delta outside the permitted range"})
            continue
        event = {
            "id": f"sim-{sim.tick}-{sim.actor}-{sim.resource}-{index}",
            "type": "sim_reconcile",
            "faction": sim.actor,
            "resource": sim.resource,
            "delta": sim.delta,
            "source": "simulation",
            "reason": sim.reason,
        }
        try:
            applied.append(apply_event(event))
        except ValueError as error:
            refused.append({"actor": sim.actor, "resource": sim.resource, "delta": sim.delta,
                            "reason": str(error)})
    return {"applied": len(applied), "refused": len(refused),
            "refusals": refused, "records": applied}
