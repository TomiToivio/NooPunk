"""Runtime contracts for the first-contact translation model (issue #348).

Executable behaviour only: the communication-mode set, the ladder's direction, the lexicon's refusal to
collapse ambiguity, the machine-translator warning, and session round-tripping. No assertion about
entity prose or about what an interpretation *means* — the issue says a successful interpretation
"can unlock diplomacy, treaties, research and ideology signifiers", and that consequence belongs to the
strategy layer, not here.

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game.codex import (  # noqa: E402
    COMMUNICATION_MODES,
    LOAD_BEARING_SIGNIFIERS,
    TRANSLATION_LADDER,
    CodexError,
    CommunicationMode,
    Confidence,
    ContactAttempt,
    ContactSession,
    Lexicon,
    LexiconEntry,
    Meaning,
    TranslationStage,
    machine_candidate,
    signal_variant,
)


class CommunicationModeTests(unittest.TestCase):
    def test_the_issue_s_modes_are_all_declared(self):
        for name in ("spoken", "gesture", "pheromone", "color_light", "electromagnetic",
                     "written_logogram", "chemical_gradient", "network_pulse", "telepathy",
                     "symbolic_vision", "social_embedded", "silence"):
            with self.subTest(name=name):
                self.assertIn(name, COMMUNICATION_MODES)

    def test_silence_is_a_mode_not_the_absence_of_one(self):
        self.assertIn(CommunicationMode.SILENCE.value, COMMUNICATION_MODES)

    def test_the_ladder_has_the_six_rungs_in_order(self):
        self.assertEqual([stage.value for stage in TRANSLATION_LADDER],
                         ["detect_signal", "infer_agents", "shared_referents",
                          "propose_meanings", "test_under_uncertainty", "negotiate_intent"])


class MeaningTests(unittest.TestCase):
    def test_a_candidate_needs_text(self):
        with self.assertRaises(CodexError):
            Meaning(text="  ")

    def test_confidence_is_a_label_not_a_probability(self):
        self.assertEqual({c.value for c in Confidence}, {"low", "medium", "high"})
        self.assertNotIsInstance(Meaning("x").confidence.value, float)

    def test_a_meaning_round_trips(self):
        meaning = Meaning("a reading", Confidence.MEDIUM, "a note")
        self.assertEqual(Meaning.from_dict(json.loads(json.dumps(meaning.to_dict()))), meaning)

    def test_an_unrecognised_confidence_raises(self):
        with self.assertRaises(CodexError):
            Meaning.from_dict({"text": "x", "confidence": "certain"})


class LexiconTests(unittest.TestCase):
    def test_a_lexicon_entry_needs_a_sign(self):
        with self.assertRaises(CodexError):
            LexiconEntry(sign=" ")

    def test_proposing_a_sign_creates_it_and_keeps_every_reading(self):
        lexicon = Lexicon()
        lexicon.propose("gift-or-weapon", "a gift", Confidence.LOW)
        lexicon.propose("gift-or-weapon", "a weapon", Confidence.LOW)
        self.assertEqual([m.text for m in lexicon.candidates("gift-or-weapon")],
                         ["a gift", "a weapon"])
        self.assertTrue(lexicon.entries["gift-or-weapon"].is_ambiguous)

    def test_there_is_no_method_that_returns_a_single_translation(self):
        """Ambiguity is the dramatic content, so the API cannot silently resolve it."""
        lexicon = Lexicon()
        lexicon.propose("s", "a", Confidence.LOW)
        lexicon.propose("s", "b", Confidence.LOW)
        self.assertGreater(len(lexicon.candidates("s")), 1)
        for name in ("translate", "translation", "meaning", "best"):
            self.assertFalse(hasattr(lexicon, name),
                             f"Lexicon.{name} would collapse the ambiguity the model exists to keep")

    def test_a_single_reading_is_not_ambiguous(self):
        lexicon = Lexicon()
        lexicon.propose("s", "only", Confidence.HIGH)
        self.assertFalse(lexicon.entries["s"].is_ambiguous)

    def test_an_unknown_sign_has_no_candidates_rather_than_a_guess(self):
        self.assertEqual(Lexicon().candidates("nothing"), ())

    def test_ambiguous_signs_are_listed(self):
        lexicon = Lexicon()
        lexicon.propose("a", "one", Confidence.LOW)
        lexicon.propose("a", "two", Confidence.LOW)
        lexicon.propose("b", "only", Confidence.HIGH)
        self.assertEqual(lexicon.ambiguous_signs(), ("a",))

    def test_a_lexicon_round_trips(self):
        lexicon = Lexicon()
        lexicon.propose("s", "x", Confidence.LOW, "note")
        restored = Lexicon.from_dict(json.loads(json.dumps(lexicon.to_dict())))
        self.assertEqual(restored.to_dict(), lexicon.to_dict())


class MachineCandidateTests(unittest.TestCase):
    def test_a_machine_reading_is_marked_as_a_guess(self):
        """'Even a machine translator/AGI can confidently hallucinate and break diplomacy.'"""
        candidate = machine_candidate("we come in peace")
        self.assertIs(candidate.confidence, Confidence.LOW)
        self.assertIn("machine", candidate.note.lower())
        self.assertIn("wrong", candidate.note.lower())

    def test_a_machine_reading_can_be_kept_beside_a_better_one(self):
        lexicon = Lexicon()
        lexicon.add(LexiconEntry("salutation", meanings=(machine_candidate("a greeting"),)))
        lexicon.propose("salutation", "a demand for submission", Confidence.MEDIUM)
        self.assertEqual(len(lexicon.candidates("salutation")), 2)


class ContactSessionTests(unittest.TestCase):
    def _session(self) -> ContactSession:
        return ContactSession(
            entity_id="e1",
            modes=(CommunicationMode.COLOR_LIGHT, CommunicationMode.TELEPATHY),
        )

    def test_a_session_needs_the_entity_it_is_about(self):
        with self.assertRaises(CodexError):
            ContactSession(entity_id=" ")

    def test_the_ladder_moves_forward_only(self):
        session = self._session()
        session.advance_to(TranslationStage.INFER_AGENTS)
        self.assertIs(session.stage, TranslationStage.INFER_AGENTS)
        with self.assertRaises(CodexError):
            session.advance_to(TranslationStage.DETECT_SIGNAL)

    def test_advancing_to_the_same_rung_is_allowed(self):
        session = self._session()
        self.assertIs(session.advance_to(TranslationStage.DETECT_SIGNAL),
                      TranslationStage.DETECT_SIGNAL)

    def test_the_stage_index_follows_the_ladder(self):
        session = self._session()
        self.assertEqual(session.stage_index, 0)
        session.advance_to(TranslationStage.NEGOTIATE_INTENT)
        self.assertEqual(session.stage_index, len(TRANSLATION_LADDER) - 1)

    def test_a_proposal_records_the_stage_it_was_made_at(self):
        session = self._session()
        session.advance_to(TranslationStage.PROPOSE_MEANINGS)
        attempt = session.propose("we", "the speaker and its whole commune", Confidence.MEDIUM,
                                  method="compared two encounters", outcome="the interpreter revised",
                                  seed=7)
        self.assertIs(attempt.stage, TranslationStage.PROPOSE_MEANINGS)
        self.assertEqual(session.attempts[0].seed, 7)

    def test_competing_readings_survive_a_proposal(self):
        session = self._session()
        session.advance_to(TranslationStage.PROPOSE_MEANINGS)
        session.propose("harvest", "a harvest of grain", Confidence.LOW)
        session.propose("harvest", "a harvest of minds", Confidence.LOW)
        self.assertEqual(len(session.meanings_for("harvest")), 2)
        self.assertEqual(session.unresolved_signs, ("harvest",))

    def test_one_drone_is_not_the_swarm(self):
        """The issue's own example of a species-specific misunderstanding, as recorded data."""
        session = self._session()
        session.advance_to(TranslationStage.TEST_UNDER_UNCERTAINTY)
        session.propose("i", "one body", Confidence.LOW, outcome="the sphere did not answer alone")
        session.propose("i", "one node of a planetary swarm", Confidence.LOW,
                        outcome="a second sphere completed the sentence")
        self.assertTrue(session.lexicon.entries["i"].is_ambiguous)

    def test_readiness_is_a_query_that_unlocks_nothing(self):
        session = self._session()
        self.assertFalse(session.is_ready_to_negotiate())
        session.advance_to(TranslationStage.NEGOTIATE_INTENT)
        self.assertFalse(session.is_ready_to_negotiate(), "an empty lexicon is not ready")
        session.propose("x", "a reading", Confidence.LOW)
        self.assertTrue(session.is_ready_to_negotiate())

    def test_a_session_round_trips(self):
        session = self._session()
        session.advance_to(TranslationStage.PROPOSE_MEANINGS)
        session.propose("s", "a", Confidence.LOW, seed=3)
        restored = ContactSession.from_json(session.to_json())
        self.assertEqual(restored.to_json(), session.to_json())
        self.assertEqual(restored.modes, session.modes)

    def test_an_unrecognised_mode_raises_rather_than_being_dropped(self):
        with self.assertRaises(CodexError):
            ContactSession.from_dict({"entity_id": "e1", "modes": ["telepathy", "bogus"]})

    def test_an_attempt_round_trips(self):
        attempt = ContactAttempt(TranslationStage.SHARED_REFERENTS, "s", "a", Confidence.LOW,
                                 method="m", outcome="o", seed=1)
        self.assertEqual(ContactAttempt.from_dict(json.loads(json.dumps(attempt.to_dict()))), attempt)


class SignalVariantTests(unittest.TestCase):
    def test_the_opening_mode_is_reproducible_from_a_seed(self):
        modes = (CommunicationMode.SPOKEN, CommunicationMode.COLOR_LIGHT)
        self.assertEqual(signal_variant(modes, seed=5), signal_variant(modes, seed=5))

    def test_the_variant_is_one_of_the_encounter_s_modes(self):
        modes = (CommunicationMode.SPOKEN, CommunicationMode.COLOR_LIGHT)
        self.assertIn(signal_variant(modes, seed=1), {m.value for m in modes})

    def test_a_session_with_no_mode_cannot_present_a_signal(self):
        with self.assertRaises(CodexError):
            signal_variant((), seed=1)


class LoadBearingSignifierTests(unittest.TestCase):
    """The issue's pragmatics signifiers ("gift", "we"...) as a declared, non-invented set."""

    def test_the_issue_s_pragmatic_signifiers_are_declared(self):
        for name in ("we", "gift", "weapon", "voluntary", "service", "harvest", "ownership",
                     "individual"):
            with self.subTest(name=name):
                self.assertIn(name, LOAD_BEARING_SIGNIFIERS)

    def test_the_signifier_set_is_the_issue_s_own_example_list(self):
        self.assertEqual(
            sorted(LOAD_BEARING_SIGNIFIERS),
            ["gift", "harvest", "individual", "ownership", "service", "voluntary", "we", "weapon"],
        )


class MisunderstandingIsAStateTests(unittest.TestCase):
    """A tested-but-wrong reading is a state the session keeps, not a failure that resets it."""

    def test_a_wrong_reading_does_not_move_the_ladder_backwards(self):
        session = ContactSession(entity_id="e1", modes=(CommunicationMode.SILENCE,))
        session.advance_to(TranslationStage.TEST_UNDER_UNCERTAINTY)
        session.propose("gift", "a weapon", Confidence.LOW, outcome="the reading was falsified")
        # The falsified reading stays recorded beside the surviving ones; progress is monotonic.
        self.assertIs(session.stage, TranslationStage.TEST_UNDER_UNCERTAINTY)
        self.assertEqual([m.text for m in session.meanings_for("gift")], ["a weapon"])
        session.propose("gift", "a trade good", Confidence.MEDIUM, outcome="verified on a second visit")
        self.assertEqual(len(session.meanings_for("gift")), 2)
        with self.assertRaises(CodexError):
            session.advance_to(TranslationStage.DETECT_SIGNAL)


if __name__ == "__main__":
    unittest.main()
