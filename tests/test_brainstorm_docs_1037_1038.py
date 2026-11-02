"""#1037 and #1038 are creative direction, and a future agent must not mistake them for a spec.

The failure this guards against is quiet: someone reads the brainstorm as a work order, "unlocks" the CWN core
while chasing a nice idea, or writes Romppainen as a grimdark intelligence chief because the file mentioned
intelligence. The source text forbids all three in plain words. If those words ever disappear from the
repository copy, the guard should fail rather than the architecture quietly changing.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_1037 = ROOT / "docs/design/BRAINSTORM_1037_FICTION_PLAY.md"
DOC_1038 = ROOT / "docs/design/BRAINSTORM_1038_ROMPPAINEN_PARTY.md"


class BrainstormStatusTest(unittest.TestCase):
    def test_both_brainstorm_documents_exist(self):
        for path in (DOC_1037, DOC_1038):
            self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")

    def test_both_are_marked_exploratory(self):
        for path in (DOC_1037, DOC_1038):
            text = path.read_text(encoding="utf-8")
            self.assertIn("STATUS: EXPLORATORY", text, f"{path.name} lost its status line")

    def test_1037_keeps_the_architecture_guard(self):
        text = DOC_1037.read_text(encoding="utf-8")
        # The source bolds "not", so assert on the words without the markdown asterisks.
        self.assertIn("authorization to replace the Evennia-first", text)
        self.assertIn("unlock the CWN rules core", text)
        self.assertIn("Finnish fiction is Tomi", text)

    def test_1038_keeps_the_character_guards(self):
        text = DOC_1038.read_text(encoding="utf-8")
        self.assertIn("NOT the default player character", text)
        self.assertIn("Do not pre-decide his final allegiance", text)

    def test_neither_document_is_treated_as_a_locked_specification(self):
        for path in (DOC_1037, DOC_1038):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("STATUS: LOCKED", text)
            self.assertNotIn("locked specification: this file", text.lower())


if __name__ == "__main__":
    unittest.main()
