"""The network-society board: layered nodes, typed edges, pieces — and cosmetic layout kept apart.

Issue #347 asks for a board that "represents the whole Earth as an extremely abstract network
society", not an operationally detailed political map: "Nodes are playable places, actors or
social-system abstractions with cards/tags/actions; edges have small meaningful types/states".

Two modelling decisions come straight from the issue and from
``strategy_game/docs/INTEGRATION_BOUNDARIES.md``:

* **Topology is treated separately from cosmetic positions.** :class:`Board` holds nodes, edges and
  pieces and knows nothing about where anything is drawn. :class:`Layout` holds the coordinates. A
  force-directed layout can therefore be recomputed without touching the graph, and the issue's
  "no force-directed graph jitter during gameplay" is achievable by freezing a layout instead of
  freezing the board.
* **The layers are overlay toggles, not separate boards.** The four names in :data:`BOARD_LAYERS` are
  the *suggested* overlays the issue lists; ``layer`` is a free string on nodes and edges, exactly as
  the existing :class:`strategy_game.core.NetworkEdge` already stores it, so a new overlay does not
  break the model and the four are not promoted into a closed vocabulary.

Nothing here decides what an edge costs, what an action does, or who may move a piece. Edges carry a
*type* so a renderer can draw them differently and a later approved rule layer can read them; this
module never acts on one.

Reserved: travel and communication *rules*, action eligibility, control/ownership inference, and
victory conditions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping


class BoardError(ValueError):
    """Raised for an inconsistent board, such as an edge referencing a missing node."""


#: The overlay layers the issue suggests as toggles. Advisory, not a closed set: ``layer`` is a free
#: string so a new overlay is a data change, and these four are not enforced on every node.
BOARD_LAYERS: tuple[str, ...] = ("physical", "cyber", "astral", "social")


class EdgeKind(Enum):
    """The small set of edge types the issue names. A drawing/semantic category, not a mechanic.

    "edges have small meaningful types/states (influence, alliance, communication, travel, opposition,
    institutional cooperation)". No traversal, cost or permission is derived from a kind here.
    """

    INFLUENCE = "influence"
    ALLIANCE = "alliance"
    COMMUNICATION = "communication"
    TRAVEL = "travel"
    OPPOSITION = "opposition"
    COOPERATION = "cooperation"


#: The declared value set, so callers can validate without constructing an enum member.
EDGE_KINDS: tuple[str, ...] = tuple(kind.value for kind in EdgeKind)


@dataclass
class BoardNode:
    """A playable place, actor or social-system abstraction.

    ``kind`` is a free string (``location``, ``faction``, ``organization``, ``institution``,
    ``person``, ``social_system``, ...). The issue lists kinds but does not close the list, so the
    model does not either.
    """

    identifier: str
    label: str
    kind: str = "location"
    #: Overlay layer. One of :data:`BOARD_LAYERS` by convention; not enforced.
    layer: str = "physical"
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise BoardError("a board node needs a non-empty identifier")
        self.tags = tuple(str(tag) for tag in self.tags)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "label": self.label,
            "kind": self.kind,
            "layer": self.layer,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> BoardNode:
        return cls(
            identifier=str(data.get("identifier", "")),
            label=str(data.get("label", "")),
            kind=str(data.get("kind", "location")),
            layer=str(data.get("layer", "physical")),
            tags=tuple(str(tag) for tag in (data.get("tags") or ())),
        )


@dataclass
class BoardEdge:
    """A typed relation between two nodes.

    Carries no state beyond its type and layer: the issue says edges "have small meaningful
    types/states", and inventing a numeric weight here would be an unapproved mechanic.
    """

    identifier: str
    source: str
    target: str
    kind: EdgeKind = EdgeKind.COMMUNICATION
    layer: str = "social"
    notes: str = ""

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise BoardError("a board edge needs a non-empty identifier")
        if self.source == self.target:
            raise BoardError(f"edge {self.identifier!r} links node {self.source!r} to itself")

    @property
    def endpoints(self) -> tuple[str, str]:
        return (self.source, self.target)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "source": self.source,
            "target": self.target,
            "kind": self.kind.value,
            "layer": self.layer,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> BoardEdge:
        raw_kind = str(data.get("kind", EdgeKind.COMMUNICATION.value))
        return cls(
            identifier=str(data.get("identifier", "")),
            source=str(data.get("source", "")),
            target=str(data.get("target", "")),
            kind=EdgeKind(raw_kind) if raw_kind in EDGE_KINDS else EdgeKind.COMMUNICATION,
            layer=str(data.get("layer", "social")),
            notes=str(data.get("notes", "")),
        )


@dataclass
class BoardPiece:
    """A token standing on a node: an agent, a unit, a team.

    The issue allows one character to lead troops, netrunners or remote viewers "in abstract
    strategic operations", so a piece is an abstract marker. What it may do is not modelled.
    """

    identifier: str
    node_id: str
    kind: str = "agent"
    owner_id: str | None = None

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise BoardError("a board piece needs a non-empty identifier")

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "node_id": self.node_id,
            "kind": self.kind,
            "owner_id": self.owner_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> BoardPiece:
        return cls(
            identifier=str(data.get("identifier", "")),
            node_id=str(data.get("node_id", "")),
            kind=str(data.get("kind", "agent")),
            owner_id=None if data.get("owner_id") is None else str(data["owner_id"]),
        )


@dataclass
class Layout:
    """Cosmetic positions, deliberately outside :class:`Board`.

    A layout is a cached drawing decision, not world state. Recomputing one must never change the
    graph, which is why it is a separate object and why :class:`Board` has no coordinate field.
    """

    positions: dict[str, tuple[float, float]] = field(default_factory=dict)

    def set(self, node_id: str, x: float, y: float) -> None:
        self.positions[node_id] = (float(x), float(y))

    def get(self, node_id: str) -> tuple[float, float] | None:
        return self.positions.get(node_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "positions": {
                key: [value[0], value[1]] for key, value in sorted(self.positions.items())
            }
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Layout:
        positions: dict[str, tuple[float, float]] = {}
        for key, value in (data.get("positions") or {}).items():
            positions[str(key)] = (float(value[0]), float(value[1]))
        return cls(positions=positions)


@dataclass
class Board:
    """Layered nodes, typed edges and pieces. A graph container, not a simulation."""

    identifier: str = "main"
    nodes: dict[str, BoardNode] = field(default_factory=dict)
    edges: dict[str, BoardEdge] = field(default_factory=dict)
    pieces: dict[str, BoardPiece] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise BoardError("a board needs a non-empty identifier")

    # -- mutation ---------------------------------------------------------------------------------

    def add_node(self, node: BoardNode) -> BoardNode:
        if node.identifier in self.nodes:
            raise BoardError(f"board {self.identifier!r} already has a node {node.identifier!r}")
        self.nodes[node.identifier] = node
        return node

    def add_edge(self, edge: BoardEdge) -> BoardEdge:
        if edge.identifier in self.edges:
            raise BoardError(f"board {self.identifier!r} already has an edge {edge.identifier!r}")
        for endpoint in edge.endpoints:
            if endpoint not in self.nodes:
                raise BoardError(
                    f"edge {edge.identifier!r} references node {endpoint!r}, which is not on the board"
                )
        self.edges[edge.identifier] = edge
        return edge

    def add_piece(self, piece: BoardPiece) -> BoardPiece:
        if piece.identifier in self.pieces:
            raise BoardError(f"board {self.identifier!r} already has a piece {piece.identifier!r}")
        if piece.node_id not in self.nodes:
            raise BoardError(
                f"piece {piece.identifier!r} stands on node {piece.node_id!r}, "
                "which is not on the board"
            )
        self.pieces[piece.identifier] = piece
        return piece

    def move_piece(self, piece_id: str, node_id: str) -> None:
        """Move a piece to another node. Legality is not checked, because legality is a rule."""
        if piece_id not in self.pieces:
            raise BoardError(f"board {self.identifier!r} has no piece {piece_id!r}")
        if node_id not in self.nodes:
            raise BoardError(f"cannot move piece {piece_id!r} to unknown node {node_id!r}")
        self.pieces[piece_id].node_id = node_id

    # -- queries ----------------------------------------------------------------------------------

    def neighbors(self, node_id: str, *, layer: str | None = None,
                  kind: EdgeKind | None = None) -> tuple[str, ...]:
        """Adjacent nodes, in edge-insertion order.

        Filters are by layer and edge kind only. There is no path cost, range or reachability model:
        whether a player may *use* a link is a strategy rule and is not approved.
        """
        if node_id not in self.nodes:
            raise BoardError(f"board {self.identifier!r} has no node {node_id!r}")
        found: list[str] = []
        for edge in self.edges.values():
            if layer is not None and edge.layer != layer:
                continue
            if kind is not None and edge.kind is not kind:
                continue
            if edge.source == node_id:
                found.append(edge.target)
            elif edge.target == node_id:
                found.append(edge.source)
        return tuple(found)

    def nodes_in_layer(self, layer: str) -> tuple[BoardNode, ...]:
        return tuple(node for node in self.nodes.values() if node.layer == layer)

    def pieces_on(self, node_id: str) -> tuple[BoardPiece, ...]:
        return tuple(piece for piece in self.pieces.values() if piece.node_id == node_id)

    def validate(self) -> None:
        """Re-check every invariant, for a board assembled or loaded from elsewhere."""
        for edge in self.edges.values():
            for endpoint in edge.endpoints:
                if endpoint not in self.nodes:
                    raise BoardError(
                        f"edge {edge.identifier!r} references node {endpoint!r}, "
                        "which is not on the board"
                    )
        for piece in self.pieces.values():
            if piece.node_id not in self.nodes:
                raise BoardError(
                    f"piece {piece.identifier!r} stands on node {piece.node_id!r}, "
                    "which is not on the board"
                )

    # -- serialization ----------------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "nodes": {key: self.nodes[key].to_dict() for key in sorted(self.nodes)},
            "edges": {key: self.edges[key].to_dict() for key in sorted(self.edges)},
            "pieces": {key: self.pieces[key].to_dict() for key in sorted(self.pieces)},
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Board:
        board = cls(identifier=str(data.get("identifier", "main")))
        for key, payload in (data.get("nodes") or {}).items():
            board.nodes[str(key)] = BoardNode.from_dict(payload)
        for key, payload in (data.get("edges") or {}).items():
            board.edges[str(key)] = BoardEdge.from_dict(payload)
        for key, payload in (data.get("pieces") or {}).items():
            board.pieces[str(key)] = BoardPiece.from_dict(payload)
        return board

    @classmethod
    def from_records(cls, nodes: Iterable[BoardNode], edges: Iterable[BoardEdge] = (),
                     pieces: Iterable[BoardPiece] = (), identifier: str = "main") -> Board:
        """Assemble a board, raising on the first inconsistency rather than repairing it."""
        board = cls(identifier=identifier)
        for node in nodes:
            board.add_node(node)
        for edge in edges:
            board.add_edge(edge)
        for piece in pieces:
            board.add_piece(piece)
        return board
