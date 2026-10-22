"""The corpus's mechanics, bound to the *Listening Ward* case.

The *Ubiquitous Maniacs* corpus arrived as two things that did not fit together: a body of
authorial mechanics written against its own Fate kernel, and a scenario that could not be
played because the data it needed was never committed upstream. Both halves are now in the
live system, and this file pins the **binding** between them.

What is pinned here is that the corpus's material is genuinely *in* the live system:

* the case's central fact — a procedure run on someone who was not asked — is represented by a
  **real state** (a psychosurgical session with the consent gate closed), not by a line of
  prose;
* the two witnesses who each saw a different person are represented by **real projection
  sessions**, and the model never resolves which of them is right;
* the scene's difficulty is a **real PSI context**, so a psychical attempt in the records room
  fails for a stated reason;
* and none of it introduces a second resolver, a second skill set or a new rule.

Nothing here asserts a difficulty, an ending distribution or an author decision. Every number
in this file is a fixture that makes one contract observable.
"""
from __future__ import annotations

import unittest
from random import Random

from strategy_game.casework import ubiquitous_maniacs, ward_mechanics
from strategy_game.characters import Tag
from strategy_game.rpg.fate import Character
from strategy_game.rpg.projection import ProjectionStatus
from strategy_game.rpg.psychosurgery import PsychosurgeryError
from strategy_game.rpg.skills import INDIVIDUAL_SKILL_NAMES, SkillLayerError


class TestTheCaseAndTheMechanicsAreOneSystem(unittest.TestCase):
    """The corpus's material lives in the live engine, not in a parallel copy."""

    def test_the_case_records_the_corpus_as_its_source(self) -> None:
        self.assertEqual(
            ubiquitous_maniacs.CASE.detail["legacy_source"],
            ward_mechanics.ARCHIVE_PATH.rstrip("/"),
        )

    def test_the_case_is_marked_non_canonical(self) -> None:
        self.assertIn("NOT CANON", ubiquitous_maniacs.CASE.detail["status"])

    def test_the_ported_modules_are_exported_by_the_rpg_package(self) -> None:
        from strategy_game import rpg

        for name in ("projection", "psi", "psychosurgery"):
            with self.subTest(module=name):
                self.assertIn(name, rpg.__all__)

    def test_the_case_plays_on_the_live_engine(self) -> None:
        """The case is playable as executable code, not merely declared."""
        session = ubiquitous_maniacs.build_session(seed=502)
        self.assertFalse(session.finished)
        self.assertEqual(session.scene_spec.id, "arrival")


class TestTheConsentGateIsTheCasesSubject(unittest.TestCase):
    """The scenario's central fact is a state, and the state refuses."""

    def _patient(self) -> Character:
        return Character(
            id=ward_mechanics.PATIENT_ID,
            name="The patient",
            aspects=["a person who came in for treatment"],
            skills={"INT": 2},
        )

    def test_the_patient_session_has_the_consent_gate_closed(self) -> None:
        session = ward_mechanics.patient_session(self._patient())
        self.assertFalse(session.consent)

    def test_the_party_may_read_the_patient_without_consent(self) -> None:
        patient = self._patient()
        session = ward_mechanics.patient_session(patient)
        session.reveal_aspect("the form was altered after she signed")
        self.assertIn("the form was altered after she signed", session.revealed_aspects)
        self.assertEqual(patient.aspects, ["a person who came in for treatment"])

    def test_the_party_may_not_change_the_patient_without_consent(self) -> None:
        patient = self._patient()
        session = ward_mechanics.patient_session(patient)
        with self.assertRaises(PsychosurgeryError):
            session.integrate_aspect("a person who was operated on without asking")
        self.assertEqual(patient.aspects, ["a person who came in for treatment"])

    def test_a_refused_write_logs_nothing(self) -> None:
        session = ward_mechanics.patient_session(self._patient())
        with self.assertRaises(PsychosurgeryError):
            session.integrate_aspect("a person who was operated on without asking")
        self.assertEqual(session.log, [])

    def test_the_case_declares_the_patient_consent_interest(self) -> None:
        """The case's own campaign must carry the consent interest the model enforces."""
        campaign = ubiquitous_maniacs.build_campaign()
        case = campaign.cases[ubiquitous_maniacs.CASE_ID]
        self.assertIn("patient consent", case.faction_interests)


class TestTheWitnessProjections(unittest.TestCase):
    """The two witnesses hold different layers, and the model never settles it."""

    def test_there_are_two_witness_projections(self) -> None:
        self.assertEqual(len(ward_mechanics.witness_projections()), 2)

    def test_both_witnesses_are_projected(self) -> None:
        for witness, session in ward_mechanics.witness_projections().items():
            with self.subTest(witness=witness):
                self.assertIs(session.status, ProjectionStatus.PROJECTED)

    def test_the_two_witnesses_disagree(self) -> None:
        """One believes it was a dream; the other that it was a construction."""
        first, second = list(ward_mechanics.witness_projections().values())
        self.assertNotEqual(first.hypotheses, second.hypotheses)

    def test_neither_witness_is_told_which_is_right(self) -> None:
        for session in ward_mechanics.witness_projections().values():
            with self.subTest(witness=session):
                # Every hypothesis stays alive: the fiction never settles the ontology.
                self.assertTrue(all(value > 0 for value in session.hypotheses.values()))

    def test_both_witnesses_saw_the_same_thing(self) -> None:
        """The disagreement is about the layer, not the event."""
        for session in ward_mechanics.witness_projections().values():
            with self.subTest(witness=session):
                self.assertTrue(
                    any(
                        "a second figure in the chair" in item
                        for item in session.known_information
                    ),
                    "both witnesses must have observed the same event",
                )


class TestTheWardContext(unittest.TestCase):
    """The records room's own properties decide how hard a psychical act is there."""

    def test_the_ward_context_is_harder_than_an_open_room(self) -> None:
        from strategy_game.rpg.psi import PsiActionContext

        open_room = PsiActionContext()
        self.assertLess(
            ward_mechanics.ward_context().trajectory_modifier,
            open_room.trajectory_modifier,
        )

    def test_a_rating_does_help(self) -> None:
        self.assertGreater(
            ward_mechanics.ward_context(psi_rating=4).trajectory_modifier,
            ward_mechanics.ward_context(psi_rating=0).trajectory_modifier,
        )

    def test_a_remote_perception_attempt_uses_the_engine_s_skills(self) -> None:
        viewer = Character(
            id="viewer",
            name="A viewer",
            aspects=[],
            skills={"INT": 3},
            tags=(Tag("competence", "REMOTE_VIEWER"),),
        )
        result = ward_mechanics.attempt_remote_perception(
            viewer, "the records room", rng=Random(3)
        )
        self.assertIn(result.skill, INDIVIDUAL_SKILL_NAMES)

    def test_a_character_without_the_capability_is_refused(self) -> None:
        plain = Character(id="plain", name="Plain", aspects=[], skills={"INT": 3})
        with self.assertRaises(SkillLayerError):
            ward_mechanics.attempt_remote_perception(
                plain, "the records room", rng=Random(3)
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
