"""Participant specifications for the Concordia runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from rules import AttributeSet


@dataclass(frozen=True, slots=True)
class GameMasterSpec:
    """Runtime identity for the GM, without GM procedures or hidden lore."""

    name: str = "placeholder_gm"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("GM name must not be empty.")


@dataclass(frozen=True, slots=True)
class LLMAgentSpec:
    """Runtime identity plus optional structured canonical attributes."""

    name: str
    attributes: AttributeSet | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Agent name must not be empty.")


@dataclass(slots=True)
class HumanPlayer:
    """Minimal adapter for an optional human-controlled player."""

    name: str = "placeholder_human"
    read_action: Callable[[str], str] = input
    attributes: AttributeSet | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Human player name must not be empty.")

    def choose_action(self, prompt: str) -> str:
        action = self.read_action(prompt).strip()
        if not action:
            raise ValueError("Human player action must not be empty.")
        return action
