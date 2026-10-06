"""Compatibility guard: issue #144 supersedes issue #108 UNHSS / Firewall naming."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
FACTIONS = (ROOT / "FACTIONS.md").read_text(encoding="utf-8")
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")


class Issue108SupersededBy144Tests(unittest.TestCase):
    def test_unsa_is_the_canonical_successor(self):
        self.assertIn("United Nations Security Agency (UNSA)", BOOK)
        self.assertIn("supersedes the UNHSS / Firewall naming", BOOK)
        self.assertIn("## Default Helsinki / UNSA affiliation", FACTIONS)

    def test_default_pc_is_unsa_agent(self):
        self.assertIn("belongs to and works for UNSA", BOOK)
        self.assertIn("default: UNSA agent", ORG)
        self.assertIn("multi_faction_membership: true", ORG)

    def test_unsa_keeps_the_broad_human_security_mission(self):
        for phrase in (
            "law-enforcement", "intelligence", "counterintelligence",
            "scientific research", "civil-defence", "disaster relief",
            "planetary defence", "Wallfacer",
        ):
            self.assertIn(phrase.lower(), BOOK.lower())

    def test_machine_readable_model_uses_unsa(self):
        self.assertIn("UNSA:", ORG)
        self.assertIn("canonical_name: United Nations Security Agency", ORG)
        self.assertNotIn("\nUNHSS:", ORG)


if __name__ == "__main__":
    unittest.main()
