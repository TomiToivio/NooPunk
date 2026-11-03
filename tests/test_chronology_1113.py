"""Integrity tests for the #1113 chronology data.

The chronology is data (`data/world/chronology_1113.json`), and the canon document renders a table from it. These
tests check the data itself — ordering, stable ids, vocabulary, and the one rule that protects the setting's
deliberate mysteries: **an OPEN event may not carry a precise date.**

Deliberately not tested: whether the markdown table in the canon document matches the JSON.
`AGENTS.md` forbids documentation gates and text-matching assertions over prose, and `tools/chronology_1113_render.py`
regenerates the table rather than policing it.
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "world" / "chronology_1113.json"

sys.path.insert(0, str(ROOT / "tools"))

import chronology_1113_render

REQUIRED = ("order", "id", "when", "title", "summary", "status", "regions", "source")


class ChronologyIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.events = cls.data["events"]

    def test_the_file_declares_its_vocabulary_and_its_source_issue(self):
        self.assertEqual(self.data["format"], "noopunk.world.chronology")
        self.assertIn("/1113", self.data["issue"])
        self.assertEqual(set(self.data["statuses"]), {"canon", "in_world_claim", "open"})

    def test_every_event_has_the_required_fields(self):
        for event in self.events:
            with self.subTest(event=event.get("id", "?")):
                for field in REQUIRED:
                    self.assertIn(field, event, f"{event.get('id')} is missing {field}")

    def test_ids_are_unique_and_orders_are_contiguous(self):
        ids = [event["id"] for event in self.events]
        self.assertEqual(len(ids), len(set(ids)), "duplicate event ids make canon references ambiguous")
        orders = [event["order"] for event in self.events]
        self.assertEqual(orders, list(range(1, len(self.events) + 1)),
                         "order must run 1..N with no gaps; the order is the authoritative field")

    def test_every_event_uses_the_declared_status_vocabulary(self):
        for event in self.events:
            with self.subTest(event=event["id"]):
                self.assertIn(event["status"], self.data["statuses"])

    def test_every_canon_event_cites_a_source(self):
        # Canon without a citation is someone's memory of a decision.
        for event in self.events:
            if event["status"] == "canon":
                with self.subTest(event=event["id"]):
                    self.assertTrue(event["source"].strip(), "a canon event must cite where it came from")

    def test_open_events_do_not_invent_a_date(self):
        # rulebook/7_TIMELINE.md leaves the ordering and dating of the paradigm shifts open. An undecided
        # question must not acquire a year by being written down.
        year = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
        for event in self.events:
            if event["status"] == "open":
                with self.subTest(event=event["id"]):
                    self.assertIsNone(year.search(event["when"]),
                                      f"OPEN event {event['id']} carries a date: {event['when']!r}")

    def test_no_event_is_dated_after_the_setting_year(self):
        # 2045 is the setting present (rulebook/7_TIMELINE.md). Nothing may be dated past it.
        year = re.compile(r"\b(2\d{3})\b")
        for event in self.events:
            for found in year.findall(event["when"]):
                with self.subTest(event=event["id"]):
                    self.assertLessEqual(int(found), self.data["setting_year"])

    def test_the_nuclear_and_disinformation_sequence_keeps_its_order(self):
        # These four are the chain the scenario's tension depends on; reordering them changes the story.
        by_id = {event["id"]: event["order"] for event in self.events}
        self.assertLess(by_id["us_emp_strikes"], by_id["birdsong_whalesong"])
        self.assertLess(by_id["jerusalem_manifestation"], by_id["transmission_failure"])
        self.assertLess(by_id["soviet_of_saturn_1952"], by_id["soviet_of_saturn_identity"],
                        "the contact is canon; its meaning is open")

    def test_the_table_renders_deterministically(self):
        first = chronology_1113_render.render_table()
        self.assertEqual(chronology_1113_render.render_table(), first)
        self.assertIn("| 27 |", first)
        self.assertIn("OPEN", first)


if __name__ == "__main__":
    unittest.main()
