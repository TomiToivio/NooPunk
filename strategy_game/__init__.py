"""NoöPunk Strategy Game: separate, rule-free experimental package.

A scaffold only: data containers, reserved adapter protocols, serialization and a read-only view
model. It contains **no rules** — no statistics, thresholds, turn cadence, economy, dice,
strategic actions or win conditions. Optional adapters are declared in
:mod:`strategy_game.capabilities` and are never imported by loading or viewing world state.

Layer II (political simulation) adds an abstract vocabulary in :mod:`strategy_game.political`:
Laclau/Mouffe demands, signifiers and their roles, articulations and frontiers, plus Castells'
communicative modes. It is containers only too, it imports no LaclauGPT, and its proposed play loop
is unapproved (``docs/POLITICAL_SIMULATION_DESIGN.md``).
"""
from .core import WorldState
from .political import PoliticalField, PowerMode, SignifierRole
from .provenance import Provenance, ProvenanceKind

__all__ = [
    "WorldState",
    "Provenance",
    "ProvenanceKind",
    "PoliticalField",
    "SignifierRole",
    "PowerMode",
]
