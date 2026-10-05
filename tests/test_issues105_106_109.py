"""Acceptance guards for issues #105, #106, and #109."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
BOOK=(ROOT/"RULEBOOK.md").read_text(encoding="utf-8")
FACTIONS=(ROOT/"FACTIONS.md").read_text(encoding="utf-8")
PARTIES=(ROOT/"data/world/un_parties.yaml").read_text(encoding="utf-8")

class Issue105Tests(unittest.TestCase):
    def test_reverse_engineering_and_contact_map(self):
        for phrase in (
            "Soviet/Russian lineage", "Nordic lineage", "Merkabah spacecraft",
            "CE-5", "Conscious Agent / Noetic network", "Tridactyls",
            "Undersea NHI bases and transit corridors are canon", "Orion infiltration",
        ):
            self.assertIn(phrase, BOOK)
    def test_exploratory_questions_remain_open(self):
        self.assertIn("current status remains unresolved", BOOK)
        self.assertIn("exact recoveries", BOOK)

class Issue106Tests(unittest.TestCase):
    def test_wendt_disclosure_model(self):
        for phrase in (
            "Alexander Wendt", "unification and fragmentation happen simultaneously",
            "Disclosure depth model", "multiple independent epistemic systems converge",
            "Men in Black", "Sphere Network", "Noöspheric phase transition",
        ):
            self.assertIn(phrase, BOOK)

class Issue109Tests(unittest.TestCase):
    def test_initial_parties(self):
        for name in (
            "Bioconservatives", "Libertarian Party",
            "United Earth Social Democratic Party", "The Multitude",
        ):
            self.assertIn(name, BOOK)
            self.assertIn(name, PARTIES)
            self.assertIn(name, FACTIONS)
        self.assertIn("won every UN parliamentary and presidential election so far", PARTIES)
        self.assertIn("extra_parliamentary_factions: true", PARTIES)
        self.assertIn("open_for_future_parties: true", PARTIES)

if __name__=="__main__":
    unittest.main()
