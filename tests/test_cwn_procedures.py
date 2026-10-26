"""The CWN chassis procedures: combat, injury, strain, cyberware, hacking, advancement.

Each test states the rule it pins and the SRD section it comes from. The point is not coverage for
its own sake: the repository has already shipped one slice that passed its data suite while being
unplayable, so the arithmetic that decides whether a character lives, hacks, or levels up is pinned
here rather than discovered at a table.

The last test class compares the kernel's constants against ``data/rules/wn_core.json``, because two
sources of truth is how a band drifts.
"""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rules import wn_core as wn

CONTRACT = json.loads((ROOT / "data" / "rules" / "wn_core.json").read_text(encoding="utf-8"))


class AttackTests(unittest.TestCase):
    """CWN 2.4.1 - the attack roll."""

    def test_total_is_die_plus_bonus_plus_attribute_plus_skill(self) -> None:
        attack = wn.attack_roll(attack_bonus=2, attribute_modifier=1, skill_level=1,
                                target_ac=19, die=15)
        self.assertEqual(attack.total, 19)
        self.assertTrue(attack.success)

        misses = wn.attack_roll(attack_bonus=2, attribute_modifier=1, skill_level=1,
                                target_ac=20, die=15)
        self.assertFalse(misses.success)

    def test_natural_one_misses_and_natural_twenty_hits(self) -> None:
        self.assertFalse(wn.attack_roll(attack_bonus=20, target_ac=1, die=1).success)
        self.assertTrue(wn.attack_roll(attack_bonus=-5, target_ac=40, die=20).success)

    def test_untrained_attack_is_minus_two_not_minus_one(self) -> None:
        trained = wn.attack_roll(attack_bonus=0, target_ac=10, skill_level=0, die=10)
        untrained = wn.attack_roll(attack_bonus=0, target_ac=10, untrained=True, die=10)
        self.assertEqual(trained.total - untrained.total, 2)

    def test_situational_modifiers_are_clamped_to_the_ladder(self) -> None:
        attack = wn.attack_roll(attack_bonus=0, target_ac=10, die=10, situational=9)
        self.assertEqual(attack.situational, wn.SITUATIONAL_MAX)


class DamageShockTraumaTests(unittest.TestCase):
    """CWN 2.4.3 - damage, Shock and Trauma."""

    def setUp(self) -> None:
        self.pistol = wn.Weapon("light pistol", damage_count=1, damage_sides=6,
                                attribute="DEX", trauma_die=8, trauma_rating=2)
        self.knife = wn.Weapon("knife", damage_count=1, damage_sides=4, attribute="STR",
                               shock=1, shock_ac=15, trauma_die=6, trauma_rating=3)

    def test_a_hit_adds_the_attribute_modifier_to_damage(self) -> None:
        attack = wn.attack_roll(attack_bonus=0, target_ac=10, die=15)
        hit = wn.resolve_attack(attack, self.pistol, attribute_modifier=1,
                                damage_dice=(4,), trauma_roll=1)
        self.assertTrue(hit.hit)
        self.assertEqual(hit.damage, 5)
        self.assertFalse(hit.traumatic)

    def test_a_traumatic_hit_multiplies_the_whole_damage(self) -> None:
        attack = wn.attack_roll(attack_bonus=0, target_ac=10, die=15)
        hit = wn.resolve_attack(attack, self.pistol, attribute_modifier=1,
                                damage_dice=(4,), trauma_roll=6)
        self.assertTrue(hit.traumatic)
        self.assertEqual(hit.damage, 10)  # (4 + 1) x2

    def test_non_lethal_never_rolls_the_trauma_die(self) -> None:
        attack = wn.attack_roll(attack_bonus=0, target_ac=10, die=15)
        hit = wn.resolve_attack(attack, self.pistol, damage_dice=(4,), trauma_roll=3,
                                non_lethal=True)
        self.assertFalse(hit.traumatic)
        self.assertIsNone(hit.trauma_roll)

    def test_shock_lands_on_a_miss_when_the_targets_melee_ac_is_low_enough(self) -> None:
        miss = wn.attack_roll(attack_bonus=0, target_ac=14, die=2)
        hit = wn.resolve_attack(miss, self.knife, attribute_modifier=1, target_melee_ac=14)
        self.assertFalse(hit.hit)
        self.assertEqual(hit.total_damage, 2)  # Shock 1 + STR modifier 1
        self.assertFalse(hit.traumatic)

    def test_shock_does_not_land_on_a_well_armoured_target(self) -> None:
        miss = wn.attack_roll(attack_bonus=0, target_ac=17, die=2)
        hit = wn.resolve_attack(miss, self.knife, target_melee_ac=17)
        self.assertEqual(hit.total_damage, 0)

    def test_a_hit_can_never_do_less_than_its_shock(self) -> None:
        attack = wn.attack_roll(attack_bonus=0, target_ac=10, die=15)
        hit = wn.resolve_attack(attack, self.knife, attribute_modifier=1, damage_dice=(1,),
                                trauma_roll=1, target_melee_ac=10)
        self.assertEqual(hit.damage, 2)  # the Shock floor, not 1 + 1 - 2

    def test_damage_soak_absorbs_then_ablates(self) -> None:
        soak = wn.DamageSoak(5)
        self.assertEqual(soak.take(7), 2)
        self.assertTrue(soak.depleted)
        self.assertEqual(soak.take(4), 4)
        soak.refresh()
        self.assertEqual(soak.take(3), 0)


class InjuryTests(unittest.TestCase):
    """CWN 2.5.1 - 2.5.4 - mortal injury, stabilization and Major Injuries."""

    def test_a_mortal_wound_kills_at_the_end_of_the_sixth_round(self) -> None:
        wound = wn.MortalWound()
        for _round in range(wn.MORTAL_ROUNDS):
            self.assertFalse(wound.tick())
        self.assertTrue(wound.tick())
        self.assertTrue(wound.dead)

    def test_a_stabilized_wound_stops_the_clock(self) -> None:
        wound = wn.MortalWound()
        wound.tick()
        wound.stabilize()
        for _round in range(20):
            self.assertFalse(wound.tick())
        self.assertFalse(wound.dead)

    def test_recovery_is_one_hit_point_and_frailty(self) -> None:
        wound = wn.MortalWound()
        wound.stabilize()
        self.assertEqual(wound.recover(), 1)
        self.assertTrue(wound.frail)
        with self.assertRaises(wn.WnError):
            wn.MortalWound().recover()

    def test_stabilization_difficulty_counts_the_rounds_and_the_medkit(self) -> None:
        self.assertEqual(wn.stabilize_difficulty(0), 8)
        self.assertEqual(wn.stabilize_difficulty(3), 11)
        self.assertEqual(wn.stabilize_difficulty(0, has_tools=False), 10)

    def test_major_injury_needs_a_traumatic_hit_and_a_lethal_drop(self) -> None:
        self.assertTrue(wn.major_injury_risked(traumatic_hit_this_scene=True, lethal_zero_hp=True))
        self.assertFalse(wn.major_injury_risked(traumatic_hit_this_scene=False, lethal_zero_hp=True))
        self.assertFalse(wn.major_injury_risked(traumatic_hit_this_scene=True, lethal_zero_hp=False))

    def test_the_major_injury_table_is_clamped_to_its_twelve_rows(self) -> None:
        self.assertEqual(wn.major_injury(1), "instant_death")
        self.assertEqual(wn.major_injury(0), "instant_death")
        self.assertEqual(wn.major_injury(99), "flesh_wound")
        self.assertEqual(sorted(wn.MAJOR_INJURIES), list(range(1, 13)))


class StrainAndHealingTests(unittest.TestCase):
    """CWN 2.5.3 - 2.5.5 - System Strain, first aid and natural healing."""

    def test_the_maximum_is_the_constitution_score(self) -> None:
        strain = wn.SystemStrain(constitution=11)
        self.assertEqual(strain.maximum, 11)
        self.assertTrue(strain.can_accept(11))
        self.assertFalse(strain.can_accept(11.5))

    def test_an_effect_that_would_cross_the_maximum_is_unusable(self) -> None:
        strain = wn.SystemStrain(constitution=10, current=9)
        self.assertFalse(strain.add(2))
        self.assertEqual(strain.current, 9)
        self.assertTrue(strain.add(1))

    def test_an_unavoidable_overload_knocks_the_character_out(self) -> None:
        strain = wn.SystemStrain(constitution=10, current=9)
        self.assertTrue(strain.forced(3))
        self.assertFalse(wn.SystemStrain(constitution=10, current=1).forced(1))

    def test_permanent_cyberware_strain_cannot_exceed_the_maximum(self) -> None:
        strain = wn.SystemStrain(constitution=10, permanent=2.5)
        self.assertEqual(strain.permanent, 2.5)
        with self.assertRaises(wn.WnError):
            wn.SystemStrain(constitution=10, permanent=11)

    def test_rest_removes_one_point_and_no_more(self) -> None:
        strain = wn.SystemStrain(constitution=10, current=3)
        strain.rest_night()
        self.assertEqual(strain.current, 2)
        wn.SystemStrain(constitution=10, current=0).rest_night()

    def test_first_aid_adds_the_heal_skill_and_costs_one_strain(self) -> None:
        self.assertEqual(wn.first_aid_healing(heal_skill=2, die=4), 6)
        self.assertEqual(wn.first_aid_healing(heal_skill=None, die=4), 3)
        self.assertEqual(wn.FIRST_AID_STRAIN_COST, 1)

    def test_natural_healing_is_the_level_and_stops_while_frail(self) -> None:
        self.assertEqual(wn.natural_healing(level=4), 4)
        self.assertEqual(wn.natural_healing(level=4, frail=True), 0)
        self.assertEqual(wn.natural_healing(level=1, is_npc=True, hit_dice=3), 3)
        with self.assertRaises(wn.WnError):
            wn.natural_healing(level=1, is_npc=True)

    def test_frailty_can_be_attempted_in_the_field_at_difficulty_ten(self) -> None:
        self.assertEqual(wn.frail_field_removal_difficulty(), 10)


class CyberwareTests(unittest.TestCase):
    """CWN 3.6 - installation, maintenance and the optional alienation rule."""

    def test_installation_bands_follow_system_strain(self) -> None:
        self.assertEqual(wn.cyberware_installation(0)["difficulty"], 7)
        self.assertEqual(wn.cyberware_installation(0.4)["difficulty"], 8)
        self.assertEqual(wn.cyberware_installation(1.0)["difficulty"], 10)
        self.assertEqual(wn.cyberware_installation(2.5)["difficulty"], 11)
        self.assertEqual(wn.cyberware_installation(4)["difficulty"], 12)

    def test_installation_outcome_uses_the_margin(self) -> None:
        self.assertEqual(wn.installation_outcome(check_total=11, difficulty=11), "success")
        self.assertEqual(wn.installation_outcome(check_total=10, difficulty=11),
                         "success_with_complication")
        self.assertEqual(wn.installation_outcome(check_total=8, difficulty=11), "failure")

    def test_maintenance_is_five_percent_a_month(self) -> None:
        self.assertEqual(wn.cyberware_maintenance_cost(2000), 100.0)

    def test_alienation_turns_the_character_into_an_npc_only_past_wisdom(self) -> None:
        self.assertFalse(wn.alienation_exceeded(alienation=10, wisdom=10))
        self.assertTrue(wn.alienation_exceeded(alienation=11, wisdom=10))
        self.assertFalse(wn.alienation_exceeded(alienation=12, wisdom=10, syndrome_allowance=3))


class HackingTests(unittest.TestCase):
    """CWN 4.x - Access, security levels, connection penalties and the alert counter."""

    def test_access_is_intelligence_plus_program_plus_the_deck(self) -> None:
        self.assertEqual(wn.access_pool(intelligence_modifier=1, program_skill=2, deck_bonus=1), 4)
        self.assertEqual(wn.access_pool(intelligence_modifier=-2, program_skill=0), 0)

    def test_security_levels_and_situation_modifiers(self) -> None:
        self.assertEqual(wn.hacking_difficulty(8), 8)
        self.assertEqual(wn.hacking_difficulty(8, alerted=True), 9)
        self.assertEqual(wn.hacking_difficulty(8, important_device=True), 9)
        self.assertEqual(wn.hacking_difficulty(8, inside_info=3), 5)
        with self.assertRaises(wn.WnError):
            wn.hacking_difficulty(11)

    def test_cyberware_difficulty_scales_by_one_third_of_level(self) -> None:
        self.assertEqual(wn.cyber_hack_difficulty(level_or_hit_dice=1), 8)
        self.assertEqual(wn.cyber_hack_difficulty(level_or_hit_dice=3), 8)
        self.assertEqual(wn.cyber_hack_difficulty(level_or_hit_dice=4), 9)
        self.assertEqual(wn.cyber_hack_difficulty(level_or_hit_dice=9), 10)
        self.assertEqual(wn.cyber_hack_difficulty(level_or_hit_dice=4, has_operator=False), 8)

    def test_a_wireless_connection_costs_two_on_the_check(self) -> None:
        wired = wn.hacking_check(intelligence_score=12, program_skill=1, difficulty=8, dice=(3, 3))
        wireless = wn.hacking_check(intelligence_score=12, program_skill=1, difficulty=8,
                                    wireless=True, dice=(3, 3))
        self.assertEqual(wired.total - wireless.total, 2)
        crown = wn.hacking_check(intelligence_score=12, program_skill=1, difficulty=8,
                                 wireless=True, vr_crown=True, dice=(3, 3))
        self.assertEqual(wired.total - crown.total, 3)

    def test_an_untrained_hacker_takes_the_untrained_penalty(self) -> None:
        check = wn.hacking_check(intelligence_score=10, program_skill=None, difficulty=8, dice=(4, 4))
        self.assertTrue(check.untrained)
        self.assertEqual(check.total, 7)

    def test_two_failures_are_one_alert_and_two_alerts_alert_the_network(self) -> None:
        counter = wn.AlertCounter()
        self.assertFalse(counter.record_failure())   # one failure: nothing yet
        self.assertFalse(counter.record_failure())   # two failures: the first Alert action
        self.assertEqual(counter.alerts, 1)
        self.assertFalse(counter.alerted)
        self.assertFalse(counter.record_failure())
        self.assertTrue(counter.record_failure())    # fourth failure: the network is alerted
        self.assertEqual(counter.alerts, 2)
        self.assertTrue(counter.alerted)


class EncumbranceTests(unittest.TestCase):
    """CWN 2.3.x - Stowed and Readied capacity."""

    def test_capacity_is_strength_and_half_strength(self) -> None:
        self.assertEqual(wn.stowed_capacity(11), 11)
        self.assertEqual(wn.readied_capacity(11), 5)

    def test_overload_stages_cut_movement(self) -> None:
        self.assertEqual(wn.overload_stage(readied=5, stowed=11, strength=11), 0)
        self.assertEqual(wn.overload_stage(readied=7, stowed=11, strength=11), 1)
        self.assertEqual(wn.overload_stage(readied=9, stowed=11, strength=11), 2)
        self.assertEqual(wn.overload_stage(readied=12, stowed=11, strength=11), 3)
        self.assertEqual(wn.movement_for_stage(0), 10)
        self.assertEqual(wn.movement_for_stage(1), 7)
        self.assertEqual(wn.movement_for_stage(2), 5)
        self.assertEqual(wn.movement_for_stage(3), 0)


class AdvancementTests(unittest.TestCase):
    """CWN 1.9 - XP, skill points, attack bonus and hit points."""

    def test_xp_thresholds_on_both_tracks(self) -> None:
        self.assertEqual(wn.level_for_xp(0), 1)
        self.assertEqual(wn.level_for_xp(2), 1)
        self.assertEqual(wn.level_for_xp(3), 2)
        self.assertEqual(wn.level_for_xp(93), 10)
        self.assertEqual(wn.level_for_xp(500), 10)
        self.assertEqual(wn.level_for_xp(5, track="slow"), 1)
        self.assertEqual(wn.level_for_xp(6, track="slow"), 2)
        with self.assertRaises(wn.WnError):
            wn.level_for_xp(1, track="medium")

    def test_attack_bonus_is_half_level_unless_on_target(self) -> None:
        self.assertEqual(wn.attack_bonus(level=1), 0)
        self.assertEqual(wn.attack_bonus(level=5), 2)
        self.assertEqual(wn.attack_bonus(level=5, on_target_edge=True), 5)

    def test_skill_costs_and_minimum_levels(self) -> None:
        self.assertEqual([wn.skill_point_cost(i) for i in range(5)], [1, 2, 3, 4, 5])
        self.assertEqual([wn.minimum_level_for_skill(i) for i in range(5)], [1, 1, 3, 6, 9])
        with self.assertRaises(wn.WnError):
            wn.skill_point_cost(5)

    def test_hit_points_roll_per_level_and_only_rise(self) -> None:
        self.assertEqual(wn.hit_points_gain(level=1, constitution_modifier=1, dice=(4,)), 5)
        self.assertEqual(wn.hit_points_gain(level=2, constitution_modifier=1, dice=(1, 1)), 4)
        self.assertEqual(
            wn.hit_points_gain(level=2, constitution_modifier=1, dice=(1, 1), current_maximum=9), 1)
        self.assertEqual(wn.hit_points_gain(level=2, constitution_modifier=-3, dice=(1, 1)), 2)


class ContractAgreesWithProceduresTests(unittest.TestCase):
    """``data/rules/wn_core.json`` and the kernel must not drift apart."""

    def test_combat_numbers_match(self) -> None:
        combat = CONTRACT["combat"]
        self.assertEqual(wn.UNSKILLED_ATTACK_PENALTY, combat["attack"]["unskilled_penalty"])
        self.assertEqual(wn.DEFAULT_TRAUMA_TARGET, combat["trauma"]["default_target"])
        self.assertEqual(wn.ATTACK_MOVEMENT_METERS, combat["actions"]["movement_meters"])
        self.assertEqual(wn.MORTAL_ROUNDS, combat["mortal_injury"]["rounds_until_death"])
        self.assertEqual(combat["mortal_injury"]["stabilize"]["no_tools_penalty"], 2)
        table = {int(k): v for k, v in combat["major_injury"]["table"].items()}
        self.assertEqual(table, wn.MAJOR_INJURIES)

    def test_strain_and_healing_match(self) -> None:
        self.assertEqual(CONTRACT["strain"]["maximum"], "CON score")
        self.assertEqual(wn.FIRST_AID_STRAIN_COST, CONTRACT["healing"]["first_aid"]["strain_cost"])
        self.assertEqual(CONTRACT["healing"]["frail_removal"]["bed_rest_days"], 7)

    def test_cyberware_bands_match(self) -> None:
        bands = CONTRACT["cyberware"]["installation"]["difficulty_by_strain"]
        kernel = [(None if b[0] is None else float(b[0]), b[1], b[2]) for b in wn.CYBERWARE_INSTALLATION]
        contract = [(None if b["max_strain"] is None else float(b["max_strain"]),
                     b["difficulty"], b["cost"]) for b in bands]
        self.assertEqual(kernel, contract)
        self.assertEqual(wn.CYBERWARE_MAINTENANCE_FRACTION,
                         CONTRACT["cyberware"]["maintenance"]["monthly_cost_fraction_of_base"])

    def test_hacking_numbers_match(self) -> None:
        hacking = CONTRACT["hacking"]
        self.assertEqual(wn.WIRELESS_PENALTY, hacking["connection"]["wireless"]["penalty"])
        self.assertEqual(wn.VR_CROWN_PENALTY, hacking["connection"]["vr_crown"]["penalty"])
        self.assertEqual(sorted(wn.HACK_SECURITY_LEVELS), sorted(int(k) for k in hacking["security_levels"]))
        self.assertEqual(wn.HACK_FAILURES_PER_ALERT, hacking["alert"]["failures_per_alert_action"])
        self.assertEqual(wn.ALERTS_TO_ALERT_NETWORK, hacking["alert"]["alert_actions_to_alert_network"])
        self.assertEqual(hacking["connection"]["wireless"]["range_meters"], 30)

    def test_advancement_numbers_match(self) -> None:
        advancement = CONTRACT["advancement"]
        self.assertEqual(list(wn.XP_FAST), advancement["xp"]["fast"])
        self.assertEqual(list(wn.XP_SLOW), advancement["xp"]["slow"])
        self.assertEqual(wn.MAX_LEVEL, advancement["max_level"])
        self.assertEqual(wn.SKILL_POINTS_PER_LEVEL, advancement["skill_points_per_level"])
        self.assertEqual(wn.FOCUS_LEVELS, tuple(advancement["focus_levels"]))
        self.assertEqual(wn.THIRD_EDGE_LEVEL, advancement["third_edge_level"])
        costs = [(c["level"], c["points"], c["min_character_level"]) for c in advancement["skill_costs"]]
        self.assertEqual(costs, list(wn.SKILL_COSTS))

    def test_skill_vocabulary_matches(self) -> None:
        self.assertEqual(tuple(CONTRACT["skills"]["list"]), wn.SKILLS)
        self.assertEqual(tuple(CONTRACT["skills"]["psionic_skills"]), wn.PSIONIC_SKILLS)
        self.assertEqual(CONTRACT["skills"]["untrained_modifier"], wn.UNSKILLED_PENALTY)
        self.assertEqual(CONTRACT["skills"]["untrained_attack_modifier"], wn.UNSKILLED_ATTACK_PENALTY)

    def test_encumbrance_matches(self) -> None:
        self.assertEqual(CONTRACT["encumbrance"]["stowed_capacity"], "STR score")
        self.assertEqual(CONTRACT["encumbrance"]["readied_capacity"], "floor(STR / 2)")


if __name__ == "__main__":
    unittest.main()
