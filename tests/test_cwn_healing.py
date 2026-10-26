"""Tests for mortal wounds, stabilization, Frail, first aid and System Strain."""
import unittest

from src.rules.cwn_healing import (
    HealingRulesError,
    Patient,
    SystemStrain,
    first_aid,
    frail_week,
    natural_healing,
    remove_frailty,
    stabilize_difficulty,
    stabilized,
)


class StrainAgreementTest(unittest.TestCase):
    """cwn_healing must delegate Strain to cwn_strain, never restate it."""

    def test_totals_agree_with_the_canonical_strain_module(self):
        from src.rules import cwn_strain
        mine = SystemStrain(constitution=10, current=4)
        theirs = cwn_strain.SystemStrain(constitution=10, temporary=4)
        self.assertEqual(mine.current, theirs.total)

    def test_refusal_at_the_ceiling_agrees_with_the_canonical_module(self):
        from src.rules import cwn_strain
        mine = SystemStrain(constitution=3, current=3)
        theirs = cwn_strain.SystemStrain(constitution=3, temporary=3)
        self.assertFalse(mine.add(1))
        self.assertFalse(theirs.absorb(1))
        self.assertEqual(mine.current, theirs.total)

    def test_sleep_recovers_the_same_amount_as_the_canonical_module(self):
        from src.rules import cwn_strain
        mine = SystemStrain(constitution=10, current=5)
        theirs = cwn_strain.SystemStrain(constitution=10, temporary=5)
        self.assertEqual(mine.nights_sleep(2), theirs.rest_night() + theirs.rest_night())
        self.assertEqual(mine.current, theirs.total)


class MortalWoundTest(unittest.TestCase):
    def test_a_downed_patient_dies_at_the_end_of_the_sixth_round(self):
        p = Patient(hit_points=0, level_or_hit_dice=3, downed_round=10)
        self.assertEqual(p.rounds_until_death(10), 6)
        self.assertEqual(p.rounds_until_death(14), 2)
        self.assertEqual(p.rounds_until_death(16), 0)

    def test_stabilization_difficulty_rises_each_round(self):
        self.assertEqual(stabilize_difficulty(0), 8)
        self.assertEqual(stabilize_difficulty(3), 11)

    def test_no_medkit_makes_stabilization_two_harder(self):
        self.assertEqual(stabilize_difficulty(2, has_medkit=False), 12)

    def test_stabilizing_wakes_the_patient_at_one_hit_point_and_frail(self):
        p = Patient(hit_points=0, level_or_hit_dice=3, downed_round=5)
        stabilized(p)
        self.assertEqual(p.hit_points, 1)
        self.assertTrue(p.frail)

    def test_only_a_downed_patient_needs_stabilizing(self):
        with self.assertRaises(HealingRulesError):
            stabilized(Patient(hit_points=4, level_or_hit_dice=2))

    def test_a_patient_never_downed_has_no_clock(self):
        with self.assertRaises(HealingRulesError):
            Patient(hit_points=3, level_or_hit_dice=2).rounds_until_death(4)


class FrailTest(unittest.TestCase):
    def test_the_frail_do_not_heal_naturally(self):
        self.assertEqual(natural_healing(Patient(hit_points=2, level_or_hit_dice=4, frail=True)), 0)

    def test_a_healthy_character_recovers_level_in_hit_points_per_night(self):
        self.assertEqual(natural_healing(Patient(hit_points=2, level_or_hit_dice=4)), 4)

    def test_medkit_and_heal_zero_end_frailty_after_the_week(self):
        self.assertEqual(frail_week(has_medic_care=True), "recovered")

    def test_without_care_a_failed_save_kills_and_a_passed_one_costs_a_month(self):
        self.assertEqual(frail_week(has_medic_care=False, physical_save_success=False), "dying")
        self.assertEqual(frail_week(has_medic_care=False, physical_save_success=True), "month_more")

    def test_without_care_the_week_requires_its_save(self):
        with self.assertRaises(HealingRulesError):
            frail_week(has_medic_care=False)

    def test_frailty_gets_one_removal_attempt(self):
        self.assertTrue(remove_frailty(skill_total=10)["succeeded"])
        self.assertFalse(remove_frailty(skill_total=9)["succeeded"])
        self.assertFalse(remove_frailty(skill_total=15, already_attempted=True)["allowed"])


class FirstAidTest(unittest.TestCase):
    def test_first_aid_is_a_die_plus_heal_skill(self):
        self.assertEqual(first_aid(die_roll=4, heal_skill=2)["healed"], 6)

    def test_without_any_heal_skill_first_aid_is_a_die_minus_one(self):
        self.assertEqual(first_aid(die_roll=4, heal_skill=0)["healed"], 3)

    def test_the_worst_first_aid_heals_nothing_rather_than_going_negative(self):
        self.assertEqual(first_aid(die_roll=1, heal_skill=0)["healed"], 0)

    def test_first_aid_needs_a_medkit(self):
        with self.assertRaises(HealingRulesError):
            first_aid(die_roll=3, has_medkit=False)

    def test_each_application_costs_one_system_strain(self):
        s = SystemStrain(constitution=10)
        first_aid(die_roll=4, heal_skill=1, strain=s)
        self.assertEqual(s.current, 1)

    def test_a_body_at_its_maximum_gains_nothing_from_first_aid(self):
        s = SystemStrain(constitution=2, current=2)
        out = first_aid(die_roll=4, heal_skill=1, strain=s)
        self.assertTrue(out["refused"])
        self.assertEqual(out["healed"], 0)
        self.assertEqual(s.current, 2)


class SystemStrainTest(unittest.TestCase):
    def test_maximum_strain_is_constitution(self):
        self.assertEqual(SystemStrain(constitution=13).maximum, 13)

    def test_a_nights_sleep_sheds_one_point(self):
        s = SystemStrain(constitution=10, current=4)
        self.assertEqual(s.nights_sleep(2), 2)
        self.assertEqual(s.current, 2)

    def test_implant_strain_is_never_shed_by_sleeping(self):
        s = SystemStrain(constitution=10)
        s.add_permanent(3)
        self.assertEqual(s.shedable, 0)
        self.assertEqual(s.nights_sleep(30), 0)
        self.assertEqual(s.current, 3)

    def test_ordinary_strain_still_sheds_around_the_implant_strain(self):
        s = SystemStrain(constitution=10)
        s.add_permanent(2)          # 2 permanent
        s.add(3)                    # 3 ordinary, from first aid or hardship
        self.assertEqual(s.shedable, 3)
        self.assertEqual(s.nights_sleep(10), 3)
        self.assertEqual(s.current, 2)

    def test_implant_strain_comes_off_the_ceiling_immediately(self):
        s = SystemStrain(constitution=10)
        s.add_permanent(4)
        self.assertEqual((s.current, s.permanent), (4, 4))

    def test_an_implant_beyond_the_maximum_cannot_be_installed(self):
        with self.assertRaises(HealingRulesError):
            SystemStrain(constitution=5).add_permanent(6)

    def test_adding_beyond_the_maximum_is_refused_rather_than_clamped(self):
        s = SystemStrain(constitution=3, current=3)
        self.assertFalse(s.add(1))
        self.assertEqual(s.current, 3)


if __name__ == "__main__":
    unittest.main()
