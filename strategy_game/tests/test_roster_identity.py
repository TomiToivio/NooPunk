"""Regression tests for five-seat character identity validation (#461)."""
import unittest

from strategy_game.rpg.roster import RosterError, default_seats


class RosterIdentityTests(unittest.TestCase):
    def test_empty_agent_id_is_rejected_before_orders(self):
        for missing in ("", " ", "\t"):
            with self.subTest(missing=repr(missing)):
                with self.assertRaisesRegex(RosterError, "non-empty character id"):
                    default_seats("leader", ("a", "b", missing, "d"))

    def test_valid_ids_are_unchanged_and_whitespace_is_normalized(self):
        seats = default_seats(" leader ", (" a ", "b", "c", "d"))
        self.assertEqual(tuple(seat.character_id for seat in seats),
                         ("leader", "a", "b", "c", "d"))


if __name__ == "__main__":
    unittest.main()
