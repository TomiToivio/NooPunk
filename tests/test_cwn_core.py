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


class MajorInjuryTests(unittest.TestCase):
    """SRD 2.5.6: lethal zero HP + a Traumatic Hit in the same scene -> Physical save -> d12."""

    def test_all_three_conditions_are_required(self) -> None:
        self.assertTrue(cwn.major_injury_risk(lethal=True, hit_points=0, traumatic_this_scene=True))
        self.assertFalse(cwn.major_injury_risk(lethal=False, hit_points=0, traumatic_this_scene=True),
                         "a non-lethal beating does not put you on this table")
        self.assertFalse(cwn.major_injury_risk(lethal=True, hit_points=3, traumatic_this_scene=True),
                         "you must actually be at zero")
        self.assertFalse(cwn.major_injury_risk(lethal=True, hit_points=0, traumatic_this_scene=False),
                         "no Traumatic Hit in this scene means no risk")

    def test_the_table_is_the_srd_table(self) -> None:
        self.assertEqual(cwn.injury_for_roll(1).id, "instant_death")
        self.assertTrue(cwn.injury_for_roll(1).fatal)
        self.assertEqual(cwn.injury_for_roll(3).id, "brain_damage")
        self.assertTrue(cwn.injury_for_roll(3).coma)
        self.assertEqual(cwn.injury_for_roll(4).id, "eye_damage")
        self.assertEqual(cwn.injury_for_roll(5).id, "gut_wound")
        for roll, limb in ((6, "right leg"), (7, "left leg"), (8, "right arm"), (9, "left arm")):
            with self.subTest(roll=roll):
                self.assertEqual(cwn.injury_for_roll(roll).limb, limb)
        self.assertEqual(cwn.injury_for_roll(10).id, "system_damage")
        self.assertEqual(cwn.injury_for_roll(11).id, "flesh_wound")
        self.assertEqual(cwn.injury_for_roll(12).id, "flesh_wound")

    def test_rolls_outside_the_table_clamp_rather_than_fail(self) -> None:
        # "a roll less than 1 still counts as 1, and one more than 12 still counts as 12"
        self.assertEqual(cwn.clamp_injury_roll(-3), 1)
        self.assertEqual(cwn.clamp_injury_roll(0), 1)
        self.assertEqual(cwn.clamp_injury_roll(13), 12)
        self.assertEqual(cwn.injury_for_roll(99).id, "flesh_wound")

    def test_passing_the_physical_save_leaves_you_mortally_wounded_but_uninjured(self) -> None:
        out = cwn.resolve_downed(lethal=True, hit_points=0, traumatic_this_scene=True,
                                 level=1, attributes=SHEET, save_die=20)
        self.assertTrue(out["at_risk"])
        self.assertTrue(out["mortally_wounded"])
        self.assertTrue(out["saved"])
        self.assertIsNone(out["injury"])

    def test_failing_the_save_rolls_a_major_injury(self) -> None:
        out = cwn.resolve_downed(lethal=True, hit_points=0, traumatic_this_scene=True,
                                 level=1, attributes=SHEET, save_die=1, injury_roll=3)
        self.assertFalse(out["saved"])
        self.assertEqual(out["injury"].id, "brain_damage")
        self.assertEqual(out["injury_roll"], 3)

    def test_no_risk_returns_a_plain_zero_hit_point_result(self) -> None:
        out = cwn.resolve_downed(lethal=True, hit_points=0, traumatic_this_scene=False,
                                 level=1, attributes=SHEET)
        self.assertFalse(out["at_risk"])
        self.assertIsNone(out["saved"])
        self.assertIsNone(out["injury"])

    def test_the_save_is_physical_not_luck(self) -> None:
        # A Physical save at level 1 uses best(STR, CON); the target must match save_target("Physical").
        expected = cwn.save_target("Physical", level=1, attributes=SHEET)
        out = cwn.resolve_downed(lethal=True, hit_points=0, traumatic_this_scene=True,
                                 level=1, attributes=SHEET, save_die=expected)
        self.assertTrue(out["saved"])
        out_below = cwn.resolve_downed(lethal=True, hit_points=0, traumatic_this_scene=True,
                                       level=1, attributes=SHEET, save_die=expected - 1, injury_roll=12)
        self.assertFalse(out_below["saved"])

    def test_a_seeded_resolution_replays(self) -> None:
        import random as _r
        a = cwn.resolve_downed(lethal=True, hit_points=0, traumatic_this_scene=True, level=1,
                               attributes=SHEET, rng=_r.Random(5))
        b = cwn.resolve_downed(lethal=True, hit_points=0, traumatic_this_scene=True, level=1,
                               attributes=SHEET, rng=_r.Random(5))
        self.assertEqual(a["saved"], b["saved"])
        self.assertEqual(a["injury_roll"], b["injury_roll"])


SHEET_CON = {"Strength": 10, "Dexterity": 10, "Constitution": 14,
             "Intelligence": 10, "Wisdom": 10, "Charisma": 10}


class SystemStrainTests(unittest.TestCase):
    """SRD 3.6.x: capacity is the Constitution score; cyberware adds permanent strain."""

    def test_capacity_is_the_constitution_score(self) -> None:
        self.assertEqual(cwn.strain_maximum(14), 14)
        self.assertEqual(cwn.strain_maximum(3), 3)

    def test_lifestyle_modifies_the_maximum_but_never_below_zero(self) -> None:
        self.assertEqual(cwn.strain_maximum(14, lifestyle="slum"), 13)
        self.assertEqual(cwn.strain_maximum(14, lifestyle="squatter"), 12)
        self.assertEqual(cwn.strain_maximum(14, lifestyle="fine"), 15)
        self.assertEqual(cwn.strain_maximum(14, lifestyle="luxury"), 16)
        self.assertEqual(cwn.strain_maximum(3, lifestyle="squatter"), 1,
                         "a Con 3 squatter has a maximum of 1, not a negative number")

    def test_unknown_lifestyle_is_an_error_not_a_silent_zero(self) -> None:
        with self.assertRaises(cwn.CwnError):
            cwn.strain_maximum(10, lifestyle="palace")

    def test_installation_bands_match_the_srd_table(self) -> None:
        self.assertEqual(cwn.installation_terms(0)["difficulty"], 7)
        self.assertEqual(cwn.installation_terms(0)["cost"], 100)
        self.assertEqual(cwn.installation_terms(0.5)["difficulty"], 8)
        self.assertEqual(cwn.installation_terms(0.6)["difficulty"], 10)
        self.assertEqual(cwn.installation_terms(1)["difficulty"], 10)
        self.assertEqual(cwn.installation_terms(1.1)["difficulty"], 11)
        self.assertEqual(cwn.installation_terms(3)["difficulty"], 11)
        self.assertEqual(cwn.installation_terms(3.1)["difficulty"], 12)
        self.assertEqual(cwn.installation_terms(9)["difficulty"], 12,
                         "the last band is open-ended")

    def test_an_implant_that_would_exceed_the_maximum_is_refused_before_any_roll(self) -> None:
        out = cwn.resolve_implant_surgery(strain=3, current_strain=12, maximum=14, check_total=99)
        self.assertEqual(out["outcome"], "refused")
        self.assertEqual(out["strain_after"], 12)

    def test_failing_by_two_or_less_just_fails_the_surgery(self) -> None:
        out = cwn.resolve_implant_surgery(strain=1.5, current_strain=0, maximum=14, check_total=9)
        self.assertEqual(out["outcome"], "failed")
        self.assertEqual(out["strain_after"], 0)

    def test_failing_by_more_than_two_maximizes_strain_and_drops_to_one_hp(self) -> None:
        out = cwn.resolve_implant_surgery(strain=1.5, current_strain=2, maximum=14, check_total=8)
        self.assertEqual(out["outcome"], "catastrophic")
        self.assertEqual(out["strain_after"], 14)
        self.assertEqual(out["hit_points"], 1)

    def test_success_adds_permanent_strain_fractionally(self) -> None:
        out = cwn.resolve_implant_surgery(strain=0.5, current_strain=2.5, maximum=14, check_total=12)
        self.assertEqual(out["outcome"], "installed")
        self.assertEqual(out["strain_after"], 3.0)

    def test_maintenance_is_hours_equal_to_strain_with_a_fifteen_minute_floor(self) -> None:
        self.assertEqual(cwn.maintenance_minutes(2), 120)
        self.assertEqual(cwn.maintenance_minutes(0.25), 15)
        self.assertEqual(cwn.maintenance_minutes(0), 15)

    def test_overdue_maintenance_starts_after_a_month(self) -> None:
        self.assertFalse(cwn.maintenance_overdue(1.0))
        self.assertTrue(cwn.maintenance_overdue(1.1))

    def test_first_aid_heals_and_costs_one_strain(self) -> None:
        self.assertEqual(cwn.first_aid(heal_skill=2, die=4)["healed"], 6)
        self.assertEqual(cwn.first_aid(heal_skill=2, die=4)["strain_cost"], 1)
        self.assertEqual(cwn.first_aid(heal_skill=0, die=4)["healed"], 3,
                         "no Heal skill at all: 1d6-1")
        self.assertEqual(cwn.first_aid(heal_skill=0, die=1)["healed"], 0,
                         "1d6-1 cannot heal less than zero")
        with self.assertRaises(cwn.CwnError):
            cwn.first_aid(die=7)


if __name__ == "__main__":
    unittest.main()
