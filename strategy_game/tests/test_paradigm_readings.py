"""Behaviour tests for the paradigm reading reader (issues #469, #470).

Code-only, per `AGENTS.md` and issue #271. These tests exercise the **reader**: what it returns,
what it refuses, and what it reports instead of inventing. They deliberately do **not** assert how
many seed cards exist, which factions are in the roster, or what any reading says — that is
authored material, reviewed editorially and by playtesting, not frozen in CI.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game import paradigm_readings as pr  # noqa: E402
from strategy_game.quantities import QUANTITY_IDS  # noqa: E402

FORMAT = "noopunk.strategy_game.paradigm_event_seeds"
FACTIONS = ("alpha", "beta")


def scratch(name: str, payload: dict) -> Path:
    """A document written where this process may read it."""
    path = Path(tempfile.mkdtemp()) / name
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def synthetic_seed(factions=FACTIONS, **overrides) -> dict:
    payload = {
        "format": FORMAT,
        "version": 1,
        "reading_vocabulary": {"reading_statuses": [{"id": status} for status in pr.READING_STATUSES]},
        "cards": [
            {
                "id": "event-one",
                "faction_readings": {
                    "readings": [
                        {
                            "faction": faction,
                            "reads": f"{faction} believes something specific",
                            "counts_as_evidence": "a document",
                            "trusts": "its own people",
                            "does": "acts on it",
                            "justifies_with": "a signifier",
                            "epistemic_status": "credible_incomplete_evidence",
                            "basis": "a record",
                        }
                        for faction in factions
                    ]
                },
            }
        ],
    }
    payload.update(overrides)
    return payload


class ReadingLookupTests(unittest.TestCase):
    def test_a_seed_yields_one_reading_per_named_faction_in_document_order(self):
        path = scratch("s.json", synthetic_seed())
        readings = pr.readings_for("event-one", path=path)
        self.assertEqual([reading.faction for reading in readings], list(FACTIONS))

    def test_a_reading_exposes_what_the_faction_believes_evidence_trust_and_does(self):
        path = scratch("s.json", synthetic_seed())
        reading = pr.reading_for("event-one", "beta", path=path)
        self.assertEqual(reading.faction, "beta")
        self.assertTrue(reading.reads)
        self.assertTrue(reading.counts_as_evidence)
        self.assertTrue(reading.trusts)
        self.assertTrue(reading.does)
        self.assertTrue(reading.justifies_with)
        self.assertIn(reading.epistemic_status, pr.READING_STATUSES)

    def test_an_unknown_event_is_never_synthesised(self):
        path = scratch("s.json", synthetic_seed())
        with self.assertRaises(KeyError):
            pr.readings_for("an-event-nobody-authored", path=path)

    def test_a_faction_that_does_not_read_an_event_is_absent_not_invented(self):
        path = scratch("s.json", synthetic_seed(factions=("alpha",)))
        with self.assertRaises(KeyError):
            pr.reading_for("event-one", "beta", path=path)
        self.assertEqual(pr.readings_for("event-one", path=path)[0].faction, "alpha")

    def test_a_reading_keeps_the_author_fields_the_reader_does_not_know(self):
        path = scratch("s.json", synthetic_seed())
        reading = pr.reading_for("event-one", "alpha", path=path)
        self.assertEqual(reading.detail["basis"], "a record")
        self.assertEqual(reading.to_dict()["basis"], "a record")

    def test_a_reading_declares_no_numeric_quantity(self):
        path = scratch("s.json", synthetic_seed())
        reading = pr.reading_for("event-one", "alpha", path=path)

        def walk(node):
            if isinstance(node, dict):
                for value in node.values():
                    yield from walk(value)
            elif isinstance(node, (list, tuple)):
                for item in node:
                    yield from walk(item)
            else:
                yield node

        for value in walk(reading.to_dict()):
            self.assertNotIsInstance(value, (int, float),
                                     f"a numeric quantity entered a reading: {value!r}")


class SeedDocumentTests(unittest.TestCase):
    def test_a_wrong_format_is_rejected_with_a_clear_error(self):
        path = scratch("s.json", synthetic_seed(format="something.else"))
        with self.assertRaises(ValueError) as caught:
            pr.load_event_seeds(path)
        self.assertIn(FORMAT, str(caught.exception))

    def test_a_card_without_faction_readings_is_rejected_and_named(self):
        payload = synthetic_seed()
        payload["cards"][0].pop("faction_readings")
        with self.assertRaises(ValueError) as caught:
            pr.load_event_seeds(scratch("s.json", payload))
        self.assertIn("event-one", str(caught.exception))

    def test_a_card_that_reads_one_faction_twice_is_rejected(self):
        payload = synthetic_seed(factions=("alpha", "alpha"))
        with self.assertRaises(ValueError) as caught:
            pr.load_event_seeds(scratch("s.json", payload))
        self.assertIn("twice", str(caught.exception))

    def test_a_duplicate_card_id_is_rejected(self):
        payload = synthetic_seed()
        payload["cards"].append(copy.deepcopy(payload["cards"][0]))
        with self.assertRaises(ValueError):
            pr.load_event_seeds(scratch("s.json", payload))

    def test_missing_readings_are_listed_for_the_pairs_that_are_absent(self):
        payload = synthetic_seed(factions=("alpha",))
        self.assertEqual(pr.missing_readings(("alpha", "beta"), payload=payload), ("event-one/beta",))
        self.assertEqual(pr.missing_readings(("alpha",), payload=payload), ())

    def test_an_unknown_reading_status_is_reported_not_accepted(self):
        payload = synthetic_seed()
        payload["cards"][0]["faction_readings"]["readings"][0]["epistemic_status"] = "vibes"
        self.assertEqual(pr.unknown_reading_statuses(payload), ("vibes",))


class QuantityProfileTests(unittest.TestCase):
    @staticmethod
    def _roster() -> dict:
        profile = {name: {"note": f"{name} note"} for name in QUANTITY_IDS}
        profile["influence"] = {"note": "not one of the six"}
        return {"un_parliamentary_parties": {"parties": [{"id": "alpha", "six_quantities": profile}]}}

    def test_a_profile_covers_only_the_six_quantities(self):
        profile = pr.quantity_profile("alpha", path=scratch("roster.json", self._roster()))
        self.assertEqual(list(profile), list(QUANTITY_IDS))

    def test_a_quantity_name_outside_the_six_is_reported_not_returned(self):
        path = scratch("roster.json", self._roster())
        self.assertNotIn("influence", pr.quantity_profile("alpha", path=path))
        self.assertEqual(pr.unknown_quantity_names("alpha", path=path), ("influence",))

    def test_an_unknown_party_is_reported_not_invented(self):
        path = scratch("roster.json", self._roster())
        with self.assertRaises(KeyError):
            pr.quantity_profile("gamma", path=path)

    def test_a_register_without_the_parties_block_reads_as_empty(self):
        path = scratch("roster.json", {"format": "noopunk.strategy_game.global_factions"})
        self.assertEqual(pr.load_un_parliamentary_parties(path), ())


class ShippedDocumentTests(unittest.TestCase):
    """The shipped seed file loads and reads through the mechanism; its content is not asserted."""

    def test_the_shipped_seed_document_loads(self):
        self.assertEqual(pr.load_event_seeds()["format"], pr.SEEDS_FORMAT)
        self.assertTrue(pr.event_ids(), "the packaged seed document carries no cards at all")

    def test_the_shipped_document_reads_its_own_first_event(self):
        first = pr.event_ids()[0]
        readings = pr.readings_for(first)
        self.assertTrue(readings, f"the seed {first!r} reads no faction at all")
        self.assertEqual(len({reading.faction for reading in readings}), len(readings))

    def test_the_shipped_document_uses_only_the_statuses_it_declares(self):
        self.assertEqual(pr.unknown_reading_statuses(), ())

    def test_the_statuses_are_declared_once_in_one_vocabulary(self):
        declared = pr.reading_statuses()
        self.assertEqual(len(declared), len(set(declared)))
        for status in pr.READING_STATUSES:
            self.assertIn(status, declared)

    def test_reading_the_seeds_pulls_in_no_adapter_or_laclaugpt(self):
        code = (
            "import sys, strategy_game.paradigm_readings as pr;"
            "pr.readings_for(pr.event_ids()[0]);"
            "parties = pr.load_un_parliamentary_parties();"
            "parties and pr.quantity_profile(parties[0]['id']);"
            "print([m for m in ('mesa', 'networkx', 'ollama', 'concordia', 'laclaugpt')"
            " if m in sys.modules])"
        )
        result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]",
                         f"reading the seeds pulled in a dependency: {result.stdout}")


if __name__ == "__main__":
    unittest.main()
