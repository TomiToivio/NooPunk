"""Read-only operational index for issue #1121.

Canonical prose remains in design/ZONES.md. No physical routes, CWN mechanics,
permissions, zone coordinates, scripts or author draft contents are generated.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REGISTER = Path(__file__).resolve().parents[2] / "data" / "world" / "greater_helsinki_1121.json"

ZONE_CATEGORIES = frozenset(("economic", "diplomatic", "protection", "military_exclusion"))
CLAIM_STATUSES = frozenset(
    ("setting_fact", "agency_report", "rumor", "agency_debate", "unresolved", "contested_history")
)


class HelsinkiCanonError(ValueError):
    """Malformed or ambiguous source record must fail rather than invent lore."""


def load_register(path: str | Path = REGISTER) -> dict[str, Any]:
    """Load and validate a small, engine-neutral source index."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if raw.get("year") != 2045 or raw.get("municipality", {}).get("id") != "helsinki_2045":
        raise HelsinkiCanonError("expected the merged 2045 Helsinki setting")
    if set(raw["municipality"]["merged_former_municipalities"]) != {"Helsinki", "Espoo", "Vantaa"}:
        raise HelsinkiCanonError("2045 Helsinki must include all three former municipalities")
    levels = [row["level"] for row in raw["governance"]]
    if levels != ["municipal", "national", "eu", "global_xrisk"]:
        raise HelsinkiCanonError("X-Risk governance levels are municipal/national/EU/UN")
    categories: dict[str, int] = {name: 0 for name in ZONE_CATEGORIES}
    zone_ids: set[str] = set()
    for zone in raw["zones"]:
        category, zone_id = zone["category"], zone["id"]
        if category not in categories or zone_id in zone_ids:
            raise HelsinkiCanonError(f"invalid or duplicate zone: {zone_id}")
        if zone.get("claim_status") != "setting_fact":
            raise HelsinkiCanonError("zone designations must be established setting facts")
        categories[category] += 1
        zone_ids.add(zone_id)
    if categories != {"economic": 2, "diplomatic": 2, "protection": 3, "military_exclusion": 2}:
        raise HelsinkiCanonError("the source specifies 2/2/3/2 zone categories")
    for claim in raw["claims"]:
        if claim["status"] not in CLAIM_STATUSES:
            raise HelsinkiCanonError(f"unknown provenance status: {claim['status']}")
        if not set(claim["zone_ids"]).issubset(zone_ids):
            raise HelsinkiCanonError(f"unknown zone in claim: {claim['id']}")
    if raw["routes"] or raw["coordinates"]:
        raise HelsinkiCanonError("zone boundaries and map routes require author approval")
    return raw


def get_zone(zone_id: str, path: str | Path = REGISTER) -> dict[str, Any]:
    """Stable ID lookup, usable by future tabletop and Python adapters."""
    return next(
        (zone for zone in load_register(path)["zones"] if zone["id"] == zone_id),
        None,
    ) or _unknown_zone(zone_id)


def _unknown_zone(zone_id: str) -> dict[str, Any]:
    raise HelsinkiCanonError(f"unknown zone ID: {zone_id}")


def claims_for(zone_id: str, path: str | Path = REGISTER) -> tuple[dict[str, Any], ...]:
    """Return evidence with its status intact, never promote a rumor to truth."""
    get_zone(zone_id, path)
    return tuple(claim for claim in load_register(path)["claims"] if zone_id in claim["zone_ids"])


def zone_lookup_by_category(category: str, path: str | Path = REGISTER) -> tuple[dict[str, Any], ...]:
    if category not in ZONE_CATEGORIES:
        raise HelsinkiCanonError(f"unknown zone category: {category}")
    return tuple(zone for zone in load_register(path)["zones"] if zone["category"] == category)
