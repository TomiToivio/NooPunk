"""Framework-independent adapter contract: optional engines translate I/O only."""
from dataclasses import dataclass
from typing import Protocol
from .campaign import Game, Action, Outcome

class ActionAdapter(Protocol):
    def dispatch(self, command: str) -> Outcome: ...
    def available_actions(self) -> tuple[str, ...]: ...
    def save(self) -> str: ...

@dataclass
class LocalAdapter:
    """Simple adapter shared by console, tests and future framework wrappers."""
    game: Game

    def dispatch(self, command: str) -> Outcome:
        return self.game.apply(Action(command))

    def available_actions(self) -> tuple[str, ...]:
        return self.game.available_actions()

    def save(self) -> str:
        return self.game.to_json()

    @classmethod
    def load(cls, saved: str) -> "LocalAdapter":
        return cls(Game.from_json(saved))

    def snapshot(self) -> dict:
        """Copy of state for UI presentation, never the mutable domain object."""
        from dataclasses import asdict
        return asdict(self.game.state)
