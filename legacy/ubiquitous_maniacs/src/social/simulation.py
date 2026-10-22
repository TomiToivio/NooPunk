from __future__ import annotations

import copy
import random
from dataclasses import dataclass
from pathlib import Path
import json

import networkx as nx


def _clamp(value: int, low: int = -100, high: int = 100) -> int:
    return max(low, min(high, int(value)))


@dataclass(frozen=True)
class SocialResult:
    event_id: str
    summary: str
    changes: tuple[dict[str, object], ...]
    turn: int


class SocialSimulation:
    """Small, inspectable relationship simulation with no RPG dependencies."""

    def __init__(self, graph: nx.Graph, events: list[dict[str, object]], seed: int = 1):
        self.graph = graph
        self.events = {str(event["id"]): copy.deepcopy(event) for event in events}
        self.turn = 0
        self.history: list[dict[str, object]] = []
        self._rng = random.Random(seed)

    @classmethod
    def from_dict(cls, data: dict[str, object], seed: int = 1) -> "SocialSimulation":
        graph = nx.Graph(domain="social_simulation")
        for person in data.get("characters", []):
            record = dict(person)
            person_id = str(record.pop("id"))
            record.setdefault("traits", [])
            record.setdefault("mood", "neutral")
            record.setdefault("goals", [])
            record.setdefault("affiliations", [])
            record.setdefault("history", [])
            graph.add_node(person_id, **record)
        for relation in data.get("relationships", []):
            record = dict(relation)
            source = str(record.pop("source"))
            target = str(record.pop("target"))
            if source not in graph or target not in graph:
                raise ValueError(f"Unknown relationship endpoint: {source}, {target}")
            record["relationship"] = _clamp(record.get("relationship", 0))
            record.setdefault("history", [])
            graph.add_edge(source, target, **record)
        return cls(graph, list(data.get("events", [])), seed=seed)

    @classmethod
    def from_json(cls, path: str | Path, seed: int = 1) -> "SocialSimulation":
        with Path(path).open(encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle), seed=seed)

    def relationship(self, source: str, target: str) -> int:
        if not self.graph.has_edge(source, target):
            return 0
        return int(self.graph.edges[source, target].get("relationship", 0))

    def apply_event(self, event_id: str) -> SocialResult:
        if event_id not in self.events:
            raise KeyError(f"Unknown social event: {event_id}")
        event = self.events[event_id]
        self.turn += 1
        changes: list[dict[str, object]] = []
        for effect in event.get("effects", []):
            source, target = str(effect["source"]), str(effect["target"])
            if source not in self.graph or target not in self.graph:
                raise ValueError(f"Unknown event endpoint: {source}, {target}")
            if not self.graph.has_edge(source, target):
                self.graph.add_edge(source, target, relationship=0, history=[])
            edge = self.graph.edges[source, target]
            before = int(edge.get("relationship", 0))
            delta = int(effect.get("delta", 0))
            actor_traits = set(self.graph.nodes[source].get("traits", []))
            for trait, modifier in dict(effect.get("trait_modifiers", {})).items():
                if trait in actor_traits:
                    delta += int(modifier)
            after = _clamp(before + delta)
            edge["relationship"] = after
            entry = {"turn": self.turn, "event": event_id, "delta": after - before}
            edge.setdefault("history", []).append(entry)
            changes.append({"source": source, "target": target, "before": before, "after": after})
        for person_id, mood in dict(event.get("mood_updates", {})).items():
            if person_id not in self.graph:
                raise ValueError(f"Unknown mood target: {person_id}")
            self.graph.nodes[person_id]["mood"] = str(mood)
        summary = str(event.get("summary", event_id))
        log = {"turn": self.turn, "event_id": event_id, "summary": summary, "changes": changes}
        self.history.append(log)
        return SocialResult(event_id, summary, tuple(changes), self.turn)

    def auto_step(self) -> SocialResult:
        if not self.events:
            raise RuntimeError("No social events are available")
        return self.apply_event(self._rng.choice(sorted(self.events)))

    def snapshot(self) -> dict[str, object]:
        return {
            "turn": self.turn,
            "characters": [
                {"id": node_id, **copy.deepcopy(attrs)}
                for node_id, attrs in sorted(self.graph.nodes(data=True))
            ],
            "relationships": [
                {"source": source, "target": target, **copy.deepcopy(attrs)}
                for source, target, attrs in sorted(self.graph.edges(data=True))
            ],
            "history": copy.deepcopy(self.history),
        }

