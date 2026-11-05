"""Human-authored graph records for issue #1178 — one model, the runtime one.

Markdown files begin with YAML frontmatter; the body is freeform scene prose. The loader
intentionally treats the prose as description, not game instructions.

Since the #1178 graph merge, this module compiles straight into `src/world/graphs.py` — there is no
second model. The authored `data` blocks are exactly that module's per-graph dict shapes, and the
snapshot it produces is `WorldGraphs.to_dict()` with format ``noopunk.world.graphs``.

Install the optional ``yaml`` dependency to read YAML; JSON is a YAML subset and works without
extras. Do not interpret frontmatter as executable rule code.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

try:  # imported as src.rules.graph_authoring
    from ..world.graphs import GraphError, WorldGraphs
except ImportError:  # a caller that put `src` on sys.path
    from world.graphs import GraphError, WorldGraphs  # type: ignore[no-redef]


def read_record(markdown: str) -> dict[str, Any]:
    """Read one Markdown record with a YAML (or JSON) frontmatter mapping."""
    if not markdown.startswith("---\n"):
        raise GraphError("record requires --- YAML frontmatter")
    header, separator, body = markdown[4:].partition("\n---\n")
    if not separator:
        raise GraphError("record frontmatter requires a closing ---")
    try:
        # JSON is valid YAML 1.2; permits standard-library-only deployment.
        record = json.loads(header)
    except json.JSONDecodeError:
        try:
            import yaml
        except ImportError as exc:
            raise GraphError(
                "YAML frontmatter requires optional PyYAML; use JSON frontmatter otherwise"
            ) from exc
        record = yaml.safe_load(header)
    if not isinstance(record, dict):
        raise GraphError("frontmatter must be a mapping")
    if not record.get("graph_type") or not record.get("record_id"):
        raise GraphError("record needs graph_type and record_id")
    result = dict(record)
    result["description"] = body.strip()
    return result


def load_record(path: str | Path) -> dict[str, Any]:
    return read_record(Path(path).read_text(encoding="utf-8"))


def compile_graphs(records: list[Mapping[str, Any]]) -> WorldGraphs:
    """Build the four-graph snapshot from four authored Markdown/YAML records.

    A record has a stable record_id, graph_type and 'data' mapping.
    The actual scene descriptions remain author-facing prose, not code.
    Each graph type is specified once. Astral has no entry by design.
    """
    wanted = {"physical", "cyber", "social", "story"}
    grouped: dict[str, Mapping[str, Any]] = {}
    record_ids: set[str] = set()
    for record in records:
        key = record.get("graph_type")
        identifier = record.get("record_id")
        if not isinstance(identifier, str) or not identifier or identifier in record_ids:
            raise GraphError("record_ids must be unique nonempty strings")
        record_ids.add(identifier)
        if key not in wanted or key in grouped:
            raise GraphError("only one authored record per supported graph type")
        data = record.get("data")
        if not isinstance(data, Mapping) or data.get("graph_type") != key:
            raise GraphError("graph data mapping/type mismatch")
        grouped[key] = data
    if set(grouped) != wanted:
        raise GraphError(f"four graph families required, missing {sorted(wanted - set(grouped))}")
    return WorldGraphs.from_dict({
        "format": "noopunk.world.graphs",
        "version": 1,
        **grouped,
    })
