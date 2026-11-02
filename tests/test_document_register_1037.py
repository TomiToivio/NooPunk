"""In-world documents give register 3 a mechanism without inventing a word (#1037).

The brainstorm asks for a documentary / Situationist collage layer: memos, dossiers, forms,
transcripts. A document here is a **view of canon already in play** — the case file prints the
clues the investigator actually collected and leaves the rest as blank form lines, the activity
log prints the consequences the engine actually recorded. If this file ever needs a fact that is
not already in `content.CLUES` or `state.consequences`, that is an authoring decision and belongs
in the issue, not in this test.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))

from nopunk_mud.campaign import CampaignEngine  # noqa: E402
from nopunk_mud.campaign import content  # noqa: E402


class DocumentRegister(unittest.TestCase):
    def test_read_without_an_argument_lists_the_register(self):
        engine = CampaignEngine()
        text = engine.command("read")
        for name in content.document_names():
            self.assertIn(name, text)
        self.assertIn("read case_file", text)

    def test_a_document_you_do_not_carry_is_refused_with_a_reason(self):
        engine = CampaignEngine()
        text = engine.command("read case_file")
        self.assertIn("not carrying a case file", text)
        self.assertIn("university", text)
        self.assertTrue(engine.state.turns >= 1)

    def test_the_case_file_prints_collected_clues_and_blank_forms_for_the_rest(self):
        engine = CampaignEngine()
        engine.command("go street")
        engine.command("go university")
        engine.command("examine terminal")
        engine.command("take folder")
        text = engine.command("read case_file")
        self.assertIn("DOSSIER", text)
        self.assertIn(content.CLUES["access_log"]["text"], text)
        self.assertIn("[ ]", text)
        self.assertIn("not in the file", text)
        self.assertIn(content.DOCUMENTS["case_file"]["footer"], text)

    def test_the_document_adds_no_text_of_its_own(self):
        """Every body line is either a canon clue text or the blank-form marker."""
        engine = CampaignEngine()
        engine.command("go street")
        engine.command("go university")
        engine.command("examine terminal")
        engine.command("take folder")
        body = engine._document_body(content.DOCUMENTS["case_file"])
        for line in body:
            if line.startswith("[x]"):
                self.assertTrue(any(clue["text"] in line for clue in content.CLUES.values()), line)
            else:
                self.assertTrue(line.startswith("[ ]") and line.endswith("not in the file"), line)

    def test_the_activity_log_prints_recorded_consequences(self):
        engine = CampaignEngine()
        self.assertIn("Nothing has been logged", engine.command("read activity_log"))
        # One clue is not enough to file the case, which the engine records as a consequence.
        engine.command("go street")
        engine.command("go university")
        engine.command("examine terminal")
        engine.command("go street")
        engine.command("go safehouse")
        engine.command("report")
        text = engine.command("read activity_log")
        self.assertIn("insufficient_evidence", text)
        self.assertIn("no countersignature", text)

    def test_an_unknown_document_is_refused_with_a_reason(self):
        engine = CampaignEngine()
        before = engine.state.turns
        text = engine.command("read shopping list")
        self.assertIn("no document called shopping list", text)
        self.assertEqual(engine.state.turns, before + 1)

    def test_help_advertises_read(self):
        self.assertIn("read", CampaignEngine().command("help"))

    def test_every_document_declares_the_fields_the_renderer_needs(self):
        required = {"title", "kind", "issuer", "label", "requires_flag", "empty", "footer", "source"}
        for name in content.document_names():
            doc = content.DOCUMENTS[name]
            self.assertTrue(required <= set(doc), f"{name} is missing {required - set(doc)}")
            self.assertIn(doc["source"], {"clues", "consequences"})


if __name__ == "__main__":
    unittest.main()
