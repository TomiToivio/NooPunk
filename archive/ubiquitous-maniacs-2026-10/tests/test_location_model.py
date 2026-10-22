"""Tests for the Location entity and its loader (Helsinki campaign frame, Track 4)."""

from __future__ import annotations

import pytest

from src.rpg.loaders import _locations, scenario_from_dict
from src.rpg.models import Location


# ── Location dataclass ────────────────────────────────────────────────────


def test_location_defaults_minimal() -> None:
    loc = Location(id="kumpula", name="Kumpula")
    assert loc.id == "kumpula"
    assert loc.name == "Kumpula"
    assert loc.description == ""
    assert loc.district == ""
    assert loc.npcs == []
    assert loc.threads == []


def test_location_is_frozen() -> None:
    loc = Location(id="x", name="X", npcs=["a"])
    with pytest.raises(Exception):
        loc.id = "y"  # type: ignore[misc]
    assert loc.npcs == ["a"]


# ── _locations loader ─────────────────────────────────────────────────────


def test_locations_empty_list_yields_empty_dict() -> None:
    assert _locations([]) == {}


def test_locations_parses_full_entries() -> None:
    data = [
        {
            "id": "kumpula",
            "name": "Kumpula Science Campus",
            "description": "Physics and quantum computing.",
            "district": "Kumpula",
            "npcs": ["reikka_lindqvist", "mikko_halonen"],
            "threads": ["signal_heikkinen"],
        },
        {
            "id": "kallio",
            "name": "Kallio",
            "description": "Bohemian district.",
        },
    ]
    locations = _locations(data)
    assert set(locations) == {"kumpula", "kallio"}
    assert locations["kumpula"].npcs == ["reikka_lindqvist", "mikko_halonen"]
    assert locations["kumpula"].threads == ["signal_heikkinen"]
    assert locations["kallio"].npcs == []
    assert locations["kallio"].threads == []


def test_locations_rejects_duplicate_id() -> None:
    with pytest.raises(ValueError, match="Duplicate location id"):
        _locations([{"id": "a", "name": "A"}, {"id": "a", "name": "Again"}])


def test_locations_rejects_missing_or_blank_id() -> None:
    with pytest.raises(ValueError, match="Invalid location id"):
        _locations([{"name": "NoId"}])
    with pytest.raises(ValueError, match="Invalid location id"):
        _locations([{"id": "  ", "name": "Blank"}])


def test_locations_rejects_missing_or_blank_name() -> None:
    with pytest.raises(ValueError, match="Invalid location name"):
        _locations([{"id": "a", "name": ""}])


def test_scenario_locations_load_via_scenario_from_dict() -> None:
    scenario = scenario_from_dict(
        {
            "id": "loc_test",
            "title": "Location test",
            "entry_scene": "s1",
            "scenes": [
                {"id": "s1", "title": "S1", "description": "d", "location": "kumpula",
                 "participants": [], "interactions": [
                     {"id": "auto", "label": "Auto", "outcome": {"text": "ok"}}]}
            ],
            "locations": [{"id": "kumpula", "name": "Kumpula Science Campus"}],
        }
    )
    assert "kumpula" in scenario.locations
    assert scenario.locations["kumpula"].name == "Kumpula Science Campus"