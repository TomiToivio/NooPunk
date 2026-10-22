"""Validated adapters between RPG graph effects and live domain graphs."""

from __future__ import annotations

from collections.abc import Mapping

import networkx as nx

from .models import GraphEffect


def apply_social_graph_effect(
    graph: nx.Graph,
    effect: GraphEffect,
    *,
    aliases: Mapping[str, str] | None = None,
) -> bool:
    """Apply one bounded social relationship delta; ignore other domains.

    Returns ``True`` when the effect was applied. IDs must resolve to existing
    social nodes so an integration mismatch cannot silently create ghost actors.
    """
    if effect.domain != "social":
        return False
    if effect.operation != "adjust_edge" or effect.target is None or effect.key != "relationship":
        raise ValueError(f"Unsupported social graph effect: {effect.operation}/{effect.key}")
    if isinstance(effect.value, bool) or not isinstance(effect.value, (int, float)):
        raise ValueError("Social relationship adjustment must be numeric")

    source = (aliases or {}).get(effect.source, effect.source)
    if source not in graph or effect.target not in graph:
        raise ValueError(f"Social effect references unknown character: {source} -> {effect.target}")
    if not graph.has_edge(source, effect.target):
        graph.add_edge(source, effect.target, relationship=0)
    current = graph[source][effect.target].get("relationship", 0)
    if isinstance(current, bool) or not isinstance(current, (int, float)):
        raise ValueError("Existing social relationship must be numeric")
    graph[source][effect.target]["relationship"] = max(-100, min(100, current + effect.value))
    return True
