"""NoöPunk Concordia runtime adapters.

This package contains infrastructure only. Canonical RPG rules and world data
must remain outside the Concordia-specific runtime.
"""

from .config import ConcordiaRuntimeConfig
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
]
