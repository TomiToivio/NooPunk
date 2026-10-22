"""Social simulation demo for Noöpunk: Ubiquitous Maniacs.

Standalone microscale network-society simulator. Not integrated with RPG.

Public API:
    sim = SocialSimulation.from_lab_data(people_csv, relationships_csv)
    sim.step()                         # advance one tick
    sim.interact(a, b, action)         # player-triggered interaction
    sim.state()                        # inspectable graph state
    sim.history()                      # event log
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import networkx as nx

REL_MIN = -100
REL_MAX = 100


def _clamp(value: int) -> int:
    return max(REL_MIN, min(REL_MAX, value))


@dataclass
class Character:
    id: str
    name: str
    role: str
    traits: list[str] = field(default_factory=list)
    mood: str = "neutral"
    goals: list[str] = field(default_factory=list)
    affiliations: list[str] = field(default_factory=list)


@dataclass
class SocialEvent:
    tick: int
    type: str
    source: str
    target: str
    action: str
    delta: int
    description: str


# ── Actions ─────────────────────────────────────────────────────

ACTIONS: dict[str, dict[str, Any]] = {
    "small_talk":    {"delta": +2,  "spread": 0, "desc": "Kevyt juttelu. Pieni tuttunuuden lisäys."},
    "deep_convo":    {"delta": +5,  "spread": 1, "desc": "Syvällinen keskustelu. Suurempi luottamuksen kasvu."},
    "share_secret":  {"delta": +10, "spread": 1, "desc": "Salaisuuden jakaminen. Suuri luottamuksen kasvu, mutta riski."},
    "insult":        {"delta": -10, "spread": 2, "desc": " loukkaaminen. Suuri suhteen heikkeneminen."},
    "betray":        {"delta": -25, "spread": 3, "desc": "Petos. Suuri suhteen tuho, leviää laajalle."},
    "help":          {"delta": +8,  "spread": 1, "desc": "Auta toista. Luottamuksen kasvu."},
    "ignore":        {"delta": -3,  "spread": 0, "desc": "Sivuuttaminen. Pieni suhteen heikkeneminen."},
    "flirt":         {"delta": +4,  "spread": 0, "desc": "Flirttailu. Pieni vetovoiman lisäys."},
    "argument":      {"delta": -7,  "spread": 1, "desc": "Väittely. Suhteen heikkeneminen."},
    "reconcile":     {"delta": +6,  "spread": 1, "desc": "Sovinto. Suhteen paraneminen konfliktin jälkeen."},
}

# Spread = how many other characters are affected (gossip effect)
# Positive spread = good reputation spreads, negative = bad reputation spreads


@dataclass
class SocialSimulation:
    graph: nx.Graph
    characters: dict[str, Character]
    _tick: int = 0
    _events: list[SocialEvent] = field(default_factory=list)

    @classmethod
    def from_lab_data(
        cls,
        people_records: list[dict[str, object]],
        relationship_records: list[dict[str, object]],
    ) -> SocialSimulation:
        """Build from existing CSV-loaded lab data."""
        graph = nx.Graph()
        graph.graph["domain"] = "social_sim"
        characters: dict[str, Character] = {}

        for person in people_records:
            cid = str(person["id"])
            char = Character(
                id=cid,
                name=str(person["name"]),
                role=str(person["role"]),
            )
            characters[cid] = char
            graph.add_node(cid, name=char.name, role=char.role, mood=char.mood)

        for rel in relationship_records:
            source = str(rel["source"])
            target = str(rel["target"])
            # Scale existing -5..+5 to -100..+100
            raw = int(str(rel["relationship"]))
            scaled = raw * 20
            graph.add_edge(source, target, relationship=_clamp(scaled))

        return cls(graph=graph, characters=characters)

    def step(self) -> list[SocialEvent]:
        """Advance one simulation tick. Generates ambient social dynamics."""
        self._tick += 1
        new_events: list[SocialEvent] = []

        # Ambient drift: relationships slowly decay toward 0
        for source, target, data in list(self.graph.edges(data=True)):
            current = data["relationship"]
            if abs(current) > 5:
                drift = 1 if current > 0 else -1
                new_val = _clamp(current - drift)
                self.graph[source][target]["relationship"] = new_val

        # Mood-based ambient interactions (simple probabilistic)
        import random
        edges = list(self.graph.edges(data=True))
        if edges:
            source, target, _ = random.choice(edges)
            action_name = random.choice(list(ACTIONS.keys()))
            events = self._apply_action(source, target, action_name)
            new_events.extend(events)

        self._events.extend(new_events)
        return new_events

    def interact(self, source: str, target: str, action: str) -> list[SocialEvent]:
        """Player-triggered interaction between two characters."""
        if source not in self.characters:
            raise KeyError(f"Unknown character: {source}")
        if target not in self.characters:
            raise KeyError(f"Unknown character: {target}")
        if action not in ACTIONS:
            raise KeyError(f"Unknown action: {action}")
        if source == target:
            raise ValueError("Cannot interact with self")

        events = self._apply_action(source, target, action)
        self._events.extend(events)
        return events

    def _apply_action(self, source: str, target: str, action_name: str) -> list[SocialEvent]:
        action_def = ACTIONS[action_name]
        delta = action_def["delta"]
        spread = action_def["spread"]
        desc = action_def["desc"]

        events: list[SocialEvent] = []

        # Ensure edge exists
        if not self.graph.has_edge(source, target):
            self.graph.add_edge(source, target, relationship=0)

        # Apply direct delta
        current = self.graph[source][target]["relationship"]
        new_val = _clamp(current + delta)
        self.graph[source][target]["relationship"] = new_val

        events.append(SocialEvent(
            tick=self._tick, type="interaction", source=source, target=target,
            action=action_name, delta=delta, description=desc,
        ))

        # Spread effect (gossip/reputation)
        if spread > 0:
            neighbors = [n for n in self.graph.neighbors(target) if n != source]
            import random
            spread_targets = random.sample(neighbors, min(spread, len(neighbors))) if neighbors else []
            for n in spread_targets:
                if not self.graph.has_edge(source, n):
                    self.graph.add_edge(source, n, relationship=0)
                spread_delta = delta // 3  # weaker spread
                n_current = self.graph[source][n]["relationship"]
                n_new = _clamp(n_current + spread_delta)
                self.graph[source][n]["relationship"] = n_new
                events.append(SocialEvent(
                    tick=self._tick, type="spread", source=source, target=n,
                    action=f"gossip_from_{target}", delta=spread_delta,
                    description=f"Reputaatio leviaa: {desc}",
                ))

        return events

    def state(self) -> dict[str, Any]:
        """Return inspectable graph state."""
        return {
            "tick": self._tick,
            "characters": [
                {"id": c.id, "name": c.name, "role": c.role, "mood": c.mood}
                for c in self.characters.values()
            ],
            "relationships": [
                {"source": s, "target": t, "relationship": d["relationship"]}
                for s, t, d in sorted(self.graph.edges(data=True))
            ],
            "available_actions": list(ACTIONS.keys()),
        }

    def history(self) -> list[dict[str, Any]]:
        """Return event log."""
        return [
            {
                "tick": e.tick, "type": e.type, "source": e.source,
                "target": e.target, "action": e.action,
                "delta": e.delta, "description": e.description,
            }
            for e in self._events
        ]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the complete live simulation state."""
        return {
            "tick": self._tick,
            "characters": [vars(character).copy() for character in self.characters.values()],
            "relationships": [
                {"source": source, "target": target, **dict(attrs)}
                for source, target, attrs in self.graph.edges(data=True)
            ],
            "events": self.history(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SocialSimulation:
        """Restore and validate a simulation produced by :meth:`to_dict`."""
        if not isinstance(data, dict):
            raise TypeError("Social save must be an object")
        raw_characters = data.get("characters")
        raw_relationships = data.get("relationships")
        raw_events = data.get("events", [])
        if not isinstance(raw_characters, list) or not isinstance(raw_relationships, list):
            raise TypeError("Social save requires character and relationship lists")
        if not isinstance(raw_events, list):
            raise TypeError("Social event history must be a list")

        graph = nx.Graph(domain="social_sim")
        characters: dict[str, Character] = {}
        for raw in raw_characters:
            if not isinstance(raw, dict):
                raise TypeError("Social character must be an object")
            character = Character(
                id=str(raw["id"]), name=str(raw["name"]), role=str(raw["role"]),
                traits=[str(value) for value in raw.get("traits", [])],
                mood=str(raw.get("mood", "neutral")),
                goals=[str(value) for value in raw.get("goals", [])],
                affiliations=[str(value) for value in raw.get("affiliations", [])],
            )
            if character.id in characters:
                raise ValueError(f"Duplicate social character: {character.id}")
            characters[character.id] = character
            graph.add_node(character.id, name=character.name, role=character.role, mood=character.mood)

        for raw in raw_relationships:
            if not isinstance(raw, dict):
                raise TypeError("Social relationship must be an object")
            source, target = str(raw["source"]), str(raw["target"])
            if source not in characters or target not in characters:
                raise ValueError(f"Unknown social relationship endpoint: {source}, {target}")
            relationship = int(raw["relationship"])
            if not REL_MIN <= relationship <= REL_MAX:
                raise ValueError("Social relationship is outside the supported range")
            graph.add_edge(source, target, relationship=relationship)

        events = []
        for raw in raw_events:
            if not isinstance(raw, dict):
                raise TypeError("Social event must be an object")
            events.append(SocialEvent(
                tick=int(raw["tick"]), type=str(raw["type"]), source=str(raw["source"]),
                target=str(raw["target"]), action=str(raw["action"]), delta=int(raw["delta"]),
                description=str(raw["description"]),
            ))
        tick = int(data.get("tick", 0))
        if tick < 0:
            raise ValueError("Social tick cannot be negative")
        return cls(graph=graph, characters=characters, _tick=tick, _events=events)

    def get_relationship(self, a: str, b: str) -> int:
        """Get relationship value between two characters (0 if no edge)."""
        if self.graph.has_edge(a, b):
            return self.graph[a][b]["relationship"]
        return 0
