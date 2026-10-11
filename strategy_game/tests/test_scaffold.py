"""Executable scaffold tests for the separate strategy_game package (#282).

Per AGENTS.md these cover executable code only -- containers, serialization, adapter protocols and
the read-only view model. They deliberately assert nothing about rules, mechanics, canon or the
wording of any document: none are approved, so there is nothing of that kind to test. The tests
that do exist pin the boundary the issue asks for: the containers carry no invented statistics,
and the view model exposes display fields only.
"""
import json
import subprocess
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
        leaders=[Leader("l1", "Aino", {"grit": 3}, ["stoic", "curious"])],
        factions=[Faction("f1", "Noösphere Circle", "l1", ["a1"])],
        assets=[Asset("a1", "Field office", "loc1", "f1")],
        locations=[Location("loc1", "Helsinki", 60.17, 24.94)],
        edges=[NetworkEdge("f1", "f2", "discourse")],
        events=[Event("e1", "A declaration is published", "evidence")],
    )


class ContainerTests(unittest.TestCase):
    def test_empty_state_defaults_to_no_content(self):
        state = WorldState()
        for name in ("leaders", "factions", "assets", "locations", "edges", "events"):
            self.assertEqual(getattr(state, name), [], name)

    def test_default_collections_are_not_shared_between_instances(self):
        first, second = WorldState(), WorldState()
        first.leaders.append(Leader("l", "n"))
        self.assertEqual(second.leaders, [])

    def test_leader_attributes_and_tags_are_stored_verbatim(self):
        """The scaffold must not invent statistics: whatever the author supplies is what is kept."""
        leader = Leader("l1", "Aino", {"anything": ["at", "all"]}, ["tag"])
        self.assertEqual(leader.attributes, {"anything": ["at", "all"]})
        self.assertEqual(leader.personality_tags, ["tag"])

    def test_leader_defaults_leave_attributes_unset(self):
        leader = Leader("l1", "Aino")
        self.assertEqual(leader.attributes, {})
        self.assertEqual(leader.personality_tags, [])

    def test_event_keeps_provenance_separate_from_description(self):
        event = Event("e1", "text", "evidence")
        self.assertNotEqual(event.description, event.provenance)
        self.assertEqual(Event("e2", "text").provenance, "")


class SerializationTests(unittest.TestCase):
    def test_round_trip_preserves_an_empty_state(self):
        state = WorldState()
        self.assertEqual(WorldState.from_json(state.to_json()), state)
        self.assertEqual(board_view(WorldState.from_json(state.to_json()))["network_edges"], [])

    def test_round_trip_preserves_a_populated_state(self):
        state = populated()
        self.assertEqual(WorldState.from_json(state.to_json()), state)

    def test_round_trip_preserves_unknown_author_attributes(self):
        """Author-defined values survive untouched, including ones the scaffold never reads."""
        state = WorldState(
            leaders=[Leader("leader", "Example", {"author_defined": "TBD"}, ["example"])]
        )
        restored = WorldState.from_json(state.to_json())
        self.assertEqual(restored, state)
        self.assertEqual(restored.leaders[0].attributes, {"author_defined": "TBD"})

    def test_round_trip_preserves_non_ascii(self):
        state = populated()
        text = state.to_json()
        self.assertIn("Noösphere", text)
        self.assertIn("Helsinki", WorldState.from_json(text).locations[0].label)

    def test_to_json_is_deterministic(self):
        state = populated()
        self.assertEqual(state.to_json(), state.to_json())
        self.assertEqual(state.to_json(), json.dumps(state.to_dict(), ensure_ascii=False, sort_keys=True))

    def test_to_dict_is_a_plain_json_compatible_structure(self):
        json.dumps(populated().to_dict())  # raises if any value is not serializable

    def test_schema_version_is_carried_through(self):
        self.assertEqual(WorldState().schema_version, "scaffold-1")
        self.assertEqual(WorldState.from_json(WorldState().to_json()).schema_version, "scaffold-1")


class ViewModelTests(unittest.TestCase):
    def test_empty_state_renders_without_error(self):
        view = board_view(WorldState())
        self.assertEqual(view["locations"], [])
        self.assertEqual(view["network_nodes"], [])
        self.assertEqual(view["network_edges"], [])
        self.assertEqual(view["assets"], [])

    def test_view_exposes_display_fields_only(self):
        """No score, threshold, cost or outcome may appear: there are no approved rules."""
        view = board_view(populated())
        self.assertEqual(
            set(view),
            {"schema_version", "locations", "network_nodes", "network_edges", "assets"},
        )
        self.assertEqual(set(view["network_nodes"][0]), {"id", "label", "type"})
        self.assertEqual(set(view["network_edges"][0]), {"source", "target", "layer"})
        self.assertEqual(set(view["locations"][0]), {"id", "label", "latitude", "longitude"})
        self.assertEqual(set(view["assets"][0]), {"id", "label", "location_id", "owner_faction_id"})

    def test_view_mirrors_the_state_it_was_given(self):
        view = board_view(populated())
        self.assertEqual(view["locations"][0]["label"], "Helsinki")
        self.assertEqual(view["network_nodes"][0]["id"], "f1")
        self.assertEqual(view["network_edges"][0]["source"], "f1")

    def test_view_does_not_mutate_the_state(self):
        state = populated()
        before = state.to_dict()
        board_view(state)
        self.assertEqual(state.to_dict(), before)


class PortsTests(unittest.TestCase):
    def test_each_reserved_adapter_is_a_protocol(self):
        for name in ("LeaderRPG", "PoliticalSimulation", "FactionStrategy", "AgentProvider"):
            self.assertTrue(issubclass(getattr(ports, name), Protocol), name)

    def test_each_port_declares_a_describe_hook(self):
        for name in ("LeaderRPG", "PoliticalSimulation", "FactionStrategy", "AgentProvider"):
            port = getattr(ports, name)
            self.assertTrue(callable(getattr(port, "describe", None)), name)

    def test_a_conforming_object_satisfies_a_port_structurally(self):
        class Demo:
            def describe(self, state):
                return {"state": state.schema_version}

        self.assertEqual(Demo().describe(WorldState()), {"state": "scaffold-1"})


class StandaloneEntrypointTests(unittest.TestCase):
    def test_module_entrypoint_prints_the_empty_view_as_json(self):
        result = subprocess.run(
            [sys.executable, "-m", "strategy_game"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], "scaffold-1")
        self.assertEqual(payload["locations"], [])


if __name__ == "__main__":
    unittest.main()
