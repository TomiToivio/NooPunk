"""#1217: first day reuses one WorldSession and survives a save/load boundary."""
from __future__ import annotations

import unittest

from src.console.first_day import (
    ACTOR, DISPATCH_LINE, HOME, KIT, LINKED, OFFICE, ROUTE,
    FirstDayError, available_first_day_actions, create_first_day, first_day_action,
)
from src.console.world_session import WorldSession, WorldSessionError


def prepare_kit(session: WorldSession) -> None:
    first_day_action(session, "wake")
    first_day_action(session, "uniform")
    for item in KIT:
        first_day_action(session, "inspect:" + item)
    for item in LINKED:
        first_day_action(session, "connect:" + item)


class FirstDayTests(unittest.TestCase):
    def test_fixed_identity_and_nightmare_are_not_an_extra_character_generator(self):
        session = create_first_day()
        self.assertEqual(session.identity(ACTOR)["sheet"], "sheet.tony.german")
        self.assertEqual(session.where(ACTOR), HOME)
        self.assertEqual(session.scene_id, "scene.nightmare")
        self.assertEqual(available_first_day_actions(session), ("wake",))
        with self.assertRaises(FirstDayError):
            first_day_action(session, "dispatch")
        first_day_action(session, "wake")
        self.assertEqual(session.scene_id, "scene.morning")

    def test_dispatch_requires_uniform_inspection_and_links(self):
        session = create_first_day()
        first_day_action(session, "wake")
        for item in KIT:
            first_day_action(session, "inspect:" + item)
        for item in LINKED:
            first_day_action(session, "connect:" + item)
        self.assertNotIn("dispatch", available_first_day_actions(session))
        first_day_action(session, "uniform")
        self.assertIn("dispatch", available_first_day_actions(session))
        self.assertEqual(first_day_action(session, "dispatch"), DISPATCH_LINE)
        with self.assertRaises(FirstDayError):
            first_day_action(session, "dispatch")

    def test_route_reporting_no_combat_and_no_softlock(self):
        session = create_first_day()
        prepare_kit(session)
        first_day_action(session, "dispatch")
        self.assertIn("Adlerwerke", first_day_action(session, "ride"))
        self.assertEqual(session.where(ACTOR), ROUTE)
        self.assertEqual(session.scene_id, "scene.commute")
        first_day_action(session, "arrive")
        self.assertEqual(session.where(ACTOR), OFFICE)
        self.assertEqual(session.scene_id, "scene.reporting")
        self.assertIn("Romppainen", first_day_action(session, "report"))
        self.assertEqual(available_first_day_actions(session), ())
        self.assertEqual(session.identity(ACTOR)["physical"], OFFICE)

    def test_snapshot_preserves_positions_equipment_and_actor_identity(self):
        session = create_first_day()
        prepare_kit(session)
        session = WorldSession.from_snapshot(session.to_snapshot())
        self.assertEqual(session.identity(ACTOR)["sheet"], "sheet.tony.german")
        first_day_action(session, "dispatch")
        first_day_action(session, "ride")
        restored = WorldSession.from_snapshot(session.to_snapshot())
        self.assertEqual(restored.to_snapshot(), session.to_snapshot())
        first_day_action(restored, "arrive")
        first_day_action(restored, "report")
        self.assertEqual(restored.where(ACTOR), OFFICE)

    def test_bad_save_rejected_not_silently_normalized(self):
        save = create_first_day().to_snapshot()
        save["version"] = 999
        with self.assertRaises(WorldSessionError):
            WorldSession.from_snapshot(save)
        save = create_first_day().to_snapshot()
        save["sheets"]["extra.actor"] = "sheet.tony.german"
        with self.assertRaises(WorldSessionError):
            WorldSession.from_snapshot(save)
        save = create_first_day().to_snapshot()
        save["scene_id"] = "scene.not_authored"
        with self.assertRaises(WorldSessionError):
            WorldSession.from_snapshot(save)

    def test_no_preemptive_lifepath_or_psi_grants(self):
        session = create_first_day()
        self.assertFalse(session.flags)
        self.assertFalse(hasattr(session, "roll"))
        self.assertFalse(hasattr(session, "choose_psionics"))
        self.assertNotIn("report", available_first_day_actions(session))


if __name__ == "__main__":
    unittest.main()
