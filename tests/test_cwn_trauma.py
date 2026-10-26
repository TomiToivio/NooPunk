"""Tests for the CWN damage, trauma and shock layer."""
import unittest

from src.rules.cwn_trauma import (
    Shock,
    TraumaRulesError,
    Weapon,
    absorb_with_soak,
    is_traumatic,
    resolve_hit,
    shock_on_miss,
)


class TraumaTest(unittest.TestCase):
    def test_equalling_the_trauma_target_is_traumatic(self):
        self.assertTrue(is_traumatic(6, 6))
        self.assertFalse(is_traumatic(5, 6))

    def test_armour_raising_the_target_turns_a_six_into_a_plain_hit(self):
        self.assertFalse(is_traumatic(6, 7))
        self.assertTrue(is_traumatic(7, 7))

    def test_trauma_rating_multiplies_the_whole_hit(self):
        w = Weapon("1d8", trauma_rating=3)
        plain = resolve_hit(w, damage_roll=9, trauma_die_roll=5)
        bad = resolve_hit(w, damage_roll=9, trauma_die_roll=6)
        self.assertEqual(plain.total_damage, 9)
        self.assertEqual(bad.total_damage, 27)

    def test_non_lethal_attack_skips_the_trauma_die_entirely(self):
        w = Weapon("1d6", trauma_rating=3)
        r = resolve_hit(w, damage_roll=4, lethal=False)
        self.assertFalse(r.traumatic)
        self.assertEqual(r.total_damage, 4)

    def test_lethal_hit_requires_its_trauma_die(self):
        with self.assertRaises(TraumaRulesError):
            resolve_hit(Weapon("1d6"), damage_roll=4)


class ShockTest(unittest.TestCase):
    def test_shock_reaches_targets_at_or_below_its_armour_class(self):
        s = Shock(2, max_ac=15)
        self.assertTrue(s.applies_to(13))
        self.assertTrue(s.applies_to(15))
        self.assertFalse(s.applies_to(16))

    def test_shock_without_an_armour_ceiling_always_applies(self):
        s = Shock(5, max_ac=None)
        self.assertTrue(s.applies_to(30))

    def test_immunity_negates_shock(self):
        self.assertEqual(shock_on_miss(Shock(5), 10, immune=True), 0)

    def test_a_barrier_eats_the_first_shock_of_the_round(self):
        self.assertEqual(shock_on_miss(Shock(5), 10, barrier_spent=True), 0)

    def test_only_the_attribute_modifier_adds_to_shock(self):
        self.assertEqual(shock_on_miss(Shock(2, 15), 12, attribute_modifier=1), 3)

    def test_a_hit_is_never_weaker_than_the_shock_it_avoided(self):
        w = Weapon("1d4", shock=Shock(4, max_ac=20))
        r = resolve_hit(w, damage_roll=1, trauma_die_roll=1, target_melee_ac=10)
        self.assertTrue(r.shock_floor_applied)
        self.assertEqual(r.total_damage, 4)


class SoakTest(unittest.TestCase):
    def test_soak_is_spent_down_rather_than_static(self):
        through, left = absorb_with_soak(7, 3)
        self.assertEqual((through, left), (4, 0))

    def test_soak_can_absorb_a_whole_hit(self):
        through, left = absorb_with_soak(2, 5)
        self.assertEqual((through, left), (0, 3))

    def test_spent_soak_protects_nothing_later_in_the_fight(self):
        r = resolve_hit(Weapon("1d6"), damage_roll=5, trauma_die_roll=1, soak=0)
        self.assertEqual(r.soak_absorbed, 0)
        self.assertEqual(r.damage_to_hit_points, 5)


class MajorInjuryTest(unittest.TestCase):
    def test_zero_hit_points_from_a_traumatic_hit_risks_a_major_injury(self):
        w = Weapon("1d6", trauma_rating=2)
        r = resolve_hit(w, damage_roll=6, trauma_die_roll=6, current_hit_points=10)
        self.assertTrue(r.major_injury_risk)

    def test_zero_hit_points_without_trauma_is_not_a_major_injury(self):
        r = resolve_hit(Weapon("1d6"), damage_roll=6, trauma_die_roll=1, current_hit_points=5)
        self.assertFalse(r.major_injury_risk)

    def test_earlier_trauma_in_the_same_fight_keeps_the_risk_open(self):
        r = resolve_hit(Weapon("1d6"), damage_roll=20, trauma_die_roll=1,
                        traumatic_damage_earlier_in_fight=True, current_hit_points=8)
        self.assertTrue(r.major_injury_risk)


class UnarmedTest(unittest.TestCase):
    def test_punch_skill_adds_to_a_purely_unarmed_attack(self):
        r = resolve_hit(Weapon("1d4", unarmed=True), damage_roll=3,
                        skill_bonus=2, trauma_die_roll=1)
        self.assertEqual(r.base_damage, 5)

    def test_punch_skill_does_not_add_to_an_artificial_weapon(self):
        r = resolve_hit(Weapon("1d4", unarmed=False), damage_roll=3,
                        skill_bonus=2, trauma_die_roll=1)
        self.assertEqual(r.base_damage, 3)


if __name__ == "__main__":
    unittest.main()
