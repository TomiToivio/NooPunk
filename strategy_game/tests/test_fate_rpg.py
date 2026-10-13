"""Executable checks for the Fate-based RPG layer (#389)."""
import unittest
from random import Random

from strategy_game.rpg.fate import (
    Action, Character, Outcome, ResourceError,
    demo_investigation, resolve, roll_fate, skill_check,
)


class FateRpgTests(unittest.TestCase):
    def test_fate_dice_seeded_and_bounded(self):
        a, b = Random(17), Random(17)
        self.assertEqual([roll_fate(a) for _ in range(10)],
                         [roll_fate(b) for _ in range(10)])
        for dice in (roll_fate(Random(i)) for i in range(200)):
            self.assertEqual(len(dice), 4)
            self.assertTrue(all(face in (-1, 0, 1) for face in dice))
            self.assertTrue(-4 <= sum(dice) <= 4)

    def test_all_actions_and_result_ranges(self):
        for action in Action:
            result = resolve(action, skill=1, difficulty=1, rng=Random(5))
            self.assertIn(result.outcome, Outcome)
            self.assertEqual(result.total - result.difficulty, result.shifts)

    def test_fate_point_invocation_is_explicit(self):
        actor = Character("a", "Agent", ["Focused"], fate_points=1)
        self.assertEqual(actor.invoke("Focused"), 2)
        self.assertEqual(actor.fate_points, 0)
        with self.assertRaises(ResourceError):
            actor.invoke("Focused")
        with self.assertRaises(ResourceError):
            actor.invoke("Other")

    def test_stress_and_consequence(self):
        actor = Character("a", "Agent", [])
        self.assertEqual(actor.absorb_hit(2), "stress_2")
        self.assertEqual(actor.absorb_hit(2), "unabsorbed")
        actor.take_consequence("Shaken", 2)
        with self.assertRaises(ResourceError):
            actor.take_consequence("Another", 2)
        actor.clear_stress()
        self.assertEqual(actor.physical_stress, [False, False])

    def test_rare_stacks_and_natural_psi_separate(self):
        ordinary = Character("a", "Civilian", [])
        self.assertEqual(ordinary.body, "original_biological")
        self.assertFalse(ordinary.cortical_stack)
        self.assertFalse(ordinary.resleeved)
        self.assertFalse(ordinary.natural_psi)
        psychic = Character("b", "Sensitive", ["Natural talent"], natural_psi=True,
                            psi_abilities=["empathy"])
        self.assertTrue(psychic.natural_psi)
        with self.assertRaises(ResourceError):
            Character("c", "Unspecified", [], psi_abilities=["telepathy"])

    def test_demo_cyber_and_psi_use_same_engine(self):
        first, second = demo_investigation(12), demo_investigation(12)
        self.assertEqual(first, second)
        self.assertEqual(first["cyber"].action, Action.OVERCOME)
        self.assertEqual(first["psi"].action, Action.CREATE_ADVANTAGE)

    def test_skill_check(self):
        actor = Character("id", "Name", ["Augmented"], skills={"Tech": 2})
        result = skill_check(actor, Action.OVERCOME, "Tech", 2, rng=Random(1),
                             invoked_aspect="Augmented")
        self.assertEqual(actor.fate_points, 2)
        self.assertEqual(result.total, sum(result.dice) + 4)


if __name__ == "__main__":
    unittest.main()
