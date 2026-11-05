"""Guards for the author writing queue audit (#1216)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "docs" / "design" / "AUTHOR_WRITING_QUEUE_1216.md"
LIFEPATH = ROOT / "docs" / "campaign" / "TONY_GERMAN_LIFEPATH.md"
FIRST_DAY = ROOT / "docs" / "campaign" / "EPISODE_00_FIRST_DAY.md"
CASE = ROOT / "docs" / "scenarios" / "CASE_01_THE_TUESDAY_COMPLAINT.md"
LEDGER_TARGET = ROOT / "docs" / "campaign" / "EPISODE_01_EPISTEMIC_LEDGER.md"
CASE_TARGET = ROOT / "docs" / "campaign" / "EPISODE_01_FIRST_CASE.md"


class AuthorQueueTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.queue = QUEUE.read_text(encoding="utf-8")

    def test_queue_is_a_status_index_not_a_manuscript(self):
        self.assertIn("Author-owned queue", self.queue)
        self.assertIn("not a manuscript", self.queue)
        self.assertIn("Do not ghostwrite", self.queue)
        for mark in ("READY", "EMPTY", "COVERED", "OPEN"):
            self.assertIn(mark, self.queue)

    def test_existing_case_and_ledger_are_not_duplicated(self):
        self.assertTrue(CASE.exists())
        self.assertIn("CASE_01_THE_TUESDAY_COMPLAINT.md", self.queue)
        self.assertFalse(CASE_TARGET.exists(), "EPISODE_01_FIRST_CASE.md would duplicate the case")
        self.assertFalse(LEDGER_TARGET.exists(), "the ledger is §6 of the canonical case")

    def test_author_drafts_are_empty_placeholders(self):
        for path in (LIFEPATH, FIRST_DAY):
            text = path.read_text(encoding="utf-8")
            self.assertIn("Tomi writes", text)
            self.assertIn("Agents must not", text)
            body = [line for line in text.splitlines()
                    if line.strip() and not line.startswith("#") and not line.startswith(">")
                    and not line.startswith("<!--")]
            self.assertEqual(body, [], f"{path.name} contains drafted prose")

    def test_queue_links_the_real_campaign_files(self):
        self.assertIn("docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md", self.queue)
        self.assertIn("docs/scenarios/CAMPAIGN_ROADMAP_1120.md", self.queue)
        self.assertIn("docs/proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md", self.queue)
        self.assertIn("docs/design/ROMPPAINEN_PARTY_1038.md", self.queue)
        self.assertIn("docs/campaign/DREAMS.md", self.queue)


if __name__ == "__main__":
    unittest.main()
