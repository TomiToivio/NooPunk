"""NoöPunk Strategy Game: separate, rule-free experimental package.

A scaffold only: data containers, reserved adapter protocols, serialization and a read-only view
model. It contains **no rules** — no statistics, thresholds, turn cadence, economy, dice,
strategic actions or win conditions. Optional adapters are declared in
:mod:`strategy_game.capabilities` and are never imported by loading or viewing world state.
"""
from .core import WorldState
from .provenance import Provenance, ProvenanceKind

__all__ = ["WorldState", "Provenance", "ProvenanceKind"]
