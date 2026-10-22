"""Small social state used by scenes and the autonomous graph simulator."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import GraphEffect


@dataclass
class Relationship:
    source: str
    target: str
    values: dict[str, int] = field(default_factory=dict)
    history: list[str] = field(default_factory=list)

    def change(self, dimension: str, delta: int, reason: str = "") -> GraphEffect:
        old_value = self.values.get(dimension, 0)
        new_value = max(-100, min(100, old_value + delta))
        applied_delta = new_value - old_value
        self.values[dimension] = new_value
        if reason:
            self.history.append(reason)
        return GraphEffect(
            "social", "adjust_edge", self.source, self.target, dimension, applied_delta
        )
