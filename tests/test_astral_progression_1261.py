"""The #1261 governing rank ladder, as gates rather than prose.

The author's 2026-11-06 update makes Astral Projection a superskill whose ranks describe understanding and
permission, keeps ranks 2–4 design-only, and moves Devachanic/Etheric/Buddhic access from rank 2 to rank 4.
These tests exist so that ladder cannot be skipped by a later edit, and so that a rank never becomes a
backdoor into CWN skills, hacking or the physical world.
"""
import unittest

from src.rules.astral_progression import (
    AstralProgressionError,
    assert_astral_domain_only,
    duration_cap_minutes,
    mvp_max_rank,
    rank_of,
    ranks,
    require_plane,
    require_playable,
    require_starting_rank,
    require_technique,
)


class RankTableTests(unittest.TestCase):
    def test_five_ranks_with_the_author_names(self):
        table = ranks()
        self.assertEqual(sorted(table), [0, 1, 2, 3, 4])
        self.assertEqual(table[0].name, "Disorientation")
        self.assertEqual(table[1].name, "Lucidity and dream navigation")
        self.assertEqual(table[2].name, "Conscious Agent Network")
        self.assertEqual(table[3].name, "Authorised informational agency")
        self.assertEqual(table[4].name, "Cosmological research")

    def test_only_ranks_zero_and_one_are_playable(self):
        table = ranks()
        self.assertEqual(mvp_max_rank(), 1)
        self.assertTrue(table[0].playable and table[1].playable)
        for rank in (2, 3, 4):
            self.assertFalse(table[rank].playable, f"rank {rank} must stay design-only")

    def test_rank_outside_zero_to_four_is_refused(self):
        for bad in (-1, 5, "three", None):
            with self.subTest(bad=bad):
                with self.assertRaises(AstralProgressionError):
                    rank_of(bad)


class MvpScopeTests(unittest.TestCase):
    def test_character_creation_refuses_two_to_four(self):
        self.assertEqual(require_starting_rank(0).rank, 0)
        self.assertEqual(require_starting_rank(1).rank, 1)
        for rank in (2, 3, 4):
            with self.subTest(rank=rank):
                with self.assertRaises(AstralProgressionError):
                    require_starting_rank(rank)

    def test_play_refuses_design_only_ranks(self):
        with self.assertRaises(AstralProgressionError):
            require_playable(2)


class RankCapabilityTests(unittest.TestCase):
    def test_rank_zero_has_no_flight_and_no_lower_astral(self):
        zero = rank_of(0)
        self.assertFalse(zero.flight)
        self.assertFalse(zero.lower_astral)
        self.assertTrue(zero.perception, "rank 0 still sees the near astral overlay")

    def test_rank_one_flies_and_enters_dream_worlds_but_cannot_rote(self):
        one = rank_of(1)
        self.assertTrue(one.flight)
        self.assertTrue(one.lower_astral)
        self.assertFalse(one.rote)
        with self.assertRaises(AstralProgressionError):
            require_technique(1, "rote")

    def test_rank_two_learns_rote_and_ident_but_does_not_use_ident(self):
        two = rank_of(2)
        self.assertTrue(two.rote)
        self.assertTrue(two.ident_learn)
        self.assertFalse(two.ident_use)
        require_technique(2, "rote")
        require_technique(2, "learn_ident")
        with self.assertRaises(AstralProgressionError):
            require_technique(2, "use_ident")

    def test_rank_three_uses_ident_and_rank_four_is_not_required(self):
        require_technique(3, "use_ident")
        require_technique(4, "use_ident")

    def test_an_unknown_technique_is_refused(self):
        with self.assertRaises(AstralProgressionError):
            require_technique(4, "astral teleport")


class PlaneAccessTests(unittest.TestCase):
    def test_higher_planes_are_rank_four(self):
        for plane in ("devachanic", "etheric", "buddhic"):
            with self.subTest(plane=plane):
                require_plane(4, plane)
                with self.assertRaises(AstralProgressionError):
                    require_plane(3, plane)
                with self.assertRaises(AstralProgressionError):
                    require_plane(2, plane)

    def test_akashic_records_are_rank_four(self):
        self.assertTrue(rank_of(4).akashic)
        for rank in (0, 1, 2, 3):
            self.assertFalse(rank_of(rank).akashic)


class DurationTests(unittest.TestCase):
    def test_provisional_caps_rise_with_rank(self):
        caps = [duration_cap_minutes(rank) for rank in range(5)]
        self.assertEqual(caps, [10, 60, 600, 2880, 10080])
        self.assertEqual(caps, sorted(caps), "a higher rank never has a shorter ceiling")


class DomainBoundaryTests(unittest.TestCase):
    def test_no_rank_claims_a_physical_cyber_or_hacking_power(self):
        assert_astral_domain_only()  # raises if a rank's capability text smuggles one in

    def test_time_space_is_not_a_rank_zero_or_one_capability(self):
        """Rank 1 enters dream worlds that resemble Time/Space; deliberate switching is a later permission."""
        self.assertFalse(rank_of(0).time_space)
        self.assertFalse(rank_of(1).time_space)

    def test_every_rank_states_what_it_understands(self):
        for rank in ranks().values():
            self.assertTrue(rank.understanding.strip(), f"rank {rank.rank} has no model of reality")
            self.assertTrue(rank.capability, f"rank {rank.rank} has no permission")


if __name__ == "__main__":
    unittest.main()
