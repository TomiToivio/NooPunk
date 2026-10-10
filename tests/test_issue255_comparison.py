"""Guard for the #255 comparison gate.

`COMPARISON.md` is hand-written (it is long, argued prose, and that is the right form for a
research gate), so these guards test the **requirements the issue states** rather than any
particular wording: every skill mapped, six attributes, four families, honest labels, a rights
matrix, and the author's explicit instructions.

They also guard the machine-readable crosswalk in `data/rules/skill_mapping_crosssystem.json`
for completeness, and the separate exact-odds appendix, which IS generated.

Deliberately NOT checked: the exact phrases of `COMPARISON.md`. An earlier version of this file
asserted my own sentences and failed against a better document written in parallel; a guard
should pin requirements, not authorship.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "data" / "rules" / "skill_mapping_crosssystem.json"
SKILLS = ROOT / "data" / "rules" / "skills.json"
CORE = ROOT / "data" / "rules" / "core.json"
SOURCES = ROOT / "data" / "sources" / "game_system_rights.json"
DOC = ROOT / "COMPARISON.md"
ODDS = ROOT / "docs" / "design" / "ISSUE_255_ODDS.md"

sys.path.insert(0, str(ROOT / "tools"))
import issue255_comparison_report as report

LOCKED_STATS = ("FIT", "REF", "INT", "SOC", "CYB", "PSY")
FAMILIES = ("Fate", "Eclipse Phase", "Cities Without Number", "The Veil")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def doc_text() -> str:
    return DOC.read_text(encoding="utf-8")


class CrosswalkCompletenessTests(unittest.TestCase):
    """A skill missing from the crosswalk is exactly the handwave #255 forbids."""

    def test_every_canonical_skill_is_mapped(self) -> None:
        canonical = {s["name"] for s in load(SKILLS)["skills"]}
        mapped = {row["skill"] for row in load(MAPPING)["mapping"]}
        self.assertFalse(canonical - mapped, f"unmapped: {sorted(canonical - mapped)}")

    def test_nothing_is_mapped_that_is_not_canonical(self) -> None:
        canonical = {s["name"] for s in load(SKILLS)["skills"]}
        mapped = {row["skill"] for row in load(MAPPING)["mapping"]}
        self.assertFalse(mapped - canonical, f"invented: {sorted(mapped - canonical)}")

    def test_no_skill_is_mapped_twice(self) -> None:
        names = [row["skill"] for row in load(MAPPING)["mapping"]]
        self.assertEqual(sorted(names), sorted(set(names)))

    def test_every_row_covers_all_four_families(self) -> None:
        families = [f["id"] for f in load(MAPPING)["families"]]
        self.assertEqual(len(families), 4)
        for row in load(MAPPING)["mapping"]:
            with self.subTest(skill=row["skill"]):
                for family in families:
                    self.assertIn(family, row)

    def test_every_label_is_from_the_declared_vocabulary(self) -> None:
        vocabulary = set(load(MAPPING)["label_vocabulary"])
        for row in load(MAPPING)["mapping"]:
            for family in (f["id"] for f in load(MAPPING)["families"]):
                with self.subTest(skill=row["skill"], family=family):
                    self.assertIn(row[family]["label"], vocabulary)

    def test_a_named_counterpart_is_never_labelled_unsupported(self) -> None:
        for row in load(MAPPING)["mapping"]:
            for family in (f["id"] for f in load(MAPPING)["families"]):
                cell = row[family]
                if cell["name"]:
                    self.assertNotEqual(cell["label"], "unsupported",
                                        f"{row['skill']}/{family} names a counterpart but "
                                        f"calls it unsupported")

    def test_the_summary_matches_the_mapping(self) -> None:
        declared = {k: v for k, v in load(MAPPING)["summary"].items() if not k.startswith("$")}
        self.assertEqual(declared, report.skill_summary(load(MAPPING)))

    def test_every_family_states_its_verification_status_and_licence(self) -> None:
        for family in load(MAPPING)["families"]:
            with self.subTest(family=family["id"]):
                self.assertTrue(family["verification"].strip())
                self.assertTrue(family["license"].strip())


class DocumentRequirementsTests(unittest.TestCase):
    """The issue's own acceptance criteria, tested against the document as written."""

    def test_the_document_exists_and_is_substantial(self) -> None:
        text = doc_text()
        self.assertGreater(len(text.splitlines()), 200)

    def test_the_document_has_one_title_and_no_duplicate_section_numbers(self) -> None:
        """A merged COMPARISON.md carried two H1 titles and two of every §1–§8.

        The concatenation arrived because two PRs each treated this file as *the*
        comparison and their contents were merged rather than reconciled. Nothing in the
        other guards notices it — a presence check passes a file that says everything twice
        — so this pins the structural requirement directly: exactly one title, and no
        section number defined more than once.
        """
        text = doc_text()
        titles = re.findall(r"(?m)^# .+", text)
        self.assertEqual(len(titles), 1,
                         f"COMPARISON.md must have exactly one H1 title, found {titles!r}")
        numbers = re.findall(r"(?m)^## (\d+)\.", text)
        duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
        self.assertEqual(duplicates, [],
                         f"section number(s) defined more than once: {duplicates}")

    def test_the_six_attributes_are_all_present(self) -> None:
        text = doc_text()
        for stat in LOCKED_STATS:
            with self.subTest(stat=stat):
                self.assertIn(stat, text)

    def test_all_four_families_are_compared(self) -> None:
        text = doc_text()
        for family in FAMILIES:
            with self.subTest(family=family):
                self.assertIn(family, text)

    def test_every_canonical_skill_name_appears_in_the_document(self) -> None:
        """The full mapping must be *shown*, per the issue, not merely stored in JSON."""
        text = doc_text()
        missing = [s["name"] for s in load(SKILLS)["skills"] if s["name"] not in text]
        self.assertFalse(missing, f"not shown in COMPARISON.md: {missing}")

    def test_the_gamist_and_narrativist_corners_are_named(self) -> None:
        text = doc_text()
        self.assertIn("Stars Without Number", text)
        self.assertIn("Apocalypse World", text)

    def test_the_psi_non_identity_is_explained(self) -> None:
        """Issue deliverable 5: a Move is not merely a power."""
        text = doc_text().lower()
        self.assertIn("move", text)
        self.assertIn("stunt", text)
        self.assertIn("sleight", text)

    def test_no_rule_is_declared_canonical(self) -> None:
        text = doc_text().lower()
        self.assertIn("no rule becomes", text.replace("\n", " "))

    def test_fudge_is_marked_out_of_scope(self) -> None:
        self.assertIn("out of scope", doc_text().lower())

    def test_the_superseded_premise_is_flagged_and_preserved(self) -> None:
        """The issue requires flagging #200's centre superseded WITHOUT deleting prior work."""
        text = doc_text().lower()
        self.assertIn("supersede", text)
        self.assertIn("preserved", text)

    def test_a_rights_matrix_covers_the_nc_sources(self) -> None:
        text = doc_text()
        self.assertIn("NC", text)
        self.assertIn("NonCommercial", text.replace(" ", ""))

    def test_the_swn_free_edition_is_not_treated_as_open(self) -> None:
        text = doc_text().lower()
        self.assertTrue("not an open" in text or "not an srd" in text,
                        "the document must not present SWN's free edition as an open SRD")


class AuthorInstructionTests(unittest.TestCase):
    def test_the_six_locked_stats_are_unchanged(self) -> None:
        canon = load(CORE)
        stats = canon["stats"]["names"] if isinstance(canon["stats"], dict) else canon["stats"]
        self.assertEqual(tuple(stats), LOCKED_STATS)

    def test_mapped_stats_stay_within_the_locked_set(self) -> None:
        allowed = set(LOCKED_STATS) | {"Variable"}
        for row in load(MAPPING)["mapping"]:
            with self.subTest(skill=row["skill"]):
                self.assertIn(row["stat"], allowed)

    def test_prior_implementation_is_preserved_not_deleted(self) -> None:
        self.assertTrue((ROOT / "src/rules/kernel_prototype.py").exists(),
                        "the superseded prototype must survive for audit")

    def test_the_nc_sources_are_not_reusable_in_the_rights_ledger(self) -> None:
        by_id = {s["id"]: s for s in load(SOURCES)["sources"]}
        for source_id in ("eclipse-phase-2e", "transhumanitys-fate"):
            with self.subTest(source=source_id):
                self.assertNotIn(by_id[source_id]["decision"], ("verified-permissive",))


class OddsAppendixTests(unittest.TestCase):
    """The exact arithmetic is generated, so it is checked for currency."""

    def test_the_appendix_exists(self) -> None:
        self.assertTrue(ODDS.exists(), "docs/design/ISSUE_255_ODDS.md is missing")

    def test_the_appendix_is_current(self) -> None:
        result = subprocess.run([sys.executable, "tools/issue255_comparison_report.py", "--check"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_the_4df_distribution_is_exact(self) -> None:
        distribution = report.fdf()
        self.assertEqual(len(distribution), 9)
        self.assertEqual(sum(distribution.values()), 1)
        self.assertEqual(distribution[0], report.Fraction(19, 81))

    def test_a_plus_four_bonus_guarantees_success(self) -> None:
        """The measurement the cap argument rests on: 4dF cannot roll below -4."""
        self.assertEqual(report.vs_dv(4, 0), 1)
        self.assertEqual(report.vs_dv(3, 0), report.Fraction(80, 81))


if __name__ == "__main__":
    unittest.main()
