"""The rules constitution is only permanent if a test can catch a quiet reversal (#1006).

The failure this guards against is not malice. It is an agent six months from now adding a fourth system, or
promoting WWN to core, or "simplifying" a rule because it looked heavy — all of it plausible, none of it visible
in a diff that only touches a JSON file.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION = ROOT / "data/rules/rules_constitution.json"
DOC = ROOT / "docs/rules/RULES_CONSTITUTION.md"


class RulesConstitutionTest(unittest.TestCase):
    def setUp(self):
        self.c = json.loads(CONSTITUTION.read_text(encoding="utf-8"))

    def test_the_constitution_exists_and_names_its_issue(self):
        self.assertEqual(self.c["format"], "noopunk.rules.constitution")
        self.assertIn("issues/1006", self.c["issue"])

    def test_cwn_is_first_in_precedence_and_is_the_only_core(self):
        self.assertEqual(self.c["precedence"][0], "CWN")
        core = [n for n, s in self.c["sources"].items() if s["role"] == "core"]
        self.assertEqual(core, ["CWN"], "exactly one source may be core")

    def test_wwn_and_awn_may_not_be_promoted_to_module_without_a_decision(self):
        """They are optional by author decision. A promotion must be a deliberate edit, not a drive-by."""
        for name in ("WWN", "AWN"):
            self.assertEqual(self.c["sources"][name]["role"], "mod")

    def test_the_minimum_playable_system_is_cwn_plus_swn(self):
        self.assertEqual(self.c["minimum_playable"], ["CWN", "SWN"])

    def test_every_source_declares_role_status_and_licence(self):
        for name, s in self.c["sources"].items():
            self.assertIn(s["role"], self.c["layers"], f"{name}: unknown layer")
            self.assertIn(s["licence_status"], ("verified", "unverified"), f"{name}: licence not assessed")
            self.assertTrue(s["licence"], f"{name}: no licence recorded")

    def test_an_unverified_licence_is_not_silently_trusted(self):
        """SWN and AWN are unverified here; recording that is the point, not an embarrassment."""
        unverified = [n for n, s in self.c["sources"].items() if s["licence_status"] == "unverified"]
        self.assertTrue(unverified, "if every licence becomes verified, this test should be deleted deliberately")

    def test_the_document_states_precedence_and_the_prohibitions(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Cities Without Number", text)
        self.assertIn("authoritative core", text)
        for phrase in ("Do not redesign", "Do not silently alter", "verbatim in behaviour"):
            self.assertIn(phrase, text, f"the doctrine lost a load-bearing line: {phrase}")


if __name__ == "__main__":
    unittest.main()
