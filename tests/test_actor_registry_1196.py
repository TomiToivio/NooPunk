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

if __name__ == "__main__":
    unittest.main()
