"""Pins #709's reconciliation of the investigation API with CWN semantics.

Three things are tested here, and each one was a real defect in the merged prototype:

* **rank 0 is trained** - CWN skills are level 0..4 and 0 is basic competence, so a
  character who has the skill at all is competent at it;
* **competence is necessary, never sufficient** - access and declared inquiry are separate
  gates, so a medically trained investigator does not read a terminal they cannot reach;
* **a terminal scene needs no exit** - validation must not force authors to invent a lead.
"""
import unittest

from src.rules.investigation import (
    Case,
    Clue,
    ClueKind,
    InvestigationError,
    Investigator,
    Scene,
    discover,
)

WARD_ROSTER = Clue(
    id="roster", scene_id="ward", kind=ClueKind.CORE, competency="Administer",
    fact="The shift roster was changed twice that night.", access="ward", inquiry="search",
)
WARD_TERMINAL = Clue(
    id="terminal", scene_id="ward", kind=ClueKind.OPTIONAL, competency="Program",
    fact="The drip pump logs a manual reset.", access="medical_records",
)
WARD_OBVIOUS = Clue(
    id="chart", scene_id="ward", kind=ClueKind.OPTIONAL, competency="Heal",
    fact="The chart is open on the desk.", passive=True,
)
CLOSING = Scene(id="interview", title="Patient interview", terminal=True,
                clues=(Clue(id="account", scene_id="interview", kind=ClueKind.OPTIONAL,
                            competency="Empathy", fact="The patient contradicts the chart.",
                            inquiry="interview"),))

WARD = Scene(id="ward", title="Ward", clues=(WARD_ROSTER, WARD_TERMINAL, WARD_OBVIOUS))
CASE = Case(id="lakkahaltia", scenes=(WARD, CLOSING))


class RankZeroTest(unittest.TestCase):
    def test_rank_zero_counts_as_trained(self):
        clinician = Investigator.from_sheet("Romppainen", {"Heal": 0})
        self.assertTrue(clinician.is_competent("Heal"))

    def test_an_absent_skill_is_not_competent(self):
        self.assertFalse(Investigator.from_sheet("Clerk", {"Administer": 1}).is_competent("Heal"))


class AccessTest(unittest.TestCase):
    def test_a_clue_needs_access_as_well_as_competence(self):
        clerk = Investigator.from_sheet("Clerk", {"Administer": 2})
        found = discover(CASE, "ward", clerk)          # competent, but not admitted
        self.assertNotIn("roster", found.clue_ids)

    def test_access_alone_without_competence_still_fails(self):
        outsider = Investigator.from_sheet("Guard", {"Shoot": 1})
        found = discover(CASE, "ward", outsider, access={"ward", "medical_records"}, inquiry={"search"})
        self.assertNotIn("roster", found.clue_ids)

    def test_competence_with_access_and_inquiry_grants_the_clue(self):
        clerk = Investigator.from_sheet("Clerk", {"Administer": 2})
        found = discover(CASE, "ward", clerk, access={"ward"}, inquiry={"search"})
        self.assertIn("roster", found.clue_ids)
        self.assertTrue(found.can_leave)

    def test_a_separate_access_gate_keeps_the_terminal_out_of_reach(self):
        programmer = Investigator.from_sheet("Tech", {"Program": 1, "Administer": 1})
        found = discover(CASE, "ward", programmer, access={"ward"}, inquiry={"search"})
        self.assertNotIn("terminal", found.clue_ids)
        self.assertIn("terminal", found.withheld_ids)


class InquiryTest(unittest.TestCase):
    def test_a_declared_inquiry_is_required_for_an_active_clue(self):
        clerk = Investigator.from_sheet("Clerk", {"Administer": 2})
        found = discover(CASE, "ward", clerk, access={"ward"})       # no inquiry declared
        self.assertNotIn("roster", found.clue_ids)

    def test_a_passive_clue_needs_no_declared_search(self):
        clinician = Investigator.from_sheet("Nurse", {"Heal": 0})
        found = discover(CASE, "ward", clinician)
        self.assertIn("chart", found.clue_ids)

    def test_withheld_clues_are_reported_rather_than_silently_dropped(self):
        clerk = Investigator.from_sheet("Clerk", {"Administer": 2})
        found = discover(CASE, "ward", clerk)
        self.assertIn("roster", found.withheld_ids)


class TerminalSceneTest(unittest.TestCase):
    def test_a_terminal_scene_validates_without_a_core_clue(self):
        CASE.validate()   # CLOSING is terminal and has no core clue

    def test_a_non_terminal_scene_without_a_core_clue_still_fails(self):
        broken = Case(id="broken", scenes=(Scene(id="empty", title="Nothing"),))
        with self.assertRaises(InvestigationError):
            broken.validate()


if __name__ == "__main__":
    unittest.main()
