"""Load the canonical Helsinki location data into the physical graph (#1178).

`data/world/helsinki_locations.json` already lists the places a NoöPunk game opens with, but it carries no routes:
travel is an action the old map panel handled. The graph model needs edges, so this adapter loads the places and
takes the routes from the caller rather than inventing Helsinki geography inside a test.

Import as ``src.world.helsinki`` (or with ``src`` on the path and a package-qualified name). A bare
``import world.helsinki`` is ambiguous in this repository: ``mud/world`` is also importable as ``world`` when the
MUD test packages put ``mud/`` on ``sys.path``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

try:  # the repository's own layout
    from .graphs import GraphError, LocationNode, PhysicalGraph, PhysicalRoute
except ImportError:  # a caller that put `src` on sys.path
    from world.graphs import GraphError, LocationNode, PhysicalGraph, PhysicalRoute  # type: ignore[no-redef]

__all__ = ["load_helsinki_physical", "HELSINKI_LOCATIONS"]

HELSINKI_LOCATIONS = Path(__file__).resolve().parents[2] / "data" / "world" / "helsinki_locations.json"


def _district_node_id(name: str) -> str:
    return "district_" + name.split("/")[0].strip().lower().replace(" ", "_")


def load_helsinki_physical(
    path: str | Path | None = None,
    *,
    routes: Iterable[tuple[str, str]] = (),
    directed: bool = False,
) -> PhysicalGraph:
    """Build a `PhysicalGraph` from the canonical location file.

    Districts become parent nodes so the hierarchy is world → district → location, matching the graph model's
    scale ordering. Every place keeps its canonical id, so nothing downstream has to remap names.
    """
    source = Path(path) if path is not None else HELSINKI_LOCATIONS
    raw: Mapping[str, object] = json.loads(source.read_text(encoding="utf-8"))
    entries = list(raw.get("nodes", ()))  # type: ignore[arg-type]

    nodes: dict[str, LocationNode] = {}
    for entry in entries:
        district = str(entry.get("district", "")).strip()
        if not district:
            continue
        district_id = _district_node_id(district)
        if district_id not in nodes:
            nodes[district_id] = LocationNode(district_id, district, kind="district")

    for entry in entries:
        node_id = str(entry["id"])
        district = str(entry.get("district", "")).strip()
        nodes[node_id] = LocationNode(
            node_id,
            str(entry.get("name", node_id)),
            kind="location",
            parent_id=_district_node_id(district) if district else "",
        )

    edges = tuple(PhysicalRoute(source_node, target_node, directed=directed) for source_node, target_node in routes)
    for edge in edges:
        for end in (edge.source, edge.target):
            if end not in nodes:
                raise GraphError(f"route endpoint {end!r} is not a Helsinki location")

    return PhysicalGraph(nodes=nodes, routes=edges)


def start_location(path: str | Path | None = None) -> str:
    """The canonical opening location id, so callers do not hard-code it."""
    source = Path(path) if path is not None else HELSINKI_LOCATIONS
    raw: Mapping[str, object] = json.loads(source.read_text(encoding="utf-8"))
    start = str(raw.get("start", "")).strip()
    if not start:
        raise GraphError("the location file has no start node")
    return start
