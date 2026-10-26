"""Foci engine (SRD 1.6.0-1.6.2, 2.7.1.6). Values asserted here are read from the SRD."""

from __future__ import annotations

import unittest

from src.rules import cwn_foci as f


class FocusCatalogTests(unittest.TestCase):
    """SRD 1.6.1: 26 Foci, four of them single-level."""

    def test_there_are_twenty_six_foci(self) -> None:
        self.assertEqual(len(f.FOCI), 26)

    def test_exactly_four_foci_have_one_level(self) -> None:
        one = {name for name, x in f.FOCI.items() if x.levels == 1}
        self.assertEqual(one, {"All Natural", "Many Faces", "Unique Gift", "Unregistered"})
        self.assertEqual(sum(1 for x in f.FOCI.values() if x.levels == 2), 22)

    def test_the_focused_edge_is_not_a_focus(self) -> None:
        # "Focused" is an Edge that grants an extra Focus pick (SRD 1.6.0); it is not itself a Focus.
        self.assertNotIn("Focused", f.FOCI)

    def test_specific_names_from_the_srd(self) -> None:
        for name in ("Ace Driver", "Drone Pilot", "Pop Idol", "Safe Haven",
                     "Sniper's Eye", "Unarmed Combatant", "Whirlwind Assault"):
            with self.subTest(focus=name):
                self.assertIn(name, f.FOCI)

    def test_unknown_focus_raises(self) -> None:
        with self.assertRaises(f.FocusError):
            f.max_level("Ghost")


class PickTests(unittest.TestCase):
    """SRD 1.6.0 and 2.7.1.6."""

    def test_a_new_character_gets_one_focus(self) -> None:
        self.assertEqual(f.new_character_picks(), 1)

    def test_the_focused_edge_adds_exactly_one_more(self) -> None:
        self.assertEqual(f.new_character_picks(has_focused_edge=True), 2)

    def test_advancement_picks_come_at_levels_two_five_seven_ten(self) -> None:
        self.assertEqual(f.PICK_LEVELS, (2, 5, 7, 10))
        self.assertEqual(f.advancement_picks(1), 0)
        self.assertEqual(f.advancement_picks(2), 1)
        self.assertEqual(f.advancement_picks(4), 1)
        self.assertEqual(f.advancement_picks(5), 2)
        self.assertEqual(f.advancement_picks(6), 2)
        self.assertEqual(f.advancement_picks(7), 3)
        self.assertEqual(f.advancement_picks(10), 4)
        self.assertEqual(f.advancement_picks(20), 4, "no further picks past level 10")

    def test_total_includes_the_creation_pick(self) -> None:
        self.assertEqual(f.total_picks(1), 1)
        self.assertEqual(f.total_picks(10), 5)
        self.assertEqual(f.total_picks(10, has_focused_edge=True), 6)

    def test_level_one_must_come_before_level_two(self) -> None:
        self.assertTrue(f.can_take_level("Ace Driver", current_level=0))
        self.assertTrue(f.can_take_level("Ace Driver", current_level=1))
        self.assertFalse(f.can_take_level("Ace Driver", current_level=2))
        self.assertEqual(f.take_level("Ace Driver", current_level=0), 1)
        self.assertEqual(f.take_level("Ace Driver", current_level=1), 2)

    def test_a_single_level_focus_refuses_a_second_pick(self) -> None:
        self.assertFalse(f.can_take_level("Unique Gift", current_level=1))
        with self.assertRaises(f.FocusError):
            f.take_level("Unique Gift", current_level=1)


class GearBudgetTests(unittest.TestCase):
    """SRD 1.6.2 table."""

    def test_budget_by_level(self) -> None:
        self.assertEqual(f.gear_budget(1, kind="vehicle"), 5_000)
        self.assertEqual(f.gear_budget(1, kind="drone"), 1_000)
        self.assertEqual(f.gear_budget(5, kind="vehicle"), 30_000)
        self.assertEqual(f.gear_budget(5, kind="drone"), 20_000)
        self.assertEqual(f.gear_budget(10, kind="vehicle"), 200_000)
        self.assertEqual(f.gear_budget(10, kind="drone"), 80_000)

    def test_the_budget_only_rises(self) -> None:
        vehicles = [f.gear_budget(lv, kind="vehicle") for lv in range(1, 11)]
        drones = [f.gear_budget(lv, kind="drone") for lv in range(1, 11)]
        self.assertEqual(vehicles, sorted(vehicles))
        self.assertEqual(drones, sorted(drones))

    def test_only_three_foci_grant_a_budget(self) -> None:
        self.assertEqual(set(f.GEAR_BUDGET_FOCI), {"Ace Driver", "Roamer", "Drone Pilot"})
        self.assertEqual(f.GEAR_BUDGET_FOCI["Drone Pilot"], "drone")
        self.assertEqual(f.GEAR_BUDGET_FOCI["Ace Driver"], "vehicle")

    def test_out_of_table_levels_and_bad_kinds_raise(self) -> None:
        with self.assertRaises(f.FocusError):
            f.gear_budget(11, kind="vehicle")
        with self.assertRaises(f.FocusError):
            f.gear_budget(1, kind="boat")  # type: ignore[arg-type]  # deliberate bad input


if __name__ == "__main__":
    unittest.main()
