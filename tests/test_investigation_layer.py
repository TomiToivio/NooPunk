"""Tests for the investigative layer (#704).

These pin the three separations the design rests on: discovery is not a roll,
interpretation is not the system's, and action is where CWN does its work.
"""
import inspect
import unittest

from src.rules.investigation import (
    Case,
    Clue,
    ClueKind,
    Hypothesis,
    InvestigationError,
    Investigator,
    Scene,
    Stance,
    discover,
    hypotheses_remain_open,
)

CORE = Clue(id="c1", scene_id="ward", kind=ClueKind.CORE, competency="Forensics",
            fact="The drip counter was reset by hand after the last round.",
            leads_to=("office",))
OPTIONAL = Clue(id="c2", scene_id="ward", kind=ClueKind.OPTIONAL, competency="Notice",
                fact="A visitor badge lies under the radiator.")
OBSCURE = Clue(id="c3", scene_id="office", kind=ClueKind.CORE, competency="Xenolinguistics",
               fact="The log contains a second, older signature.", obscure=True)
OFFICE_CORE = Clue(id="c4", scene_id="office", kind=ClueKind.CORE, competency="Administer",
                   fact="The shift roster was changed twice on the night in question.")

WARD = Scene(id="ward", title="Psychiatric ward", clues=(CORE, OPTIONAL))
OFFICE = Scene(id="office", title="Night office", clues=(OBSCURE, OFFICE_CORE))
CASE = Case(id="lakkahaltia", scenes=(WARD, OFFICE))

FORENSIC = Investigator(name="Romppainen", ratings={"Forensics": 2})
CLERK = Investigator(name="Clerk", ratings={"Administer": 1})


class DiscoveryTest(unittest.TestCase):
    def test_a_competent_investigator_gets_the_core_clue_without_a_roll(self):
        found = discover(CASE, "ward", FORENSIC)
        self.assertIn("c1", [clue.id for clue in found.clues])
        self.assertTrue(found.can_leave)
        self.assertEqual(found.granted_by, "competency")

    def test_no_competency_means_no_core_clue_and_no_exit(self):
        found = discover(CASE, "ward", InvestigatorsWithNothing)
        self.assertEqual(found.clues, ())
        self.assertFalse(found.can_leave)
        self.assertEqual(found.granted_by, "none")

    def test_an_alternative_method_is_granted_not_rolled(self):
        found = discover(CASE, "ward", InvestigatorsWithNothing, alternative_method=True)
        self.assertTrue(found.can_leave)
        self.assertEqual(found.granted_by, "alternative_method")

    def test_optional_clues_follow_the_competencies_the_investigator_actually_has(self):
        found = discover(CASE, "ward", FORENSIC)
        self.assertNotIn("c2", [clue.id for clue in found.clues])  # no Notice rating

        observer = Investigator(name="Observer", ratings={"Forensics": 1, "Notice": 1})
        found_both = discover(CASE, "ward", observer)
        self.assertIn("c2", [clue.id for clue in found_both.clues])

    def test_discovery_takes_no_randomness(self):
        params = set(inspect.signature(discover).parameters)
        self.assertFalse(params & {"roll", "die", "dice", "rng", "random"})


InvestigatorsWithNothing = Investigator(name="Unqualified")


class CaseValidationTest(unittest.TestCase):
    def test_a_scene_without_a_core_clue_is_a_dead_end(self):
        case = Case(id="broken", scenes=(Scene(id="empty", title="Nothing here"),))
        with self.assertRaises(InvestigationError):
            case.validate()

    def test_a_scene_whose_only_exit_is_obscure_is_refused(self):
        case = Case(id="gated", scenes=(Scene(id="office", title="Office", clues=(OBSCURE, OFFICE_CORE)),))
        # OFFICE_CORE is not obscure, so this case is legal; remove it to test the gate.
        case.validate()
        gated = Case(id="gated", scenes=(Scene(id="office", title="Office",
                    clues=(Clue(id="only", scene_id="office", kind=ClueKind.CORE,
                                competency="Xenolinguistics", fact="...", obscure=True),)),))
        with self.assertRaises(InvestigationError):
            gated.validate()

    def test_a_lead_to_a_missing_scene_is_refused(self):
        case = Case(id="dangling", scenes=(Scene(id="ward", title="Ward", clues=(
            Clue(id="x", scene_id="ward", kind=ClueKind.CORE, competency="Forensics",
                 fact="...", leads_to=("nowhere",)),)),))
        with self.assertRaises(InvestigationError):
            case.validate()

    def test_the_real_case_validates(self):
        CASE.validate()

    def test_an_unknown_scene_is_refused(self):
        with self.assertRaises(InvestigationError):
            discover(CASE, "basement", FORENSIC)


class HypothesisTest(unittest.TestCase):
    def test_the_system_classifies_evidence_but_never_sets_confidence(self):
        hypothesis = Hypothesis(id="h1", statement="A night nurse falsified the roster.")
        hypothesis.consider(CORE, Stance.SUPPORTS)
        hypothesis.consider(OPTIONAL, Stance.NEUTRAL)
        self.assertEqual(hypothesis.confidence, 0)          # untouched by evidence
        self.assertEqual(hypothesis.support_count(), 1)
        hypothesis.set_confidence(60)                        # the player's call
        self.assertEqual(hypothesis.confidence, 60)

    def test_a_contradicting_fact_is_a_legal_state(self):
        hypothesis = Hypothesis(id="h2", statement="It was a fault, not a person.")
        hypothesis.consider(CORE, Stance.CONTRADICTS)
        self.assertEqual(hypothesis.contradiction_count(), 1)

    def test_confidence_must_be_a_percentage(self):
        with self.assertRaises(InvestigationError):
            Hypothesis(id="h3", statement="...").set_confidence(101)

    def test_the_case_is_never_resolved_by_the_model(self):
        self.assertTrue(hypotheses_remain_open([Hypothesis(id="h", statement="...")]))


class SpendTest(unittest.TestCase):
    def test_a_spend_buys_extra_information_not_permission_to_find_a_clue(self):
        investigator = Investigator(name="Romppainen", ratings={"Forensics": 2})
        self.assertEqual(investigator.spend("Forensics", 1), 1)
        # still competent at 1: spending does not remove the ability
        self.assertTrue(investigator.is_competent("Forensics"))

    def test_a_spend_beyond_the_rating_is_refused(self):
        investigator = Investigator(name="R", ratings={"Forensics": 1})
        with self.assertRaises(InvestigationError):
            investigator.spend("Forensics", 2)

    def test_an_unrated_competency_cannot_be_spent(self):
        with self.assertRaises(InvestigationError):
            Investigator(name="R").spend("Forensics", 1)


if __name__ == "__main__":
    unittest.main()
