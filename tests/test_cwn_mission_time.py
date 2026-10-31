"""Scenes, rounds and mission time — every assertion traced to the CWN SRD section.

SRD: ``rules-of-the-game/scenes-rounds-mission-time/``
"""
import unittest

from src.rules.cwn_mission_time import (
    ROUND_SECONDS,
    SCENE_MINUTES,
    STANDARD_ACTION_MINUTES,
    MissionClock,
    MissionTimeError,
)


class ConstantsTests(unittest.TestCase):
    def test_a_round_is_six_seconds(self) -> None:
        self.assertEqual(ROUND_SECONDS, 6)

    def test_a_scene_is_ten_minutes(self) -> None:
        self.assertEqual(SCENE_MINUTES, 10)

    def test_a_standard_action_is_one_minute(self) -> None:
        self.assertEqual(STANDARD_ACTION_MINUTES, 1)


class AdvanceTests(unittest.TestCase):
    def test_the_clock_starts_at_minute_zero_in_scene_zero(self) -> None:
        clock = MissionClock()
        self.assertEqual((clock.minute, clock.scenes), (0, 0))

    def test_a_standard_action_costs_one_minute(self) -> None:
        clock = MissionClock()
        tick = clock.spend_action()
        self.assertEqual(tick.minute, 1)
        self.assertFalse(tick.scene_refreshed)

    def test_nine_minutes_do_not_spend_a_scene(self) -> None:
        clock = MissionClock()
        self.assertFalse(clock.advance(9).scene_refreshed)

    def test_the_tenth_minute_spends_the_scene(self) -> None:
        clock = MissionClock()
        tick = clock.advance(10)
        self.assertEqual((tick.minute, tick.scene), (10, 1))
        self.assertTrue(tick.scene_refreshed)

    def test_a_long_jump_reports_every_scene_it_crossed(self) -> None:
        clock = MissionClock()
        tick = clock.advance(35)
        self.assertEqual((tick.minute, tick.scene, tick.scenes_elapsed), (35, 3, 3))

    def test_the_boundary_between_scenes_is_the_exact_minute(self) -> None:
        clock = MissionClock()
        clock.advance(19)
        self.assertEqual(clock.scenes, 1)
        self.assertEqual(clock.advance(1).scenes_elapsed, 1)
        self.assertEqual(clock.scenes, 2)

    def test_backwards_is_refused(self) -> None:
        clock = MissionClock()
        with self.assertRaises(MissionTimeError):
            clock.advance(-1)
        with self.assertRaises(MissionTimeError):
            MissionClock(minute=-5)

    def test_a_zero_jump_is_a_no_op_not_an_error(self) -> None:
        clock = MissionClock(minute=7)
        tick = clock.advance(0)
        self.assertEqual((tick.minute, tick.scenes_elapsed, tick.scene_refreshed), (7, 0, False))


class SceneTests(unittest.TestCase):
    def test_minutes_into_scene_counts_the_current_window(self) -> None:
        clock = MissionClock(minute=13)
        self.assertEqual(clock.minutes_into_scene, 3)

    def test_ending_a_scene_early_refreshes_without_moving_the_clock(self) -> None:
        clock = MissionClock(minute=4)
        tick = clock.end_scene()
        self.assertEqual(tick.minute, 4)
        self.assertTrue(tick.scene_refreshed)
        self.assertEqual(clock.scenes, 1)

    def test_the_window_still_reads_from_the_minutes_after_an_early_end(self) -> None:
        clock = MissionClock(minute=4)
        clock.end_scene()
        self.assertEqual(clock.minutes_into_scene, 4)

    def test_a_restart_from_a_saved_minute_restores_the_scene(self) -> None:
        clock = MissionClock(minute=25)
        self.assertEqual(clock.scenes, 2)
        self.assertEqual(MissionClock(minute=25).scenes, clock.scenes)


class RoundTests(unittest.TestCase):
    def test_a_ten_minute_scene_holds_a_hundred_rounds(self) -> None:
        self.assertEqual((SCENE_MINUTES * 60) // ROUND_SECONDS, 100)


if __name__ == "__main__":
    unittest.main()
