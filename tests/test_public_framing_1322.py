"""#1322: both landing pages say the same, current thing.

The acceptance criteria are about a reader, not about a diff: someone arriving at the README or the GitHub Pages site must
learn (a) why the three ontological shocks are being explored, (b) that the game is *Etsivä Romppainen ja Uusi
Paradigma*, (c) why the full RPG is paused, (d) how to run the prototype, and (e) which statements are established fact,
live research, contested claims and fiction.

The README was rewritten by the #1310/#1322 documentation work that landed on `main`; these tests pin that wording's
substance rather than any particular phrasing, and pin the Pages rewrite that did not exist there.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
INDEX = ROOT / "docs" / "index.html"
TIMELINE = ROOT / "docs" / "timeline.html"


def first_screen(path: Path, *, lines: int = 60) -> str:
    return "\n".join(path.read_text(encoding="utf-8").splitlines()[:lines])


class ReadmeFramingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = README.read_text(encoding="utf-8")
        self.head = first_screen(README)

    def test_the_title_is_the_first_line(self):
        self.assertEqual(self.text.splitlines()[0], "# NoöPunk: Etsivä Romppainen ja Uusi Paradigma")

    def test_it_says_plainly_that_this_is_not_a_full_rpg(self):
        self.assertIn("not a full RPG", self.head)

    def test_the_three_shocks_are_named_early(self):
        head = self.head.lower()
        for phrase in ("agi", "uap", "consciousness"):
            self.assertIn(phrase, head, phrase)

    def test_the_author_influences_are_named(self):
        for name in ("Vallée", "idealism", "quantum-information panpsychism"):
            self.assertIn(name, self.text, name)

    def test_the_personal_forecast_is_not_presented_as_consensus(self):
        self.assertIn("personal forecast", self.text)
        self.assertIn("not a claim of scientific consensus", self.text)

    def test_the_five_levels_are_distinguished(self):
        section = self.text.split("what is fiction", 1)[-1]
        for level in ("Established", "Live research", "Contested claims", "Fiction"):
            self.assertIn(level, section, level)
        self.assertIn("Telepathy Tapes", self.text)

    def test_the_rpg_pause_is_explained_with_its_reasons(self):
        self.assertIn("paused, not deleted", self.text)
        for reason in ("Noösphere", "Physical, Cyber and Astral"):
            self.assertIn(reason, self.text, reason)

    def test_the_crisis_has_not_happened(self):
        self.assertIn("has not happened yet", self.text)

    def test_both_prototype_commands_are_present_and_run(self):
        self.assertIn("python scripts/noopunk_case.py", self.text)
        self.assertIn("python3 NooPunk-Simulator/Code/adventure.py", self.text)
        self.assertTrue((ROOT / "scripts" / "noopunk_case.py").is_file())
        self.assertTrue((ROOT / "NooPunk-Simulator" / "Code" / "adventure.py").is_file())

    def test_development_material_is_labelled_development_material(self):
        self.assertIn("development material", self.text)

    def test_the_read_only_boundaries_are_stated(self):
        self.assertIn("NooPunk-Story/Story/", self.text)
        self.assertIn("NooPunk-Simulator/Paper/", self.text)
        self.assertIn("agents read-only", self.text)

    def test_the_old_rpg_is_pointed_at_as_historical(self):
        self.assertIn("NooPunk-RPG", self.text)
        self.assertIn("historical or optional work", self.text)


class PagesFramingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = INDEX.read_text(encoding="utf-8")

    def test_the_page_title_is_the_game(self):
        self.assertIn("<title>NoöPunk · Etsivä Romppainen ja Uusi Paradigma</title>", self.text)
        self.assertIn("ETSIVÄ ROMPPAINEN", self.text)

    def test_the_hero_says_what_it_is_and_is_not(self):
        hero = self.text.split("<main>", 1)[1].split("</section>", 1)[0]
        self.assertIn("interactive fiction", hero.lower())
        for denial in ("Not a tabletop RPG", "Not a computer RPG", "Not a simulation of a world"):
            self.assertIn(denial, hero, denial)

    def test_the_three_shocks_have_their_own_section(self):
        for marker in ('id="shocks"', "AGI/ASI", "UFO/UAP/NHI", "Consciousness/PSI"):
            self.assertIn(marker, self.text, marker)

    def test_the_motivation_names_the_author_influences_and_the_forecast(self):
        for name in ("Kastrup", "Hoffman", "Faggin", "Vallée", "Telepathy Tapes"):
            self.assertIn(name, self.text, name)
        self.assertIn("personal forecast", self.text)
        self.assertIn("not a scientific consensus", self.text)

    def test_the_four_categories_are_on_the_page(self):
        for status in ("Established", "Live research", "Contested claims", "NoöPunk fiction"):
            self.assertIn(status, self.text, status)

    def test_the_rpg_is_presented_as_paused_and_archived(self):
        self.assertIn("paused and preserved", self.text)
        self.assertIn("NooPunk-RPG", self.text)
        self.assertIn("not</em> the current roadmap", self.text)

    def test_the_play_commands_are_on_the_page(self):
        self.assertIn("python3 NooPunk-Simulator/Code/adventure.py", self.text)
        self.assertIn("python3 scripts/noopunk_case.py", self.text)

    def test_the_old_marketing_claims_are_gone(self):
        for stale in ("Humanity survived the NHI Crisis", "Concordia RPG / Simulation",
                      "POLITICAL SIMULATION + FACTION STRATEGY + CHARACTER RPG",
                      "Reality has changed. You are still expected at work."):
            self.assertNotIn(stale, self.text, stale)

    def test_the_timeline_page_is_labelled_historical(self):
        timeline = TIMELINE.read_text(encoding="utf-8")
        self.assertIn("HISTORICAL MATERIAL", timeline)

    def test_the_page_scales_its_own_hero_and_code_blocks(self):
        """The shared stylesheet sizes the hero for a two-word title; this one is a Finnish byline. The page carries its
        own scale, and keeps the two navigation links the shared stylesheet hides below 640px."""
        self.assertIn(".hero h1 {", self.text)
        self.assertIn("@media (max-width: 640px)", self.text)
        self.assertIn(".nav nav a:nth-child(1)", self.text)
        self.assertIn("pre code {", self.text)

    def test_every_local_link_and_anchor_resolves(self):
        anchors = set(re.findall(r'id="([^"]+)"', self.text))
        for href in re.findall(r'href="([^"]+)"', self.text):
            if href.startswith("#"):
                self.assertIn(href[1:], anchors, href)
            elif not href.startswith(("http", "mailto")):
                target = (ROOT / "docs" / href.split("#")[0]).resolve()
                self.assertTrue(target.exists(), href)

    def test_the_page_marks_html_balanced(self):
        import html.parser

        class Balance(html.parser.HTMLParser):
            void = {"meta", "link", "br", "img", "hr", "input", "source"}

            def __init__(self) -> None:
                super().__init__()
                self.stack: list[str] = []
                self.errors: list[str] = []

            def handle_starttag(self, tag, attrs):  # noqa: ANN001
                if tag not in self.void:
                    self.stack.append(tag)

            def handle_endtag(self, tag):  # noqa: ANN001
                if self.stack and self.stack[-1] == tag:
                    self.stack.pop()
                else:
                    self.errors.append(tag)

        parser = Balance()
        parser.feed(self.text)
        self.assertEqual(parser.errors, [])
        self.assertEqual(parser.stack, [])


class AuthorOwnershipTests(unittest.TestCase):
    def test_the_pages_state_the_read_only_boundary(self):
        for path in (README, INDEX):
            text = path.read_text(encoding="utf-8")
            self.assertIn("NooPunk-Story/Story/", text, path.name)
            self.assertIn("NooPunk-Simulator/Paper/", text, path.name)

    def test_the_prompt_archive_holds_this_request(self):
        entry = ROOT / "Prompts" / "08_11_2026_ROMPPAINEN_PUBLIC_REFRAME.md"
        self.assertTrue(entry.is_file())
        self.assertIn("1322", entry.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
