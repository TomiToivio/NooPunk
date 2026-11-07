"""#1310: the pivot is documented where a newcomer looks first, and the promised playable case actually runs.

Three claims the issue makes are checkable, and each would be easy to break later:

* a new contributor must understand immediately that the game is Romppainen's detective interactive fiction, **not** a
  full RPG;
* the paused RPG and the author-owned directories must stay declared read-only in the instructions an agent reads;
* at least one detective case must be **playable end to end** with no RPG dependency — so this test plays one.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIVOT = ROOT / "docs" / "adventure" / "PIVOT_1310.md"
AGENTS = ROOT / "AGENTS.md"
README = ROOT / "README.md"


class DocumentationTests(unittest.TestCase):
    def test_the_pivot_page_exists_and_says_what_the_game_is(self):
        text = PIVOT.read_text(encoding="utf-8")
        for phrase in ("Etsivä Harri Romppainen", "interactive-fiction", "paused"):
            self.assertIn(phrase, text, phrase)

    def test_the_readme_leads_with_the_pivot(self):
        text = README.read_text(encoding="utf-8")
        head = "\n".join(text.splitlines()[:12])
        self.assertIn("#1310", head, "the pivot must be on the first screen, not buried")
        self.assertIn("PIVOT_1310.md", head)

    def test_agents_names_the_pivot_before_the_older_directive(self):
        text = AGENTS.read_text(encoding="utf-8")
        pivot_at = text.find("#1310")
        self.assertGreater(pivot_at, -1, "AGENTS.md must carry the pivot")
        simulator_at = text.find("LACLAUGPT SOCIAL SCIENCE SIMULATOR ONLY")
        self.assertGreater(simulator_at, pivot_at, "the older directive must come after the pivot")

    def test_agents_declares_the_three_untouchable_paths(self):
        text = AGENTS.read_text(encoding="utf-8")
        for path in ("NooPunk-RPG/", "NooPunk-Story/Story/", "NooPunk-Simulator/Paper/"):
            self.assertIn(path, text, path)

    def test_the_rpg_readme_is_left_alone_by_this_pivot(self):
        """The guard is that the paused track keeps its own text; if this page ever needs editing, that is a decision."""
        text = (ROOT / "NooPunk-RPG" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("#1310", text, "the pivot must not rewrite the paused RPG's own README")

    def test_the_prompt_archive_holds_the_pivot_request(self):
        entry = ROOT / "Prompts" / "07_11_2026_ROMPPAINEN_DETECTIVE_PIVOT.md"
        self.assertTrue(entry.is_file(), "a substantial author decision must be archived")
        self.assertIn("1310", entry.read_text(encoding="utf-8"))


class PlayableCaseTests(unittest.TestCase):
    """The acceptance criterion that matters: a case you can actually play, without the RPG."""

    def test_the_shipped_case_runs_from_a_script_and_yields_clues(self):
        beats = ["look", "clues", "quit"]
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "noopunk_case.py"), "--script", "/dev/stdin"],
            input="\n".join(beats) + "\n", capture_output=True, text=True, cwd=ROOT,
            env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"},
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr[-800:])
        self.assertIn("Entrance", completed.stdout)
        self.assertIn("[", completed.stdout, "a clue or a lead should be printed by `look`")

    def test_the_console_does_not_import_the_rpg_rules(self):
        source = (ROOT / "src" / "console" / "play.py").read_text(encoding="utf-8")
        for forbidden in ("cwn_combat", "cwn_character", "cwn_spells", "character_generation"):
            self.assertNotIn(forbidden, source, forbidden)


if __name__ == "__main__":
    unittest.main()
