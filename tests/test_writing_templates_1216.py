"""Every queue entry points at a real file, and no author worksheet contains drafted prose (#1216).

The queue says it is a status index. That is only true if its paths resolve. An author worksheet says Tomi
writes it. That is only true if what an agent left behind is structure — headings, prompts, tables and
placeholders — rather than a first draft somebody will be tempted to keep.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "docs" / "design" / "AUTHOR_WRITING_QUEUE_1216.md"
APPROVALS = ROOT / "docs" / "design" / "AUTHOR_APPROVALS_1216.md"

WORKSHEETS = [
    ROOT / "docs" / "campaign" / "TONY_GERMAN_LIFEPATH.md",
    ROOT / "docs" / "campaign" / "EPISODE_00_FIRST_DAY.md",
    ROOT / "docs" / "campaign" / "PLAYER_BRIEFING.md",
]

PATH_RE = re.compile(r"`((?:docs|design|rulebook|data)/[A-Za-z0-9_./-]+\.(?:md|json))`")
# A "filled in" answer is what an agent must never leave behind; these tokens mean "the author writes here".
PLACEHOLDER_RE = re.compile(
    r"\[fill|\[AUTHOR|\[write here\]|\[choose|\[verify|\[confirm|\[pending|\[TBD|\[insert|\[your", re.I)


def body_lines(text: str):
    """Lines that are neither headings, blockquotes, comments, tables, checklists, nor blank."""
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("<!--"):
            continue
        if s.startswith("|") or s.startswith("- [") or s.startswith("- "):
            continue
        if s in {"---", "***"}:
            continue
        yield s


class QueuePathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = QUEUE.read_text(encoding="utf-8")
        cls.paths = sorted(set(PATH_RE.findall(cls.queue)))
        cls.required = []
        for line in cls.queue.splitlines():
            if line.startswith("| ") and PATH_RE.findall(line) and "**COVERED**" not in line:
                cls.required.extend(PATH_RE.findall(line))
        cls.required = sorted(set(cls.required))

    def test_the_queue_names_documents_at_all(self):
        self.assertGreaterEqual(len(self.paths), 12, self.paths)

    def test_every_required_path_exists(self):
        missing = [p for p in self.required if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"queue points at files that do not exist: {missing}")

    def test_the_queue_keeps_its_no_duplicate_rows(self):
        """COVERED rows are how the index stops a second copy of a case or a memo being written."""
        self.assertGreaterEqual(self.queue.count("**COVERED**"), 3)

    def test_the_two_new_documents_are_in_the_queue(self):
        for path in ("docs/campaign/PLAYER_BRIEFING.md", "docs/design/AUTHOR_APPROVALS_1216.md"):
            self.assertIn(path, self.paths)


class WorksheetTests(unittest.TestCase):
    def test_each_worksheet_declares_the_author_and_keeps_slots(self):
        for path in WORKSHEETS:
            text = path.read_text(encoding="utf-8")
            self.assertTrue("Tomi writes" in text or "Tomi supplies" in text, path.name)
            self.assertGreaterEqual(len(PLACEHOLDER_RE.findall(text)), 5,
                                    f"{path.name} has no writing slots left for the author")

    def test_the_briefing_contains_no_drafted_prose(self):
        """The newest file is held to the strict rule: headings, prompts and comments only."""
        text = (ROOT / "docs" / "campaign" / "PLAYER_BRIEFING.md").read_text(encoding="utf-8")
        prose = [line for line in body_lines(text) if not PLACEHOLDER_RE.search(line)]
        self.assertEqual(prose, [], f"PLAYER_BRIEFING.md contains drafted prose: {prose[:3]}")

    def test_each_worksheet_prompts_every_section(self):
        for path in WORKSHEETS:
            text = path.read_text(encoding="utf-8")
            sections = [line for line in text.splitlines() if line.startswith("## ")]
            self.assertGreaterEqual(len(sections), 5, f"{path.name} has too few sections to write in")
            for start in sections:
                i = text.index(start)
                block = text[i:i + 2500]
                self.assertTrue(PLACEHOLDER_RE.search(block) or "\n>" in block,
                                f"{path.name}: section {start!r} has no prompt")

    def test_lifepath_covers_the_required_vignette_range(self):
        text = (ROOT / "docs" / "campaign" / "TONY_GERMAN_LIFEPATH.md").read_text(encoding="utf-8")
        for topic in ("Helsinki", "Crisis", "Loviisa", "Hyvinkää", "Disclosure",
                      "Academy", "Branch outcome", "Character constants"):
            self.assertIn(topic, text, f"lifepath worksheet lost the {topic} beat")

    def test_first_day_covers_the_required_beats(self):
        text = (ROOT / "docs" / "campaign" / "EPISODE_00_FIRST_DAY.md").read_text(encoding="utf-8")
        for topic in ("Nightmare", "Sörnäinen", "Equipment", "Ratakatu", "Romppainen"):
            self.assertIn(topic, text, f"first-day worksheet lost the {topic} beat")

    def test_the_briefing_states_what_it_must_not_contain(self):
        text = (ROOT / "docs" / "campaign" / "PLAYER_BRIEFING.md").read_text(encoding="utf-8")
        self.assertIn("must not contain", text)
        self.assertIn("encyclopedia", text)


class ApprovalLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = APPROVALS.read_text(encoding="utf-8")

    def test_it_records_decisions_not_canon(self):
        for mark in ("AWAITING", "APPROVED", "CHANGES", "BLOCKED"):
            self.assertIn(mark, self.text)
        self.assertIn("adds no fiction", self.text)

    def test_every_open_document_has_a_row(self):
        queue = QUEUE.read_text(encoding="utf-8")
        for name in ("CAMPAIGN_01_EUROPOL_ROOKIE.md", "CASE_01_THE_TUESDAY_COMPLAINT.md",
                     "TONY_GERMAN_LIFEPATH.md", "EPISODE_00_FIRST_DAY.md", "PLAYER_BRIEFING.md",
                     "ROMPPAINEN_PARTY_1038.md", "GREATER_HELSINKI_2045.md", "GALACTIC_MACHINE_WAR.md",
                     "DREAMS.md"):
            self.assertIn(name, self.text, f"approvals ledger has no row for {name}")
            self.assertIn(name, queue, f"queue does not mention {name}")


if __name__ == "__main__":
    unittest.main()
