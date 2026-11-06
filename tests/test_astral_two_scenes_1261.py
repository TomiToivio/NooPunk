"""The two-scene astral acceptance test the issue names (#1261).

The author's governing comment specifies a concrete demonstration:

> **Concrete two-scene test:** first awkward bedroom OOBE with the real room visible; later lucid
> flying over near-Astral Helsinki and entering a dream landscape. After return, physical body remains
> anchored and no illegal investigation shortcut is produced.

The rank ladder, the gates and the astral body already exist (#1264, #1262). What these tests add is
the *scenes*: they play the two situations in the order the author describes and assert the
differences a player would actually feel — and, just as importantly, the shortcuts that must **not**
appear.
"""

from __future__ import annotations

import unittest

from src.rules.astral_body import (
    AstralBodyError,
    Embodiment,
    EntryTrigger,
    PerceptionMode,
    TargetKind,
    apply_astral_damage,
    begin_projection,
)
from src.rules.astral_progression import (
    AstralProgressionError,
    duration_cap_minutes,
    rank_of,
    require_plane,
    require_starting_rank,
    require_technique,
)

BEDROOM = "loc.sornainen.home.bedroom"


class SceneOneAwkwardOobeTest(unittest.TestCase):
    """Rank 0: the real room is visible, wrong, and not a reconnaissance report."""

    def setUp(self) -> None:
        self.rank = require_starting_rank(0)
        self.projection = begin_projection("act.rookie", BEDROOM, EntryTrigger.SLEEP)

    def test_the_body_stays_in_the_bedroom(self) -> None:
        self.assertIs(self.projection.embodiment, Embodiment.PROJECTED)
        self.assertTrue(self.projection.body_is_fixed)
        self.assertEqual(self.projection.body_location, BEDROOM)

    def test_the_physical_room_is_visible_but_unreliable(self) -> None:
        seen = self.projection.sees(TargetKind.PHYSICAL)
        self.assertTrue(seen.allowed, "rank 0 still sees the ordinary world")
        self.assertFalse(seen.reliable, "and must not be given a trustworthy reconnaissance report")
        self.assertIn("fallible", seen.reason)

    def test_the_projection_cannot_touch_or_move_anything_physical(self) -> None:
        self.assertFalse(self.projection.may_take_physical_action())
        self.assertFalse(self.projection.may_speak_to_material())

    def test_rank_zero_cannot_fly(self) -> None:
        self.assertFalse(self.rank.flight)

    def test_rank_zero_cannot_enter_the_lower_astral(self) -> None:
        self.assertFalse(self.rank.lower_astral)

    def test_switching_to_time_space_needs_an_authored_transition(self) -> None:
        with self.assertRaises(AstralBodyError):
            self.projection.shift_mode(PerceptionMode.TIME_SPACE)

    def test_returning_leaves_the_body_where_it_was(self) -> None:
        returned = self.projection.return_to_body()
        self.assertIs(returned.embodiment, Embodiment.RETURNED)
        self.assertFalse(returned.active)
        self.assertEqual(returned.body_location, BEDROOM, "the body never travelled")

    def test_the_provisional_duration_cap_is_ten_minutes(self) -> None:
        self.assertEqual(duration_cap_minutes(0), 10)
        self.assertEqual(self.rank.duration_cap_minutes, 10)


class SceneTwoLucidFlightTest(unittest.TestCase):
    """Rank 1: flight and the Lower Astral open; ROTE, Ident and editing do not."""

    def setUp(self) -> None:
        self.rank = require_starting_rank(1)
        self.projection = begin_projection("act.rookie", BEDROOM, EntryTrigger.SLEEP)

    def test_flight_and_lower_astral_are_what_rank_one_adds(self) -> None:
        self.assertTrue(self.rank.flight)
        self.assertTrue(self.rank.lower_astral)
        self.assertFalse(rank_of(0).flight, "the difference must be a real difference")

    def test_rote_and_ident_stay_closed(self) -> None:
        self.assertFalse(self.rank.rote)
        self.assertFalse(self.rank.ident_learn)
        with self.assertRaises(AstralProgressionError):
            require_technique(1, "rote")
        with self.assertRaises(AstralProgressionError):
            require_technique(1, "use_ident")

    def test_higher_planes_are_rank_four_not_rank_one(self) -> None:
        for plane in ("devachanic", "etheric", "buddhic"):
            with self.assertRaises(AstralProgressionError):
                require_plane(1, plane)
        for plane in ("devachanic", "etheric", "buddhic"):
            require_plane(4, plane)  # the gate opens only at the top of the ladder

    def test_the_body_is_still_anchored_while_flying(self) -> None:
        self.assertTrue(self.projection.body_is_fixed)
        self.assertEqual(self.projection.body_location, BEDROOM)
        self.assertFalse(self.projection.may_take_physical_action())

    def test_the_duration_cap_is_sixty_minutes_and_still_provisional(self) -> None:
        self.assertEqual(duration_cap_minutes(1), 60)


class NoShortcutTest(unittest.TestCase):
    """Projection must not become an investigation bypass or a second combat system."""

    def test_a_projection_yields_no_evidence_object(self) -> None:
        """There is no clue, tag or evidence return value from projecting."""
        projection = begin_projection("act.rookie", BEDROOM, EntryTrigger.SLEEP)
        for name in dir(projection):
            self.assertNotIn(
                name,
                {"clues", "evidence", "tags", "clue_tags", "reveal"},
                f"{name!r} would let an OOBE hand the player evidence without an investigation",
            )

    def test_the_physical_world_and_symbols_are_never_seen_reliably(self) -> None:
        """What a projection reports about the ordinary world is a rendering, not a measurement.

        Astral agents are the one thing perceived *natively* here — reliable as a presence, which
        still says nothing about their identity, intent or what any of it means in the physical world.
        """
        projection = begin_projection("act.rookie", BEDROOM, EntryTrigger.SLEEP)
        self.assertFalse(projection.sees(TargetKind.PHYSICAL).reliable)
        self.assertFalse(projection.sees(TargetKind.SYMBOL).reliable)
        native = projection.sees(TargetKind.ASTRAL_AGENT)
        self.assertTrue(native.reliable, "agents are native to the Astral and are perceived as presences")
        self.assertNotIn("identity", native.reason.lower())

    def test_astral_damage_is_not_yet_bridged_to_cwn(self) -> None:
        """The author has not approved the damage bridge; the function refuses rather than guesses."""
        with self.assertRaises(AstralBodyError) as caught:
            apply_astral_damage("act.rookie", 3)
        self.assertIn("not approved", str(caught.exception))


class CreationGateTest(unittest.TestCase):
    def test_a_character_may_start_at_rank_zero_or_one(self) -> None:
        for rank in (0, 1):
            self.assertEqual(require_starting_rank(rank).rank, rank)

    def test_ranks_two_to_four_are_refused_at_creation(self) -> None:
        for rank in (2, 3, 4):
            with self.assertRaises(AstralProgressionError) as caught:
                require_starting_rank(rank)
            self.assertIn("may not start above", str(caught.exception))

    def test_a_rank_outside_the_ladder_is_refused(self) -> None:
        for rank in (-1, 5):
            with self.assertRaises(AstralProgressionError):
                require_starting_rank(rank)


if __name__ == "__main__":
    unittest.main()
