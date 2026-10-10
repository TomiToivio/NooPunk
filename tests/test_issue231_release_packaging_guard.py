"""Guard for the issue #231 release packaging guard.

Issue #231 asks for a machine-readable rights ledger, attribution and a **release packaging
guard**, and the release gate document's own checklist asks to *"add checks that flag
unreviewed third-party material in packaging and prevent reintroduction of explicitly excluded
licenses."* This test guards the guard, because a packaging gate that silently passes is worse
than no gate: it converts an unmade licensing decision into an apparent clearance.

What must NOT drift:

* nothing here may select a licence or add ``LICENSE``/``NOTICE`` -- that is the author's call
  and the issue records it as open;
* the excluded-licence vocabulary must keep coming FROM the rights ledger, so no second list
  can grow beside it;
* a quarantined path in an explicit release bundle is an error, while the same path merely
  existing in the working tree is not (the prototype legitimately lives in the repo);
* a public release cannot pass while the licence decision is open;
* the checks fail closed on a missing or unparseable ledger.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import release_packaging_guard as guard  # noqa: E402

POLICY = ROOT / "data" / "licenses" / "release_packaging_policy.json"
LEDGER = ROOT / "data" / "sources" / "game_system_rights.json"


def policy() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def ledger() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


class PolicyConsistencyTests(unittest.TestCase):
    def test_policy_and_ledger_exist(self) -> None:
        self.assertTrue(POLICY.exists(), "the packaging policy must exist")
        self.assertTrue(LEDGER.exists(), "the rights ledger must exist")

    def test_every_excluded_decision_is_defined_by_the_ledger(self) -> None:
        """The policy defers its exclusions to the ledger; the two cannot drift apart."""
        self.assertEqual(guard.check_policy_consistency(policy(), ledger()), [])

    def test_the_exclusion_vocabulary_is_not_empty(self) -> None:
        self.assertTrue(policy()["excluded_licence_decisions"])

    def test_the_noncommercial_decision_is_excluded(self) -> None:
        self.assertIn("verified-nc-sharealike", policy()["excluded_licence_decisions"])

    def test_the_proprietary_decision_is_excluded(self) -> None:
        self.assertIn("proprietary-out-of-scope", policy()["excluded_licence_decisions"])

    def test_no_class_is_declared_under_an_excluded_licence(self) -> None:
        self.assertEqual(guard.check_class_licences(policy()), [])

    def test_a_class_declared_under_an_excluded_licence_is_caught(self) -> None:
        """Prove the check fires, not merely that the shipped policy happens to be clean."""
        bad = json.loads(json.dumps(policy()))
        bad["artifact_classes"][0]["licence"] = "verified-nc-sharealike"
        findings = guard.check_class_licences(bad)
        self.assertEqual([f.code for f in findings], ["class-declared-under-excluded-licence"])

    def test_a_class_under_an_ordinary_licence_is_not_flagged(self) -> None:
        bad = json.loads(json.dumps(policy()))
        bad["artifact_classes"][0]["licence"] = "CC-BY-SA-4.0"
        self.assertEqual(guard.check_class_licences(bad), [])

    def test_an_excluded_decision_missing_from_the_ledger_is_caught(self) -> None:
        """Drift the other way: the policy excludes something the ledger never defines."""
        bad = json.loads(json.dumps(policy()))
        bad["excluded_licence_decisions"].append("invented-decision")
        findings = guard.check_policy_consistency(bad, ledger())
        self.assertEqual([f.code for f in findings], ["excluded-decision-not-in-ledger"])

    def test_the_author_decision_is_still_recorded_as_open(self) -> None:
        self.assertTrue(policy()["author_decision_open"])

    def test_every_class_licence_still_awaits_the_author(self) -> None:
        for cls in policy()["artifact_classes"]:
            self.assertTrue(
                str(cls["licence"]).startswith("author-decision"),
                f"{cls['id']} must not pre-select a licence")


class PathMatchingTests(unittest.TestCase):
    def test_normalize_keeps_a_leading_dot(self) -> None:
        """Regression: str.lstrip('./') ate the dot, turning .github/ into github/."""
        self.assertEqual(guard._normalize(".github/workflows/pages.yml"),
                         ".github/workflows/pages.yml")
        self.assertEqual(guard._normalize("./src/x.py"), "src/x.py")
        self.assertEqual(guard._normalize(".gitignore"), ".gitignore")

    def test_dot_directories_are_classified(self) -> None:
        self.assertEqual(guard.classify_path(".github/workflows/pages.yml", policy()),
                         "packaging-and-config")

    def test_double_star_spans_zero_directories(self) -> None:
        self.assertTrue(guard.path_matches_glob("src/core.py", "src/**"))

    def test_double_star_spans_many_directories(self) -> None:
        self.assertTrue(guard.path_matches_glob("src/a/b/c.py", "src/**"))

    def test_double_star_does_not_leak_to_a_sibling(self) -> None:
        self.assertFalse(guard.path_matches_glob("scripts/x.py", "src/**"))

    def test_double_star_matches_the_directory_itself(self) -> None:
        """`src/**` covers `src` and its whole subtree; plain fnmatch would reject `src`."""
        self.assertTrue(guard.path_matches_glob("src", "src/**"))
        self.assertTrue(guard.path_matches_glob("src/a/b.py", "src/**"))

    def test_a_prefix_that_only_shares_letters_does_not_match(self) -> None:
        self.assertFalse(guard.path_matches_glob("srcfoo/x.py", "src/**"))


class QuarantineTests(unittest.TestCase):
    def test_the_ep2_prototype_is_quarantined(self) -> None:
        reason = guard.quarantine_reason("src/eclipse_phase_homebrew/core.py", policy())
        self.assertIsNotNone(reason, "the EP2 homebrew prototype must stay quarantined")

    def test_the_concordia_ep2_adapter_is_quarantined(self) -> None:
        self.assertIsNotNone(
            guard.quarantine_reason("src/concordia_runtime/ep2_adapter.py", policy()))

    def test_the_quarantined_paths_still_exist_in_the_tree(self) -> None:
        """A quarantine that names paths no longer present has gone stale silently."""
        tree = list(guard.iter_tree_paths(ROOT))
        for entry in policy()["quarantined_paths"]:
            matches = [p for p in tree if guard.path_matches_glob(p, entry["glob"])]
            self.assertTrue(matches,
                            f"{entry['glob']} is quarantined but matches nothing in the tree "
                            f"— the quarantine has gone stale")

    def test_the_named_quarantine_globs_are_present(self) -> None:
        """Deleting a quarantine entry must not be a silent way to pass."""
        globs = {e["glob"] for e in policy()["quarantined_paths"]}
        for required in ("src/eclipse_phase_homebrew/**",
                         "src/concordia_runtime/ep2_*.py"):
            self.assertIn(required, globs, f"quarantine entry {required} was removed")

    def test_every_quarantine_entry_carries_a_reason(self) -> None:
        for entry in policy()["quarantined_paths"]:
            self.assertTrue(entry.get("reason"), f"{entry['glob']} has no reason recorded")

    def test_ordinary_source_is_not_quarantined(self) -> None:
        self.assertIsNone(guard.quarantine_reason("src/rules/core.py", policy()))


class BundleModeTests(unittest.TestCase):
    def test_a_quarantined_path_in_a_bundle_is_an_error(self) -> None:
        result = guard.run_guard(ROOT, "audit", ["src/eclipse_phase_homebrew/core.py"])
        self.assertFalse(result.ok)
        self.assertIn("quarantined-path-in-release-set", [f.code for f in result.errors])

    def test_the_same_path_in_the_full_tree_is_only_a_warning(self) -> None:
        result = guard.run_guard(ROOT, "audit")
        self.assertNotIn("quarantined-path-in-release-set", [f.code for f in result.errors])

    def test_an_unreviewed_path_in_a_bundle_is_an_error(self) -> None:
        result = guard.run_guard(ROOT, "audit", ["totally/unknown/file.bin"])
        self.assertFalse(result.ok)
        self.assertIn("unreviewed-material", [f.code for f in result.errors])

    def test_a_reviewed_path_in_a_bundle_passes(self) -> None:
        result = guard.run_guard(ROOT, "audit", ["rulebook/1_NOÖPUNK.md", "data/rules/core.json"])
        self.assertTrue(result.ok, result.format())

    def test_an_unreviewed_path_in_the_full_tree_is_only_a_warning(self) -> None:
        """No tracked path may be unreviewed, or the licence plan has a hole."""
        result = guard.run_guard(ROOT, "audit")
        unreviewed = [f for f in result.errors if f.code == "unreviewed-material"]
        self.assertEqual(unreviewed, [], "every tracked file needs an artifact class")


class ModeTests(unittest.TestCase):
    def test_audit_mode_passes_with_the_decision_open(self) -> None:
        self.assertTrue(guard.run_guard(ROOT, "audit").ok)

    def test_public_mode_fails_while_the_decision_is_open(self) -> None:
        result = guard.run_guard(ROOT, "public", ["rulebook/1_NOÖPUNK.md"])
        self.assertFalse(result.ok)
        self.assertIn("licence-decision-open", [f.code for f in result.errors])

    def test_an_unknown_mode_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            guard.run_guard(ROOT, "whatever")

    def test_a_documented_mention_is_never_an_error(self) -> None:
        """README/RULEBOOK state the game contains NC-derived material; that is not a defect."""
        result = guard.run_guard(ROOT, "audit", ["README.md", "RULEBOOK.md"])
        mentions = [f for f in result.errors if f.code == "documented-licence-mention"]
        self.assertEqual(mentions, [])
        self.assertTrue([f for f in result.warnings if f.code == "documented-licence-mention"])


class FailClosedTests(unittest.TestCase):
    def test_a_missing_ledger_raises_rather_than_passing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data" / "licenses").mkdir(parents=True)
            (root / "data" / "licenses" / "release_packaging_policy.json").write_text(
                json.dumps(policy()), encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                guard.run_guard(root, "audit")

    def test_a_malformed_policy_raises_rather_than_passing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data" / "licenses").mkdir(parents=True)
            (root / "data" / "licenses" / "release_packaging_policy.json").write_text(
                "{not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                guard.run_guard(root, "audit")

    def test_an_empty_ledger_vocabulary_is_an_error(self) -> None:
        result = guard.check_policy_consistency(policy(), {"decision_vocabulary": {}})
        self.assertTrue(result)
        self.assertEqual(result[0].code, "ledger-vocabulary-empty")


class AuthorDecisionTests(unittest.TestCase):
    def test_no_license_or_notice_file_was_added(self) -> None:
        """#231 is not authority to relicence the repository."""
        for name in ("LICENSE", "LICENSE.md", "NOTICE", "NOTICE.md"):
            self.assertFalse((ROOT / name).exists(), f"{name} must not be created by an agent")

    def test_the_policy_does_not_claim_a_selection(self) -> None:
        p = policy()
        self.assertNotIn("selected_licence", p)
        self.assertIn("guard-scaffold-author-decision-still-open", p["status"])


if __name__ == "__main__":
    unittest.main()
