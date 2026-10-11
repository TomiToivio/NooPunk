"""Only runtime behavior is tested; no lore or rulebook text assertions."""
import unittest

from strategy_game.core import Asset, Faction, Leader, Location, NetworkEdge, WorldState
from strategy_game.view import board_view


class ScaffoldTests(unittest.TestCase):
    def test_empty_state(self):
        original = WorldState()
        restored = WorldState.from_json(original.to_json())
        self.assertEqual(restored, original)
        self.assertEqual(board_view(restored)["network_edges"], [])

    def test_roundtrip_preserves_unknown_author_attributes(self):
        original = WorldState(
            leaders=[Leader("leader", "Example", {"author_defined": "TBD"}, ["example"])],
            factions=[Faction("faction", "Example faction", "leader", ["asset"])],
            assets=[Asset("asset", "Example asset", "location", "faction")],
            locations=[Location("location", "Example location", 60.0, 25.0)],
            edges=[NetworkEdge("faction", "leader", "example")],
        )
        restored = WorldState.from_json(original.to_json())
        self.assertEqual(restored, original)
        self.assertEqual(board_view(restored)["locations"][0]["id"], "location")


if __name__ == "__main__":
    unittest.main()
