"""Cyberware operations — every assertion traced to the CWN SRD section it pins.

SRD (CC0) sections: 3.6.1 installation, 3.6.1.1 implant complications, 3.6.2 removal and salvage,
3.6.3 concealment, 3.6.4 maintenance, 3.6.5 skillplugs, 3.6.6 cyberware mods, 3.6.7 the systems
catalogue, 3.6.8 Alienation.

Written as ``unittest`` on purpose: CI runs ``unittest discover`` against ``requirements.txt``,
which does not install pytest (see ``references/multi-agent-pr-and-ci-traps.md``).
"""
import json
import tempfile
import unittest
from pathlib import Path

from src.rules import cwn_cyberware as cw


class InstallationModifierTests(unittest.TestCase):
    """SRD 3.6.1: the equipment/room table."""

    def test_a_cyberdoc_kit_alone_is_minus_one(self) -> None:
        self.assertEqual(cw.surgery_check_modifier(theatre_level=0), -1)

    def test_theatre_grades_are_zero_one_two(self) -> None:
        self.assertEqual(cw.surgery_check_modifier(theatre_level=1), 0)
        self.assertEqual(cw.surgery_check_modifier(theatre_level=2), 1)
        self.assertEqual(cw.surgery_check_modifier(theatre_level=3), 2)

    def test_room_quality_table(self) -> None:
        self.assertEqual(cw.surgery_check_modifier(room="lacks_room"), -1)
        self.assertEqual(cw.surgery_check_modifier(room="clean_room"), 0)
        self.assertEqual(cw.surgery_check_modifier(room="sterile_operating_room"), 1)
        self.assertEqual(cw.surgery_check_modifier(room="medical_clinic"), 2)

    def test_new_cyber_and_a_manufacturers_kit_each_add_one(self) -> None:
        self.assertEqual(cw.surgery_check_modifier(new_cyber=True), 1)
        self.assertEqual(cw.surgery_check_modifier(manufacturers_kit=True), 1)

    def test_a_clinic_operating_on_new_cyber_stacks(self) -> None:
        self.assertEqual(
            cw.surgery_check_modifier(theatre_level=3, room="medical_clinic", new_cyber=True),
            5,
        )

    def test_unknown_theatre_or_room_raises_instead_of_guessing(self) -> None:
        with self.assertRaises(cw.CyberwareError):
            cw.surgery_check_modifier(theatre_level=4)
        with self.assertRaises(cw.CyberwareError):
            cw.surgery_check_modifier(room="dirty_garage")

    def test_difficulty_is_flat_and_comes_from_the_core_table(self) -> None:
        self.assertEqual(cw.surgery_difficulty(0.0), 7)
        self.assertEqual(cw.surgery_difficulty(0.25), 8)
        self.assertEqual(cw.surgery_difficulty(0.5), 8)
        self.assertEqual(cw.surgery_difficulty(1.0), 10)
        self.assertEqual(cw.surgery_difficulty(2.0), 11)
        self.assertEqual(cw.surgery_difficulty(4.0), 12)

    def test_a_second_attempt_carries_a_cumulative_minus_one(self) -> None:
        self.assertEqual(cw.installation_attempt_penalty(1), 0)
        self.assertEqual(cw.installation_attempt_penalty(2), -1)
        self.assertEqual(cw.installation_attempt_penalty(3), -2)

    def test_donated_work_halves_the_installation_cost(self) -> None:
        self.assertEqual(cw.installation_cost(1.0), 2_500)
        self.assertEqual(cw.installation_cost(1.0, surgeon_donates=True), 1_250)


class ImplantComplicationTests(unittest.TestCase):
    """SRD 3.6.1.1: the d12 table and its substitute-12 rule."""

    def test_the_table_has_twelve_distinct_rows(self) -> None:
        self.assertEqual(sorted(cw.COMPLICATIONS), list(range(1, 13)))
        ids = {row["id"] for row in cw.COMPLICATIONS.values()}
        self.assertEqual(len(ids), 12)

    def test_inefficient_costs_an_extra_half_point_of_strain(self) -> None:
        self.assertEqual(cw.complication(2)["id"], "inefficient")
        self.assertEqual(cw.complication_extra_strain(2), 0.5)

    def test_uncooperative_only_costs_strain_when_a_category_is_shared(self) -> None:
        self.assertEqual(cw.complication_extra_strain(8, shares_category=True), 1.0)
        self.assertEqual(cw.complication_extra_strain(8, shares_category=False), 0.0)

    def test_a_complication_that_cannot_apply_becomes_row_twelve(self) -> None:
        row = cw.complication(3, applies=False)
        self.assertEqual(row["used"], 12)
        self.assertTrue(row["substituted"])
        self.assertEqual(row["id"], "petty_annoyance")

    def test_a_roll_outside_the_d12_raises(self) -> None:
        for bad in (0, 13, -1):
            with self.assertRaises(cw.CyberwareError):
                cw.complication(bad)

    def test_debilitating_names_the_penalty_rather_than_applying_it_silently(self) -> None:
        row = cw.complication(7)
        self.assertIn("1d2", row["hook"])
        self.assertEqual(row["extra_strain"], 0.0)


class RemovalTests(unittest.TestCase):
    """SRD 3.6.2: removal, ungentle disassembly, salvage and re-use grading."""

    def test_gentle_removal_takes_an_hour_at_the_installation_difficulty(self) -> None:
        terms = cw.removal_terms(11)
        self.assertEqual(terms["minutes"], 60)
        self.assertEqual(terms["difficulty"], 11)
        self.assertTrue(terms["check_required"])

    def test_a_doc_who_does_not_care_takes_ten_minutes_and_rolls_nothing(self) -> None:
        terms = cw.removal_terms(11, gentle=False)
        self.assertEqual(terms["minutes"], 10)
        self.assertFalse(terms["check_required"])
        self.assertFalse(terms["patient_survives"])

    def test_gentle_removal_keeps_the_implant_on_a_success_and_the_patient_either_way(self) -> None:
        self.assertTrue(cw.resolve_removal(11, 11)["implant_intact"])
        failed = cw.resolve_removal(9, 11)
        self.assertFalse(failed["implant_intact"])
        self.assertTrue(failed["patient_healthy"])
        self.assertTrue(failed["system_strain_removed"])

    def test_brutal_removal_only_spares_a_minimally_invasive_system(self) -> None:
        self.assertTrue(cw.resolve_brutal_removal(minimally_invasive=True)["patient_survives"])
        self.assertFalse(cw.resolve_brutal_removal(minimally_invasive=False)["patient_survives"])

    def test_salvage_is_impossible_after_twenty_four_hours(self) -> None:
        self.assertFalse(cw.resolve_salvage(99, hours_dead=24.5)["recovered"])
        self.assertTrue(cw.resolve_salvage(10, hours_dead=2)["recovered"])
        self.assertFalse(cw.resolve_salvage(9, hours_dead=2)["recovered"])

    def test_reuse_grade_depends_on_a_difficulty_ten_check(self) -> None:
        self.assertEqual(cw.resolve_reuse(10)["state"], "used")
        secondhand = cw.resolve_reuse(9)
        self.assertEqual(secondhand["state"], "secondhand")
        self.assertTrue(secondhand["complication_required"])


class ConcealmentTests(unittest.TestCase):
    """SRD 3.6.3: what each inspection method finds."""

    def test_ranks_are_ordered_from_concealed_to_blatant(self) -> None:
        self.assertEqual(cw.concealment_rank("Medical"), 0)
        self.assertEqual(cw.concealment_rank("Touch"), 1)
        self.assertEqual(cw.concealment_rank("Sight"), 2)

    def test_the_catalogues_obvious_spelling_is_sight(self) -> None:
        self.assertEqual(cw.concealment_rank("Obvious"), cw.concealment_rank("Sight"))

    def test_medical_work_needs_a_scanner_or_an_examination(self) -> None:
        self.assertFalse(cw.detectable("medical", "visual"))
        self.assertFalse(cw.detectable("medical", "touch"))
        self.assertTrue(cw.detectable("medical", "medical"))
        self.assertTrue(cw.detectable("medical", "scanner"))

    def test_touch_work_survives_a_look_but_not_a_hand(self) -> None:
        self.assertFalse(cw.detectable("touch", "visual"))
        self.assertTrue(cw.detectable("touch", "touch"))

    def test_sight_work_is_visible_and_a_patdown_finds_it(self) -> None:
        self.assertTrue(cw.detectable("sight", "visual"))
        self.assertTrue(cw.detectable("sight", "patdown"))

    def test_an_unknown_inspection_method_raises(self) -> None:
        with self.assertRaises(cw.CyberwareError):
            cw.detectable("sight", "divination")

    def test_profile_adjustment_lowers_one_step_and_stops_at_medical(self) -> None:
        self.assertEqual(cw.profile_adjusted("sight"), "touch")
        self.assertEqual(cw.profile_adjusted("touch"), "medical")
        self.assertEqual(cw.profile_adjusted("medical"), "medical")


class MaintenanceTests(unittest.TestCase):
    """SRD 3.6.4: 5% monthly, hours equal to strain, Fix-0 or Heal-0."""

    def test_upkeep_is_five_percent_of_the_base_cost(self) -> None:
        self.assertEqual(cw.monthly_upkeep(10_000), 500)
        self.assertEqual(cw.monthly_upkeep(500), 25)
        self.assertEqual(cw.monthly_upkeep(0), 0)

    def test_a_half_cent_rounds_up_not_to_even(self) -> None:
        self.assertEqual(cw.monthly_upkeep(250), 13, "$12.50 must not round down to $12")

    def test_maintenance_hours_come_from_the_core_rule(self) -> None:
        from src.rules.cwn_core import maintenance_minutes

        self.assertEqual(maintenance_minutes(2), 120)
        self.assertEqual(maintenance_minutes(0.25), 15)

    def test_fix_zero_or_heal_zero_suffices_and_untrained_does_not(self) -> None:
        self.assertTrue(cw.can_maintain(fix_level=0))
        self.assertTrue(cw.can_maintain(heal_level=0))
        self.assertFalse(cw.can_maintain(fix_level=-1, heal_level=-1))

    def test_a_month_without_upkeep_starts_the_malfunction(self) -> None:
        self.assertFalse(cw.maintenance_required(1.0))
        self.assertTrue(cw.maintenance_required(1.01))


class SkillplugTests(unittest.TestCase):
    """SRD 3.6.5: prices, jack gates and the automatic-failure range."""

    def test_the_price_table_matches_the_srd(self) -> None:
        self.assertEqual(cw.skillplug_cost(0), 1_000)
        self.assertEqual(cw.skillplug_cost(1), 10_000)
        self.assertEqual(cw.skillplug_cost(2), 50_000)

    def test_physical_skills_cost_double(self) -> None:
        self.assertEqual(cw.skillplug_cost(1, physical=True), 20_000)

    def test_level_three_plugs_are_mission_loot_not_a_purchase(self) -> None:
        with self.assertRaises(cw.CyberwareError):
            cw.skillplug_cost(3)
        self.assertIsNone(cw.SKILLPLUG_COSTS[3])

    def test_jack_two_is_required_for_physical_skills(self) -> None:
        self.assertTrue(cw.skillplug_jack_allows("skillplug_jack_1", physical=False))
        self.assertFalse(cw.skillplug_jack_allows("skillplug_jack_1", physical=True))
        self.assertTrue(cw.skillplug_jack_allows("skillplug_jack_2", physical=True))

    def test_both_jack_spellings_are_accepted(self) -> None:
        self.assertTrue(cw.skillplug_jack_allows("skillplug_jack_ii", physical=True))
        self.assertFalse(cw.skillplug_jack_allows("skillplug_jack_i", physical=True))
        self.assertTrue(cw.skillplug_jack_allows("2", physical=True))

    def test_level_two_plugs_need_the_wiring_implant(self) -> None:
        self.assertFalse(cw.SKILLPLUG_WIRING_MIN_LEVEL > 2)
        self.assertTrue(cw.SKILLPLUG_WIRING_MIN_LEVEL > 1)

    def test_a_natural_two_fails_a_skill_check_and_a_natural_one_an_attack(self) -> None:
        self.assertTrue(cw.is_auto_failure(2))
        self.assertFalse(cw.is_auto_failure(1))
        self.assertTrue(cw.is_auto_failure(1, attack=True))
        self.assertFalse(cw.is_auto_failure(2, attack=True))

    def test_each_extra_plug_run_widens_the_range_by_one(self) -> None:
        self.assertEqual(cw.auto_failure_faces(plugs_running=1), frozenset({2}))
        self.assertEqual(cw.auto_failure_faces(plugs_running=2), frozenset({2, 3}))
        self.assertEqual(cw.auto_failure_faces(attack=True, plugs_running=3), frozenset({1, 2, 3}))

    def test_an_automatic_failure_also_locks_the_jack_for_the_scene(self) -> None:
        out = cw.resolve_skillplug_roll(2)
        self.assertTrue(out["auto_failure"])
        self.assertTrue(out["no_reroll"])
        self.assertTrue(out["jack_locked_for_scene"])
        safe = cw.resolve_skillplug_roll(11)
        self.assertFalse(safe["jack_locked_for_scene"])

    def test_zero_active_plugs_or_a_bad_die_raises(self) -> None:
        with self.assertRaises(cw.CyberwareError):
            cw.auto_failure_faces(plugs_running=0)
        with self.assertRaises(cw.CyberwareError):
            cw.resolve_skillplug_roll(21)


class CyberwareModTests(unittest.TestCase):
    """SRD 3.6.6: percentage costs, skill requirements, one copy per system."""

    def test_the_ten_mods_are_all_present(self) -> None:
        self.assertEqual(len(cw.MODS), 10)

    def test_cost_is_a_percentage_of_the_host_system(self) -> None:
        self.assertEqual(cw.mod_cost(100_000, "firewalled"), 20_000)
        self.assertEqual(cw.mod_cost(100_000, "low_maintenance"), 10_000)
        self.assertEqual(cw.mod_cost(50_000, "monoblade"), 10_000)

    def test_requirements_name_both_skills(self) -> None:
        req = cw.mod_requirements("tailored_interface")
        self.assertEqual(req["fix_level"], 1)
        self.assertEqual(req["heal_level"], 3)
        self.assertEqual(req["components"], 1)

    def test_a_mod_can_only_be_installed_once_per_system(self) -> None:
        self.assertFalse(cw.can_install_mod("firewalled", installed=["firewalled"])["ok"])
        self.assertTrue(cw.can_install_mod("firewalled", installed=["monoblade"])["ok"])

    def test_mod_names_normalise_spacing_and_case(self) -> None:
        self.assertEqual(cw.mod_cost(10_000, "Low Maintenance"), cw.mod_cost(10_000, "low_maintenance"))

    def test_tailored_interface_needs_a_two_point_system(self) -> None:
        self.assertFalse(cw.can_install_mod("tailored_interface", system_strain=1.0)["ok"])
        self.assertTrue(cw.can_install_mod("tailored_interface", system_strain=2.0)["ok"])
        with self.assertRaises(cw.CyberwareError):
            cw.can_install_mod("tailored_interface")

    def test_an_unknown_mod_raises(self) -> None:
        with self.assertRaises(cw.CyberwareError):
            cw.mod_cost(1_000, "rocket_boots")


class AlienationTests(unittest.TestCase):
    """SRD 3.6.8: permanent gain, chrome syndromes, checks, CIP and therapy."""

    def test_the_option_is_declared_optional(self) -> None:
        self.assertTrue(cw.ALIENATION_IS_OPTIONAL)

    def test_permanent_gain_is_the_strain_rounded_up(self) -> None:
        self.assertEqual(cw.alienation_for_system(0.25), 1, "a discounted eye mod is still 1")
        self.assertEqual(cw.alienation_for_system(0.5), 1)
        self.assertEqual(cw.alienation_for_system(1.0), 1)
        self.assertEqual(cw.alienation_for_system(1.5), 2)
        self.assertEqual(cw.alienation_for_system(3.0), 3)
        self.assertEqual(cw.alienation_for_system(0.0), 0)

    def test_nerve_cyber_adds_two_per_system(self) -> None:
        self.assertEqual(cw.alienation_for_system(0.25, nerve=True), 3)
        self.assertEqual(cw.alienation_for_system(2.0, nerve=True), 4)

    def test_the_floor_is_the_sum_over_the_systems_still_implanted(self) -> None:
        systems = [
            {"strain": 0.25, "table": "nerve"},
            {"strain": 1.0, "table": "body"},
            {"strain_cost": 2.0, "nerve": True},
        ]
        self.assertEqual(cw.permanent_alienation(systems), 3 + 1 + 4)

    def test_removing_cyber_lowers_the_floor(self) -> None:
        carried = [{"strain": 1.0, "table": "body"}, {"strain": 2.0, "table": "skin"}]
        self.assertEqual(cw.permanent_alienation(carried), 3)
        self.assertEqual(cw.permanent_alienation(carried[:1]), 1)

    def test_the_twelve_syndromes_and_their_bonuses(self) -> None:
        self.assertEqual(len(cw.SYNDROMES), 12)
        self.assertEqual(cw.SYNDROMES["murderous"]["bonus"], 6)
        self.assertEqual(cw.SYNDROMES["distant"]["bonus"], 3)

    def test_maximum_is_wisdom_plus_syndrome_bonuses(self) -> None:
        self.assertEqual(cw.max_alienation(10), 10)
        self.assertEqual(cw.max_alienation(10, ["distant", "savage"]), 18)

    def test_the_same_syndrome_cannot_be_taken_twice(self) -> None:
        with self.assertRaises(cw.CyberwareError):
            cw.max_alienation(10, ["distant", "distant"])

    def test_an_unknown_syndrome_raises(self) -> None:
        with self.assertRaises(cw.CyberwareError):
            cw.max_alienation(10, ["fluffy"])

    def test_the_check_gains_on_equal_or_under_the_current_score(self) -> None:
        self.assertTrue(cw.gains_alienation_point(5, 5))
        self.assertTrue(cw.gains_alienation_point(4, 5))
        self.assertFalse(cw.gains_alienation_point(6, 5))

    def test_a_character_at_zero_can_never_gain_from_a_check(self) -> None:
        for die in range(1, 21):
            self.assertFalse(cw.gains_alienation_point(die, 0))

    def test_a_character_sitting_at_the_maximum_is_still_stable(self) -> None:
        # Alienation 10, Wisdom 10: a roll of 11 is above the score, so nothing is gained.
        out = cw.resolve_alienation_check(d20=11, current=10, wisdom=10)
        self.assertEqual(out["outcome"], "stable")
        self.assertEqual(out["total"], 10)
        self.assertFalse(out["gained"])

    def test_going_over_the_maximum_demands_a_mental_save_first(self) -> None:
        out = cw.resolve_alienation_check(d20=1, current=10, wisdom=10)
        self.assertEqual(out["total"], 11)
        self.assertEqual(out["outcome"], "needs_mental_save")

    def test_a_successful_save_lets_the_character_pick_a_syndrome(self) -> None:
        out = cw.resolve_alienation_check(d20=1, current=10, wisdom=10, mental_save=True)
        self.assertEqual(out["outcome"], "pick_syndrome")

    def test_a_failed_save_is_cyber_induced_psychosis(self) -> None:
        out = cw.resolve_alienation_check(d20=1, current=10, wisdom=10, mental_save=False)
        self.assertEqual(out["outcome"], "psychosis")

    def test_psychosis_is_strictly_above_the_maximum(self) -> None:
        self.assertFalse(cw.is_psychotic(10, 10))
        self.assertTrue(cw.is_psychotic(11, 10))
        self.assertFalse(cw.is_psychotic(11, 10, ["candid"]), "a syndrome raises the ceiling")

    def test_therapy_costs_two_thousand_a_week(self) -> None:
        self.assertEqual(cw.THERAPY_COST_PER_WEEK, 2_000)

    def test_therapy_drops_one_point_but_never_below_the_permanent_floor(self) -> None:
        self.assertEqual(cw.therapy_week(6, permanent_floor=4), 5)
        self.assertEqual(cw.therapy_week(4, permanent_floor=4), 4)

    def test_cip_rescue_needs_the_cyber_out_and_the_score_below_wisdom(self) -> None:
        blocked = cw.rescue_from_cip(alienation=8, wisdom=10, cyber_removed_except_medical=False,
                                     mental_save_total=12, save_target=14)
        self.assertEqual(blocked["outcome"], "ineligible")
        too_high = cw.rescue_from_cip(alienation=10, wisdom=10, cyber_removed_except_medical=True,
                                      mental_save_total=12, save_target=14)
        self.assertEqual(too_high["outcome"], "ineligible")

    def test_cip_rescue_save_carries_the_therapists_best_skill(self) -> None:
        recovered = cw.rescue_from_cip(alienation=9, wisdom=10, cyber_removed_except_medical=True,
                                       mental_save_total=10, save_target=14, therapist_bonus=4)
        self.assertEqual(recovered["outcome"], "recovered")
        lost = cw.rescue_from_cip(alienation=9, wisdom=10, cyber_removed_except_medical=True,
                                  mental_save_total=10, save_target=14, therapist_bonus=3)
        self.assertEqual(lost["outcome"], "permanently_compromised")


class CatalogueTests(unittest.TestCase):
    """SRD 3.6.7: the mechanical rows the data file carries."""

    def test_the_committed_catalogue_covers_all_seven_tables(self) -> None:
        systems = cw.load_systems()
        self.assertEqual({row.table for row in systems}, set(cw.CYBERWARE_TABLES))
        self.assertGreaterEqual(len(systems), 80)

    def test_lookup_by_printed_name_and_by_id(self) -> None:
        by_name = cw.system("Cybereyes (pair)")
        by_id = cw.system("cybereyes_pair")
        self.assertEqual(by_name, by_id)
        self.assertEqual(by_name.cost, 10_000)
        self.assertEqual(by_name.strain, 0.25)

    def test_lookup_normalises_typographic_apostrophes(self) -> None:
        payload = {
            "tables": [
                {"id": "snipers_eye", "name": "Sniper\u2019s Eye", "table": "sensory",
                 "cost": 5_000, "type": "Sensory", "concealment": "Touch", "strain": 0.25}
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalogue.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            systems = cw.load_systems(path)
        self.assertEqual(cw.system("Sniper's Eye", systems).id, "snipers_eye")
        self.assertEqual(cw.system("Sniper\u2019s Eye", systems).id, "snipers_eye")

    def test_an_unknown_system_raises(self) -> None:
        with self.assertRaises(cw.CyberwareError):
            cw.system("Rocket Boots")

    def test_nerve_systems_are_flagged_and_carry_the_surcharge(self) -> None:
        jack = cw.system("Skillplug Jack I")
        self.assertTrue(jack.is_nerve)
        self.assertEqual(jack.alienation, 3, "0.25 rounds up to 1, plus 2 for Nerve")
        eyes = cw.system("Cybereyes (pair)")
        self.assertFalse(eyes.is_nerve)
        self.assertEqual(eyes.alienation, 1)

    def test_a_pair_of_systems_totals_their_permanent_strain(self) -> None:
        total = cw.permanent_strain_total([cw.system("Cybereyes (pair)"), cw.system("Skillplug Jack I")])
        self.assertAlmostEqual(total, 0.5)

    def test_an_empty_catalogue_file_is_an_error_not_an_empty_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.json"
            path.write_text(json.dumps({"tables": []}), encoding="utf-8")
            with self.assertRaises(cw.CyberwareError):
                cw.load_systems(path)


if __name__ == "__main__":
    unittest.main()
