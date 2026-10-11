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
        # #282 moved provenance from a bare string to a structured record, so the origin is now
        # carried on `.source` (kind stays UNKNOWN for an unclassified legacy value).
        self.assertEqual(restored.events[0].provenance.source, "author:TBD")

    def test_to_json_is_json_and_carries_every_collection(self):
        import json
        from dataclasses import fields as dataclass_fields

        payload = json.loads(WorldState().to_json())
        # Derived, not a frozen literal. Issue #282 added the Layer II political collections to
        # `WorldState`, and a hard-coded set would go stale on every future addition instead of
        # failing for a real reason. Deriving the expectation keeps this test's actual intent --
        # *every declared collection is carried* -- and makes a collection that serializes under
        # the wrong key impossible to miss.
        self.assertEqual(set(payload), {f.name for f in dataclass_fields(WorldState)})

    def test_containers_default_to_empty_and_are_not_shared(self):
        first, second = WorldState(), WorldState()
        first.factions.append(Faction("faction", "Example faction"))
        self.assertEqual(second.factions, [])


if __name__ == "__main__":
    unittest.main()
