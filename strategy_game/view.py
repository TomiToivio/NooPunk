"""Read-only cartographic/network view model, without a map or game engine.

The political layer (issue #282, Layer II) appears here in two ways, and neither adds a rule:

* :func:`board_view` emits political records as **typed nodes inside its existing
  ``network_nodes``**, after the faction nodes. The view's documented key set and the node/edge
  field sets are unchanged, because the whole political field is one labelled multiplex graph
  rather than a second structure. Political *relations* are ordinary entries in
  ``network_edges`` whose ``layer`` is a
  :class:`strategy_game.politics.RelationLayer` value.
* :func:`political_view` is the dedicated Layer II panel: the four political collections plus the
  relations between them, display fields only.

Neither function decides what any record means, what a player may do, or what a relation costs.
"""
from __future__ import annotations

from typing import Any

from .core import WorldState
from .politics import RELATION_LAYERS


def _political_nodes(state: WorldState) -> list[dict[str, Any]]:
    """Political records as nodes. Emitted after factions, in a fixed kind order."""
    groups = (
        ("demand", state.demands),
        ("signifier", state.signifiers),
        ("formation", state.formations),
        ("frontier", state.frontiers),
    )
    return [
        {"id": item.identifier, "label": item.label, "type": kind}
        for kind, collection in groups
        for item in collection
    ]


def board_view(state: WorldState) -> dict[str, Any]:
    return {
        "schema_version": state.schema_version,
        "locations": [
            {"id": x.identifier, "label": x.label, "grid_row": x.grid_row,
             "grid_column": x.grid_column} for x in state.locations
        ],
        "network_nodes": [
            {"id": x.identifier, "label": x.name, "type": "faction"}
            for x in state.factions
        ] + _political_nodes(state),
        "network_edges": [
            {"source": x.source, "target": x.target, "layer": x.layer}
            for x in state.edges
        ],
        "assets": [
            {"id": x.identifier, "label": x.label, "location_id": x.location_id,
             "owner_faction_id": x.owner_faction_id} for x in state.assets
        ],
    }


def political_view(state: WorldState) -> dict[str, Any]:
    """The Layer II panel: the declared political field, display fields only.

    Returns the four political collections, the relations among them (edges whose ``layer`` is a
    declared political relation), and each demand's declared claimant. No strength, score,
    stability, confidence or threshold appears, because this layer has no approved rules.
    """
    return {
        "schema_version": state.schema_version,
        "signifier_kinds": [
            {"id": x.identifier, "label": x.label, "kind": x.kind.value}
            for x in state.signifiers
        ],
        "demands": [
            {"id": x.identifier, "label": x.label, "claimant_id": x.claimant_id}
            for x in state.demands
        ],
        "formations": [
            {"id": x.identifier, "label": x.label} for x in state.formations
        ],
        "frontiers": [
            {"id": x.identifier, "label": x.label} for x in state.frontiers
        ],
        "relations": [
            {"source": x.source, "target": x.target, "layer": x.layer}
            for x in state.edges if x.layer in RELATION_LAYERS
        ],
    }
