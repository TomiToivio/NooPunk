"""Projection from the shared world state to a board — as an explicit argument, not an integration.

The issue says to "integrate with existing interfaces/state rather than force this exact tree". But
`strategy_game/docs/RULE_SYSTEM_RESEARCH.md` reserves:

    Gate D: explicit integration contract and prototype playtest.

and wiring a new subsystem into the shared container **is** the Gate D decision. So this module does
not touch :class:`strategy_game.core.WorldState`; it *reads* one and returns a new
:class:`~strategy_game.tabletop.board.Board`. The consequence is deliberate: a renderer has something
real to draw today, the world model gains no new field, and when the author opens Gate D the only
change needed is to delete the argument and read the board off the state.

Two properties are contractual and are asserted in the tests:

* **Nothing is copied by reference and nothing is mutated.** The projection builds fresh
  :class:`~strategy_game.tabletop.board.BoardNode` objects; ``world.to_json()`` is byte-identical
  before and after.
* **No edge kind is inferred.** :class:`strategy_game.core.NetworkEdge` carries only ``source``,
  ``target`` and a free-text ``layer``. The projection preserves that ``layer`` verbatim and uses the
  neutral :attr:`~strategy_game.tabletop.board.EdgeKind.COMMUNICATION` default for ``kind`` — it does
  not dress a guess up as data. The authoritative label stays where the author put it.

Node kinds mirror what the world state already distinguishes: ``locations`` are ``physical``
``location`` nodes, ``factions`` are ``social`` ``faction`` nodes. Characters, institutions and
social-system abstractions are not invented here; a later approved scenario supplies those nodes.

## The first board with content on it (#347's own step 1)

``board_from_world`` draws whatever the world state holds, which on a fresh state is nothing. The one
piece of **complete authored local content in the crossover** is ``data/ukweli_local.json`` (the
Republic of Ukweli slice, #322/#324), and the board the issue describes — a layered network society
with places, factions and people — can be projected from it without inventing a single record:

* locations → ``physical`` ``location`` nodes; parties → ``social`` ``faction`` nodes; leaders →
  ``social`` ``person`` nodes;
* routes → ``travel`` edges on ``physical``; relationships → ``social`` edges;
* every identifier is preserved verbatim, and every edge's id is derived from its two endpoints, so it
  survives a reordering of the source;
* :meth:`strategy_game.tabletop.board.Board.validate` must pass.

The mapping is **data, not code**: ``data/board_local.json`` declares which source collection becomes
which kind and layer, it declares the cosmetic layout, and it declares what is reserved. So a new
place, faction or person enters the board by editing the slice data alone — which is exactly the
modding test the issue asks for.

Two exclusions are the point of this function:

* **No number is carried.** The slice holds illustrative quantities (``pressure``, ``trust``,
  ``legitimacy_delta``, a per-leader ``skill``). None of them may reach the shared board model, or a
  prototype's number becomes an unapproved rule by the back door. The projection reads identity,
  topology, layer, kind and declared tags, and nothing else.
* **No piece is invented.** The slice declares no token and no position, so no piece is projected and
  no leader is placed "on" a location; that reading would be an added semantic.

Layout stays outside the board, as the model requires, and a binding that lays out a node the board no
longer has is **refused** rather than quietly ignored.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from ..core import WorldState
from .board import Board, BoardEdge, BoardNode, EdgeKind, Layout

#: The declared format, so a caller cannot silently load a different document.
BOARD_BINDING_FORMAT = "noopunk.strategy_game.board_binding"

#: The binding that turns the one complete local slice into a board. Kept as data so the mapping — and
#: the cosmetic layout — can be edited without touching code (#347's modding ask).
BOARD_BINDING_DATA = Path(__file__).resolve().parents[1] / "data" / "board_local.json"


class BoardBindingError(ValueError):
    """Raised for a binding that is not one, or a layout that describes nodes the board does not have."""


def _strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _label(item: Mapping[str, Any]) -> str:
    return str(item.get("name") or item.get("label") or item.get("id") or "")


def _edge_kind(value: Any) -> EdgeKind:
    """A declared edge kind, or the neutral default. An undeclared kind is never invented."""
    if isinstance(value, str) and value in {kind.value for kind in EdgeKind}:
        return EdgeKind(value)
    return EdgeKind.COMMUNICATION


def load_board_binding(path: Path | str | None = None) -> dict[str, Any]:
    """Read a board binding, refusing a document that is not one."""
    target = Path(path) if path is not None else BOARD_BINDING_DATA
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("format") != BOARD_BINDING_FORMAT:
        raise BoardBindingError(f"not a NoöPunk board binding: format={data.get('format')!r}")
    for key in ("slice", "board_identifier", "node_bindings", "edge_bindings"):
        if key not in data:
            raise BoardBindingError(f"the board binding is missing {key!r}")
    return data


def board_from_local_slice(
    slice_data: Mapping[str, Any],
    binding: Mapping[str, Any],
) -> Board:
    """Project a parsed local slice onto a layered board. Pure: the slice is not modified.

    ``binding`` is passed in rather than read here, for the same reason :func:`board_from_world` takes
    its state as an argument: joining a new subsystem to the shared world is the Gate D decision, and a
    projection with an explicit argument performs no gate. Nothing in this function reads a numeric
    field of the slice.
    """
    board = Board(identifier=str(binding.get("board_identifier") or "local-slice"))
    node_bindings = binding.get("node_bindings") or {}
    for family in ("locations", "parties", "leaders"):
        rules = node_bindings.get(family)
        if rules is None:
            raise BoardBindingError(f"the board binding does not bind {family!r}")
        for item in slice_data.get(family) or ():
            identifier = str(item.get("id") or "")
            if not identifier:
                continue  # a record with no id cannot be a node, and an invented id would be a lie
            board.add_node(
                BoardNode(
                    identifier=identifier,
                    label=_label(item),
                    kind=str(rules.get("kind") or "location"),
                    layer=str(rules.get("layer") or "physical"),
                    tags=_strings(item.get("tags")),
                )
            )

    edge_bindings = binding.get("edge_bindings") or {}
    route_rules = edge_bindings.get("routes") or {}
    for pair in slice_data.get("routes") or ():
        if not isinstance(pair, (list, tuple)) or len(pair) < 2:
            continue
        source, target = str(pair[0]), str(pair[1])
        # Skipping is honest: a dangling edge would be a false statement about the map, and inventing
        # its endpoint is worse. Same behaviour as board_from_world.
        if source not in board.nodes or target not in board.nodes:
            continue
        board.add_edge(
            BoardEdge(
                identifier=f"route-{source}-{target}",
                source=source,
                target=target,
                kind=_edge_kind(route_rules.get("kind")),
                layer=str(route_rules.get("layer") or "physical"),
                notes=(
                    "projected from the slice's declared routes; direction, meaning and control are "
                    "not implied"
                ),
            )
        )

    relationship_rules = edge_bindings.get("relationships") or {}
    kind_from_tags = relationship_rules.get("kind_from_tags") or {}
    for item in slice_data.get("relationships") or ():
        source, target = str(item.get("a") or ""), str(item.get("b") or "")
        if source not in board.nodes or target not in board.nodes:
            continue
        tags = _strings(item.get("tags"))
        mapped_kind = next((kind_from_tags[tag] for tag in tags if tag in kind_from_tags), None)
        declared = mapped_kind if mapped_kind is not None else relationship_rules.get("kind")
        board.add_edge(
            BoardEdge(
                identifier=f"relationship-{source}-{target}",
                source=source,
                target=target,
                kind=_edge_kind(declared),
                layer=str(relationship_rules.get("layer") or "social"),
                notes=(
                    "projected from the slice's declared relationships; the source declares no kind, "
                    "and the declared tags are kept verbatim: "
                    + (", ".join(tags) if tags else "(none)")
                ),
            )
        )

    board.validate()
    return board


def layout_from_slice_binding(binding: Mapping[str, Any], board: Board) -> Layout:
    """Read the cosmetic layout the binding declares, refusing one that describes a node that is gone.

    Layout is deliberately not part of :class:`Board`, so this can be recomputed or replaced without
    touching the graph — the issue's "no force-directed graph jitter during gameplay" is then a caching
    decision rather than a hope.
    """
    positions = (binding.get("layout") or {}).get("positions") or {}
    stale = sorted(set(positions) - set(board.nodes))
    if stale:
        raise BoardBindingError(
            f"the binding lays out nodes that are not on the board: {stale}"
        )
    layout = Layout()
    for node_id, point in positions.items():
        layout.set(str(node_id), float(point[0]), float(point[1]))
    return layout


def local_slice_board(binding_path: Path | str | None = None) -> tuple[Board, Layout]:
    """The first non-empty board, and its declared cosmetic layout, read from the packaged data."""
    binding_file = Path(binding_path) if binding_path is not None else BOARD_BINDING_DATA
    binding = load_board_binding(binding_file)
    slice_file = binding_file.parent / str(binding["slice"])
    slice_data = json.loads(slice_file.read_text(encoding="utf-8"))
    board = board_from_local_slice(slice_data, binding)
    return board, layout_from_slice_binding(binding, board)


def board_from_world(state: WorldState, *, identifier: str = "world") -> Board:
    """Read ``state`` and return a board projection. The state is not modified."""
    board = Board(identifier=identifier)
    for location in state.locations:
        board.add_node(
            BoardNode(
                identifier=location.identifier,
                label=location.label,
                kind="location",
                layer="physical",
            )
        )
    for faction in state.factions:
        board.add_node(
            BoardNode(
                identifier=faction.identifier,
                label=faction.name,
                kind="faction",
                layer="social",
            )
        )
    for index, edge in enumerate(state.edges):
        # An edge may reference a node kind this projection does not create (a leader, an asset).
        # Skipping is honest: a dangling edge would be a lie, and inventing its endpoint is worse.
        if edge.source not in board.nodes or edge.target not in board.nodes:
            continue
        board.add_edge(
            BoardEdge(
                identifier=f"world-edge-{index:04d}",
                source=edge.source,
                target=edge.target,
                kind=EdgeKind.COMMUNICATION,
                layer=edge.layer,
                notes="projected from WorldState.edges; kind not declared by the source record",
            )
        )
    board.validate()
    return board
