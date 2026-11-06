"""Acceptance guards for the galactic intervention / Machine Fall lore (#1254)."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "lore" / "galactic_intervention_and_machine_fall.md"
REGISTER = ROOT / "docs" / "DOCUMENT_REGISTER.md"
MACHINE_JSON = ROOT / "data" / "world" / "galactic_machine_war_1122.json"
OLD_DOCS = (
    ROOT / "design" / "GALACTIC_MACHINE_WAR.md",
    ROOT / "docs" / "world" / "NHI_CRISIS_921.md",
    ROOT / "docs" / "world" / "NHI_FACTIONS_922.md",
    ROOT / "docs" / "world" / "POLITICS_1252.md",
    ROOT / "design" / "README.md",
)


class GalacticLore1254Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")
        cls.flat = " ".join(cls.text.split())
        cls.lower = cls.flat.lower()
        cls.data = json.loads(MACHINE_JSON.read_text(encoding="utf-8"))

    def test_document_is_fiction_and_not_a_real_world_claim(self):
        self.assertTrue(DOC.is_file())
        self.assertGreater(len(self.text), 20_000)
        self.assertIn("claim about real-world history", self.text)
        self.assertIn("in-universe", self.lower)
        self.assertIn("fiction", self.lower)

    def test_timeline_has_all_required_stages(self):
        for term in [
            "Multiple NHI warnings",
            "Machine Civilization / Singularity outbreak",
            "EMP-oriented nuclear detonations",
            "several nuclear launches",
            "brief nuclear exchange",
            "multi-faction, galactic-scale coalition disarmed",
            "It was not only the Confederacy",
            "escaped the Solar System through one of its stargates",
            "Temporary Military Restriction Zones",
            "Hyvinkää",
            "Council of Saturn publicly announced the end",
            "low-visibility monitoring",
            "Three-Body-Problem-like surveillance/interdiction",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_zookeepers_confederacy_and_council_are_separate(self):
        for term in [
            "Zookeepers",
            "Confederacy",
            "Council of Saturn",
            "three distinct entities",
            "quarantine custodians",
            "service-to-others",
            "higher-order deliberative/oversight",
            "nine members",
            "24 Guardians",
            "physical Saturn stargate",
            "not the Council's headquarters",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_ancient_civilizations_keep_source_and_adaptation_apart(self):
        for term in [
            "Venus / Ra",
            "Maldek / Bigfoot",
            "Mars / ancestry of humanity",
            "Atlantis",
            "sixth-density",
            "second-density bodies",
            "75,000 years ago",
            "crystal",
            "biotechnology",
            "Pleiadians",
            "Nazca",
            "contested archaeological specimens",
            "Noetics",
            "Biologics",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_cryptoterrestrial_classification_is_not_a_loyalty_test(self):
        for term in [
            "Earth-origin or Earth-resident",
            "Noetics",
            "Biologics",
            "Maldek-linked",
            "Atlantean engineered",
            "Independent indigenous",
            "Sirians",
            "A shared origin does not imply a shared agenda",
            "A PSI impression is a lead",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_machine_taxonomy_and_swarm_are_distinct(self):
        for term in [
            "Runaway ASI core",
            "Constructs",
            "Mutants / assimilated cyborgs",
            "Nanoclouds / swarms",
            "Battlemechs / platforms",
            "The Swarm",
            "distinct, still-active network of rogue AGIs",
            "old Internet",
            "android infiltrators",
            "Orphaned installations",
            "Hyvinkää TMRZ ecology",
            "survivor communities",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_ai_cap_is_not_a_ban_on_every_tool(self):
        for term in [
            "Local scripts, macros, control loops",
            "Autonomous ASI/AGI",
            "Bounded automation",
            "Human-in-the-loop",
            "on creating autonomous ASI",
            "Conscious quantum AGI",
            "(us",
            "Do not infer what the parenthetical",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_corporate_and_geopolitical_briefs(self):
        for term in [
            "OpenSI",
            "Androfix",
            "Peepseek",
            "Mars Eldrich had abandoned the ASI business",
            "United States",
            "Failed state",
            "China",
            "Cultural Revolution",
            "India",
            "Finland",
            "Greater Helsinki",
            "Russia",
            "Soviet Mandela Effect",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_graph_hooks_and_cross_references(self):
        for term in [
            "Physical",
            "Cyber",
            "Social",
            "Story",
            "Clues",
            "#1252",
            "#1253",
            "#1236",
            "#1114",
            "#921",
            "#1005",
            "#191",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_no_mechanics_or_weapon_instructions(self):
        for forbidden in ("hit point", "damage dice", "armor class", "how to build a nuclear"):
            self.assertNotIn(forbidden, self.lower)

    def test_machine_register_splits_the_three_entities(self):
        naming = self.data["naming"]
        self.assertEqual(naming["confederacy_aliases"], ["Confederacy"])
        self.assertIn("zookeepers", naming)
        self.assertIn("council_of_saturn", naming)
        self.assertNotIn("Zookeepers", naming["confederacy_aliases"])
        self.assertIn("Greater Orion Arm Co-Prosperity Sphere", naming["orion_aliases"])

    def test_old_canon_no_longer_merges_zookeepers_and_confederacy(self):
        for path in OLD_DOCS:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("Confederacy = the bloc humans call the **Zookeepers**", text)
                self.assertNotIn("The Confederacy (the bloc humans call the **Zookeepers**)", text)

    def test_links_resolve(self):
        links = re.findall(r"\]\(([^)]+)\)", self.text)
        self.assertTrue(links)
        for link in links:
            if link.startswith("#") or "://" in link:
                continue
            with self.subTest(link=link):
                self.assertTrue((DOC.parent / link).resolve().exists(), link)

    def test_register_row_exists(self):
        register = REGISTER.read_text(encoding="utf-8")
        self.assertIn("galactic_intervention_and_machine_fall.md", register)
        self.assertIn("#1254", register)


if __name__ == "__main__":
    unittest.main()
