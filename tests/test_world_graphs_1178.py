"""Acceptance tests for the four current world graphs (#1178)."""

import unittest

from src.world.graphs import (
    CyberGraph,
    DeviceNode,
    GraphError,
    LocationNode,
    NetworkLink,
    PhysicalGraph,
    PhysicalRoute,
    Relationship,
    SocialGraph,
    SocialNode,
    StoryGraph,
    StoryLink,
    StoryNode,
    WorldGraphs,
)


class PhysicalGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = PhysicalGraph(
            nodes={
                "loc.home": LocationNode("loc.home", "Kurvi home", "room"),
                "loc.office": LocationNode("loc.office", "Europol office", "room"),
                "loc.corridor": LocationNode("loc.corridor", "Corridor", "room"),
            },
            routes=(
                PhysicalRoute("loc.home", "loc.corridor", directed=True),
                PhysicalRoute("loc.corridor", "loc.office", directed=True),
                PhysicalRoute("loc.office", "loc.home", directed=True),
            ),
        )
        self.graph.enter("pc.rookie", "loc.home")
        self.graph.enter("npc.falk", "loc.home")

    def test_characters_meet_only_when_they_occupy_the_same_location(self):
        self.assertTrue(self.graph.co_located("pc.rookie", "npc.falk"))
        self.assertEqual(self.graph.occupants_at("loc.home"), ("npc.falk", "pc.rookie"))
        self.graph.move("npc.falk", "loc.corridor")
        self.assertFalse(self.graph.co_located("pc.rookie", "npc.falk"))

    def test_movement_follows_one_route_and_cannot_teleport(self):
        with self.assertRaises(GraphError):
            self.graph.move("pc.rookie", "loc.office")  # not adjacent from home
        self.graph.move("pc.rookie", "loc.corridor")
        self.assertEqual(self.graph.at("pc.rookie"), "loc.corridor")
        self.graph.move("pc.rookie", "loc.office")
        self.assertEqual(self.graph.at("pc.rookie"), "loc.office")
        with self.assertRaises(GraphError):
            self.graph.move("pc.rookie", "loc.corridor")  # office -> home is one-way

    def test_directed_route_is_one_way(self):
        self.assertIn("loc.corridor", self.graph.adjacent("loc.home"))
        self.assertNotIn("loc.home", self.graph.adjacent("loc.corridor"))

    def test_roundtrip_preserves_nodes_routes_and_occupancy(self):
        restored = PhysicalGraph.from_dict(self.graph.to_dict())
        self.assertEqual(restored.to_dict(), self.graph.to_dict())


class CyberGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = CyberGraph(
            nodes={
                "cyber.camera": DeviceNode(
                    "cyber.camera",
                    "Corridor camera",
                    "camera",
                    "loc.corridor",
                    ("observe", "record"),
                ),
                "cyber.door": DeviceNode(
                    "cyber.door",
                    "Door controller",
                    "controller",
                    "loc.corridor",
                    ("unlock", "lock"),
                ),
                "cyber.server": DeviceNode(
                    "cyber.server", "Evidence server", "server", "", ("query", "copy")
                ),
            },
            links=(
                NetworkLink("cyber.camera", "cyber.server"),
                NetworkLink("cyber.door", "cyber.server"),
            ),
        )

    def test_devices_at_a_physical_location_are_the_same_devices_an_avatar_visits(self):
        self.assertEqual(
            self.graph.devices_at("loc.corridor"), ("cyber.camera", "cyber.door")
        )
        self.graph.enter("pc.rookie", "cyber.camera")
        self.assertEqual(self.graph.actions_at("pc.rookie"), ("observe", "record"))

    def test_avatar_moves_through_network_edges_without_moving_the_body(self):
        self.graph.enter("pc.rookie", "cyber.camera")
        self.graph.move_avatar("pc.rookie", "cyber.server")
        self.assertEqual(self.graph.at("pc.rookie"), "cyber.server")
        # The graph has no physical body position; that remains the PhysicalGraph's fact.
        with self.assertRaises(GraphError):
            self.graph.leave("npc.absent")

    def test_avatar_cannot_teleport(self):
        self.graph.enter("pc.rookie", "cyber.camera")
        with self.assertRaises(GraphError):
            self.graph.move_avatar("pc.rookie", "cyber.door")

    def test_roundtrip(self):
        self.graph.enter("pc.rookie", "cyber.camera")
        restored = CyberGraph.from_dict(self.graph.to_dict())
        self.assertEqual(restored.to_dict(), self.graph.to_dict())


class SocialGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = SocialGraph(
            nodes={
                "pc.rookie": SocialNode("pc.rookie", "Rookie", "character"),
                "npc.falk": SocialNode("npc.falk", "Laura Falk", "character"),
                "faction.europol": SocialNode("faction.europol", "Europol", "faction"),
            },
            relationships=(
                Relationship("pc.rookie", "npc.falk", 2, "colleague", "first case"),
                Relationship("pc.rookie", "faction.europol", -1, "employer"),
            ),
        )

    def test_nodes_are_characters_or_factions_and_scores_are_signed(self):
        self.assertEqual(self.graph.score("pc.rookie", "npc.falk"), 2)
        self.assertEqual(self.graph.score("pc.rookie", "faction.europol"), -1)
        self.assertIsNone(self.graph.score("npc.falk", "pc.rookie"))

    def test_relationships_are_directed_and_replaceable(self):
        self.graph.set_relationship("npc.falk", "pc.rookie", 3, kind="trust")
        self.assertEqual(self.graph.score("npc.falk", "pc.rookie"), 3)
        self.assertEqual(self.graph.score("pc.rookie", "npc.falk"), 2)
        with self.assertRaises(GraphError):
            self.graph.set_relationship("pc.rookie", "npc.falk", 5)

    def test_social_nodes_are_not_spatial_routes(self):
        self.assertFalse(hasattr(self.graph, "move"))

    def test_roundtrip(self):
        restored = SocialGraph.from_dict(self.graph.to_dict())
        self.assertEqual(restored.to_dict(), self.graph.to_dict())


class StoryGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = StoryGraph(
            nodes={
                "series.first": StoryNode("series.first", "First series", "series"),
                "episode.one": StoryNode(
                    "episode.one", "First case", "episode", "series.first"
                ),
                "scene.briefing": StoryNode(
                    "scene.briefing",
                    "Briefing",
                    "scene",
                    "episode.one",
                    ("social",),
                    ("goal.case",),
                ),
                "scene.raid": StoryNode(
                    "scene.raid",
                    "Raid",
                    "scene",
                    "episode.one",
                    ("investigation", "Action"),
                    (),
                    ("flag.warrant",),
                ),
                "episode.two": StoryNode(
                    "episode.two",
                    "Second case",
                    "episode",
                    "series.first",
                    (),
                    (),
                    ("flag.case_closed",),
                ),
            },
            links=(
                StoryLink("series.first", "episode.one"),
                StoryLink("episode.one", "scene.briefing"),
                StoryLink("scene.briefing", "scene.raid", condition="flag.warrant"),
                StoryLink("episode.one", "episode.two", condition="flag.case_closed"),
            ),
        )

    def test_hierarchy_is_series_episode_scene(self):
        self.assertEqual(
            self.graph.children("series.first"), ("episode.one", "episode.two")
        )
        self.assertEqual(
            self.graph.children("episode.one"), ("scene.briefing", "scene.raid")
        )

    def test_scene_entry_respects_prerequisites_and_transition_condition(self):
        self.assertTrue(self.graph.can_enter("scene.briefing", completed={"goal.case"}))
        self.assertFalse(self.graph.can_enter("scene.raid"))
        self.assertFalse(self.graph.advance("scene.briefing", "scene.raid"))
        self.assertTrue(
            self.graph.advance("scene.briefing", "scene.raid", flags={"flag.warrant"})
        )

    def test_episode_transition_requires_its_flag(self):
        self.assertFalse(self.graph.advance("episode.one", "episode.two"))
        self.assertTrue(
            self.graph.advance("episode.one", "episode.two", flags={"flag.case_closed"})
        )

    def test_roundtrip(self):
        restored = StoryGraph.from_dict(self.graph.to_dict())
        self.assertEqual(restored.to_dict(), self.graph.to_dict())


class WorldGraphsTest(unittest.TestCase):
    def test_cross_graph_bundle_roundtrips(self):
        bundle = WorldGraphs(
            physical=PhysicalGraph(
                nodes={"loc.office": LocationNode("loc.office", "Office")},
                routes=(),
                occupants={"pc.rookie": "loc.office"},
            ),
            cyber=CyberGraph(
                nodes={
                    "cyber.camera": DeviceNode(
                        "cyber.camera", "Camera", "camera", "loc.office"
                    )
                },
            ),
            social=SocialGraph(nodes={"pc.rookie": SocialNode("pc.rookie", "Rookie")}),
            story=StoryGraph(
                nodes={"series.first": StoryNode("series.first", "Series", "series")}
            ),
        )
        restored = WorldGraphs.from_dict(bundle.to_dict())
        self.assertEqual(restored.to_dict(), bundle.to_dict())

    def test_cyber_device_must_reference_a_real_physical_location(self):
        with self.assertRaises(GraphError):
            WorldGraphs(
                physical=PhysicalGraph(
                    nodes={"loc.office": LocationNode("loc.office", "Office")}
                ),
                cyber=CyberGraph(
                    nodes={
                        "cyber.camera": DeviceNode(
                            "cyber.camera", "Camera", physical_location="loc.missing"
                        )
                    }
                ),
                social=SocialGraph(),
                story=StoryGraph(),
            )

    def test_avatar_movement_does_not_move_the_operator_body(self):
        bundle = WorldGraphs(
            physical=PhysicalGraph(
                nodes={
                    "loc.home": LocationNode("loc.home", "Home"),
                    "loc.office": LocationNode("loc.office", "Office"),
                },
                routes=(PhysicalRoute("loc.home", "loc.office"),),
                occupants={"pc.rookie": "loc.home"},
            ),
            cyber=CyberGraph(
                nodes={
                    "cyber.camera": DeviceNode(
                        "cyber.camera", "Camera", "camera", "loc.home"
                    ),
                    "cyber.server": DeviceNode(
                        "cyber.server", "Server", "server", "loc.office"
                    ),
                },
                links=(NetworkLink("cyber.camera", "cyber.server"),),
            ),
            social=SocialGraph(nodes={"pc.rookie": SocialNode("pc.rookie", "Rookie")}),
            story=StoryGraph(
                nodes={"series.first": StoryNode("series.first", "Series", "series")}
            ),
        )
        bundle.cyber.enter("pc.rookie", "cyber.camera")
        bundle.cyber.move_avatar("pc.rookie", "cyber.server")
        self.assertEqual(bundle.physical.at("pc.rookie"), "loc.home")

    def test_social_ties_survive_physical_travel(self):
        physical = PhysicalGraph(
            nodes={
                "loc.home": LocationNode("loc.home", "Home"),
                "loc.office": LocationNode("loc.office", "Office"),
            },
            routes=(PhysicalRoute("loc.home", "loc.office"),),
            occupants={"pc.rookie": "loc.home"},
        )
        social = SocialGraph(
            nodes={
                "pc.rookie": SocialNode("pc.rookie", "Rookie"),
                "npc.falk": SocialNode("npc.falk", "Falk"),
            },
            relationships=(Relationship("pc.rookie", "npc.falk", 3),),
        )
        self.assertEqual(social.score("pc.rookie", "npc.falk"), 3)
        physical.move("pc.rookie", "loc.office")
        self.assertEqual(social.score("pc.rookie", "npc.falk"), 3)

    def test_networkx_views_are_derived_from_the_authored_dicts(self):
        try:
            import networkx  # noqa: F401
        except ImportError:
            self.skipTest("NetworkX is not installed")
        bundle = WorldGraphs(
            physical=PhysicalGraph(
                nodes={"loc.office": LocationNode("loc.office", "Office")},
                routes=(),
                occupants={"pc.rookie": "loc.office"},
            ),
            cyber=CyberGraph(
                nodes={
                    "cyber.camera": DeviceNode(
                        "cyber.camera", "Camera", "camera", "loc.office"
                    )
                },
            ),
            social=SocialGraph(nodes={"pc.rookie": SocialNode("pc.rookie", "Rookie")}),
            story=StoryGraph(
                nodes={"series.first": StoryNode("series.first", "Series", "series")}
            ),
        )
        views = bundle.to_networkx()
        self.assertEqual(set(views), {"physical", "cyber", "social", "story"})
        self.assertIn("loc.office", views["physical"])
        self.assertIn("cyber.camera", views["cyber"])

    def test_astral_is_not_a_fifth_graph_in_this_slice(self):
        bundle = WorldGraphs(
            physical=PhysicalGraph(
                nodes={"loc.office": LocationNode("loc.office", "Office")}
            ),
            cyber=CyberGraph(),
            social=SocialGraph(),
            story=StoryGraph(),
        )
        self.assertNotIn("astral", bundle.to_dict())


if __name__ == "__main__":
    unittest.main()
