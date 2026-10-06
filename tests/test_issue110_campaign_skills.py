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
        ):
            self.assertIn(phrase, rulebook)

        # The deferred character-design work must still be assigned to a dedicated issue.
        # Matched as a pattern rather than one literal phrase: issue #168 reworded this from
        # "attribute-system design issue" to "character-layer design issue" (more accurate,
        # since #39.8 covers Density, Polarization and the character ontology, not only
        # attributes) without updating the assertion, which is what left main red. The fact
        # asserted is unchanged, so the guard tolerates either wording instead of pinning
        # one and going stale on the next rename.
        self.assertRegex(
            rulebook,
            r"A dedicated [a-z-]+ design issue owns this work before it becomes executable "
            r"rules\.",
            "the deferred character-design work is no longer assigned to a dedicated issue",
        )


if __name__ == "__main__":
    unittest.main()
