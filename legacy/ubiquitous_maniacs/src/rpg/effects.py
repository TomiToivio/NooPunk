"""Application of portable RPG effects to NetworkX domain graphs."""

from __future__ import annotations

import networkx as nx

from .models import GraphEffect


def apply_graph_effect(graph: nx.Graph, effect: GraphEffect) -> None:
    if effect.operation == "set_node":
        graph.add_node(effect.source)
        graph.nodes[effect.source][effect.key] = effect.value
        return
    if effect.target is None:
        raise ValueError(f"{effect.operation} requires a target")
    if effect.operation == "remove_edge":
        if graph.has_edge(effect.source, effect.target):
            graph.remove_edge(effect.source, effect.target)
        return
    graph.add_edge(effect.source, effect.target)
    if effect.operation == "set_edge":
        graph[effect.source][effect.target][effect.key] = effect.value
    elif effect.operation == "adjust_edge":
        old = graph[effect.source][effect.target].get(effect.key, 0)
        graph[effect.source][effect.target][effect.key] = old + (effect.value or 0)
    else:
        raise ValueError(f"Unknown graph operation: {effect.operation}")
