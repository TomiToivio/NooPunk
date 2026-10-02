"""NoöPunk Concordia runtime adapters.

Canonical RPG rules remain in the shared rules package. Concordia consumes those
rules through deterministic adapters rather than asking an LLM to invent them.

The resolver seam (:mod:`resolver`) is the only path from agent output into the
simulation event log, per ``docs/SIMULATION_ARCHITECTURE_SPEC.md`` §7.4.
"""

from .config import ConcordiaRuntimeConfig
from .mechanics import resolve_structured_check, resolve_structured_opposed
from .participants import GameMasterSpec, HumanPlayer, LLMAgentSpec
from .providers import LanguageModelProvider, OllamaProvider
from .resolver import (
    UNRESOLVED_REASONS,
    Capability,
    Decision,
    ProposedAction,
    Resolution,
    ResolverSeam,
    resolve_proposal,
)
from .session import SessionSpec, build_concordia_config, build_simulation

__all__ = [
    "Capability",
    "ConcordiaRuntimeConfig",
    "Decision",
    "GameMasterSpec",
    "HumanPlayer",
    "LanguageModelProvider",
    "LLMAgentSpec",
    "OllamaProvider",
    "ProposedAction",
    "Resolution",
    "ResolverSeam",
    "SessionSpec",
    "UNRESOLVED_REASONS",
    "build_concordia_config",
    "build_simulation",
    "resolve_proposal",
    "resolve_structured_check",
    "resolve_structured_opposed",
]
