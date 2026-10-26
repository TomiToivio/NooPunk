"""CWN saves, Shock and Trauma — every assertion traced to an SRD section.

Values are checked against the SRD rather than against the module's own behaviour, because a
module that agrees with itself proves nothing.
"""
import random
import unittest

from src.rules import cwn_core as cwn
from src.rules import wn_core as wn

SHEET = {"Strength": 14, "Dexterity": 12, "Constitution": 8,
         "Intelligence": 10, "Wisdom": 16, "Charisma": 9}


class SaveTargetTests(unittest.TestCase):
    """SRD 2.2.0: 16 - level - best relevant modifier."""

    def test_the_formula_at_level_one_matches_character_creation(self) -> None:
        # 1.7.3 says a new character's Physical target is "15 minus the better modifier".
        target = cwn.save_target("Physical", level=1, attributes=SHEET)
        expected = 16 - 1 - wn.attribute_modifier(14)   # best(STR 14 -> +1, CON 8 -> 0)
        self.assertEqual(target, expected)
        self.assertEqual(target, 14)                    # 15 - 1

    def test_evasion_uses_dexterity_or_intelligence(self) -> None:
        self.assertEqual(cwn.save_target("Evasion", level=1, attributes=SHEET),
                         16 - 1 - max(wn.attribute_modifier(12), wn.attribute_modifier(10)))

    def test_mental_uses_wisdom_or_charisma(self) -> None:
        self.assertEqual(cwn.save_target("Mental", level=1, attributes=SHEET),
                         16 - 1 - wn.attribute_modifier(16))

    def test_luck_ignores_attributes_and_is_fifteen_at_level_one(self) -> None:
        # SRD 1.7.3: "A new character's Luck save target is always 15."
        self.assertEqual(cwn.save_target("Luck", level=1, attributes=SHEET), 15)
        self.assertEqual(cwn.save_target("Luck", level=1, attributes={"Strength": 18}), 15)

    def test_each_level_lowers_every_target_by_one(self) -> None:
        for kind in cwn.SAVE_KINDS:
            with self.subTest(kind=kind):
                self.assertEqual(cwn.save_target(kind, level=4, attributes=SHEET),
                                 cwn.save_target(kind, level=1, attributes=SHEET) - 3)

    def test_an_unknown_save_and_a_bad_level_are_refused(self) -> None:
        with self.assertRaises(cwn.CwnError):
            cwn.save_target("Sanity", level=1, attributes=SHEET)
        with self.assertRaises(cwn.CwnError):
            cwn.save_target("Luck", level=0, attributes=SHEET)


class SavingThrowTests(unittest.TestCase):
    """SRD 2.2.0: 1d20 >= target; natural 1 fails, natural 20 succeeds."""

    def test_meeting_the_target_succeeds(self) -> None:
        target = cwn.save_target("Luck", level=1, attributes=SHEET)
        self.assertTrue(cwn.saving_throw("Luck", level=1, attributes=SHEET, die=target).success)

    def test_one_below_the_target_fails(self) -> None:
        target = cwn.save_target("Luck", level=1, attributes=SHEET)
        self.assertFalse(cwn.saving_throw("Luck", level=1, attributes=SHEET, die=target - 1).success)

    def test_a_natural_one_always_fails_even_with_bonuses(self) -> None:
        save = cwn.saving_throw("Luck", level=20, attributes=SHEET, die=1, bonus=50)
        self.assertFalse(save.success)
        self.assertTrue(save.natural)

    def test_a_natural_twenty_always_succeeds_even_against_a_hopeless_target(self) -> None:
        save = cwn.saving_throw("Physical", level=30, attributes=SHEET, die=20)
        self.assertTrue(save.success)
        self.assertTrue(save.natural)

    def test_bonuses_apply_to_the_total_not_the_natural_result(self) -> None:
        save = cwn.saving_throw("Luck", level=1, attributes=SHEET, die=10, bonus=3)
        self.assertEqual(save.total, 13)
        self.assertFalse(save.success)   # 13 < 15

    def test_a_die_outside_1_to_20_is_refused(self) -> None:
        for bad in (0, 21):
            with self.subTest(die=bad), self.assertRaises(cwn.CwnError):
                cwn.saving_throw("Luck", level=1, attributes=SHEET, die=bad)


class SeededReplayTests(unittest.TestCase):
    def test_the_same_seed_replays_exactly(self) -> None:
        a = cwn.saving_throw("Luck", level=1, attributes=SHEET, rng=random.Random(7)).die
        b = cwn.saving_throw("Luck", level=1, attributes=SHEET, rng=random.Random(7)).die
        self.assertEqual(a, b)


class TraumaTests(unittest.TestCase):
    """SRD 2.4.6.3: Trauma Die >= Trauma Target multiplies TOTAL damage by the rating."""

    def test_the_default_target_is_six(self) -> None:
        self.assertEqual(cwn.DEFAULT_TRAUMA_TARGET, 6)
        self.assertTrue(cwn.is_traumatic_hit(6))
        self.assertFalse(cwn.is_traumatic_hit(5))

    def test_a_raised_target_resists(self) -> None:
        self.assertFalse(cwn.is_traumatic_hit(6, trauma_target=8))
        self.assertTrue(cwn.is_traumatic_hit(8, trauma_target=8))

    def test_total_damage_is_multiplied_not_the_weapon_die(self) -> None:
        # SRD example: a x3 shotgun doing 9 damage instead does 27.
        self.assertEqual(cwn.trauma_damage(9, 3, traumatic=True), 27)

    def test_a_non_traumatic_hit_is_unchanged(self) -> None:
        self.assertEqual(cwn.trauma_damage(9, 3, traumatic=False), 9)


class ShockTests(unittest.TestCase):
    """SRD 2.4.6.4: Shock lands on a miss if Melee AC <= the rating; "-" ignores AC."""

    def test_shock_never_lands_on_a_hit(self) -> None:
        self.assertFalse(cwn.shock_applies(hit=True, shock_ac=15, target_melee_ac=10))

    def test_shock_lands_on_a_miss_when_the_ac_is_within_rating(self) -> None:
        self.assertEqual(
            cwn.shock_damage(hit=False, shock_value=2, shock_ac=15, target_melee_ac=13), 2)
        self.assertTrue(cwn.shock_applies(hit=False, shock_ac=15, target_melee_ac=15))

    def test_shock_does_not_land_when_the_ac_is_above_the_rating(self) -> None:
        self.assertEqual(
            cwn.shock_damage(hit=False, shock_value=2, shock_ac=15, target_melee_ac=16), 0)

    def test_the_dash_rating_ignores_armour_class(self) -> None:
        # "Shock 5/-" applies regardless of AC.
        self.assertEqual(
            cwn.shock_damage(hit=False, shock_value=5, shock_ac=None, target_melee_ac=25), 5)

    def test_only_explicit_bonuses_add_to_shock(self) -> None:
        self.assertEqual(
            cwn.shock_damage(hit=False, shock_value=2, shock_ac=None, target_melee_ac=10,
                             attribute_modifier=1, explicit_bonus=2), 5)

    def test_a_hit_never_deals_less_than_its_shock_floor(self) -> None:
        self.assertEqual(cwn.damage_floor(1, 4), 4)
        self.assertEqual(cwn.damage_floor(7, 4), 7)

    def test_shock_cannot_cause_trauma(self) -> None:
        self.assertFalse(cwn.shock_can_cause_trauma())


class AttackResolutionTests(unittest.TestCase):
    """The three invariants together, in the order the SRD applies them."""

    def test_a_miss_with_shock_returns_shock_and_no_trauma(self) -> None:
        out = cwn.resolve_attack(hit=False, shock_value=2, shock_ac=15, target_melee_ac=13,
                                 trauma_die=6, trauma_rating=3)
        self.assertEqual(out["damage"], 2)
        self.assertFalse(out["trauma"], "shock can never be a Traumatic Hit")

    def test_a_traumatic_hit_multiplies_then_applies_the_shock_floor(self) -> None:
        out = cwn.resolve_attack(hit=True, total_damage=9, trauma_die=6, trauma_rating=3,
                                 shock_value=2, shock_ac=15, target_melee_ac=13)
        self.assertEqual(out["damage"], 27)
        self.assertTrue(out["trauma"])

    def test_the_shock_floor_rescues_a_weak_hit(self) -> None:
        out = cwn.resolve_attack(hit=True, total_damage=1, trauma_die=1, trauma_rating=1,
                                 shock_value=4, shock_ac=None, target_melee_ac=13)
        self.assertEqual(out["damage"], 4)

    def test_non_lethal_attacks_pass_no_trauma_die(self) -> None:
        out = cwn.resolve_attack(hit=True, total_damage=5, trauma_die=None, trauma_rating=3)
        self.assertFalse(out["trauma"])
        self.assertEqual(out["damage"], 5)


if __name__ == "__main__":
    unittest.main()
