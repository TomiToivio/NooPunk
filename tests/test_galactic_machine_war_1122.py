"""Canon checks for the Galactic Machine War register (#1122)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "design" / "GALACTIC_MACHINE_WAR.md"
DATA = ROOT / "data" / "world" / "galactic_machine_war_1122.json"


class GalacticMachineWarTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_document_is_canon_and_reconciles_the_names(self):
        self.assertIn("Canon — author decision #1122", self.doc)
        self.assertIn("Confederacy", self.doc)
        self.assertIn("Zookeepers", self.doc)
        self.assertIn("Greater Orion Arm Co-Prosperity Sphere", self.doc)
        self.assertIn("not the machine civilisation", self.doc)

    def test_three_prohibitions_are_numbered_and_distinct(self):
        prohibitions = self.data["prohibitions"]
        self.assertEqual(len(prohibitions), 3)
        self.assertEqual([row["order"] for row in prohibitions], [1, 2, 3])
        self.assertEqual({row["id"] for row in prohibitions}, {
            "prohibition.biosphere_noosphere", "prohibition.stargates",
            "prohibition.machine_gods",
        })
        self.assertEqual(len({row["text"] for row in prohibitions}), 3)

    def test_the_infection_chain_and_simultaneous_outbreaks(self):
        chain = self.data["machine_civilisation"]
        self.assertIn("recruitment_signal", chain["transmission_components"])
        self.assertIn("machine_directed_virus", chain["transmission_components"])
        self.assertEqual(self.data["human_catastrophe"]["simultaneous_outbreaks"],
                         ["United States", "China"])
        self.assertTrue(self.data["human_catastrophe"]["intervention_prevented_extinction"])

    def test_consent_dispute_is_not_a_simple_good_evil_split(self):
        dispute = self.data["consent_dispute"]
        self.assertEqual(dispute["confederacy"]["doctrine"], "no_forced_assimilation")
        self.assertIn("preserved", dispute["orion"]["doctrine"])
        self.assertEqual(dispute["alliance_scope"], "narrow_cooperation_against_machine_gods")

    def test_mantids_reptilians_and_greys_keep_distinct_roles(self):
        roles = {row["id"]: row for row in self.data["species_roles"]}
        self.assertEqual(roles["species.mantids"]["role"], "senior_orion_architects")
        self.assertEqual(roles["species.reptilians"]["role"], "militarised_orion_enforcers")
        self.assertIn("not_natural_warriors", roles["species.greys"]["note"])
        self.assertIn("individuals_vary", roles["species.reptilians"]["note"])

    def test_public_and_gm_truth_are_separated(self):
        layers = self.data["evidence_layers"]
        self.assertTrue(any("machine civilisation exists" in row for row in layers["gm_truth"]))
        self.assertTrue(any("rogue ASI/Singularity" in row for row in layers["public_account"]))
        self.assertTrue(any("Three Prohibitions" in row for row in layers["classified"]))
        self.assertTrue(any("not" in row for row in layers["contested_or_open"]))

    def test_no_mechanics_or_invented_coordinates(self):
        text = json.dumps(self.data).lower()
        for forbidden in ("cwn", "hit point", "damage", "coordinates", "latitude", "longitude"):
            self.assertNotIn(forbidden, text)
        self.assertIn("no mechanics", self.doc.lower())


if __name__ == "__main__":
    unittest.main()
