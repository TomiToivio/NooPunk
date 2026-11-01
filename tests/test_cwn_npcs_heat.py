"""Vanilla CWN reaction, morale and Heat procedures (#1025)."""
from __future__ import annotations

import unittest

from src.rules.cwn_heat import HeatError, HeatTrack, heat_band
from src.rules.cwn_npcs import NpcRuleError, morale_check, reaction_band, reaction_roll


class ReactionTests(unittest.TestCase):
    def test_reaction_table_boundaries(self) -> None:
        for total, band in ((2, "violent_hostile"), (3, "hostile"), (5, "hostile"),
                            (6, "neutral"), (8, "neutral"), (9, "friendly"),
                            (11, "friendly"), (12, "helpful")):
            self.assertEqual(reaction_band(total), band)

    def test_roll_applies_charisma_and_caps_at_the_table(self) -> None:
        self.assertEqual(reaction_roll(3, 3, 0).band, "neutral")
        self.assertEqual(reaction_roll(1, 1, 2).total, 4)
        self.assertEqual(reaction_roll(1, 1, 2).band, "hostile")
        self.assertEqual(reaction_roll(6, 6, 2).band, "helpful")

    def test_impossible_dice_and_modifiers_are_refused(self) -> None:
        with self.assertRaises(NpcRuleError):
            reaction_roll(0, 3)
        with self.assertRaises(NpcRuleError):
            reaction_roll(3, 3, 3)
        with self.assertRaises(NpcRuleError):
            reaction_band(13)


class MoraleTests(unittest.TestCase):
    def test_equal_or_higher_breaks_and_lower_holds(self) -> None:
        self.assertTrue(morale_check(6, 6, 12).broken)
        self.assertFalse(morale_check(6, 5, 12).broken)
        self.assertTrue(morale_check(2, 2, 4).broken)
        self.assertFalse(morale_check(2, 1, 4).broken)

    def test_morale_is_two_to_twelve(self) -> None:
        with self.assertRaises(NpcRuleError):
            morale_check(3, 3, 1)
        with self.assertRaises(NpcRuleError):
            morale_check(3, 3, 13)


class HeatTests(unittest.TestCase):
    def test_heat_band_boundaries(self) -> None:
        for score, band in ((0, "avoided"), (1, "low"), (3, "low"), (4, "significant"),
                            (5, "significant"), (6, "hunted"), (7, "hunted"),
                            (8, "overwhelmed"), (9, "overwhelmed"),
                            (10, "megacorp_enemy"), (30, "megacorp_enemy")):
            self.assertEqual(heat_band(score)[0], band)

    def test_heat_is_team_wide_and_never_negative(self) -> None:
        track = HeatTrack()
        self.assertEqual(track.add(5), 5)
        self.assertEqual(track.band, "significant")
        self.assertEqual(track.reduce(2), 3)
        self.assertEqual(track.reduce(99), 0)
        with self.assertRaises(HeatError):
            HeatTrack(-1)
        with self.assertRaises(HeatError):
            track.add(-1)
