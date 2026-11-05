"""Acceptance tests for #1178: four graphs now; Astral navigation later."""
import json
import unittest

from src.rules.four_graphs import (
    FourGraphs, GraphContractError, Place, Route, SpatialGraph,
    Relationship, SocialEntity, SocialGraph,
    StoryEdge, StoryGraph, StoryNode,
)


def example() -> FourGraphs:
    physical = SpatialGraph(
        "physical", {
            "physical.kurvi": Place("physical.kurvi", "Kurvi residence"),
            "physical.office": Place("physical.office", "Europol office"),
        },
        (Route("physical.kurvi", "physical.office", "walk.kurvi.office", directed=False),),
        {"pc.tony": "physical.kurvi", "npc.laura": "physical.kurvi"},
    )
    cyber = SpatialGraph(
        "cyber", {
            "cyber.gateway": Place("cyber.gateway", "Europol gateway", kind="host",
                                   physical_ref="physical.office", device_actions=("authenticate",)),
            "cyber.camera": Place("cyber.camera", "CCTV camera", kind="camera",
                                  physical_ref="physical.office", device_actions=("record",)),
        },
        (Route("cyber.gateway", "cyber.camera", "lan.gateway.camera", directed=True, gate="cwn.access"),),
        {"avatar.tony": "cyber.gateway"},
    )
    social = SocialGraph(
        {"pc.tony": SocialEntity("pc.tony", "character", "Tony"),
         "npc.laura": SocialEntity("npc.laura", "character", "Laura"),
         "faction.europol": SocialEntity("faction.europol", "faction", "Europol")},
        (Relationship("npc.laura", "pc.tony", 2, directed=True),
         Relationship("pc.tony", "faction.europol", 0, directed=False)),
    )
    story = StoryGraph(
        {"series.europol": StoryNode("series.europol", "series", "Europol Rookie"),
         "episode.invoice": StoryNode("episode.invoice", "episode", "Invoice"),
         "scene.office": StoryNode("scene.office", "scene", "At the office",
                                   ("Investigation", "Cyber"), ("physical.office", "cyber.camera"),
                                   ("goal.invoice",)),
         "scene.followup": StoryNode("scene.followup", "scene", "Follow the lead",
                                     ("Social",), ("pc.tony",)),
        },
        (StoryEdge("series.europol", "episode.invoice", "contains"),
         StoryEdge("episode.invoice", "scene.office", "contains"),
         StoryEdge("episode.invoice", "scene.followup", "contains"),
         StoryEdge("scene.office", "scene.followup", all_flags=("clue.invoice",),
                   all_goals=("goal.invoice",))),
    )
    return FourGraphs(physical, cyber, social, story, {"avatar.tony": "pc.tony"})


class FourGraphTests(unittest.TestCase):
    def test_physical_nodes_are_places_and_actors_are_occupants(self):
        graphs = example()
        self.assertNotIn("pc.tony", graphs.physical.nodes)
        self.assertTrue(graphs.physical.co_located("pc.tony", "npc.laura"))
        self.assertEqual(graphs.physical.occupants("physical.kurvi"),
                         ("npc.laura", "pc.tony"))
        graphs.physical.move("pc.tony", "physical.office")
        self.assertFalse(graphs.physical.co_located("pc.tony", "npc.laura"))
        self.assertEqual(graphs.social.relationship("npc.laura", "pc.tony"), 2)

    def test_movement_rejects_missing_route_and_locked_gate(self):
        graphs = example()
        with self.assertRaises(GraphContractError):
            graphs.physical.move("npc.laura", "physical.unknown")
        with self.assertRaises(GraphContractError):
            graphs.cyber.move("avatar.tony", "cyber.camera")
        graphs.cyber.move("avatar.tony", "cyber.camera",
                          flags=frozenset(("cwn.access",)))
        with self.assertRaises(GraphContractError):
            graphs.cyber.move("avatar.tony", "cyber.gateway")

    def test_cyber_is_device_and_avatar_location_not_body(self):
        graphs = example()
        camera = graphs.cyber.nodes["cyber.camera"]
        self.assertEqual(camera.physical_ref, "physical.office")
        self.assertIn("record", camera.device_actions)
        graphs.move_avatar("avatar.tony", "cyber.camera",
                           flags=frozenset(("cwn.access",)))
        self.assertEqual(graphs.cyber.positions["avatar.tony"], "cyber.camera")
        self.assertEqual(graphs.physical.positions["pc.tony"], "physical.kurvi")

    def test_social_unknown_is_not_neutral_and_direction_matters(self):
        social = example().social
        self.assertIsNone(social.relationship("pc.tony", "npc.laura"))
        self.assertEqual(social.relationship("npc.laura", "pc.tony"), 2)
        self.assertEqual(social.relationship("faction.europol", "pc.tony"), 0)
        with self.assertRaises(GraphContractError):
            Relationship("pc.tony", "npc.laura", 5)
        with self.assertRaises(GraphContractError):
            Relationship("pc.tony", "npc.laura", True)

    def test_story_goals_flags_and_containment(self):
        story = example().story
        self.assertEqual(story.children("series.europol"), ("episode.invoice",))
        self.assertEqual(story.available("scene.office"), ())
        self.assertEqual(story.available("scene.office",
                                         flags=frozenset(("clue.invoice",))), ())
        self.assertEqual(story.available("scene.office",
                                         flags=frozenset(("clue.invoice",)),
                                         completed_goals=frozenset(("goal.invoice",))),
                         ("scene.followup",))

    def test_roundtrip_json_replay(self):
        state = example()
        self.assertEqual(FourGraphs.from_json(state.to_json()).to_dict(), state.to_dict())
        state.move_avatar("avatar.tony", "cyber.camera", flags=frozenset(("cwn.access",)))
        restored = FourGraphs.from_json(state.to_json())
        self.assertEqual(restored.cyber.positions["avatar.tony"], "cyber.camera")
        self.assertEqual(restored.physical.positions["pc.tony"], "physical.kurvi")
        self.assertNotIn("astral", restored.to_dict())

    def test_bad_records_are_rejected(self):
        with self.assertRaises(GraphContractError):
            SpatialGraph("physical", {"pc.tony": Place("pc.tony", "Not a place")},
                         (), {"pc.tony": "pc.tony"})
        with self.assertRaises(GraphContractError):
            SpatialGraph("physical", {"p": Place("p", "Place")},
                         (Route("p", "missing", "bad"),))
        with self.assertRaises(GraphContractError):
            SocialGraph({"a": SocialEntity("a", "character", "A")},
                        (Relationship("a", "missing", 0),))
        with self.assertRaises(GraphContractError):
            FourGraphs.from_dict({"format": "noopunk.four_graphs", "version": 1,
                                  "physical": {"graph_type": "astral", "version": 1,
                                               "nodes": [], "edges": []}})
        with self.assertRaises(GraphContractError):
            StoryGraph({"s": StoryNode("s", "series", "S"),
                        "x": StoryNode("x", "scene", "X")},
                       (StoryEdge("s", "x", "contains"),))
        with self.assertRaises(GraphContractError):
            FourGraphs(example().physical,
                       SpatialGraph("cyber", {"bad": Place("bad", "Bad", "camera",
                                                          physical_ref="physical.unknown")},
                                    ()), example().social, example().story)

    def test_optional_networkx_is_only_a_projection(self):
        try:
            import networkx  # noqa: F401
        except ImportError:
            self.skipTest("optional networkx unavailable")
        from src.rules.four_graphs import networkx_view
        state = example()
        p = networkx_view(state.physical)
        self.assertEqual(set(p.nodes), {"physical.kurvi", "physical.office"})
        self.assertEqual(p.nodes["physical.kurvi"]["occupants"], ("npc.laura", "pc.tony"))
        self.assertNotIn("pc.tony", p.nodes)


if __name__ == "__main__":
    unittest.main()
