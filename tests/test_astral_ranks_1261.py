"""Astral Projection as a ranked superskill, MVP levels 0-1 (#1261 author update 2026-11-06).

The author's latest direction makes Astral Projection a *superskill inside the Astral*: each rank is a
model of reality, a perception and a capability at once. The initial campaign allows 0 or 1; 2-4 are
designed, gated and refused until a later campaign earns them.

What is pinned here is only what the new direction states as testable behaviour. The provisional
duration caps are exposed as ceilings, not as promises: a longer projection does not yield better
knowledge, and the module says "provisional" in the only place it can — the constant's name.

`unittest`, because the CI gate runs `python -m unittest discover` and does not install pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.rules import psi_access
from src.rules.astral_body import (
    IDENT_SOURCES,
    MVP_RANKS,
    PROVISIONAL_MINUTES,
    AstralBodyError,
    AstralRank,
    AstralSkill,
    begin_projection,
    learn_ident,
    use_ident,
)


def ranked(rank: int) -> AstralSkill:
    return AstralSkill(rank=AstralRank(rank))


class TestCharacterCreationWindow(unittest.TestCase):
    def test_the_initial_campaign_allows_zero_or_one(self) -> None:
        self.assertEqual(tuple(int(rank) for rank in MVP_RANKS), (0, 1))
        for rank in (0, 1):
            self.assertEqual(int(AstralSkill.starting(rank).rank), rank)

    def test_ranks_two_to_four_are_refused_at_creation(self) -> None:
        for rank in (2, 3, 4):
            with self.assertRaises(AstralBodyError) as caught:
                AstralSkill.starting(rank)
            self.assertIn("not available at character creation", str(caught.exception))


class TestRankZeroIsDisorientation(unittest.TestCase):
    def test_no_flight_and_no_lower_astral(self) -> None:
        skill = ranked(0)
        self.assertFalse(skill.can_fly)
        self.assertFalse(skill.can_enter_lower_astral)
        self.assertEqual(skill.planes(), frozenset({"near_astral"}))

    def test_the_cap_is_ten_provisional_minutes(self) -> None:
        self.assertEqual(ranked(0).duration_cap_minutes(), 10)


class TestRankOneIsLucidity(unittest.TestCase):
    def test_flight_and_lower_astral_arrive_but_not_rote(self) -> None:
        skill = ranked(1)
        self.assertTrue(skill.can_fly)
        self.assertTrue(skill.can_enter_lower_astral)
        self.assertFalse(skill.can_send_rote)
        self.assertFalse(skill.can_learn_ident)
        self.assertEqual(skill.duration_cap_minutes(), 60)

    def test_the_upper_planes_are_not_reachable_at_one(self) -> None:
        for plane in ("devachanic", "etheric", "buddhic"):
            self.assertFalse(ranked(1).may_enter(plane), plane)


class TestRankTwoLearnsButCannotJump(unittest.TestCase):
    def test_rote_and_ident_learning_together(self) -> None:
        skill = ranked(2)
        self.assertTrue(skill.can_send_rote)
        self.assertTrue(skill.can_learn_ident)
        self.assertFalse(skill.can_use_ident)
        self.assertTrue(skill.understands_quantum_information)

    def test_learning_an_ident_at_two_cannot_yet_be_used(self) -> None:
        skill = ranked(2)
        ident = learn_ident(skill, "agent.wendt", via="authored_encounter")
        projection = begin_projection("pc.tony", "loc.hki.bedroom", "sleep")
        with self.assertRaises(AstralBodyError) as caught:
            use_ident(projection, skill, ident)
        self.assertIn("Use Ident is Astral Projection 3", str(caught.exception))


class TestRankThreeUseIdent(unittest.TestCase):
    def test_arrival_is_instant_and_only_the_astral_body_moves(self) -> None:
        skill = ranked(3)
        ident = learn_ident(skill, "agent.wendt", via="consensual_exchange")
        projection = begin_projection("pc.tony", "loc.hki.bedroom", "sleep")
        use_ident(projection, skill, ident)
        self.assertEqual(projection.astral_location, "presence:agent.wendt")
        self.assertEqual(projection.body_location, "loc.hki.bedroom")
        self.assertEqual(projection.actor_id, "pc.tony")
        self.assertTrue(projection.active)

    def test_a_ward_refuses_arrival_without_revealing_the_agent(self) -> None:
        skill = ranked(3)
        ident = learn_ident(skill, "agent.wendt", via="recognition_technique")
        projection = begin_projection("pc.tony", "loc.hki.bedroom", "sleep")
        with self.assertRaises(AstralBodyError) as caught:
            use_ident(projection, skill, ident, ward="AntiPSI shell")
        message = str(caught.exception)
        self.assertIn("not revealed", message)
        self.assertNotIn("agent.wendt", message)
        self.assertEqual(projection.astral_location, "")

    def test_a_plane_the_rank_does_not_reach_refuses_the_jump(self) -> None:
        skill = ranked(3)
        ident = learn_ident(skill, "agent.wendt", via="consensual_exchange")
        projection = begin_projection("pc.tony", "loc.hki.bedroom", "sleep")
        with self.assertRaises(AstralBodyError) as caught:
            use_ident(projection, skill, ident, plane="devachanic")
        self.assertIn("does not reach", str(caught.exception))

    def test_an_embodied_character_cannot_use_an_ident(self) -> None:
        skill = ranked(3)
        ident = learn_ident(skill, "agent.wendt", via="consensual_exchange")
        projection = begin_projection("pc.tony", "loc.hki.bedroom", "sleep").return_to_body()
        with self.assertRaises(AstralBodyError):
            use_ident(projection, skill, ident)


class TestIdentIsNotAName(unittest.TestCase):
    def test_a_photograph_or_a_name_does_not_establish_an_ident(self) -> None:
        skill = ranked(2)
        for via in ("a photograph", "her name", "her address", "the body in the morgue"):
            with self.assertRaises(AstralBodyError) as caught:
                learn_ident(skill, "agent.wendt", via=via)
            self.assertIn("does not establish an Ident", str(caught.exception))

    def test_the_three_legitimate_sources_are_the_whole_list(self) -> None:
        self.assertEqual(
            IDENT_SOURCES, ("authored_encounter", "consensual_exchange", "recognition_technique")
        )

    def test_continuity_keeps_the_ident_and_duplication_does_not(self) -> None:
        ident = learn_ident(ranked(2), "agent.wendt", via="authored_encounter")
        for event in ("death", "reincarnation", "resleeve", "upload"):
            self.assertTrue(ident.survives(event), event)
        for event in ("copy", "fork", "simulation"):
            self.assertFalse(ident.survives(event), event)

    def test_an_unknown_continuity_event_is_refused_rather_than_guessed(self) -> None:
        ident = learn_ident(ranked(2), "agent.wendt", via="authored_encounter")
        with self.assertRaises(AstralBodyError):
            ident.survives("teleported by the plot")


class TestEditingIsPermissionNotPower(unittest.TestCase):
    def test_rank_three_edits_only_its_own_information_or_an_unclaimed_limbo(self) -> None:
        skill = ranked(3)
        self.assertTrue(skill.may_edit(owner="pc.tony", editor="pc.tony"))
        self.assertTrue(skill.may_edit(owner="limbo:unclaimed", editor="pc.tony"))
        self.assertFalse(skill.may_edit(owner="agent.wendt", editor="pc.tony"))

    def test_below_rank_three_nothing_is_editable(self) -> None:
        self.assertFalse(ranked(1).may_edit(owner="pc.tony", editor="pc.tony"))


class TestNoSecondEngine(unittest.TestCase):
    def test_projection_grants_no_swn_discipline_and_no_teleport_prerequisite(self) -> None:
        before = set(psi_access.PC_DISCIPLINES)
        skill = ranked(3)
        ident = learn_ident(skill, "agent.wendt", via="consensual_exchange")
        use_ident(begin_projection("pc.tony", "loc.hki.bedroom", "sleep"), skill, ident)
        self.assertEqual(set(psi_access.PC_DISCIPLINES), before)
        self.assertEqual({"Telekinesis", "Telepathy"}, set(psi_access.PC_DISCIPLINES))
        self.assertFalse(hasattr(skill, "teleportation"))
        self.assertFalse(hasattr(skill, "telepathy"))

    def test_the_duration_caps_are_named_provisional(self) -> None:
        self.assertIn("PROVISIONAL", "PROVISIONAL_MINUTES")
        self.assertEqual(set(PROVISIONAL_MINUTES), set(AstralRank))


if __name__ == "__main__":
    unittest.main()
