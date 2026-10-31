"""Mission time in the authoritative world state (#950).

The clock is the SRD's (`src/rules/cwn_mission_time.py`); the state is the MUD's
(`mud/nopunk_mud/world_state.py`). These tests pin where the two meet: time moves only through an
event, the scene index is derived rather than stored, and a save/load round-trip does not lose a
minute.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mud.nopunk_mud.world_state import EVENT_TYPES, RejectedEvent, WorldState
from src.rules.cwn_mission_time import SCENE_MINUTES


def _tick(state: WorldState, event_id: str, minutes: int | None = None) -> dict:
    event = {"id": event_id, "type": "advance_time", "actor": "clock"}
    if minutes is not None:
        event["minutes"] = minutes
    return state.apply(event)


class RegistrationTests(unittest.TestCase):
    def test_time_advance_is_a_declared_event_type(self) -> None:
        self.assertIn("advance_time", EVENT_TYPES)


class AdvanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = WorldState.helsinki_opening()

    def test_a_new_world_starts_at_minute_zero(self) -> None:
        self.assertEqual(self.state.clock().minute, 0)
        self.assertEqual(self.state.scene, 0)

    def test_an_event_without_minutes_costs_one_standard_action(self) -> None:
        record = _tick(self.state, "t1")
        self.assertEqual(record["changes"]["minute"], 1)
        self.assertEqual(self.state.clock().minute, 1)

    def test_crossing_the_ten_minute_mark_reports_the_scene(self) -> None:
        changes = _tick(self.state, "t2", SCENE_MINUTES)["changes"]
        self.assertEqual((changes["scene"], changes["scenes_elapsed"]), (1, 1))

    def test_a_long_advance_reports_every_scene_it_crossed(self) -> None:
        changes = _tick(self.state, "t3", 3 * SCENE_MINUTES)["changes"]
        self.assertEqual(changes["scenes_elapsed"], 3)

    def test_time_cannot_run_backwards(self) -> None:
        _tick(self.state, "t4", 5)
        with self.assertRaises(RejectedEvent):
            _tick(self.state, "t5", -1)
        self.assertEqual(self.state.clock().minute, 5, "a rejected event must not move the clock")

    def test_the_same_event_twice_applies_once(self) -> None:
        _tick(self.state, "t6", 4)
        again = _tick(self.state, "t6", 4)
        self.assertTrue(again["duplicate"])
        self.assertEqual(self.state.clock().minute, 4)

    def test_the_scene_index_is_derived_not_stored(self) -> None:
        """Only minutes are persisted: a stored scene could disagree with the minutes."""
        self.state.apply({"id": "t7", "type": "advance_time", "minutes": 25})
        self.assertNotIn("scene", self.state.time)
        self.assertEqual(self.state.scene, 2)


class PersistenceTests(unittest.TestCase):
    def test_a_save_round_trip_keeps_the_minute(self) -> None:
        state = WorldState.helsinki_opening()
        state.apply({"id": "t8", "type": "advance_time", "minutes": 23})
        with TemporaryDirectory() as folder:
            path = Path(folder) / "world.json"
            state.save(path)
            restored = WorldState.load(path)
        self.assertEqual(restored.clock().minute, 23)
        self.assertEqual(restored.scene, state.scene)

    def test_a_snapshot_written_before_the_field_existed_still_loads(self) -> None:
        """An older save has no `time` key. That means minute zero, not a broken world."""
        with TemporaryDirectory() as folder:
            path = Path(folder) / "world.json"
            path.write_text(json.dumps({"schema_version": 1, "rooms": {}, "characters": {},
                                        "items": {}, "factions": {}, "applied": [],
                                        "log": []}), encoding="utf-8")
            restored = WorldState.load(path)
        self.assertEqual(restored.clock().minute, 0)


class ExistingBehaviourTests(unittest.TestCase):
    def test_the_clock_does_not_disturb_the_other_events(self) -> None:
        state = WorldState.helsinki_opening()
        state.apply({"id": "j1", "type": "join", "character": "ai", "room": "street"})
        state.apply({"id": "m1", "type": "move", "character": "ai", "direction": "east"})
        state.apply({"id": "t9", "type": "advance_time"})
        self.assertEqual(state.room_of("ai"), "safehouse")
        self.assertEqual(state.clock().minute, 1)


if __name__ == "__main__":
    unittest.main()
