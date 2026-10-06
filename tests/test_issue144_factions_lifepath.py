"""Acceptance guard for issue #144: factions, UNSA and Lifepath character generation."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
FACTIONS = (ROOT / "rulebook" / "8_FACTIONS.md").read_text(encoding="utf-8")
SOCIAL = (ROOT / "rulebook" / "4_SOCIAL.md").read_text(encoding="utf-8")
SCHEMA = json.loads((ROOT / "data" / "world" / "social_affect_schema.json").read_text(encoding="utf-8"))
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")


class FactionModelTests(unittest.TestCase):
    def test_taxonomy(self):
        for term in (
            "Political Factions", "Criminal Factions", "Civil Society and Knowledge Factions",
            "Religious and Esoteric Factions", "Corporate Factions", "Governmental Factions",
            "NHI Factions / Civilizations",
        ):
            with self.subTest(term=term):
                self.assertIn(term, FACTIONS)

    def test_nhi_type_is_not_faction(self):
        self.assertIn("NHI ontology is not NHI allegiance", FACTIONS)
        for term in ("Biologics", "Constructs", "Plasmoids", "Noetics", "Process Intelligences"):
            self.assertIn(term, FACTIONS)

    def test_multi_faction_reputation_pool(self):
        self.assertIn("several factions simultaneously", FACTIONS)
        self.assertIn("10 positive Faction Reputation points", FACTIONS)
        self.assertIn("6 / 4", FACTIONS)
        self.assertIn("5 / 3 / 2", FACTIONS)

    def test_social_scale(self):
        self.assertEqual(SCHEMA["score_range"], [-10, 10])
        self.assertIn("-10 to +10", FACTIONS)
        self.assertIn("-10 to +10", SOCIAL)


class UNSATests(unittest.TestCase):
    def test_name_and_chain(self):
        self.assertIn("United Nations Security Agency", BOOK)
        self.assertIn("Suojelupoliisi → Europol", BOOK)
        self.assertIn("UNSA:", ORG)

    def test_disclosure_both(self):
        self.assertIn("Both happen", BOOK)
        self.assertIn("simultaneously", BOOK)
        self.assertIn("federal government of Earth", BOOK)

    def test_nicknames(self):
        for term in ("UN X-Risk Agency", "UN NHI Agency", "X-COM", "X-Files", "Men in Black"):
            self.assertIn(term, BOOK)
        self.assertIn("MJ-12 is not a tolerated nickname", BOOK)


class CharacterGenerationTests(unittest.TestCase):
    def test_chapter_exists(self):
        self.assertIn("## Character Generation", BOOK)
        self.assertIn("choose", BOOK.lower())
        self.assertIn("roll randomly", BOOK.lower())

    def test_training(self):
        for term in ("UNSA Police Academy", "UNSA SWAT Academy", "UNSA PSI Academy",
                     "UNSA TECH Academy", "UNSA NHI Academy"):
            self.assertIn(term, BOOK)

    def test_alternative_campaigns(self):
        self.assertIn("Alternative campaigns", BOOK)
        self.assertIn("independent investigators", BOOK)


if __name__ == "__main__":
    unittest.main()
