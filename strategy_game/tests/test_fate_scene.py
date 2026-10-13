"""Behavioral tests for executable RPG mechanics (not rulebook prose)."""
import unittest
from random import Random

from strategy_game.rpg.fate import Action, Character, Outcome, ResourceError, roll_fate
from strategy_game.rpg.scene import (
    Scene, check, interpret, apply_hit, compel, refresh, strategy_event_payload,
)


class FateSceneTests(unittest.TestCase):
    def actor(self):
        return Character("a", "Agent", ["Careful operator"], skills={"Infosec": 2, "Psi": 1})

    def test_dice_seed_and_bounds(self):
        self.assertEqual([roll_fate(Random(13)) for _ in range(1)],
                         [roll_fate(Random(13))])
        rng = Random(7)
        for _ in range(2000):
            roll = roll_fate(rng)
            self.assertEqual(len(roll), 4)
            self.assertTrue(all(d in (-1, 0, 1) for d in roll))
            self.assertTrue(-4 <= sum(roll) <= 4)

    def test_scene_invoke_accounting_and_reproducibility(self):
        a, b = self.actor(), self.actor()
        scene_a, scene_b = Scene(), Scene()
        scene_a.create_aspect("Blind camera", free_invocations=1)
        scene_b.create_aspect("Blind camera", free_invocations=1)
        first = check(a, Action.OVERCOME, "Infosec", 2, rng=Random(41),
                      scene=scene_a, invocation="Blind camera", free=True)
        second = check(b, Action.OVERCOME, "Infosec", 2, rng=Random(41),
                       scene=scene_b, invocation="Blind camera", free=True)
        self.assertEqual(first, second)
        self.assertEqual(a.fate_points, 3)
        self.assertEqual(scene_a.aspects["Blind camera"].free_invocations, 0)
        with self.assertRaises(ResourceError):
            check(a, Action.OVERCOME, "Infosec", 2, rng=Random(41),
                  scene=scene_a, invocation="Blind camera", free=True)

    def test_paid_invoke_and_reroll(self):
        actor = self.actor()
        check(actor, Action.OVERCOME, "Infosec", 1, rng=Random(2),
              invocation="Careful operator", reroll=True)
        self.assertEqual(actor.fate_points, 2)

    def test_permission_failure_never_spends_resources(self):
        actor = self.actor()
        with self.assertRaises(ResourceError):
            check(actor, Action.OVERCOME, "Infosec", 2, rng=Random(1),
                  invocation="Careful operator", permitted=False)
        self.assertEqual(actor.fate_points, 3)

    def test_attack_and_consequence(self):
        actor = self.actor()
        hit = apply_hit(actor, 5, consequence=("Shaken", 4))
        self.assertEqual(hit.stress_box, 1)
        self.assertFalse(hit.taken_out)
        self.assertEqual(actor.physical_stress, [True, False])
        with self.assertRaises(ResourceError):
            apply_hit(actor, 3, consequence=("Duplicate", 4))
        self.assertEqual(len(actor.consequences), 1)
        fatal = apply_hit(actor, 7)
        self.assertTrue(fatal.taken_out)
        self.assertEqual(fatal.remaining, 7)

    def test_compel_refresh(self):
        actor = self.actor()
        compel(actor, accepted=False)
        self.assertEqual(actor.fate_points, 2)
        compel(actor, accepted=True)
        self.assertEqual(actor.fate_points, 3)
        refresh(actor, 5)
        self.assertEqual(actor.fate_points, 5)

    def test_psi_is_natural_and_stack_optional(self):
        actor = Character("psi", "Seer", ["Uncanny instinct"],
                          natural_psi=True, psi_abilities=["impression"],
                          skills={"Psi": 2})
        self.assertFalse(actor.cortical_stack)
        self.assertFalse(actor.resleeved)
        self.assertEqual(actor.body, "original_biological")
        result = check(actor, Action.CREATE_ADVANTAGE, "Psi", 1,
                       rng=Random(9), permitted=True).resolution
        self.assertEqual(strategy_event_payload(actor, result)["agent_id"], "psi")
        self.assertGreaterEqual(interpret(result).free_invocations, 0)

    def test_all_action_signals(self):
        actor = self.actor()
        for action in Action:
            result = check(actor, action, "Infosec", 1, rng=Random(10)).resolution
            self.assertIn(result.outcome, Outcome)
            self.assertEqual(interpret(result).shifts, result.shifts)


if __name__ == "__main__":
    unittest.main()
