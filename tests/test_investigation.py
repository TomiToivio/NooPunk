"""The investigation procedure (#704): finding is free, interpretation costs a check.

Stdlib unittest only — NoöPunk's CI has no pytest.
"""

from __future__ import annotations

import unittest

from src.rules.investigation import (
    Case,
    Clue,
    DeadEndError,
    Grade,
    Hypothesis,
    InvestigationError,
    Outcome,
    ReadingKind,
    actionable,
    support_report,
)


def clue(cid, scene, grade, methods, discriminator="a test exists"):
    return Clue(
        id=cid, scene=scene, grade=grade,
        fact=f"fact {cid}",
        mundane_reading=f"mundane {cid}",
        anomalous_reading=f"anomalous {cid}",
        discriminator=discriminator,
        methods=tuple(methods),
    )


def ward_case() -> Case:
    return Case(
        id="lakkahaltia",
        scenes=("intake", "office", "morgue"),
        clues=(
            clue("C1", "intake", Grade.CORE, ("Infosec", "Research")),
            clue("C2", "office", Grade.CORE, ("Talk", "Administrate")),
            clue("C3", "morgue", Grade.CORE, ("Medicine", "Forensics")),
            clue("O1", "intake", Grade.OPTIONAL, ("Forensics",)),
            clue("X1", "office", Grade.COLOUR, ("Perceive",)),
        ),
    )


class TestNoDeadEnds(unittest.TestCase):
    def test_a_well_formed_case_validates(self):
        ward_case().validate()

    def test_a_single_path_core_clue_is_refused(self):
        bad = Case(
            id="bad", scenes=("a",),
            clues=(clue("C1", "a", Grade.CORE, ("Forensics",)),),
        )
        self.assertEqual(len(bad.dead_ends()), 1)
        with self.assertRaises(DeadEndError):
            bad.validate()

    def test_the_same_method_twice_is_still_one_path(self):
        bad = Case(
            id="bad", scenes=("a",),
            clues=(clue("C1", "a", Grade.CORE, ("Forensics", "Forensics")),),
        )
        with self.assertRaises(DeadEndError):
            bad.validate()

    def test_optional_and_colour_clues_may_have_one_path(self):
        Ward = ward_case()
        dead = [c.id for c in Ward.dead_ends()]
        self.assertNotIn("O1", dead)
        self.assertNotIn("X1", dead)


class TestFindingIsFree(unittest.TestCase):
    def setUp(self):
        self.case = ward_case()

    def test_a_trained_declaration_yields_the_fact_without_a_roll(self):
        r = self.case.seek("C1", "Infosec", trained=True)
        self.assertEqual(r.outcome, Outcome.GUARANTEED)
        self.assertEqual(r.fact, "fact C1")
        self.assertIn("C1", self.case.discovered)

    def test_an_untrained_declaration_does_not_get_the_guarantee(self):
        r = self.case.seek("C1", "Infosec", trained=False)
        self.assertEqual(r.outcome, Outcome.REQUIRES_CHECK)
        self.assertIsNone(r.fact)
        self.assertNotIn("C1", self.case.discovered)

    def test_a_wrong_method_names_the_real_ones(self):
        r = self.case.seek("C1", "Melee", trained=True)
        self.assertEqual(r.outcome, Outcome.UNKNOWN)
        self.assertEqual(set(r.alternatives), {"Infosec", "Research"})

    def test_an_optional_clue_costs_a_spend(self):
        r = self.case.seek("O1", "Forensics", trained=True)
        self.assertEqual(r.outcome, Outcome.REQUIRES_SPEND)
        self.assertNotIn("O1", self.case.discovered)
        paid = self.case.pay_and_take("O1", spent="two hours and a favour")
        self.assertEqual(paid.fact, "fact O1")
        self.assertIn("O1", self.case.discovered)

    def test_a_spend_must_name_its_cost(self):
        with self.assertRaises(InvestigationError):
            self.case.pay_and_take("O1", spent="   ")

    def test_colour_is_free_on_arrival(self):
        r = self.case.seek("X1", "Perceive", trained=False)
        self.assertEqual(r.outcome, Outcome.COLOUR)
        self.assertEqual(r.fact, "fact X1")


class TestInterpretationIsNotFree(unittest.TestCase):
    def setUp(self):
        self.case = ward_case()

    def test_a_reading_needs_its_fact_first(self):
        with self.assertRaises(InvestigationError):
            self.case.interpret("C1", ReadingKind.MUNDANE)

    def test_every_reading_requires_a_check(self):
        self.case.seek("C1", "Infosec", trained=True)
        for kind in (ReadingKind.MUNDANE, ReadingKind.ANOMALOUS):
            r = self.case.interpret("C1", kind)
            self.assertTrue(r.requires_check)
            self.assertIn(kind.value, r.statement)

    def test_the_module_never_returns_a_conclusion(self):
        # A reading carries no truth value — only a statement and a flag.
        self.case.seek("C1", "Infosec", trained=True)
        r = self.case.interpret("C1", ReadingKind.ANOMALOUS)
        self.assertFalse(hasattr(r, "true"))
        self.assertFalse(hasattr(r, "resolved"))


class TestTheAnomalyGate(unittest.TestCase):
    def setUp(self):
        self.case = ward_case()

    def test_the_gate_starts_closed(self):
        self.assertFalse(self.case.anomaly_gate_open())

    def test_the_gate_opens_only_when_every_core_discriminator_is_attempted(self):
        for cid in ("C1", "C2"):
            self.case.attempt_discriminator(cid)
        self.assertFalse(self.case.anomaly_gate_open())
        self.case.attempt_discriminator("C3")
        self.assertTrue(self.case.anomaly_gate_open())

    def test_resolving_as_anomalous_before_the_gate_raises(self):
        with self.assertRaises(InvestigationError):
            self.case.require_anomaly_gate()

    def test_a_discriminator_cannot_resolve_unattempted(self):
        with self.assertRaises(InvestigationError):
            self.case.resolve_discriminator("C1", supports=ReadingKind.ANOMALOUS)


class TestTheUncertaintyLedger(unittest.TestCase):
    def setUp(self):
        self.case = ward_case()

    def test_one_support_is_not_actionable(self):
        self.case.seek("C1", "Infosec", trained=True)
        h = Hypothesis("H2", ReadingKind.ANOMALOUS, "precognitive files", support=("C1",))
        self.assertFalse(actionable(h, self.case))

    def test_two_supports_from_different_scenes_are_actionable(self):
        self.case.seek("C1", "Infosec", trained=True)
        self.case.seek("C2", "Talk", trained=True)
        h = Hypothesis("H2", ReadingKind.ANOMALOUS, "precognitive files", support=("C1", "C2"))
        self.assertTrue(actionable(h, self.case))

    def test_two_supports_from_one_scene_count_once(self):
        # C1 and O1 are both in "intake": one document wearing two hats.
        self.case.seek("C1", "Infosec", trained=True)
        self.case.pay_and_take("O1", spent="an hour")
        h = Hypothesis("H2", ReadingKind.ANOMALOUS, "precognitive files", support=("C1", "O1"))
        self.assertFalse(actionable(h, self.case))

    def test_an_undiscovered_support_does_not_count(self):
        self.case.seek("C1", "Infosec", trained=True)
        h = Hypothesis("H2", ReadingKind.ANOMALOUS, "x", support=("C1", "C2"))
        self.assertFalse(actionable(h, self.case))

    def test_a_contradiction_blocks_action(self):
        self.case.seek("C1", "Infosec", trained=True)
        self.case.seek("C2", "Talk", trained=True)
        h = Hypothesis("H2", ReadingKind.ANOMALOUS, "x", support=("C1", "C2"), contradict=("C3",))
        self.assertFalse(actionable(h, self.case))

    def test_the_report_covers_every_hypothesis(self):
        self.case.seek("C1", "Infosec", trained=True)
        hs = (
            Hypothesis("H1", ReadingKind.MUNDANE, "template artefact", support=("C1",)),
            Hypothesis("H2", ReadingKind.ANOMALOUS, "precognition", support=("C1",)),
        )
        report = support_report(hs, self.case)
        self.assertEqual(set(report), {"H1", "H2"})
        self.assertFalse(any(report.values()))


class TestCaseIntegrity(unittest.TestCase):
    def test_a_clue_in_an_unknown_scene_is_refused(self):
        with self.assertRaises(InvestigationError):
            Case(id="x", scenes=("a",), clues=(clue("C1", "b", Grade.CORE, ("A", "B")),))

    def test_duplicate_clue_ids_are_refused(self):
        with self.assertRaises(InvestigationError):
            Case(
                id="x", scenes=("a",),
                clues=(clue("C1", "a", Grade.CORE, ("A", "B")), clue("C1", "a", Grade.COLOUR, ("C",))),
            )

    def test_a_core_clue_must_name_a_discriminator(self):
        with self.assertRaises(InvestigationError):
            clue("C1", "a", Grade.CORE, ("A", "B"), discriminator="  ")


if __name__ == "__main__":
    unittest.main()
