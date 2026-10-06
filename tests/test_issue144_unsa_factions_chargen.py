"""Acceptance guard for issue #144: Helsinki factions, UNSA and Lifepath chargen."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
FACTIONS = (ROOT / "FACTIONS.md").read_text(encoding="utf-8")
TERMS = (ROOT / "rulebook" / "8_FACTIONS.md").read_text(encoding="utf-8")
SOCIAL = (ROOT / "rulebook" / "4_SOCIAL.md").read_text(encoding="utf-8")
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")
SCHEMA = json.loads((ROOT / "data" / "world" / "social_affect_schema.json").read_text(encoding="utf-8"))


class HelsinkiScopeTests(unittest.TestCase):
    def test_default_campaign_is_helsinki_centered(self):
        self.assertIn("default NoöPunk campaign is centered on **Helsinki**", BOOK)
        self.assertIn("small number of factions", BOOK)
        self.assertIn("small Helsinki-centered faction network", FACTIONS)

    def test_local_institutional_chain(self):
        for name in ("Suojelupoliisi", "Europol", "UNSA"):
            self.assertIn(name, BOOK)
            self.assertIn(name, ORG)


class UNSATests(unittest.TestCase):
    def test_canonical_name_and_mandate(self):
        self.assertIn("United Nations Security Agency (UNSA)", BOOK)
        for term in ("law-enforcement", "intelligence", "counterintelligence", "military",
                     "scientific", "NHI", "X-Risk"):
            self.assertIn(term.lower(), BOOK.lower())

    def test_civilian_side(self):
        for term in ("scientific research", "diplomatic", "civil-defence", "development",
                     "humanitarian", "disaster relief", "reconstruction"):
            self.assertIn(term.lower(), BOOK.lower())

    def test_nicknames_and_mj12_boundary(self):
        for term in ("UN X-Risk Agency", "UN NHI Agency", "X-COM", "X-Files",
                     "Men in Black", "MJ-12"):
            self.assertIn(term, BOOK)
        self.assertIn("not an acceptable nickname", BOOK)

    def test_world_government_role(self):
        self.assertIn("federal government of Earth", BOOK)
        self.assertIn("engines of global federalization", BOOK)

    def test_wendt_double_outcome(self):
        self.assertIn("Alexander Wendt", BOOK)
        self.assertIn("both outcomes happen", BOOK)
        for term in ("ontological shock", "alle-gegen-alle", "alien-worshipping cults",
                     "xenophobic", "hybrid", "PSI", "global unification"):
            self.assertIn(term.lower(), BOOK.lower())


class FactionMechanicsTests(unittest.TestCase):
    def test_scale_is_minus10_plus10_everywhere(self):
        self.assertEqual(SCHEMA["score_range"], [-10, 10])
        self.assertIn("−10…+10", TERMS)
        self.assertIn("-10 to +10", SOCIAL)

    def test_multiple_memberships_and_starting_reputation(self):
        for text in (BOOK, TERMS):
            self.assertIn("10 positive", text)
            self.assertIn("two or three factions", text)
            self.assertIn("6/4", text)
            self.assertIn("5/3/2", text)

    def test_taxonomy_separates_nhi_ontology_from_faction(self):
        for term in ("Political", "Criminal", "Civil Society", "Religious",
                     "Corporate", "Governmental", "NHI"):
            self.assertIn(term, TERMS)
        self.assertIn("ontology/type separate from political faction", TERMS)


class CharacterGenerationTests(unittest.TestCase):
    def test_character_generation_chapter_exists(self):
        self.assertIn("## 9. Character Generation", BOOK)
        self.assertIn("chosen manually", BOOK)
        self.assertIn("randomized", BOOK)

    def test_default_training(self):
        self.assertIn("UNSA Police Academy", BOOK)
        for track in ("UNSA SWAT Academy", "UNSA PSI Academy",
                      "UNSA TECH Academy", "UNSA NHI Academy"):
            self.assertIn(track, BOOK)

    def test_lifepath_connects_social_and_career_layers(self):
        for term in ("Origin / place of birth", "Motivations", "Contacts",
                     "Recruitment into UNSA", "Starting assignment",
                     "Starting Reputation allocation", "Final character summary"):
            self.assertIn(term, BOOK)


if __name__ == "__main__":
    unittest.main()
