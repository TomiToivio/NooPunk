"""The astral graph's own invariants (#1261).

The perception and targeting layer of #1261 lives in `src/rules/astral_body.py` (merged in #1262), and
this module must not re-implement it. What belongs *here* is the part only the graph can answer:

* an edge has a **relation**, and in Time/Space a relation *is* the route — a `corridor` between two
  astral places says nothing about whether one is reachable from the other;
* a conscious agent is an **occupant**, never a node: the #1178 rule applied to Noöspace.

`unittest`, because the CI gate runs `python -m unittest discover` and does not install pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.rules.astral import (
    AstralEdge,
    AstralError,
    AstralGraph,
    AstralNode,
)


class TestEdgeRelations(unittest.TestCase):
    def test_an_edge_reports_its_relation(self) -> None:
        graph = AstralGraph(
            nodes={"a": AstralNode("a", "A"), "b": AstralNode("b", "B")},
            edges=(AstralEdge("a", "b", relation="memory"),),
        )
        self.assertEqual(graph.relation("a", "b"), "memory")

    def test_an_undirected_edge_reports_its_relation_in_both_directions(self) -> None:
        graph = AstralGraph(
            nodes={"a": AstralNode("a", "A"), "b": AstralNode("b", "B")},
            edges=(AstralEdge("a", "b", relation="kinship", directed=False),),
        )
        self.assertEqual(graph.relation("b", "a"), "kinship")

    def test_unconnected_nodes_report_no_relation(self) -> None:
        graph = AstralGraph(nodes={"a": AstralNode("a", "A"), "b": AstralNode("b", "B")})
        self.assertEqual(graph.relation("a", "b"), "")


class TestAgentsAreOccupantsNotPlaces(unittest.TestCase):
    def test_a_conscious_agent_cannot_be_a_location_node(self) -> None:
        with self.assertRaises(AstralError) as caught:
            AstralNode("agent.wendt", "Laura Wendt", node_type="agent")
        self.assertIn("occupant", str(caught.exception))

    def test_ordinary_astral_locations_are_still_allowed(self) -> None:
        for node_type in ("symbolic_site", "physical_anchor"):
            self.assertEqual(
                AstralNode("astral.x", "X", node_type=node_type).node_type, node_type
            )


if __name__ == "__main__":
    unittest.main()
