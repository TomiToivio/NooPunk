"""Moniulotteinen sosiaalinen suhdeverkko Noöpunk: Ubiquitous Maniacs -peliin.

Jokainen suhde on suunnattu kaari (A -> B) ja tallentaa kuusi dimension:

  trust        — luottamus: uskallatko kääntää selkäsi?
  attraction   — vetovoima: haluatko olla lähellä?
  fear         — pelko: mitä tapahtuu jos hän päättää olevansa vaarallinen?
  suspicion    — epäily: onko hänellä piilotettuja motiiveja?
  authority    — auktoriteetti: kuka käskee ketä C.G. Jung -instituutissa?
  familiarity  — tuttunuus: kuinka hyvin tunnet hänet — vai luuletko tuntevasi?

Dimensiot on inspiroitu Jungilaisesta psykologiasta ja Castellsin
verkostoyhteiskunnasta: jokainen suhde on voimasuhde, joka voi olla
symmetrinen tai epäsymmetrinen, tietoinen tai alitajunta.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import networkx as nx


RELATIONSHIP_DIMENSIONS = (
    "trust",
    "attraction",
    "fear",
    "suspicion",
    "authority",
    "familiarity",
)

MIN_VAL = -100
MAX_VAL = 100


def _clamp(value: int) -> int:
    return max(MIN_VAL, min(MAX_VAL, int(value)))


@dataclass
class RelationshipDimensions:
    """Suunnattu suhde yhdestä hahmosta toiseen — kuusi dimensiota."""

    trust: int = 0
    attraction: int = 0
    fear: int = 0
    suspicion: int = 0
    authority: int = 0
    familiarity: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "trust": self.trust,
            "attraction": self.attraction,
            "fear": self.fear,
            "suspicion": self.suspicion,
            "authority": self.authority,
            "familiarity": self.familiarity,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RelationshipDimensions:
        return cls(
            trust=_clamp(data.get("trust", 0)),
            attraction=_clamp(data.get("attraction", 0)),
            fear=_clamp(data.get("fear", 0)),
            suspicion=_clamp(data.get("suspicion", 0)),
            authority=_clamp(data.get("authority", 0)),
            familiarity=_clamp(data.get("familiarity", 0)),
        )


@dataclass
class ChangeRecord:
    """Yksi suhdemuutos historiaan."""

    turn: int
    source: str
    target: str
    dimension: str
    delta: int
    new_value: int
    reason: str = ""


@dataclass(frozen=True)
class NPCMemory:
    """A compact, save-safe recollection owned by one social-graph character."""

    turn: int
    scene: str
    interaction: str
    actor: str
    summary: str
    valence: int = 0
    tags: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "scene": self.scene,
            "interaction": self.interaction,
            "actor": self.actor,
            "summary": self.summary,
            "valence": self.valence,
            "tags": sorted(set(self.tags)),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | str) -> NPCMemory:
        if isinstance(data, str):
            return cls(0, "", "", "", data, tags=("legacy",))
        if not isinstance(data, dict):
            raise TypeError("NPC memory must be an object")
        summary = str(data.get("summary", "")).strip()
        if not summary:
            raise ValueError("NPC memory requires a summary")
        return cls(
            turn=max(0, int(data.get("turn", 0))),
            scene=str(data.get("scene", "")),
            interaction=str(data.get("interaction", "")),
            actor=str(data.get("actor", "")),
            summary=summary,
            valence=_clamp(data.get("valence", 0)),
            tags=tuple(sorted({str(tag) for tag in data.get("tags", [])})),
        )


class MultiDimensionalSocialGraph:
    """Suunnattu moniulotteinen suhdeverkko.

    Kaaret kulkevat lähdestä kohteeseen ja tallentavat kuusi
    suhdeulottuvuutta. Jokainen hahmo on solmu, jolla on nimi, rooli,
    tavoitteet, mieliala ja muisti.
    """

    def __init__(self, seed: int | None = None) -> None:
        self.graph: nx.DiGraph = nx.DiGraph()
        self.turn: int = 0
        self.history: list[ChangeRecord] = []
        self._hidden_edges: set[tuple[str, str]] = set()
        # Seeded RNG so NPC reactions and any stochastic social ticks are
        # deterministic across save/load and replays (spec: deterministic seed).
        self.rng: random.Random = random.Random(seed)

    def add_character(
        self,
        character_id: str,
        name: str,
        role: str = "",
        goals: list[str] | None = None,
        mood: str = "neutral",
        memory: list[str] | None = None,
    ) -> None:
        self.graph.add_node(
            character_id,
            name=name,
            role=role,
            goals=goals or [],
            mood=mood,
            memory=memory or [],
        )

    def set_relationship(
        self,
        source: str,
        target: str,
        dimensions: dict[str, int] | None = None,
        hidden: bool = False,
    ) -> None:
        if source not in self.graph or target not in self.graph:
            raise KeyError(f"Unknown character: {source} or {target}")
        if source == target:
            raise ValueError("Cannot have a relationship with self")
        dims = dimensions or {}
        # Merge into an existing edge rather than silently overwriting it:
        # only the dimensions explicitly passed are written; others are
        # preserved. This lets a hidden "deeper truth" layer (e.g. Ragnarök's
        # true assessment) augment a visible edge without erasing it.
        if self.graph.has_edge(source, target):
            edge = self.graph[source][target]
            for dim in RELATIONSHIP_DIMENSIONS:
                if dim in dims:
                    edge[dim] = _clamp(dims[dim])
        else:
            self.graph.add_edge(source, target, **RelationshipDimensions.from_dict(dims).to_dict())
        if hidden:
            self._hidden_edges.add((source, target))

    def change_relationship(
        self,
        source: str,
        target: str,
        dimension: str,
        delta: int,
        reason: str = "",
    ) -> ChangeRecord:
        if dimension not in RELATIONSHIP_DIMENSIONS:
            raise ValueError(f"Unknown dimension: {dimension}")
        if source not in self.graph or target not in self.graph:
            raise KeyError(f"Unknown character: {source} or {target}")
        if not self.graph.has_edge(source, target):
            self.graph.add_edge(source, target, **RelationshipDimensions().to_dict())

        old_val = self.graph[source][target].get(dimension, 0)
        new_val = _clamp(old_val + delta)
        actual_delta = new_val - old_val
        self.graph[source][target][dimension] = new_val

        record = ChangeRecord(
            turn=self.turn,
            source=source,
            target=target,
            dimension=dimension,
            delta=actual_delta,
            new_value=new_val,
            reason=reason,
        )
        self.history.append(record)
        return record

    def get_relationship(self, source: str, target: str) -> RelationshipDimensions:
        if not self.graph.has_edge(source, target):
            return RelationshipDimensions()
        data = self.graph[source][target]
        return RelationshipDimensions(
            trust=data.get("trust", 0),
            attraction=data.get("attraction", 0),
            fear=data.get("fear", 0),
            suspicion=data.get("suspicion", 0),
            authority=data.get("authority", 0),
            familiarity=data.get("familiarity", 0),
        )

    def is_hidden(self, source: str, target: str) -> bool:
        return (source, target) in self._hidden_edges

    def reveal_edge(self, source: str, target: str) -> None:
        self._hidden_edges.discard((source, target))

    @property
    def hidden_edge_count(self) -> int:
        return len(self._hidden_edges)

    def known_characters(self, observer: str | None = None) -> list[dict[str, Any]]:
        """Listaa hahmot jotka näkyvät tarkkailijalle (kaikki jos observer=None)."""
        result = []
        for node_id, data in sorted(self.graph.nodes(data=True)):
            result.append({
                "id": node_id,
                "name": data.get("name", node_id),
                "role": data.get("role", ""),
                "mood": data.get("mood", "neutral"),
            })
        return result

    def visible_relationships(self, observer: str | None = None) -> list[dict[str, Any]]:
        """Listaa suhteet jotka näkyvät tarkkailijalle. Piilokaaret näkyvät vain jos observer=None."""
        result = []
        for source, target, data in sorted(self.graph.edges(data=True)):
            if observer is not None and (source, target) in self._hidden_edges:
                continue
            result.append({
                "source": source,
                "target": target,
                **RelationshipDimensions.from_dict(data).to_dict(),
                "hidden": (source, target) in self._hidden_edges,
            })
        return result

    def recent_changes(self, n: int = 10) -> list[dict[str, Any]]:
        """Palauta N viimeisintä suhdemuutosta."""
        return [
            {
                "turn": r.turn,
                "source": r.source,
                "target": r.target,
                "dimension": r.dimension,
                "delta": r.delta,
                "new_value": r.new_value,
                "reason": r.reason,
            }
            for r in self.history[-n:]
        ]

    def advance_turn(self) -> None:
        self.turn += 1

    def remember(self, character_id: str, memory: NPCMemory) -> bool:
        """Store one recollection, deduplicated by its narrative origin."""
        if character_id not in self.graph:
            raise KeyError(f"Unknown character: {character_id}")
        memories = self.graph.nodes[character_id].setdefault("memory", [])
        restored = [NPCMemory.from_dict(item) for item in memories]
        key = (memory.scene, memory.interaction, memory.actor)
        if any((item.scene, item.interaction, item.actor) == key for item in restored):
            return False
        memories.append(memory.to_dict())
        del memories[:-50]
        return True

    def memories(self, character_id: str, limit: int | None = None) -> list[dict[str, Any]]:
        """Return newest memories first without exposing mutable graph storage."""
        if character_id not in self.graph:
            raise KeyError(f"Unknown character: {character_id}")
        items = [
            NPCMemory.from_dict(item).to_dict()
            for item in self.graph.nodes[character_id].get("memory", [])
        ]
        items.reverse()
        return items if limit is None else items[:max(0, int(limit))]

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "characters": [
                {"id": n, **dict(d)} for n, d in sorted(self.graph.nodes(data=True))
            ],
            "relationships": [
                {"source": s, "target": t, **RelationshipDimensions.from_dict(d).to_dict(),
                 "hidden": (s, t) in self._hidden_edges}
                for s, t, d in sorted(self.graph.edges(data=True))
            ],
            "hidden_edges": [list(e) for e in sorted(self._hidden_edges)],
            "history": [
                {"turn": r.turn, "source": r.source, "target": r.target,
                 "dimension": r.dimension, "delta": r.delta, "new_value": r.new_value,
                 "reason": r.reason}
                for r in self.history
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], seed: int | None = None) -> MultiDimensionalSocialGraph:
        graph = cls(seed=seed)
        graph.turn = data.get("turn", 0)
        for char in data.get("characters", []):
            memories = [NPCMemory.from_dict(item).to_dict() for item in char.get("memory", [])]
            graph.add_character(
                char["id"],
                char.get("name", char["id"]),
                char.get("role", ""),
                char.get("goals", []),
                char.get("mood", "neutral"),
                memories,
            )
        for rel in data.get("relationships", []):
            graph.set_relationship(
                rel["source"],
                rel["target"],
                {k: rel.get(k, 0) for k in RELATIONSHIP_DIMENSIONS},
                hidden=rel.get("hidden", False),
            )
        graph.history = [
            ChangeRecord(
                turn=h["turn"],
                source=h["source"],
                target=h["target"],
                dimension=h["dimension"],
                delta=h["delta"],
                new_value=h["new_value"],
                reason=h.get("reason", ""),
            )
            for h in data.get("history", [])
        ]
        return graph

    def save(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str | Path) -> MultiDimensionalSocialGraph:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
