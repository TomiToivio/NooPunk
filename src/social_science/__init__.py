"""Standalone LaclauGPT social-science simulator (#1286).

This package deliberately does not import the NoöPunk RPG, CWN/SWN/AWN rules,
Evennia, Godot or campaign data. It consumes read-only AI26 canonical exports and
produces synthetic, provenance-labelled event traces and metrics.
"""

from .adapter import AdapterError, AI26Adapter, AI26Export
from .engine import DEFAULT_RULES, SimulationError, SocialScienceSimulation
from .events import EVENT_KINDS, EventLog, SimEvent
from .export import export_run, write_run
from .metrics import graph_metrics, simulation_metrics
from .model import (
    Actor,
    Articulation,
    Claim,
    CommunicationEdge,
    Material,
    Provenance,
    SimulationConfig,
    SocialEdge,
)
from .scenario import build_synthetic_scenario

__all__ = [
    "DEFAULT_RULES",
    "EVENT_KINDS",
    "AI26Adapter",
    "AI26Export",
    "Actor",
    "AdapterError",
    "Articulation",
    "Claim",
    "CommunicationEdge",
    "EventLog",
    "Material",
    "Provenance",
    "SimEvent",
    "SimulationConfig",
    "SimulationError",
    "SocialEdge",
    "SocialScienceSimulation",
    "build_synthetic_scenario",
    "export_run",
    "graph_metrics",
    "simulation_metrics",
    "write_run",
]
