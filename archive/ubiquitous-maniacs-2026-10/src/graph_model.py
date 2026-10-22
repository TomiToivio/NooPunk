"""Backward-compatible exports for the social graph domain module."""

from .social.graph import (
    build_social_graph,
    get_person_relationships,
    graph_to_dict,
    graph_to_dot,
    graph_to_gexf_bytes,
    list_people,
    list_relationships,
)

__all__ = [
    "build_social_graph",
    "get_person_relationships",
    "graph_to_dict",
    "graph_to_dot",
    "graph_to_gexf_bytes",
    "list_people",
    "list_relationships",
]
