"""Configuration for the NoöPunk Concordia runtime."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True, slots=True)
class ConcordiaRuntimeConfig:
    """Runtime-only configuration.

    No model identifier or generation setting is canonical NoöPunk content.
    """

    ollama_model: str
    ollama_base_url: str = "http://127.0.0.1:11434"
    temperature: float = 0.5
    top_p: float = 1.0
    top_k: int = 40

    @classmethod
    def from_env(cls) -> "ConcordiaRuntimeConfig":
        model = os.getenv("NOOPUNK_OLLAMA_MODEL", "").strip()
        if not model:
            raise ValueError(
                "NOOPUNK_OLLAMA_MODEL is required; no Ollama model is canonical."
            )
        return cls(
            ollama_model=model,
            ollama_base_url=os.getenv(
                "NOOPUNK_OLLAMA_BASE_URL", "http://127.0.0.1:11434"
            ).rstrip("/"),
            temperature=float(os.getenv("NOOPUNK_OLLAMA_TEMPERATURE", "0.5")),
            top_p=float(os.getenv("NOOPUNK_OLLAMA_TOP_P", "1.0")),
            top_k=int(os.getenv("NOOPUNK_OLLAMA_TOP_K", "40")),
        )
