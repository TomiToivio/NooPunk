"""Integration checks against the current NoöPunk Fate scene interface."""
import unittest
from strategy_game.scenarios.ubiquitous_maniacs import UbiquitousManiacs, ScenarioError, cast, demo


class UbiquitousManiacsTests(unittest.TestCase):
    def test_two_days_and_finish(self):
        session = UbiquitousManiacs()
        self.assertEqual(session.day, 1)
        while not session.finished:
            session.choose(next(iter(session.view()["choices"])))
        self.assertEqual(session.day, 2)
        self.assertTrue(session.finished)

    def test_uses_current_rpg_skills_and_fate(self):
        self.assertEqual(set(cast()["romppainen"].skills), {"SAV", "WIL"})
        a = UbiquitousManiacs().attempt("romppainen", "SAV", 1, 42)
        b = UbiquitousManiacs().attempt("romppainen", "SAV", 1, 42)
        self.assertEqual(a, b)
        self.assertEqual(len(a["dice"]), 4)

    def test_replay_and_invalid_save(self):
        session = UbiquitousManiacs()
        # `falk` is the canon Laura Falk. The corpus's *Ingrid* Falk is a different person and
        # is not in the cast; see the canon-anchoring test for why that matters.
        session.attempt("falk", "COG", 2, 9)
        session.choose("read_form")
        restored = UbiquitousManiacs.from_dict(session.to_dict())
        self.assertEqual(restored.to_dict(), session.to_dict())
        tampered = session.to_dict()
        tampered["checks"][0]["total"] = 999
        with self.assertRaises(ScenarioError):
            UbiquitousManiacs.from_dict(tampered)

    def test_invalid_moves(self):
        with self.assertRaises(ScenarioError):
            UbiquitousManiacs().choose("unlisted")
        with self.assertRaises(ScenarioError):
            UbiquitousManiacs().attempt("romppainen", "not_a_skill", 1, 1)

    def test_demo(self):
        self.assertTrue(demo()["replay_valid"])


if __name__ == "__main__":
    unittest.main()
