"""Pins the 2d6 anchoring of the narrative layer (#697, D41-D43).

The rulebook states three claims that are arithmetic, and a claim in prose that nothing
executes is a claim that drifts. These tests execute them against the shipped layer.
"""
import unittest

from src.rules.narrative_layer import (
    MAX_INVOCATIONS_PER_ROLL,
    POOL_MAX,
    POOL_MIN,
    band_distribution,
    can_invoke,
)


def success_share(modifier: int, difficulty: int) -> float:
    """Success is everything that is not a miss, read off the shipped band model."""
    return 1.0 - float(band_distribution(modifier=modifier, difficulty=difficulty)["miss"])


class AnchoringTest(unittest.TestCase):
    def test_the_standard_difficulty_is_a_minority_chance_without_aspects(self):
        self.assertAlmostEqual(success_share(0, 8), 41.7 / 100, places=3)

    def test_a_plus_two_invoke_is_worth_about_thirty_points_at_the_standard_difficulty(self):
        """D42's number: +30.6 pp at DV 8, against the retired 4dF figure of +32.1 pp."""
        shift = (success_share(2, 8) - success_share(0, 8)) * 100
        self.assertAlmostEqual(shift, 30.6, delta=0.2)

    def test_the_same_bonus_is_worth_nothing_at_the_hardest_difficulty(self):
        """D43: an aspect's worth is difficulty-dependent, not a fixed quantity."""
        shift = (success_share(1, 14) - success_share(0, 14)) * 100
        self.assertAlmostEqual(shift, 0.0, delta=0.1)

    def test_stacking_four_steps_reaches_ninety_one_point_seven_not_certainty(self):
        self.assertAlmostEqual(success_share(4, 8), 91.7 / 100, places=3)

    def test_one_invoke_per_roll_is_still_the_rule(self):
        self.assertEqual(MAX_INVOCATIONS_PER_ROLL, 1)
        self.assertTrue(can_invoke(0))
        self.assertFalse(can_invoke(1))

    def test_the_pool_is_bounded_zero_to_three(self):
        self.assertEqual((POOL_MIN, POOL_MAX), (0, 3))


if __name__ == "__main__":
    unittest.main()
