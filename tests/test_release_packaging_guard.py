"""Executable contracts for the release packaging guard (issue #421 item 3, guard from #231).

Code-only, per `AGENTS.md` and issue #271. Until now the guard had **no test at all**, which is how its
artefact classes came to describe a layout the repository no longer had: they covered ``src/**`` and
``tests/**`` while the game lives in ``strategy_game/**``, so the audit warned "unreviewed-material" on
159 first-party paths and "must not ship" for the whole game. A guard that warns on everything warns on
nothing.

The pair of contracts below is the point: the **false alarms are gone** *and* the genuine NC-SA
exposure still fires. Silencing the guard would have been easy and wrong, so one test asserts the
noise is gone and another asserts the signal remains.

Run:
    python -m unittest discover -s tests -p "test_release_packaging_guard.py"
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from release_packaging_guard import (  # noqa: E402
    classify_path,
    iter_tree_paths,
    load_policy,
    quarantine_reason,
    run_guard,
)

#: The EP2 homebrew prototype: the largest NC-SA clean-up obligation before S1.
#: The last two entries were added by issue #421 — the modules that exercise the prototype import
#: the quarantined code directly and carry its percentile/pool fixtures, so they are inside the same
#: boundary. Measured before that: a public-mode bundle of those two paths returned **no**
#: quarantined-path-in-release-set finding.
EP2_QUARANTINED = (
    "src/eclipse_phase_homebrew/core.py",
    "src/concordia_runtime/ep2_session.py",
    "tests/test_ep2_session.py",
    "tests/test_issue60_ep2_interactions.py",
)


class FalseAlarmsAreGoneTests(unittest.TestCase):
    """The guard must not warn on first-party paths it should already know how to classify."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run_guard(ROOT, "audit")

    def test_the_audit_reports_no_unreviewed_material(self) -> None:
        """The regression pin for the #421 classification fix: 159 -> 0."""
        unreviewed = [f for f in self.result.findings if f.code == "unreviewed-material"]
        self.assertEqual(unreviewed, [], "first-party paths must be covered by an artefact class")

    def test_the_audit_reports_no_errors(self) -> None:
        self.assertTrue(self.result.ok, self.result.format())

    def test_every_tracked_path_is_classified_or_quarantined(self) -> None:
        policy = load_policy(ROOT)
        unclassified = [rel for rel in iter_tree_paths(ROOT)
                        if classify_path(rel, policy) is None
                        and quarantine_reason(rel, policy) is None]
        self.assertEqual(unclassified, [])


class TheGameIsInThePlanTests(unittest.TestCase):
    """The game package must be covered, mirrored onto the classes its old layout used."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_policy(ROOT)

    def test_game_source_is_classified_as_source_code(self) -> None:
        for rel in ("strategy_game/view.py", "strategy_game/rpg/fate.py",
                    "strategy_game/tests/test_map_spec.py", "strategy_game/tabletop/board.py"):
            self.assertEqual(classify_path(rel, self.policy), "source-code", rel)

    def test_game_rule_data_is_grouped_with_the_rules_not_the_code(self) -> None:
        self.assertEqual(classify_path("strategy_game/data/council.json", self.policy), "rule-data")

    def test_game_design_records_are_grouped_with_the_records(self) -> None:
        self.assertEqual(classify_path("strategy_game/docs/GENRE_PARADIGMS.md", self.policy),
                         "design-and-audit-records")

    def test_the_game_readme_is_prose_not_code(self) -> None:
        self.assertEqual(classify_path("strategy_game/README.md", self.policy), "rulebook-prose")

    def test_a_quarantine_glob_is_never_swallowed_by_a_later_class(self) -> None:
        """Class order matters: a quarantined path must still report a quarantine reason."""
        for rel in EP2_QUARANTINED:
            self.assertIsNotNone(quarantine_reason(rel, self.policy), rel)


class TheSignalRemainsTests(unittest.TestCase):
    """The genuine NC-SA exposure must still fire. Silencing it would defeat the guard."""

    def test_a_quarantined_path_in_a_release_set_is_an_error(self) -> None:
        result = run_guard(ROOT, "public", bundle=list(EP2_QUARANTINED))
        codes = {f.code for f in result.findings}
        self.assertIn("quarantined-path-in-release-set", codes)
        self.assertFalse(result.ok, "a release set containing NC-SA-derived material must not pass")

    def test_the_ep2_prototype_is_still_in_the_quarantine_list(self) -> None:
        policy = load_policy(ROOT)
        globs = " ".join(entry["glob"] for entry in policy["quarantined_paths"])
        self.assertIn("eclipse_phase_homebrew", globs)

    def test_a_clean_release_set_has_no_quarantine_error(self) -> None:
        result = run_guard(ROOT, "public", bundle=["strategy_game/view.py", "README.md"])
        codes = {f.code for f in result.findings}
        self.assertNotIn("quarantined-path-in-release-set", codes)

    def test_a_public_release_is_blocked_until_the_author_decides(self) -> None:
        """Correct behaviour, and worth pinning: the gate refuses to call a release clean while the
        licence decision is still the author's. The blocker is the decision, not packaging."""
        result = run_guard(ROOT, "public", bundle=["strategy_game/view.py", "README.md"])
        codes = {f.code for f in result.findings}
        self.assertIn("licence-decision-open", codes)
        self.assertFalse(result.ok)


class NoLicenceIsSelectedHereTests(unittest.TestCase):
    """This guard records packaging rules. It must not select a licence or write a licence file."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_policy(ROOT)

    def test_the_author_decision_is_still_recorded_as_open(self) -> None:
        self.assertIs(self.policy["author_decision_open"], True)

    def test_the_status_says_the_decision_is_still_open(self) -> None:
        self.assertIn("author-decision-still-open", self.policy["status"])

    def test_no_licence_or_notice_file_has_been_created(self) -> None:
        for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "NOTICE", "NOTICE.md"):
            self.assertFalse((ROOT / name).exists(), f"{name} must await the author's decision")

    def test_no_class_declares_a_selected_licence(self) -> None:
        """Every class defers: either 'author-decision' or 'author-decision-<what follows>'."""
        for artifact_class in self.policy["artifact_classes"]:
            self.assertTrue(artifact_class["licence"].startswith("author-decision"),
                            artifact_class["id"])

    def test_the_guard_reads_the_exclusion_set_from_the_ledger(self) -> None:
        """One home for exclusions: the policy must defer rather than restate."""
        comment = self.policy["$comment"]
        self.assertIn("Do not add a second exclusion list anywhere", comment)


class PolicyConsistencyTests(unittest.TestCase):
    def test_the_policy_and_ledger_agree(self) -> None:
        from release_packaging_guard import check_policy_consistency, load_ledger
        self.assertEqual(check_policy_consistency(load_policy(ROOT), load_ledger(ROOT)), [])

    def test_every_path_matching_a_class_has_no_quarantine_overlap(self) -> None:
        from release_packaging_guard import path_matches_glob
        policy = load_policy(ROOT)
        self.assertTrue(path_matches_glob("strategy_game/view.py", "strategy_game/**"))
        self.assertTrue(path_matches_glob("src/x.py", "src/**"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
