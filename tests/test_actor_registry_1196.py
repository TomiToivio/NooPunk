"""One actor, one sheet, many views (#1196 §6).

The bug this pins is quiet: every module keys actors by string, so an actor can be one person on the
sheet, another on the social graph and a third body in a room while the whole suite stays green.
These tests make the mapping fail loudly instead.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.world.actor_registry import (
    ActorIdentityError,
    ActorRegistry,
    CanonicalActor,
    Handle,
)
from src.world.graphs import (
    CyberGraph,
    DeviceNode,
    LocationNode,
    NetworkLink,
    PhysicalGraph,
    PhysicalRoute,
    SocialGraph,
    SocialNode,
    StoryGraph,
    StoryNode,
    WorldGraphs,
)


def graphs(occupant: str = "act.rookie", avatar: str = "av.rookie") -> WorldGraphs:
    physical = PhysicalGraph(
        {"loc.hq": LocationNode("loc.hq", "HQ"), "loc.street": LocationNode("loc.street", "Street")},
        (PhysicalRoute("loc.hq", "loc.street"),),
        {occupant: "loc.hq"},
    )
    cyber = CyberGraph(
        {
            "dev.cam": DeviceNode("dev.cam", "Lobby camera", "camera", "loc.hq", ("record",)),
            "dev.gw": DeviceNode("dev.gw", "Gateway", "host", "loc.hq", ("authenticate",)),
        },
        (NetworkLink("dev.cam", "dev.gw"),),
        {avatar: "dev.cam"},
    )
    social = SocialGraph({"act.rookie": SocialNode("act.rookie", "Rookie", "character")}, ())
    story = StoryGraph({"scene.one": StoryNode("scene.one", "Briefing", "scene")}, ())
    return WorldGraphs(physical, cyber, social, story)


def registry() -> ActorRegistry:
    book = ActorRegistry()
    book.register(
        CanonicalActor(
            "act.rookie",
            "Rookie",
            (
                Handle("physical", "act.rookie"),
                Handle("cyber", "av.rookie"),
                Handle("social", "rookie"),
                Handle("sheet", "act.rookie"),
            ),
        )
    )
    return book


class Resolution(unittest.TestCase):
    def test_one_actor_answers_to_different_handles_per_view(self) -> None:
        book = registry()
        for view, handle in (("physical", "act.rookie"), ("cyber", "av.rookie"), ("social", "rookie")):
            self.assertEqual(book.canonical(view, handle), "act.rookie")
        self.assertEqual(book.actor("act.rookie").in_view("social"), "rookie")

    def test_an_unmapped_handle_is_refused_rather_than_assumed(self) -> None:
        with self.assertRaises(ActorIdentityError) as caught:
            registry().canonical("physical", "act.someone")
        self.assertIn("physical:act.someone", str(caught.exception))


class Conflicts(unittest.TestCase):
    def test_a_handle_cannot_belong_to_two_actors(self) -> None:
        book = registry()
        rival = CanonicalActor("npc.wendt", "Wendt", (Handle("social", "rookie"),))
        with self.assertRaises(ActorIdentityError):
            book.register(rival)
        self.assertEqual(book.canonical("social", "rookie"), "act.rookie")

    def test_a_handle_cannot_be_another_actors_canonical_id(self) -> None:
        book = registry()
        clash = CanonicalActor("npc.other", "Other", (Handle("social", "act.rookie"),))
        with self.assertRaises(ActorIdentityError):
            book.register(clash)

    def test_the_same_actor_cannot_be_registered_twice(self) -> None:
        with self.assertRaises(ActorIdentityError):
            registry().register(CanonicalActor("act.rookie", "Rookie again"))


class TheSeventhCheck(unittest.TestCase):
    def test_every_graph_actor_resolves(self) -> None:
        self.assertEqual(registry().check_graphs(graphs()), [])

    def test_an_unregistered_occupant_is_reported(self) -> None:
        problems = registry().check_graphs(graphs(occupant="act.stray"))
        self.assertEqual(len(problems), 1)
        self.assertIn("act.stray", problems[0])

    def test_an_avatar_is_a_session_not_a_person(self) -> None:
        problems = registry().check_avatar_operators({"av.rookie": "act.rookie"})
        self.assertEqual(problems, [])
        book = registry()
        book.register(CanonicalActor("av.rookie", "Rookie avatar", ()))
        problems = book.check_avatar_operators({"av.rookie": "act.rookie"})
        self.assertTrue(any("session, not a person" in problem for problem in problems))

    def test_an_avatar_must_name_a_known_operator(self) -> None:
        problems = registry().check_avatar_operators({"av.rookie": "act.nobody"})
        self.assertTrue(any("unknown operator" in problem for problem in problems))

    def test_two_actors_cannot_share_one_sheet(self) -> None:
        book = registry()
        book.register(CanonicalActor("npc.wendt", "Wendt"))
        problems = book.one_sheet(
            sheets={"act.rookie": "sheet.1", "npc.wendt": "sheet.1"}
        )
        self.assertTrue(any("one actor, one sheet" in problem for problem in problems))
        self.assertEqual(book.one_sheet(sheets={"act.rookie": "sheet.1"}), [])


class Serialization(unittest.TestCase):
    def test_roundtrip_preserves_handles(self) -> None:
        book = registry()
        restored = ActorRegistry.from_dict(book.to_dict())
        self.assertEqual(restored.to_dict(), book.to_dict())
        self.assertEqual(restored.canonical("social", "rookie"), "act.rookie")

    def test_the_module_resolves_identity_only(self) -> None:
        """CWN stays the action authority: no resolution surface may appear here."""
        from src.world import actor_registry

        surface = {name for name in dir(actor_registry.ActorRegistry) if not name.startswith("_")}
        self.assertFalse(surface & {"roll", "resolve", "attack", "modifier", "damage"})
        source = Path(actor_registry.__file__).read_text(encoding="utf-8")
        self.assertNotIn("from .rules", source)
        self.assertNotIn("import rules", source)


class AgreementWithTheSession(unittest.TestCase):
    """The registry and the console session must not disagree about who owns a sheet."""

    def test_registry_and_world_session_agree_on_one_sheet(self) -> None:
        from src.console.world_session import WorldSession, WorldSessionError

        book = registry()
        session = WorldSession(graphs(), sheets={"act.rookie": "sheet.rookie"})
        self.assertEqual(book.one_sheet(sheets=session.sheets), [])
        with self.assertRaises(WorldSessionError):
            session.register("npc.wendt", "sheet.rookie")
        book.register(CanonicalActor("npc.wendt", "Wendt"))
        self.assertTrue(
            any("one actor, one sheet" in problem
                for problem in book.one_sheet(sheets={"act.rookie": "sheet.rookie",
                                                      "npc.wendt": "sheet.rookie"}))
        )

# Issue #1217: First-day flow exercises the same WorldSession actor registry.
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
