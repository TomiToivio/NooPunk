"""Inspectable, non-predictive metrics for simulator runs (#1286).

The metrics describe the synthetic graph and trace. They are **not** hegemony
scores, legitimacy measures or predictions about real politics. A high degree or
a dense coalition is a property of the model's assumptions and seed.
"""

from __future__ import annotations

from collections import Counter, deque
from collections.abc import Iterable
from typing import Any

from .engine import SocialScienceSimulation

__all__ = ["graph_metrics", "simulation_metrics"]


def _components(
    nodes: Iterable[str], edges: Iterable[tuple[str, str]]
) -> list[set[str]]:
    adjacency: dict[str, set[str]] = {node: set() for node in nodes}
    for source, target in edges:
        adjacency.setdefault(source, set()).add(target)
        adjacency.setdefault(target, set()).add(source)
    seen: set[str] = set()
    found: list[set[str]] = []
    for node in sorted(adjacency):
        if node in seen:
            continue
        queue = deque([node])
        seen.add(node)
        component: set[str] = set()
        while queue:
            current = queue.popleft()
            component.add(current)
            for neighbour in sorted(adjacency[current]):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        found.append(component)
    return found


def graph_metrics(
    nodes: Iterable[str], edges: Iterable[tuple[str, str]], *, label: str
) -> dict[str, Any]:
    node_set = set(nodes)
    edge_list = [
        (source, target)
        for source, target in edges
        if source in node_set and target in node_set
    ]
    degree = Counter()
    for source, target in edge_list:
        degree[source] += 1
        degree[target] += 1
    components = _components(node_set, edge_list)
    possible = len(node_set) * (len(node_set) - 1)
    density = (2.0 * len(edge_list) / possible) if possible else 0.0
    return {
        "label": label,
        "nodes": len(node_set),
        "edges": len(edge_list),
        "density": round(density, 6),
        "components": len(components),
        "isolated": sum(1 for node in node_set if degree[node] == 0),
        "top_degree": [
            {"actor": actor, "degree": value}
            for actor, value in sorted(
                degree.items(), key=lambda item: (-item[1], item[0])
            )[:10]
        ],
    }


def simulation_metrics(simulation: SocialScienceSimulation) -> dict[str, Any]:
    actors = simulation.actors
    social = graph_metrics(
        actors,
        ((edge.source, edge.target) for edge in simulation.social_edges),
        label="social",
    )
    communication = graph_metrics(
        actors,
        ((edge.source, edge.target) for edge in simulation.communication_edges),
        label="communication",
    )
    event_kinds = Counter(event.kind for event in simulation.log.events)
    by_claim: dict[str, dict[str, Any]] = {}
    for claim_id, claim in sorted(simulation.claims.items()):
        stances = [
            float(actor.disposition.get(claim_id, 0.0)) for actor in actors.values()
        ]
        by_claim[claim_id] = {
            "label": claim.label,
            "mean_disposition": round(sum(stances) / len(stances), 6)
            if stances
            else 0.0,
            "positive": sum(1 for value in stances if value > 0),
            "negative": sum(1 for value in stances if value < 0),
            "neutral": sum(1 for value in stances if value == 0),
        }
    return {
        "synthetic": True,
        "turn": simulation.turn,
        "seed": simulation.config.seed,
        "actors": {
            "individual": sum(
                1 for actor in actors.values() if actor.kind == "individual"
            ),
            "organization": sum(
                1 for actor in actors.values() if actor.kind == "organization"
            ),
            "active": sum(1 for actor in actors.values() if actor.active),
        },
        "graphs": {"social": social, "communication": communication},
        "events": {
            "total": len(simulation.log.events),
            "by_kind": dict(sorted(event_kinds.items())),
        },
        "claims": by_claim,
        "provenance_note": "All values describe a synthetic run; they are exploratory, not empirical or predictive.",
    }
