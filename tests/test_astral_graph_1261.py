"""The astral graph's own invariants (#1261).

The perception and targeting layer of #1261 lives in `src/rules/astral_body.py` (PR #1262), and this
module must not re-implement it. What belongs *here* is the part that only the graph can answer:

* an edge has a **relation**, and in Time/Space a relation is the route — a `corridor` between two
  astral places says nothing about whether one is reachable from the other;
* a conscious agent is an **occupant**, never a node, which is the #1178 rule applied to Noöspace.

Both are cheap now and expensive to retrofit once a mission navigates symbolically.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.rules.astral import (
    AstralEdge,
    AstralError,
    AstralGraph,
    AstralNode,
)


def graph() -> AstralGraph:
    return AstralGraph(
        nodes={
            "astral.room": AstralNode("astral.room", "Bedroom overlay"),
            "astral.corridor": AstralNode("astral.corridor", "Symbolic corridor"),
        },
        edges=(
            AstralEdge("astral.room", "astral.corridor", relation="memory"),
            AstralEdge("astral.corridor", "astral.room", relation="", directed=False),
        ),
    )


def test_an_edge_reports_its_relation() -> None:
    assert graph().relation("astral.room", "astral.corridor") == "memory"


def test_an_undirected_edge_reports_its_relation_in_both_directions() -> None:
    book = AstralGraph(
        nodes={"a": AstralNode("a", "A"), "b": AstralNode("b", "B")},
        edges=(AstralEdge("a", "b", relation="kinship", directed=False),),
    )
    assert book.relation("b", "a") == "kinship"


def test_unconnected_nodes_report_no_relation() -> None:
    book = AstralGraph(nodes={"a": AstralNode("a", "A"), "b": AstralNode("b", "B")})
    assert book.relation("a", "b") == ""


def test_a_conscious_agent_cannot_be_a_location() -> None:
    with pytest.raises(AstralError) as caught:
        AstralNode("agent.wendt", "Laura Wendt", node_type="agent")
    assert "occupant" in str(caught.value)


def test_ordinary_astral_locations_are_still_allowed() -> None:
    for node_type in ("symbolic_site", "physical_anchor", ""):
        assert AstralNode("astral.x", "X", node_type=node_type or "symbolic_site")
