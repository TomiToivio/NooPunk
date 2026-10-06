import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Issue110CampaignSkillsTest(unittest.TestCase):
    def test_campaign_profile_is_compact_and_contains_required_fields(self):
        profile = json.loads((ROOT / "data/rules/campaign_skill_fields.json").read_text())
        fields = profile["fields"]

        self.assertEqual(
            fields["Pilot"],
            ["Ground Vehicles", "Aircraft", "Spacecraft", "Drones"],
        )
        self.assertIn("Emergency Medicine", fields["Medicine"])
        self.assertIn("Psychotronic Medicine", fields["Medicine"])
        self.assertIn("Psychotronics", fields["Hardware"])

        required_know = {
            "Psychology",
            "Law",
            "Quantum Information Panpsychism",
            "Parapsychology",
            "NHI Studies",
            "X-Risk Studies",
            "Noetics",
        }
        self.assertTrue(required_know.issubset(set(fields["Know"])))
        self.assertNotIn("Investigation", fields["Know"])
        self.assertNotIn("Intelligence", fields["Know"])
        self.assertNotIn("Counterintelligence", fields["Know"])
        self.assertEqual(fields["Exotic Skill"], [])

    def test_rulebook_records_canonical_boundaries_and_psi_design(self):
        rulebook = (ROOT / "RULEBOOK.md").read_text()
        for phrase in (
            "## 39. Campaign-scoped skills and specialist fields",
            "Dr. Harri S. Romppainen primarily solves cases through Know (Psychology)",
            "The **Law of One / Ra Material belongs inside NHI Studies**",
            "**Hardware (Psychotronics)**",
            "**Noetic Projection**",
            "dedicated character-layer design issue",
        ):
            self.assertIn(phrase, rulebook)


if __name__ == "__main__":
    unittest.main()
