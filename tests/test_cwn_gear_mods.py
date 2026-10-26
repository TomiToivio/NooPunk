"""Behavioural tests for CWN crafting, gear mods and mod maintenance (SRD 2.8).

Code-only, per AGENTS.md and #271. Each test names the rule it pins.
"""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules import cwn_equipment
from src.rules import cwn_gear_mods as m


class MaintenanceTests(unittest.TestCase):
    def test_score_is_int_plus_con_plus_three_times_fix(self):
        self.assertEqual(m.maintenance_score(1, -1, 1), 3)
        self.assertEqual(m.maintenance_score(0, 0, 0), 0)

    def test_full_time_maintenance_doubles_the_score(self):
        self.assertEqual(m.maintenance_score(1, 0, 2, full_time=True), 14)

    def test_a_negative_total_is_none_not_negative(self):
        self.assertEqual(m.maintenance_score(-2, -2, 0), 0)

    def test_untrained_fix_cannot_maintain_anything(self):
        with self.assertRaises(m.ModError):
            m.maintenance_score(0, 0, -1)

    def test_maintenance_requires_the_build_skill(self):
        dampers = m.armor_mod("trauma_dampers")  # Fix-3
        self.assertFalse(m.can_maintain(2, dampers))
        self.assertTrue(m.can_maintain(3, dampers))

    def test_lapse_clocks_are_24_hours_and_7_days(self):
        self.assertEqual(m.maintenance_lapse(hours_without=23), "working")
        self.assertEqual(m.maintenance_lapse(hours_without=24), "mod_dead")
        self.assertEqual(m.maintenance_lapse(hours_without=24 * 7), "item_dead")


class CraftingTests(unittest.TestCase):
    def test_jury_rigged_is_half_time_and_quarter_parts(self):
        plan = m.craft_plan("jury_rigged", 1000)
        self.assertEqual(plan.days, 4)
        self.assertEqual(plan.parts_cost, 250)
        self.assertEqual(plan.stops_after_hours, 24)
        self.assertFalse(plan.further_modding)

    def test_mastercrafted_is_ten_times_parts_and_twice_the_time(self):
        plan = m.craft_plan("mastercrafted", 1000)
        self.assertEqual(plan.days, 14)
        self.assertEqual(plan.parts_cost, 10000)
        self.assertTrue(plan.first_mod_needs_no_maintenance)

    def test_a_vehicle_takes_a_month_to_build(self):
        self.assertEqual(m.craft_plan("normal", 5000, vehicle=True).days, 30)

    def test_factory_modding_multiplies_the_mod_price_and_each_component_doubles_it(self):
        self.assertEqual(m.factory_price(1000, 1000, 0), 6000)
        self.assertEqual(m.factory_price(1000, 1000, 1), 12000)
        self.assertEqual(m.factory_price(1000, 1000, 2), 24000)

    def test_install_time_is_one_week_per_minimum_skill_level(self):
        self.assertEqual(m.install_weeks(m.weapon_mod("customized")), 1)      # Fix-1
        self.assertEqual(m.install_weeks(m.weapon_mod("predictive_guidance")), 3)  # Fix-3

    def test_an_assistant_and_obsession_halve_install_time(self):
        mod = m.weapon_mod("predictive_guidance")
        self.assertEqual(m.install_weeks(mod, assistant=True), 2)
        self.assertEqual(m.install_weeks(mod, obsessive=True), 2)
        self.assertEqual(m.install_weeks(mod, assistant=True, obsessive=True), 1)

    def test_install_time_never_rounds_down_to_zero_weeks(self):
        self.assertGreaterEqual(m.install_weeks(m.weapon_mod("customized"), assistant=True), 1)


class WeaponModTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pistol = cwn_equipment.damage_profile("light_pistol")

    def test_customized_adds_one_to_hit(self):
        result = m.apply_weapon_mods(self.pistol, ["customized"])
        self.assertEqual(result.hit_bonus, 1)
        self.assertEqual(result.describe()["mod_hit_bonus"], 1)

    def test_extended_magazine_doubles_capacity(self):
        self.assertEqual(m.apply_weapon_mods(self.pistol, ["extended_mag"]).magazine_multiplier, 2)

    def test_shock_burst_is_uncapped_and_reported_separately(self):
        result = m.apply_weapon_mods(self.pistol, ["shock_burst"])
        self.assertEqual(result.uncapped_damage, "2d6")
        self.assertEqual(result.damage_bonus, 0)

    def test_a_connection_mod_is_installed_but_inactive_without_a_gunlink(self):
        result = m.apply_weapon_mods(self.pistol, ["autotargeting"], connected=False)
        self.assertEqual(result.hit_bonus, 0)
        self.assertEqual(result.inactive, ("autotargeting",))
        connected = m.apply_weapon_mods(self.pistol, ["autotargeting"], connected=True)
        self.assertEqual(connected.hit_bonus, 1)

    def test_stun_rounds_halve_range_drop_two_damage_and_remove_the_trauma_die(self):
        result = m.apply_weapon_mods(self.pistol, ["stun_rounds"])
        self.assertEqual(result.range_multiplier, 0.5)
        self.assertEqual(result.damage_bonus, -2)
        self.assertTrue(result.loses_trauma_die)
        self.assertTrue(result.nonlethal)
        self.assertEqual(result.describe()["trauma_die"], 0)

    def test_heavy_sabot_grants_vehicle_trauma(self):
        self.assertTrue(m.apply_weapon_mods(self.pistol, ["heavy_sabot"]).vehicle_trauma)

    def test_a_melee_only_mod_is_refused_on_a_firearm(self):
        with self.assertRaises(m.ModError):
            m.apply_weapon_mods(self.pistol, ["integral_toxins"])

    def test_a_melee_mod_applies_to_a_melee_weapon(self):
        knife = cwn_equipment.damage_profile("knife")
        result = m.apply_weapon_mods(knife, ["savage_impact"], category="melee")
        self.assertEqual(result.damage_bonus, 1)
        self.assertEqual(result.shock_bonus, 1)

    def test_a_mod_may_be_applied_only_once(self):
        with self.assertRaises(m.ModError):
            m.apply_weapon_mods(self.pistol, ["customized", "customized"])

    def test_hit_and_damage_bonuses_never_exceed_the_three_point_cap(self):
        combos = itertools.combinations(
            ["customized", "autotargeting", "predictive_guidance"], 2
        )
        for combo in combos:
            result = m.apply_weapon_mods(self.pistol, list(combo), connected=True)
            self.assertLessEqual(result.hit_bonus, m.MOD_BONUS_CAP["hit"])
        full = m.apply_weapon_mods(self.pistol, ["customized", "autotargeting",
                                                 "predictive_guidance"], connected=True)
        self.assertEqual(full.hit_bonus, 3)
        self.assertEqual(full.damage_bonus, 1)


class ArmorModTests(unittest.TestCase):
    def setUp(self) -> None:
        self.coat = cwn_equipment.armor_piece("ordinary_clothing")

    def test_absorption_pads_add_five_soak(self):
        self.assertEqual(m.apply_armor_mods(self.coat, ["absorption_pads"]).damage_soak, 5)

    def test_trauma_dampers_require_absorption_pads_first(self):
        with self.assertRaises(m.ModError):
            m.apply_armor_mods(self.coat, ["trauma_dampers"])
        stacked = m.apply_armor_mods(self.coat, ["absorption_pads", "trauma_dampers"])
        self.assertEqual(stacked.damage_soak, 10)

    def test_customized_adds_one_to_both_armor_classes(self):
        result = m.apply_armor_mods(self.coat, ["customized"])
        self.assertEqual(result.ac_ranged, int(self.coat["ac_ranged"]) + 1)
        self.assertEqual(result.ac_melee, int(self.coat["ac_melee"]) + 1)

    def test_tailored_rig_adds_encumbrance_capacity(self):
        result = m.apply_armor_mods(self.coat, ["tailored_rig"])
        self.assertEqual((result.readied_bonus, result.stowed_bonus), (1, 2))

    def test_whisperlight_reduces_encumbrance_without_going_negative(self):
        self.assertEqual(m.apply_armor_mods(self.coat, ["whisperlight"]).encumbrance, 0)

    def test_active_response_raises_the_wearers_trauma_target(self):
        self.assertEqual(m.apply_armor_mods(self.coat, ["active_response"]).trauma_target_modifier, 1)


class DroneAndDeckModTests(unittest.TestCase):
    def test_redundant_systems_raises_drone_hit_points_by_a_quarter(self):
        out = m.apply_drone_mods({"ac": 15, "move": 20, "hit_points": 8, "encumbrance": 3},
                                 ["redundant_systems"])
        self.assertEqual(out["hit_points"], 10)
        self.assertEqual(out["encumbrance"], 4)

    def test_heavy_plating_trades_speed_for_armor(self):
        out = m.apply_drone_mods({"ac": 13, "move": 20, "hit_points": 5, "encumbrance": 3},
                                 ["heavy_plating"])
        self.assertEqual((out["ac"], out["move"]), (15, 15))

    def test_stripped_fittings_never_drops_encumbrance_below_one(self):
        out = m.apply_drone_mods({"encumbrance": 1, "fittings": 2}, ["stripped_fittings"])
        self.assertEqual(out["encumbrance"], 1)
        self.assertEqual(out["fittings"], 1)

    def test_deck_mods_add_cpu_memory_and_shielding(self):
        out = m.apply_deck_mods({"cpu": 2, "memory": 8, "shielding": 5, "bonus_access": 1},
                                ["cpu_overclocking", "memory_expansion", "buffer_circuits"])
        self.assertEqual((out["cpu"], out["memory"], out["shielding"]), (3, 12, 10))

    def test_polymorphic_algorithms_trade_cpu_for_access(self):
        out = m.apply_deck_mods({"cpu": 3, "bonus_access": 1}, ["polymorphic_intrusion_algorithms"])
        self.assertEqual((out["cpu"], out["bonus_access"]), (2, 2))

    def test_percentage_priced_mods_need_the_item_cost(self):
        self.assertEqual(m.deck_mod("cpu_overclocking").price(10000), 3000)
        with self.assertRaises(m.ModError):
            m.deck_mod("cpu_overclocking").price(0)


if __name__ == "__main__":
    unittest.main()
