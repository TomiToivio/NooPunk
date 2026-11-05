"""CWN traceability and immutability (#1068): the audit must stay true, and CWN must not drift.

Three contracts, each one a way the audit could quietly become decoration:

1. **The matrix is regenerated, not written by hand.** The committed JSON and the coverage report must
   equal what the tools produce from the repository right now. A stale matrix is a lie about coverage.
2. **Curated evidence is checked against the code.** Every module, procedure/class/constant and test a
   curated row cites must exist; a renamed function must fail here, not in a reader's head.
3. **CWN core modules are immutable.** Their SHA-256 is pinned in `data/rules/cwn_baseline_sha256.json`;
   any edit, however small, fails until someone re-pins the baseline in a PR that admits it is changing
   CWN. That is the mechanical form of "locked forever".

These are code tests: they read JSON produced by a tool and files that hold executable code. Nothing
here asserts on rulebook prose (#271): the tabletop side is enforced by the AGENTS.md PR checklist.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from cwn_parity_audit import MATRIX, REPORT, build, render_report, stable_view  # noqa: E402

CURATED = ROOT / "data" / "rules" / "cwn_traceability.json"
BASELINE = ROOT / "data" / "rules" / "cwn_baseline_sha256.json"
STATUSES = {"implemented", "partial", "missing", "not_applicable", "unverified"}


def fresh_matrix() -> dict:
    return build()


class FreshnessTests(unittest.TestCase):
    def test_the_committed_matrix_matches_the_tool(self) -> None:
        """Compare the rule-bearing content, not the names of the test files that happened to exist.

        The matrix records test filenames as evidence; including them in the equality made the lock depend on other
        branches (a PR that changed no CWN rule went red because main gained a test file). `stable_view` reduces each
        row's test list to its count, so a *new* test cannot fail a rule-unchanged branch, while a deleted or
        re-pointed module still does.
        """
        self.assertTrue(MATRIX.is_file(), "run python3 tools/cwn_parity_audit.py")
        committed = json.loads(MATRIX.read_text(encoding="utf-8"))
        self.assertEqual(
            stable_view(committed), stable_view(fresh_matrix()),
            "data/rules/cwn_compliance_matrix.json is stale; run python3 tools/cwn_parity_audit.py")

    def test_every_implemented_row_has_a_test_in_the_current_tree(self) -> None:
        """The evidence rule is enforced on a fresh build, not on the committed file.

        The committed matrix names test files, and those names move whenever any branch adds or deletes one. Checking
        the *committed* file against the tree therefore makes the lock fail for reasons that have nothing to do with
        CWN (#1228, #1229). The invariant that matters — an `implemented` row must have a real test behind it — is
        checked against the build of the current tree instead.
        """
        rows = fresh_matrix()["rows"]
        orphans = [
            row["system"] for row in rows
            if row["coverage"] == "implemented"
            and not any((ROOT / test).is_file() for test in row.get("tests", ()))
        ]
        self.assertEqual(orphans, [], "implemented rows without an existing test")

    def test_the_coverage_report_matches_the_tool(self) -> None:
        self.assertTrue(REPORT.is_file(), "run python3 tools/cwn_parity_audit.py")
        self.assertEqual(
            REPORT.read_text(encoding="utf-8"), render_report(fresh_matrix()),
            "docs/rules/CWN_COVERAGE_1068.md is stale; run python3 tools/cwn_parity_audit.py")

    def test_the_check_mode_agrees_with_the_test(self) -> None:
        result = subprocess.run([sys.executable, "tools/cwn_parity_audit.py", "--check"],
                                cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class CuratedEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = fresh_matrix()
        self.rows = {row["id"]: row for row in self.matrix["rows"]}
        self.curated = json.loads(CURATED.read_text(encoding="utf-8"))["rows"]

    def test_every_curated_row_exists_in_the_matrix(self) -> None:
        for entry in self.curated:
            self.assertIn(entry["id"], self.rows, f"curated row {entry['id']!r} is not an SRD section")

    def test_no_duplicate_curated_rows(self) -> None:
        ids = [entry["id"] for entry in self.curated]
        self.assertEqual(len(ids), len(set(ids)))

    def test_curated_evidence_verifies_against_the_code(self) -> None:
        problems = {key: value["problems"]
                    for key, value in self.matrix["verification"].items() if value["problems"]}
        self.assertEqual(problems, {}, f"curated evidence does not match the code: {problems}")

    def test_every_status_is_in_the_vocabulary(self) -> None:
        for row in self.matrix["rows"]:
            self.assertIn(row["coverage"], STATUSES, row["id"])

    def test_an_implemented_curated_row_names_its_evidence(self) -> None:
        for entry in self.curated:
            row = self.rows[entry["id"]]
            if row["coverage"] != "implemented":
                continue
            self.assertTrue(row["python"], f"{row['id']}: no module")
            self.assertTrue(row["tests"], f"{row['id']}: no test")
            self.assertTrue(row.get("procedures"), f"{row['id']}: no named procedure")
            self.assertTrue(row.get("rulebook"), f"{row['id']}: no rulebook anchor")

    def test_a_missing_row_states_why(self) -> None:
        for row in self.matrix["rows"]:
            if row["coverage"] in {"missing", "partial"}:
                self.assertTrue(row.get("divergence"), f"{row['id']}: a gap with no recorded reason")

    def test_every_row_points_at_the_srd_or_says_why_not(self) -> None:
        for row in self.matrix["rows"]:
            self.assertTrue(row["srd"], row["id"])


class ImmutabilityTests(unittest.TestCase):
    def test_the_baseline_covers_every_cwn_module(self) -> None:
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["files"]
        on_disk = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "src" / "rules").glob("cwn_*.py"))
        self.assertEqual(sorted(baseline), on_disk,
                         "a new CWN module must be pinned in data/rules/cwn_baseline_sha256.json")

    def test_no_cwn_rule_file_has_changed(self) -> None:
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["files"]
        changed = []
        for rel, expected in baseline.items():
            actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
            if actual != expected:
                changed.append(rel)
        self.assertEqual(changed, [],
                         "CWN core is locked (#1068): these files changed. Revert them, or re-pin the "
                         f"baseline in a PR that explicitly says it is changing CWN: {changed}")

    def test_the_new_lifestyle_module_is_pinned_too(self) -> None:
        """A module added by the audit is protected by the same lock from the day it lands."""
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["files"]
        self.assertIn("src/rules/cwn_lifestyles.py", baseline)


if __name__ == "__main__":
    unittest.main()
