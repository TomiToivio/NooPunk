"""Portable exports for a social-science run (#1286).

The export keeps observed/inferred/synthesized/simulated labels attached to each
record and includes a run manifest with the rule text and parameters. It is a
JSON document a researcher can inspect without the Python package.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .engine import DEFAULT_RULES, SocialScienceSimulation
from .metrics import simulation_metrics

__all__ = ["export_run", "write_run"]


def export_run(simulation: SocialScienceSimulation) -> dict[str, Any]:
    """Return a JSON-compatible run document; never mutates the simulation."""
    return {
        "format": "noopunk.social_science.run",
        "version": 1,
        "manifest": {
            "simulation_format": "noopunk.social_science.simulation",
            "seed": simulation.config.seed,
            "turns": simulation.turn,
            "config": simulation.config.to_dict(),
            "rules": dict(DEFAULT_RULES),
            "digest": simulation.digest(),
            "provenance_note": (
                "Synthetic simulation output. Observed and inferred source records are labelled "
                "separately; no value here is an empirical finding or a prediction."
            ),
        },
        "actors": [
            actor.to_dict()
            for actor in sorted(simulation.actors.values(), key=lambda a: a.id)
        ],
        "claims": [
            claim.to_dict()
            for claim in sorted(simulation.claims.values(), key=lambda c: c.id)
        ],
        "articulations": [
            item.to_dict()
            for item in sorted(simulation.articulations.values(), key=lambda a: a.id)
        ],
        "social_edges": [edge.to_dict() for edge in simulation.social_edges],
        "communication_edges": [
            edge.to_dict() for edge in simulation.communication_edges
        ],
        "events": simulation.log.to_dicts(),
        "metrics": simulation_metrics(simulation),
    }


def write_run(path: str | Path, simulation: SocialScienceSimulation) -> Path:
    """Write a stable, sorted JSON export and return the path."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(export_run(simulation), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    return target
