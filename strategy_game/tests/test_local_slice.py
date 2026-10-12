"""Repeatable experimental strategy slice tests."""
import unittest
from strategy_game.local_slice import Game, Mission, play


class LocalSliceTests(unittest.TestCase):
    def test_rosters_and_replay(self):
        a, b = play(12, 42), play(12, 42)
        self.assertEqual(a.snapshot(), b.snapshot())
        self.assertEqual(len(a.history), 12)
        self.assertEqual(len(a.parties), 3)
        self.assertTrue(all(len(p.leader_ids) == 4 for p in a.parties))
        self.assertTrue(all(len(t["actions"]) == 12 for t in a.history))

    def test_no_leaderless_or_duplicate_or_injured_missions(self):
        game = Game.from_scenario()
        for orders in ([Mission("unknown", "rest", "civic")],
                       [Mission("cpu1", "rest", "civic")] * 2):
            with self.assertRaises(ValueError):
                game.step(orders)
        game.leaders[0].status = "injured"
        with self.assertRaises(ValueError):
            game.step([Mission("cpu1", "rest", "civic")])

    def test_invalid_travel_and_overspending_are_atomic(self):
        game = Game.from_scenario()
        initial = game.snapshot()
        with self.assertRaises(ValueError):
            game.step([Mission("cpu1", "campaign", "outer_island")])
        self.assertEqual(initial, game.snapshot())
        with self.assertRaises(ValueError):
            game.step([Mission("cpu1", "campaign", "civic", cost=999)])
        self.assertEqual(initial, game.snapshot())

    def test_portfolio_and_relationship(self):
        game = Game.from_scenario()
        game.reassign("cpu1", "operations")
        before = next(p.treasury for p in game.parties if p.id == "cpu")
        game.step([Mission("cpu1", "negotiate", "civic", target="uip1")])
        self.assertGreater(next(p.treasury for p in game.parties if p.id == "cpu"), before)
        self.assertEqual(game.history[0]["actions"][0]["leader"], "CPU Chair")


if __name__ == "__main__":
    unittest.main()
