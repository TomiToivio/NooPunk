"""Guards for the author prompt archive policy (#1302)."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "Prompts"
README = PROMPTS / "README.md"
FIRST = PROMPTS / "07_11_2026_PROMPT_LOGGING.md"


class PromptArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        cls.readme = README.read_text(encoding="utf-8")
        cls.first = FIRST.read_text(encoding="utf-8")

    def test_agents_has_a_discoverable_prompt_archive_policy(self):
        self.assertIn("Author prompt archive (#1302)", self.agents)
        self.assertIn("Prompts/README.md", self.agents)
        self.assertIn("selective author-prompt archiving", self.agents)
        self.assertIn("Do not log", self.agents)

    def test_readme_is_the_canonical_compact_policy(self):
        for term in (
            "substantial original NoöPunk design and development prompts",
            "What qualifies",
            "What does not qualify",
            "DD_MM_YYYY_TOPIC_NAME.md",
            "Duplicate and normalization rules",
            "privacy",
            "not approved canon",
            "does not authorize",
        ):
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.readme.lower())

    def test_first_prompt_is_archived_verbatim_with_metadata(self):
        self.assertTrue(FIRST.is_file())
        self.assertIn("**Date:** 2026-11-07", self.first)
        self.assertIn("**Topic:** Prompt logging", self.first)
        self.assertIn("**Issue:** [#1302]", self.first)
        self.assertIn("## Original prompt (verbatim text", self.first)
        self.assertIn("I waste a lot of background material", self.first)
        self.assertIn("Save my prompts in directory Prompts", self.first)
        self.assertIn("Do this only when my prompt is clearly related", self.first)

    def test_short_requests_are_explicitly_exempt(self):
        self.assertIn('"do this"', self.readme)
        self.assertIn('"fix this"', self.readme)
        self.assertIn("status questions", self.readme)

    def test_filenames_follow_the_date_topic_convention(self):
        pattern = re.compile(r"^\d{2}_\d{2}_\d{4}_[A-Z0-9_]+\.md$")
        for path in PROMPTS.glob("*.md"):
            if path.name == "README.md":
                continue
            with self.subTest(path=path.name):
                self.assertRegex(path.name, pattern)

    def test_no_duplicate_prompt_bodies(self):
        bodies = {}
        for path in PROMPTS.glob("*.md"):
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            marker = "## Original prompt"
            body = text.split(marker, 1)[1] if marker in text else text
            digest = hashlib.sha256(" ".join(body.split()).encode("utf-8")).hexdigest()
            self.assertNotIn(digest, bodies, f"{path.name} duplicates {bodies.get(digest)}")
            bodies[digest] = path.name

    def test_archive_is_documentation_only(self):
        self.assertIn("documentation only", self.readme.lower())
        self.assertIn("does not authorize new rpg, story or simulator feature development", self.readme.lower())


if __name__ == "__main__":
    unittest.main()
