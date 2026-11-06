"""Small baseline benchmark for the simulator (#1286).

This is a scaling check, not a performance promise. It reports wall time and
peak Python allocation for a ring of synthetic actors; the numbers belong in the
run note, not in a claim about real social systems.
"""

from __future__ import annotations

import time
import tracemalloc
from typing import Any

from .engine import SocialScienceSimulation
from .model import Actor, Claim, Material, Provenance, SimulationConfig, SocialEdge

__all__ = ["benchmark"]


def benchmark(*, actors: int = 200, turns: int = 10, seed: int = 1) -> dict[str, Any]:
    if actors < 2:
        raise ValueError("benchmark needs at least two actors")
    provenance = Provenance(
        Material.SYNTHESIZED, "fixture:benchmark", "benchmark-fixture"
    )
    sim = SocialScienceSimulation(config=SimulationConfig(seed=seed, turns=turns))
    for index in range(actors):
        sim.add_actor(
            Actor(
                f"actor.{index:04d}",
                f"Actor {index}",
                attention=0.5,
                provenance=provenance,
            )
        )
    for index in range(3):
        sim.add_claim(Claim(f"claim.{index}", f"Claim {index}", provenance=provenance))
    for index in range(actors):
        sim.add_social_edge(
            SocialEdge(
                f"actor.{index:04d}",
                f"actor.{(index + 1) % actors:04d}",
                "ring",
                0,
                provenance,
            )
        )
    tracemalloc.start()
    started = time.perf_counter()
    sim.run()
    elapsed = time.perf_counter() - started
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "actors": actors,
        "turns": turns,
        "events": len(sim.log.events),
        "seconds": round(elapsed, 4),
        "peak_kib": round(peak / 1024.0, 1),
        "seed": seed,
        "synthetic": True,
    }
