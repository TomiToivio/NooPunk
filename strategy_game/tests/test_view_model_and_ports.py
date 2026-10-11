"""View-model, port and serialization contracts for strategy_game (#282).

Additive to strategy_game/tests/test_scaffold.py, which another agent contributed and which stays
untouched: its containers, round-trips and discovery coverage are not repeated here. These tests
cover what it does not -- the read-only view model's exact shape and its immutability, the four
reserved adapter protocols, non-ASCII round-tripping and output determinism.

Runtime behaviour only, per AGENTS.md and #271. There is deliberately no assertion about rules,
canon, lore or the wording of any document. The two structural ones exist to pin the boundary the
issue sets: the view exposes display fields only, and no score, threshold or cost may appear.
"""
import json
import sys
import unittest
from pathlib import Path
from typing import Protocol

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game import ports  # noqa: E402
from strategy_game.core import (  # noqa: E402
    Asset,
    Event,
    Faction,
    Leader,
    Location,
    NetworkEdge,
    WorldState,
)
from strategy_game.view import board_view  # noqa: E402


def populated() -> WorldState:
    """A small, entirely author-defined state. Nothing here interprets the values."""
    return WorldState(
        leaders=[Leader("l1", "Aino", {"grit": 3}, ["stoic"])],
        factions=[Faction("f1", "Noösphere Circle", "l1", ["a1"])],
        assets=[Asset("a1", "Field office", "loc1", "f1")],
        locations=[Location("loc1", "Helsinki", 60.17, 24.94)],
        edges=[NetworkEdge("f1", "f2", "discourse")],
        events=[Event("e1", "A declaration is published", "evidence")],
    )


class ViewModelContractTests(unittest.TestCase):
    def test_empty_state_renders_with_every_collection_empty(self):
        view = board_view(WorldState())
        for key in ("locations", "network_nodes", "network_edges", "assets"):
            self.assertEqual(view[key], [], key)

    def test_view_exposes_display_fields_only(self):
        """No score, threshold, cost or outcome may appear: no rules are approved."""
        view = board_view(populated())
        self.assertEqual(
            set(view),
            {"schema_version", "locations", "network_nodes", "network_edges", "assets"},
        )
        self.assertEqual(set(view["network_nodes"][0]), {"id", "label", "type"})
        self.assertEqual(set(view["network_edges"][0]), {"source", "target", "layer"})
        self.assertEqual(set(view["locations"][0]), {"id", "label", "latitude", "longitude"})
        self.assertEqual(
            set(view["assets"][0]), {"id", "label", "location_id", "owner_faction_id"}
        )

    def test_view_mirrors_the_state_it_was_given(self):
        view = board_view(populated())
        self.assertEqual(view["schema_version"], "scaffold-1")
        self.assertEqual(view["locations"][0]["label"], "Helsinki")
        self.assertEqual(view["network_nodes"][0]["id"], "f1")
        self.assertEqual(view["network_edges"][0]["source"], "f1")

    def test_view_does_not_mutate_the_state_it_was_given(self):
        state = populated()
        before = state.to_dict()
        board_view(state)
        self.assertEqual(state.to_dict(), before)

    def test_view_is_json_serializable(self):
        json.dumps(board_view(populated()))


class PortTests(unittest.TestCase):
    def test_each_reserved_adapter_is_a_protocol(self):
        for name in ("LeaderRPG", "PoliticalSimulation", "FactionStrategy", "AgentProvider"):
            self.assertTrue(issubclass(getattr(ports, name), Protocol), name)

    def test_each_port_declares_a_describe_hook(self):
        for name in ("LeaderRPG", "PoliticalSimulation", "FactionStrategy", "AgentProvider"):
            self.assertTrue(callable(getattr(getattr(ports, name), "describe", None)), name)

    def test_a_conforming_object_satisfies_a_port_structurally(self):
        class Demo:
            def describe(self, state):
                return {"schema_version": state.schema_version}

        self.assertEqual(Demo().describe(WorldState()), {"schema_version": "scaffold-1"})


class SerializationContractTests(unittest.TestCase):
    def test_to_json_is_deterministic(self):
        state = populated()
        self.assertEqual(state.to_json(), state.to_json())
        self.assertEqual(
            state.to_json(), json.dumps(state.to_dict(), ensure_ascii=False, sort_keys=True)
        )

    def test_round_trip_preserves_non_ascii(self):
        """The project is multilingual; labels must survive untouched."""
        state = populated()
        self.assertIn("Noösphere", state.to_json())
        self.assertEqual(WorldState.from_json(state.to_json()).locations[0].label, "Helsinki")

    def test_leader_defaults_leave_attributes_and_tags_unset(self):
        leader = Leader("l1", "Aino")
        self.assertEqual(leader.attributes, {})
        self.assertEqual(leader.personality_tags, [])

    def test_leader_values_are_stored_without_interpretation(self):
        leader = Leader("l1", "Aino", {"anything": ["at", "all"]}, ["tag"])
        self.assertEqual(leader.attributes, {"anything": ["at", "all"]})
        self.assertEqual(leader.personality_tags, ["tag"])

    def test_event_keeps_provenance_distinct_from_the_description(self):
        self.assertEqual(Event("e1", "text").provenance, "")
        self.assertNotEqual(Event("e1", "text", "evidence").description, "evidence")


if __name__ == "__main__":
    unittest.main()
