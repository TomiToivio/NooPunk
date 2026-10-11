"""Only runtime behavior is tested; no lore or rulebook text assertions."""
import unittest

from strategy_game.core import (
    Asset,
    Event,
    Faction,
    Leader,
    Location,
    NetworkEdge,
    WorldState,
)
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


class ContractTests(unittest.TestCase):
    """Runtime contracts only. No lore, rulebook or design-text assertions (#271)."""

    def test_every_container_type_survives_a_round_trip(self):
        # Event is the one container the tests above never construct, so a regression in its
        # serialisation would otherwise be invisible.
        original = WorldState(
            events=[Event("event", "Example event", provenance="author:TBD")]
        )
        restored = WorldState.from_json(original.to_json())
        self.assertEqual(restored, original)
        self.assertEqual(restored.events[0].provenance, "author:TBD")

    def test_to_json_is_json_and_carries_every_collection(self):
        import json
        payload = json.loads(WorldState().to_json())
        self.assertEqual(
            set(payload),
            {"schema_version", "leaders", "factions", "assets", "locations", "edges", "events"},
        )

    def test_containers_default_to_empty_and_are_not_shared(self):
        first, second = WorldState(), WorldState()
        first.factions.append(Faction("faction", "Example faction"))
        self.assertEqual(second.factions, [])


if __name__ == "__main__":
    unittest.main()
