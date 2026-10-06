"""Acceptance guard for issues #158 and #162."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
ACADEMY = json.loads((ROOT / "data" / "rules" / "unsa_academy.json").read_text(encoding="utf-8"))
DOCTRINE = (ROOT / "docs" / "design" / "DEFAULT_INVESTIGATION_FANTASY.md").read_text(encoding="utf-8")
CYBER = (ROOT / "rulebook" / "5_CYBERNETIC.md").read_text(encoding="utf-8")
SKILLS = json.loads((ROOT / "data" / "rules" / "skills.json").read_text(encoding="utf-8"))
FIELDS = json.loads((ROOT / "data" / "rules" / "campaign_skill_fields.json").read_text(encoding="utf-8"))


class UNSAAcademyTests(unittest.TestCase):
    def test_universal_package_uses_canonical_skills(self):
        canonical = {row["name"] for row in SKILLS["skills"]}
        self.assertEqual(ACADEMY["universal_training_rating"], 3)
        for skill in ACADEMY["universal_skills"]:
            self.assertIn(skill, canonical)

    def test_required_campaign_fields_exist(self):
        for spec in ACADEMY["universal_fields"]:
            family, value = spec.split(" (", 1)
            value = value[:-1]
            self.assertIn(value, FIELDS["fields"][family])

    def test_no_new_generic_psionics_skill(self):
        self.assertIn("Psychic Defence", ACADEMY["universal_skills"])
        self.assertNotIn("Psionics", ACADEMY["universal_skills"])

    def test_equipment_stays_stat_free(self):
        self.assertIn("Numeric equipment statistics remain undefined", CYBER)
        self.assertNotIn('"damage"', (ROOT / "data" / "rules" / "unsa_academy.json").read_text(encoding="utf-8"))


class InvestigationDoctrineTests(unittest.TestCase):
    def test_distributed_cell(self):
        for term in ("Player character", "Field partner", "Controller", "Embedded forensic AI"):
            self.assertIn(term, DOCTRINE)

    def test_reality_triangulation_and_force_boundary(self):
        self.assertIn("Triangulate reality before acting", DOCTRINE)
        self.assertIn("NHI status alone is never grounds for lethal force", DOCTRINE)
        self.assertIn("Never authorize lethal force solely from augmented perception", DOCTRINE)

    def test_ai_is_not_agi(self):
        self.assertIn("not an AGI", DOCTRINE)
        self.assertIn("may not autonomously", CYBER)

    def test_ace_is_multichannel(self):
        self.assertIn("Anomalous Cognition Examination", DOCTRINE)
        self.assertIn("No single channel is definitive", DOCTRINE)


if __name__ == "__main__":
    unittest.main()
