"""#1295: the three-subproject skeleton, the Story boundary, and the shared contract.

These tests exist because the pivot's central promise is a **negative** one: nothing an agent does may
touch Tomi's manuscript. A rule that is only written in prose is a rule that gets edited away during a
refactor. Each guard below fails when the promise is weakened, not when it is honoured.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SUBPROJECTS = {
    "NooPunk-Story": ["README.md", "Story/README.md", "Graph/README.md"],
    "NooPunk-Simulator": ["README.md"],
    "NooPunk-RPG": ["README.md"],
}

#: Directories that P0 must map before anything is moved. If one appears and is not in the map, the
#: migration has started without a plan; if one disappears, the map is stale.
INVENTORIED = ("src", "tests", "docs", "data", "design", "rulebook", "mud", "campaign",
               "strategy_game", "godot", "mods", "portable_noopunk", "scripts", "tools")


class LayoutTests(unittest.TestCase):
    def test_the_three_subprojects_exist_with_their_readmes(self):
        for project, files in SUBPROJECTS.items():
            for name in files:
                path = ROOT / project / name
                self.assertTrue(path.is_file(), f"missing {project}/{name}")

    def test_story_keeps_the_two_directories_apart(self):
        self.assertTrue((ROOT / "NooPunk-Story/Story").is_dir())
        self.assertTrue((ROOT / "NooPunk-Story/Graph").is_dir())


class StoryBoundaryTests(unittest.TestCase):
    def test_the_story_readme_says_human_only(self):
        text = (ROOT / "NooPunk-Story/Story/README.md").read_text(encoding="utf-8")
        self.assertIn("READ ONLY", text)
        self.assertIn("No writing, rewriting", text)

    def test_agents_md_carries_the_hard_rule(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("NooPunk-Story/Story/", text)
        self.assertIn("must NEVER write", text)
        self.assertIn("human-only", text.lower())

    def test_codeowners_protects_the_manuscript(self):
        text = (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^/NooPunk-Story/Story/\*\*?\s+@")

    def test_no_executable_or_generated_content_lives_in_story(self):
        allowed = {".md", ".txt", ""}
        for path in (ROOT / "NooPunk-Story/Story").rglob("*"):
            if path.is_dir():
                continue
            self.assertIn(path.suffix, allowed,
                          f"generated or executable file inside the manuscript: {path}")

    def test_the_graph_readme_states_the_direction_of_truth(self):
        text = (ROOT / "NooPunk-Story/Graph/README.md").read_text(encoding="utf-8")
        self.assertIn("never edits the manuscript", text)
        self.assertIn("review note", text)


class ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = (ROOT / "docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md").read_text(
            encoding="utf-8")

    def test_the_contract_is_versioned(self):
        self.assertIn("version 1", self.text)
        self.assertIn("`format` and `version` are **required**", self.text)

    def test_the_four_graph_families_are_the_contract(self):
        for family in ("Physical", "Cyber", "Social", "Story"):
            self.assertIn(family, self.text, family)
        self.assertIn("An **Astral** family does not exist", self.text)

    def test_the_four_tag_families_are_the_contract(self):
        for family in ("SocialTag", "GoalTag", "ClueTag", "PersonalityTag"):
            self.assertIn(family, self.text, family)

    def test_the_contract_keeps_the_direction_of_travel(self):
        self.assertIn("Tomi's Story  →  Story Graph  →  RPG narrative", self.text)

    def test_the_contract_declares_what_it_does_not_own(self):
        self.assertIn("character sheets (CWN owns them)", self.text)


class MigrationMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = (ROOT / "docs/architecture/PIVOT_1295_MIGRATION_MAP.md").read_text(
            encoding="utf-8")

    def test_the_map_says_nothing_has_been_moved(self):
        self.assertIn("Nothing has been moved", self.text)

    def test_the_map_inventories_the_existing_tree(self):
        missing = [name for name in INVENTORIED if f"`{name}/`" not in self.text]
        self.assertFalse(missing, f"unmapped directories: {missing}")

    def test_the_map_states_the_simulator_does_not_exist_yet(self):
        self.assertIn("no Simulator code exists in this repository", self.text)

    def test_the_map_names_the_hard_prohibitions(self):
        for phrase in ("No agent writes inside `NooPunk-Story/Story/`", "No change to CWN",
                       "No big-bang move"):
            self.assertIn(phrase, self.text)

    def test_the_map_admits_what_the_guards_cannot_do(self):
        flat = " ".join(self.text.split())
        self.assertIn("no git-level check can prove who typed a line", flat)


class RpgBoundaryTests(unittest.TestCase):
    def test_cwn_is_still_classified_and_unmodified(self):
        """The pivot must not become a quiet rules change: the constitution audit still governs."""
        import subprocess
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools/rules_constitution_audit.py"), "--check"],
            capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_the_rpg_readme_states_the_immutable_boundary(self):
        text = (ROOT / "NooPunk-RPG/README.md").read_text(encoding="utf-8")
        self.assertIn("immutable core", text)
        self.assertIn("Nothing has been moved yet", text)


if __name__ == "__main__":
    unittest.main()
