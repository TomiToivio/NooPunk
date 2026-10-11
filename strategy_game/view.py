"""Read-only cartographic/network view model, without a map or game engine."""
from __future__ import annotations

from typing import Any

from .core import WorldState


def board_view(state: WorldState) -> dict[str, Any]:
    return {
        "schema_version": state.schema_version,
        "locations": [
            {"id": x.identifier, "label": x.label, "latitude": x.latitude,
             "longitude": x.longitude} for x in state.locations
        ],
        "network_nodes": [
            {"id": x.identifier, "label": x.name, "type": "faction"}
            for x in state.factions
        ],
        "network_edges": [
            {"source": x.source, "target": x.target, "layer": x.layer}
            for x in state.edges
        ],
        "assets": [
            {"id": x.identifier, "label": x.label, "location_id": x.location_id,
             "owner_faction_id": x.owner_faction_id} for x in state.assets
        ],
    }
