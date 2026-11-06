"""#1230 Phase 1: one clock, one queue, no double-fired events.

The tests are written against the acceptance criteria in the issue, not against the implementation:

* three consecutive days fast-forward with appointments firing in order;
* a save resumed mid-window does not re-fire anything;
* a local time that does not exist is refused rather than silently shifted.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simulation.clock import HELSINKI, ClockError, GameClock  # noqa: E402
from simulation.scheduler import DueEvent, Scheduler, SchedulerError  # noqa: E402

TZ = ZoneInfo(HELSINKI)


def moment(year=2041, month=3, day=4, hour=8, minute=0):
    return GameClock.local(year, month, day, hour, minute)


def at(clock: GameClock, days=0, minutes=0):
    return clock.now + timedelta(days=days, minutes=minutes)


class ClockTests(unittest.TestCase):
    def test_the_clock_starts_where_it_is_told(self):
        clock = GameClock.start(year=2041, month=3, day=4, hour=8)
        self.assertEqual(clock.now.hour, 8)
        self.assertEqual(clock.date_key, "2041-03-04")
        self.assertEqual(clock.zone, HELSINKI)

    def test_a_naive_moment_is_refused(self):
        with self.assertRaises(ClockError):
            GameClock(now=datetime(2041, 3, 4, 8, 0))

    def test_time_only_moves_forward(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        self.assertEqual((clock.advance(minutes=90).now - clock.now), timedelta(minutes=90))
        self.assertEqual((clock.advance(days=3).now - clock.now), timedelta(days=3))
        with self.assertRaises(ClockError):
            clock.advance(minutes=-1)
        with self.assertRaises(ClockError):
            clock.advance()

    def test_the_clock_does_not_mutate(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        clock.advance(minutes=30)
        self.assertEqual(clock.now.hour, 8, "advance returned a new clock; the original is unchanged")

    def test_advance_to_refuses_the_past(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        with self.assertRaises(ClockError):
            clock.advance_to(clock.now)
        self.assertEqual(clock.advance_to(at(clock, days=1)).now, clock.now + timedelta(days=1))

    def test_minutes_until_is_signed(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        self.assertEqual(clock.minutes_until(at(clock, minutes=45)), 45)
        self.assertEqual(clock.minutes_until(at(clock, minutes=-45)), -45)

    def test_a_local_time_that_does_not_exist_is_refused(self):
        """Helsinki springs forward at 03:00 on the last Sunday of March; 03:30 never happens."""
        with self.assertRaises(ClockError):
            GameClock.local(2041, 3, 31, 3, 30)

    def test_a_normal_local_time_round_trips(self):
        self.assertEqual(GameClock.local(2041, 3, 31, 4, 30).hour, 4)

    def test_the_clock_survives_a_save_and_a_load(self):
        clock = GameClock.start(year=2041, month=3, day=4, hour=17, minute=25).advance(minutes=15)
        restored = GameClock.from_dict(json.loads(json.dumps(clock.to_dict())))
        self.assertEqual(restored, clock)
        self.assertEqual(restored.now.utcoffset(), clock.now.utcoffset())


class SchedulerBasicsTests(unittest.TestCase):
    def test_due_events_are_ordered_by_time_then_id(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        same = at(clock, minutes=10)
        for event_id in ("c", "a", "b"):
            queue.schedule(DueEvent(event_id, same, "briefing"))
        queue.schedule(DueEvent("early", at(clock, minutes=5), "alarm"))
        names = [event.id for event in queue.due(clock, horizon_minutes=60)]
        self.assertEqual(names, ["early", "a", "b", "c"])

    def test_future_events_are_not_due(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        queue.schedule(DueEvent("tomorrow", at(clock, days=1), "briefing"))
        self.assertEqual(queue.due(clock), ())
        self.assertEqual(queue.next_due().id, "tomorrow")

    def test_an_event_due_exactly_now_fires(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        queue.schedule(DueEvent("now", clock.now, "briefing"))
        self.assertEqual([e.id for e in queue.due(clock)], ["now"])

    def test_rescheduling_the_same_event_is_a_no_op(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        event = DueEvent("briefing", at(clock, minutes=5), "briefing", {"room": "ratakatu"})
        self.assertTrue(queue.schedule(event))
        self.assertFalse(queue.schedule(event))
        self.assertEqual(len(queue.pending), 1)

    def test_rescheduling_with_different_content_is_refused(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        queue.schedule(DueEvent("briefing", at(clock, minutes=5), "briefing"))
        with self.assertRaises(SchedulerError):
            queue.schedule(DueEvent("briefing", at(clock, minutes=9), "briefing"))

    def test_a_fired_id_cannot_be_scheduled_again(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        queue.schedule(DueEvent("briefing", clock.now, "briefing"))
        queue.run(clock, lambda event: None)
        with self.assertRaises(SchedulerError):
            queue.schedule(DueEvent("briefing", at(clock, days=1), "briefing"))

    def test_a_naive_due_time_is_refused(self):
        with self.assertRaises(SchedulerError):
            DueEvent("x", datetime(2041, 3, 4, 9, 0), "briefing")

    def test_cancelling_a_pending_event_removes_it(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        queue.schedule(DueEvent("briefing", clock.now, "briefing"))
        self.assertIsNotNone(queue.cancel("briefing"))
        self.assertIsNone(queue.cancel("briefing"))
        self.assertEqual(queue.due(clock), ())


class IdempotencyTests(unittest.TestCase):
    def test_running_the_same_window_twice_fires_nothing_the_second_time(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        queue.schedule(DueEvent("a", clock.now, "briefing"))
        queue.schedule(DueEvent("b", at(clock, minutes=5), "task"))
        fired = []
        queue.run(clock.advance(minutes=10), fired.append)
        self.assertEqual([e.id for e in fired], ["a", "b"])
        again = queue.run(clock.advance(minutes=10), fired.append)
        self.assertEqual(again, ())
        self.assertEqual(len(fired), 2)

    def test_a_handler_that_raises_still_consumes_the_event(self):
        """The guarantee is 'at most once', even when the caller breaks. A crash must not replay a world event."""
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        queue.schedule(DueEvent("a", clock.now, "briefing"))

        def explode(event):
            raise RuntimeError("handler bug")

        with self.assertRaises(RuntimeError):
            queue.run(clock, explode)
        self.assertEqual(queue.run(clock, lambda event: None), ())
        self.assertEqual(queue.fired, ["a"])

    def test_a_save_resumed_mid_window_does_not_re_fire(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        for index in range(3):
            queue.schedule(DueEvent(f"e{index}", at(clock, minutes=index * 10), "task"))
        seen = []
        queue.run(clock.advance(minutes=15), seen.append)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "save.json"
            queue.save(path, clock.advance(minutes=15))
            restored_clock, restored_queue = Scheduler.load(path)

        self.assertEqual(restored_clock.now, clock.advance(minutes=15).now)
        self.assertEqual(restored_queue.fired, ["e0", "e1"])
        # At +15 nothing else is due yet: the resumed queue knows the past fired and the future has not arrived.
        self.assertEqual([e.id for e in restored_queue.due(restored_clock)], [])
        restored_queue.run(restored_clock.advance(minutes=10), seen.append)
        self.assertEqual([e.id for e in seen], ["e0", "e1", "e2"])

    def test_a_corrupt_save_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "save.json"
            path.write_text(json.dumps({"version": 99, "clock": {}, "scheduler": {}}), encoding="utf-8")
            with self.assertRaises(SchedulerError):
                Scheduler.load(path)


class ThreeDayFastForwardTests(unittest.TestCase):
    """The acceptance test's scheduling half: three days, briefings every morning, one appointment, no duplicates."""

    def test_three_days_of_morning_briefings_fire_in_order_once_each(self):
        clock = GameClock.start(year=2041, month=3, day=4, hour=7)
        queue = Scheduler()
        queue.schedule(DueEvent("appointment:dentist", at(clock, days=1, minutes=600), "appointment"))

        fired: list[str] = []

        def handler(event: DueEvent) -> None:
            # The queue never re-arms; the daily loop would enqueue tomorrow's briefing here.
            fired.append(event.id)

        for day in range(3):
            queue.schedule(DueEvent(f"briefing:day{day}", at(clock, days=day, minutes=60), "briefing"))

        current = clock
        for _ in range(3):
            current = current.advance(days=1)
            queue.run(current, handler)

        self.assertEqual(fired, ["briefing:day0", "briefing:day1", "appointment:dentist", "briefing:day2"])

    def test_next_due_supports_fast_forward_without_simulating_minutes(self):
        clock = GameClock.start(year=2041, month=3, day=4)
        queue = Scheduler()
        queue.schedule(DueEvent("later", at(clock, days=2), "appointment"))
        upcoming = queue.next_due()
        self.assertIsNotNone(upcoming)
        self.assertEqual(clock.advance_to(upcoming.due).now, at(clock, days=2))


if __name__ == "__main__":
    unittest.main()
