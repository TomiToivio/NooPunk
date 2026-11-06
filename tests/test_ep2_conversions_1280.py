"""The EP→CWN reference must stay a scene guide, not become a conversion engine (#1280).

Eclipse Phase is CC BY-NC-SA and not importable, and its percentile numbers have no CWN equivalent. The risk in
a page like this is drift in two directions: copied text, or a numeric mapping that quietly invents a rule. The
tests below check the data rows for the second, and the document for the licence and the reject criteria.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "rules" / "ep2_cwn_conversions_1280.json"
DOC = ROOT / "docs" / "rules" / "EP2_CONVERSION_1280.md"

#: Wording that would mean someone tried to convert a system rather than borrow a scene idea.
FORBIDDEN_NUMERIC = ("percentile", "d100", "33-66", "degrees of success", "mesh damage")


class ConversionDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.rows = cls.data["conversions"]

    def test_the_eight_elements_are_present(self):
        self.assertEqual(len(self.rows), 8)

    def test_every_row_names_a_cwn_reference_and_a_consequence(self):
        for row in self.rows:
            self.assertTrue(row["cwn_reference"].strip(), row["id"])
            self.assertTrue(row["consequence"].strip(), row["id"])

    def test_every_row_states_what_it_must_not_become(self):
        for row in self.rows:
            self.assertTrue(row["forbidden"], f"{row['id']} has no trap recorded")

    def test_no_conversion_row_proposes_a_numeric_ep_conversion(self):
        blob = json.dumps(self.rows).lower()
        for phrase in FORBIDDEN_NUMERIC:
            self.assertNotIn(phrase, blob, f"a conversion row smuggles in {phrase!r}")

    def test_the_rule_says_there_is_no_conversion(self):
        self.assertIn("No numerical conversion", self.data["rule"])

    def test_the_licence_is_recorded_as_not_importable(self):
        self.assertIn("CC BY-NC-SA", self.data["licence_note"])
        self.assertIn("not importable", self.data["licence_note"].lower())

    def test_psi_sleights_state_what_still_decides(self):
        for sleight in self.data["psi_sleights"]:
            self.assertTrue(sleight["bounded_use"].strip(), sleight["id"])
            self.assertTrue(sleight["what_still_decides"].strip(), sleight["id"])

    def test_a_technique_is_not_ready_without_all_ten_fields(self):
        self.assertEqual(len(self.data["technique_record_fields"]), 10)
        for field in ("owner", "range", "effort", "evidentiary limit"):
            self.assertIn(field, self.data["technique_record_fields"])

    def test_the_playtest_criterion_and_rejects_exist(self):
        self.assertIn("changes the next field decision", self.data["playtest_criterion"])
        self.assertEqual(
            set(self.data["reject_if"]),
            {"a second hacking roll", "an alert track", "a compulsory PSI subsystem"},
        )


class DocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_it_states_the_licence_and_no_import(self):
        self.assertIn("CC BY-NC-SA", self.text)
        self.assertIn("not importable", self.text.lower())

    def test_it_says_cwn_owns_resolution(self):
        self.assertIn("CWN owns hacking resolution", self.text)

    def test_the_two_worked_cases_are_present(self):
        self.assertIn("The Kurvi camera", self.text)
        self.assertIn("The dispatch audit", self.text)

    def test_the_playtest_criterion_is_printed(self):
        self.assertIn("CWN alone", self.text)
        self.assertIn("changes the next field decision", self.text)

    def test_no_ep_stat_block_or_numeric_mapping_appears(self):
        """The words may appear in a sentence that refuses them; they may not appear as a mapping."""
        negations = ("no ", "not ", "nothing", "never", "without")
        for sentence in re.split(r"(?<=[.!?])\s+", self.text.lower()):
            for phrase in FORBIDDEN_NUMERIC:
                if phrase in sentence:
                    self.assertTrue(any(word in sentence for word in negations),
                                    f"a sentence uses {phrase!r} as a mapping: {sentence[:120]}")
        self.assertIsNone(re.search(r"\b\d{1,3}%\b", self.text), "a percentage looks like a converted rating")


if __name__ == "__main__":
    unittest.main()
