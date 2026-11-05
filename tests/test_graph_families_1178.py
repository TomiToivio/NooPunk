"""Tests for the four graph families (#1178).

These are code tests: they exercise `src/world/graphs.py` behaviour, not document text, per AGENTS.md §1.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from noopunk_graphs import (  # noqa: E402
    Edge,
    Family,
    Graph,
    GraphError,
    Node,
    World,
    physical_from_helsinki,
)


def physical() -> Graph:
    graph = Graph(Family.PHYSICAL)
    graph.add_node(Node("city_helsinki", Family.PHYSICAL, "city", label="Helsinki"))
    graph.add_node(Node("kurvi_flat", Family.PHYSICAL, "room", label="Kurvi flat", parent_id="city_helsinki"))
    graph.add_node(Node("street", Family.PHYSICAL, "location", label="Kurvi street", parent_id="city_helsinki"))
    graph.add_node(Node("hq", Family.PHYSICAL, "location", label="Europol HQ", parent_id="city_helsinki"))
    graph.add_edge(Edge("door_home", Family.PHYSICAL, "kurvi_flat", "street", relation="door"))
    graph.add_edge(Edge("route_street_hq", Family.PHYSICAL, "street", "hq", relation="route", travel_cost="scene"))
    return graph


def cyber() -> Graph:
    graph = Graph(Family.CYBER)
    graph.add_node(Node("hq_terminal", Family.CYBER, "device", label="HQ terminal", location_ref="hq"))
    graph.add_node(Node("case_service", Family.CYBER, "service", label="Case service"))
    graph.add_edge(Edge("link_terminal_case", Family.CYBER, "hq_terminal", "case_service", relation="link"))
    return graph


class PhysicalFamilyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = World([physical(), cyber()])

    def test_characters_occupy_places_and_are_never_places(self) -> None:
        graph = self.world.graph(Family.PHYSICAL)
        kinds = {node.kind for node in graph.nodes}
        self.assertNotIn("character", kinds)
        self.assertNotIn("agent", kinds)
        with self.assertRaises(GraphError):
            graph.add_node(Node("rookie", Family.PHYSICAL, "character"))

    def test_two_characters_meet_only_in_the_same_node(self) -> None:
        self.world.place("rookie", "kurvi_flat")
        self.world.place("partner", "kurvi_flat")
        self.assertTrue(self.world.co_located("rookie", "partner"))

        self.world.move("rookie", "street")
        self.assertFalse(self.world.co_located("rookie", "partner"))
        self.assertEqual(self.world.occupants("street"), ("rookie",))

    def test_movement_requires_an_edge(self) -> None:
        self.world.place("rookie", "kurvi_flat")
        with self.assertRaises(GraphError):
            self.world.move("rookie", "hq")          # no edge flat → hq
        self.assertEqual(self.world.move("rookie", "street"), "street")
        self.assertEqual(self.world.move("rookie", "hq"), "hq")

    def test_a_location_cannot_be_an_occupant(self) -> None:
        with self.assertRaises(GraphError):
            self.world.place("kurvi_flat", "street")

    def test_unknown_node_is_refused(self) -> None:
        with self.assertRaises(GraphError):
            self.world.place("rookie", "atlantis")


class CyberFamilyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = World([physical(), cyber()])
        self.world.place("rookie", "hq")
        self.world.place("rookie", "hq_terminal")          # the avatar

    def test_a_device_is_a_place_and_an_actor(self) -> None:
        node = self.world.graph(Family.CYBER).node("hq_terminal")
        self.assertEqual(node.kind, "device")
        self.assertEqual(node.location_ref, "hq")
        self.assertTrue(node.is_place)

    def test_the_camera_is_a_cyber_node_with_a_physical_location(self) -> None:
        self.assertEqual(self.world.graph(Family.CYBER).node("hq_terminal").location_ref, "hq")

    def test_avatar_movement_does_not_move_the_body(self) -> None:
        self.world.move("rookie", "case_service", Family.CYBER)
        self.assertEqual(self.world.at("rookie", Family.CYBER), "case_service")
        self.assertEqual(self.world.at("rookie", Family.PHYSICAL), "hq")

    def test_a_cyber_node_may_not_reference_another_cyber_node(self) -> None:
        graph = Graph(Family.CYBER)
        graph.add_node(Node("a", Family.CYBER, "device"))
        graph.add_node(Node("b", Family.CYBER, "device", location_ref="a"))
        with self.assertRaises(GraphError):
            graph.validate()


class SocialFamilyTests(unittest.TestCase):
    def test_characters_are_nodes_and_scores_are_signed(self) -> None:
        graph = Graph(Family.SOCIAL)
        graph.add_node(Node("rookie", Family.SOCIAL, "character"))
        graph.add_node(Node("europol", Family.SOCIAL, "faction"))
        graph.add_edge(Edge("rep_rookie_europol", Family.SOCIAL, "rookie", "europol", relation="relationship",
                            relationship=2))
        self.assertEqual(graph.node("rookie").kind, "character")

    def test_relationship_bounds_and_no_travel(self) -> None:
        with self.assertRaises(GraphError):
            Edge("bad", Family.SOCIAL, "a", "b", relationship=5)
        with self.assertRaises(GraphError):
            Edge("bad", Family.SOCIAL, "a", "b", relationship=1, travel_cost="scene")
        with self.assertRaises(GraphError):
            Edge("bad", Family.SOCIAL, "a", "b", relationship=None)

    def test_social_links_never_move_anyone(self) -> None:
        social = Graph(Family.SOCIAL)
        social.add_node(Node("rookie", Family.SOCIAL, "character"))
        social.add_node(Node("maki", Family.SOCIAL, "character"))
        social.add_edge(Edge("tie", Family.SOCIAL, "rookie", "maki", relation="relationship", relationship=-1))
        world = World([physical(), social])
        with self.assertRaises(GraphError):
            world.move("rookie", "maki", Family.SOCIAL)

    def test_a_character_cannot_be_placed_at_a_social_node(self) -> None:
        social = Graph(Family.SOCIAL)
        social.add_node(Node("rookie", Family.SOCIAL, "character"))
        world = World([physical(), social])
        with self.assertRaises(GraphError):
            world.place("rookie", "rookie")

    def test_social_tie_persists_across_physical_travel(self) -> None:
        social = Graph(Family.SOCIAL)
        social.add_node(Node("rookie", Family.SOCIAL, "character"))
        social.add_node(Node("maki", Family.SOCIAL, "character"))
        social.add_edge(Edge("tie", Family.SOCIAL, "rookie", "maki", relation="relationship", relationship=3))
        world = World([physical(), social])
        world.place("rookie", "kurvi_flat")
        world.move("rookie", "street")
        world.move("rookie", "hq")
        self.assertEqual(world.at("rookie"), "hq")
        tie = world.graph(Family.SOCIAL).edge_between("rookie", "maki")
        self.assertIsNotNone(tie)
        self.assertEqual(tie.relationship, 3)


class StoryFamilyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.story = Graph(Family.STORY)
        self.story.add_node(Node("campaign01", Family.STORY, "series", label="Campaign 01"))
        self.story.add_node(Node(
            "ep01", Family.STORY, "episode", parent_id="campaign01",
            metadata={"required_scenes": ["sc_briefing", "sc_interview"]},
        ))
        self.story.add_node(Node("sc_briefing", Family.STORY, "scene"))
        self.story.add_node(Node("sc_interview", Family.STORY, "scene"))
        self.story.add_node(Node("sc_depot", Family.STORY, "scene"))
        self.story.add_edge(Edge("entry_ep01", Family.STORY, "ep01", "sc_briefing", relation="entry"))
        self.story.add_edge(Edge("seq_briefing_interview", Family.STORY, "sc_briefing", "sc_interview",
                                 relation="sequence", when="flag:briefed"))
        self.story.add_edge(Edge("seq_interview_depot", Family.STORY, "sc_interview", "sc_depot",
                                 relation="sequence", when="flag:ledger_read"))
        self.world = World([self.story])

    def test_a_transition_needs_its_flag(self) -> None:
        self.assertEqual(self.world.available_scenes("ep01", []), ("sc_briefing",))
        self.assertEqual(self.world.available_scenes("ep01", ["flag:briefed"]), ("sc_briefing",))
        self.assertEqual(self.world.available_scenes("sc_briefing", ["flag:briefed"]), ("sc_interview",))
        self.assertEqual(self.world.available_scenes("sc_briefing", []), ())

    def test_a_transition_must_name_the_flag_that_gates_it(self) -> None:
        with self.assertRaises(GraphError):
            Edge("bad", Family.STORY, "sc_depot", "sc_interview", relation="sequence")

    def test_required_scenes_exist_and_are_scenes(self) -> None:
        self.world.verify_required_scenes("ep01")
        broken = Graph(Family.STORY)
        broken.add_node(Node("ep", Family.STORY, "episode", metadata={"required_scenes": ["missing_scene"]}))
        with self.assertRaises(GraphError):
            World([broken]).verify_required_scenes("ep")

    def test_scenes_are_not_places(self) -> None:
        with self.assertRaises(GraphError):
            self.world.place("rookie", "sc_briefing")


class DeferralAndDataTests(unittest.TestCase):
    def test_the_astral_graph_is_deferred_with_a_reason(self) -> None:
        with self.assertRaises(GraphError) as caught:
            Graph(Family.ASTRAL)
        self.assertIn("deferred", str(caught.exception))
        self.assertIn("Astral Projection", str(caught.exception))

    def test_helsinki_locations_load_as_a_physical_graph(self) -> None:
        path = ROOT / "data" / "world" / "helsinki_locations.json"
        graph = physical_from_helsinki(path)
        raw = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len([n for n in graph.nodes if n.kind == "location"]), len(raw["nodes"]))
        self.assertIn(raw["start"], graph)
        self.assertTrue(graph.node(raw["start"]).metadata["start"])
        self.assertTrue(any(n.kind == "district" for n in graph.nodes))

    def test_world_round_trips_through_json(self) -> None:
        world = World([physical(), cyber()])
        world.place("rookie", "hq")
        world.place("rookie", "hq_terminal")
        restored = World.from_dict(json.loads(json.dumps(world.to_dict())))
        self.assertEqual(restored.at("rookie", Family.PHYSICAL), "hq")
        self.assertEqual(restored.at("rookie", Family.CYBER), "hq_terminal")
        self.assertEqual(len(restored.graph(Family.PHYSICAL)), len(world.graph(Family.PHYSICAL)))

    def test_duplicate_ids_are_refused(self) -> None:
        graph = physical()
        with self.assertRaises(GraphError):
            graph.add_node(Node("hq", Family.PHYSICAL, "location"))
        with self.assertRaises(GraphError):
            graph.add_edge(Edge("door_home", Family.PHYSICAL, "street", "hq"))


if __name__ == "__main__":
    unittest.main()
