from __future__ import annotations

import networkx as nx

from ..graph_serialization import empty_domain_graph, graph_to_dict, graph_to_dot, graph_to_gexf_bytes


def build_noetic_graph() -> nx.Graph:
    """Create the noetic domain graph without defining its discourse content yet."""
    return empty_domain_graph("noetic")


__all__ = ["build_noetic_graph", "graph_to_dict", "graph_to_dot", "graph_to_gexf_bytes"]
