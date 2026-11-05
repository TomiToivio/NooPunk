"""Issue #1178: four interoperable graph views, NOT a replacement rules engine.

Physical and Cyber nodes are places one can occupy; Social nodes are entities;
Story nodes are narrative records. No Astral graph or psychic actions here.
The adapters validate author data and offer topology/occupancy/transition checks.
CWN hacking, combat, investigation and advancement stay with their own modules.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
import json

GRAPH_FAMILIES = ("physical", "cyber", "social", "story")
SCENE_TYPES = frozenset(("Investigation", "Exploration", "Combat", "Social", "Cyber", "Astral"))
SOCIAL_MIN, SOCIAL_MAX = -4, 4


class GraphContractError(ValueError):
    """Invalid author data or attempted traversal across a missing/locked edge."""


def _id(value: str, label: str = "id") -> str:
    if not isinstance(value, str) or not value.strip():
        raise GraphContractError(f"{label} must be a nonempty string")
    return value


def _known(source: str, target: str, nodes: Mapping[str, Any]) -> None:
    if source not in nodes or target not in nodes:
        raise GraphContractError(f"dangling graph edge {source!r} -> {target!r}")


@dataclass(frozen=True)
class Place:
    id: str
    label: str
    kind: str = "location"
    parent_id: str = ""
    physical_ref: str = ""
    device_actions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _id(self.id)
        _id(self.label, "label")
        if not isinstance(self.device_actions, tuple) or any(not isinstance(a, str) or not a for a in self.device_actions):
            raise GraphContractError("device_actions must be a tuple of nonempty strings")


@dataclass(frozen=True)
class Route:
    source: str
    target: str
    id: str
    directed: bool = False
    gate: str = ""

    def __post_init__(self) -> None:
        _id(self.id)
        _id(self.source, "source")
        _id(self.target, "target")


@dataclass
class SpatialGraph:
    """Locations and edges, with occupancies stored separately from nodes.

    `positions` maps actor or avatar IDs to place IDs. These are references
    to external character sheets, not independent actor records or a new HP pool.
    """

    family: str
    nodes: dict[str, Place]
    edges: tuple[Route, ...]
    positions: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.family not in ("physical", "cyber"):
            raise GraphContractError("spatial graph must be physical or cyber")
        for key, node in self.nodes.items():
            if key != node.id:
                raise GraphContractError("node key and id must agree")
            if self.family == "physical" and (node.physical_ref or node.device_actions):
                raise GraphContractError("device fields belong to Cyber nodes")
            if self.family == "cyber" and node.kind not in ("device", "computer", "camera", "turret", "network", "service", "host", "account", "data"):
                raise GraphContractError("Cyber nodes must be network devices/services")
            if node.parent_id and node.parent_id not in self.nodes:
                raise GraphContractError(f"unknown parent {node.parent_id}")
        if len({e.id for e in self.edges}) != len(self.edges):
            raise GraphContractError("duplicate edge id")
        for edge in self.edges:
            _known(edge.source, edge.target, self.nodes)
        for actor, location in self.positions.items():
            _id(actor, "occupant")
            if actor in self.nodes:
                raise GraphContractError("occupant ID cannot be a location node ID")
            if location not in self.nodes:
                raise GraphContractError(f"occupant {actor} at missing node {location}")

    def occupants(self, place_id: str) -> tuple[str, ...]:
        if place_id not in self.nodes:
            raise GraphContractError("unknown place")
        return tuple(sorted(actor for actor, location in self.positions.items() if location == place_id))

    def co_located(self, left: str, right: str) -> bool:
        return left in self.positions and right in self.positions and self.positions[left] == self.positions[right]

    def enter(self, actor_id: str, place_id: str) -> None:
        _id(actor_id, "occupant")
        if actor_id in self.nodes or place_id not in self.nodes:
            raise GraphContractError("invalid occupant or location")
        self.positions[actor_id] = place_id

    def neighbors(self, place_id: str, *, flags: frozenset[str] = frozenset()) -> tuple[str, ...]:
        if place_id not in self.nodes:
            raise GraphContractError("unknown place")
        result = set()
        for edge in self.edges:
            if edge.gate and edge.gate not in flags:
                continue
            if edge.source == place_id:
                result.add(edge.target)
            if not edge.directed and edge.target == place_id:
                result.add(edge.source)
        return tuple(sorted(result))

    def move(self, actor_id: str, destination: str, *, flags: frozenset[str] = frozenset()) -> None:
        if actor_id not in self.positions:
            raise GraphContractError("actor/avatar must enter a graph first")
        if destination not in self.neighbors(self.positions[actor_id], flags=flags):
            raise GraphContractError("no accessible edge to destination")
        self.positions[actor_id] = destination

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_type": self.family,
            "version": 1,
            "nodes": [vars(node) | {"device_actions": list(node.device_actions)} for node in self.nodes.values()],
            "edges": [vars(edge).copy() for edge in self.edges],
            "positions": dict(self.positions),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SpatialGraph":
        if data.get("version") != 1:
            raise GraphContractError("unsupported graph version")
        nodes = [Place(**(dict(item) | {"device_actions": tuple(item.get("device_actions", ())) }))
                 for item in data["nodes"]]
        if len({node.id for node in nodes}) != len(nodes):
            raise GraphContractError("duplicate node IDs")
        return cls(
            family=data["graph_type"],
            nodes={n.id: n for n in nodes},
            edges=tuple(Route(**item) for item in data["edges"]),
            positions=dict(data.get("positions", {})),
        )


@dataclass(frozen=True)
class SocialEntity:
    id: str
    kind: str  # character | faction
    label: str

    def __post_init__(self) -> None:
        _id(self.id)
        if self.kind not in ("character", "faction"):
            raise GraphContractError("social nodes must be characters or factions")
        _id(self.label, "label")


@dataclass(frozen=True)
class Relationship:
    source: str
    target: str
    score: int  # relational score -4 ... +4; not faction resource statistics
    kind: str = "relationship"
    directed: bool = True

    def __post_init__(self) -> None:
        if type(self.score) is not int or not SOCIAL_MIN <= self.score <= SOCIAL_MAX:
            raise GraphContractError("relationship score must be an integer -4..+4")


@dataclass
class SocialGraph:
    nodes: dict[str, SocialEntity]
    edges: tuple[Relationship, ...]

    def __post_init__(self) -> None:
        for key, value in self.nodes.items():
            if key != value.id:
                raise GraphContractError("social node key mismatch")
        for edge in self.edges:
            _known(edge.source, edge.target, self.nodes)
        identities = [(e.source, e.target, e.kind) if e.directed
                      else (min(e.source, e.target), max(e.source, e.target), e.kind)
                      for e in self.edges]
        if len(identities) != len(set(identities)):
            raise GraphContractError("duplicate social relationship")

    def relationship(self, source: str, target: str) -> int | None:
        """Missing relation is UNKNOWN, not known-neutral zero."""
        for edge in self.edges:
            if edge.source == source and edge.target == target:
                return edge.score
            if not edge.directed and edge.source == target and edge.target == source:
                return edge.score
        return None

    def to_dict(self) -> dict[str, Any]:
        return {"graph_type": "social", "version": 1,
                "nodes": [vars(n).copy() for n in self.nodes.values()],
                "edges": [vars(e).copy() for e in self.edges]}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SocialGraph":
        if data.get("graph_type") != "social" or data.get("version") != 1:
            raise GraphContractError("unsupported social graph")
        nodes = [SocialEntity(**n) for n in data["nodes"]]
        if len({n.id for n in nodes}) != len(nodes):
            raise GraphContractError("duplicate social node IDs")
        return cls({n.id: n for n in nodes}, tuple(Relationship(**e) for e in data["edges"]))


@dataclass(frozen=True)
class StoryNode:
    id: str
    kind: str
    label: str
    scene_types: tuple[str, ...] = ()
    references: tuple[str, ...] = ()  # external Physical/Cyber/Social refs
    goal_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _id(self.id)
        if self.kind not in ("series", "episode", "scene"):
            raise GraphContractError("story node kind must be series/episode/scene")
        if self.kind != "scene" and self.scene_types:
            raise GraphContractError("scene types apply to scenes only")
        if set(self.scene_types) - SCENE_TYPES:
            raise GraphContractError("invalid scene type")


@dataclass(frozen=True)
class StoryEdge:
    source: str
    target: str
    kind: str = "transition"  # contains | transition
    all_flags: tuple[str, ...] = ()
    all_goals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in ("contains", "transition"):
            raise GraphContractError("story edge kind must be contains or transition")


@dataclass
class StoryGraph:
    nodes: dict[str, StoryNode]
    edges: tuple[StoryEdge, ...]

    def __post_init__(self) -> None:
        for key, node in self.nodes.items():
            if key != node.id:
                raise GraphContractError("story node key mismatch")
        for edge in self.edges:
            _known(edge.source, edge.target, self.nodes)
            src, dst = self.nodes[edge.source], self.nodes[edge.target]
            if edge.kind == "contains":
                if (src.kind, dst.kind) not in (("series", "episode"), ("episode", "scene")):
                    raise GraphContractError("contains must be Series->Episode or Episode->Scene")
                if edge.all_flags or edge.all_goals:
                    raise GraphContractError("contains edges cannot have transition gates")
            elif src.kind != dst.kind:
                raise GraphContractError("transition endpoints must share a narrative level")
        # Containment must be a hierarchy, not a cyclic or multi-parent graph.
        parents: dict[str, str] = {}
        for edge in self.edges:
            if edge.kind == "contains":
                if edge.target in parents:
                    raise GraphContractError("Story node has multiple parents")
                parents[edge.target] = edge.source

    def children(self, parent_id: str) -> tuple[str, ...]:
        return tuple(e.target for e in self.edges if e.kind == "contains" and e.source == parent_id)

    def available(self, current: str, *, flags: frozenset[str] = frozenset(),
                  completed_goals: frozenset[str] = frozenset()) -> tuple[str, ...]:
        """Read completion from existing GoalLog and pass the IDs; no new XP owner."""
        if current not in self.nodes:
            raise GraphContractError("unknown current story node")
        return tuple(e.target for e in self.edges if e.kind == "transition"
                     and e.source == current and set(e.all_flags) <= flags
                     and set(e.all_goals) <= completed_goals)

    def to_dict(self) -> dict[str, Any]:
        return {"graph_type": "story", "version": 1,
                "nodes": [vars(n) | {"scene_types": list(n.scene_types),
                                     "references": list(n.references), "goal_refs": list(n.goal_refs)}
                          for n in self.nodes.values()],
                "edges": [vars(e) | {"all_flags": list(e.all_flags),
                                     "all_goals": list(e.all_goals)} for e in self.edges]}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "StoryGraph":
        if data.get("graph_type") != "story" or data.get("version") != 1:
            raise GraphContractError("unsupported story graph")
        nodes = [StoryNode(**(dict(n) | {
            "scene_types": tuple(n.get("scene_types", ())),
            "references": tuple(n.get("references", ())),
            "goal_refs": tuple(n.get("goal_refs", ())),
        })) for n in data["nodes"]]
        if len({n.id for n in nodes}) != len(nodes):
            raise GraphContractError("duplicate story node IDs")
        edges = tuple(StoryEdge(**(dict(e) | {
            "all_flags": tuple(e.get("all_flags", ())),
            "all_goals": tuple(e.get("all_goals", ())),
        })) for e in data["edges"])
        return cls({n.id: n for n in nodes}, edges)


@dataclass
class FourGraphs:
    physical: SpatialGraph
    cyber: SpatialGraph
    social: SocialGraph
    story: StoryGraph
    avatars: dict[str, str] = field(default_factory=dict)  # avatar -> operator character

    def __post_init__(self) -> None:
        if self.physical.family != "physical" or self.cyber.family != "cyber":
            raise GraphContractError("wrong graph family")
        for node in self.cyber.nodes.values():
            if node.physical_ref and node.physical_ref not in self.physical.nodes:
                raise GraphContractError(f"Cyber device {node.id} has unknown Physical location")
        for avatar, operator in self.avatars.items():
            if avatar not in self.cyber.positions or operator not in self.physical.positions:
                raise GraphContractError("avatar and operator must have recorded positions")
            if avatar == operator:
                raise GraphContractError("Cyber avatar and physical operator need distinct IDs")
        for node in self.story.nodes.values():
            for ref in node.references:
                if ref not in self.physical.nodes and ref not in self.cyber.nodes and ref not in self.social.nodes:
                    raise GraphContractError(f"unresolved scene reference {ref}")

    def move_avatar(self, avatar: str, target: str, *, flags: frozenset[str] = frozenset()) -> None:
        if avatar not in self.avatars:
            raise GraphContractError("unregistered cyber avatar")
        self.cyber.move(avatar, target, flags=flags)
        # The operator's physical position is intentionally untouched.

    def to_dict(self) -> dict[str, Any]:
        return {"format": "noopunk.four_graphs", "version": 1,
                "physical": self.physical.to_dict(), "cyber": self.cyber.to_dict(),
                "social": self.social.to_dict(), "story": self.story.to_dict(),
                "avatars": dict(self.avatars)}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "FourGraphs":
        if data.get("format") != "noopunk.four_graphs" or data.get("version") != 1:
            raise GraphContractError("unsupported four-graph snapshot")
        return cls(SpatialGraph.from_dict(data["physical"]),
                   SpatialGraph.from_dict(data["cyber"]),
                   SocialGraph.from_dict(data["social"]),
                   StoryGraph.from_dict(data["story"]),
                   dict(data.get("avatars", {})))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_json(cls, content: str) -> "FourGraphs":
        return cls.from_dict(json.loads(content))


def networkx_view(graph: SpatialGraph | SocialGraph | StoryGraph) -> Any:
    """Optional *derived* NetworkX projection; source is the portable author data.

    Dependency is optional: pip install networkx to enable rendering/analysis.
    Occupants are node attributes, NEVER graph nodes.
    """
    try:
        import networkx as nx
    except ImportError as exc:
        raise ImportError("networkx is optional; install it for graph visualization") from exc
    result = nx.MultiDiGraph()
    if isinstance(graph, SpatialGraph):
        for node in graph.nodes.values():
            result.add_node(node.id, **vars(node), occupants=graph.occupants(node.id))
        for edge in graph.edges:
            result.add_edge(edge.source, edge.target, key=edge.id, gate=edge.gate)
            if not edge.directed:
                result.add_edge(edge.target, edge.source, key=edge.id + ":return", gate=edge.gate)
    elif isinstance(graph, SocialGraph):
        for node in graph.nodes.values():
            result.add_node(node.id, **vars(node))
        for edge in graph.edges:
            result.add_edge(edge.source, edge.target, score=edge.score, kind=edge.kind)
            if not edge.directed:
                result.add_edge(edge.target, edge.source, score=edge.score, kind=edge.kind)
    else:
        for node in graph.nodes.values():
            result.add_node(node.id, **vars(node))
        for edge in graph.edges:
            result.add_edge(edge.source, edge.target, kind=edge.kind,
                            all_flags=edge.all_flags, all_goals=edge.all_goals)
    return result
