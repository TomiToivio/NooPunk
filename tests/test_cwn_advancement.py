"""Character advancement — every assertion traced to the CWN SRD section.

SRD: ``rules-of-the-game/character-advancement/``.
"""
import unittest

from src.rules import cwn_advancement as adv


class ExperienceTests(unittest.TestCase):
    def test_the_fast_thresholds_are_the_srd_table(self) -> None:
        expected = {1: 0, 2: 3, 3: 6, 4: 12, 5: 18, 6: 27, 7: 39, 8: 54, 9: 72, 10: 93}
        self.assertEqual(dict(adv.XP_FOR_LEVEL["fast"]), expected)

    def test_the_slow_thresholds_are_the_srd_table(self) -> None:
        expected = {1: 0, 2: 6, 3: 15, 4: 24, 5: 36, 6: 51, 7: 69, 8: 87, 9: 105, 10: 139}
        self.assertEqual(dict(adv.XP_FOR_LEVEL["slow"]), expected)

    def test_a_threshold_is_inclusive(self) -> None:
        self.assertEqual(adv.level_for_xp(2), 1)
        self.assertEqual(adv.level_for_xp(3), 2)
        self.assertEqual(adv.level_for_xp(92), 9)
        self.assertEqual(adv.level_for_xp(93), 10)

    def test_experience_does_not_reset_so_totals_are_accumulated(self) -> None:
        self.assertEqual(adv.level_for_xp(12), 4)
        self.assertEqual(adv.level_for_xp(500), 10, "capped at tenth level")

    def test_the_slow_track_needs_more(self) -> None:
        self.assertEqual(adv.level_for_xp(6, track="fast"), 3)
        self.assertEqual(adv.level_for_xp(6, track="slow"), 2)

    def test_the_three_xp_average_mission_is_recorded(self) -> None:
        self.assertEqual(adv.DEFAULT_XP_PER_MISSION, 3)

    def test_the_next_threshold_is_available_and_none_at_the_cap(self) -> None:
        self.assertEqual(adv.xp_for_next_level(1), 3)
        self.assertIsNone(adv.xp_for_next_level(10))

    def test_negative_experience_is_refused(self) -> None:
        with self.assertRaises(adv.AdvancementError):
            adv.level_for_xp(-1)


class AttackAndSaveTests(unittest.TestCase):
    def test_attack_bonus_is_half_level_rounded_down(self) -> None:
        self.assertEqual(adv.attack_bonus(1), 0)
        self.assertEqual(adv.attack_bonus(3), 1)
        self.assertEqual(adv.attack_bonus(7), 3)
        self.assertEqual(adv.attack_bonus(10), 5)

    def test_on_target_gives_the_full_level(self) -> None:
        self.assertEqual(adv.attack_bonus(7, on_target=True), 7)

    def test_saving_throws_improve_by_one_per_level(self) -> None:
        # SRD: a first-level character has 15; second level, 14.
        self.assertEqual(adv.save_target(1), 15)
        self.assertEqual(adv.save_target(2), 14)
        self.assertEqual(adv.save_target(10), 6)

    def test_levels_outside_the_range_are_refused(self) -> None:
        for bad in (0, 11):
            with self.subTest(level=bad), self.assertRaises(adv.AdvancementError):
                adv.attack_bonus(bad)


class HitPointTests(unittest.TestCase):
    def test_each_die_adds_the_constitution_modifier(self) -> None:
        self.assertEqual(adv.hit_points_rolled(3, 0, dice=[4, 4, 4]), 12)
        self.assertEqual(adv.hit_points_rolled(3, 1, dice=[4, 4, 4]), 15)
        self.assertEqual(adv.hit_points_rolled(3, -2, dice=[4, 4, 4]), 6)

    def test_no_die_is_reduced_below_one(self) -> None:
        # A 1 on the die with a -3 modifier would be -2; the SRD floors each die at 1.
        self.assertEqual(adv.hit_points_rolled(2, -3, dice=[1, 1]), 2)

    def test_hard_to_kill_adds_two_per_die(self) -> None:
        self.assertEqual(adv.hit_points_rolled(2, 0, hard_to_kill=True, dice=[3, 3]), 10)

    def test_hard_to_kill_still_floors_each_die(self) -> None:
        self.assertEqual(adv.hit_points_rolled(2, -3, hard_to_kill=True, dice=[1, 1]), 2)

    def test_the_roll_replaces_the_maximum_only_when_higher(self) -> None:
        self.assertEqual(adv.new_maximum_hit_points(20, 25), 25)
        self.assertEqual(adv.new_maximum_hit_points(20, 20), 21)
        self.assertEqual(adv.new_maximum_hit_points(20, 9), 21)

    def test_a_wrong_number_of_dice_is_refused(self) -> None:
        with self.assertRaises(adv.AdvancementError):
            adv.hit_points_rolled(3, 0, dice=[4, 4])


class SkillPointTests(unittest.TestCase):
    def test_three_points_per_level_four_with_educated(self) -> None:
        self.assertEqual(adv.skill_points_for_level(), 3)
        self.assertEqual(adv.skill_points_for_level(educated=True), 4)

    def test_ranks_are_bought_in_order(self) -> None:
        # SRD: level 1 needs 1 point for rank 0, then 2 for rank 1.
        self.assertEqual(adv.skill_point_cost(0), 1)
        self.assertEqual(adv.skill_point_cost(1), 2)
        self.assertEqual(adv.total_skill_cost(1), 3)
        self.assertEqual(adv.total_skill_cost(4), 15, "1+2+3+4+5")

    def test_rank_gates_follow_the_table(self) -> None:
        self.assertTrue(adv.skill_rank_allowed(1, 1))
        self.assertFalse(adv.skill_rank_allowed(2, 2))
        self.assertTrue(adv.skill_rank_allowed(2, 3))
        self.assertFalse(adv.skill_rank_allowed(3, 5))
        self.assertTrue(adv.skill_rank_allowed(3, 6))
        self.assertFalse(adv.skill_rank_allowed(4, 8))
        self.assertTrue(adv.skill_rank_allowed(4, 9))

    def test_rank_five_does_not_exist(self) -> None:
        with self.assertRaises(adv.AdvancementError):
            adv.skill_point_cost(5)


class AttributeAndFocusTests(unittest.TestCase):
    def test_each_boost_costs_its_number(self) -> None:
        self.assertEqual([adv.attribute_boost_cost(n) for n in range(1, 6)], [1, 2, 3, 4, 5])

    def test_boost_level_gates(self) -> None:
        self.assertTrue(adv.attribute_boost_allowed(1, 1))
        self.assertTrue(adv.attribute_boost_allowed(2, 1))
        self.assertFalse(adv.attribute_boost_allowed(3, 2))
        self.assertTrue(adv.attribute_boost_allowed(3, 3))
        self.assertFalse(adv.attribute_boost_allowed(4, 5))
        self.assertTrue(adv.attribute_boost_allowed(4, 6))
        self.assertFalse(adv.attribute_boost_allowed(5, 8))
        self.assertTrue(adv.attribute_boost_allowed(5, 9))

    def test_six_boosts_do_not_exist(self) -> None:
        with self.assertRaises(adv.AdvancementError):
            adv.attribute_boost_cost(6)

    def test_focus_picks_arrive_at_two_five_seven_ten(self) -> None:
        self.assertEqual(adv.focus_picks_at(1), 0)
        self.assertEqual(adv.focus_picks_at(2), 1)
        self.assertEqual(adv.focus_picks_at(4), 1)
        self.assertEqual(adv.focus_picks_at(5), 2)
        self.assertEqual(adv.focus_picks_at(7), 3)
        self.assertEqual(adv.focus_picks_at(10), 4)

    def test_the_third_edge_arrives_at_five(self) -> None:
        self.assertFalse(adv.has_third_edge(4))
        self.assertTrue(adv.has_third_edge(5))


if __name__ == "__main__":
    unittest.main()
