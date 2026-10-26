"""Behavioural tests for the CWN vehicle kernel (SRD 3.7, 2.5.1, 2.6).

Code-only, per AGENTS.md and #271: every assertion here exercises arithmetic in
``src/rules/cwn_vehicles.py`` against the contract in ``data/rules/cwn_vehicles.json``.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules import cwn_vehicles as v


class ContractTests(unittest.TestCase):
    def test_every_vehicle_row_loads_with_a_trauma_target_of_at_least_six(self):
        rows = v.load_vehicles()["vehicles"]
        self.assertEqual(len(rows), 10)
        for row in rows:
            hull = v.vehicle(row["id"])
            self.assertGreaterEqual(hull.trauma_target, 6, hull.id)
            self.assertIn(hull.size, v.SIZE_RANK, hull.id)

    def test_armor_column_distinguishes_zero_from_immune(self):
        self.assertEqual(v.vehicle("micro_flyer").armor, 0)
        self.assertIsNone(v.vehicle("tank").armor)
        self.assertEqual(v.vehicle("tank").armor_note, "immune")
        self.assertEqual(v.vehicle("apc").armor_note, "heavy_only")

    def test_fitting_minimum_size_is_always_a_known_size(self):
        for row in v.load_vehicles()["fittings"]:
            self.assertIn(row["min_size"], v.SIZE_RANK, row["id"])
            piece = v.fitting(row["id"])
            self.assertGreaterEqual(piece.power, 0, row["id"])
            self.assertGreaterEqual(piece.mass, 0, row["id"])

    def test_every_vehicle_mod_names_both_fix_and_drive(self):
        for row in v.load_vehicles()["mods"]:
            mod = v.modification(row["id"])
            self.assertIn("Fix", mod.skills, row["id"])
            self.assertIn("Drive", mod.skills, row["id"])
            self.assertGreater(mod.cost_percent, 0, row["id"])

    def test_vehicle_weapon_rows_carry_a_trauma_die_unless_marked_nonlethal(self):
        for row in v.load_vehicles()["vehicle_weapons"]:
            piece = v.weapon(row["id"])
            if piece.nonlethal:
                self.assertIsNone(piece.trauma_die, row["id"])
            else:
                self.assertIsNotNone(piece.trauma_die, row["id"])


class FittingTests(unittest.TestCase):
    def test_armor_plating_adds_three_armor_each(self):
        fitted = v.fit_out("car", fittings=["armor_plating"])
        self.assertEqual(fitted.armor, 9)
        self.assertEqual(fitted.base.armor, 6)

    def test_a_medium_hull_may_take_armor_plating_twice_and_a_third_is_illegal(self):
        self.assertEqual(v.fit_out("car", fittings=["armor_plating"] * 2).armor, 12)
        with self.assertRaises(v.VehicleError):
            v.fit_out("car", fittings=["armor_plating"] * 3)

    def test_small_hull_may_take_armor_plating_once_only(self):
        with self.assertRaises(v.VehicleError):
            v.fit_out("motorcycle", fittings=["armor_plating"] * 2)

    def test_min_size_is_a_floor_not_an_equality(self):
        # Crash Pod needs a medium hull; a truck (large) may take it, a bike may not.
        self.assertEqual(v.fit_out("truck", fittings=["crash_pod"]).base.id, "truck")
        with self.assertRaises(v.VehicleError):
            v.fit_out("motorcycle", fittings=["crash_pod"])

    def test_power_budget_refuses_an_overdraw(self):
        # A car has 3 Power: ECM (2) + cloaking (1) + sensors (1) is 4.
        with self.assertRaises(v.VehicleError):
            v.fit_out("car", fittings=["ecm_emitter", "emissions_cloaking", "advanced_sensors"])

    def test_a_power_system_buys_the_budget_it_needs(self):
        fitted = v.fit_out("car", fittings=["ecm_emitter", "emissions_cloaking",
                                            "advanced_sensors", "power_system_small"])
        self.assertEqual(fitted.power_available, 5)
        self.assertEqual(fitted.power_used, 4)
        self.assertTrue(fitted.legal)

    def test_extra_durability_raises_hit_points_by_a_quarter_of_base(self):
        self.assertEqual(v.fit_out("car", fittings=["extra_durability"]).hit_points, 38)

    def test_reinforced_chassis_raises_hp_and_costs_two_mass(self):
        fitted = v.fit_out("car", mods=["reinforced_chassis"])
        self.assertEqual(fitted.hit_points, 38)
        self.assertEqual(fitted.mass_available, 5)

    def test_ultralight_components_trade_hit_points_for_mass(self):
        fitted = v.fit_out("car", mods=["ultralight_components"])
        self.assertEqual(fitted.hit_points, 24)
        self.assertEqual(fitted.mass_available, 10)

    def test_mass_budget_refuses_an_overload(self):
        # A motorcycle has 3 Mass; three armour platings (9 Mass) cannot fit.
        with self.assertRaises(v.VehicleError):
            v.fit_out("motorcycle", fittings=["armor_plating", "afterburners", "crash_pod"])

    def test_a_fitting_may_stack_only_when_the_contract_allows_it(self):
        fitted = v.fit_out("truck", fittings=["cargo_space", "cargo_space", "extra_passengers"])
        self.assertEqual(fitted.crew, 6)

    def test_derived_effects_are_visible_to_the_caller(self):
        fitted = v.fit_out("car", fittings=["medbay", "tool_rack"])
        self.assertTrue(fitted.has("emergency_clinic"))
        self.assertTrue(fitted.has("workshop"))


class CombatTests(unittest.TestCase):
    def test_a_stationary_hull_is_easier_to_hit(self):
        self.assertEqual(v.armor_class_in_combat(11, moving=False), 7)

    def test_a_moving_hull_adds_its_drivers_drive_skill(self):
        self.assertEqual(v.armor_class_in_combat(11, moving=True, driver_drive_skill=2), 13)

    def test_armor_comes_off_after_the_trauma_multiplier(self):
        self.assertEqual(v.damage_to_vehicle(12, trauma_multiplier=3, armor=6), 30)

    def test_damage_floors_at_zero_and_rejects_a_bogus_multiplier(self):
        self.assertEqual(v.damage_to_vehicle(4, trauma_multiplier=1, armor=6), 0)
        with self.assertRaises(v.VehicleError):
            v.damage_to_vehicle(4, trauma_multiplier=0)

    def test_heavy_only_hulls_ignore_ordinary_weapons(self):
        apc = v.vehicle("apc")
        self.assertFalse(v.can_be_harmed(apc))
        self.assertTrue(v.can_be_harmed(apc, heavy_weapon=True))
        self.assertTrue(v.can_be_harmed(apc, vehicle_trauma=True))

    def test_an_immune_hull_is_a_referee_call_not_a_code_call(self):
        self.assertIsNone(v.can_be_harmed(v.vehicle("tank")))

    def test_crash_outcomes_are_three_distinct_results(self):
        safe = v.crash_outcome(physical_save_made=True, luck_save_made=True)
        hurt = v.crash_outcome(physical_save_made=True, luck_save_made=False)
        down = v.crash_outcome(physical_save_made=False, luck_save_made=False)
        self.assertTrue(safe.unscathed)
        self.assertEqual(safe.damage_fraction, 0.0)
        self.assertEqual(hurt.damage_fraction, 0.5)
        self.assertFalse(hurt.mortally_wounded)
        self.assertTrue(down.mortally_wounded)
        self.assertTrue(down.major_injury_if_survives)

    def test_destruction_damage_halves_on_a_luck_save(self):
        self.assertEqual(v.destruction_damage(18, luck_save_made=True), 9)
        self.assertEqual(v.destruction_damage(18, luck_save_made=False), 18)

    def test_ramming_a_person_needs_a_strict_win_and_a_failed_evasion_save(self):
        hit = v.ram_person(driver_total=11, target_total=11, evasion_save_made=False,
                           hull_hit_points=30)
        self.assertFalse(hit.driver_won)
        self.assertEqual(hit.damage_dealt, 0)

    def test_a_rammed_person_takes_the_hulls_maximum_hit_points(self):
        hit = v.ram_person(driver_total=12, target_total=11, evasion_save_made=False,
                           hull_hit_points=30)
        self.assertEqual(hit.damage_dealt, 30)
        saved = v.ram_person(driver_total=12, target_total=11, evasion_save_made=True,
                             hull_hit_points=30)
        self.assertEqual(saved.damage_dealt, 0)

    def test_hull_versus_hull_has_no_evasion_save(self):
        result = v.ram_vehicle(driver_total=12, target_total=11, hull_hit_points=30)
        self.assertEqual(result.damage_dealt, 30)


class ChaseTests(unittest.TestCase):
    def test_a_tie_is_an_escape(self):
        outcome = v.resolve_chase(12, [12])
        self.assertEqual(outcome.caught_by, (False,))
        self.assertTrue(outcome.escaped)

    def test_only_a_higher_total_catches_up(self):
        outcome = v.resolve_chase(12, [11, 13, 12])
        self.assertEqual(outcome.caught_by, (False, True, False))
        self.assertFalse(outcome.escaped)

    def test_hindrance_is_capped_at_three(self):
        self.assertEqual(v.hindrance_bonus(1), 1)
        self.assertEqual(v.hindrance_bonus(5), 3)
        self.assertEqual(v.hindrance_bonus(2, botched=1), 1)

    def test_foot_chase_head_start_ladder(self):
        self.assertEqual(v.foot_chase_modifier(head_start="none"), 2)
        self.assertEqual(v.foot_chase_modifier(head_start="one_round"), 1)
        self.assertEqual(v.foot_chase_modifier(head_start="under_a_minute"), 0)
        self.assertEqual(v.foot_chase_modifier(head_start="over_a_minute"), -2)

    def test_foot_chase_combines_fixed_modifiers(self):
        total = v.foot_chase_modifier(
            more_pursuers_than_pursued=True, head_start="none", terrain_knowledge=-1,
            half_hearted=True, enraged=True,
        )
        self.assertEqual(total, 0)

    def test_terrain_knowledge_outside_the_band_is_refused(self):
        with self.assertRaises(v.VehicleError):
            v.foot_chase_modifier(terrain_knowledge=3)

    def test_vehicle_chase_flight_asymmetry(self):
        self.assertEqual(v.vehicle_chase_modifier(pursuer_flying=True), 3)
        self.assertEqual(v.vehicle_chase_modifier(pursued_flying=True), -3)
        self.assertEqual(v.vehicle_chase_modifier(pursuer_flying=True, pursued_flying=True), 0)

    def test_a_chase_needs_a_pursuer(self):
        with self.assertRaises(v.VehicleError):
            v.resolve_chase(10, [])


class RepairTests(unittest.TestCase):
    def test_one_hit_point_per_day_plus_fix_plus_drive(self):
        estimate = v.repair_estimate(v.vehicle("car"), 10, fix_skill=1, drive_skill=0)
        self.assertEqual(estimate.days, 5)
        self.assertEqual(estimate.cost, 2000)
        self.assertTrue(estimate.qualified)

    def test_an_ace_driver_pays_nothing(self):
        self.assertEqual(v.repair_estimate(v.vehicle("car"), 10, fix_skill=1, drive_skill=1,
                                           free_parts=True).cost, 0)

    def test_untrained_in_both_skills_cannot_repair(self):
        self.assertFalse(v.repair_estimate(v.vehicle("car"), 10, fix_skill=-1,
                                           drive_skill=0).qualified)

    def test_a_totalled_hull_cannot_be_repaired(self):
        estimate = v.repair_estimate(v.vehicle("car"), 30, fix_skill=3, drive_skill=3,
                                     current_hit_points=0)
        self.assertTrue(estimate.totaled)


class DataContractTests(unittest.TestCase):
    def test_the_contract_keeps_its_srd_citations_and_licence(self):
        raw = json.loads(v.VEHICLES_PATH.read_text(encoding="utf-8"))
        self.assertEqual(raw["source"]["licence"], "CC0")
        for key in ("vehicles", "repair", "fittings", "vehicle_mods", "combat", "chases"):
            self.assertIn(key, raw["source"]["sections"])


if __name__ == "__main__":
    unittest.main()
