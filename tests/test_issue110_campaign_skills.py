import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Issue110CampaignSkillsTest(unittest.TestCase):
    def test_campaign_profile_is_compact_and_contains_required_fields(self):
        profile = json.loads((ROOT / "data/rules/campaign_skill_fields.json").read_text())
        fields = profile["fields"]

        # Re-baselined by issue #164: #159/#160 locked the canonical skill vocabulary
        # and rewrote this profile, so the guard now asserts the resolved profile
        # instead of the pre-#160 Eclipse Phase-derived names.
        self.assertEqual(fields["Pilot"], ["Ground Vehicles", "Aircraft", "Spacecraft", "Drones"])
        self.assertIn("Emergency Medicine", fields["Medicine"])
        # Forensics is a standalone canonical Skill under §4.1, not a Medicine field.
        self.assertNotIn("Forensics", fields["Medicine"])
        self.assertIn("Psychotronics", fields["Hardware"])

        required_know = {
            "Psychology",
            "Law",
            "NHI Studies",
            "X-Risk Studies",
            "Noetics",
            "Quantum Information Panpsychism",
            "Parapsychology",
        }
        self.assertTrue(required_know.issubset(set(fields["Know"])))
        self.assertEqual(fields["Exotic Skill"], [])

    def test_rulebook_records_boundaries_and_deferred_psi_design(self):
        rulebook = (ROOT / "RULEBOOK.md").read_text()
        for phrase in (
            "## 39. Campaign-scoped skills and specialist fields",
            "Dr. Harri S. Romppainen primarily solves cases through Know (Psychology)",
            "The **Law of One / Ra Material belongs inside NHI Studies**",
            "**Hardware (Psychotronics)**",
            "**Noetic Projection**",
            "dedicated attribute-system design issue",
        ):
            self.assertIn(phrase, rulebook)


if __name__ == "__main__":
    unittest.main()
