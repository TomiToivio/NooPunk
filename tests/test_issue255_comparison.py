"""Guard for the #255 comparison gate.

#255 is emphatic that the skill mapping must be *shown*, not handwaved ("no handwaving that
different lists are identical"), and that the licence boundaries must be explicit. So this file
pins four things:

1. **Completeness** -- every skill in the canonical list is mapped into all four families,
   exactly once, and nothing else is. A missing skill is the handwave.
2. **Honest labelling** -- every cell carries a label from the declared vocabulary, so a
   conversion cannot be presented as `direct` without saying so.
3. **The document is current** -- generated from the data, so its numbers cannot drift.
4. **The author's explicit instructions survive** -- Fudge out of scope, #200's centre flagged
   superseded *while its implementation is preserved*, six locked STATs kept distinct from skills.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "data" / "rules" / "skill_mapping_crosssystem.json"
SKILLS = ROOT / "data" / "rules" / "skills.json"
CORE = ROOT / "data" / "rules" / "core.json"
DOC = ROOT / "COMPARISON.md"

sys.path.insert(0, str(ROOT / "tools"))
import issue255_comparison_report as report

LOCKED_STATS = ("FIT", "REF", "INT", "SOC", "CYB", "PSY")


def mapping() -> dict:
    return json.loads(MAPPING.read_text(encoding="utf-8"))


def skills() -> dict:
    return json.loads(SKILLS.read_text(encoding="utf-8"))


class CompletenessTests(unittest.TestCase):
    """A skill missing from the table is exactly the handwave the issue forbids."""

    def test_every_canonical_skill_is_mapped(self) -> None:
        canonical = {s["name"] for s in skills()["skills"]}
        mapped = {row["skill"] for row in mapping()["mapping"]}
        self.assertFalse(canonical - mapped, f"unmapped: {sorted(canonical - mapped)}")

    def test_nothing_is_mapped_that_is_not_canonical(self) -> None:
        canonical = {s["name"] for s in skills()["skills"]}
        mapped = {row["skill"] for row in mapping()["mapping"]}
        self.assertFalse(mapped - canonical, f"invented: {sorted(mapped - canonical)}")

    def test_no_skill_is_mapped_twice(self) -> None:
        names = [row["skill"] for row in mapping()["mapping"]]
        self.assertEqual(sorted(names), sorted(set(names)))

    def test_the_declared_count_matches_the_canonical_list(self) -> None:
        self.assertEqual(mapping()["skills_in_source"], len(skills()["skills"]))

    def test_every_family_is_present_in_every_row(self) -> None:
        families = [f["id"] for f in mapping()["families"]]
        self.assertEqual(len(families), 4)
        for row in mapping()["mapping"]:
            with self.subTest(skill=row["skill"]):
                for family in families:
                    self.assertIn(family, row)

    def test_the_summary_matches_the_mapping(self) -> None:
        """The summary is computed, never hand-written; a guard stops it drifting."""
        declared = {k: v for k, v in mapping()["summary"].items() if not k.startswith("$")}
        self.assertEqual(declared, report.skill_summary(mapping()))


class LabellingTests(unittest.TestCase):
    def test_every_label_is_from_the_vocabulary(self) -> None:
        vocabulary = set(mapping()["label_vocabulary"])
        for row in mapping()["mapping"]:
            for family in (f["id"] for f in mapping()["families"]):
                with self.subTest(skill=row["skill"], family=family):
                    self.assertIn(row[family]["label"], vocabulary)

    def test_a_cell_named_as_a_counterpart_is_not_labelled_unsupported(self) -> None:
        """Internal consistency: naming a counterpart and calling it unsupported is a contradiction."""
        for row in mapping()["mapping"]:
            for family in (f["id"] for f in mapping()["families"]):
                cell = row[family]
                if cell["name"] and cell["label"] == "unsupported":
                    self.fail(f"{row['skill']}/{family}: names {cell['name']!r} but says unsupported")

    def test_unsupported_cells_name_no_counterpart(self) -> None:
        for row in mapping()["mapping"]:
            for family in (f["id"] for f in mapping()["families"]):
                cell = row[family]
                if cell["label"] == "unsupported":
                    self.assertIsNone(cell["name"], f"{row['skill']}/{family}")

    def test_every_family_states_its_verification_status(self) -> None:
        """Facts and analogies must be separable, as the issue requires."""
        for family in mapping()["families"]:
            with self.subTest(family=family["id"]):
                self.assertTrue(family["verification"].strip())
                self.assertTrue(family["license"].strip())

    def test_pbta_is_marked_as_moves_not_skills(self) -> None:
        pbta = next(f for f in mapping()["families"] if f["id"] == "pbta")
        self.assertIn("MOVE", pbta["mechanic_type"].upper())


class AuthorInstructionTests(unittest.TestCase):
    """The instructions the issue states explicitly must survive into the artifact."""

    def test_the_six_locked_stats_are_unchanged(self) -> None:
        canon = json.loads(CORE.read_text(encoding="utf-8"))
        stats = canon["stats"]["names"] if isinstance(canon["stats"], dict) else canon["stats"]
        self.assertEqual(tuple(stats), LOCKED_STATS)

    def test_mapped_stats_stay_within_the_locked_set(self) -> None:
        allowed = set(LOCKED_STATS) | {"Variable"}
        for row in mapping()["mapping"]:
            with self.subTest(skill=row["skill"]):
                self.assertIn(row["stat"], allowed)

    def test_fudge_is_marked_out_of_scope_in_the_document(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Fudge is out of scope", text)
        self.assertIn("OUT OF SCOPE", text)

    def test_200s_centre_is_flagged_superseded(self) -> None:
        self.assertIn("superseded", DOC.read_text(encoding="utf-8").lower())

    def test_prior_implementation_is_preserved_not_deleted(self) -> None:
        """The issue is explicit: flag superseded, preserve the work until audited."""
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("preserved", text.lower())
        self.assertTrue((ROOT / "src/rules/kernel_prototype.py").exists(),
                        "the superseded prototype must survive for audit")

    def test_the_document_denies_canonical_status(self) -> None:
        self.assertIn("Nothing in this file is canonical", DOC.read_text(encoding="utf-8"))


class RightsTests(unittest.TestCase):
    def test_the_rights_matrix_covers_all_four_families(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        for system in ("Fate Core", "Eclipse Phase", "Cities Without Number",
                       "Stars Without Number", "The Veil", "Apocalypse World"):
            with self.subTest(system=system):
                self.assertIn(system, text)

    def test_non_commercial_sources_are_not_marked_reusable(self) -> None:
        """A conversion that could quote these would breach the CC release target."""
        for row in report.t_rights():
            if "NC" in row:
                with self.subTest(row=row[:40]):
                    self.assertIn("| no |", row)

    def test_the_nc_sources_are_named_as_sources_only(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("inspiration", text)
        self.assertIn("cannot appear in a commercially released CC NoöPunk", text)

    def test_the_swn_caveat_survives(self) -> None:
        self.assertIn("not automatically an open SRD", DOC.read_text(encoding="utf-8"))


class DocumentIsGeneratedTests(unittest.TestCase):
    def test_the_document_is_current(self) -> None:
        result = subprocess.run([sys.executable, "tools/issue255_comparison_report.py", "--check"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_the_document_carries_the_required_sections(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        for heading in ("## 1. Purpose", "## 2–3.", "## 4. Subsystem", "## 5. PSI",
                        "## 6. Two alternative", "## 7. Sources", "## 8. Cross-references"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_the_four_d_f_distribution_is_exact(self) -> None:
        """81 outcomes, and +4 must guarantee success -- the argument the kernels rest on."""
        distribution = report.fdf()
        self.assertEqual(len(distribution), 9)
        self.assertEqual(sum(distribution.values()), 1)
        self.assertEqual(report.vs_dv(4, 0), 1)


if __name__ == "__main__":
    unittest.main()
