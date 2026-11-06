"""#1261: the astral superskill's ranks, gates and permission model.

Written against the author's 2026-11-06 revision, whose test checklist is the list below. The tests refuse to let a
later change quietly promote a design-only rank into the opening campaign.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import astral_body  # noqa: E402
from rules.astral_ranks import (  # noqa: E402
    CAMPAIGN_MAX_STARTING_RANK,
    DURATIONS_ARE_PROVISIONAL,
    RANKS,
    AstralRankError,
    Capability,
    InformationPattern,
    Projector,
    capabilities_for,
    duration_cap_minutes,
    has,
    may_edit,
    rank_spec,
    require_edit,
    starting_rank,
)


class RankTableTests(unittest.TestCase):
    def test_every_rank_states_all_three_axes(self):
        for rank, spec in RANKS.items():
            self.assertEqual(spec.rank, rank)
            self.assertTrue(spec.name and spec.understanding and spec.perception and spec.actions, rank)

    def test_capabilities_are_cumulative(self):
        for rank in range(1, 5):
            self.assertTrue(capabilities_for(rank - 1) <= capabilities_for(rank),
                            f"rank {rank} must include everything rank {rank - 1} grants")

    def test_ranks_outside_zero_to_four_are_refused(self):
        for bad in (-1, 5, 2.5, True, "2"):
            with self.assertRaises(AstralRankError):
                rank_spec(bad)  # type: ignore[arg-type]

    def test_durations_are_marked_provisional(self):
        self.assertTrue(DURATIONS_ARE_PROVISIONAL)
        self.assertEqual([duration_cap_minutes(rank) for rank in range(5)],
                         [10, 60, 600, 2880, 10080])


class CampaignScopeTests(unittest.TestCase):
    def test_creation_allows_rank_zero_and_one_only(self):
        self.assertEqual(CAMPAIGN_MAX_STARTING_RANK, 1)
        self.assertEqual(starting_rank(0), 0)
        self.assertEqual(starting_rank(1), 1)
        for rank in (2, 3, 4):
            with self.assertRaises(AstralRankError):
                starting_rank(rank)

    def test_the_refusal_says_why(self):
        with self.assertRaises(AstralRankError) as caught:
            starting_rank(3)
        self.assertIn("design-only", str(caught.exception))

    def test_a_projector_knows_whether_it_may_start(self):
        self.assertTrue(Projector("tony.german", 1).may_start_campaign())
        self.assertFalse(Projector("npc.specialist", 3).may_start_campaign())


class RankZeroTests(unittest.TestCase):
    def test_rank_zero_separates_returns_and_walks(self):
        for capability in (Capability.SEPARATE, Capability.RETURN, Capability.WALK, Capability.PHYSICAL_OVERLAY):
            self.assertTrue(has(0, capability), capability)

    def test_rank_zero_cannot_fly_or_enter_the_lower_astral(self):
        self.assertFalse(has(0, Capability.FLIGHT))
        self.assertFalse(has(0, Capability.LOWER_ASTRAL))
        self.assertFalse(has(0, Capability.DREAM_ENTRY))
        self.assertFalse(has(0, Capability.LUCID))

    def test_rank_zero_sees_the_physical_overlay_but_not_dreams(self):
        self.assertTrue(has(0, Capability.PHYSICAL_OVERLAY))
        self.assertFalse(has(0, Capability.DREAM_ENTRY))


class RankOneTests(unittest.TestCase):
    def test_rank_one_unlocks_flight_and_dream_navigation(self):
        for capability in (Capability.LUCID, Capability.FLIGHT, Capability.LOWER_ASTRAL, Capability.DREAM_ENTRY):
            self.assertTrue(has(1, capability), capability)

    def test_rank_one_does_not_unlock_rote_or_ident(self):
        for capability in (Capability.ROTE, Capability.LEARN_IDENT, Capability.USE_IDENT):
            self.assertFalse(has(1, capability), capability)

    def test_rank_one_does_not_edit_or_reach_higher_planes(self):
        self.assertFalse(has(1, Capability.EDIT_OWN_INFORMATION))
        self.assertFalse(has(1, Capability.HIGHER_PLANES))
        self.assertFalse(has(1, Capability.AKASHIC))


class HigherRankTests(unittest.TestCase):
    def test_rote_arrives_at_rank_two_ident_use_at_three(self):
        self.assertTrue(has(2, Capability.ROTE))
        self.assertTrue(has(2, Capability.LEARN_IDENT))
        self.assertFalse(has(2, Capability.USE_IDENT))
        self.assertTrue(has(3, Capability.USE_IDENT))

    def test_higher_planes_and_akashic_are_rank_four_only(self):
        for rank in range(4):
            self.assertFalse(has(rank, Capability.HIGHER_PLANES), rank)
            self.assertFalse(has(rank, Capability.AKASHIC), rank)
        self.assertTrue(has(4, Capability.HIGHER_PLANES))
        self.assertTrue(has(4, Capability.AKASHIC))


class InformationEditTests(unittest.TestCase):
    def test_rank_two_cannot_edit_anything(self):
        own = InformationPattern("self-memory", "tony.german", mutable=True)
        self.assertFalse(may_edit(2, "tony.german", own))

    def test_rank_three_edits_its_own_mutable_information(self):
        own = InformationPattern("self-memory", "tony.german", mutable=True)
        self.assertTrue(may_edit(3, "tony.german", own))

    def test_an_immutable_pattern_is_never_editable(self):
        fixed = InformationPattern("bank-record", "tony.german", mutable=False)
        for rank in range(5):
            self.assertFalse(may_edit(rank, "tony.german", fixed), rank)

    def test_another_agents_pattern_needs_a_mandate(self):
        other = InformationPattern("someone-elses-memory", "npc.witness", mutable=True)
        self.assertFalse(may_edit(3, "tony.german", other))
        self.assertTrue(may_edit(3, "tony.german", other, mandate=True))

    def test_rank_alone_never_grants_another_agents_information(self):
        other = InformationPattern("identity", "npc.witness", mutable=True)
        self.assertFalse(may_edit(4, "tony.german", other), "rank 4 is plane access, not a licence")

    def test_a_refused_edit_says_which_reason_applies(self):
        with self.assertRaises(AstralRankError) as caught:
            require_edit(3, "tony.german", InformationPattern("x", "npc.other", mutable=True))
        self.assertIn("another agent", str(caught.exception))
        with self.assertRaises(AstralRankError) as caught:
            require_edit(1, "tony.german", InformationPattern("x", "tony.german", mutable=True))
        self.assertIn("rank 1", str(caught.exception))


class NoDuplicateMechanismTests(unittest.TestCase):
    def test_the_projection_model_is_still_the_only_one(self):
        """The superskill adds capabilities, not a second body, sheet or combat system."""
        for banned in ("Projection", "Combatant", "Combat"):
            self.assertFalse(hasattr(sys.modules["rules.astral_ranks"], banned), banned)

    def test_astral_damage_remains_gated(self):
        self.assertFalse(astral_body.ASTRAL_DAMAGE_BRIDGE_APPROVED)

    def test_a_high_rank_still_cannot_act_physically_while_projected(self):
        projection = astral_body.begin_projection(
            "tony.german", "loc.sornainen_home", astral_body.EntryTrigger.SLEEP,
        )
        self.assertFalse(projection.may_take_physical_action())
        self.assertTrue(has(4, Capability.FLIGHT), "rank 4 is a navigator, not a poltergeist")

    def test_rote_and_ident_are_not_swn_techniques(self):
        """ROTE and Ident belong to Astral Projection, not to the SWN discipline catalogue."""
        from rules.psionics import load_catalogue

        catalogue = load_catalogue()
        for key in ("rote", "transmit_information", "learn_ident", "use_ident"):
            self.assertNotIn(key, catalogue)


if __name__ == "__main__":
    unittest.main()
