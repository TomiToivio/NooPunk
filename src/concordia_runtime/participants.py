"""Neutral participant specifications for the Concordia runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, slots=True)
class LLMAgentSpec:
    """Non-canonical runtime identity for an LLM-controlled participant."""

    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Agent name must not be empty.")


@dataclass(slots=True)
class HumanPlayer:
    """Minimal adapter for an optional human-controlled player."""

    name: str
    read_action: Callable[[str], str] = input

    def choose_action(self, prompt: str) -> str:
        action = self.read_action(prompt).strip()
        if not action:
            raise ValueError("Human player action must not be empty.")
        return action
