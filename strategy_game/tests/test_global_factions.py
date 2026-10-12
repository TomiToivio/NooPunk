"""Executable contracts for the authored global faction roster (issues #328 and #329).

Code-only, per `AGENTS.md` and issue #271. These tests exercise the **loader and the record types**.
They deliberately do **not** assert which factions exist, how many there are, or what any faction
says — that is authored canon, reviewed editorially and by playtesting, not frozen in CI. What is
asserted here is code behaviour: the shipped document parses, required structure is enforced with a
clear error, unknown author fields survive instead of being dropped, provenance follows the
repository's default rule, and the records introduce no numeric quantity (the no-mechanics
boundary).

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import copy
import dataclasses
import json
import subprocess
import sys
import typing
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game.factions import (  # noqa: E402
    DATA_PATH,
    ENTITY_KINDS,
    PARADIGM_STANCES,
    ROSTER_FORMAT,
    load_roster,
    roster_from_dict,
)
from strategy_game.provenance import ProvenanceKind  # noqa: E402

OPTIONAL = ("mesa", "networkx", "ollama", "concordia")


def shipped_payload() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def minimal_payload(**overrides) -> dict:
    payload = {
        "format": ROSTER_FORMAT,
        "version": 1,
        "status": "author_canon",
        "provenance": {"kind": "authored", "source": "test"},
        "factions": [{"id": "f1", "label": "Example", "kind": ENTITY_KINDS[0]}],
    }
    payload.update(overrides)
    return payload


class RosterLoadingTests(unittest.TestCase):
    def test_the_shipped_roster_loads(self):
        roster = load_roster()
        self.assertEqual(roster.format, ROSTER_FORMAT)
        self.assertTrue(roster.factions, "the packaged roster loaded no factions at all")

    def test_every_faction_exposes_the_required_structure(self):
        for faction in load_roster().factions:
            with self.subTest(faction=faction.identifier):
                for field_name in ("identifier", "label", "kind"):
                    self.assertTrue(getattr(faction, field_name),
                                    f"{field_name} is empty on {faction.identifier!r}")

    def test_identifiers_are_unique(self):
        identifiers = [faction.identifier for faction in load_roster().factions]
        self.assertEqual(len(identifiers), len(set(identifiers)), "duplicate faction identifiers")

    def test_each_faction_kind_is_declared_by_the_module(self):
        for faction in load_roster().factions:
            with self.subTest(faction=faction.identifier):
                self.assertIn(faction.kind, ENTITY_KINDS,
                              f"undeclared entity kind {faction.kind!r}")

    def test_the_paradigm_stances_are_declared_separately_from_the_axes(self):
        """#329 s4.1: paradigm positions are their own dimension, not derived from the compass."""
        self.assertIn("agi", PARADIGM_STANCES)
        self.assertIn("psi", PARADIGM_STANCES)
        self.assertIn("nhi", PARADIGM_STANCES)

    def test_lookups_are_read_only_and_tolerant(self):
        roster = load_roster()
        first = roster.factions[0]
        self.assertIs(roster.by_id(first.identifier), first)
        self.assertIsNone(roster.by_id("no-such-faction"))
        self.assertEqual(roster.of_kind("no-such-kind"), ())
        self.assertEqual(roster.by_id(first.identifier), first, "a lookup mutated the roster")

    def test_a_faction_round_trips_through_to_dict(self):
        for faction in load_roster().factions:
            with self.subTest(faction=faction.identifier):
                payload = faction.to_dict()
                self.assertEqual(payload["id"], faction.identifier)
                self.assertEqual(payload["kind"], faction.kind)

    def test_loading_the_same_document_twice_is_deterministic(self):
        self.assertEqual(load_roster().factions, load_roster().factions)


class ToleranceTests(unittest.TestCase):
    def test_an_unknown_author_field_is_retained_not_dropped(self):
        payload = minimal_payload()
        payload["factions"][0]["a_field_code_does_not_know_yet"] = {"later": "author material"}
        faction = roster_from_dict(payload).factions[0]
        self.assertEqual(faction.detail["a_field_code_does_not_know_yet"],
                         {"later": "author material"})

    def test_the_whole_document_is_retained(self):
        payload = minimal_payload()
        payload["cross_cutting_rules"] = [{"id": "x", "text": "kept"}]
        self.assertEqual(roster_from_dict(payload).detail["cross_cutting_rules"],
                         [{"id": "x", "text": "kept"}])

    def test_a_missing_required_field_is_rejected_with_a_clear_error(self):
        for missing in ("id", "label", "kind"):
            with self.subTest(missing=missing):
                payload = minimal_payload()
                del payload["factions"][0][missing]
                with self.assertRaises(ValueError) as caught:
                    roster_from_dict(payload)
                self.assertIn(missing, str(caught.exception))
                self.assertIn("factions[0]", str(caught.exception))

    def test_a_wrong_format_is_rejected(self):
        with self.assertRaises(ValueError) as caught:
            roster_from_dict(minimal_payload(format="something.else"))
        self.assertIn(ROSTER_FORMAT, str(caught.exception))

    def test_a_non_object_faction_is_rejected(self):
        with self.assertRaises(ValueError):
            roster_from_dict(minimal_payload(factions=["not-an-object"]))

    def test_absent_optional_collections_read_as_empty_not_as_failure(self):
        payload = minimal_payload()
        payload["factions"][0].pop("sources", None)
        roster = roster_from_dict(payload)
        self.assertEqual(roster.factions[0].sources, ())
        self.assertEqual(roster.factions[0].stances, {})


class ProvenanceContractTests(unittest.TestCase):
    """`docs/INTEGRATION_BOUNDARIES.md`: absence stays visibly unknown, never silently evidence."""

    def test_a_roster_without_provenance_reads_unknown_not_evidence(self):
        payload = minimal_payload()
        del payload["provenance"]
        provenance = roster_from_dict(payload).provenance
        self.assertIs(provenance.kind, ProvenanceKind.UNKNOWN)
        self.assertFalse(provenance.is_evidence)

    def test_an_unrecognised_provenance_kind_falls_back_to_unknown(self):
        payload = minimal_payload(provenance={"kind": "not-a-kind"})
        self.assertIs(roster_from_dict(payload).provenance.kind, ProvenanceKind.UNKNOWN)

    def test_a_faction_inherits_the_document_provenance(self):
        payload = minimal_payload()
        faction = roster_from_dict(payload).factions[0]
        self.assertIs(faction.provenance.kind, ProvenanceKind.AUTHORED)

    def test_the_shipped_roster_declares_its_origin(self):
        provenance = load_roster().provenance
        self.assertIsNot(provenance.kind, ProvenanceKind.UNKNOWN,
                         "the packaged roster must state where it came from")
        self.assertFalse(provenance.is_evidence,
                         "authored setting canon is not an observation")

    def test_an_evidence_kind_is_never_inferred(self):
        for kind in ProvenanceKind:
            if kind is ProvenanceKind.EVIDENCE:
                continue
            with self.subTest(kind=kind):
                payload = minimal_payload(provenance={"kind": kind.value})
                self.assertFalse(roster_from_dict(payload).provenance.is_evidence)


class NoMechanicsContractTests(unittest.TestCase):
    """The roster is setting data. #329 s5.7: no simulation rules before review."""

    def test_the_record_types_declare_no_numeric_field(self):
        for record in (type(load_roster()), type(load_roster().factions[0])):
            hints = typing.get_type_hints(record)
            for declared in dataclasses.fields(record):
                with self.subTest(record=record.__name__, field=declared.name):
                    self.assertNotIn(hints[declared.name], (int, float),
                                     f"{record.__name__}.{declared.name} is a numeric quantity")

    def test_a_faction_carries_no_numeric_quantity(self):
        """A faction is described, not scored: no strength, rating, alignment value or threshold."""
        factors = copy.deepcopy(shipped_payload()["factions"])

        def walk(node):
            if isinstance(node, dict):
                for value in node.values():
                    yield from walk(value)
            elif isinstance(node, list):
                for item in node:
                    yield from walk(item)
            else:
                yield node

        for value in walk(factors):
            self.assertNotIsInstance(value, (int, float),
                                     f"a numeric quantity entered a faction record: {value!r}")

    def test_the_open_questions_are_exposed_for_review(self):
        """The author's unresolved questions are carried, not silently answered by code."""
        self.assertTrue(load_roster().open_question_ids)


class IsolationContractTests(unittest.TestCase):
    def test_loading_the_roster_pulls_in_no_adapter_or_laclaugpt(self):
        forbidden = list(OPTIONAL) + ["laclaugpt"]
        code = (
            "import sys, strategy_game.factions as f;"
            "r = f.load_roster(); r.by_id(r.factions[0].identifier);"
            f"print([m for m in {forbidden!r} if m in sys.modules])"
        )
        result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]",
                         f"loading the roster pulled in a dependency: {result.stdout}")


if __name__ == "__main__":
    unittest.main()
