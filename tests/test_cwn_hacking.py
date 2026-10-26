"""Behavioural tests for CWN hacking (``src/rules/cwn_hacking.py``).

Each test pins the rule it comes from. Two of them exist because the flattening would be invisible at a
table: Access is a *pool* that a deck tops up, and the wireless/VR-crown penalties are flat, so a
wireless hack through a crown is at −3 and not at the −2 a situational clamp would leave.
"""
import random
import unittest

from src.rules.cwn_hacking import (
    ALERT_ACTIONS_TO_ALERT,
    SECURITY_LEVELS,
    UNOPERATED_DRONE_DIFFICULTY,
    VR_CROWN_PENALTY,
    WIRELESS_PENALTY,
    AlertClock,
    HackError,
    access_pool,
    cyberware_difficulty,
    hacking_check,
    security_difficulty,
)


class AccessPoolTests(unittest.TestCase):
    def test_access_is_intelligence_plus_program_plus_the_deck(self):
        self.assertEqual(access_pool(intelligence_modifier=1, program_skill=2, deck_bonus=1), 4)
        self.assertEqual(access_pool(intelligence_modifier=2, program_skill=0), 2)

    def test_access_never_goes_negative(self):
        self.assertEqual(access_pool(intelligence_modifier=-2, program_skill=0), 0)

    def test_a_negative_program_skill_is_a_data_error(self):
        with self.assertRaises(HackError):
            access_pool(intelligence_modifier=1, program_skill=-1)


class SecurityTests(unittest.TestCase):
    def test_the_ladder_is_the_recorded_one(self):
        self.assertEqual(sorted(SECURITY_LEVELS), [7, 8, 9, 10, 12])
        self.assertEqual(security_difficulty(7), 7)
        self.assertEqual(security_difficulty(12), 12)

    def test_situation_modifiers(self):
        self.assertEqual(security_difficulty(8, alerted=True), 9)
        self.assertEqual(security_difficulty(8, important_device=True), 9)
        self.assertEqual(security_difficulty(8, alerted=True, important_device=True), 10)
        self.assertEqual(security_difficulty(9, tech_quality=-2), 7)
        self.assertEqual(security_difficulty(9, inside_info=3), 6)

    def test_an_unrecorded_level_is_refused(self):
        with self.assertRaises(HackError):
            security_difficulty(11)

    def test_cyberware_difficulty_is_seven_plus_a_third_of_level(self):
        self.assertEqual(cyberware_difficulty(level_or_hit_dice=1), 8)
        self.assertEqual(cyberware_difficulty(level_or_hit_dice=3), 8)
        self.assertEqual(cyberware_difficulty(level_or_hit_dice=4), 9)
        self.assertEqual(cyberware_difficulty(level_or_hit_dice=9), 10)
        self.assertEqual(cyberware_difficulty(level_or_hit_dice=4, has_operator=False),
                         UNOPERATED_DRONE_DIFFICULTY)

    def test_cyberware_needs_a_positive_level(self):
        with self.assertRaises(HackError):
            cyberware_difficulty(level_or_hit_dice=0)


class HackCheckTests(unittest.TestCase):
    def test_total_is_dice_plus_modifier_plus_program(self):
        check = hacking_check(intelligence_score=14, program_skill=1, difficulty=9, dice=(3, 4))
        self.assertEqual(check.total, 7 + 1 + 1)
        self.assertTrue(check.success)          # 9 against 9 meets the difficulty
        harder = hacking_check(intelligence_score=14, program_skill=1, difficulty=10, dice=(3, 4))
        self.assertFalse(harder.success)

    def test_wireless_costs_two_and_a_crown_costs_one_more(self):
        wired = hacking_check(intelligence_score=14, program_skill=1, difficulty=9, dice=(3, 4))
        wireless = hacking_check(intelligence_score=14, program_skill=1, difficulty=9,
                                 wireless=True, dice=(3, 4))
        crown = hacking_check(intelligence_score=14, program_skill=1, difficulty=9,
                              wireless=True, vr_crown=True, dice=(3, 4))
        self.assertEqual(wired.total - wireless.total, -WIRELESS_PENALTY)
        self.assertEqual(wired.total - crown.total, -(WIRELESS_PENALTY + VR_CROWN_PENALTY))
        self.assertEqual(wired.total - crown.total, 3)

    def test_an_untrained_hacker_takes_minus_one(self):
        check = hacking_check(intelligence_score=10, program_skill=None, difficulty=8, dice=(4, 4))
        self.assertTrue(check.untrained)
        self.assertEqual(check.total, 7)

    def test_the_verb_modifier_is_applied(self):
        check = hacking_check(intelligence_score=14, program_skill=1, difficulty=9,
                              verb_modifier=-2, dice=(5, 5))
        self.assertEqual(check.total, 10 + 1 + 1 - 2)

    def test_circumstances_are_clamped_but_penalties_are_not(self):
        check = hacking_check(intelligence_score=14, program_skill=1, difficulty=9,
                              situational=-5, wireless=True, dice=(5, 5))
        self.assertEqual(check.situational, -2)
        self.assertEqual(check.connection_penalty, -2)
        self.assertEqual(check.total, 10 + 1 + 1 - 2 - 2)

    def test_dice_may_be_injected_for_a_replay(self):
        first = hacking_check(intelligence_score=12, program_skill=2, difficulty=9,
                              rng=random.Random(652))
        second = hacking_check(intelligence_score=12, program_skill=2, difficulty=9,
                               rng=random.Random(652))
        self.assertEqual(first.dice, second.dice)
        with self.assertRaises(HackError):
            hacking_check(intelligence_score=12, program_skill=2, difficulty=9, dice=(0, 7))


class AlertClockTests(unittest.TestCase):
    def test_two_failures_are_one_alert_action_and_two_actions_alert_the_network(self):
        clock = AlertClock()
        self.assertFalse(clock.record_failure())
        self.assertEqual(clock.alert_actions, 0)
        self.assertFalse(clock.record_failure())          # first Alert action
        self.assertEqual(clock.alert_actions, 1)
        self.assertFalse(clock.record_failure())
        self.assertTrue(clock.record_failure())           # second Alert action: alerted
        self.assertEqual(clock.alert_actions, ALERT_ACTIONS_TO_ALERT)
        self.assertTrue(clock.alerted)

    def test_a_demon_can_alert_without_a_failed_check(self):
        clock = AlertClock()
        self.assertFalse(clock.record_alert_action())
        self.assertTrue(clock.record_alert_action())
        self.assertTrue(clock.alerted)


if __name__ == "__main__":
    unittest.main()
