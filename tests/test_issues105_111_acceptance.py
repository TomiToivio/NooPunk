"""Acceptance guards for coordinated issues #105, #106, #107, #109, #110, #111."""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
BOOK=(ROOT/"RULEBOOK.md").read_text(encoding="utf-8")
AGENTS=(ROOT/"AGENTS.md").read_text(encoding="utf-8")
FACTIONS=(ROOT/"FACTIONS.md").read_text(encoding="utf-8")
README=(ROOT/"README.md").read_text(encoding="utf-8")
LOOP=(ROOT/"docs/design/GAMEPLAY_LOOP.md").read_text(encoding="utf-8")
GRAPH=json.loads((ROOT/"data/world/social_graph.json").read_text(encoding="utf-8"))
CORE=json.loads((ROOT/"data/rules/core.json").read_text(encoding="utf-8"))
PARTIES=(ROOT/"data/world/un_parties.yaml").read_text(encoding="utf-8")


class Issue105Lore(unittest.TestCase):
    def test_national_programs_and_contact(self):
        for phrase in ("Soviet/Russian lineage","China","Nordic lineage","India","Egypt","Israel",
                       "CE-5","Tridactyls","Undersea NHI bases","Orion infiltration"):
            self.assertIn(phrase,BOOK)
    def test_open_questions_stay_open(self):
        self.assertIn("current status remains unresolved",BOOK)
        self.assertIn("exact recoveries",BOOK)


class Issue106Disclosure(unittest.TestCase):
    def test_wendt_model_and_depths(self):
        for phrase in ("Alexander Wendt","unification and fragmentation simultaneously",
                       "Disclosure depth model","independent epistemic systems converge",
                       "Men in Black","Sphere Network","Noöspheric phase transition"):
            self.assertIn(phrase,BOOK)


class Issue107Affect(unittest.TestCase):
    def test_one_affect_model(self):
        self.assertEqual(GRAPH["affect_score"],{"min":-100,"max":100,"zero":"explicit neutral only; missing edge means unknown"})
        self.assertTrue(GRAPH["rules"]["directional"])
        self.assertTrue(GRAPH["rules"]["ambivalence"])
        for domain in ("faction_us","faction_frontier","motivation","reputation","contact"):
            self.assertIn(domain,GRAPH["edge"]["domains"])
        self.assertIn("Faction = US^",BOOK)
        self.assertIn("Asteroid Belt",LOOP)


class Issue109Parties(unittest.TestCase):
    def test_four_initial_blocs(self):
        for party in ("Bioconservatives","Libertarian Party","United Earth Social Democratic Party","The Multitude"):
            self.assertIn(party,BOOK)
            self.assertIn(party,PARTIES)
        self.assertIn("won every UN parliamentary and presidential election so far",PARTIES)
        self.assertIn("extra_parliamentary_factions: true",PARTIES)


class Issue110SkillsOntology(unittest.TestCase):
    def test_campaign_fields_and_future_mechanics(self):
        for phrase in ("Pilot (Space)","Medicine (Emergency Care)","Know (Investigation)",
                       "Know (Psychology)","Know (QIP)","Know (Parapsychology)",
                       "Know (NHI Studies)","Noetic Projection","Density","Polarization"):
            self.assertIn(phrase,BOOK)
        self.assertIn("Language belongs to Social",BOOK)
        self.assertIn("final skill list is deferred",BOOK.lower())


class Issue111IndependentCore(unittest.TestCase):
    def test_independent_identity(self):
        self.assertTrue(CORE["system_identity"]["independent"])
        self.assertIn("independent RPG system",BOOK)
        self.assertIn("independent NoöPunk d10 rules system",README)
        self.assertIn("independent original rules system",AGENTS)
    def test_numeric_core(self):
        self.assertEqual((CORE["stats"]["min"],CORE["stats"]["max"]),(1,10))
        self.assertEqual((CORE["skills"]["min"],CORE["skills"]["max"]),(1,10))
        self.assertEqual(CORE["skill_check"]["formula"],"STAT + Skill + 1d10")
        self.assertEqual(sorted(map(int,CORE["difficulties"].keys())),[9,13,15,17,21,24,29])
        self.assertEqual(CORE["opposed"]["tie"],"deferred")
        self.assertEqual(CORE["criticals"],"deferred")
        self.assertEqual(CORE["situational_modifiers"],"deferred")


if __name__=="__main__":
    unittest.main()
