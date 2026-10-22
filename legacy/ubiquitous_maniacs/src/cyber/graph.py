from __future__ import annotations

import networkx as nx

from ..graph_serialization import empty_domain_graph, graph_to_dict, graph_to_dot, graph_to_gexf_bytes


def build_cyber_graph() -> nx.Graph:
    """Create the cyber domain graph without adding infrastructure content yet."""
    return empty_domain_graph("cyber")


__all__ = ["build_cyber_graph", "graph_to_dict", "graph_to_dot", "graph_to_gexf_bytes"]
