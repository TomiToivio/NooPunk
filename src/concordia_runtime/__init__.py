"""NoöPunk Concordia runtime adapters.

Canonical RPG rules remain in the shared rules package. Concordia consumes those
rules through deterministic adapters rather than asking an LLM to invent them.
"""

from .config import ConcordiaRuntimeConfig
from .mechanics import resolve_structured_check, resolve_structured_opposed
from .participants import GameMasterSpec, HumanPlayer, LLMAgentSpec
from .providers import LanguageModelProvider, OllamaProvider
from .session import SessionSpec, build_concordia_config, build_simulation

__all__ = [
    "ConcordiaRuntimeConfig",
    "GameMasterSpec",
    "HumanPlayer",
    "LanguageModelProvider",
    "LLMAgentSpec",
    "OllamaProvider",
    "SessionSpec",
    "build_concordia_config",
    "build_simulation",
    "resolve_structured_check",
    "resolve_structured_opposed",
]
