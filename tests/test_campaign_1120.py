"""Structure checks for the #1120 campaign-writing deliverables."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "docs" / "campaign" / "CAMPAIGN_01_CASE_TUESDAY.md"
LEDGER = ROOT / "docs" / "campaign" / "CAMPAIGN_01_LEDGER.md"
ROADMAP = ROOT / "docs" / "campaign" / "CAMPAIGN_01_ROADMAP.md"
BRIEF = ROOT / "design" / "CAMPAIGN_WRITING_PIVOT.md"
README = ROOT / "docs" / "campaign" / "README.md"


class CampaignWritingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case = CASE.read_text(encoding="utf-8")
        cls.ledger = LEDGER.read_text(encoding="utf-8")
        cls.roadmap = ROADMAP.read_text(encoding="utf-8")
        cls.brief = BRIEF.read_text(encoding="utf-8")
        cls.readme = README.read_text(encoding="utf-8")

    def test_all_first_outputs_exist_and_are_linked(self):
        for name in ("CAMPAIGN_01_CASE_TUESDAY.md", "CAMPAIGN_01_LEDGER.md", "CAMPAIGN_01_ROADMAP.md"):
            self.assertIn(name, self.readme)
        self.assertIn("CAMPAIGN_WRITING_PIVOT.md", self.readme)
        self.assertIn("CAMPAIGN_01_CASE_TUESDAY.md", self.brief)

    def test_case_has_reachable_core_clues_and_no_retired_resolver(self):
        for clue in ("C1", "C2", "C3", "C4"):
            self.assertIn(clue, self.case)
        self.assertIn("Core clue", self.case)
        self.assertIn("2d6 + attribute modifier + skill rank", self.case)
        self.assertNotIn("1d10", self.case)
        self.assertNotIn("Fate", self.case)

    def test_case_is_a_complete_six_scene_manuscript(self):
        for scene in ("Scene 1", "Scene 2", "Scene 3", "Scene 4", "Scene 5", "Scene 6"):
            self.assertIn(scene, self.case)
        self.assertIn("Option A", self.case)
        self.assertIn("Option D", self.case)
        self.assertIn("Handout A", self.case)

    def test_ledger_keeps_observation_and_interpretation_apart(self):
        for status in ("verified", "institutional", "testimony", "rumor", "contested", "open"):
            self.assertIn(status, self.ledger)
        for row in ("L1", "L10"):
            self.assertIn(row, self.ledger)
        self.assertIn("GM ONLY", self.ledger)

    def test_roadmap_has_seven_episodes_and_no_final_ontology(self):
        for episode in ("E01", "E02", "E03", "E04", "E05", "E06", "E07"):
            self.assertIn(episode, self.roadmap)
        self.assertIn("does not resolve", self.roadmap.lower())

    def test_brief_records_the_50_25_25_and_priority(self):
        self.assertIn("50 / 25 / 25", self.brief)
        self.assertIn("Write adventures, cases, episodes and connected campaigns", self.brief)
        self.assertIn("No exposition dump", self.brief)
        self.assertIn("CWN remains the immutable core", self.brief)


if __name__ == "__main__":
    unittest.main()
