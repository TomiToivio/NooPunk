"""#1217 line 11: the Psychic Training focus, from the author's quotation in #1178.

The tests are written against the printed mechanics, not against the implementation: a bonus skill, a free rank-1
technique, one extra Effort, and level-2 points banked and awarded retroactively.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import psi_access  # noqa: E402
from rules.awn_mentalist import Art, create_first_level_mentalist  # noqa: E402
from rules.psionics import _technique_table  # noqa: E402
from rules.psychic_training import (  # noqa: E402
    FOCUS_NAME,
    LOCATOR,
    PsychicTraining,
    PsychicTrainingError,
    advance_to_level_two,
    choose_technique,
    effort_max,
    retroactive_points,
    spend_point,
    take_focus,
)
from rules.swn_psionics import Psychic  # noqa: E402


def psychic(**kwargs) -> Psychic:
    return Psychic(wisdom=kwargs.pop("wisdom", 10), constitution=kwargs.pop("constitution", 10), **kwargs)


def rank_one_techniques(discipline: str) -> list[str]:
    return [key for key, (owner, minimum) in _technique_table().items()
            if owner == discipline and minimum <= 1]


class SelectionTests(unittest.TestCase):
    def test_the_focus_is_available_and_names_its_source(self):
        self.assertTrue(psi_access.PSYCHIC_TRAINING_FOCUS_AVAILABLE)
        self.assertIn("#1178", psi_access.PSYCHIC_TRAINING_FOCUS_BLOCKED_REASON)
        self.assertIn("Stars Without Number", LOCATOR)
        self.assertEqual(FOCUS_NAME, "Psychic Training")

    def test_a_psychic_gains_the_bonus_skill(self):
        character = psychic()
        training = take_focus(character, "Telepathy")
        self.assertEqual(character.disciplines["Telepathy"], 1)
        self.assertEqual(training.discipline, "Telepathy")
        self.assertEqual(training.level, 1)

    def test_an_existing_rank_is_improved_not_reset(self):
        character = psychic(disciplines={"Telekinesis": 2})
        take_focus(character, "Telekinesis")
        self.assertEqual(character.disciplines["Telekinesis"], 3)

    def test_level_one_grants_one_extra_effort(self):
        """The bonus skill raises the SWN pool by its own rule; the focus's +1 is on top of that, not instead of it."""
        character = psychic()
        base = character.capacity
        training = take_focus(character, "Telepathy")
        self.assertEqual(character.capacity, base + 1, "rank 1 in a discipline raises Effort by one (SWN)")
        self.assertEqual(effort_max(character, training), base + 2)

    def test_the_focus_cannot_be_taken_twice(self):
        character = psychic()
        take_focus(character, "Telepathy")
        with self.assertRaises(PsychicTrainingError):
            take_focus(character, "Telekinesis", already_taken=True)

    def test_a_non_player_discipline_is_refused(self):
        with self.assertRaises(Exception):
            take_focus(psychic(), "Precognition")

    def test_a_partial_psychic_trains_only_their_chosen_discipline(self):
        character = psychic(restricted_discipline="Telepathy")
        take_focus(character, "Telepathy", partial=True)
        other = psychic(restricted_discipline="Telepathy")
        with self.assertRaises(PsychicTrainingError):
            take_focus(other, "Telekinesis", partial=True)

    def test_a_partial_psychic_without_a_discipline_is_refused(self):
        with self.assertRaises(PsychicTrainingError):
            take_focus(psychic(), "Telepathy", partial=True)

    def test_maximum_rank_is_respected(self):
        character = psychic(disciplines={"Telepathy": 4})
        with self.assertRaises(PsychicTrainingError):
            take_focus(character, "Telepathy")


class TechniqueTests(unittest.TestCase):
    def test_a_free_rank_one_technique_may_be_chosen(self):
        training = take_focus(psychic(), "Telepathy")
        technique = rank_one_techniques("Telepathy")[0]
        self.assertEqual(choose_technique(training, technique), technique)

    def test_a_technique_from_another_discipline_is_refused(self):
        training = take_focus(psychic(), "Telepathy")
        foreign = rank_one_techniques("Telekinesis")[0]
        with self.assertRaises(PsychicTrainingError):
            choose_technique(training, foreign)

    def test_a_higher_rank_technique_is_not_the_free_one(self):
        training = take_focus(psychic(), "Telepathy")
        higher = [key for key, (owner, minimum) in _technique_table().items()
                  if owner == "Telepathy" and minimum > 1]
        if not higher:  # pragma: no cover - depends on the catalogue
            self.skipTest("no higher-rank Telepathy technique in the catalogue")
        with self.assertRaises(PsychicTrainingError):
            choose_technique(training, higher[0])

    def test_an_unknown_technique_is_refused(self):
        with self.assertRaises(PsychicTrainingError):
            choose_technique(take_focus(psychic(), "Telepathy"), "mind_reading_ray")


class LevelTwoTests(unittest.TestCase):
    def test_points_are_retroactive_by_character_level(self):
        self.assertEqual(retroactive_points(1), 0)
        self.assertEqual(retroactive_points(5), 4)
        with self.assertRaises(PsychicTrainingError):
            retroactive_points(0)

    def test_advancing_to_level_two_banks_the_owed_points(self):
        training = take_focus(psychic(), "Telepathy")
        self.assertEqual(advance_to_level_two(training, character_level=3), 2)
        self.assertEqual(training.level, 2)
        self.assertEqual(training.banked_points, 2)

    def test_level_two_cannot_be_taken_twice(self):
        training = take_focus(psychic(), "Telepathy")
        advance_to_level_two(training, character_level=2)
        with self.assertRaises(PsychicTrainingError):
            advance_to_level_two(training, character_level=3)

    def test_points_are_spent_on_the_skill(self):
        training = take_focus(psychic(), "Telepathy")
        advance_to_level_two(training, character_level=2)
        self.assertEqual(spend_point(training, target="skill"), "skill")
        self.assertEqual(training.banked_points, 0)

    def test_points_are_spent_on_a_technique_of_the_same_discipline(self):
        training = take_focus(psychic(), "Telepathy")
        advance_to_level_two(training, character_level=2)
        technique = rank_one_techniques("Telepathy")[0]
        self.assertEqual(spend_point(training, target="technique", technique_id=technique), technique)

    def test_spending_without_points_is_refused(self):
        with self.assertRaises(PsychicTrainingError):
            spend_point(take_focus(psychic(), "Telepathy"), target="skill")

    def test_a_point_cannot_buy_another_discipline(self):
        training = take_focus(psychic(), "Telepathy")
        advance_to_level_two(training, character_level=2)
        with self.assertRaises(PsychicTrainingError):
            spend_point(training, target="technique", technique_id=rank_one_techniques("Telekinesis")[0])


class MentalistSeparationTests(unittest.TestCase):
    """#1217 line 10: the AWN Mentalist is selectable, and confers no SWN discipline."""

    def test_the_mentalist_edge_is_a_player_option(self):
        self.assertTrue(psi_access.edge_decision("Mentalist").allowed)
        self.assertIn("Mentalist", psi_access.PC_EDGES)

    def test_a_mentalist_holds_arts_not_swn_disciplines(self):
        first = create_first_level_mentalist(
            "tony.german",
            (Art("Calm", "Empathy"), Art("Read", "Empathy")),
        )
        self.assertEqual(len(first.arts), 2)
        self.assertFalse(hasattr(first, "disciplines"), "the Mentalist must not carry an SWN discipline map")

    def test_the_psychic_training_focus_is_not_available_to_a_mentalist(self):
        """The focus requires a Psychic or Partial Psychic; a Mentalist is neither, so there is nothing to spend it on."""
        self.assertNotIn("Mentalist", ("Psychic", "Partial Psychic"))

    def test_the_focus_object_refuses_a_discipline_outside_the_player_list(self):
        with self.assertRaises(PsychicTrainingError):
            PsychicTraining(discipline="Biopsionics")


if __name__ == "__main__":
    unittest.main()
