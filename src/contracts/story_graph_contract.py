"""The Story Graph contract: what an adaptation may claim, and what it may not (#1295).

A story graph is a *derivative* of the manuscript. The failure mode this module exists to prevent is an
adaptation that quietly acquires a scene the author never wrote: a node with a plausible label, no source, and
no one noticing until the RPG ships it as canon.

So the contract is strict about one thing and lenient about the rest: every node must say where it came from,
and a node whose source does not resolve must be explicitly marked `authored: true` — meaning Tomi approved it
outside the manuscript, by hand.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = json.loads((ROOT / "data" / "schema" / "subproject_contracts_1295.json").read_text(encoding="utf-8"))
STORY_GRAPH = CONTRACT["story_graph"]
SCHEMA = STORY_GRAPH["schema"]
STORY_ROOT = ROOT / "NooPunk-Story" / "Story"


class StoryContractError(ValueError):
    """A document that is not a valid story graph."""


@dataclass(frozen=True, slots=True)
class StoryScene:
    """One validated node, in the shape the RPG adapter wants."""

    id: str
    kind: str
    label: str
    source_ref: str
    authored: bool
    scene_types: tuple[str, ...]
    prerequisites: tuple[str, ...]
    parent_id: str
    summary: str


def _problem(message: str) -> str:
    return message


def validate(document: dict, *, story_root: Path = STORY_ROOT) -> list[str]:
    """Return every contract violation. An empty list means the document may be consumed."""
    problems: list[str] = []
    if document.get("schema") != SCHEMA:
        problems.append(_problem(f"schema must be {SCHEMA!r}, got {document.get('schema')!r}"))
        return problems

    nodes = document.get("nodes")
    edges = document.get("edges", [])
    if not isinstance(nodes, list) or not nodes:
        problems.append(_problem("a story graph needs a non-empty 'nodes' list"))
        return problems

    seen: set[str] = set()
    kinds = {node.get("id"): node.get("kind") for node in nodes if isinstance(node, dict)}
    for index, node in enumerate(nodes):
        where = f"nodes[{index}]"
        if not isinstance(node, dict):
            problems.append(_problem(f"{where} is not an object"))
            continue
        missing = [field for field in STORY_GRAPH["required_node_fields"] if not node.get(field)]
        if missing:
            problems.append(_problem(f"{where} is missing {', '.join(missing)}"))
            continue
        node_id = node["id"]
        if node_id in seen:
            problems.append(_problem(f"duplicate node id {node_id!r}"))
        seen.add(node_id)
        if node["kind"] not in STORY_GRAPH["node_kinds"]:
            problems.append(_problem(f"{where} has unknown kind {node['kind']!r}"))
        authored = bool(node.get("authored", False))
        source_ref = str(node["source_ref"])
        if not authored and not (story_root / source_ref).exists():
            problems.append(
                _problem(
                    f"{where} cites {source_ref!r}, which is not in the manuscript; "
                    "mark it authored:true only if Tomi approved it by hand"
                )
            )
        for scene_type in node.get("scene_types", []):
            if scene_type not in STORY_GRAPH["scene_type_vocabulary"]:
                problems.append(_problem(f"{where} has unknown scene type {scene_type!r}"))

    for index, edge in enumerate(edges):
        where = f"edges[{index}]"
        if not isinstance(edge, dict):
            problems.append(_problem(f"{where} is not an object"))
            continue
        missing = [field for field in STORY_GRAPH["required_edge_fields"] if not edge.get(field)]
        if missing:
            problems.append(_problem(f"{where} is missing {', '.join(missing)}"))
            continue
        if edge["kind"] not in STORY_GRAPH["edge_kinds"]:
            problems.append(_problem(f"{where} has unknown kind {edge['kind']!r}"))
        for end in ("source", "target"):
            if edge[end] not in kinds:
                problems.append(_problem(f"{where} points at unknown node {edge[end]!r}"))
        if edge["kind"] == "choice" and not edge.get("label"):
            problems.append(_problem(f"{where} is a choice without a label a player would recognise"))
    return problems


def scenes(document: dict, *, story_root: Path = STORY_ROOT) -> tuple[StoryScene, ...]:
    """The validated nodes as records. Raises instead of returning a partial graph."""
    problems = validate(document, story_root=story_root)
    if problems:
        raise StoryContractError("; ".join(problems))
    out = []
    for node in document["nodes"]:
        out.append(
            StoryScene(
                id=node["id"],
                kind=node["kind"],
                label=node["label"],
                source_ref=node["source_ref"],
                authored=bool(node.get("authored", False)),
                scene_types=tuple(node.get("scene_types", ())),
                prerequisites=tuple(node.get("prerequisites", ())),
                parent_id=node.get("parent_id", ""),
                summary=node.get("summary", ""),
            )
        )
    return tuple(out)


def choices(document: dict, scene_id: str) -> tuple[dict, ...]:
    """The labelled choices leaving a scene, in document order."""
    return tuple(
        edge for edge in document.get("edges", [])
        if edge.get("source") == scene_id and edge.get("kind") == "choice"
    )
