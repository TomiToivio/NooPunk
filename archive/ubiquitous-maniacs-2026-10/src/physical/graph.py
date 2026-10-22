from __future__ import annotations

import networkx as nx

from ..graph_serialization import empty_domain_graph, graph_to_dict, graph_to_dot, graph_to_gexf_bytes


def build_physical_graph() -> nx.Graph:
    """Create the physical domain graph without adding laboratory spaces yet."""
    return empty_domain_graph("physical")


__all__ = ["build_physical_graph", "graph_to_dict", "graph_to_dot", "graph_to_gexf_bytes"]
