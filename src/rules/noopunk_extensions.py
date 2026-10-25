"""Additive, standard-library NoöPunk extension kernel (#572/#564).

Ubiquitous *reachability* is not omnipotent access: networked objects can relay
messages along connected edges; local-only nodes remain local. This module does
not replace the existing 1d10 or Fate checks, and does not import rulebook text.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
from random import Random


@dataclass(frozen=True)
class Node:
    id: str
    online: bool = True
    protected: bool = False
    # Users/agents can reach a protected node only if it is an authorized endpoint
    owner: str = ""


@dataclass
class UbiquitousNetwork:
    nodes: dict[str, Node] = field(default_factory=dict)
    links: set[tuple[str, str]] = field(default_factory=set)

    def add(self, node: Node) -> None:
        if not node.id:
            raise ValueError("node ID required")
        self.nodes[node.id] = node

    def connect(self, a: str, b: str) -> None:
        if a == b or a not in self.nodes or b not in self.nodes:
            raise ValueError("links need two distinct existing nodes")
        self.links.add(tuple(sorted((a, b))))

    def route(self, source: str, target: str) -> tuple[str, ...] | None:
        if source not in self.nodes or target not in self.nodes:
            return None
        if not self.nodes[source].online or not self.nodes[target].online:
            return None
        frontier = deque([(source,)])
        visited = {source}
        while frontier:
            path = frontier.popleft()
            if path[-1] == target:
                return path
            for a, b in sorted(self.links):
                nxt = b if a == path[-1] else a if b == path[-1] else None
                if nxt and nxt not in visited and self.nodes[nxt].online:
                    visited.add(nxt)
                    frontier.append((*path, nxt))
        return None

    def assess(self, source: str, target: str, actor: str, *,
               physical_presence: bool = False) -> str:
        """Return blocked / contested / permitted; never silently authorize hacking."""
        if target not in self.nodes or source not in self.nodes:
            return "blocked"
        endpoint = self.nodes[target]
        if not endpoint.online and not physical_presence:
            return "blocked"
        if not physical_presence and self.route(source, target) is None:
            return "blocked"
        if endpoint.protected and endpoint.owner != actor:
            return "contested"
        return "permitted"


PSI_DISCIPLINES = ("perception", "telepathy", "psychokinesis", "precognition", "noetic_defense")


@dataclass
class HumanPsi:
    """Learnable human PSI: training grants competence, not a separate species/class.

    The Effort-inspired committed pool is original implementation.  All actions
    requiring PSI spend or commit finite effort and may resolve using the owning
    RPG layer's check.  Training is possible for every human character.
    """
    training: dict[str, int] = field(default_factory=dict)
    capacity: int = 2
    spent: int = 0
    committed: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.capacity < 1 or self.spent < 0:
            raise ValueError("invalid effort")
        if any(k not in PSI_DISCIPLINES or not isinstance(v, int) or v < 0 or v > 4
               for k, v in self.training.items()):
            raise ValueError("invalid PSI training")
        if self.spent + sum(self.committed.values()) > self.capacity:
            raise ValueError("effort exceeds capacity")

    @property
    def available(self) -> int:
        return self.capacity - self.spent - sum(self.committed.values())

    def learn(self, discipline: str) -> int:
        if discipline not in PSI_DISCIPLINES:
            raise ValueError("unknown PSI discipline")
        level = self.training.get(discipline, 0)
        if level >= 4:
            raise ValueError("PSI discipline already mastered")
        self.training[discipline] = level + 1
        return level + 1

    def activate(self, discipline: str, *, ongoing_id: str | None = None) -> bool:
        if discipline not in PSI_DISCIPLINES or self.training.get(discipline, 0) < 1:
            return False
        if self.available < 1:
            return False
        if ongoing_id is None:
            self.spent += 1
        else:
            if not ongoing_id or ongoing_id in self.committed:
                return False
            self.committed[ongoing_id] = 1
        return True

    def release(self, ongoing_id: str) -> None:
        del self.committed[ongoing_id]

    def rest(self) -> None:
        """Rest restores spent effort, not effort bound to sustained powers."""
        self.spent = 0

    def snapshot(self) -> dict:
        return {"training": dict(sorted(self.training.items())), "capacity": self.capacity,
                "spent": self.spent, "committed": dict(sorted(self.committed.items()))}

    @classmethod
    def restore(cls, snapshot: dict) -> "HumanPsi":
        return cls(training=dict(snapshot["training"]), capacity=snapshot["capacity"],
                   spent=snapshot["spent"], committed=dict(snapshot["committed"]))


@dataclass
class Crisis:
    """Optional local crisis pressure; no universal apocalypse assumption."""
    scarcity: int = 0
    trust: int = 3
    exposure: int = 0

    def event(self, *, supply_loss: int = 0, solidarity: int = 0,
              exposure_gain: int = 0) -> None:
        self.scarcity = max(0, self.scarcity + supply_loss)
        self.trust = max(0, min(6, self.trust + solidarity))
        self.exposure = max(0, self.exposure + exposure_gain)


@dataclass
class Contact:
    """NHI contact is negotiation across differing goals, not good/evil alignment."""
    reciprocity: int = 0
    autonomy: int = 3

    def negotiate(self, *, exchange: int, pressure: int) -> None:
        self.reciprocity = max(-6, min(6, self.reciprocity + exchange))
        self.autonomy = max(0, min(6, self.autonomy - pressure))


def seeded_scene(seed: int, aptitude: int, difficulty: int) -> bool:
    """Optional standalone d10 demonstration, NOT a replacement RPG resolver."""
    return Random(seed).randint(1, 10) + aptitude >= difficulty
