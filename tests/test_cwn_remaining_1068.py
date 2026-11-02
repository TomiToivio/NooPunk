"""The CWN rules that were missing or unverified (#1068).

Each class pins the numbers from the Cities Without Number SRD (public domain) and the boundary
behaviour that a table would notice: a failed operation, a failed stabilization, a barrier on a link.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))

from nopunk_mud.cwn import chase, combat_mods, cyberware, economy, hacking, injury  # noqa: E402


class HackingIsAMap(unittest.TestCase):
    def test_access_is_intelligence_plus_program_plus_deck(self):
        deck = hacking.Cyberdeck("scrapdeck", bonus_access=1, memory=6, cpu=3, shielding=5)
        self.assertEqual(hacking.access_score(2, 1, deck), 4)

    def test_a_deck_cannot_run_more_programs_than_its_cpu(self):
        deck = hacking.Cyberdeck("scrapdeck", cpu=1)
        program = hacking.Program(verb="Blind", subject="Camera")
        with self.assertRaises(hacking.HackingError):
            hacking.run_program(program=program, deck=deck, running=1, access_available=5,
                                security=8, total=10)

    def test_a_program_that_costs_more_access_than_you_have_is_refused(self):
        deck = hacking.Cyberdeck("scrapdeck", cpu=2)
        program = hacking.Program(verb="Sabotage", subject="Camera", access_cost=3)
        with self.assertRaises(hacking.HackingError):
            hacking.run_program(program=program, deck=deck, running=0, access_available=2,
                                security=8, total=10)

    def test_wireless_costs_two_and_a_vr_crown_another_one(self):
        self.assertEqual(hacking.connection_penalty(wireless=True, vr_crown=True), -3)
        self.assertEqual(hacking.connection_penalty(), 0)

    def test_a_guarded_link_refuses_the_hop_until_the_barrier_is_down(self):
        net = hacking.Cyberspace(security=9)
        net.add_node("camera", neighbours={"panel"})
        net.barriers[frozenset({"camera", "panel"})] = 10
        blocked = hacking.move_node(net, from_node="camera", to_node="panel")
        self.assertFalse(blocked["moved"])
        self.assertEqual(blocked["difficulty"], 10)
        self.assertTrue(hacking.move_node(net, from_node="camera", to_node="panel",
                                          barrier_defeated=True)["moved"])

    def test_an_unlinked_node_is_not_reachable(self):
        net = hacking.Cyberspace(security=9)
        net.add_node("camera")
        net.add_node("vault")
        self.assertFalse(hacking.move_node(net, from_node="camera", to_node="vault")["moved"])

    def test_every_two_failures_raise_one_alert(self):
        net = hacking.Cyberspace(security=9)
        program = hacking.Program(verb="Blind", subject="Camera")
        deck = hacking.Cyberdeck("deck", cpu=4)
        results = [
            hacking.run_program(program=program, deck=deck, running=0, access_available=5,
                                security=9, total=1, network=net)
            for _ in range(4)
        ]
        self.assertEqual([r["alert"] for r in results], [0, 1, 0, 1])
        self.assertEqual(net.alerts, 2)

    def test_a_persistent_program_holds_cpu_but_a_transient_one_does_not(self):
        deck = hacking.Cyberdeck("deck", cpu=4)
        persistent = hacking.Program(verb="Activate", subject="Camera", persistent=True)
        transient = hacking.Program(verb="Blind", subject="Camera")
        self.assertEqual(hacking.run_program(program=persistent, deck=deck, running=0,
                                             access_available=5, security=5, total=20)["cpu_held"], 1)
        self.assertEqual(hacking.run_program(program=transient, deck=deck, running=0,
                                             access_available=5, security=5, total=20)["cpu_held"], 0)


class Surgery(unittest.TestCase):
    def test_cost_recovery_and_difficulty_follow_the_strain_band(self):
        self.assertEqual(cyberware.install_difficulty(0), 7)
        self.assertEqual(cyberware.install_difficulty(0.5), 8)
        self.assertEqual(cyberware.install_difficulty(1.0), 10)
        self.assertEqual(cyberware.install_difficulty(3.0), 11)
        self.assertEqual(cyberware.install_difficulty(3.1), 12)
        self.assertEqual(cyberware.install_cost(0), 100)
        self.assertEqual(cyberware.install_cost(3.1), 50_000)
        self.assertEqual(cyberware.recovery_time(0.5), "1 day")

    def test_the_theatre_and_a_new_implant_modify_the_check(self):
        self.assertEqual(cyberware.surgery_modifier(circumstances=["cyberdoc_kit"]), -1)
        self.assertEqual(cyberware.surgery_modifier(circumstances=["theater_2", "new_implant"]), 2)

    def test_failing_by_more_than_two_maxes_strain_and_drops_to_one_hp(self):
        outcome = cyberware.install_outcome(margin=-3, strain=1.0)
        self.assertFalse(outcome.success)
        self.assertTrue(outcome.strain_maxed)
        self.assertEqual(outcome.hp_set_to, 1)

    def test_failing_by_one_or_two_installs_but_complicates(self):
        outcome = cyberware.install_outcome(margin=-2, strain=1.0)
        self.assertTrue(outcome.success)
        self.assertTrue(outcome.complication)

    def test_a_failed_careful_removal_ruins_the_implant_but_not_the_patient(self):
        outcome = cyberware.remove_outcome(margin=-1, patient_alive=True)
        self.assertTrue(outcome.success)
        self.assertFalse(outcome.implant_reusable)

    def test_salvage_from_the_dead_can_fail(self):
        self.assertFalse(cyberware.remove_outcome(margin=-1, patient_alive=False).implant_reusable)

    def test_skillplugs_cost_double_for_physical_skills_and_level_three_is_mission_only(self):
        self.assertEqual(cyberware.skillplug_price(1), 10_000)
        self.assertEqual(cyberware.skillplug_price(1, physical=True), 20_000)
        self.assertIsNone(cyberware.skillplug_price(3))

    def test_a_natural_two_locks_the_jack_and_extra_plugs_widen_the_range(self):
        self.assertTrue(cyberware.skillplug_check_fails(die=2, attack=False, plugs_running=1))
        self.assertFalse(cyberware.skillplug_check_fails(die=3, attack=False, plugs_running=1))
        self.assertTrue(cyberware.skillplug_check_fails(die=3, attack=False, plugs_running=2))

    def test_concealment_grades_differ_by_method(self):
        self.assertFalse(cyberware.detectability("medical", method="visual"))
        self.assertTrue(cyberware.detectability("medical", method="cyber_scanner"))
        self.assertTrue(cyberware.detectability("touch", method="touch"))
        self.assertFalse(cyberware.detectability("touch", method="visual"))
        self.assertTrue(cyberware.detectability("sight", method="visual"))


class Mortality(unittest.TestCase):
    def test_six_rounds_without_stabilization_kills(self):
        state = injury.MortalState()
        for _ in range(6):
            state.tick()
        self.assertTrue(state.is_dead)

    def test_stabilization_difficulty_grows_with_the_round_and_the_missing_kit(self):
        self.assertEqual(injury.stabilization_difficulty(rounds_since_fall=0), 8)
        self.assertEqual(injury.stabilization_difficulty(rounds_since_fall=3, has_medkit=False), 13)

    def test_a_stabilized_victim_recovers_with_one_hp_and_frail(self):
        state = injury.MortalState()
        state.tick()
        self.assertTrue(injury.try_stabilize(state, total=12))
        self.assertEqual(injury.recover(state), {"hit_points": 1, "frail": True})

    def test_zero_hit_points_while_frail_is_death(self):
        state = injury.MortalState(stabilized=True, frail=True)
        injury.zero_hit_points_while_frail(state)
        self.assertTrue(state.is_dead)

    def test_frailty_clears_with_rest_or_a_difficulty_ten_check(self):
        state = injury.MortalState(frail=True)
        self.assertFalse(injury.clear_frailty(state, method="physician", total=9))
        self.assertTrue(injury.clear_frailty(state, method="physician", total=10))
        state.frail = True
        self.assertTrue(injury.clear_frailty(state, method="rest"))

    def test_major_injury_table_is_clamped_and_flagged(self):
        self.assertEqual(injury.major_injury(0)["roll"], 1)
        self.assertTrue(injury.major_injury(1)["lethal"])
        self.assertEqual(injury.major_injury(13)["roll"], 12)
        self.assertFalse(injury.major_injury(12)["lethal"])
        self.assertTrue(injury.major_injury(6)["limb_lost"])

    def test_non_lethal_incapacitation_does_not_cause_frailty(self):
        self.assertEqual(injury.nonlethal_incapacitation(), {"minutes": 10, "hit_points": 1, "frail": False})


class Chases(unittest.TestCase):
    def test_helpers_add_one_each_to_a_maximum_of_three(self):
        self.assertEqual(chase.helper_bonus(2), 2)
        self.assertEqual(chase.helper_bonus(9), 3)

    def test_head_start_and_number_modify_the_pursuit(self):
        result = chase.foot_pursuit(pursuer_total=8, pace=10,
                                    situations=["one_round_head_start", "more_pursuers_than_pursued"])
        self.assertEqual(result["total"], 8)
        self.assertFalse(result["caught"])

    def test_vehicle_chase_resolves_each_pursuer_separately(self):
        outcome = chase.resolve_vehicle_chase(pace=11, pursuers={"black saloon": 12, "drone": 9})
        self.assertEqual(outcome["caught"], ["black saloon"])
        self.assertEqual(outcome["lost"], ["drone"])

    def test_an_unknown_situation_is_refused(self):
        with self.assertRaises(chase.ChaseError):
            chase.foot_pursuit(pursuer_total=5, pace=5, situations=["plot_armour"])


class AttackModifiers(unittest.TestCase):
    def test_cover_and_range_stack(self):
        result = combat_mods.attack_total(die=10, base_attack=1, attribute_modifier=1, combat_skill=1,
                                          circumstances=["target_half_cover", "beyond_normal_range"])
        self.assertEqual(result["total"], 9)

    def test_an_impossible_shot_raises_rather_than_returning_a_bonus(self):
        with self.assertRaises(combat_mods.CombatRuleError):
            combat_mods.attack_total(die=10, base_attack=1, attribute_modifier=0, combat_skill=1,
                                     circumstances=["two_handed_gun_in_melee"])

    def test_being_unskilled_costs_two(self):
        result = combat_mods.attack_total(die=10, base_attack=0, attribute_modifier=0, combat_skill=-1)
        self.assertEqual(result["total"], 8)
        self.assertTrue(result["unskilled"])

    def test_a_gunlink_ignores_two_points_of_cover(self):
        plain = combat_mods.attack_total(die=10, base_attack=0, attribute_modifier=0, combat_skill=1,
                                         circumstances=["target_almost_full_cover"])
        linked = combat_mods.attack_total(die=10, base_attack=0, attribute_modifier=0, combat_skill=1,
                                          circumstances=["target_almost_full_cover"], gunlink=True)
        self.assertEqual(linked["total"] - plain["total"], 2)

    def test_size_penalties_apply_to_opposed_maneuvers(self):
        self.assertFalse(combat_mods.opposed_maneuver(attacker_total=10, defender_total=10,
                                                      target_size="quadruped"))

    def test_dual_wielding_adds_two_damage_but_not_to_shock(self):
        result = combat_mods.dual_wield(damage=5, shock=2)
        self.assertEqual(result["damage"], 7)
        self.assertEqual(result["shock"], 2)

    def test_dual_wielding_needs_level_one(self):
        with self.assertRaises(combat_mods.CombatRuleError):
            combat_mods.dual_wield(damage=5, weapon_ranks=(0, 1))


class Wages(unittest.TestCase):
    def test_the_table_is_the_srd_table(self):
        table = economy.wages()
        self.assertEqual(table["unskilled_street_laborer"], 10)
        self.assertEqual(table["street_cop_or_skilled_corp_worker"], 100)
        self.assertEqual(table["oligarchic_elite_of_a_city"], 10_000)
        self.assertEqual(len(table), 18)

    def test_hiring_is_per_day_and_budgeted(self):
        self.assertEqual(economy.hire_cost("competent_street_bodyguard", 3), 150)
        self.assertEqual(economy.affordable_hirelings(200, "competent_street_bodyguard", 1), 4)

    def test_an_unknown_role_is_refused(self):
        with self.assertRaises(economy.WageError):
            economy.daily_wage("freelance philosopher")


if __name__ == "__main__":
    unittest.main()
