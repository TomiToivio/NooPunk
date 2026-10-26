"""Behavioural tests for the AWN crisis-survival layer and the WWN project clock.

Code-only, per AGENTS.md and #271.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules import awn_survival as a
from src.rules import wwn_projects as w


class TravelTests(unittest.TestCase):
    def test_a_road_halves_walking_time_to_a_minimum_of_one_hour(self):
        self.assertEqual(a.travel_hours("light_forest_suburbs_desert"), 2)
        self.assertEqual(a.travel_hours("light_forest_suburbs_desert", road=True), 1)
        self.assertEqual(a.travel_hours("plains_or_scrubland", road=True), 1)

    def test_a_vehicle_needs_a_road_through_the_worst_terrain(self):
        with self.assertRaises(a.SurvivalError):
            a.travel_hours("jungle_swamp_ruins", mode="vehicular")
        self.assertEqual(a.travel_hours("jungle_swamp_ruins", mode="vehicular", road=True), 1)

    def test_mountains_stop_a_vehicle_even_with_a_road(self):
        with self.assertRaises(a.SurvivalError):
            a.travel_hours("mountains", mode="vehicular")

    def test_a_travel_day_is_ten_hours_and_a_forced_march_four_more(self):
        self.assertEqual(a.travel_day_hours(), 10)
        self.assertEqual(a.travel_day_hours(forced_march=True), 14)

    def test_hexes_per_day_follows_the_terrain(self):
        self.assertEqual(a.hexes_per_day("plains_or_scrubland"), 10)
        self.assertEqual(a.hexes_per_day("mountains"), 1)

    def test_driving_and_forced_marching_are_exposed(self):
        self.assertTrue(a.is_exposed(driving=True))
        self.assertTrue(a.is_exposed(forced_march=True))
        self.assertFalse(a.is_exposed())

    def test_scouting_takes_terrain_days_and_removes_the_astray_check(self):
        self.assertEqual(a.scouting_days("heavy_forest_hills_urban"), 3)
        self.assertIsNone(a.going_astray_difficulty("heavy_forest_hills_urban", scouted=True))
        self.assertEqual(a.going_astray_difficulty("heavy_forest_hills_urban"), 9)

    def test_a_party_goes_astray_below_the_difficulty_only(self):
        self.assertTrue(a.goes_astray(check_total=8, terrain_id="heavy_forest_hills_urban"))
        self.assertFalse(a.goes_astray(check_total=9, terrain_id="heavy_forest_hills_urban"))
        self.assertFalse(a.goes_astray(check_total=1, terrain_id="plains_or_scrubland"))

    def test_an_encounter_happens_on_a_one_or_less(self):
        self.assertTrue(a.encounter_check(1))
        self.assertFalse(a.encounter_check(2))
        with self.assertRaises(a.SurvivalError):
            a.encounter_check(9)


class SupplyTests(unittest.TestCase):
    def test_one_encumbrance_per_person_day_of_food(self):
        self.assertEqual(a.food_encumbrance(3), 3)

    def test_packed_travel_rations_are_four_per_week(self):
        self.assertEqual(a.food_encumbrance(7, travel_rations=True), 4)
        self.assertEqual(a.food_encumbrance(8, travel_rations=True), 8)

    def test_the_first_day_without_water_costs_more_than_the_first_day_without_food(self):
        self.assertEqual(a.privation_strain("first_day_without_food"), 0)
        self.assertEqual(a.privation_strain("consecutive_day_without_food"), 1)
        self.assertEqual(a.privation_strain("first_day_without_water"), 2)
        self.assertEqual(a.privation_strain("consecutive_day_without_water"), 3)

    def test_privation_feeds_cwn_system_strain(self):
        result = a.apply_privation(current_strain=8, maximum_strain=10,
                                   kind="first_day_without_water")
        self.assertEqual(result.current_strain, 10)
        self.assertFalse(result.needs_physical_save)
        self.assertTrue(result.recovery_blocked)

    def test_crossing_the_maximum_forces_a_physical_save(self):
        result = a.apply_privation(current_strain=10, maximum_strain=10,
                                   kind="consecutive_day_without_water")
        self.assertTrue(result.over_maximum)
        self.assertTrue(a.starvation_death_save_needed(result))

    def test_an_unknown_privation_is_refused(self):
        with self.assertRaises(a.SurvivalError):
            a.privation_strain("ate_a_bad_mushroom")  # type: ignore[arg-type]


class ForageTests(unittest.TestCase):
    def test_a_failed_check_finds_nothing(self):
        result = a.forage(7, 8, survive_levels=1, die=4)
        self.assertFalse(result.success)
        self.assertEqual(result.units, 0)

    def test_a_successful_check_adds_the_groups_survive_levels(self):
        result = a.forage(10, 8, survive_levels=2, die=4)
        self.assertTrue(result.success)
        self.assertEqual(result.units, 6)

    def test_units_cap_at_ten(self):
        self.assertEqual(a.forage(10, 8, survive_levels=4, die=6).units, 10)

    def test_a_group_without_the_skill_subtracts_one_but_still_finds_something(self):
        self.assertEqual(a.forage(10, 8, survive_levels=-1, die=1).units, 1)

    def test_the_forage_die_is_a_d6(self):
        with self.assertRaises(a.SurvivalError):
            a.forage(10, 8, survive_levels=1, die=7)

    def test_the_terrain_difficulty_table_is_recorded_as_not_transcribed(self):
        self.assertFalse(a.load_survival()["foraging"]["difficulty_table_transcribed"])


class ProjectTests(unittest.TestCase):
    def test_a_plausible_village_project_with_no_opposition_is_cheap(self):
        self.assertEqual(w.project_difficulty("plausible", "village", "none"), 2)

    def test_the_sources_worked_example_lands_on_1024(self):
        # Improbable (2) x kingdom (16) x a king (16) x popular disapproval (2).
        self.assertEqual(
            w.project_difficulty("improbable", "kingdom", "king_or_legendary_power",
                                 disapproval=True),
            1024,
        )

    def test_only_the_greatest_opponent_counts(self):
        greatest = w.project_difficulty("plausible", "city", "king_or_legendary_power")
        lesser = w.project_difficulty("plausible", "city", "minor_figures")
        self.assertEqual(greatest, lesser * 8)

    def test_a_permanent_working_costs_four_times_more(self):
        ordinary = w.project_difficulty("improbable", "city", "local_leaders")
        permanent = w.project_difficulty("improbable", "city", "local_leaders", permanent=True)
        self.assertEqual(permanent, ordinary * 4)

    def test_unknown_keys_are_refused(self):
        with self.assertRaises(w.ProjectError):
            w.project_difficulty("certain", "city")  # type: ignore[arg-type]
        with self.assertRaises(w.ProjectError):
            w.project_difficulty("plausible", "galaxy")  # type: ignore[arg-type]

    def test_renown_accrues_one_per_adventure(self):
        self.assertEqual(w.renown_after_adventures(4, starting=10), 14)

    def test_an_adventure_share_rounds_up(self):
        self.assertEqual(w.adventure_share(1024, adventures_planned=3), 342)

    def test_an_allied_institution_supplies_a_quarter(self):
        self.assertEqual(w.allied_faction_share(1024), 256)

    def test_a_project_completes_only_when_nothing_remains(self):
        state = w.ProjectState(difficulty=10)
        self.assertFalse(state.advance(9).complete)
        self.assertTrue(state.advance(10).complete)

    def test_quelling_an_opponent_lowers_the_remaining_cost(self):
        state = w.ProjectState(difficulty=1024)
        self.assertEqual(state.reduce_difficulty(512).remaining, 512)

    def test_the_money_ladder_is_declared_unmodelled_rather_than_guessed(self):
        self.assertFalse(w.money_purchase_is_modelled())


if __name__ == "__main__":
    unittest.main()
