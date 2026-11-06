"""Every queue entry points at a real file, and every author draft is a template, not prose (#1216).

The queue says it is a status index. That is only true if its paths resolve. The author drafts say Tomi
writes them. That is only true if what an agent left behind is structure — headings and prompts — rather
than a first draft someone will be tempted to keep.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "docs" / "design" / "AUTHOR_WRITING_QUEUE_1216.md"
APPROVALS = ROOT / "docs" / "design" / "AUTHOR_APPROVALS_1216.md"

TEMPLATES = [
    ROOT / "docs" / "campaign" / "TONY_GERMAN_LIFEPATH.md",
    ROOT / "docs" / "campaign" / "EPISODE_00_FIRST_DAY.md",
    ROOT / "docs" / "campaign" / "PLAYER_BRIEFING.md",
]

PATH_RE = re.compile(r"`((?:docs|design|rulebook|data)/[A-Za-z0-9_./-]+\.(?:md|json))`")


def body_lines(text: str):
    """Lines that are neither headings, blockquote prompts, HTML comments, nor blank."""
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("<!--"):
            continue
        yield s


class QueuePathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = QUEUE.read_text(encoding="utf-8")
        cls.paths = sorted(set(PATH_RE.findall(cls.queue)))
        # A COVERED row names the path it deliberately does NOT create, so its absence is the point.
        cls.required, cls.refused = [], []
        for line in cls.queue.splitlines():
            if not line.startswith("| "):
                continue
            found = PATH_RE.findall(line)
            if not found:
                continue
            if "**COVERED**" in line:
                cls.refused.extend(found)
            else:
                cls.required.extend(found)
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


class TemplateTests(unittest.TestCase):
    def test_each_template_is_structure_without_prose(self):
        for path in TEMPLATES:
            text = path.read_text(encoding="utf-8")
            self.assertIn("Tomi writes", text, path.name)
            self.assertIn("Agents must not", text, path.name)
            self.assertIn("<!-- Tomi writes below. -->", text, path.name)
            extra = list(body_lines(text))
            self.assertEqual(extra, [], f"{path.name} contains drafted prose: {extra[:3]}")

    def test_each_template_prompts_every_section(self):
        for path in TEMPLATES:
            lines = path.read_text(encoding="utf-8").splitlines()
            sections = [i for i, line in enumerate(lines) if line.startswith("## ")]
            self.assertGreaterEqual(len(sections), 8, f"{path.name} has too few sections to write in")
            for i, start in enumerate(sections):
                end = sections[i + 1] if i + 1 < len(sections) else len(lines)
                block = lines[start:end]
                self.assertTrue(any(line.strip().startswith(">") for line in block),
                                f"{path.name}: section {lines[start]!r} has no prompt")

    def test_lifepath_covers_the_required_vignette_range(self):
        text = (ROOT / "docs" / "campaign" / "TONY_GERMAN_LIFEPATH.md").read_text(encoding="utf-8")
        for topic in ("Acceleration", "NHI Crisis", "Loviisa", "Hyvinkää", "Disclosure",
                      "Academy", "Graduation", "branch map", "Fixed anchors"):
            self.assertIn(topic, text, f"lifepath template lost the {topic} beat")

    def test_first_day_covers_the_required_beats(self):
        text = (ROOT / "docs" / "campaign" / "EPISODE_00_FIRST_DAY.md").read_text(encoding="utf-8")
        for topic in ("nightmare", "Sörnäinen", "uniform", "equipment", "Dispatch",
                      "Adlerwerke", "Ratakatu", "Romppainen"):
            self.assertIn(topic, text, f"first-day template lost the {topic} beat")


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
