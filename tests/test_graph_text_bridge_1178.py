"""Read-only text-game Physical graph parity, issue #1178."""
import unittest

from src.rules.graph_text_bridge import (
    physical_from_text_world,
    validate_text_world_parity,
)
from src.text_game.model import fixture_world
from src.world.graphs import GraphError as GraphContractError


class TextWorldBridgeTests(unittest.TestCase):
    def test_room_edges_and_actors_project_without_cloning(self):
        world = fixture_world(with_sheets=False)
        projected = physical_from_text_world(world)
        actor = next(iter(world.actors))
        self.assertEqual(projected.occupants[actor], world.actors[actor].room_id)
        self.assertNotIn(actor, projected.nodes)
        self.assertTrue(projected.adjacent("fixture:hub"))
        self.assertEqual(projected.nodes["fixture:hub"].kind, "room")
        validate_text_world_parity(world, projected)

    def test_world_remains_authority_after_character_moves(self):
        world = fixture_world(with_sheets=False)
        graph = physical_from_text_world(world)
        world.actors["fixture:human"].room_id = "fixture:goal"
        with self.assertRaises(GraphContractError):
            validate_text_world_parity(world, graph)
        rebuilt = physical_from_text_world(world)
        self.assertEqual(rebuilt.occupants["fixture:human"], "fixture:goal")
        self.assertEqual(graph.occupants["fixture:human"], "fixture:hub")
        validate_text_world_parity(world, rebuilt)


if __name__ == "__main__":
    unittest.main()
