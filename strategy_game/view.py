"""Read-only cartographic/network view model, without a map or game engine.

The board view renders :class:`~strategy_game.core.WorldState` and stays map/network-neutral.

:func:`political_view` is the Layer II rendering hook. It takes a
:class:`~strategy_game.political.PoliticalField` **explicitly** rather than reading one off the
world state, because integrating Layer II into ``WorldState`` is a Gate D decision that has not
been made (``docs/RULE_SYSTEM_RESEARCH.md``; ``docs/INTEGRATION_BOUNDARIES.md``). Passing the
field in keeps that boundary intact while still giving the layer something to render.

Neither function decides what a record means, what a player may do, or what a relation costs.
"""
from __future__ import annotations

from typing import Any

from .core import WorldState
from .political import PoliticalField


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


def political_view(field: PoliticalField) -> dict[str, Any]:
    """The Layer II panel: the declared political field, display fields only.

    Exposes the field's own ``schema_version``, the four record kinds, the articulations and the
    communicative ties — each as display fields and nothing more. No strength, score, stability,
    confidence, threshold or reach appears, and a tie's ``mode`` is passed through exactly as
    recorded (``None`` when the author has not recorded one) rather than being defaulted.

    The caller supplies the field, so this hook never reaches into the world state.
    """
    return {
        "schema_version": field.schema_version,
        "signifiers": [
            {"id": x.identifier, "label": x.label,
             "role": None if x.role is None else x.role.value}
            for x in field.signifiers
        ],
        "demands": [
            {"id": x.identifier, "text": x.text} for x in field.demands
        ],
        "formations": [
            {"id": x.identifier, "label": x.label, "signifier_ids": list(x.signifier_ids)}
            for x in field.formations
        ],
        "frontiers": [
            {"id": x.identifier, "signifier_id": x.signifier_id,
             "included_demand_ids": list(x.included_demand_ids),
             "excluded_demand_ids": list(x.excluded_demand_ids)}
            for x in field.frontiers
        ],
        "articulations": [
            {"signifier_id": x.signifier_id, "demand_id": x.demand_id}
            for x in field.articulations
        ],
        "ties": [
            {"source_id": x.source_id, "target_id": x.target_id,
             "mode": None if x.mode is None else x.mode.value}
            for x in field.ties
        ],
    }
