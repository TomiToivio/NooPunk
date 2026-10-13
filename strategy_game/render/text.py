"""A text map provider and board renderer for the crossover game (issue #347's interface spike).

Design constraints this file obeys, and the reason each is stated rather than assumed:

* **A view, not a rule.** Nothing here resolves anything. It reads declared state and returns text.
* **No inference.** :class:`TextMapProvider` returns locations, nodes, declared edges and assets —
  never borders, travel, control or ownership, which is the constraint ``ports.MapProvider`` states.
* **No second game.** The state comes in as a :class:`strategy_game.core.WorldState` argument, so
  no Gate D join is performed and there is an argument left to remove. The display projection is
  :func:`strategy_game.view.board_view`, whose five-key shape is pinned by tests and a CI smoke
  step; this module builds its *own* view model on top instead of widening that one.
* **Offline and dependency-free.** Standard library only, so ``VISION.md`` §7a's "runnable from
  source, offline, no account, no service" holds by construction, and no model provider is in the
  import graph.
* **Deterministic.** The same state renders to byte-identical text, so a test can assert it.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..core import Faction, Leader, Location, NetworkEdge, WorldState
from ..view import board_view

#: Version of this renderer's own view model (not the world's ``schema_version``).
RENDER_SCHEMA_VERSION = "render-text-1"

#: The only complete local content in the crossover (#322/#323/#324): 8 locations, 7 routes,
#: 3 parties, 12 leaders. Used by the command line so the spike draws something real.
LOCAL_SLICE_DATA = Path(__file__).resolve().parents[1] / "data" / "ukweli_local.json"

#: Keys a renderer must never invent. Asserted by the tests.
FORBIDDEN_INFERENCE_KEYS = ("borders", "travel", "control", "ownership", "victory", "score")


class TextMapProvider:
    """The reserved ``MapProvider`` seam, filled in as a text view.

    ``describe`` returns a portable mapping for a renderer to draw. It is deliberately a *copy* of
    the pinned board projection plus a renderer version, and it adds no interpretation: a map
    provider that inferred a border or a sphere of control would be writing rules.
    """

    def describe(self, state: WorldState) -> dict[str, Any]:
        view = board_view(state)
        return {
            "schema_version": RENDER_SCHEMA_VERSION,
            "world_schema_version": view["schema_version"],
            "locations": view["locations"],
            "network_nodes": view["network_nodes"],
            "network_edges": view["network_edges"],
            "assets": view["assets"],
        }


def _label_index(view: dict[str, Any]) -> dict[str, str]:
    labels = {node["id"]: node["label"] for node in view["network_nodes"]}
    labels.update({loc["id"]: loc["label"] for loc in view["locations"]})
    return labels


def board_lines(state: WorldState) -> tuple[str, ...]:
    """The board as deterministic text lines. Empty state yields an empty-board note."""
    view = board_view(state)
    header = (
        f"board [{view['schema_version']}] — {len(view['locations'])} locations, "
        f"{len(view['network_nodes'])} nodes, {len(view['network_edges'])} routes, "
        f"{len(view['assets'])} assets, {len(state.leaders)} leaders"
    )
    lines: list[str] = [header]
    if not view["locations"] and not view["network_nodes"] and not view["network_edges"]:
        lines.append("(empty scaffold board: no declared content)")
        return tuple(lines)

    labels = _label_index(view)
    if view["locations"]:
        lines.append("")
        lines.append("locations:")
        for loc in view["locations"]:
            coords = ""
            if loc["latitude"] is not None and loc["longitude"] is not None:
                coords = f" ({loc['latitude']}, {loc['longitude']})"
            lines.append(f"  - {loc['label']} [{loc['id']}]{coords}")
    if view["network_nodes"]:
        lines.append("")
        lines.append("nodes:")
        for node in view["network_nodes"]:
            lines.append(f"  - {node['label']} [{node['id']}] ({node['type']})")
    if view["network_edges"]:
        lines.append("")
        lines.append("routes (declared edges; direction, meaning and control are not implied):")
        for edge in view["network_edges"]:
            layer = edge["layer"] or "unlabelled"
            lines.append(
                f"  - {labels.get(edge['source'], edge['source'])}"
                f" -- {labels.get(edge['target'], edge['target'])} [{layer}]"
            )
    if view["assets"]:
        lines.append("")
        lines.append("assets:")
        for asset in view["assets"]:
            where = labels.get(asset["location_id"] or "", asset["location_id"] or "-")
            owner = labels.get(asset["owner_faction_id"] or "", asset["owner_faction_id"] or "-")
            lines.append(f"  - {asset['label']} at {where}, held by {owner}")
    if state.leaders:
        lines.append("")
        lines.append("leaders:")
        for leader in state.leaders:
            attributes = ""
            if leader.attributes:
                attributes = " " + json.dumps(leader.attributes, sort_keys=True, ensure_ascii=False)
            lines.append(f"  - {leader.name} [{leader.identifier}]{attributes}")
    return tuple(lines)


def render_board_text(state: WorldState) -> str:
    """The whole board as one string."""
    return "\n".join(board_lines(state))


def render_roster_text(roster: Any) -> str:
    """Card faces for a character roster, in roster order.

    Uses the character-card layer's own front renderer, which never prints ``gm_notes``: a renderer
    must not be the thing that leaks a secret.
    """
    from ..characters import render_front

    cards = list(roster)
    lines = [f"cards [{RENDER_SCHEMA_VERSION}] — {len(cards)} in the roster"]
    for card in cards:
        lines.append("")
        lines.extend(render_front(card).splitlines())
    return "\n".join(lines)


def state_from_local_slice(path: Path | str | None = None) -> WorldState:
    """Build a display :class:`WorldState` from ``data/ukweli_local.json``.

    A **view adapter**, not a simulation: locations, parties and leaders are copied as declared, and
    each route pair becomes an unlabelled-layer edge. There is no transition, no turn and no rule —
    the local slice's own provisional playtest rules stay in ``strategy_game/local_slice.py`` where
    they belong.
    """
    source = Path(path) if path is not None else LOCAL_SLICE_DATA
    data = json.loads(source.read_text(encoding="utf-8"))

    def name_of(item: dict[str, Any]) -> str:
        return str(item.get("name") or item.get("label") or item.get("id") or "")

    locations = [
        Location(identifier=str(item["id"]), label=name_of(item))
        for item in data.get("locations", [])
        if item.get("id")
    ]
    factions = [
        Faction(identifier=str(item["id"]), name=name_of(item))
        for item in data.get("parties", [])
        if item.get("id")
    ]
    leaders = [
        Leader(identifier=str(item["id"]), name=name_of(item))
        for item in data.get("leaders", [])
        if item.get("id")
    ]
    edges = [
        NetworkEdge(source=str(pair[0]), target=str(pair[1]), layer="route")
        for pair in data.get("routes", [])
        if isinstance(pair, (list, tuple)) and len(pair) >= 2
    ]
    return WorldState(locations=locations, factions=factions, leaders=leaders, edges=edges)
