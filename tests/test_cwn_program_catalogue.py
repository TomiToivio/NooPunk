"""The CWN program catalogue: verbs, subjects, and what the table actually forbids (#752).

Transcribed from the SRD tables at <https://cwn.quadrifons.com/hacking/programs/>. These tests pin the
transcription, not an interpretation of it: if a row is mistyped, the numbers here disagree with the
published table and CI says so.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# This module imports a src/ package, so it puts src/ on sys.path itself rather than relying on
# another test module having done it first (tests/test_test_isolation.py enforces this form).
sys.path.insert(0, str(ROOT / "src"))

from rules.cwn_hacking import HackError
from rules.cwn_program_catalogue import (
    SPECIALIZED_SUBJECT_MULTIPLIER,
    SUBJECTS,
    UNIQUE_SUBJECT_MULTIPLIER,
    VERBS,
    program_cost,
    require_access,
    run_program,
    subject_cost,
    validate_program,
)


class VerbTableTest(unittest.TestCase):
    def test_the_srd_lists_twenty_four_verbs(self):
        self.assertEqual(len(VERBS), 24)

    def test_spot_check_published_rows(self):
        # Each tuple: cost, access cost, skill modifier, self-terminating
        self.assertEqual(
            (VERBS["Blind"].cost_usd, VERBS["Blind"].access_cost,
             VERBS["Blind"].skill_modifier, VERBS["Blind"].self_terminating),
            (2000, 1, 0, False),
        )
        self.assertEqual(
            (VERBS["Glitch"].cost_usd, VERBS["Glitch"].access_cost, VERBS["Glitch"].skill_modifier),
            (1000, 0, 2),
        )
        self.assertEqual(
            (VERBS["Paralyze"].access_cost, VERBS["Paralyze"].skill_modifier), (1, -2)
        )
        self.assertEqual((VERBS["Siege"].cost_usd, VERBS["Siege"].skill_modifier), (2500, -2))

    def test_self_terminating_verbs_are_the_starred_rows(self):
        starred = {name for name, verb in VERBS.items() if verb.self_terminating}
        self.assertEqual(
            starred,
            {"Activate", "Analyze", "Append", "Deactivate", "Decrypt", "Erase", "Frisk",
             "Kill", "Replace", "Sabotage", "Stun", "Terminate", "Unlock"},
        )

    def test_defend_is_the_only_verb_with_no_check(self):
        no_check = {name for name, verb in VERBS.items() if verb.skill_modifier is None}
        self.assertEqual(no_check, {"Defend"})


class SubjectTableTest(unittest.TestCase):
    def test_the_srd_lists_twelve_subjects(self):
        self.assertEqual(len(SUBJECTS), 12)

    def test_subject_types_cover_the_five_verb_targets(self):
        types = {subject.subject_type for subject in SUBJECTS.values()}
        self.assertEqual(types, {"Avatar", "Data", "Device", "Cyber", "Program"})

    def test_published_subject_prices(self):
        self.assertEqual(SUBJECTS["Avatar"].cost_usd, 500)
        self.assertEqual(SUBJECTS["Barrier"].cost_usd, 1000)
        self.assertEqual(SUBJECTS["Drone"].subject_type, "Device")
        self.assertEqual(SUBJECTS["Transmission"].subject_type, "Data")


class TargetLegalityTest(unittest.TestCase):
    def test_srd_example_cannot_blind_a_datafile(self):
        """The SRD names this exact case: 'you can't Blind a data file'."""
        with self.assertRaises(HackError) as caught:
            validate_program("Blind", "Datafile")
        self.assertIn("cannot target", str(caught.exception))

    def test_srd_example_cannot_delude_an_avatar(self):
        with self.assertRaises(HackError):
            validate_program("Delude", "Avatar")

    def test_terminate_only_targets_programs(self):
        self.assertTrue(validate_program("Terminate", "Program"))
        with self.assertRaises(HackError):
            validate_program("Terminate", "Door")

    def test_unknown_names_fail_closed(self):
        with self.assertRaises(HackError):
            validate_program("Frobnicate", "Door")
        with self.assertRaises(HackError):
            validate_program("Blind", "Toaster")


class RunCostTest(unittest.TestCase):
    def test_legal_run_spends_access_and_holds_cpu(self):
        run = run_program("Blind", "Camera", access_available=3, cpu_free=2)
        self.assertEqual((run.access_spent, run.cpu_held), (1, 1))
        self.assertTrue(run.requires_check)

    def test_self_terminating_returns_the_cpu_slot(self):
        run = run_program("Analyze", "Datafile", access_available=0, cpu_free=1)
        self.assertEqual(run.access_spent, 0)
        self.assertEqual(run.cpu_held, 0, "a self-terminating verb must not keep its slot")

    def test_insufficient_access_is_refused(self):
        with self.assertRaises(HackError) as caught:
            run_program("Blind", "Camera", access_available=0, cpu_free=4)
        self.assertIn("Access", str(caught.exception))

    def test_no_free_cpu_is_refused_even_for_a_free_verb(self):
        with self.assertRaises(HackError):
            run_program("Analyze", "Datafile", access_available=5, cpu_free=0)

    def test_defend_rolls_nothing(self):
        run = run_program("Defend", "Cyber", access_available=0, cpu_free=1)
        self.assertFalse(run.requires_check)
        self.assertIsNone(run.skill_modifier)


class PurchaseTest(unittest.TestCase):
    def test_program_cost_is_verb_plus_subject(self):
        self.assertEqual(program_cost("Blind", "Camera"), 2000 + 500)

    def test_specialized_and_unique_multipliers(self):
        base = subject_cost("Camera")
        self.assertEqual(subject_cost("Camera", specialized=True), base * SPECIALIZED_SUBJECT_MULTIPLIER)
        self.assertEqual(subject_cost("Camera", unique=True), base * UNIQUE_SUBJECT_MULTIPLIER)
        with self.assertRaises(HackError):
            subject_cost("Camera", specialized=True, unique=True)

    def test_access_requirement_helper(self):
        require_access(VERBS["Analyze"], access_available=0)  # costs 0
        with self.assertRaises(HackError):
            require_access(VERBS["Lock"], access_available=0)


class ExportedJsonTest(unittest.TestCase):
    """The Godot layer reads the JSON; it must not drift from the Python table."""

    def test_json_matches_the_transcribed_tables(self):
        import json

        path = Path(__file__).resolve().parents[1] / "data" / "rules" / "cwn_program_catalogue.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(set(data["verbs"]), set(VERBS))
        self.assertEqual(set(data["subjects"]), set(SUBJECTS))
        for name, row in data["verbs"].items():
            verb = VERBS[name]
            self.assertEqual(row["access_cost"], verb.access_cost, name)
            self.assertEqual(row["skill_modifier"], verb.skill_modifier, name)
            self.assertEqual(row["self_terminating"], verb.self_terminating, name)
            self.assertEqual(row["target_types"], sorted(verb.target_types), name)


if __name__ == "__main__":
    unittest.main()
