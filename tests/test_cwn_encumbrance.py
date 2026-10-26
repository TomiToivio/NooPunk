"""Encumbrance — assertions traced to the CWN SRD encumbrance section."""
import unittest

from src.rules import cwn_encumbrance as enc


class CapacityTests(unittest.TestCase):
    def test_stowed_capacity_is_strength(self) -> None:
        self.assertEqual(enc.stowed_capacity(11), 11)

    def test_readied_capacity_is_half_strength_rounded_down(self) -> None:
        self.assertEqual(enc.readied_capacity(11), 5)
        self.assertEqual(enc.readied_capacity(10), 5)

    def test_negative_strength_is_refused(self) -> None:
        with self.assertRaises(enc.EncumbranceError):
            enc.stowed_capacity(-1)


class TierTests(unittest.TestCase):
    def test_within_limits_is_normal(self) -> None:
        self.assertEqual(enc.tier_for(11, enc.Load(stowed=11, readied=5)), "normal")
        self.assertEqual(enc.move_speed(11, enc.Load(stowed=11, readied=5)), 10.0)

    def test_one_point_over_readied_is_heavy(self) -> None:
        self.assertEqual(enc.tier_for(11, enc.Load(stowed=0, readied=6)), "heavy")
        self.assertAlmostEqual(enc.move_speed(11, enc.Load(stowed=0, readied=6)), 7.0)

    def test_one_point_over_stowed_is_heavy(self) -> None:
        self.assertEqual(enc.tier_for(11, enc.Load(stowed=12, readied=0)), "heavy")

    def test_the_first_push_allows_two_ready_and_four_stowed(self) -> None:
        self.assertEqual(enc.tier_for(11, enc.Load(stowed=15, readied=7)), "heavy")

    def test_the_second_push_is_a_fifty_percent_cut(self) -> None:
        self.assertEqual(enc.tier_for(11, enc.Load(stowed=19, readied=9)), "overloaded")
        self.assertAlmostEqual(enc.move_speed(11, enc.Load(stowed=19, readied=9)), 5.0)

    def test_beyond_the_second_push_cannot_be_hauled(self) -> None:
        self.assertEqual(enc.tier_for(11, enc.Load(stowed=20, readied=0)), "immobile")
        self.assertEqual(enc.move_speed(11, enc.Load(stowed=20, readied=0)), 0.0)
        self.assertFalse(enc.can_haul(11, enc.Load(stowed=20, readied=0)))

    def test_negative_load_is_refused(self) -> None:
        with self.assertRaises(enc.EncumbranceError):
            enc.Load(stowed=-1)


class ConversionTests(unittest.TestCase):
    def test_three_small_items_bundle_into_one_point(self) -> None:
        self.assertEqual(enc.bundled_points(0), 0)
        self.assertEqual(enc.bundled_points(3), 1)
        self.assertEqual(enc.bundled_points(4), 2)
        self.assertEqual(enc.bundled_points(6), 2)
        self.assertEqual(enc.bundled_points(7), 3)

    def test_twenty_five_kilograms_are_ten_points(self) -> None:
        self.assertAlmostEqual(enc.kilograms_to_points(25), 10.0)
        self.assertAlmostEqual(enc.kilograms_to_points(50), 20.0)

    def test_base_speed_can_be_overridden(self) -> None:
        self.assertAlmostEqual(enc.move_speed(10, enc.Load(stowed=11), base=12.0), 8.4)


if __name__ == "__main__":
    unittest.main()
