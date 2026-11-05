"""Author-facing world graphs for NoöPunk (#1178).

Four graph families, one rule: **the graph stores positions and connections; CWN resolves
actions**. Nothing here rolls dice, spends Effort, changes hit points or replaces CWN
Hacking, movement, exploration or combat.

The correction in #1178 is structural:

* **Physical** and (later) **Astral** nodes are *locations*. Characters occupy a node and
  move along edges; co-location is what allows ordinary interaction.
* **Cyber** nodes are *devices* (cameras, turrets, hosts) that are also navigable
  destinations for an avatar. A physical character stays in its Physical node.
* **Social** nodes are *characters or factions*; edges are relationships, not routes.
* **Story** nodes are Series, Episodes and Scenes; edges are progression conditions, not
  spatial travel.

The records are plain dictionaries, so an author can keep them in YAML/JSON and a later
loader can project them into NetworkX. The classes deliberately do not import NetworkX.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any


#: The scene-kind vocabulary (#1184). **Action**, not "Combat": the scene kind is an arrest, a
#: pursuit, a containment or a forced entry, and CWN's combat rules are what an Action scene calls
#: when force cannot be avoided. The old word is refused rather than aliased, because a synonym that
#: validates is a second undocumented vocabulary.
SCENE_TYPES = frozenset(("Investigation", "Exploration", "Action", "Social", "Cyber", "Astral"))
_SCENE_TYPES_CASELESS = frozenset(name.lower() for name in SCENE_TYPES)


class GraphError(ValueError):
    """A graph invariant was about to be violated."""


# --------------------------------------------------------------------------- #
# Shared validation
# --------------------------------------------------------------------------- #


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GraphError(f"{field_name} must be a non-empty string")
    return value.strip()


def _add_node(nodes: dict[str, Any], node: Any) -> None:
    node_id = _text(node.id, "node id")
    if node_id in nodes:
        raise GraphError(f"duplicate node id: {node_id}")
    nodes[node_id] = node


def _endpoints(edges: Iterable[Any], nodes: Mapping[str, Any]) -> None:
    for edge in edges:
        for endpoint in (edge.source, edge.target):
            if endpoint not in nodes:
                raise GraphError(f"dangling edge endpoint: {endpoint}")
        if edge.source == edge.target:
            raise GraphError(f"self-loop is not a route: {edge.source}")


# --------------------------------------------------------------------------- #
# Physical graph: locations, routes, occupancy
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class LocationNode:
    """A place at any useful scale: world, city, district, location or room."""

    id: str
    label: str
    kind: str = "room"
    parent_id: str = ""

    def __post_init__(self) -> None:
        _text(self.id, "location id")
        _text(self.label, "location label")
        if self.parent_id and self.parent_id == self.id:
            raise GraphError("a location cannot be its own parent")


@dataclass(frozen=True)
class PhysicalRoute:
    """A route, door or path. One row can be an undirected edge."""

    source: str
    target: str
    directed: bool = False
    kind: str = "door"
    label: str = ""


@dataclass
class PhysicalGraph:
    """Location graph + actor occupancy. Movement follows one valid route."""

    nodes: dict[str, LocationNode] = field(default_factory=dict)
    routes: tuple[PhysicalRoute, ...] = ()
    occupants: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for node_id, node in self.nodes.items():
            if node_id != node.id:
                raise GraphError(f"node key {node_id!r} does not match id {node.id!r}")
            if node.parent_id and node.parent_id not in self.nodes:
                raise GraphError(f"dangling parent location: {node.parent_id}")
        _endpoints(self.routes, self.nodes)
        for actor, node_id in self.occupants.items():
            if actor in self.nodes:
                raise GraphError(
                    f"{actor!r} is both an occupant and a location node; "
                    "actors occupy places, they are not places (#1178)"
                )
            if node_id not in self.nodes:
                raise GraphError(
                    f"actor {actor!r} occupies unknown location {node_id!r}"
                )

    # -- occupancy ---------------------------------------------------------
    def enter(self, actor_id: str, node_id: str) -> None:
        if actor_id in self.occupants:
            raise GraphError(f"{actor_id!r} is already on the physical graph")
        if node_id not in self.nodes:
            raise GraphError(f"unknown location: {node_id}")
        self.occupants[actor_id] = node_id

    def leave(self, actor_id: str) -> str:
        if actor_id not in self.occupants:
            raise GraphError(f"{actor_id!r} is not on the physical graph")
        return self.occupants.pop(actor_id)

    def at(self, actor_id: str) -> str:
        try:
            return self.occupants[actor_id]
        except KeyError as exc:
            raise GraphError(f"{actor_id!r} is not on the physical graph") from exc

    def occupants_at(self, node_id: str) -> tuple[str, ...]:
        return tuple(
            sorted(actor for actor, where in self.occupants.items() if where == node_id)
        )

    def co_located(self, first: str, second: str) -> bool:
        return self.at(first) == self.at(second)

    # -- movement ----------------------------------------------------------
    def adjacent(self, node_id: str) -> tuple[str, ...]:
        if node_id not in self.nodes:
            raise GraphError(f"unknown location: {node_id}")
        found: list[str] = []
        for route in self.routes:
            if route.source == node_id:
                found.append(route.target)
            elif not route.directed and route.target == node_id:
                found.append(route.source)
        return tuple(dict.fromkeys(found))

    def can_move(self, actor_id: str, destination: str) -> bool:
        return actor_id in self.occupants and destination in self.adjacent(
            self.occupants[actor_id]
        )

    def move(self, actor_id: str, destination: str) -> str:
        """Move along one route; no teleport and no implicit map-wide travel."""
        if destination not in self.nodes:
            raise GraphError(f"unknown location: {destination}")
        if not self.can_move(actor_id, destination):
            raise GraphError(f"no route from {self.at(actor_id)} to {destination}")
        self.occupants[actor_id] = destination
        return destination

    # -- authoring / serialization ----------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_type": "physical",
            "nodes": [
                {
                    "id": node.id,
                    "label": node.label,
                    "kind": node.kind,
                    "parent_id": node.parent_id,
                }
                for node in sorted(self.nodes.values(), key=lambda n: n.id)
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "directed": edge.directed,
                    "kind": edge.kind,
                    "label": edge.label,
                }
                for edge in self.routes
            ],
            "occupants": dict(sorted(self.occupants.items())),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> PhysicalGraph:
        nodes: dict[str, LocationNode] = {}
        for raw in payload.get("nodes", ()):
            node = LocationNode(
                str(raw["id"]),
                str(raw["label"]),
                str(raw.get("kind", "room")),
                str(raw.get("parent_id", "")),
            )
            _add_node(nodes, node)
        routes = tuple(
            PhysicalRoute(
                str(raw["source"]),
                str(raw["target"]),
                bool(raw.get("directed", False)),
                str(raw.get("kind", "door")),
                str(raw.get("label", "")),
            )
            for raw in payload.get("edges", ())
        )
        occupants = {
            str(actor): str(where)
            for actor, where in payload.get("occupants", {}).items()
        }
        return cls(nodes, routes, occupants)


# --------------------------------------------------------------------------- #
# Cyber graph: devices, network links, avatar occupancy
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class DeviceNode:
    """A device that is both a machine and a place an avatar can occupy."""

    id: str
    label: str
    device_type: str = "device"
    physical_location: str = ""
    actions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _text(self.id, "device id")
        _text(self.label, "device label")
        if self.physical_location and not self.physical_location.strip():
            raise GraphError("physical_location must be empty or a stable id")


@dataclass(frozen=True)
class NetworkLink:
    source: str
    target: str
    directed: bool = True
    kind: str = "network"


@dataclass
class CyberGraph:
    """Device graph + hacker-avatar positions. The operator's body does not move."""

    nodes: dict[str, DeviceNode] = field(default_factory=dict)
    links: tuple[NetworkLink, ...] = ()
    avatars: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for node_id, node in self.nodes.items():
            if node_id != node.id:
                raise GraphError(f"node key {node_id!r} does not match id {node.id!r}")
        _endpoints(self.links, self.nodes)
        for actor, node_id in self.avatars.items():
            if actor in self.nodes:
                raise GraphError(
                    f"{actor!r} is both an avatar and a device node; "
                    "avatars occupy devices, they are not devices (#1178)"
                )
            if node_id not in self.nodes:
                raise GraphError(
                    f"avatar {actor!r} occupies unknown device {node_id!r}"
                )

    def devices_at(self, physical_location: str) -> tuple[str, ...]:
        return tuple(
            sorted(
                device.id
                for device in self.nodes.values()
                if device.physical_location == physical_location
            )
        )

    def enter(self, actor_id: str, device_id: str) -> None:
        if actor_id in self.avatars:
            raise GraphError(f"{actor_id!r} already has an avatar on the cyber graph")
        if device_id not in self.nodes:
            raise GraphError(f"unknown device: {device_id}")
        self.avatars[actor_id] = device_id

    def leave(self, actor_id: str) -> str:
        if actor_id not in self.avatars:
            raise GraphError(f"{actor_id!r} has no avatar on the cyber graph")
        return self.avatars.pop(actor_id)

    def at(self, actor_id: str) -> str:
        try:
            return self.avatars[actor_id]
        except KeyError as exc:
            raise GraphError(f"{actor_id!r} has no avatar on the cyber graph") from exc

    def adjacent(self, device_id: str) -> tuple[str, ...]:
        if device_id not in self.nodes:
            raise GraphError(f"unknown device: {device_id}")
        found: list[str] = []
        for link in self.links:
            if link.source == device_id:
                found.append(link.target)
            elif not link.directed and link.target == device_id:
                found.append(link.source)
        return tuple(dict.fromkeys(found))

    def can_move(self, actor_id: str, destination: str) -> bool:
        return actor_id in self.avatars and destination in self.adjacent(
            self.avatars[actor_id]
        )

    def move_avatar(self, actor_id: str, destination: str) -> str:
        if destination not in self.nodes:
            raise GraphError(f"unknown device: {destination}")
        if not self.can_move(actor_id, destination):
            raise GraphError(
                f"no network link from {self.at(actor_id)} to {destination}"
            )
        self.avatars[actor_id] = destination
        return destination

    def actions_at(self, actor_id: str) -> tuple[str, ...]:
        """What the occupied device declares it can do; CWN Hacking still resolves it."""
        return self.nodes[self.at(actor_id)].actions

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_type": "cyber",
            "nodes": [
                {
                    "id": node.id,
                    "label": node.label,
                    "device_type": node.device_type,
                    "physical_location": node.physical_location,
                    "actions": list(node.actions),
                }
                for node in sorted(self.nodes.values(), key=lambda n: n.id)
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "directed": edge.directed,
                    "kind": edge.kind,
                }
                for edge in self.links
            ],
            "avatars": dict(sorted(self.avatars.items())),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> CyberGraph:
        nodes: dict[str, DeviceNode] = {}
        for raw in payload.get("nodes", ()):
            node = DeviceNode(
                str(raw["id"]),
                str(raw["label"]),
                str(raw.get("device_type", "device")),
                str(raw.get("physical_location", "")),
                tuple(str(action) for action in raw.get("actions", ())),
            )
            _add_node(nodes, node)
        links = tuple(
            NetworkLink(
                str(raw["source"]),
                str(raw["target"]),
                bool(raw.get("directed", True)),
                str(raw.get("kind", "network")),
            )
            for raw in payload.get("edges", ())
        )
        avatars = {
            str(actor): str(where)
            for actor, where in payload.get("avatars", {}).items()
        }
        return cls(nodes, links, avatars)


# --------------------------------------------------------------------------- #
# Social graph: characters/factions and directed relationships
# --------------------------------------------------------------------------- #

SOCIAL_NODE_KINDS = ("character", "faction")
RELATIONSHIP_MIN = -4
RELATIONSHIP_MAX = 4


@dataclass(frozen=True)
class SocialNode:
    id: str
    label: str
    kind: str = "character"

    def __post_init__(self) -> None:
        _text(self.id, "social node id")
        _text(self.label, "social node label")
        if self.kind not in SOCIAL_NODE_KINDS:
            raise GraphError(f"social node kind must be one of {SOCIAL_NODE_KINDS}")


@dataclass(frozen=True)
class Relationship:
    source: str
    target: str
    score: int
    kind: str = ""
    evidence: str = ""

    def __post_init__(self) -> None:
        if (
            not isinstance(self.score, int)
            or not RELATIONSHIP_MIN <= self.score <= RELATIONSHIP_MAX
        ):
            raise GraphError(
                f"relationship score must be an integer {RELATIONSHIP_MIN}..{RELATIONSHIP_MAX}"
            )


@dataclass
class SocialGraph:
    """Nodes are people/factions; edges are relationships, never travel routes."""

    nodes: dict[str, SocialNode] = field(default_factory=dict)
    relationships: tuple[Relationship, ...] = ()

    def __post_init__(self) -> None:
        for node_id, node in self.nodes.items():
            if node_id != node.id:
                raise GraphError(f"node key {node_id!r} does not match id {node.id!r}")
        _endpoints(self.relationships, self.nodes)
        seen: set[tuple[str, str]] = set()
        for edge in self.relationships:
            key = (edge.source, edge.target)
            if key in seen:
                raise GraphError(f"duplicate relationship: {key}")
            seen.add(key)

    def relationship(self, source: str, target: str) -> Relationship | None:
        for edge in self.relationships:
            if edge.source == source and edge.target == target:
                return edge
        return None

    def score(self, source: str, target: str) -> int | None:
        edge = self.relationship(source, target)
        return None if edge is None else edge.score

    def set_relationship(
        self,
        source: str,
        target: str,
        score: int,
        *,
        kind: str = "",
        evidence: str = "",
    ) -> Relationship:
        if source not in self.nodes or target not in self.nodes:
            raise GraphError("both relationship endpoints must exist")
        replacement = Relationship(source, target, score, kind, evidence)
        edges = [
            edge
            for edge in self.relationships
            if not (edge.source == source and edge.target == target)
        ]
        edges.append(replacement)
        self.relationships = tuple(edges)
        return replacement

    def neighbours(self, node_id: str) -> tuple[str, ...]:
        if node_id not in self.nodes:
            raise GraphError(f"unknown social node: {node_id}")
        return tuple(
            dict.fromkeys(
                edge.target for edge in self.relationships if edge.source == node_id
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_type": "social",
            "nodes": [
                {"id": node.id, "label": node.label, "kind": node.kind}
                for node in sorted(self.nodes.values(), key=lambda n: n.id)
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "score": edge.score,
                    "kind": edge.kind,
                    "evidence": edge.evidence,
                }
                for edge in self.relationships
            ],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> SocialGraph:
        nodes: dict[str, SocialNode] = {}
        for raw in payload.get("nodes", ()):
            node = SocialNode(
                str(raw["id"]), str(raw["label"]), str(raw.get("kind", "character"))
            )
            _add_node(nodes, node)
        edges = tuple(
            Relationship(
                str(raw["source"]),
                str(raw["target"]),
                int(raw["score"]),
                str(raw.get("kind", "")),
                str(raw.get("evidence", "")),
            )
            for raw in payload.get("edges", ())
        )
        return cls(nodes, edges)


# --------------------------------------------------------------------------- #
# Story graph: Series -> Episodes -> Scenes
# --------------------------------------------------------------------------- #

STORY_NODE_KINDS = ("series", "episode", "scene")


@dataclass(frozen=True)
class StoryNode:
    id: str
    label: str
    kind: str
    parent_id: str = ""
    scene_types: tuple[str, ...] = ()
    goal_ids: tuple[str, ...] = ()
    prerequisites: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _text(self.id, "story node id")
        _text(self.label, "story node label")
        if self.kind not in STORY_NODE_KINDS:
            raise GraphError(f"story node kind must be one of {STORY_NODE_KINDS}")
        if self.parent_id and self.parent_id == self.id:
            raise GraphError("a story node cannot be its own parent")
        if self.kind != "scene" and self.scene_types:
            raise GraphError("scene types belong to scenes")
        unknown = sorted({v for v in self.scene_types if v.strip().lower() not in _SCENE_TYPES_CASELESS})
        if unknown:
            raise GraphError(
                f"unknown scene types {unknown}; Action is the scene kind, not Combat"
            )


@dataclass(frozen=True)
class StoryLink:
    source: str
    target: str
    kind: str = "transition"
    condition: str = ""


@dataclass
class StoryGraph:
    """Series -> Episodes -> Scenes, with gated transitions and goal references."""

    nodes: dict[str, StoryNode] = field(default_factory=dict)
    links: tuple[StoryLink, ...] = ()

    def __post_init__(self) -> None:
        for node_id, node in self.nodes.items():
            if node_id != node.id:
                raise GraphError(f"node key {node_id!r} does not match id {node.id!r}")
            if node.parent_id:
                parent = self.nodes.get(node.parent_id)
                if parent is None:
                    raise GraphError(f"dangling story parent: {node.parent_id}")
                if node.kind == "series" or parent.kind == "scene":
                    raise GraphError(
                        f"invalid story hierarchy: {parent.kind} -> {node.kind}"
                    )
                if node.kind == "episode" and parent.kind != "series":
                    raise GraphError("an episode's parent must be a series")
                if node.kind == "scene" and parent.kind != "episode":
                    raise GraphError("a scene's parent must be an episode")
        _endpoints(self.links, self.nodes)

    def children(self, node_id: str) -> tuple[str, ...]:
        if node_id not in self.nodes:
            raise GraphError(f"unknown story node: {node_id}")
        return tuple(
            sorted(node.id for node in self.nodes.values() if node.parent_id == node_id)
        )

    def available(
        self, current: str, *, flags: Iterable[str] = (), completed: Iterable[str] = ()
    ) -> tuple[str, ...]:
        """Transitions whose condition is satisfied; an empty condition is always open."""
        if current not in self.nodes:
            raise GraphError(f"unknown story node: {current}")
        satisfied = set(flags) | set(completed)
        result: list[str] = []
        for link in self.links:
            if link.source == current and (
                not link.condition or link.condition in satisfied
            ):
                result.append(link.target)
        return tuple(dict.fromkeys(result))

    def can_enter(
        self, node_id: str, *, flags: Iterable[str] = (), completed: Iterable[str] = ()
    ) -> bool:
        node = self.nodes.get(node_id)
        if node is None:
            return False
        satisfied = set(flags) | set(completed)
        return all(requirement in satisfied for requirement in node.prerequisites)

    def advance(
        self,
        current: str,
        target: str,
        *,
        flags: Iterable[str] = (),
        completed: Iterable[str] = (),
    ) -> bool:
        """Whether the story may move from ``current`` to ``target``; no state is mutated."""
        return target in self.available(
            current, flags=flags, completed=completed
        ) and self.can_enter(target, flags=flags, completed=completed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_type": "story",
            "nodes": [
                {
                    "id": node.id,
                    "label": node.label,
                    "kind": node.kind,
                    "parent_id": node.parent_id,
                    "scene_types": list(node.scene_types),
                    "goal_ids": list(node.goal_ids),
                    "prerequisites": list(node.prerequisites),
                }
                for node in sorted(self.nodes.values(), key=lambda n: n.id)
            ],
            "edges": [
                {
                    "source": link.source,
                    "target": link.target,
                    "kind": link.kind,
                    "condition": link.condition,
                }
                for link in self.links
            ],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> StoryGraph:
        nodes: dict[str, StoryNode] = {}
        for raw in payload.get("nodes", ()):
            node = StoryNode(
                str(raw["id"]),
                str(raw["label"]),
                str(raw["kind"]),
                str(raw.get("parent_id", "")),
                tuple(str(value) for value in raw.get("scene_types", ())),
                tuple(str(value) for value in raw.get("goal_ids", ())),
                tuple(str(value) for value in raw.get("prerequisites", ())),
            )
            _add_node(nodes, node)
        links = tuple(
            StoryLink(
                str(raw["source"]),
                str(raw["target"]),
                str(raw.get("kind", "transition")),
                str(raw.get("condition", "")),
            )
            for raw in payload.get("edges", ())
        )
        return cls(nodes, links)


# --------------------------------------------------------------------------- #
# Cross-graph references
# --------------------------------------------------------------------------- #


@dataclass
class WorldGraphs:
    """The four current families. Astral is deliberately absent until #1178 says so."""

    physical: PhysicalGraph
    cyber: CyberGraph
    social: SocialGraph
    story: StoryGraph

    def __post_init__(self) -> None:
        for device in self.cyber.nodes.values():
            if (
                device.physical_location
                and device.physical_location not in self.physical.nodes
            ):
                raise GraphError(
                    f"cyber device {device.id!r} references unknown physical location "
                    f"{device.physical_location!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "noopunk.world.graphs",
            "version": 1,
            "physical": self.physical.to_dict(),
            "cyber": self.cyber.to_dict(),
            "social": self.social.to_dict(),
            "story": self.story.to_dict(),
        }

    def to_networkx(self) -> dict[str, Any]:
        """Derived views for analysis/drawing; the dicts remain the authored source.

        NetworkX is optional: importing it here keeps the rules layer usable without it.
        Undirected routes are represented as two directed edges so one view type covers both.
        """
        try:
            import networkx as nx
        except ImportError as exc:  # pragma: no cover - environment guard
            raise GraphError("NetworkX is not installed") from exc

        physical = nx.DiGraph()
        for node in self.physical.nodes.values():
            physical.add_node(
                node.id, label=node.label, kind=node.kind, parent_id=node.parent_id
            )
        for route in self.physical.routes:
            physical.add_edge(
                route.source, route.target, kind=route.kind, directed=route.directed
            )
            if not route.directed:
                physical.add_edge(
                    route.target, route.source, kind=route.kind, directed=False
                )

        cyber = nx.DiGraph()
        for node in self.cyber.nodes.values():
            cyber.add_node(
                node.id,
                label=node.label,
                device_type=node.device_type,
                physical_location=node.physical_location,
                actions=list(node.actions),
            )
        for link in self.cyber.links:
            cyber.add_edge(
                link.source, link.target, kind=link.kind, directed=link.directed
            )
            if not link.directed:
                cyber.add_edge(link.target, link.source, kind=link.kind, directed=False)

        social = nx.DiGraph()
        for node in self.social.nodes.values():
            social.add_node(node.id, label=node.label, kind=node.kind)
        for edge in self.social.relationships:
            social.add_edge(
                edge.source,
                edge.target,
                score=edge.score,
                kind=edge.kind,
                evidence=edge.evidence,
            )

        story = nx.DiGraph()
        for node in self.story.nodes.values():
            story.add_node(
                node.id,
                label=node.label,
                kind=node.kind,
                parent_id=node.parent_id,
                prerequisites=list(node.prerequisites),
                goal_ids=list(node.goal_ids),
                scene_types=list(node.scene_types),
            )
        for link in self.story.links:
            story.add_edge(
                link.source, link.target, kind=link.kind, condition=link.condition
            )

        return {"physical": physical, "cyber": cyber, "social": social, "story": story}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> WorldGraphs:
        return cls(
            PhysicalGraph.from_dict(payload.get("physical", {})),
            CyberGraph.from_dict(payload.get("cyber", {})),
            SocialGraph.from_dict(payload.get("social", {})),
            StoryGraph.from_dict(payload.get("story", {})),
        )


__all__ = [
    "CyberGraph",
    "DeviceNode",
    "GraphError",
    "LocationNode",
    "NetworkLink",
    "PhysicalGraph",
    "PhysicalRoute",
    "Relationship",
    "SocialGraph",
    "SocialNode",
    "StoryGraph",
    "StoryLink",
    "StoryNode",
    "WorldGraphs",
]
