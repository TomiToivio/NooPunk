"""The four playable graph families (#1178): physical, cyber, social and story.

The model is deliberately small, and its shape is the decision the issue records:

* **Physical** nodes are *places* (world → city → district → location → room). A character is never a node here; it
  **occupies** one and moves along edges, and two characters can interact only when both occupy the same place.
* **Cyber** nodes are *devices* (cameras, turrets, services, hosts) and they are also *destinations*: an avatar
  occupies a cyber node and moves along network edges. A device can act as a machine and be a place at the same
  time, which is why node kinds carry no "agent" member.
* **Social** nodes *are* characters and factions. Social edges are relationships (−4…+4) and are never routes.
* **Story** nodes are series, episodes and scenes; transitions gate on flags.

**The Astral graph is deferred** (#1178 §5–§6). Constructing it raises: the point of the deferral is that an
astral *agent* is an occupant of an astral *location*, and that shape should be built when projection scenes exist,
not before.

No third-party dependency: the graph is an adjacency map, not a NetworkX object. A projection can be built later
by whoever needs one; this module is the source-of-truth model.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping

__all__ = [
    "Family", "GraphError", "Node", "Edge", "Graph", "World",
    "physical_from_helsinki",
]


class GraphError(ValueError):
    """Raised when a graph breaks the family contract (#1178 §5)."""


class Family(str, Enum):
    PHYSICAL = "physical"
    CYBER = "cyber"
    SOCIAL = "social"
    STORY = "story"
    ASTRAL = "astral"

    @property
    def is_deferred(self) -> bool:
        return self is Family.ASTRAL

    @property
    def is_place_family(self) -> bool:
        """Families whose nodes are places a character or avatar can occupy."""
        return self in (Family.PHYSICAL, Family.CYBER)

    @property
    def is_entity_family(self) -> bool:
        """The one family whose nodes are characters and factions."""
        return self is Family.SOCIAL


NODE_KINDS: dict[Family, frozenset[str]] = {
    Family.PHYSICAL: frozenset({"world", "city", "district", "location", "room"}),
    Family.CYBER: frozenset({"device", "service", "network"}),
    Family.SOCIAL: frozenset({"character", "faction"}),
    Family.STORY: frozenset({"series", "episode", "scene"}),
}

VISIBILITIES = frozenset({"player", "discovered", "gm_secret"})
ASTRAL_DEFERRED = (
    "the Astral graph is deferred until Astral Projection exists (#1178); a scripted astral scene is a story "
    "scene with tags for now, not a navigable fifth graph"
)


@dataclass(frozen=True, slots=True)
class Node:
    node_id: str
    family: Family
    kind: str
    label: str = ""
    parent_id: str | None = None
    #: Cyber only: the physical node this device sits in. A reference, never a copy.
    location_ref: str | None = None
    tags: tuple[str, ...] = ()
    visibility: str = "player"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.node_id:
            raise GraphError("a node needs an id")
        if self.kind not in NODE_KINDS[self.family]:
            raise GraphError(
                f"{self.node_id!r}: kind {self.kind!r} is not a {self.family.value} node kind "
                f"({sorted(NODE_KINDS[self.family])})"
            )
        if self.visibility not in VISIBILITIES:
            raise GraphError(f"{self.node_id!r}: visibility {self.visibility!r} is not one of {sorted(VISIBILITIES)}")
        if self.location_ref is not None and self.family is not Family.CYBER:
            raise GraphError(f"{self.node_id!r}: only a cyber node carries a physical location reference")

    @property
    def is_place(self) -> bool:
        return self.family.is_place_family

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "node_id": self.node_id,
            "family": self.family.value,
            "kind": self.kind,
            "label": self.label,
            "tags": list(self.tags),
            "visibility": self.visibility,
        }
        if self.parent_id is not None:
            out["parent_id"] = self.parent_id
        if self.location_ref is not None:
            out["location_ref"] = self.location_ref
        if self.metadata:
            out["metadata"] = dict(self.metadata)
        return out

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "Node":
        return cls(
            node_id=str(raw["node_id"]),
            family=Family(raw["family"]),
            kind=str(raw["kind"]),
            label=str(raw.get("label", "")),
            parent_id=None if raw.get("parent_id") is None else str(raw["parent_id"]),
            location_ref=None if raw.get("location_ref") is None else str(raw["location_ref"]),
            tags=tuple(str(t) for t in raw.get("tags", ())),
            visibility=str(raw.get("visibility", "player")),
            metadata=dict(raw.get("metadata", {})),
        )


@dataclass(frozen=True, slots=True)
class Edge:
    edge_id: str
    family: Family
    source: str
    target: str
    relation: str = "route"
    directed: bool = False
    access: str | None = None
    travel_cost: str | None = None
    knowledge_gate: str | None = None
    #: Social only: the signed relationship, −4…+4.
    relationship: int | None = None
    #: Story only: the flag that must hold for this transition.
    when: str | None = None

    def __post_init__(self) -> None:
        if not self.edge_id:
            raise GraphError("an edge needs an id")
        if self.source == self.target:
            raise GraphError(f"{self.edge_id!r}: an edge must join two different nodes")
        if self.family is Family.SOCIAL:
            if self.relationship is None:
                raise GraphError(f"{self.edge_id!r}: a social edge needs a relationship score")
            if not -4 <= self.relationship <= 4:
                raise GraphError(f"{self.edge_id!r}: relationship must be in -4..+4, got {self.relationship}")
            if self.travel_cost is not None:
                raise GraphError(f"{self.edge_id!r}: a social link is not a route")
        elif self.relationship is not None:
            raise GraphError(f"{self.edge_id!r}: only a social edge carries a relationship score")
        if self.family is Family.STORY and self.relation not in {"entry", "sequence", "alternative"}:
            raise GraphError(f"{self.edge_id!r}: story relation {self.relation!r} is not entry/sequence/alternative")
        if self.family is Family.STORY and self.relation != "entry" and self.when is None:
            raise GraphError(f"{self.edge_id!r}: a story transition needs the flag that gates it")

    def touches(self, node_id: str) -> bool:
        return node_id in (self.source, self.target)

    def other(self, node_id: str) -> str:
        if node_id == self.source:
            return self.target
        if node_id == self.target:
            return self.source
        raise GraphError(f"{self.edge_id!r} does not touch {node_id!r}")

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "edge_id": self.edge_id,
            "family": self.family.value,
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
        }
        for name in ("access", "travel_cost", "knowledge_gate", "when"):
            value = getattr(self, name)
            if value is not None:
                out[name] = value
        if self.directed:
            out["directed"] = True
        if self.relationship is not None:
            out["relationship"] = self.relationship
        return out

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "Edge":
        return cls(
            edge_id=str(raw["edge_id"]),
            family=Family(raw["family"]),
            source=str(raw["source"]),
            target=str(raw["target"]),
            relation=str(raw.get("relation", "route")),
            directed=bool(raw.get("directed", False)),
            access=None if raw.get("access") is None else str(raw["access"]),
            travel_cost=None if raw.get("travel_cost") is None else str(raw["travel_cost"]),
            knowledge_gate=None if raw.get("knowledge_gate") is None else str(raw["knowledge_gate"]),
            relationship=None if raw.get("relationship") is None else int(raw["relationship"]),
            when=None if raw.get("when") is None else str(raw["when"]),
        )


class Graph:
    """One family's nodes and edges, with the family contract enforced on construction."""

    def __init__(self, family: Family, *, version: int = 1) -> None:
        if family.is_deferred:
            raise GraphError(f"{ASTRAL_DEFERRED}")
        self.family = family
        self.version = version
        self._nodes: dict[str, Node] = {}
        self._edges: dict[str, Edge] = {}

    # -- construction -------------------------------------------------------------------------
    def add_node(self, node: Node) -> Node:
        if node.family is not self.family:
            raise GraphError(f"{node.node_id!r} belongs to {node.family.value}, not {self.family.value}")
        if node.node_id in self._nodes:
            raise GraphError(f"duplicate node id {node.node_id!r}")
        self._nodes[node.node_id] = node
        return node

    def add_edge(self, edge: Edge) -> Edge:
        if edge.family is not self.family:
            raise GraphError(f"{edge.edge_id!r} belongs to {edge.family.value}, not {self.family.value}")
        if edge.edge_id in self._edges:
            raise GraphError(f"duplicate edge id {edge.edge_id!r}")
        for end in (edge.source, edge.target):
            if end not in self._nodes:
                raise GraphError(f"{edge.edge_id!r}: unknown node {end!r}")
        self._edges[edge.edge_id] = edge
        return edge

    # -- reading ------------------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, node_id: object) -> bool:
        return node_id in self._nodes

    @property
    def nodes(self) -> tuple[Node, ...]:
        return tuple(self._nodes[key] for key in sorted(self._nodes))

    @property
    def edges(self) -> tuple[Edge, ...]:
        return tuple(self._edges[key] for key in sorted(self._edges))

    def node(self, node_id: str) -> Node:
        try:
            return self._nodes[node_id]
        except KeyError:
            raise GraphError(f"unknown node {node_id!r} in the {self.family.value} graph") from None

    def edge_between(self, a: str, b: str) -> Edge | None:
        for edge in self._edges.values():
            if {edge.source, edge.target} == {a, b}:
                return edge
        return None

    def neighbours(self, node_id: str) -> tuple[str, ...]:
        """Nodes reachable in one step, honouring direction."""
        reachable: set[str] = set()
        for edge in self._edges.values():
            if edge.source == node_id:
                reachable.add(edge.target)
            elif not edge.directed and edge.target == node_id:
                reachable.add(edge.source)
        return tuple(sorted(reachable))

    def validate(self) -> None:
        """Whole-graph checks that a single Node or Edge cannot make on its own."""
        for node in self._nodes.values():
            if node.parent_id is not None:
                parent = self._nodes.get(node.parent_id)
                if parent is None:
                    raise GraphError(f"{node.node_id!r}: unknown parent {node.parent_id!r}")
                if parent.family is not self.family:
                    raise GraphError(f"{node.node_id!r}: parent belongs to another family")
        for node in self._nodes.values():
            if node.location_ref is not None:
                # A cyber device points at a physical node; the reference is checked on load, not copied.
                if node.location_ref in self._nodes:
                    raise GraphError(
                        f"{node.node_id!r}: location_ref {node.location_ref!r} is a {self.family.value} node; "
                        "a cyber device references the physical graph, it does not live in it"
                    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "noopunk.graph",
            "version": self.version,
            "family": self.family.value,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "Graph":
        graph = cls(Family(raw["family"]), version=int(raw.get("version", 1)))
        for node_raw in raw.get("nodes", ()):
            graph.add_node(Node.from_dict(node_raw))
        for edge_raw in raw.get("edges", ()):
            graph.add_edge(Edge.from_dict(edge_raw))
        graph.validate()
        return graph


class World:
    """The four graphs plus who occupies what.

    Occupancy is keyed by ``(actor_id, family)`` on purpose: a hacker's avatar moving through the cyber graph must
    not move the officer's body, and a character's social existence is a node rather than a position.
    """

    def __init__(self, graphs: Iterable[Graph] = ()) -> None:
        self._graphs: dict[Family, Graph] = {}
        for graph in graphs:
            if graph.family in self._graphs:
                raise GraphError(f"duplicate {graph.family.value} graph")
            graph.validate()
            self._graphs[graph.family] = graph
        self._occupancy: dict[tuple[str, Family], str] = {}

    # -- graphs -------------------------------------------------------------------------------
    def graph(self, family: Family) -> Graph:
        if family.is_deferred:
            raise GraphError(f"{ASTRAL_DEFERRED}")
        try:
            return self._graphs[family]
        except KeyError:
            raise GraphError(f"no {family.value} graph in this world") from None

    def add_graph(self, graph: Graph) -> Graph:
        if graph.family in self._graphs:
            raise GraphError(f"duplicate {graph.family.value} graph")
        graph.validate()
        self._graphs[graph.family] = graph
        return graph

    # -- occupancy ----------------------------------------------------------------------------
    def place(self, actor_id: str, node_id: str) -> None:
        """Put a character or avatar at a place node.

        Refused when the target is a social node (characters *are* those nodes), a story node (a scene is not a
        place), or when the id is already a place — a location cannot walk into a room.
        """
        if not actor_id:
            raise GraphError("an occupant needs an id")
        holders = [graph for graph in self._graphs.values() if node_id in graph]
        if not holders:
            raise GraphError(f"unknown node {node_id!r}")
        graph = holders[0]
        if not graph.family.is_place_family:
            raise GraphError(
                f"{node_id!r} is a {graph.family.value} node; characters occupy places, and only the social graph "
                "has character nodes"
            )
        if actor_id in graph:
            raise GraphError(f"{actor_id!r} is a node id; an occupant cannot be a location or a scene")
        self._occupancy[(actor_id, graph.family)] = node_id

    def at(self, actor_id: str, family: Family = Family.PHYSICAL) -> str | None:
        return self._occupancy.get((actor_id, family))

    def occupants(self, node_id: str) -> tuple[str, ...]:
        return tuple(sorted(actor for (actor, _), place in self._occupancy.items() if place == node_id))

    def co_located(self, first: str, second: str, family: Family = Family.PHYSICAL) -> bool:
        """Two characters can interact when they occupy the same place in the same family."""
        here = self.at(first, family)
        return here is not None and here == self.at(second, family)

    # -- movement -----------------------------------------------------------------------------
    def available_moves(self, actor_id: str, family: Family = Family.PHYSICAL) -> tuple[str, ...]:
        here = self.at(actor_id, family)
        if here is None:
            return ()
        return self.graph(family).neighbours(here)

    def move(self, actor_id: str, target_id: str, family: Family = Family.PHYSICAL) -> str:
        """Move along one edge. Social links are relationships, not routes, and never move anyone."""
        if family is Family.SOCIAL:
            raise GraphError("social edges are relationships, not routes; use them for reactions, not travel")
        here = self.at(actor_id, family)
        if here is None:
            raise GraphError(f"{actor_id!r} is not in the {family.value} graph")
        graph = self.graph(family)
        if target_id not in graph:
            raise GraphError(f"unknown node {target_id!r}")
        if target_id not in graph.neighbours(here):
            raise GraphError(f"no {family.value} edge from {here!r} to {target_id!r}")
        self._occupancy[(actor_id, family)] = target_id
        return target_id

    # -- story --------------------------------------------------------------------------------
    def available_scenes(self, episode_id: str, flags: Iterable[str]) -> tuple[str, ...]:
        """Story transitions from an episode that the current flags permit."""
        held = set(flags)
        graph = self.graph(Family.STORY)
        out: list[str] = []
        for edge in graph.edges:
            if edge.source != episode_id:
                continue
            if edge.when is None or edge.when in held:
                out.append(edge.target)
        return tuple(sorted(set(out)))

    def required_scenes(self, episode_id: str) -> tuple[str, ...]:
        """The scenes an episode promises, which no single check may hide."""
        node = self.graph(Family.STORY).node(episode_id)
        return tuple(sorted(str(s) for s in node.metadata.get("required_scenes", ())))

    def verify_required_scenes(self, episode_id: str) -> None:
        graph = self.graph(Family.STORY)
        for scene_id in self.required_scenes(episode_id):
            if scene_id not in graph:
                raise GraphError(f"{episode_id!r}: required scene {scene_id!r} does not exist")
            if graph.node(scene_id).kind != "scene":
                raise GraphError(f"{episode_id!r}: required node {scene_id!r} is not a scene")

    # -- serialization ------------------------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "noopunk.world",
            "version": 1,
            "graphs": [self._graphs[family].to_dict() for family in sorted(self._graphs, key=lambda f: f.value)],
            "occupancy": [
                {"actor_id": actor, "family": family.value, "node_id": node}
                for (actor, family), node in sorted(self._occupancy.items(), key=lambda item: (item[0][0], item[0][1].value))
            ],
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "World":
        world = cls(Graph.from_dict(item) for item in raw.get("graphs", ()))
        for entry in raw.get("occupancy", ()):
            actor = str(entry["actor_id"])
            node = str(entry["node_id"])
            world.place(actor, node)
            if Family(entry.get("family", "physical")) is not world.graph(_family_of(world, node)).family:
                raise GraphError(f"occupancy for {actor!r} names the wrong family for {node!r}")
        return world


def _family_of(world: World, node_id: str) -> Family:
    for family in world._graphs:  # noqa: SLF001 - same module
        if node_id in world._graphs[family]:
            return family
    raise GraphError(f"unknown node {node_id!r}")


def physical_from_helsinki(path: str | Path, *, routes: Iterable[tuple[str, str]] = ()) -> Graph:
    """Build the physical graph from the existing `data/world/helsinki_locations.json`.

    The file has places and a start node but no routes, so routes are supplied by the caller rather than invented
    here. Districts become parent nodes so the hierarchy is world → district → location.
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    graph = Graph(Family.PHYSICAL)
    districts: dict[str, str] = {}
    for entry in raw.get("nodes", ()):
        district = str(entry.get("district", "")).strip()
        if district and district not in districts:
            district_id = "district_" + district.split("/")[0].strip().lower().replace(" ", "_")
            districts[district] = district_id
            if district_id not in graph:
                graph.add_node(Node(district_id, Family.PHYSICAL, "district", label=district))
    for entry in raw.get("nodes", ()):
        node_id = str(entry["id"])
        district = str(entry.get("district", "")).strip()
        graph.add_node(
            Node(
                node_id,
                Family.PHYSICAL,
                "location",
                label=str(entry.get("name", node_id)),
                parent_id=districts.get(district),
                tags=tuple(str(tag) for tag in entry.get("tags", ())),
                metadata={
                    "start": node_id == raw.get("start"),
                    "actions": list(entry.get("actions", ())),
                    "description": str(entry.get("description", "")),
                },
            )
        )
    for index, (source, target) in enumerate(routes, start=1):
        graph.add_edge(
            Edge(f"route_{index}_{source}_{target}", Family.PHYSICAL, source, target, relation="route",
                 travel_cost="scene")
        )
    graph.validate()
    return graph
