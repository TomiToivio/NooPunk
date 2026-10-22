"""Loader-validointi eksplisiittisille ``npc_memory``-tapahtumille.

Koodikatselmoinnin P2-korjaus teki relationship-tapahtumista
fail-fast-vauhtisia; samaa suojaa ei aiemmin ollut npc_memory-tapahtumille,
jotka kaatuivat vasta ajonaikaisesti _record_npc_memoriesissä osittain
mutatoidun tilan jälkeen. Nämä testit varmistavat, että loader hylkää
virheelliset payloadit ennen pelin alkua.
"""

from __future__ import annotations

import pytest

from src.rpg import scenario_from_dict


def _scenario_with_event(payload: dict, event_type: str = "npc_memory") -> dict:
    return {
        "id": "memory_event",
        "title": "Memory event",
        "entry_scene": "room",
        "scenes": [
            {
                "id": "room",
                "title": "Room",
                "description": "A memory event waits here.",
                "location": "Test Annex",
                "interactions": [
                    {
                        "id": "trigger",
                        "label": "Trigger",
                        "outcome": {
                            "text": "A memory forms.",
                            "events": [{"type": event_type, "payload": payload}],
                        },
                    }
                ],
            }
        ],
    }


def test_loader_accepts_well_formed_npc_memory_event() -> None:
    scenario = scenario_from_dict(_scenario_with_event({
        "target": "elin_dahl",
        "summary": "Dahl noted the patient's hesitation.",
        "valence": -1,
        "tags": ["diagnostic", "humor"],
    }))
    assert "room" in scenario.scenes


def test_loader_rejects_npc_memory_without_target() -> None:
    with pytest.raises(ValueError, match="Invalid npc_memory target"):
        scenario_from_dict(_scenario_with_event({
            "target": "   ",
            "summary": "Something happened.",
        }))


def test_loader_rejects_npc_memory_without_summary() -> None:
    with pytest.raises(ValueError, match="Invalid npc_memory summary"):
        scenario_from_dict(_scenario_with_event({
            "target": "elin_dahl",
            "summary": "",
        }))


def test_loader_rejects_npc_memory_with_non_integer_valence() -> None:
    with pytest.raises(ValueError, match="Invalid npc_memory valence"):
        scenario_from_dict(_scenario_with_event({
            "target": "elin_dahl",
            "summary": "Something happened.",
            "valence": True,
        }))


def test_loader_rejects_npc_memory_with_non_list_tags() -> None:
    with pytest.raises(ValueError, match="Invalid npc_memory tags"):
        scenario_from_dict(_scenario_with_event({
            "target": "elin_dahl",
            "summary": "Something happened.",
            "tags": "diagnostic",
        }))


def test_loader_rejects_npc_memory_with_non_string_tag() -> None:
    with pytest.raises(ValueError, match="Invalid npc_memory tags"):
        scenario_from_dict(_scenario_with_event({
            "target": "elin_dahl",
            "summary": "Something happened.",
            "tags": ["diagnostic", 3],
        }))