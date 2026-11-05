"""#1178: read-only projection of the existing text-game rooms into a Physical graph.

The `World` owns actors, inventories, exits and actions; this adapter does not
modify World or install a competing movement resolver. Rebuild the projection
after game actions to observe current positions.

Since the #1178 graph merge this targets the single runtime model,
`src/world/graphs.py::PhysicalGraph` — the earlier `four_graphs` duplicate is gone.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

try:  # imported as src.rules.graph_text_bridge
    from ..world.graphs import GraphError, LocationNode, PhysicalGraph, PhysicalRoute
except ImportError:  # a caller that put `src` on sys.path
    from world.graphs import (  # type: ignore[no-redef]
        GraphError,
        LocationNode,
        PhysicalGraph,
        PhysicalRoute,
    )

if TYPE_CHECKING:
    from text_game.model import World


def physical_from_text_world(world: World) -> PhysicalGraph:
    """Export existing room topology/occupancy, without mutating actor records."""
    world.validate()
    nodes = {
        room_id: LocationNode(id=room_id, label=room.label, kind="room")
        for room_id, room in world.rooms.items()
    }
    routes = tuple(
        PhysicalRoute(source=room_id, target=destination, directed=True,
                      kind="exit", label=exit_name)
        for room_id, room in world.rooms.items()
        for exit_name, destination in room.exits.items()
    )
    occupants = {actor_id: actor.room_id for actor_id, actor in world.actors.items()}
    return PhysicalGraph(nodes, routes, occupants)


def validate_text_world_parity(world: World, graph: PhysicalGraph) -> None:
    """Guard against a stale graph snapshot accidentally becoming actor authority."""
    if graph.to_dict() != physical_from_text_world(world).to_dict():
        raise GraphError("Physical view stale: rebuild from authoritative World")
