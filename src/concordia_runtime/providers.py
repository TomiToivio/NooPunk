"""Replaceable language-model providers for Concordia."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .config import ConcordiaRuntimeConfig


class LanguageModelProvider(Protocol):
    """Factory boundary for a Concordia-compatible language model."""

    def build(self) -> Any:
        """Return an object implementing Concordia's LanguageModel interface."""


@dataclass(frozen=True, slots=True)
class OllamaProvider:
    """Build Concordia's current native Ollama language-model adapter.

    Importing Concordia is deferred so the NoöPunk scaffold and unit tests can
    be inspected without installing the optional simulation dependencies.
    """

    config: ConcordiaRuntimeConfig

    def build(self) -> Any:
        try:
            from concordia.contrib.language_models.ollama import ollama_model
        except ImportError as exc:
            raise RuntimeError(
                "Concordia Ollama support is not installed. "
                "Install dependencies from requirements-concordia.txt."
            ) from exc

        # Concordia's current Ollama adapter uses ollama.Client(), whose host is
        # normally controlled through OLLAMA_HOST. Set it only for this build.
        import os

        previous = os.environ.get("OLLAMA_HOST")
        os.environ["OLLAMA_HOST"] = self.config.ollama_base_url
        try:
            return ollama_model.OllamaLanguageModel(
                model_name=self.config.ollama_model,
                system_message=(
                    "You are a runtime language model for a NoöPunk simulation. "
                    "Do not invent canonical rules or world facts. Use only the "
                    "context supplied by the simulation. Attribute values, dice "
                    "rolls, modifiers and check results are resolved in code and "
                    "supplied as structured state. You may describe or reason about "
                    "that state, but never invent a roll, value, modifier or alternate "
                    "mechanic, and never override a resolved result."
                ),
            )
        finally:
            if previous is None:
                os.environ.pop("OLLAMA_HOST", None)
            else:
                os.environ["OLLAMA_HOST"] = previous
