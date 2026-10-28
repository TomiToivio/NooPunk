"""Tests for the conditions model (#698, D46-D48) and the falsification case (#699)."""
import inspect
import unittest

from src.rules import mental_load
from src.rules.mental_load import (
    CharacterMind,
    Condition,
    Layer,
    MentalLoadError,
    ParadigmShock,
    WorldviewState,
)

SHOCK = ParadigmShock(
    id="shock:nhi-contact",
    claim="The government disclosed non-human contact.",
    contradicts="Non-human contact is a conspiracy theory.",
    source="test fixture",
)


class StructureTest(unittest.TestCase):
    def test_a_new_character_holds_a_belief_as_received(self):
        mind = CharacterMind()
        self.assertIs(mind.state_of(SHOCK.contradicts), WorldviewState.RECEIVED)

    def test_an_event_is_not_a_condition(self):
        with self.assertRaises(MentalLoadError):
            Condition(id="x", layer=Layer.EVENT, constrains="nothing")

    def test_a_condition_needs_an_id(self):
        with self.assertRaises(MentalLoadError):
            Condition(id="", layer=Layer.PERSISTENT, constrains="something")


class DecisionTest(unittest.TestCase):
    def test_a_shock_offers_two_different_costs(self):
        choice = CharacterMind().present(SHOCK)
        self.assertNotEqual(choice.accept.constrains, choice.hold.constrains)
        self.assertNotEqual(choice.accept.id, choice.hold.id)

    def test_accepting_the_reframe_reframes_the_belief(self):
        mind = CharacterMind()
        state = mind.apply_choice(mind.present(SHOCK), accept=True)
        self.assertIs(state, WorldviewState.REFRAMED)
        self.assertIs(mind.state_of(SHOCK.contradicts), WorldviewState.REFRAMED)

    def test_holding_the_belief_fractures_it(self):
        mind = CharacterMind()
        state = mind.apply_choice(mind.present(SHOCK), accept=False)
        self.assertIs(state, WorldviewState.FRACTURED)

    def test_an_integrated_belief_is_no_longer_destabilised_by_the_same_shock(self):
        mind = CharacterMind()
        mind.apply_choice(mind.present(SHOCK), accept=True)
        mind.integrate(SHOCK.contradicts)
        with self.assertRaises(MentalLoadError):
            mind.present(SHOCK)

    def test_integration_requires_a_reframe_first(self):
        with self.assertRaises(MentalLoadError):
            CharacterMind().integrate(SHOCK.contradicts)


class NoRollInvariantTest(unittest.TestCase):
    """D48 is structural: the module must have no way to decide belief from a die."""

    def test_no_public_function_takes_a_roll(self):
        for name, member in inspect.getmembers(mental_load, inspect.isfunction):
            if name.startswith("_") or member.__module__ != mental_load.__name__:
                continue
            params = set(inspect.signature(member).parameters)
            self.assertFalse(
                params & {"roll", "die", "dice", "rng", "random"},
                f"{name} takes randomness; D48 forbids deciding belief from a roll",
            )

    def test_apply_choice_refuses_a_non_boolean_decision(self):
        mind = CharacterMind()
        choice = mind.present(SHOCK)
        with self.assertRaises(MentalLoadError):
            mind.apply_choice(choice, accept=None)  # type: ignore[arg-type]


class FalsificationCaseTest(unittest.TestCase):
    """#699: the two branches must differ in kind, not only in number."""

    def _play(self, *, accept: bool):
        mind = CharacterMind()
        shock = ParadigmShock(
            id="case:xenolinguistics",
            claim="The transcripts are a language, not interference.",
            contradicts="The recordings are instrumental artefacts.",
        )
        state = mind.apply_choice(mind.present(shock), accept=accept)
        return mind, state

    def test_the_two_branches_constrain_different_actions(self):
        accept_mind, accept_state = self._play(accept=True)
        hold_mind, hold_state = self._play(accept=False)
        self.assertNotEqual(accept_state, hold_state)
        self.assertNotEqual(
            accept_mind.conditions[-1].constrains,
            hold_mind.conditions[-1].constrains,
            "if both branches produce the same constraint, the choice is not real",
        )

    def test_the_choice_is_what_determines_the_outcome_not_a_die(self):
        """The falsification criterion: identical inputs, different decisions, different states."""
        _, first = self._play(accept=True)
        _, second = self._play(accept=True)
        self.assertEqual(first, second)
        self.assertNotEqual(first, self._play(accept=False)[1])


if __name__ == "__main__":
    unittest.main()
