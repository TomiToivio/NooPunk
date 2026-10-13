"""Behavioral tests for the isolated illustrative #338 prototype only."""
import unittest

from strategy_game.global_slice import sample_world, view, demo


class GlobalSliceTests(unittest.TestCase):
    def test_four_views(self):
        world = sample_world()
        for name in ("map", "faction", "politics", "events"):
            self.assertTrue(view(world, name))
        self.assertIn("New York", view(world, "map"))
        self.assertIn("passive until assigned", view(world, "faction"))
        self.assertNotIn("Unknown installation", view(world, "map"))

    def test_agent_activates_asset_and_reveals_site(self):
        world = sample_world()
        outcome = world.perform("investigate_crash", "leader", "field",
                                "protect witnesses", die=6)
        self.assertTrue(outcome["success"])
        self.assertIn("Unknown installation", view(world, "map"))
        self.assertEqual(len(world.political_reactions), 1)
        self.assertEqual(world.resources[0].quantity, 2)

    def test_failed_check_is_complication_not_dead_end(self):
        world = sample_world()
        outcome = world.perform("archive_heist", "officer", "security",
                                "quiet access", die=1)
        self.assertFalse(outcome["success"])
        self.assertIn("Complication", outcome["summary"])
        self.assertEqual(len(world.log), 1)

    def test_hidden_site_and_repeated_mission_rejected(self):
        world = sample_world()
        with self.assertRaises(ValueError):
            world.perform("base_response", "officer", "security",
                          "attempt contact", die=6)
        world.perform("investigate_crash", "leader", "field",
                      "share evidence", die=5)
        with self.assertRaises(ValueError):
            world.perform("investigate_crash", "leader", "field",
                          "share evidence", die=5)

    def test_choices_and_dice_validated(self):
        world = sample_world()
        for die in (0, 7, True):
            with self.assertRaises(ValueError):
                world.perform("archive_heist", "analyst", "cyber",
                              "quiet access", die=die)
        with self.assertRaises(ValueError):
            world.perform("archive_heist", "analyst", "cyber",
                          "impossible choice", die=4)

    def test_seeded_demo_is_reproducible(self):
        self.assertEqual(demo(12), demo(12))


if __name__ == "__main__":
    unittest.main()
