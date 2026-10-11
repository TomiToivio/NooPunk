"""Runtime contracts for the rule-free strategy-game scaffold (issue #282).

These tests assert **executable behaviour only** — container defaults, serialization, determinism,
the view model, the provenance separation, the optional-dependency seam and the adapter protocols.
Per `AGENTS.md` they contain **no** assertion about rules, statistics, canon, lore or wording: the
scaffold has no mechanics to test, only contracts.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game import Provenance, ProvenanceKind, WorldState  # noqa: E402
from strategy_game import capabilities, ports  # noqa: E402
from strategy_game.core import (  # noqa: E402
    Asset,
    Event,
    Faction,
    Leader,
    Location,
    NetworkEdge,
)
from strategy_game.provenance import NON_EVIDENCE_KINDS, PROVENANCE_KINDS  # noqa: E402
from strategy_game.view import board_view  # noqa: E402

OPTIONAL = ("mesa", "networkx", "ollama", "concordia")


def populated() -> WorldState:
    return WorldState(
        leaders=[Leader("l1", "Helsinki lead", {"author_defined": "TBD"}, ["example"])],
        factions=[Faction("f1", "Example faction", "l1", ["a1"])],
        assets=[Asset("a1", "Example asset", "loc1", "f1")],
        locations=[Location("loc1", "Noösphere station", 60.17, 24.94)],
        edges=[NetworkEdge("f1", "l1", "communication")],
        events=[
            Event("e1", "recorded observation", Provenance(ProvenanceKind.EVIDENCE, "case-file")),
            Event("e2", "modelled outcome", Provenance(ProvenanceKind.SIMULATED, "run-1")),
        ],
    )


class SerializationContractTests(unittest.TestCase):
    def test_empty_state_round_trips(self):
        original = WorldState()
        self.assertEqual(WorldState.from_json(original.to_json()), original)

    def test_populated_state_round_trips(self):
        original = populated()
        self.assertEqual(WorldState.from_json(original.to_json()), original)

    def test_output_is_deterministic_and_key_sorted(self):
        state = populated()
        self.assertEqual(state.to_json(), state.to_json())
        parsed = json.loads(state.to_json())
        self.assertEqual(list(parsed), sorted(parsed))

    def test_json_round_trip_is_stable_across_a_second_pass(self):
        once = populated().to_json()
        twice = WorldState.from_json(once).to_json()
        self.assertEqual(once, twice)

    def test_non_ascii_is_preserved_not_escaped(self):
        text = populated().to_json()
        self.assertIn("Noösphere", text)
        self.assertNotIn("\\u00f6", text)

    def test_a_snapshot_missing_a_section_still_loads(self):
        """Forward/backward tolerance: an older snapshot without `events` must not raise."""
        minimal = json.dumps({"schema_version": "scaffold-1"})
        self.assertEqual(WorldState.from_json(minimal), WorldState())

    def test_collections_are_not_shared_between_instances(self):
        first, second = WorldState(), WorldState()
        first.locations.append(Location("x", "y"))
        self.assertEqual(second.locations, [])


class ProvenanceContractTests(unittest.TestCase):
    """`docs/INTEGRATION_BOUNDARIES.md`: unknown provenance must stay unknown, never evidence."""

    def test_declared_kinds_match_the_enum(self):
        self.assertEqual(set(PROVENANCE_KINDS), {kind.value for kind in ProvenanceKind})
        self.assertEqual(
            set(ProvenanceKind),
            {ProvenanceKind.UNKNOWN, ProvenanceKind.EVIDENCE, ProvenanceKind.AUTHORED,
             ProvenanceKind.GENERATED, ProvenanceKind.SIMULATED},
        )

    def test_the_default_kind_is_unknown_not_evidence(self):
        self.assertIs(Provenance().kind, ProvenanceKind.UNKNOWN)
        self.assertTrue(Provenance().is_unknown)
        self.assertFalse(Provenance().is_evidence)

    def test_an_event_without_provenance_is_unknown_not_evidence(self):
        self.assertIs(Event("e", "d").provenance.kind, ProvenanceKind.UNKNOWN)

    def test_every_kind_round_trips(self):
        for kind in ProvenanceKind:
            with self.subTest(kind=kind):
                state = WorldState(events=[Event("e", "d", Provenance(kind, "src", "note"))])
                restored = WorldState.from_json(state.to_json())
                self.assertIs(restored.events[0].provenance.kind, kind)
                self.assertEqual(restored.events[0].provenance.source, "src")

    def test_only_evidence_reports_as_evidence(self):
        for kind in NON_EVIDENCE_KINDS:
            with self.subTest(kind=kind):
                self.assertFalse(Provenance(kind).is_evidence)
        self.assertTrue(Provenance(ProvenanceKind.EVIDENCE).is_evidence)

    def test_evidence_and_simulated_stay_distinct_after_a_snapshot(self):
        restored = WorldState.from_json(populated().to_json())
        kinds = [event.provenance.kind for event in restored.events]
        self.assertEqual(kinds, [ProvenanceKind.EVIDENCE, ProvenanceKind.SIMULATED])

    def test_a_legacy_bare_string_is_read_as_an_unknown_source(self):
        legacy = json.dumps({
            "schema_version": "scaffold-1",
            "events": [{"identifier": "e", "description": "d", "provenance": "old-note"}],
        })
        provenance = WorldState.from_json(legacy).events[0].provenance
        self.assertIs(provenance.kind, ProvenanceKind.UNKNOWN,
                      "a legacy string must not be silently upgraded into evidence")
        self.assertEqual(provenance.source, "old-note")

    def test_an_unrecognised_kind_falls_back_to_unknown(self):
        payload = json.dumps({
            "schema_version": "scaffold-1",
            "events": [{"identifier": "e", "description": "d",
                        "provenance": {"kind": "not-a-kind"}}],
        })
        self.assertIs(WorldState.from_json(payload).events[0].provenance.kind,
                      ProvenanceKind.UNKNOWN)

    def test_serialized_provenance_is_plain_scalars(self):
        payload = populated().to_dict()["events"][0]["provenance"]
        self.assertEqual(payload, {"kind": "evidence", "source": "case-file", "note": ""})
        self.assertIsInstance(payload["kind"], str)


class ViewContractTests(unittest.TestCase):
    def test_view_exposes_the_documented_fields_only(self):
        self.assertEqual(
            set(board_view(populated())),
            {"schema_version", "locations", "network_nodes", "network_edges", "assets"},
        )

    def test_view_is_network_and_map_neutral_for_an_empty_world(self):
        view = board_view(WorldState())
        self.assertEqual(view["locations"], [])
        self.assertEqual(view["network_nodes"], [])
        self.assertEqual(view["network_edges"], [])
        self.assertEqual(view["assets"], [])

    def test_view_renders_locations_nodes_and_edges(self):
        view = board_view(populated())
        self.assertEqual(view["locations"][0]["id"], "loc1")
        self.assertEqual(view["network_nodes"][0], {"id": "f1", "label": "Example faction",
                                                    "type": "faction"})
        self.assertEqual(view["network_edges"][0]["layer"], "communication")

    def test_view_does_not_mutate_its_state(self):
        state = populated()
        before = state.to_json()
        board_view(state)
        self.assertEqual(state.to_json(), before)


class OptionalDependencyContractTests(unittest.TestCase):
    """No optional adapter may be required to load or view world state."""

    def test_declared_adapters_are_exactly_the_expected_seam(self):
        self.assertEqual(capabilities.OPTIONAL_ADAPTERS, OPTIONAL)
        self.assertEqual(set(capabilities.ADAPTER_PURPOSE), set(OPTIONAL))

    def test_availability_reports_booleans_without_importing(self):
        report = capabilities.available_adapters()
        self.assertEqual(set(report), set(OPTIONAL))
        for name, value in report.items():
            with self.subTest(adapter=name):
                self.assertIsInstance(value, bool)

    def test_missing_adapters_are_a_subset_of_the_declared_seam(self):
        self.assertTrue(set(capabilities.missing_adapters()) <= set(OPTIONAL))

    def test_is_available_never_raises_for_a_nonsense_name(self):
        self.assertIs(capabilities.is_available("strategy_game_definitely_not_a_module"), False)

    def test_require_refuses_an_undeclared_adapter(self):
        with self.assertRaises(ValueError):
            capabilities.require("os")

    def test_importing_the_package_pulls_in_no_optional_adapter(self):
        """Asserted in a subprocess so the parent's own imports cannot mask the answer."""
        code = (
            "import sys, strategy_game, strategy_game.capabilities, strategy_game.view;"
            f"print([m for m in {list(OPTIONAL)!r} if m in sys.modules])"
        )
        result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]",
                         f"loading the package imported an optional adapter: {result.stdout}")

    def test_viewing_state_pulls_in_no_optional_adapter(self):
        code = (
            "import json, sys, strategy_game;"
            "from strategy_game.view import board_view;"
            "json.dumps(board_view(strategy_game.WorldState()));"
            f"print([m for m in {list(OPTIONAL)!r} if m in sys.modules])"
        )
        result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]", result.stdout)


class PortAndEntrypointTests(unittest.TestCase):
    def test_all_five_reserved_ports_exist(self):
        for name in ("LeaderRPG", "PoliticalSimulation", "FactionStrategy", "AgentProvider",
                     "MapProvider"):
            with self.subTest(port=name):
                proto = getattr(ports, name)
                self.assertTrue(getattr(proto, "_is_protocol", False), f"{name} is not a Protocol")

    def test_a_concrete_adapter_satisfies_a_port_structurally(self):
        class Stub:
            def describe(self, state):
                return {"ok": True}

        stub: ports.MapProvider = Stub()
        self.assertEqual(stub.describe(WorldState()), {"ok": True})

    def test_package_exports_are_declared(self):
        import strategy_game

        self.assertEqual(set(strategy_game.__all__),
                         {"WorldState", "Provenance", "ProvenanceKind"})

    def test_module_entrypoint_emits_the_view_model(self):
        result = subprocess.run([sys.executable, "-m", "strategy_game"], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], "scaffold-1")
        self.assertEqual(payload["network_edges"], [])


if __name__ == "__main__":
    unittest.main()
