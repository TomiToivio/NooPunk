import networkx as nx
import pytest

from src.rpg import GraphEffect, apply_social_graph_effect


def social_graph() -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(("sven_olof_romppainen", "ingrid_falk"))
    graph.add_edge("sven_olof_romppainen", "ingrid_falk", relationship=98)
    return graph


def test_social_adapter_maps_rpg_identity_and_clamps_relationship() -> None:
    graph = social_graph()
    effect = GraphEffect(
        "social", "adjust_edge", "romppainen_day_1", "ingrid_falk", "relationship", 5
    )

    applied = apply_social_graph_effect(
        graph, effect, aliases={"romppainen_day_1": "sven_olof_romppainen"}
    )

    assert applied is True
    assert graph["sven_olof_romppainen"]["ingrid_falk"]["relationship"] == 100
    assert "romppainen_day_1" not in graph


def test_social_adapter_ignores_other_domains() -> None:
    graph = social_graph()
    effect = GraphEffect("cyber", "set_node", "terminal", key="access", value=True)

    assert apply_social_graph_effect(graph, effect) is False
    assert "terminal" not in graph


@pytest.mark.parametrize(
    "effect",
    [
        GraphEffect("social", "set_edge", "a", "ingrid_falk", "relationship", 1),
        GraphEffect("social", "adjust_edge", "a", "ingrid_falk", "trust", 1),
        GraphEffect("social", "adjust_edge", "a", "ingrid_falk", "relationship", "five"),
        GraphEffect("social", "adjust_edge", "ghost", "ingrid_falk", "relationship", 1),
    ],
)
def test_social_adapter_rejects_malformed_or_unknown_effects(effect: GraphEffect) -> None:
    with pytest.raises(ValueError):
        apply_social_graph_effect(social_graph(), effect, aliases={"a": "sven_olof_romppainen"})
