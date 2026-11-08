"""Public-facing introduction checks for #1322."""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PAGE = ROOT / "docs" / "index.html"
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"


class _PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.hrefs = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        for key, value in attrs:
            if key == "href" and value:
                self.hrefs.append(value)

    def handle_data(self, data):
        self.text.append(data)


class PublicIntroductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README.read_text(encoding="utf-8")
        cls.page = PAGE.read_text(encoding="utf-8")
        cls.parser = _PageParser()
        cls.parser.feed(cls.page)
        cls.page_text = " ".join(" ".join(cls.parser.text).split())

    def test_readme_has_the_new_title_and_scope(self):
        self.assertTrue(self.readme.startswith("# NoöPunk: Etsivä Romppainen ja Uusi Paradigma"))
        for phrase in ("detective interactive-fiction", "not a full role-playing game", "Helsinki, 2045"):
            self.assertIn(phrase, self.readme)

    def test_readme_explains_the_three_shifts_and_motivation(self):
        for phrase in (
            "quantum-information panpsychism",
            "AGI / ASI",
            "UFO / UAP / NHI",
            "Jacques Vallée",
            "Bernardo Kastrup",
            "Donald Hoffman",
            "Federico Faggin",
            "Telepathy Tapes",
            "personal forecast",
            "not a claim of scientific consensus",
            "LaclauGPT",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.readme)

    def test_readme_explains_the_paused_rpg_and_preserves_the_archive(self):
        for phrase in (
            "almost absurd in scope",
            "noopunk-rpg",
            "paused archive",
            "not a full role-playing game",
            "cross-plane rules",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.readme.lower())
        self.assertIn("NooPunk-RPG/README.md", self.readme)

    def test_readme_has_the_play_story_and_archive_navigation(self):
        for phrase in (
            "Play the prototype",
            "Read the story",
            "Historical RPG archive",
            "NooPunk-Simulator/Code/adventure.py",
            "docs/adventure/PIVOT_1310.md",
            "CAMPAIGN_01_EUROPOL_ROOKIE.md",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.readme)

    def test_readme_has_no_old_primary_game_or_post_crisis_claim(self):
        for stale in (
            "Primary game (#950)",
            "The game is apocalyptic cyberpunk science fiction",
            "Humanity survived the NHI Crisis",
            "CWN-first rules foundation",
            "full computer RPG and social simulation",
        ):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, self.readme)

    def test_readme_local_links_resolve(self):
        for target in re.findall(r"\]\(([^)#]+)\)", self.readme):
            if "://" in target or target.startswith("#"):
                continue
            with self.subTest(target=target):
                self.assertTrue((ROOT / target).resolve().exists(), target)

    def test_page_has_title_and_public_sections(self):
        self.assertIn("<title>NoöPunk · Etsivä Romppainen ja Uusi Paradigma</title>", self.page)
        self.assertIn("DETECTIVE INTERACTIVE FICTION", self.page)
        for phrase in ("Why NoöPunk exists", "Three challenges", "The small adventure", "paused", "Play the prototype"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.page_text.lower())

    def test_page_explains_the_shifts_without_overclaiming(self):
        for phrase in ("AGI", "NHI", "PSI", "Kastrup", "Vallée", "personal forecast", "not a consensus"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.page.lower())

    def test_page_has_working_navigation_and_no_old_claims(self):
        for href in self.parser.hrefs:
            if href.startswith("#"):
                self.assertIn('id="' + href[1:] + '"', self.page)
        for stale in ("Humanity survived the NHI Crisis", "CWN / SWN first", "Godot RPG", "Primary game"):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, self.page)

    def test_pages_publishes_the_docs_directory(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("path: docs", workflow)
        self.assertIn("actions/deploy-pages", workflow)


if __name__ == "__main__":
    unittest.main()
