"""Agents must share one Godot implementation (docs/godot/CANONICAL_GODOT_TREE.md).

Parallel agents landed two catalogues, two character modules and two test roots. Each worked, each was
tested, and a rule fixed in one was silently missing from the other. This guard fails CI when that
shape comes back.

It does not police style or file counts: it polices the one thing that caused real drift - the same
rule implemented twice under two roots.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Rule logic lives here. A second copy of a rule may not appear in godot/core/.
RULES_ROOT = ROOT / "src" / "godot"
GLUE_ROOT = ROOT / "godot" / "core"

#: Known duplicates, listed so the guard cannot be satisfied by widening it. Each must be deleted
#: per docs/godot/CANONICAL_GODOT_TREE.md; removing a name here is the completion signal.
#: Workflows still pointing at the legacy test root. Four separate Godot workflows grew in parallel;
#: each must be folded into one. Listed so this guard fails on a *new* stray rather than on known debt.
KNOWN_LEGACY_WORKFLOWS = {
    "godot-smoke.yml",
    "cwn-progression.yml",
    "cwn-godot-rules.yml",
    "godot.yml",
}

KNOWN_DUPLICATES = {
    "cwn_catalogue.gd",   # godot/core copy to be deleted; test repointed at src/godot
    "cwn_character.gd",   # same
    # Found by this guard on 2026-10-30: a later merge reintroduced these two. They are debt, not
    # permission - deleting a name from this set is the completion signal for #791.
    # "cwn_healing.gd" retired in #791: merged into godot/core/cwn_healing.gd and deleted.
    # "cwn_strain.gd" retired in #791: merged into godot/core/cwn_strain.gd and deleted.
}


def _basenames(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {path.name for path in root.rglob("*.gd")}


class GodotSingleImplementationTest(unittest.TestCase):
    def test_the_two_roots_exist(self) -> None:
        """A guard over missing directories would pass vacuously."""
        self.assertTrue(RULES_ROOT.is_dir(), RULES_ROOT)
        self.assertTrue(GLUE_ROOT.is_dir(), GLUE_ROOT)

    def test_no_new_rule_module_is_implemented_twice(self) -> None:
        overlap = _basenames(RULES_ROOT) & _basenames(GLUE_ROOT)
        unexpected = sorted(overlap - KNOWN_DUPLICATES)
        self.assertEqual(
            unexpected,
            [],
            "a rule module now exists in both src/godot/ and godot/core/: {}. "
            "Put rule logic in src/godot/ and glue in godot/core/; see "
            "docs/godot/CANONICAL_GODOT_TREE.md".format(unexpected),
        )

    def test_the_known_duplicates_are_still_real(self) -> None:
        """When a duplicate is merged away, delete it from the allow-list in the same change."""
        overlap = _basenames(RULES_ROOT) & _basenames(GLUE_ROOT)
        stale = sorted(KNOWN_DUPLICATES - overlap)
        self.assertEqual(
            stale,
            [],
            "these names are no longer duplicated; remove them from KNOWN_DUPLICATES: {}".format(stale),
        )

    def test_ci_runs_one_test_root(self) -> None:
        """`tests/godot/` is legacy. CI must run godot/tests/ only, or two suites drift apart."""
        workflows = list((ROOT / ".github" / "workflows").glob("*.yml"))
        self.assertTrue(workflows, "expected CI workflows")
        runners = [
            path.name
            for path in workflows
            if "godot/tests/run_tests.gd" in path.read_text(encoding="utf-8")
        ]
        self.assertTrue(runners, "no workflow runs godot/tests/run_tests.gd")
        strays = sorted(
            path.name
            for path in workflows
            if "tests/godot/" in path.read_text(encoding="utf-8")
            and path.name not in KNOWN_LEGACY_WORKFLOWS
        )
        self.assertEqual(strays, [], "a new workflow runs the legacy test root: {}".format(strays))

    def test_the_canonical_tree_is_documented(self) -> None:
        doc = ROOT / "docs" / "godot" / "CANONICAL_GODOT_TREE.md"
        self.assertTrue(doc.is_file(), "the canonical-tree rule must be written down")
        text = doc.read_text(encoding="utf-8")
        self.assertIn("src/godot/", text)
        self.assertIn("godot/core/", text)


if __name__ == "__main__":
    sys.exit(unittest.main())
