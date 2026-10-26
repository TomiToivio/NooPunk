"""Tests for the zero-hit-point procedure: risk gate, save, and the table."""
import unittest

from src.rules.cwn_injury_procedure import ProcedureError, resolve_zero_hit_points
from src.rules.cwn_major_injury import dies_without_care_within, is_lethal

ATTRIBUTES = {"Strength": 10, "Dexterity": 10, "Constitution": 10,
              "Intelligence": 10, "Wisdom": 10, "Charisma": 10}


class NoRiskTest(unittest.TestCase):
    def test_positive_hit_points_are_not_an_injury(self):
        out = resolve_zero_hit_points(hit_points_after=3, traumatic_in_fight=True,
                                      level=1, attributes=ATTRIBUTES)
        self.assertFalse(out.risked_major_injury)
        self.assertFalse(out.mortally_wounded)
        self.assertIsNone(out.save)
        self.assertIsNone(out.injury)

    def test_zero_without_trauma_is_a_knockout_not_a_wound(self):
        out = resolve_zero_hit_points(hit_points_after=0, traumatic_in_fight=False,
                                      level=1, attributes=ATTRIBUTES)
        self.assertTrue(out.mortally_wounded)
        self.assertFalse(out.risked_major_injury)
        self.assertIsNone(out.save)


class LethalityTest(unittest.TestCase):
    def test_a_non_lethal_beating_to_zero_is_still_only_a_knockout(self):
        out = resolve_zero_hit_points(hit_points_after=0, traumatic_in_fight=True,
                                      lethal=False, level=1, attributes=ATTRIBUTES)
        self.assertTrue(out.mortally_wounded)
        self.assertFalse(out.risked_major_injury)
        self.assertIsNone(out.save)

    def test_lethal_damage_at_zero_with_trauma_does_force_the_save(self):
        with self.assertRaises(ProcedureError):
            resolve_zero_hit_points(hit_points_after=0, traumatic_in_fight=True,
                                    lethal=True, level=1, attributes=ATTRIBUTES)


class SaveGateTest(unittest.TestCase):
    def test_trauma_at_zero_demands_a_physical_save(self):
        with self.assertRaises(ProcedureError):
            resolve_zero_hit_points(hit_points_after=0, traumatic_in_fight=True,
                                    level=1, attributes=ATTRIBUTES)

    def test_a_passed_save_still_leaves_the_character_mortally_wounded(self):
        out = resolve_zero_hit_points(hit_points_after=0, traumatic_in_fight=True,
                                      level=1, attributes=ATTRIBUTES, save_die=20)
        self.assertTrue(out.mortally_wounded)
        self.assertTrue(out.risked_major_injury)
        self.assertTrue(out.save.success)
        self.assertIsNone(out.injury)

    def test_a_natural_one_fails_even_against_a_beatable_target(self):
        out = resolve_zero_hit_points(hit_points_after=0, traumatic_in_fight=True,
                                      level=1, attributes=ATTRIBUTES, save_die=1,
                                      injury_roll=12)
        self.assertFalse(out.save.success)
        self.assertIsNotNone(out.injury)

    def test_a_failed_save_needs_its_table_roll(self):
        with self.assertRaises(ProcedureError):
            resolve_zero_hit_points(hit_points_after=0, traumatic_in_fight=True,
                                    level=1, attributes=ATTRIBUTES, save_die=1)


class TableTest(unittest.TestCase):
    def _failed(self, roll, modifier=0):
        return resolve_zero_hit_points(
            hit_points_after=0, traumatic_in_fight=True, level=1, attributes=ATTRIBUTES,
            save_die=1, injury_roll=roll, injury_modifier=modifier,
        ).injury

    def test_a_failed_save_consults_the_d12_table(self):
        self.assertEqual(self._failed(11).id, "flesh_wound")

    def test_the_roll_is_clamped_into_the_table(self):
        self.assertEqual(self._failed(20).roll, 12)
        self.assertEqual(self._failed(-5).roll, 1)

    def test_the_modifier_is_applied_before_clamping(self):
        self.assertEqual(self._failed(10, modifier=5).roll, 12)

    def test_the_instant_death_row_is_lethal(self):
        self.assertTrue(is_lethal(self._failed(1)))

    def test_a_row_that_kills_without_care_says_how_long(self):
        # Row 2 is not an instant death: it is fatal in an hour without a street doc.
        self.assertEqual(dies_without_care_within(self._failed(2)), 1)

    def test_a_non_lethal_row_is_not_flagged_lethal(self):
        self.assertFalse(is_lethal(self._failed(11)))

    def test_a_risk_that_was_taken_but_passed_never_touches_the_table(self):
        out = resolve_zero_hit_points(hit_points_after=0, traumatic_in_fight=True,
                                      level=1, attributes=ATTRIBUTES, save_die=20,
                                      injury_roll=2)
        self.assertIsNone(out.injury)


if __name__ == "__main__":
    unittest.main()
