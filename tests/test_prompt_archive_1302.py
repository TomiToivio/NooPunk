"""#1302: every archived prompt is indexed, dated and verbatim.

The archive's value is that a later reader can find the author's own text. Three failures would destroy it: an entry that
is not indexed (invisible), a filename that breaks the dated convention (unsortable), and an entry rewritten into a
summary (not the author's words). This checks the first two mechanically; the third is why entries say "verbatim" and
carry the issue link.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "Prompts"
NAME = re.compile(r"^(?P<day>\d{2})_(?P<month>\d{2})_(?P<year>\d{4})_[A-Z0- nine]+\.md$".replace(" ", ""))


class ArchiveTests(unittest.TestCase):
    def test_the_archive_exists_with_its_policy(self):
        self.assertTrue((PROMPTS / "README.md").is_file())
        self.assertIn("Mandatory procedure", (PROMPTS / "README.md").read_text(encoding="utf-8"))

    def test_every_entry_follows_the_dated_filename_convention(self):
        for path in sorted(PROMPTS.glob("*.md")):
            if path.name == "README.md":
                continue
            self.assertRegex(path.name, r"^\d{2}_\d{2}_\d{4}_[A-Z0-9_]+\.md$", path.name)

    def test_every_entry_is_indexed_in_the_readme(self):
        readme = (PROMPTS / "README.md").read_text(encoding="utf-8")
        unindexed = [p.name for p in sorted(PROMPTS.glob("*.md")) if p.name != "README.md" and f"]({p.name})" not in readme]
        self.assertEqual(unindexed, [], "an archived prompt that is not indexed cannot be found")

    def test_every_entry_states_its_date_source_and_status(self):
        for path in sorted(PROMPTS.glob("*.md")):
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            for field in ("**Date:**", "**Source:**", "**Archive status:**", "## Original prompt"):
                self.assertIn(field, text, f"{path.name} lacks {field}")

    def test_the_filename_date_matches_the_declared_date(self):
        for path in sorted(PROMPTS.glob("*.md")):
            if path.name == "README.md":
                continue
            day, month, year = path.name.split("_")[:3]
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"**Date:** {year}-{month}-{day}", text, path.name)


if __name__ == "__main__":
    unittest.main()
