"""Replay must draw the same numbers, or a save stops reproducing (#1230).

#1230 makes this non-negotiable: *"Durable event IDs/idempotent reducers ... Deterministic RNG seeding
for tests, persistence and replay/debuggability."* The scheduler's idempotency covers the ids; these
tests cover the randomness, which is the half that fails silently — a replay that produces different
numbers still "works", it just quietly tells a different story.
"""

from __future__ import annotations

import hashlib
import random
import unittest
from datetime import UTC, datetime

from src.simulation.scheduler import DueEvent, Scheduler


def utc(day: int, hour: int = 8, minute: int = 0) -> datetime:
    return datetime(2045, 3, day, hour, minute, tzinfo=UTC)


class ReplayTest(unittest.TestCase):
    def test_the_same_event_draws_the_same_number_in_two_schedulers(self) -> None:
        first, second = Scheduler(), Scheduler()
        self.assertEqual(
            first.rng_for("briefing@2045-03-03").random(),
            second.rng_for("briefing@2045-03-03").random(),
        )

    def test_different_events_draw_different_numbers(self) -> None:
        scheduler = Scheduler()
        self.assertNotEqual(
            scheduler.rng_for("briefing@2045-03-03").random(),
            scheduler.rng_for("briefing@2045-03-04").random(),
        )

    def test_the_stream_is_independent_of_when_the_event_is_handled(self) -> None:
        """Same event id, different queue order: the draw must not move."""
        scheduler = Scheduler()
        scheduler.schedule(DueEvent("late", utc(3, 9), "briefing"))
        scheduler.schedule(DueEvent("early", utc(3, 7), "briefing"))

        expected = scheduler.rng_for("late").random()
        scheduler.cancel("early")
        self.assertEqual(scheduler.rng_for("late").random(), expected)

    def test_a_replay_after_a_save_draws_the_same_numbers(self) -> None:
        scheduler = Scheduler()
        scheduler.schedule(DueEvent("briefing", utc(3), "briefing"))
        before = scheduler.rng_for("briefing").random()

        restored = Scheduler.from_dict(scheduler.to_dict())

        self.assertEqual(restored.seed, scheduler.seed)
        self.assertEqual(restored.rng_for("briefing").random(), before)

    def test_changing_the_seed_changes_the_numbers(self) -> None:
        scheduler = Scheduler()
        default = scheduler.rng_for("briefing").random()
        scheduler.seed = 7
        self.assertNotEqual(scheduler.rng_for("briefing").random(), default)

    def test_the_derivation_is_stable_across_processes(self) -> None:
        """``hash()`` is salted per interpreter; this derivation must not be.

        Recomputing it here with ``sha256`` is the point: an implementation using ``hash()`` would
        still agree with itself inside one process, but not with this independent derivation.
        """
        scheduler = Scheduler(seed=0)
        expected = random.Random(int.from_bytes(hashlib.sha256(b"x").digest()[:8], "big")).random()
        self.assertEqual(scheduler.rng_for("x").random(), expected)

    def test_two_generators_for_one_event_are_independent_objects(self) -> None:
        scheduler = Scheduler()
        a, b = scheduler.rng_for("x"), scheduler.rng_for("x")
        self.assertEqual(a.random(), b.random())
        a.random()
        self.assertNotEqual(a.random(), b.random())


if __name__ == "__main__":
    unittest.main()
