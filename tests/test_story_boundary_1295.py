"""Executable contracts for the diff-level Story boundary (#1295).

`tests/test_issue_1295_structure.py` protects the *statement* of the rule. This file protects the
*check*: the allowlist is exactly the boundary note, a Windows separator cannot escape the prefix test,
a sibling directory with a similar name is not inside it, deletions count as changes, and the CLI's
exit codes mean what the workflow thinks they mean.

Run:
    python -m unittest discover -s tests -p "test_story_boundary_1295.py"
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from story_boundary import (
    ALLOWED,
    STORY_DIR,
    changed_paths,
    main,
    normalize,
    violations,
)


class AllowlistTests(unittest.TestCase):
    def test_the_only_allowlisted_path_is_the_boundary_note(self):
        self.assertEqual(ALLOWED, {f"{STORY_DIR}/README.md"})

    def test_the_boundary_note_exists_and_is_not_prose_holder(self):
        note = ROOT / STORY_DIR / "README.md"
        self.assertTrue(note.is_file())
        self.assertFalse((ROOT / STORY_DIR / "chapter-01.md").exists(),
                         "no agent may stage prose to make a test pass")


class ViolationTests(unittest.TestCase):
    def test_the_boundary_note_is_not_a_violation(self):
        self.assertEqual(violations([f"{STORY_DIR}/README.md"]), [])

    def test_an_empty_change_is_clean(self):
        self.assertEqual(violations([]), [])

    def test_a_chapter_is_a_violation(self):
        self.assertEqual(violations([f"{STORY_DIR}/chapter-01.md"]), [f"{STORY_DIR}/chapter-01.md"])

    def test_a_nested_draft_is_a_violation(self):
        paths = [f"{STORY_DIR}/drafts/scene-4.md"]
        self.assertEqual(violations(paths), paths)

    def test_a_deletion_is_a_violation_too(self):
        self.assertEqual(violations([f"{STORY_DIR}/old-scene.md"]), [f"{STORY_DIR}/old-scene.md"])

    def test_a_windows_separator_cannot_escape_the_check(self):
        self.assertEqual(
            violations([f"{STORY_DIR}\\chapter-01.md"]),
            [f"{STORY_DIR}/chapter-01.md"],
        )

    def test_a_leading_dot_slash_is_normalised(self):
        self.assertEqual(violations([f"./{STORY_DIR}/x.md"]), [f"{STORY_DIR}/x.md"])

    def test_a_sibling_directory_is_not_inside_the_boundary(self):
        for path in (f"{STORY_DIR}-drafts/x.md", "NooPunk-Story/Graph/scene.json",
                     "NooPunk-Story/templates/SCENE_SCRIPT.md",
                     "docs/architecture/PIVOT_1295_MIGRATION_MAP.md"):
            self.assertEqual(violations([path]), [], path)

    def test_the_directory_itself_is_a_violation(self):
        self.assertEqual(violations([STORY_DIR]), [STORY_DIR])

    def test_duplicates_collapse(self):
        self.assertEqual(violations([f"{STORY_DIR}/a.md"] * 3), [f"{STORY_DIR}/a.md"])


class CliTests(unittest.TestCase):
    def test_an_explicit_story_path_fails(self):
        self.assertEqual(main(["--paths", f"{STORY_DIR}/chapter-02.md"]), 1)

    def test_an_explicit_path_outside_story_passes(self):
        self.assertEqual(main(["--paths", "NooPunk-Story/Graph/README.md", "README.md"]), 0)

    def test_the_repository_as_committed_is_clean(self):
        """The diff against HEAD is empty, so the guard must pass on its own tree."""
        self.assertEqual(main(["--base", "HEAD", "--root", str(ROOT)]), 0)

    def test_an_unreadable_base_is_reported_rather_than_passing(self):
        self.assertEqual(main(["--base", "no-such-ref-anywhere", "--root", str(ROOT)]), 2)


class DiffTests(unittest.TestCase):
    def test_a_bogus_base_raises_rather_than_returning_nothing(self):
        with self.assertRaises(RuntimeError):
            changed_paths("definitely-not-a-ref", str(ROOT))

    def test_head_against_head_is_empty(self):
        self.assertEqual(changed_paths("HEAD", str(ROOT)), [])


class NormalizeTests(unittest.TestCase):
    def test_separators_and_prefixes(self):
        self.assertEqual(normalize("./NooPunk-Story\\Story\\a.md"), "NooPunk-Story/Story/a.md")


if __name__ == "__main__":
    unittest.main()
