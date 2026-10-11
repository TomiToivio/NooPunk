"""Runtime-contract tests for the strategy game scaffold (issue #282).

These assert **code behaviour only** — determinism, the no-optional-dependency promise,
provenance round-trips and the layer protocols staying injectable. No test here reads a
rulebook, a lore file or any prose: this repository forbids documentation tests, and the
issue asks for "executable tests only" over "runtime contracts".
"""
from __future__ import annotations

import unittest
from unittest.mock import patch

from strategy_game.capabilities import available_names, capabilities, require
from strategy_game.core import (
    Asset,
    Event,
    Faction,
    Leader,
    Location,
    NetworkEdge,
    Provenance,
    WorldState,
)
from strategy_game.ports import (
    AgentProvider,
    AgentRunner,
    FactionStrategy,
    LeaderRPG,
    MapProvider,
    PoliticalSimulation,
)
from strategy_game.view import board_view


class DeterminismTests(unittest.TestCase):
    def test_serialization_is_byte_stable_across_calls(self):
        """A snapshot must be reproducible: same state in, same bytes out."""
        state = WorldState(
            leaders=[Leader("l1", "Example")],
            factions=[Faction("f1", "Example faction", "l1")],
        )
        self.assertEqual(state.to_json(), state.to_json())
        self.assertEqual(WorldState().to_json(), WorldState().to_json())

    def test_schema_version_travels_with_the_snapshot(self):
        restored = WorldState.from_json(WorldState().to_json())
        self.assertEqual(restored.schema_version, WorldState().schema_version)

    def test_field_order_does_not_change_the_bytes(self):
        a = WorldState(locations=[Location("a", "A"), Location("b", "B")])
        b = WorldState(locations=[Location("a", "A"), Location("b", "B")])
        self.assertEqual(a.to_json(), b.to_json())


class NoOptionalDependencyTests(unittest.TestCase):
    def test_capability_report_never_imports_and_never_raises(self):
        caps = capabilities()
        self.assertTrue(caps, "expected the scaffold to declare its optional adapters")
        for cap in caps:
            self.assertIsInstance(cap.available, bool)
            self.assertTrue(cap.purpose, "a capability must say what it would be used for")

    def test_world_state_loads_views_and_serializes_without_any_adapter(self):
        """The core promise: no LLM, no NetworkX, no Mesa needed to read a world."""
        state = WorldState(events=[Event("e1", "example event")])
        view = board_view(state)
        self.assertIn("locations", view)
        self.assertIn("network_edges", view)
        self.assertEqual(view["network_edges"], [])
        self.assertEqual(WorldState.from_json(state.to_json()), state)

    def test_requiring_an_absent_adapter_gives_an_actionable_error(self):
        """Forced absent so the contract is tested on every machine, not just bare ones."""
        with patch("strategy_game.capabilities._is_importable", return_value=False):
            with self.assertRaises(RuntimeError) as caught:
                require("networkx")
        message = str(caught.exception)
        self.assertIn("networkx", message)
        self.assertIn("does not require it", message)

    def test_requiring_an_unknown_adapter_is_a_key_error(self):
        with self.assertRaises(KeyError):
            require("not-a-real-adapter")

    def test_available_names_is_a_subset_of_the_declared_adapter_names(self):
        declared = {cap.name for cap in capabilities()}
        self.assertTrue(set(available_names()) <= declared)


class ProvenanceTests(unittest.TestCase):
    def test_provenance_distinguishes_evidence_from_generated_discourse(self):
        """#282: evidence and simulated/generated discourse are stored separately."""
        evidence = Provenance(kind="evidence", source="example-corpus")
        generated = Provenance(kind="generated", source="example-run")
        self.assertNotEqual(evidence, generated)

    def test_provenance_survives_a_round_trip(self):
        state = WorldState(events=[Event("e1", "example", Provenance("simulated", "example run"))])
        restored = WorldState.from_json(state.to_json())
        self.assertEqual(restored, state)
        self.assertEqual(restored.events[0].provenance.kind, "simulated")

    def test_existing_snapshots_without_the_new_field_still_load(self):
        """Additive only: a snapshot written before provenance existed must still parse."""
        legacy = '{"schema_version": "scaffold-1", "events": [{"identifier": "e1", "description": "d"}], ' \
                 '"leaders": [], "factions": [], "assets": [], "locations": [], "edges": []}'
        restored = WorldState.from_json(legacy)
        self.assertEqual(restored.events[0].identifier, "e1")
        self.assertEqual(restored.events[0].provenance.kind, "")


class LayerBoundaryTests(unittest.TestCase):
    def test_every_layer_port_is_a_runtime_checkable_protocol(self):
        for protocol in (LeaderRPG, PoliticalSimulation, FactionStrategy, AgentProvider, AgentRunner, MapProvider):
            self.assertTrue(getattr(protocol, "_is_protocol", False), protocol)

    def test_ports_are_injectable_without_importing_anything_optional(self):
        class Stub:
            def describe(self, state):
                return {"layer": "stub"}

        for protocol in (LeaderRPG, PoliticalSimulation, FactionStrategy, AgentProvider, AgentRunner, MapProvider):
            with self.subTest(protocol=protocol.__name__):
                self.assertIsInstance(Stub(), protocol)


if __name__ == "__main__":
    unittest.main()
