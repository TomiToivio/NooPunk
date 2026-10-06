"""Regression guard for issue #144 superseding issue #108 organization naming."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
FACTIONS = (ROOT / "FACTIONS.md").read_text(encoding="utf-8")
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")
SOCIAL = (ROOT / "rulebook" / "4_SOCIAL.md").read_text(encoding="utf-8")


class UNSACanonTests(unittest.TestCase):
    def test_canonical_name(self):
        self.assertIn("United Nations Security Agency", BOOK)
        self.assertIn("## 38. UNSA: default campaign institution", BOOK)
        self.assertIn("UNSA:", ORG)

    def test_old_in_world_name_is_superseded(self):
        self.assertIn("Firewall remains a design inspiration", BOOK)
        self.assertIn("no longer uses Firewall as an in-world faction name", BOOK)

    def test_early_labels_and_nicknames(self):
        for label in ("UN X-Risk Agency", "UN NHI Agency", "X-COM", "X-Files", "Men in Black"):
            with self.subTest(label=label):
                self.assertIn(label, BOOK)
        self.assertIn("MJ-12 is not a tolerated nickname", BOOK)

    def test_humanity_protection_mandate(self):
        for term in ("law-enforcement", "intelligence", "counterintelligence", "military", "scientific"):
            with self.subTest(term=term):
                self.assertIn(term, BOOK)
        for risk in ("NHI", "AGI/ASI", "Noöspace", "X-Risks"):
            with self.subTest(risk=risk):
                self.assertIn(risk, BOOK)

    def test_civilian_side_and_world_government_role(self):
        for term in ("scientific research", "diplomatic", "civil-defence", "development", "disaster relief", "reconstruction"):
            with self.subTest(term=term):
                self.assertIn(term, BOOK)
        self.assertIn("federal government of Earth", BOOK)

    def test_default_character_is_unsa_agent(self):
        self.assertIn("belongs to and works for UNSA", BOOK)
        self.assertIn("Default UNSA affiliation", FACTIONS)
        self.assertIn("## UNSA campaign frame", SOCIAL)


if __name__ == "__main__":
    unittest.main()
