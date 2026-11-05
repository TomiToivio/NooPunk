"""Human-authored graph records for issue #1178.

Markdown files begin with YAML frontmatter; the body is freeform scene prose.
The loader intentionally treats the prose as description, not game instructions.
Install the optional 'yaml' dependency to read YAML; JSON is a YAML subset and
works without extras. Do not interpret frontmatter as executable rule code.
"""
from __future__ import annotations

from pathlib import Path
import json
from typing import Any, Mapping

from .four_graphs import FourGraphs, GraphContractError


def read_record(markdown: str) -> dict[str, Any]:
    """Read one Markdown record with a YAML (or JSON) frontmatter mapping."""
    if not markdown.startswith("---\n"):
        raise GraphContractError("record requires --- YAML frontmatter")
    header, separator, body = markdown[4:].partition("\n---\n")
    if not separator:
        raise GraphContractError("record frontmatter requires a closing ---")
    try:
        # JSON is valid YAML 1.2; permits standard-library-only deployment.
        record = json.loads(header)
    except json.JSONDecodeError:
        try:
            import yaml
        except ImportError as exc:
            raise GraphContractError(
                "YAML frontmatter requires optional PyYAML; use JSON frontmatter otherwise"
            ) from exc
        record = yaml.safe_load(header)
    if not isinstance(record, dict):
        raise GraphContractError("frontmatter must be a mapping")
    if not record.get("graph_type") or not record.get("record_id"):
        raise GraphContractError("record needs graph_type and record_id")
    result = dict(record)
    result["description"] = body.strip()
    return result


def load_record(path: str | Path) -> dict[str, Any]:
    return read_record(Path(path).read_text(encoding="utf-8"))


def compile_graphs(records: list[Mapping[str, Any]]) -> FourGraphs:
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
            raise GraphContractError("record_ids must be unique nonempty strings")
        record_ids.add(identifier)
        if key not in wanted or key in grouped:
            raise GraphContractError("only one authored record per supported graph type")
        data = record.get("data")
        if not isinstance(data, Mapping) or data.get("graph_type") != key:
            raise GraphContractError("graph data mapping/type mismatch")
        grouped[key] = data
    if set(grouped) != wanted:
        raise GraphContractError(f"four graph families required, missing {sorted(wanted-set(grouped))}")
    return FourGraphs.from_dict({
        "format": "noopunk.four_graphs", "version": 1,
        **grouped,
        "avatars": {},
    })
