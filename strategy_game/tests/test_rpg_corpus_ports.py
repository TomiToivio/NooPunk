"""The corpus-derived RPG modules, ported onto the live engine.

Three modules were ported from the *Ubiquitous Maniacs* corpus onto this repository's engine
so that the corpus's material and the live RPG are **one** system rather than two parallel
ones:

* :mod:`strategy_game.rpg.projection` — psyche projection and what it costs;
* :mod:`strategy_game.rpg.psychosurgery` — consent-gated changes to a patient;
* :mod:`strategy_game.rpg.psi` — PSI as trajectory steering, on the one Fate resolver.

What is pinned here is that each port **behaves like the engine it now lives in**:

* each introduces **no new dice, no new skill, no new outcome rung and no second resolver** —
  a PSI check is a check like any other, on the same kernel;
* the PSI port resolves against the engine's **six** individual skills and gates capabilities on
  the existing tag vocabulary, so the corpus's seven-attribute, TF-named skill system does not
  reappear in the live tree;
* the psychosurgery port's **consent gate** refuses every write and permits every read, and it
  refuses *before* any state changes;
* the projection port is **deterministic** and never consults a random number.

Nothing here asserts a difficulty, an ending distribution or an author decision. Every number
in this file is a fixture that makes one contract observable.
"""
from __future__ import annotations

import unittest
from random import Random

from strategy_game.characters import Tag
from strategy_game.rpg.fate import Action, Character, Outcome
from strategy_game.rpg.projection import (
    ProjectionLayer,
    ProjectionSession,
    ProjectionStatus,
)
from strategy_game.rpg.psi import (
    PsiActionContext,
    PsiMode,
    belief_bonus,
    consensus_modifier,
    resolve_psi_action,
)
from strategy_game.rpg.psychosurgery import PsychosurgeryError, PsychosurgerySession
from strategy_game.rpg.skills import INDIVIDUAL_SKILL_NAMES


def _character(
    identifier: str = "actor",
    *,
    name: str = "An actor",
    aspects: list[str] | None = None,
    skills: dict[str, int] | None = None,
    tags: tuple[Tag, ...] = (),
) -> Character:
    return Character(
        id=identifier,
        name=name,
        aspects=list(aspects or []),
        skills=dict(skills or {"INT": 3, "SAV": 2, "WIL": 3, "COG": 2}),
        tags=tags,
    )


class TestProjection(unittest.TestCase):
    """The projection model charges and tracks; it never rolls and never decides."""

    def test_a_projection_starts_embodied(self) -> None:
        session = ProjectionSession()
        self.assertIs(session.status, ProjectionStatus.EMBODIED)

    def test_entering_requires_an_embodied_state(self) -> None:
        session = ProjectionSession()
        session.enter()
        with self.assertRaises(ValueError):
            session.enter()

    def test_actions_require_an_active_projection(self) -> None:
        session = ProjectionSession()
        for call in (
            lambda: session.observe("clue"),
            lambda: session.traverse(1),
            lambda: session.resonate("other"),
            lambda: session.manifest("witness"),
            lambda: session.return_to_body(),
        ):
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()

    def test_the_model_is_deterministic(self) -> None:
        """A projection must be replayable: the same calls give the same state."""
        first = ProjectionSession()
        second = ProjectionSession()
        for session in (first, second):
            session.enter(preparation=5, anchor_support=5)
            session.observe("clue", {ProjectionLayer.NOETIC: 10})
            session.traverse(2)
            session.manifest("witness")
            session.return_to_body(assistance=10)
        self.assertEqual(first.inspect_state(), second.inspect_state())

    def test_the_four_hypotheses_are_never_resolved(self) -> None:
        """The model must not settle what the experience *was*."""
        session = ProjectionSession()
        session.enter()
        session.observe("clue", {ProjectionLayer.NOETIC: 40})
        state = session.inspect_state()
        hypotheses = state["hypotheses"]
        assert isinstance(hypotheses, dict)
        self.assertEqual(set(hypotheses), {layer.value for layer in ProjectionLayer})
        self.assertTrue(
            any(value > 0 for value in hypotheses.values()),
            "the model must keep every hypothesis alive",
        )

    def test_the_hypothesis_weights_sum_to_one_hundred(self) -> None:
        session = ProjectionSession()
        session.enter()
        session.observe("clue", {ProjectionLayer.DREAM: 15, ProjectionLayer.NOETIC: 5})
        state = session.inspect_state()
        hypotheses = state["hypotheses"]
        assert isinstance(hypotheses, dict)
        self.assertEqual(sum(hypotheses.values()), 100)

    def test_coherence_and_anchor_are_charged(self) -> None:
        session = ProjectionSession()
        session.enter(preparation=0, anchor_support=0)
        before = (session.coherence, session.anchor)
        session.traverse(2)
        self.assertLess(session.coherence, before[0])
        self.assertLess(session.anchor, before[1])

    def test_running_a_resource_to_zero_loses_the_projection(self) -> None:
        session = ProjectionSession()
        session.enter(preparation=0, anchor_support=0)
        # Each observation costs 2 coherence, so the session runs out after 35 of them.
        # The loop stops as soon as the session is no longer projected: once a resource
        # hits zero the session is LOST, and a lost session refuses further actions.
        for _ in range(40):
            if session.status is not ProjectionStatus.PROJECTED:
                break
            session.observe("clue")
        self.assertIs(session.status, ProjectionStatus.LOST)
        self.assertIn("projection_integrity_lost", session.known_information)

    def test_a_distant_projection_is_harder_to_leave(self) -> None:
        """The return threshold grows with distance and with a thin anchor.

        The threshold is ``distance * 3 + max(0, 30 - anchor)``, so a projection that has
        travelled far cannot be abandoned with the coherence a short one still has.
        """
        near = ProjectionSession()
        near.enter(preparation=0, anchor_support=0)
        near.traverse(1)
        far = ProjectionSession()
        far.enter(preparation=0, anchor_support=0)
        far.traverse(20)
        near.return_to_body()
        far.return_to_body()
        self.assertIs(near.status, ProjectionStatus.RETURNED)
        self.assertIs(far.status, ProjectionStatus.LOST)

    def test_the_inspection_is_plain_data(self) -> None:
        session = ProjectionSession()
        session.enter()
        state = session.inspect_state()
        self.assertIsInstance(state, dict)
        self.assertEqual(state["status"], "projected")
        for value in state.values():
            self.assertIsInstance(value, (str, int, list, dict))


class TestPsychosurgery(unittest.TestCase):
    """The consent gate is the module's whole point."""

    def test_a_read_is_permitted_without_consent(self) -> None:
        patient = _character("patient")
        session = PsychosurgerySession(patient=patient, operator="Dr. Dahl", consent=False)
        session.reveal_aspect("something was altered")
        self.assertIn("something was altered", session.revealed_aspects)

    def test_a_write_is_refused_without_consent(self) -> None:
        patient = _character("patient")
        session = PsychosurgerySession(patient=patient, operator="Dr. Dahl", consent=False)
        with self.assertRaises(PsychosurgeryError):
            session.integrate_aspect("a person who was operated on without asking")
        self.assertNotIn(
            "a person who was operated on without asking",
            patient.aspects,
            "a refused write must not change the sheet",
        )

    def test_treating_a_consequence_is_refused_without_consent(self) -> None:
        patient = _character("patient")
        session = PsychosurgerySession(patient=patient, operator="Dr. Dahl", consent=False)
        with self.assertRaises(PsychosurgeryError):
            session.heal_consequence("anything")
        self.assertEqual(session.log, [])

    def test_resonance_is_refused_without_consent(self) -> None:
        patient = _character("patient")
        session = PsychosurgerySession(patient=patient, operator="Dr. Dahl", consent=False)
        with self.assertRaises(PsychosurgeryError):
            session.resonate("someone-else")

    def test_a_write_is_permitted_with_consent(self) -> None:
        patient = _character("patient")
        session = PsychosurgerySession(patient=patient, operator="Dr. Dahl", consent=True)
        session.integrate_aspect("a person who chose this")
        self.assertIn("a person who chose this", patient.aspects)

    def test_a_refused_write_logs_nothing(self) -> None:
        """The log is a record of what was done. A refused write was not done."""
        patient = _character("patient")
        session = PsychosurgerySession(patient=patient, operator="Dr. Dahl", consent=False)
        with self.assertRaises(PsychosurgeryError):
            session.integrate_aspect("a person who was operated on without asking")
        self.assertEqual(session.log, [])

    def test_a_condition_is_recorded(self) -> None:
        patient = _character("patient")
        session = PsychosurgerySession(patient=patient, operator="Dr. Dahl", consent=False)
        session.add_condition("post-procedural disorientation")
        self.assertIn("post-procedural disorientation", patient.statuses)

    def test_everything_done_is_logged(self) -> None:
        patient = _character("patient")
        session = PsychosurgerySession(patient=patient, operator="Dr. Dahl", consent=True)
        session.reveal_aspect("a revealed thing")
        session.integrate_aspect("an integrated thing")
        session.add_condition("a condition")
        self.assertEqual(len(session.log), 3)
        self.assertTrue(session.log[0].startswith("revealed:"))
        self.assertTrue(session.log[1].startswith("integrated:"))
        self.assertTrue(session.log[2].startswith("condition:"))


class TestPsi(unittest.TestCase):
    """PSI is trajectory steering on the one resolver, not a second mechanic."""

    def test_every_mode_resolves_against_an_engine_skill(self) -> None:
        """The corpus's seven-attribute, TF-named skill system must not reappear.

        A mode whose fiction needs a capability is refused by the engine's own gate; that
        refusal is a *capability* result, not a skill error, and the modes that are not gated
        must all resolve against one of the six.
        """
        from strategy_game.rpg.skills import SkillLayerError

        actor = _character()
        for mode in PsiMode:
            with self.subTest(mode=mode):
                try:
                    result = resolve_psi_action(
                        actor, "target", mode, 2, rng=Random(1)
                    )
                except SkillLayerError:
                    # Refused for a capability, which is the engine's own rule.
                    continue
                self.assertIn(result.skill, INDIVIDUAL_SKILL_NAMES)

    def test_the_skill_is_one_of_the_six(self) -> None:
        self.assertEqual(len(INDIVIDUAL_SKILL_NAMES), 6)

    def test_a_capability_is_refused_before_any_dice(self) -> None:
        """The engine's rule: a gated action cannot be rolled at a lower rating."""
        actor = _character("no-capability")
        with self.assertRaises(Exception) as caught:
            resolve_psi_action(
                actor, "target", PsiMode.REMOTE_PERCEPTION, 2, rng=Random(1)
            )
        self.assertIn("REMOTE_VIEWER", str(caught.exception))

    def test_a_capability_holder_may_act(self) -> None:
        actor = _character("viewer", tags=(Tag("competence", "REMOTE_VIEWER"),))
        result = resolve_psi_action(
            actor, "target", PsiMode.REMOTE_PERCEPTION, 2, rng=Random(1)
        )
        self.assertIsInstance(result.outcome, Outcome)

    def test_the_resolver_is_the_engine_s_resolver(self) -> None:
        """The same dice, the same shifts, the same outcomes as a plain Fate check."""
        actor = _character()
        result = resolve_psi_action(actor, "target", PsiMode.INTUITION, 2, rng=Random(11))
        from strategy_game.rpg.fate import resolve

        plain = resolve(Action.CREATE_ADVANTAGE, 3, 2, rng=Random(11))
        self.assertEqual(result.dice, plain.dice)
        self.assertEqual(result.shifts, plain.shifts)
        self.assertIs(result.outcome, plain.outcome)

    def test_a_pinned_roll_is_honoured(self) -> None:
        actor = _character()
        result = resolve_psi_action(
            actor, "target", PsiMode.INTUITION, 2, rng=Random(1), roll=4
        )
        self.assertEqual(result.shifts, 4 + 3 - 2)

    def test_the_situational_modifier_moves_the_roll(self) -> None:
        actor = _character()
        easy = resolve_psi_action(
            actor, "t", PsiMode.INTUITION, 3, rng=Random(7),
            context=PsiActionContext(corridor_strength=4),
        )
        hard = resolve_psi_action(
            actor, "t", PsiMode.INTUITION, 3, rng=Random(7),
            context=PsiActionContext(semantic_distance=4, local_noise=4),
        )
        self.assertGreater(easy.total, hard.total)

    def test_the_modifier_is_clamped(self) -> None:
        context = PsiActionContext(
            corridor_strength=4, bifurcation_openness=4, affective_salience=4,
            composite_coherence=4, semantic_distance=4, instrumentality=4, local_noise=4,
        )
        self.assertGreaterEqual(context.trajectory_modifier, -4)
        self.assertLessEqual(context.trajectory_modifier, 4)

    def test_consensus_is_capped_symmetrically(self) -> None:
        self.assertEqual(consensus_modifier(50, 0), 3)
        self.assertEqual(consensus_modifier(0, 50), -3)
        self.assertEqual(consensus_modifier(0, 0), 0)

    def test_a_belief_is_a_bonus_and_not_a_capability(self) -> None:
        """A belief helps a little; it never enables."""
        actor = _character("believer", tags=(Tag("belief", "intuition"),))
        self.assertEqual(belief_bonus(actor, "intuition"), 1)
        self.assertEqual(belief_bonus(actor, "telepathy"), 0)
        from strategy_game.rpg.skills import capabilities_of

        self.assertNotIn("intuition", capabilities_of(actor))

    def test_a_belief_moves_the_roll(self) -> None:
        plain = _character("plain")
        believer = _character("believer", tags=(Tag("belief", "intuition"),))
        a = resolve_psi_action(plain, "t", PsiMode.INTUITION, 3, rng=Random(7))
        b = resolve_psi_action(believer, "t", PsiMode.INTUITION, 3, rng=Random(7))
        self.assertEqual(b.total - a.total, 1)

    def test_the_pressure_depends_on_the_target(self) -> None:
        """An instrumental target is cheap to touch; a person is not."""
        actor = _character()
        machine = resolve_psi_action(
            actor, "t", PsiMode.INTUITION, 1, rng=Random(1),
            context=PsiActionContext(instrumentality=4),
        )
        person = resolve_psi_action(
            actor, "t", PsiMode.INTUITION, 1, rng=Random(1),
            context=PsiActionContext(instrumentality=0),
        )
        self.assertGreaterEqual(
            machine.pressure.noetic_trace, person.pressure.noetic_trace
        )

    def test_a_cross_layer_effect_needs_consent_to_apply(self) -> None:
        from strategy_game.rpg.psi import CrossLayerEffect

        effect = CrossLayerEffect(
            source_layer="astral", target_layer="physical", interface="noosphere",
            trigger="psi", consent_required=True, consent=False,
        )
        self.assertFalse(effect.permitted)
        allowed = CrossLayerEffect(
            source_layer="astral", target_layer="physical", interface="noosphere",
            trigger="psi", consent_required=True, consent=True,
        )
        self.assertTrue(allowed.permitted)

    def test_a_failed_act_carries_no_cross_layer_effect(self) -> None:
        from strategy_game.rpg.psi import CrossLayerEffect

        actor = _character()
        effect = CrossLayerEffect(
            source_layer="astral", target_layer="physical", interface="noosphere",
            trigger="psi", consent_required=True, consent=True,
        )
        result = resolve_psi_action(
            actor, "t", PsiMode.INTUITION, 12, rng=Random(1),
            cross_layer_effects=(effect,),
        )
        self.assertFalse(result.succeeded)
        self.assertEqual(result.applicable_cross_layer_effects, ())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
