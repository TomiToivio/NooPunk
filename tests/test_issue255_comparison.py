# -*- coding: utf-8 -*-
"""Issue #255 — the comparison gate exists, is complete, and stays a gate.

The issue is explicit that this is a *research/design gate, not permission to rewrite the
rulebook, code or already merged work*, and that **no rule becomes canonical** without
approval. So the guards are about three things:

 1. the document is COMPLETE against the issue's own eight required sections;
 2. the full canonical skill list is actually mapped, family by family (the issue forbids
    "handwaving that different lists are identical");
 3. **the gate held** — `data/rules/core.json` still carries the legacy kernel, because a
    comparison that silently migrated the core would be the exact failure the gate exists to
    prevent.

The licence rows are asserted as *honesty about verification*, not as verdicts: an
unverified source must be recorded unverified, so this test fails if a row is later
upgraded to a clean grant without evidence.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "COMPARISON.md"
SKILLS = ROOT / "data" / "rules" / "skills.json"
CORE = ROOT / "data" / "rules" / "core.json"


def text() -> str:
    return DOC.read_text(encoding="utf-8")


def flat() -> str:
    return " ".join(text().split())


class TheGateExistsTests(unittest.TestCase):
    def test_the_document_exists_at_the_repo_root(self) -> None:
        self.assertTrue(DOC.is_file(), "COMPARISON.md is missing")

    def test_it_declares_itself_a_gate_and_not_canon(self) -> None:
        t = flat().lower()
        self.assertIn("nothing in this document is canonical", t)
        self.assertIn("no rule becomes canonical", t)

    def test_every_required_section_is_present(self) -> None:
        t = text()
        for needle in (
            "## 1. Goals, design triangle, trade-offs and scope",
            "## 2. Side-by-side conversion tables",
            "## 3. Labelling discipline",
            "## 4. Subsystem-by-subsystem comparison",
            "## 5. PSI as three different design objects",
            "## 6. Two alternative Fate-first kernels",
            "## 7. Source and rights matrix",
            "## 8. Cross-references to existing repo work",
        ):
            with self.subTest(section=needle):
                self.assertIn(needle, t)


class SkillsAreActuallyMappedTests(unittest.TestCase):
    """The issue: 'Show full skill mapping; no handwaving that different lists are identical.'"""

    def setUp(self) -> None:
        self.skills = [s["name"] for s in json.loads(SKILLS.read_text(encoding="utf-8"))["skills"]]

    def test_the_canonical_skill_list_is_the_one_mapped(self) -> None:
        self.assertEqual(len(self.skills), 40, "the canonical list changed; re-map it")

    def test_every_canonical_skill_appears_in_the_mapping_table(self) -> None:
        body = text()
        missing = [name for name in self.skills if f"| {name} (" not in body]
        self.assertEqual(missing, [], f"skills absent from the mapping table: {missing}")

    def test_the_mapping_marks_unsupported_explicitly(self) -> None:
        t = flat()
        self.assertIn("no counterpart", t.lower())
        self.assertIn("**U** = no counterpart", t)

    def test_it_refuses_to_call_the_lists_identical(self) -> None:
        t = flat()
        self.assertIn("No two of these lists are identical", t)
        self.assertIn("Neither direction is lossless", t, "as written in the document")

    def test_it_does_not_claim_the_list_is_fate_derived(self) -> None:
        t = flat()
        self.assertIn("should not be described as Fate-derived", t)


class AuthorConstraintsTests(unittest.TestCase):
    def test_six_separate_attributes_are_stated(self) -> None:
        t = flat()
        self.assertIn("FIT / REF / INT / SOC / PSY / CYB", t)
        self.assertIn("Attributes distinct from Skills", t)

    def test_fudge_and_psi_punk_are_out_of_scope(self) -> None:
        t = flat()
        self.assertIn("Fudge and Psi-Punk are **out of scope as active sources**", t)
        self.assertIn("carries no Fudge or Psi-Punk column", t)

    def test_the_200_supersession_is_flagged(self) -> None:
        t = flat()
        self.assertIn("#255 supersedes that centre for all future comparison decisions", t)
        self.assertIn("This is a direction change, not an erasure", t)

    def test_prior_work_is_preserved_not_deleted(self) -> None:
        t = flat()
        self.assertIn("remain in the tree and keep passing", t)
        self.assertIn("Nothing is deleted", t)


class ProbabilityTests(unittest.TestCase):
    """The numbers must be the computed ones, not plausible-looking ones."""

    def test_the_4df_distribution_is_exact(self) -> None:
        t = flat()
        self.assertIn("1 | 4 | 10 | 16 | **19** | 16 | 10 | 4 | 1", t)
        self.assertIn("61.7%", t)

    def test_the_spread_comparison_is_stated_with_both_numbers(self) -> None:
        t = flat()
        self.assertIn("SD 1.633", t)
        self.assertIn("SD 2.872", t)
        self.assertIn("57% of 1d10's", t)

    def test_both_kernels_are_present_and_labelled_proposals(self) -> None:
        t = flat()
        self.assertIn("### 6.2 Kernel A", t)
        self.assertIn("### 6.3 Kernel B", t)
        self.assertIn("proposals for review", t)
        self.assertIn("Neither is implemented", t)

    def test_the_worked_case_admits_the_kernels_are_not_equivalent(self) -> None:
        t = flat()
        self.assertIn("the three are not the same task", t)
        self.assertIn("a single worked case is not sufficient evidence", t)


class LicenceHonestyTests(unittest.TestCase):
    def test_the_reusable_grant_is_attributed(self) -> None:
        t = flat()
        self.assertIn("only **Fate Core's SRD** is cleanly adaptable today", t)
        self.assertIn("Powered by Fate", t)

    def test_noncommercial_sources_are_marked_not_reusable(self) -> None:
        t = flat()
        self.assertIn("CC BY-NC-SA 4.0", t)
        self.assertIn("Attribution to Posthuman Studios", t)

    def test_unverified_sources_are_recorded_unverified(self) -> None:
        """A blocked or unchecked source is not a negative finding."""
        t = flat()
        self.assertIn("not established in this pass", t)
        self.assertIn("Unverified at source", t)
        self.assertIn("free-to-read, licence not established", t)

    def test_the_cwn_mirror_caveat_survives(self) -> None:
        t = flat()
        self.assertIn("it is a mirror and omits optional rules", t)


class TheGateHeldTests(unittest.TestCase):
    """The strongest guard: the comparison must not have migrated the core."""

    def test_the_live_kernel_is_still_the_legacy_one(self) -> None:
        core = json.loads(CORE.read_text(encoding="utf-8"))
        check = core["skill_check"]
        self.assertEqual(check["dice"], "1d10", "the core was migrated by a comparison issue")
        self.assertEqual(check["formula"], "STAT + Skill + 1d10")
        self.assertEqual(core["stats"]["min"], 1)
        self.assertEqual(core["stats"]["max"], 10)

    def test_the_document_says_the_live_kernel_is_unchanged(self) -> None:
        self.assertIn("**Unchanged by this document**", flat())

    def test_it_cross_references_the_issues_the_author_named(self) -> None:
        t = flat()
        for ref in ("#200", "#217", "#144", "#158", "#159", "skills.json"):
            with self.subTest(ref=ref):
                self.assertIn(ref, t)

    def test_it_names_the_conflicts_without_resolving_them(self) -> None:
        t = flat()
        self.assertIn("Conflicts identified, not resolved", t)

    def test_row_labels_are_defined(self) -> None:
        t = flat()
        for label in ("**D** = direct correspondence", "**A** = conceptual analogy",
                      "**U** = no counterpart"):
            with self.subTest(label=label):
                self.assertIn(label, t)


if __name__ == "__main__":
    unittest.main()
