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
import sys as _sys

from . import interpreter as _interpreter

# The gate has to live here, at the top of the package, rather than in a `__main__`: running
# `python -m strategy_game.rpg` makes `runpy` import the package `strategy_game.rpg` first, and
# that package's `__init__` is what reaches `enum.StrEnum`. A check inside `__main__` would
# therefore never run on the interpreter that needs it. The message names the interpreter, the
# missing symbols and how to get a supported one, instead of a bare ImportError from deep inside
# the rules layer.
try:
    _interpreter.require()
except _interpreter.UnsupportedInterpreter as _exc:  # pragma: no cover - only on old interpreters
    print(_interpreter.message(_exc), file=_sys.stderr)
    raise SystemExit(2) from None

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
