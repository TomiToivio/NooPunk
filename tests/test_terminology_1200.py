"""Terminology integrity for #1200: the name, the nickname, the retired word, and the open question.

#1200 arrived after rulebook/22 had already retired "Firewall" as an in-world name and warned that the
"Great Firewall" is a different thing entirely. Both texts are the author's, so the fix is not to pick a
winner in prose — it is to record which word is which, and to refuse to close the one question (#1200 vs
#344: EuroNET or Safenet) that only the author can answer.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "world" / "terminology_1200.json"

STATUSES = {
    "canon", "canon_project_name", "canon_official_name", "canon_operational_shorthand",
    "canon_perimeter_name", "unofficial_nickname", "legacy_and_journalistic", "retired", "not_canon",
}


class TerminologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.terms = {t["term"]: t for t in cls.data["terms"]}

    def test_schema_and_both_source_issues(self):
        self.assertEqual(self.data["schema"], "noopunk.terminology/1")
        joined = " ".join(self.data["source_issues"])
        self.assertIn("issues/1200", joined)
        self.assertIn("issues/517", joined)

    def test_every_term_has_a_known_status_and_a_real_source(self):
        for name, term in self.terms.items():
            self.assertIn(term["status"], STATUSES, name)
            path = ROOT / term["governed_by"]
            self.assertTrue(path.exists(), f"{name} is governed by a document that does not exist")
            self.assertIn(name.split(" (")[0], path.read_text(encoding="utf-8"),
                          f"{name} is attributed to a document that never mentions it")

    def test_firewall_is_not_an_in_world_name(self):
        self.assertEqual(self.terms["Firewall"]["status"], "retired")
        self.assertEqual(self.terms["Great Firewall"]["status"], "legacy_and_journalistic")
        for name in ("Firewall", "Great Firewall"):
            self.assertNotIn(self.terms[name]["status"], {"canon", "canon_perimeter_name"})

    def test_panopticon_stays_a_nickname(self):
        term = self.terms["Panopticon"]
        self.assertEqual(term["status"], "unofficial_nickname")
        self.assertIn("must_not", term)

    def test_aegis_is_not_canon(self):
        self.assertEqual(self.terms["AEGIS"]["status"], "not_canon")

    def test_the_perimeter_has_a_name(self):
        self.assertEqual(self.terms["Plato/EISS perimeter"]["status"], "canon_perimeter_name")

    def test_euronet_versus_safenet_stays_open(self):
        """The one decision this file must not make for the author."""
        term = self.terms["EuroNET"]
        self.assertEqual(term["relationship_to_safenet"], "OPEN")
        self.assertTrue(term["open_question"].strip())
        self.assertEqual(self.terms["Safenet"]["status"], "canon")

    def test_the_containment_regime_is_named_once(self):
        self.assertEqual(self.terms["Blackwall"]["status"], "canon")
        self.assertIn("containment regime", self.terms["Blackwall"]["meaning"])


if __name__ == "__main__":
    unittest.main()
