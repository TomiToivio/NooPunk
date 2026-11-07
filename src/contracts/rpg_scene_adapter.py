"""Turn a validated Story Graph into the graph objects the RPG already uses (#1295).

The RPG consumed a story graph before this issue existed — `src.world.graphs.StoryNode` and `StoryGraph`. The
adapter exists so the new contract feeds that existing structure instead of growing a second one.
"""

from __future__ import annotations

from ..world.graphs import GraphError, StoryGraph, StoryLink, StoryNode
from .story_graph_contract import StoryScene, scenes


def to_story_graph(document: dict, *, story_root=None) -> StoryGraph:
    """Build the RPG's own StoryGraph from a validated document.

    Raises :class:`~src.contracts.story_graph_contract.StoryContractError` on a contract violation and
    :class:`~src.world.graphs.GraphError` if the hierarchy itself is inconsistent (a scene under a scene, a
    dangling parent). Both are refusals, not repairs.
    """
    nodes: dict[str, StoryNode] = {}
    for scene in scenes(document, **({'story_root': story_root} if story_root else {})):
        nodes[scene.id] = StoryNode(
            id=scene.id,
            label=scene.label,
            kind=scene.kind,
            parent_id=scene.parent_id,
            scene_types=scene.scene_types,
            prerequisites=scene.prerequisites,
        )
    links = tuple(
        StoryLink(
            source=edge["source"],
            target=edge["target"],
            kind=edge["kind"],
            condition=edge.get("condition", ""),
        )
        for edge in document.get("edges", [])
    )
    try:
        return StoryGraph(nodes=nodes, links=links)
    except GraphError as exc:
        raise GraphError(f"story graph is invalid: {exc}") from exc


def scene_brief(scene: StoryScene) -> dict:
    """What the RPG needs to open a scene, and where it came from."""
    return {
        "id": scene.id,
        "label": scene.label,
        "kind": scene.kind,
        "scene_types": list(scene.scene_types),
        "prerequisites": list(scene.prerequisites),
        "source_ref": scene.source_ref,
        "authored": scene.authored,
        "summary": scene.summary,
    }
