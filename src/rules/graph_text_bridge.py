"""#1178: read-only projection of the existing text-game rooms into a Physical graph.

The `World` owns actors, inventories, exits and actions; this adapter does not
modify World or install a competing movement resolver. Rebuild the projection
after game actions to observe current positions.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .four_graphs import Place, Route, SpatialGraph, GraphContractError

if TYPE_CHECKING:
    from src.text_game.model import World


def physical_from_text_world(world: "World") -> SpatialGraph:
    """Export existing room topology/occupancy, without mutating actor records."""
    world.validate()
    nodes = {room_id: Place(id=room_id, label=room.label, kind="room")
             for room_id, room in world.rooms.items()}
    edges = tuple(Route(source=room_id, target=destination,
                        id=f"text_exit:{room_id}:{exit_name}", directed=True)
                  for room_id, room in world.rooms.items()
                  for exit_name, destination in room.exits.items())
    positions = {actor_id: actor.room_id for actor_id, actor in world.actors.items()}
    return SpatialGraph("physical", nodes, edges, positions)


def validate_text_world_parity(world: "World", graph: SpatialGraph) -> None:
    """Guard against a stale graph snapshot accidentally becoming actor authority."""
    if graph.to_dict() != physical_from_text_world(world).to_dict():
        raise GraphContractError("Physical view stale: rebuild from authoritative World")
