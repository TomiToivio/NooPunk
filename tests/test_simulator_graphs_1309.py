"""#1309: the three Simulator graph views, validated together.

The tests follow the issue's own increments: social first (mutual versus one-sided ties, tags, stable ids,
serialization), ideology next (actor–concept–position, the DNA bridge, and no claim that co-occurrence is a tie), then the
physical city graph (place kinds, routes, no invented coordinates), and finally all three loaded as one world with stable
ids and a headless round trip.

Fixtures are the small labelled synthetic files in `NooPunk-Simulator/Graphs/fixtures/`. The author's `Paper/` drafts are
read for their conventions and never modified.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from social_sim.graphs import (  # noqa: E402
    Concept,
    GraphError,
    IdeologyGraph,
    PhysicalGraph,
    Place,
    Route,
    SocialGraph,
    SocialNode,
    SocialTie,
    Stance,
    World,
    load_world,
    shared_id,
)

FIXTURES = ROOT / "NooPunk-Simulator" / "Graphs" / "fixtures"


def social() -> SocialGraph:
    return SocialGraph(
        nodes={
            "person_a": SocialNode("person_a", "A", "person", ("witness",)),
            "person_b": SocialNode("person_b", "B", "person"),
            "organization_c": SocialNode("organization_c", "C", "organization"),
        },
        ties=[
            SocialTie("person_a", "person_b", 2, "friend", reciprocal=True),
            SocialTie("person_b", "person_a", 2, "friend", reciprocal=True),
            SocialTie("person_a", "organization_c", -4, "opinion", reciprocal=False),
        ],
    )


class SocialGraphTests(unittest.TestCase):
    def test_a_mutual_tie_must_have_its_mirror(self):
        with self.assertRaises(GraphError):
            SocialGraph(nodes={"person_a": SocialNode("person_a", "A"),
                               "person_b": SocialNode("person_b", "B")},
                        ties=[SocialTie("person_a", "person_b", 2, "friend", reciprocal=True)])

    def test_a_one_sided_tie_must_not_have_its_mirror(self):
        with self.assertRaises(GraphError):
            SocialGraph(nodes={"person_a": SocialNode("person_a", "A"),
                               "person_b": SocialNode("person_b", "B")},
                        ties=[SocialTie("person_a", "person_b", 2, "friend", reciprocal=False),
                              SocialTie("person_b", "person_a", 2, "friend", reciprocal=False)])

    def test_the_value_scale_is_the_authors_minus_four_to_four(self):
        for bad in (-5, 5):
            with self.assertRaises(GraphError):
                SocialTie("person_a", "person_b", bad)
        self.assertEqual((SocialTie("person_a", "person_b", -4).value,
                          SocialTie("person_a", "person_b", 4).value), (-4, 4))

    def test_mutual_and_one_sided_ties_are_reported_separately(self):
        graph = social()
        self.assertEqual(len(graph.mutual()), 1)
        self.assertEqual(len(graph.one_sided()), 1)
        self.assertEqual(graph.one_sided()[0].source, "person_a")

    def test_a_tie_must_join_known_actors_and_not_itself(self):
        with self.assertRaises(GraphError):
            SocialGraph(nodes={"person_a": SocialNode("person_a", "A")},
                        ties=[SocialTie("person_a", "person_z", 1)])
        with self.assertRaises(GraphError):
            SocialTie("person_a", "person_a", 1)

    def test_tags_and_provenance_survive_serialization(self):
        graph = social()
        payload = graph.to_dict()
        self.assertEqual(payload["format"], "noopunk.simulator.social")
        node = next(n for n in payload["nodes"] if n["id"] == "person_a")
        self.assertIn("witness", node["tags"])
        self.assertEqual(node["provenance"]["origin"], "synthesized")


class IdentifierTests(unittest.TestCase):
    def test_paper_ids_map_to_the_shared_contract_without_being_rewritten(self):
        self.assertEqual(shared_id("person_mars_eldrich", kind="person"), "social.person_mars_eldrich")
        self.assertEqual(shared_id("location_europol_field_office", kind="location"),
                         "loc.location_europol_field_office")
        self.assertEqual(shared_id("social.person_mars_eldrich", kind="person"), "social.person_mars_eldrich")

    def test_a_bare_id_needs_to_know_what_it_is(self):
        with self.assertRaises(GraphError):
            shared_id("mars_eldrich")

    def test_the_fixtures_use_the_authors_underscore_convention(self):
        nodes = json.loads((FIXTURES / "social_graph_1309.json").read_text(encoding="utf-8"))["nodes"]
        self.assertTrue(all("_" in node["id"] and "." not in node["id"] for node in nodes))


class IdeologyTests(unittest.TestCase):
    def ideology(self) -> IdeologyGraph:
        concepts = {"signifier_x": Concept("signifier_x", "X"), "demand_y": Concept("demand_y", "Y", "demand")}
        stances = [
            Stance("person_a", "signifier_x", "support", "s1"),
            Stance("person_a", "demand_y", "oppose", "s2"),
            Stance("person_b", "signifier_x", "support", "s3"),
            Stance("person_b", "demand_y", "support", "s4"),
            Stance("organization_c", "signifier_x", "unknown", "s5"),
        ]
        return IdeologyGraph(concepts=concepts, stances=stances, actor_ids=frozenset({"person_a", "person_b", "organization_c"}))

    def test_the_table_is_actor_to_concept_to_position(self):
        table = self.ideology().table()
        self.assertEqual(table["person_a"], {"signifier_x": "support", "demand_y": "oppose"})

    def test_agreement_counts_only_shared_coded_concepts(self):
        graph = self.ideology()
        self.assertEqual(graph.agreement("person_a", "person_b"), 0.5)

    def test_unknown_is_absence_not_agreement(self):
        graph = self.ideology()
        with self.assertRaises(GraphError):
            graph.agreement("person_a", "organization_c")

    def test_conflict_needs_a_patient_of_opposed_stances(self):
        graph = self.ideology()
        self.assertEqual(graph.conflicts(threshold=1), (("person_a", "person_b"),))
        self.assertEqual(graph.conflicts(threshold=2), ())

    def test_a_stance_must_belong_to_a_social_actor_and_a_known_concept(self):
        concepts = {"signifier_x": Concept("signifier_x", "X")}
        with self.assertRaises(GraphError):
            IdeologyGraph(concepts=concepts, stances=[Stance("person_z", "signifier_x", "support", "s1")],
                          actor_ids=frozenset({"person_a"}))
        with self.assertRaises(GraphError):
            IdeologyGraph(concepts=concepts, stances=[Stance("person_a", "signifier_missing", "support", "s1")],
                          actor_ids=frozenset({"person_a"}))

    def test_a_stance_must_name_its_statement(self):
        with self.assertRaises(GraphError):
            Stance("person_a", "signifier_x", "support", "")

    def test_an_unknown_position_is_refused(self):
        with self.assertRaises(GraphError):
            Stance("person_a", "signifier_x", "enthusiastic", "s1")


class PhysicalTests(unittest.TestCase):
    def physical(self) -> PhysicalGraph:
        return PhysicalGraph(
            places={
                "location_home": Place("location_home", "Home", "active"),
                "location_square": Place("location_square", "Square", "passive"),
                "location_office": Place("location_office", "Office", "graph", graph_ref="location_office_interior"),
                "location_office_interior": Place("location_office_interior", "Office interior", "active"),
            },
            routes=[
                Route("location_home", "location_square", "tram"),
                Route("location_square", "location_office", "street"),
            ],
        )

    def test_the_three_node_kinds_are_the_authors(self):
        with self.assertRaises(GraphError):
            Place("location_x", "X", "boss-room")

    def test_a_graph_node_must_name_the_graph_it_opens(self):
        with self.assertRaises(GraphError):
            Place("location_office", "Office", "graph")

    def test_routes_must_join_known_places(self):
        with self.assertRaises(GraphError):
            PhysicalGraph(places={"location_home": Place("location_home", "Home")},
                          routes=[Route("location_home", "location_elsewhere", "street")])

    def test_reachability_respects_one_way_routes(self):
        graph = PhysicalGraph(
            places={"location_a": Place("location_a", "A"), "location_b": Place("location_b", "B")},
            routes=[Route("location_a", "location_b", "street", directed=True)],
        )
        self.assertIn("location_b", graph.reachable_from("location_a"))
        self.assertEqual(graph.reachable_from("location_b"), ("location_b",),
                         "a one-way route must not be walkable backwards")

    def test_a_blocked_route_is_not_traversable(self):
        graph = PhysicalGraph(
            places={"location_a": Place("location_a", "A"), "location_b": Place("location_b", "B")},
            routes=[Route("location_a", "location_b", "street", traversable=False)],
        )
        self.assertEqual(graph.reachable_from("location_a"), ("location_a",))

    def test_coordinates_are_optional_and_never_invented(self):
        for place in load_world(FIXTURES).physical.places.values():
            self.assertIsNone(place.coordinates, f"{place.id} should not carry invented coordinates")

    def test_a_city_graph_without_routes_is_refused(self):
        with self.assertRaises(GraphError):
            PhysicalGraph(places={"location_home": Place("location_home", "Home")}, routes=[])


class WorldTests(unittest.TestCase):
    def test_the_fixtures_load_as_one_world(self):
        world = load_world(FIXTURES)
        counts = world.cross_reference()
        self.assertEqual(counts["actors"], 6)
        self.assertEqual(counts["concepts"], 3)
        self.assertEqual(counts["stances"], 6)
        self.assertEqual(counts["routes"], 3)

    def test_ids_are_stable_across_a_json_round_trip(self):
        world = load_world(FIXTURES)
        restored = World.from_dict(json.loads(json.dumps(world.to_dict())))
        self.assertEqual(restored.to_dict(), world.to_dict())
        self.assertEqual(restored.cross_reference(), world.cross_reference())

    def test_ideology_cannot_name_an_actor_the_social_graph_lacks(self):
        world = load_world(FIXTURES)
        payload = world.to_dict()
        payload["ideology"]["stances"][0]["actor"] = "person_ghost"
        with self.assertRaises(GraphError):
            World.from_dict(payload)

    def test_the_ideology_graph_creates_no_social_ties(self):
        """The DNA bridge is a projection: agreement never becomes a friendship."""
        world = load_world(FIXTURES)
        before = len(world.social.ties)
        world.ideology.conflicts()
        world.ideology.table()
        self.assertEqual(len(world.social.ties), before)

    def test_a_world_document_needs_its_format(self):
        with self.assertRaises(GraphError):
            World.from_dict({"social": {}, "ideology": {}, "physical": {}})

    def test_the_three_fixtures_are_small_and_labelled(self):
        for name in ("social_graph_1309.json", "ideology_graph_1309.json", "physical_graph_1309.json"):
            payload = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
            self.assertIn("note", payload, f"{name} must say what it is")
            self.assertIn("synthetic", payload["note"].lower() + payload.get("format", ""), name)


if __name__ == "__main__":
    unittest.main()
