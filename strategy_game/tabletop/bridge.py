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
"""
from __future__ import annotations

from ..core import WorldState
from .board import Board, BoardEdge, BoardNode, EdgeKind


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
