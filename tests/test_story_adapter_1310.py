"""Tests for the #1310 author-story-to-case adapter."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "NooPunk-Simulator" / "Code" / "story_adapter.py"
ADVENTURE_PATH = ROOT / "NooPunk-Simulator" / "Code" / "adventure.py"
FIXTURE = (
    ROOT / "NooPunk-Simulator" / "Graphs" / "fixtures" / "story_source_development.md"
)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StoryAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = _load("story_adapter_1310", ADAPTER_PATH)
        cls.adventure = _load("adventure_1310_story", ADVENTURE_PATH)

    def test_parses_author_fixture_and_preserves_prose(self):
        case = self.adapter.parse_story(FIXTURE)
        self.assertEqual(case["id"], "story_fixture_01")
        self.assertEqual(case["title"], "The Quiet Petition")
        self.assertEqual(case["start"], "briefing")
        self.assertEqual(case["source"]["kind"], "author_story")
        self.assertFalse(case["source"]["canon"])
        self.assertFalse(case["source"]["author_reviewed"])
        self.assertIn("not Tomi's manuscript", case["scenes"]["briefing"]["text"])
        self.assertEqual(len(case["scenes"]), 7)
        self.assertEqual(
            case["scenes"]["decision"]["choices"][0]["to"], "ending_private"
        )

    def test_generated_case_is_playable_by_the_adventure_runner(self):
        case = self.adapter.parse_story(FIXTURE)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            path.write_text(json.dumps(case), encoding="utf-8")
            loaded = self.adventure.load_case(path)
            game = self.adventure.Adventure(loaded)
            self.assertIn("Europol briefing", game.scene["title"])
            game.choose(1)
            game.choose(1)
            game.choose(1)
            game.choose(1)
            self.assertEqual(game.state["scene"], "decision")
            game.choose(2)
            self.assertEqual(game.state["scene"], "ending_review")
            self.assertTrue(game.state["finished"])
            self.assertIn("event register", game.notebook())

    def test_optional_contradictions_section_is_parsed(self):
        """Contradictory testimony is something the author writes, not something an agent hand-edits."""
        case = self.adapter.parse_story(FIXTURE)
        self.assertEqual(len(case["contradictions"]), 1)
        contradiction = case["contradictions"][0]
        self.assertEqual(contradiction["between"], ["roster", "witness"])
        self.assertIn("only one present", contradiction["text"])

    def test_a_contradiction_between_unknown_clues_is_rejected(self):
        text = FIXTURE.read_text(encoding="utf-8").replace(
            "- roster + witness:", "- roster + ghost:"
        )
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "broken.md"
            source.write_text(text, encoding="utf-8")
            with self.assertRaises(self.adapter.StoryFormatError):
                self.adapter.parse_story(source)

    def test_a_contradiction_needs_two_clues(self):
        text = FIXTURE.read_text(encoding="utf-8").replace(
            "- roster + witness:", "- roster:"
        )
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "broken.md"
            source.write_text(text, encoding="utf-8")
            with self.assertRaises(self.adapter.StoryFormatError):
                self.adapter.parse_story(source)

    def test_an_unknown_section_is_still_rejected(self):
        text = FIXTURE.read_text(encoding="utf-8").replace(
            "## Contradictions", "## Speculations"
        )
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "broken.md"
            source.write_text(text, encoding="utf-8")
            with self.assertRaises(self.adapter.StoryFormatError):
                self.adapter.parse_story(source)

    def test_semicolon_separated_attributes_are_accepted(self):
        text = FIXTURE.read_text(encoding="utf-8").replace(
            "](records) adds=missing,roster",
            "](records) adds=missing,roster; requires=missing",
        )
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "choice.md"
            source.write_text(text, encoding="utf-8")
            case = self.adapter.parse_story(source)
        self.assertEqual(
            case["scenes"]["briefing"]["choices"][0]["requires"], ["missing"]
        )

    def test_missing_choice_target_is_rejected(self):
        text = FIXTURE.read_text(encoding="utf-8").replace(
            "](records)", "](missing_scene)"
        )
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "broken.md"
            source.write_text(text, encoding="utf-8")
            with self.assertRaises(self.adapter.StoryFormatError):
                self.adapter.parse_story(source)

    def test_unknown_clue_is_rejected(self):
        text = FIXTURE.read_text(encoding="utf-8").replace(
            "adds=missing,roster", "adds=missing,unknown"
        )
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "broken.md"
            source.write_text(text, encoding="utf-8")
            with self.assertRaises(self.adapter.StoryFormatError):
                self.adapter.parse_story(source)

    def test_missing_header_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "broken.md"
            source.write_text("id: x\nstart: y\n", encoding="utf-8")
            with self.assertRaises(self.adapter.StoryFormatError):
                self.adapter.parse_story(source)

    def test_source_hash_and_path_survive(self):
        case = self.adapter.parse_story(FIXTURE)
        self.assertEqual(
            case["source"]["source_sha256"],
            self.adapter.hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        )
        self.assertEqual(case["source"]["story_manuscript"], str(FIXTURE))

    def test_adapter_does_not_import_rpg_or_write_story(self):
        source = ADAPTER_PATH.read_text(encoding="utf-8")
        for forbidden in ("src.rules", "src.console", "NooPunk-RPG", "evennia", "cwn"):
            self.assertNotIn(forbidden, source)
        self.assertIn("NooPunk-Story/Story", source)
        self.assertIn("never writes", source)


if __name__ == "__main__":
    unittest.main()
