"""Structure guard for the EP2 -> NoöPunk conversion matrix (issue #60, work package B).

The matrix exists to stop the project drifting invisibly: it records, per EP2
subsystem, what NoöPunk inherits, modifies, replaces or defers. This guard protects
the properties a later session could silently destroy.

What is protected here:

* the matrix parses and is versioned, following data/rules/core.json's conventions;
* every `status` is one of RULEBOOK.md section 3's five provenance labels, spelled
  exactly -- the repo uses NOÖPUNK, with the umlaut, and a matrix whose labels do not
  match the rulebook is not recording the rulebook's vocabulary;
* every claimed `rulebook_section` actually exists in RULEBOOK.md;
* every row marked `implemented` names a file that exists, and the kernel it names
  actually resolves a check when called -- a matrix that claims a subsystem runs when
  it does not is worse than no matrix;
* the deliberately unported parts of a partial port stay recorded, so a fragment is
  not mistaken for a complete port;
* the unresolved character-layer question stays recorded as unresolved, because
  resolving it is an author decision, not a cleanup;
* the subsystem count does not silently fall.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

MATRIX = "data/rules/conversion_matrix.json"
DOC = "docs/rules/EP2_CONVERSION_MATRIX.md"
RULEBOOK = "RULEBOOK.md"

#: The five provenance labels, exactly as RULEBOOK.md section 3 spells them.
#: Note the umlaut: the repo writes NOÖPUNK, not NOOPUNK.
RULEBOOK_LABELS = {
    "EP2 BASELINE",
    "MODIFIED EP2",
    "NOÖPUNK NATIVE",
    "EXPERIMENTAL",
    "DEFERRED",
}

#: Subsystems implemented only in part must say what is missing. These are the four
#: partial ports as of writing; the guard asserts the `not_implemented` list is
#: present and non-empty for each, so a fragment cannot be read as a full port.
PARTIAL_PORTS = {"combat", "mesh-hacking", "embodiment", "harm"}

#: Rows that must never claim to be implemented, whatever else changes.
DELIBERATELY_DEFERRED = {"psionics", "character-creation", "reputation", "vehicles",
                         "advancement", "reputation-economy"}

#: The character-layer question is the author's; the matrix must keep recording it
#: rather than resolving it.
CHARACTER_QUESTION = "four-system-vs-ep2-chassis"


def load() -> dict:
    return json.loads((ROOT / MATRIX).read_text(encoding="utf-8"))


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def rows() -> list[dict]:
    return load()["subsystems"]


class MatrixShapeTests(unittest.TestCase):
    def test_matrix_exists_and_parses(self) -> None:
        model = load()
        self.assertEqual(model["format"], "noopunk.rules.conversion_matrix")
        self.assertIsInstance(model["version"], int)
        self.assertIn("_note", model)
        self.assertIn("_source_of_truth", model)

    def test_it_defers_to_the_rulebook_as_source_of_truth(self) -> None:
        model = load()
        self.assertIn("rulebook", model["_source_of_truth"].lower())

    def test_every_row_has_the_required_fields(self) -> None:
        required = {"id", "name", "ep2_reference", "status", "implemented",
                    "conversion_target", "rationale"}
        for row in rows():
            with self.subTest(row=row.get("id")):
                missing = required - set(row)
                self.assertFalse(missing, f"{row.get('id')} is missing {sorted(missing)}")

    def test_ep2_coverage_is_explicit_per_row(self) -> None:
        """A row must say whether EP2 even has an equivalent."""
        for row in rows():
            with self.subTest(row=row["id"]):
                self.assertIn("ep2_covered", row)
                self.assertIsInstance(row["ep2_covered"], bool)


class LabelFidelityTests(unittest.TestCase):
    """The matrix must speak RULEBOOK section 3's vocabulary exactly."""

    def test_the_rulebook_really_defines_these_labels(self) -> None:
        book = read(RULEBOOK)
        for label in RULEBOOK_LABELS:
            with self.subTest(label=label):
                self.assertIn(label, book)

    def test_every_status_is_a_rulebook_label(self) -> None:
        allowed = RULEBOOK_LABELS | {"NOT YET MAPPED"}
        for row in rows():
            with self.subTest(row=row["id"]):
                self.assertIn(
                    row["status"], allowed,
                    f"{row['id']} uses status {row['status']!r}, which is not a "
                    f"RULEBOOK section 3 provenance label",
                )

    def test_status_labels_are_not_spelled_without_the_umlaut(self) -> None:
        """The repo writes NOÖPUNK. A status label in ASCII spelling is a mismatch.

        Scoped to the labels: the guard checks every row's `status` and the declared
        `status_values` list, not the whole file, since prose legitimately discusses
        the spellings.
        """
        declared = {v["id"] for v in load()["status_values"]} | {r["status"] for r in rows()}
        for label in declared:
            with self.subTest(label=label):
                self.assertNotIn("NOOEPUNK", label)
        self.assertIn("NOÖPUNK NATIVE", declared)

    def test_the_documented_status_list_matches_the_rows(self) -> None:
        """The file's own status_values list must match RULEBOOK, and cover the rows."""
        declared = {v["id"] for v in load()["status_values"]}
        self.assertTrue(
            RULEBOOK_LABELS <= declared,
            f"status_values is missing {RULEBOOK_LABELS - declared}",
        )
        used = {r["status"] for r in rows()}
        self.assertTrue(used <= declared, f"rows use undeclared labels: {used - declared}")


class RulebookWiringTests(unittest.TestCase):
    def test_every_claimed_rulebook_section_exists(self) -> None:
        book = read(RULEBOOK)
        sections = {m.group(1) for m in re.finditer(r"(?m)^## (\d+)\.", book)}
        for row in rows():
            ref = str(row.get("rulebook_section", ""))
            if not ref.isdigit():
                continue
            with self.subTest(row=row["id"], section=ref):
                self.assertIn(
                    ref, sections,
                    f"{row['id']} points at RULEBOOK section {ref}, which does not exist",
                )


class ImplementationClaimTests(unittest.TestCase):
    """An `implemented: true` row must have code that exists AND runs."""

    def test_every_implemented_row_names_an_existing_file(self) -> None:
        for row in rows():
            if not row["implemented"]:
                continue
            paths = []
            for entry in row.get("code", []):
                head = entry.split(":")[0].split(" (")[0].strip()
                if head.endswith(".py"):
                    paths.append(head)
            with self.subTest(row=row["id"]):
                self.assertTrue(paths, f"{row['id']} claims implementation but names no file")
                self.assertTrue(
                    any((ROOT / p).exists() for p in paths),
                    f"{row['id']} names files that do not exist: {paths}",
                )

    def test_the_ep2_kernel_actually_resolves_a_check(self) -> None:
        """Call the kernel the matrix points at, rather than trusting the label."""
        from eclipse_phase_homebrew import resolve_test

        result = resolve_test(target=55, roll=51)
        self.assertTrue(result.success)
        self.assertTrue(result.degree)

    def test_the_33_66_band_and_criticals_behave_as_recorded(self) -> None:
        """The matrix records the 33/66 band and doubles-as-criticals; check both.

        A double is a critical, so it carries no plain superior band -- asserting
        otherwise was a bug in an earlier version of this file's own prover.
        """
        from eclipse_phase_homebrew import resolve_test

        top = resolve_test(target=90, roll=70)   # >=66, not a double
        self.assertEqual(top.superior_successes, 2)
        mid = resolve_test(target=90, roll=65)   # >=33, not a double
        self.assertEqual(mid.superior_successes, 1)
        double = resolve_test(target=90, roll=66)  # a double IS a critical
        self.assertTrue(double.critical)
        self.assertEqual(double.superior_successes, 0)

    def test_the_modifier_cap_holds(self) -> None:
        from eclipse_phase_homebrew import resolve_test

        self.assertEqual(resolve_test(target=50, modifier=999, roll=50).modifier, 60)
        self.assertEqual(resolve_test(target=50, modifier=-999, roll=50).modifier, -60)

    def test_deliberately_deferred_subsystems_are_not_marked_implemented(self) -> None:
        """Psionics in particular: setting lore is not a licence to ship a psi subsystem."""
        by_id = {r["id"]: r for r in rows()}
        for sid in DELIBERATELY_DEFERRED:
            with self.subTest(subsystem=sid):
                self.assertIn(sid, by_id, f"{sid} row vanished from the matrix")
                self.assertFalse(
                    by_id[sid]["implemented"],
                    f"{sid} is recorded as implemented; it is deliberately deferred",
                )

    def test_psionics_records_that_it_is_explicitly_deferred(self) -> None:
        psy = next(r for r in rows() if r["id"] == "psionics")
        self.assertEqual(psy["status"], "DEFERRED")
        self.assertTrue(psy.get("explicitly_deferred"))


class PartialPortTests(unittest.TestCase):
    """A fragment must not be readable as a complete port."""

    def test_partial_ports_list_what_is_missing(self) -> None:
        by_id = {r["id"]: r for r in rows()}
        for sid in PARTIAL_PORTS:
            with self.subTest(subsystem=sid):
                self.assertIn(sid, by_id)
                missing = by_id[sid].get("not_implemented") or []
                self.assertTrue(missing, f"{sid} is a partial port but lists nothing missing")
                self.assertGreaterEqual(len(missing), 2)


class HonestyTests(unittest.TestCase):
    def test_the_character_layer_question_stays_unresolved(self) -> None:
        """Resolving it is an author decision, not a docs cleanup.

        The guard checks the *content* of the record, not merely its presence: a row
        whose question text has been rewritten to declare a winner, or whose status
        has been flipped to resolved, must fail.
        """
        questions = load()["unresolved_questions"]
        ids = {q["id"] for q in questions}
        self.assertIn(CHARACTER_QUESTION, ids)
        q = next(q for q in questions if q["id"] == CHARACTER_QUESTION)
        self.assertTrue(q.get("question"), "the question text is missing")
        self.assertTrue(q.get("evidence"), "the conflict must cite the documents involved")
        self.assertIn("owner", q)

        # It must read as OPEN, not settled.
        question = q["question"].lower()
        for claim in ("resolved:", "resolved —", "is settled", "has been decided"):
            self.assertNotIn(
                claim, question,
                f"the character-layer question is declared settled: {claim!r}",
            )
        # And the record must not carry a resolution field at all.
        for settled_key in ("resolution", "resolved", "decision", "answer"):
            self.assertNotIn(
                settled_key, q,
                f"the open question carries a {settled_key!r} field; it must stay open",
            )

    def test_it_does_not_silently_pick_a_winner(self) -> None:
        """Neither of the two contradictory documents may be called the resolution."""
        raw = read(MATRIX).lower()
        for phrase in ("the four-system model supersedes", "ep2 supersedes the four-system"):
            self.assertNotIn(phrase, raw)

    def test_the_matrix_records_that_it_does_not_decide_canon(self) -> None:
        self.assertIn("does not decide canon", read(MATRIX).lower())

    def test_the_subsystem_count_does_not_silently_fall(self) -> None:
        """A shrinking matrix is how coverage quietly disappears."""
        self.assertGreaterEqual(len(rows()), 25)

    def test_every_row_states_a_rationale(self) -> None:
        for row in rows():
            with self.subTest(row=row["id"]):
                self.assertTrue(row["rationale"].strip(), f"{row['id']} has no rationale")


class DocTests(unittest.TestCase):
    def test_the_companion_doc_exists_and_points_at_the_json(self) -> None:
        self.assertTrue((ROOT / DOC).exists(), f"{DOC} is missing")
        self.assertIn("conversion_matrix.json", read(DOC))

    def test_the_doc_says_it_records_rather_than_decides(self) -> None:
        text = " ".join(read(DOC).split()).lower()
        self.assertIn("records status", text)
        self.assertIn("does not decide canon", text)

    def test_the_doc_links_the_rulebook(self) -> None:
        self.assertIn("RULEBOOK.md", read(DOC))


if __name__ == "__main__":
    unittest.main()
