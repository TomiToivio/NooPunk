"""The canonical Helsinki data loads into the #1178 physical graph.

Code tests: they exercise `src/world/helsinki.py` and `src/world/graphs.py`, not document text.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.world.graphs import GraphError, PhysicalGraph
from src.world.helsinki import HELSINKI_LOCATIONS, load_helsinki_physical, start_location

ROOT = Path(__file__).resolve().parents[1]


class HelsinkiAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = json.loads(HELSINKI_LOCATIONS.read_text(encoding="utf-8"))

    def test_every_canonical_place_is_present_with_its_id(self) -> None:
        graph = load_helsinki_physical()
        for entry in self.raw["nodes"]:
            self.assertIn(entry["id"], graph.nodes, entry["id"])
        places = [node for node in graph.nodes.values() if node.kind == "location"]
        self.assertEqual(len(places), len(self.raw["nodes"]))

    def test_districts_become_parents(self) -> None:
        graph = load_helsinki_physical()
        start = graph.nodes[start_location()]
        self.assertTrue(start.parent_id.startswith("district_"), start.parent_id)
        self.assertIn(start.parent_id, graph.nodes)
        self.assertEqual(graph.nodes[start.parent_id].kind, "district")

    def test_routes_come_from_the_caller_and_are_validated(self) -> None:
        start = start_location()
        other = next(entry["id"] for entry in self.raw["nodes"] if entry["id"] != start)
        graph = load_helsinki_physical(routes=[(start, other)])
        self.assertEqual(len(graph.routes), 1)
        self.assertTrue(graph.routes[0].source == start)
        with self.assertRaises(GraphError):
            load_helsinki_physical(routes=[(start, "atlantis")])

    def test_the_loaded_graph_moves_an_actor_along_a_real_route(self) -> None:
        start = start_location()
        other = next(entry["id"] for entry in self.raw["nodes"] if entry["id"] != start)
        graph = load_helsinki_physical(routes=[(start, other)])
        graph.enter("rookie", start)
        graph.move("rookie", other)
        self.assertEqual(graph.at("rookie"), other)
        self.assertTrue(graph.co_located("rookie", "rookie") is True)

    def test_a_graph_without_routes_still_validates(self) -> None:
        graph = load_helsinki_physical()
        self.assertIsInstance(graph, PhysicalGraph)
        self.assertEqual(graph.routes, ())


if __name__ == "__main__":
    unittest.main()
