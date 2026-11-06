"""Acceptance tests for the living-campaign clock, tasks, arcs and dreams (#1230)."""

import unittest

from src.campaign import (
    Arc,
    ClockError,
    DailyLoop,
    DayTemplate,
    DreamEngine,
    DreamKind,
    EventLog,
    FiredEvent,
    GameClock,
    GameTime,
    ScheduledEvent,
    StoryDirector,
    Task,
    TaskBoard,
)


class ClockTest(unittest.TestCase):
    def test_time_advances_across_midnight(self):
        self.assertEqual(GameTime(1, 23 * 60 + 30).add(60), GameTime(2, 30))
        self.assertEqual(GameTime(1, 0).weekday, "Monday")
        self.assertTrue(GameTime(6, 0).is_weekend)

    def test_due_events_fire_once_and_replay_is_idempotent(self):
        clock = GameClock(GameTime(1, 0))
        clock.schedule(ScheduledEvent("briefing", GameTime(1, 8 * 60), "briefing"))
        clock.schedule(ScheduledEvent("late", GameTime(1, 9 * 60), "appointment"))
        first = clock.advance(8 * 60)
        self.assertEqual([event.id for event in first], ["briefing"])
        again = clock.advance(8 * 60)
        self.assertEqual([event.id for event in again], ["late"])
        self.assertFalse(clock.advance(8 * 60))
        self.assertEqual(len(clock.log.entries), 2)

    def test_duplicate_scheduled_id_is_rejected(self):
        clock = GameClock()
        event = ScheduledEvent("same", GameTime(1, 60), "x")
        clock.schedule(event)
        with self.assertRaises(ClockError):
            clock.schedule(event)

    def test_save_and_load_preserve_time_queue_and_log(self):
        clock = GameClock(GameTime(1, 0))
        clock.schedule(ScheduledEvent("briefing", GameTime(1, 8 * 60), "briefing"))
        clock.advance(8 * 60)
        restored = GameClock.from_snapshot(clock.snapshot())
        self.assertEqual(restored.time, clock.time)
        self.assertEqual(restored.snapshot(), clock.snapshot())
        self.assertEqual(restored.log.entries, clock.log.entries)


class TaskTest(unittest.TestCase):
    def test_partial_progress_can_span_days(self):
        board = TaskBoard()
        board.add(Task("report", "Write the Europol report", 240))
        board.start("report")
        board.advance("report", 120)
        self.assertFalse(board.task("report").completed)
        board.advance("report", 120)
        self.assertTrue(board.task("report").completed)

    def test_failed_check_costs_time_and_quality_not_all_progress(self):
        board = TaskBoard()
        board.add(Task("archive", "Search the archive", 120, difficulty=10))
        board.start("archive")
        result = board.advance("archive", 30, check_total=8)
        self.assertFalse(result.success)
        self.assertEqual(result.quality, "reduced")
        self.assertEqual(board.task("archive").remaining_minutes, 120)
        self.assertFalse(board.task("archive").completed)

    def test_pause_resume_interrupt_and_double_spend_guard(self):
        board = TaskBoard()
        board.add(Task("guard", "Guard the warehouse", 60))
        board.start("guard")
        board.interrupt("guard")
        self.assertEqual(board.task("guard").state, "paused")
        board.start("guard")
        board.advance("guard", 60)
        self.assertTrue(board.task("guard").completed)
        result = board.advance("guard", 10)
        self.assertEqual(result.elapsed_minutes, 0)
        self.assertTrue(result.completed)

    def test_task_roundtrip(self):
        board = TaskBoard()
        board.add(Task("read", "Read the file", 45, difficulty=8))
        board.start("read")
        board.advance("read", 15)
        restored = TaskBoard.from_snapshot(board.snapshot())
        self.assertEqual(restored.snapshot(), board.snapshot())


class StoryTest(unittest.TestCase):
    def test_arc_activates_progresses_and_resolves_without_spoiler_text(self):
        director = StoryDirector()
        director.add(
            Arc(
                "arc.continuity",
                "The Continuity Business",
                "conditional",
                activation_event="complaint_filed",
                progress_events=("invoice_found", "witness_talks"),
                resolution_event="case_closed",
                goal_ids=("goal.case",),
            )
        )
        self.assertEqual(director.on_event("complaint_filed"), ("arc.continuity",))
        self.assertEqual(director.on_event("invoice_found"), ("arc.continuity",))
        active = director.active()
        self.assertEqual(active[0]["title"], "The Continuity Business")
        self.assertNotIn("goal_ids", active[0])
        self.assertEqual(director.on_event("case_closed"), ("arc.continuity",))
        self.assertEqual(director.arcs["arc.continuity"].status, "resolved")
        self.assertEqual(director.active(), ())


class DreamTest(unittest.TestCase):
    def test_many_nights_have_no_recalled_dream(self):
        engine = DreamEngine()
        self.assertEqual(engine.choose(1, forced=DreamKind.NONE).kind, DreamKind.NONE)
        self.assertFalse(engine.choose(1, forced=DreamKind.NONE).is_playable_dream)

    def test_spontaneous_precognition_needs_no_swm_ability(self):
        dream = DreamEngine().choose(3, forced=DreamKind.SPONTANEOUS_PRECOGNITION)
        self.assertEqual(dream.kind, DreamKind.SPONTANEOUS_PRECOGNITION)
        self.assertTrue(dream.possible_future)
        self.assertFalse(dream.reliable)

    def test_psychic_attack_is_a_scene_not_a_free_damage_rule(self):
        dream = DreamEngine().choose(
            4, forced=DreamKind.PSYCHIC_ATTACK, source="npc.mantid"
        )
        self.assertEqual(dream.kind, DreamKind.PSYCHIC_ATTACK)
        self.assertIn("SWN/CWN", dream.mechanic)
        self.assertEqual(dream.source, "npc.mantid")

    def test_selection_is_deterministic_by_night_and_seed(self):
        engine = DreamEngine()
        first = engine.choose(7, seed=42)
        second = engine.choose(7, seed=42)
        self.assertEqual(first.kind, second.kind)


class ThreeDayIntegrationTest(unittest.TestCase):
    def test_three_days_of_daily_loop_tasks_and_dreams(self):
        loop = DailyLoop(GameClock(GameTime(1, 0)), template=DayTemplate())
        loop.schedule_day(1)

        # Day 1: morning briefing, a task, an appointment, sleep.
        fired = loop.advance(8 * 60)
        self.assertIn("morning_briefing", [event["kind"] for event in fired])
        board = TaskBoard()
        board.add(Task("research", "Read the 2043 archive", 240, difficulty=10))
        board.start("research")
        board.advance("research", 120, check_total=12)
        self.assertEqual(board.task("research").remaining_minutes, 120)
        loop.clock.schedule(
            ScheduledEvent("appointment", GameTime(1, 15 * 60), "appointment")
        )
        loop.advance(7 * 60)
        dream = loop.sleep(forced_dream=DreamKind.LIFEPATH_MEMORY)
        self.assertEqual(dream.kind, DreamKind.LIFEPATH_MEMORY)

        # Day 2: wake, finish the task, keep the appointment.
        loop.advance(8 * 60)  # 23:00 -> 07:00 next day
        self.assertEqual(loop.clock.time.day, 2)
        board.advance("research", 120)
        self.assertTrue(board.task("research").completed)
        loop.clock.schedule(
            ScheduledEvent("appointment2", GameTime(2, 10 * 60), "appointment")
        )
        loop.advance(3 * 60)
        self.assertTrue(loop.clock.log.has("appointment2"))

        # Day 3: event-driven fast-forward reaches the next structural event.
        loop.sleep(forced_dream=DreamKind.NONE)
        loop.advance(8 * 60)
        loop.schedule_day(3)
        events = loop.fast_forward(limit_events=10)
        self.assertTrue(events)
        self.assertEqual(loop.clock.log.entries[-1].id, "day.3.sleep")

    def test_daily_loop_save_roundtrip_does_not_duplicate_events(self):
        loop = DailyLoop(GameClock(GameTime(1, 0)))
        loop.schedule_day(1)
        loop.advance(9 * 60)
        restored = DailyLoop.from_snapshot(loop.snapshot())
        self.assertEqual(restored.snapshot()["clock"], loop.snapshot()["clock"])
        # Rescheduling the same day must not create duplicate ids.
        restored.schedule_day(1)
        scheduled_ids = [row["id"] for row in restored.clock.scheduler.snapshot()]
        self.assertEqual(len(scheduled_ids), len(set(scheduled_ids)))

    def test_event_log_is_idempotent(self):
        log = EventLog()
        event = FiredEvent("e1", GameTime(1, 60), "test")
        self.assertTrue(log.record(event))
        self.assertFalse(log.record(event))
        self.assertEqual(len(log.entries), 1)


if __name__ == "__main__":
    unittest.main()
