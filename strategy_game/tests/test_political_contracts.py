"""Executable contracts for the Layer II political-field containers (issue #282).

These tests assert **executable behaviour only** — container defaults, serialization, determinism,
the read-only structural queries, the provenance separation, and the two boundaries this layer
promises: it never imports LaclauGPT or an optional adapter, and it stores no numeric quantity.
Per `AGENTS.md` there is no assertion about rules, canon, lore or wording: Layer II has no mechanics
yet, only contracts.

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

from strategy_game import Provenance, ProvenanceKind  # noqa: E402
from strategy_game.political import (  # noqa: E402
    POWER_MODES,
    SIGNIFIER_ROLES,
    Articulation,
    CommunicativeTie,
    Demand,
    Frontier,
    PoliticalField,
    PoliticalFormation,
    PowerMode,
    Signifier,
    SignifierRole,
)

OPTIONAL = ("mesa", "networkx", "ollama", "concordia")

#: Keys that would mean Layer II had drifted into storing a metric or a score.
METRIC_TOKENS = ("score", "power", "strength", "influence", "support", "threshold", "weight",
                 "level", "rating", "meter")


def populated_field() -> PoliticalField:
    """A small abstract field: two competing readings of one nodal signifier."""
    return PoliticalField(
        demands=[
            Demand("d1", "affordable housing", Provenance(ProvenanceKind.EVIDENCE, "case-file")),
            Demand("d2", "public transport", Provenance(ProvenanceKind.EVIDENCE, "case-file")),
            Demand("d3", "law and order", Provenance(ProvenanceKind.AUTHORED, "scenario-1")),
        ],
        signifiers=[
            Signifier("s1", "the Noösphere commons", SignifierRole.EMPTY,
                      Provenance(ProvenanceKind.AUTHORED, "scenario-1")),
            Signifier("s2", "the nation", SignifierRole.NODAL,
                      Provenance(ProvenanceKind.SIMULATED, "run-1")),
        ],
        articulations=[
            Articulation("s1", "d1", Provenance(ProvenanceKind.EVIDENCE, "case-file")),
            Articulation("s1", "d2", Provenance(ProvenanceKind.EVIDENCE, "case-file")),
            Articulation("s2", "d3", Provenance(ProvenanceKind.SIMULATED, "run-1")),
        ],
        frontiers=[
            Frontier("fr1", "s1", ["d1", "d2"], ["d3"],
                     Provenance(ProvenanceKind.AUTHORED, "scenario-1")),
        ],
        ties=[
            CommunicativeTie("f1", "s1", PowerMode.PROGRAMMING,
                             Provenance(ProvenanceKind.AUTHORED, "scenario-1")),
        ],
        formations=[
            PoliticalFormation("fm1", "commons bloc", ["s1"],
                               Provenance(ProvenanceKind.SIMULATED, "run-1")),
        ],
    )


def _scalars(node: object):
    """Every leaf value in a nested JSON structure."""
    if isinstance(node, dict):
        for value in node.values():
            yield from _scalars(value)
    elif isinstance(node, list):
        for item in node:
            yield from _scalars(item)
    else:
        yield node


def _keys(node: object):
    """Every dict key in a nested JSON structure."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield key
            yield from _keys(value)
    elif isinstance(node, list):
        for item in node:
            yield from _keys(item)


class SerializationContractTests(unittest.TestCase):
    def test_empty_field_round_trips(self):
        original = PoliticalField()
        self.assertEqual(PoliticalField.from_json(original.to_json()), original)

    def test_populated_field_round_trips(self):
        original = populated_field()
        self.assertEqual(PoliticalField.from_json(original.to_json()), original)

    def test_every_collection_is_serialized(self):
        payload = populated_field().to_dict()
        self.assertEqual(
            set(payload),
            {"schema_version", "demands", "signifiers", "articulations", "frontiers", "ties",
             "formations"},
        )
        for name in ("demands", "signifiers", "articulations", "frontiers", "ties", "formations"):
            with self.subTest(collection=name):
                self.assertTrue(payload[name], f"{name} was dropped from the payload")

    def test_output_is_deterministic_and_key_sorted(self):
        field = populated_field()
        self.assertEqual(field.to_json(), field.to_json())
        parsed = json.loads(field.to_json())
        self.assertEqual(list(parsed), sorted(parsed))

    def test_json_round_trip_is_stable_across_a_second_pass(self):
        once = populated_field().to_json()
        self.assertEqual(once, PoliticalField.from_json(once).to_json())

    def test_non_ascii_is_preserved_not_escaped(self):
        text = populated_field().to_json()
        self.assertIn("Noösphere", text)
        self.assertNotIn("\\u00f6", text)

    def test_a_snapshot_missing_a_collection_still_loads(self):
        self.assertEqual(PoliticalField.from_json(json.dumps({"schema_version": "political-1"})),
                         PoliticalField())

    def test_collections_are_not_shared_between_instances(self):
        first, second = PoliticalField(), PoliticalField()
        first.demands.append(Demand("d1", "example"))
        self.assertEqual(second.demands, [])


class VocabularyContractTests(unittest.TestCase):
    def test_signifier_roles_are_laclau_roles_only(self):
        self.assertEqual({role.value for role in SignifierRole},
                         {"nodal", "floating", "empty"})
        self.assertEqual(set(SIGNIFIER_ROLES), {role.value for role in SignifierRole})

    def test_power_modes_are_castells_modes_only(self):
        self.assertEqual({mode.value for mode in PowerMode}, {"programming", "switching"})
        self.assertEqual(set(POWER_MODES), {mode.value for mode in PowerMode})

    def test_an_unrecorded_role_stays_visible_as_none(self):
        """A signifier with no recorded role must not be silently read as nodal."""
        self.assertIsNone(Signifier("s1", "unclassified").role)
        restored = PoliticalField.from_json(
            PoliticalField(signifiers=[Signifier("s1", "unclassified")]).to_json()
        )
        self.assertIsNone(restored.signifiers[0].role)

    def test_an_unrecognised_role_reads_as_none(self):
        payload = json.dumps({"schema_version": "political-1",
                              "signifiers": [{"identifier": "s1", "role": "charismatic"}]})
        self.assertIsNone(PoliticalField.from_json(payload).signifiers[0].role)

    def test_an_unrecognised_power_mode_reads_as_none(self):
        payload = json.dumps({"schema_version": "political-1",
                              "ties": [{"source_id": "a", "target_id": "b", "mode": "coercion"}]})
        self.assertIsNone(PoliticalField.from_json(payload).ties[0].mode)

    def test_every_role_and_mode_round_trips(self):
        for role in SignifierRole:
            with self.subTest(role=role):
                field = PoliticalField(signifiers=[Signifier("s", "x", role)])
                self.assertIs(PoliticalField.from_json(field.to_json()).signifiers[0].role, role)
        for mode in PowerMode:
            with self.subTest(mode=mode):
                field = PoliticalField(ties=[CommunicativeTie("a", "b", mode)])
                self.assertIs(PoliticalField.from_json(field.to_json()).ties[0].mode, mode)


class ProvenanceSeparationContractTests(unittest.TestCase):
    """The issue asks that evidence stay distinct from simulated or generated discourse."""

    def test_evidence_and_simulated_stay_distinct_after_a_snapshot(self):
        restored = PoliticalField.from_json(populated_field().to_json())
        self.assertIs(restored.demands[0].provenance.kind, ProvenanceKind.EVIDENCE)
        self.assertIs(restored.signifiers[1].provenance.kind, ProvenanceKind.SIMULATED)
        self.assertIs(restored.articulations[2].provenance.kind, ProvenanceKind.SIMULATED)
        self.assertIs(restored.demands[2].provenance.kind, ProvenanceKind.AUTHORED)

    def test_a_container_without_provenance_reads_unknown_not_evidence(self):
        self.assertIs(Demand("d1", "x").provenance.kind, ProvenanceKind.UNKNOWN)
        self.assertIs(Signifier("s1", "x").provenance.kind, ProvenanceKind.UNKNOWN)
        self.assertIs(Articulation("s1", "d1").provenance.kind, ProvenanceKind.UNKNOWN)
        self.assertFalse(Demand("d1", "x").provenance.is_evidence)

    def test_a_record_omitting_provenance_reads_unknown_not_evidence(self):
        """A record with no provenance key at all must load as UNKNOWN, not as evidence."""
        payload = json.dumps({
            "schema_version": "political-1",
            "demands": [{"identifier": "d1", "text": "x"}],
            "signifiers": [{"identifier": "s1", "label": "y"}],
        })
        restored = PoliticalField.from_json(payload)
        self.assertIs(restored.demands[0].provenance.kind, ProvenanceKind.UNKNOWN)
        self.assertIs(restored.signifiers[0].provenance.kind, ProvenanceKind.UNKNOWN)

    def test_a_legacy_bare_string_is_read_as_an_unknown_source(self):
        payload = json.dumps({"schema_version": "political-1",
                              "demands": [{"identifier": "d1", "text": "x",
                                           "provenance": "old-note"}]})
        provenance = PoliticalField.from_json(payload).demands[0].provenance
        self.assertIs(provenance.kind, ProvenanceKind.UNKNOWN,
                      "a legacy string must not be silently upgraded into evidence")
        self.assertEqual(provenance.source, "old-note")

    def test_serialized_provenance_is_plain_scalars(self):
        payload = populated_field().to_dict()["demands"][0]["provenance"]
        self.assertEqual(payload, {"kind": "evidence", "source": "case-file", "note": ""})
        self.assertIsInstance(payload["kind"], str)


class StructuralQueryContractTests(unittest.TestCase):
    """A chain is read from the structure. Nothing here computes an outcome or a score."""

    def test_demands_of_returns_the_articulated_chain_in_order(self):
        self.assertEqual(populated_field().demands_of("s1"), ("d1", "d2"))
        self.assertEqual(populated_field().demands_of("s2"), ("d3",))

    def test_signifiers_of_is_the_reverse_lookup(self):
        self.assertEqual(populated_field().signifiers_of("d3"), ("s2",))

    def test_an_unarticulated_signifier_has_no_demands(self):
        self.assertEqual(populated_field().demands_of("not-a-signifier"), ())
        self.assertEqual(populated_field().signifiers_of("not-a-demand"), ())

    def test_queries_do_not_mutate_the_field(self):
        field = populated_field()
        before = field.to_json()
        field.demands_of("s1")
        field.signifiers_of("d1")
        self.assertEqual(field.to_json(), before)


class NoMetricContractTests(unittest.TestCase):
    """`docs/RULE_SYSTEM_RESEARCH.md`: political hegemony is not automatically a scalar score."""

    def test_the_layer_carries_no_numeric_quantity(self):
        for value in _scalars(populated_field().to_dict()):
            self.assertNotIsInstance(
                value, (int, float),
                f"a numeric quantity entered the political layer: {value!r}",
            )

    def test_no_metric_shaped_key_appears(self):
        keys = set(_keys(populated_field().to_dict()))
        for token in METRIC_TOKENS:
            with self.subTest(token=token):
                self.assertEqual([key for key in keys if token in key], [],
                                 f"a metric-shaped key entered the political layer: {token}")


class IsolationContractTests(unittest.TestCase):
    def test_importing_the_political_layer_pulls_in_no_adapter_or_laclaugpt(self):
        """LaclauGPT is a theory source here, never a dependency; asserted in a subprocess."""
        forbidden = list(OPTIONAL) + ["laclaugpt"]
        code = (
            "import sys, strategy_game.political;"
            "from strategy_game.political import PoliticalField;"
            "PoliticalField().to_json();"
            f"print([m for m in {forbidden!r} if m in sys.modules])"
        )
        result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]",
                         f"Layer II is meant to be dependency-free: {result.stdout}")

    def test_the_field_is_not_wired_into_world_state(self):
        """Integration is a Gate D decision: Layer II must stand alone for now."""
        from strategy_game.core import WorldState

        self.assertNotIn("political", {field for field in WorldState().__dict__})
        self.assertFalse(hasattr(WorldState(), "demands"))


if __name__ == "__main__":
    unittest.main()
