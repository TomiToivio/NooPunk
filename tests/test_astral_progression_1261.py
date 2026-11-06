"""Issue #1261: rank-gated Astral Projection without CWN/SWN rewrites."""
from __future__ import annotations

import unittest

from src.rules.astral_body import EntryTrigger, PerceptionMode, TargetKind, begin_projection
from src.rules.astral_progression_1261 import (
    AstralRankAction, authorize_rank_action, describe_rank, starting_rank_allowed,
)


def body():
    return begin_projection("tony.german", "home.helsinki", EntryTrigger.SLEEP)


class AstralProgressionTests(unittest.TestCase):
    def test_starting_campaign_only_zero_and_one(self):
        self.assertTrue(starting_rank_allowed(0))
        self.assertTrue(starting_rank_allowed(1))
        for rank in (-1, 2, 3, 4, True):
            self.assertFalse(starting_rank_allowed(rank))

    def test_zero_observes_walks_and_returns(self):
        p = body()
        for action in ("observe", "walk", "astral_contact", "return"):
            self.assertTrue(authorize_rank_action(p, 0, action).allowed)
        self.assertEqual(p.body_location, "home.helsinki")
        self.assertFalse(p.sees(TargetKind.PHYSICAL).reliable)

    def test_zero_cannot_fly_or_enter_dream(self):
        p = body()
        self.assertFalse(authorize_rank_action(p, 0, "fly").allowed)
        self.assertFalse(authorize_rank_action(
            p, 0, "enter_lower_astral", authored_gateway=True
        ).allowed)

    def test_one_flight_is_astral_only(self):
        p = body()
        self.assertTrue(authorize_rank_action(p, 1, "fly").allowed)
        self.assertFalse(p.may_take_physical_action())
        self.assertEqual(p.body_location, "home.helsinki")

    def test_one_dream_gateway_must_be_authored(self):
        p = body()
        self.assertFalse(authorize_rank_action(p, 1, "enter_lower_astral").allowed)
        self.assertTrue(authorize_rank_action(
            p, 1, "enter_lower_astral", authored_gateway=True
        ).allowed)

    def test_gateway_does_not_bypass_mode_filter(self):
        p = body()
        self.assertTrue(authorize_rank_action(
            p, 1, AstralRankAction.ENTER_LOWER_ASTRAL, authored_gateway=True
        ).allowed)
        p.shift_mode(PerceptionMode.TIME_SPACE, authored=True)
        self.assertFalse(p.sees(TargetKind.PHYSICAL).allowed)
        self.assertFalse(authorize_rank_action(p, 1, "fly").allowed)

    def test_two_through_four_remain_design_only_even_if_rank_is_supplied(self):
        p = body()
        for rank, action in ((2, "transmit_rote"), (2, "learn_ident"),
                             (3, "use_ident"), (3, "edit_quantum_information"),
                             (4, "enter_higher_planes")):
            result = authorize_rank_action(p, rank, action)
            self.assertFalse(result.allowed)
            self.assertIn("design-only", result.reason)

    def test_return_closes_actions(self):
        p = body()
        p.return_to_body()
        self.assertFalse(authorize_rank_action(p, 1, "fly").allowed)
        self.assertEqual(p.body_location, "home.helsinki")

    def test_unknown_action_or_invalid_rank_fails_closed(self):
        p = body()
        self.assertFalse(authorize_rank_action(p, 1, "hack_bank").allowed)
        self.assertFalse(authorize_rank_action(p, True, "observe").allowed)

    def test_rank_descriptions_do_not_leak_network_or_ident_to_rookies(self):
        for rank in (0, 1):
            text = describe_rank(rank).lower()
            self.assertNotIn("ident", text)
            self.assertNotIn("akashic", text)


if __name__ == "__main__":
    unittest.main()
