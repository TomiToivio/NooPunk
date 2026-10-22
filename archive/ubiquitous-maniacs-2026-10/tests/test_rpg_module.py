from __future__ import annotations

from pathlib import Path

import pytest

from src.rpg import (
    RPGSession,
    ResultTier,
    character_from_dict,
    load_character,
    load_scenario,
    scenario_from_dict,
)


ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/demo_operator.md"
SCENARIO = ROOT / "data/rpg/scenarios/neutral_terminal.json"


def session(die=lambda: 0) -> RPGSession:
    return RPGSession(load_character(CHARACTER), load_scenario(SCENARIO), fate_die=die)


def test_character_loads_from_shared_markdown_model() -> None:
    character = load_character(CHARACTER)
    assert character.name == "Demo Operator"
    assert character.attributes["Cybernetics"] == 1
    assert "Curiosity Over Caution" in character.aspects
    assert character.psyche["status"] == "present"


def test_scene_and_interactions_load() -> None:
    game = session()
    assert game.scene.id == "quiet_room"
    assert {item.id for item in game.available_interactions()} == {"inspect_signal", "name_the_pattern", "leave"}


def test_condition_can_block_interaction() -> None:
    game = session()
    game.state.conditions.add("anxious")
    assert "leave" not in {item.id for item in game.available_interactions()}


def test_aspect_can_unlock_interaction() -> None:
    game = session()
    assert "name_the_pattern" in {item.id for item in game.available_interactions()}
    game.character.aspects.clear()
    assert "name_the_pattern" not in {item.id for item in game.available_interactions()}


def test_skill_check_and_success_outcome_update_state_and_transition() -> None:
    game = session()
    result = game.perform_interaction("inspect_signal")
    assert result.check is not None
    assert result.check.tier == ResultTier.SUCCESS
    assert "four_pulse_pattern" in game.state.known_information
    assert game.state.current_scene == "debrief"
    assert {event.type for event in game.events} >= {"skill_check_completed", "interaction_completed", "scene_completed"}


def test_failure_outcome_still_advances_story() -> None:
    game = session(die=lambda: -1)
    game.character.tags.clear()
    game.character.aspects.clear()
    game.character.skills.clear()
    result = game.perform_interaction("inspect_signal")
    assert result.check is not None
    assert result.check.tier == ResultTier.CATASTROPHIC_FAILURE
    assert "anxious" in game.state.conditions
    assert "Observed by the annex" in game.state.consequences
    assert game.state.current_scene == "debrief"


def test_event_boundary_emits_requests_without_integrating_modules() -> None:
    game = session()
    game.perform_interaction("leave")
    game.perform_interaction("request_followup")
    types = [event.type for event in game.events]
    assert "hacking_encounter_requested" in types
    assert "relationship_change_requested" in types


def test_completed_nonrepeatable_interaction_is_removed() -> None:
    game = session()
    game.perform_interaction("leave")
    game.perform_interaction("request_followup")
    assert game.available_interactions() == []
    with pytest.raises(ValueError, match="not available"):
        game.perform_interaction("request_followup")


def test_terminal_scene_with_epilogue_interaction_completes_after_acknowledgement() -> None:
    data = {
        "id": "epilogue_test",
        "title": "Epilogue test",
        "entry_scene": "epilogue",
        "terminal_scenes": ["epilogue"],
        "scenes": [{
            "id": "epilogue",
            "title": "Epilogue",
            "description": "One final choice remains.",
            "location": "Test Annex",
            "interactions": [{
                "id": "finish",
                "label": "Finish",
                "outcome": {"set_flags": {"finished": True}},
            }],
        }],
    }
    game = RPGSession(load_character(CHARACTER), scenario_from_dict(data))

    assert not game.is_complete
    game.perform_interaction("finish")
    assert game.is_complete
    assert game.state.campaign_flags["finished"] is True


def test_dialogue_node_without_choices_does_not_leak_scene_interactions() -> None:
    data = {
        "id": "closed_dialogue",
        "title": "Closed dialogue",
        "entry_scene": "room",
        "scenes": [{
            "id": "room",
            "title": "Room",
            "description": "The conversation has ended.",
            "location": "Test Annex",
            "opening_dialogue": "closed",
            "dialogue": [{"id": "closed", "speaker": "Vale", "text": "Enough.", "choices": []}],
            "interactions": [{"id": "hidden", "label": "Hidden", "outcome": {"text": "Should stay hidden."}}],
        }],
    }
    game = RPGSession(load_character(CHARACTER), scenario_from_dict(data))

    assert game.available_interactions() == []


def test_loader_rejects_malformed_integration_event() -> None:
    data = {
        "id": "bad_event",
        "title": "Bad event",
        "entry_scene": "room",
        "scenes": [{
            "id": "room",
            "title": "Room",
            "description": "A malformed request waits here.",
            "location": "Test Annex",
            "interactions": [{
                "id": "trigger",
                "label": "Trigger",
                "outcome": {
                    "text": "Malformed.",
                    "events": [{"type": "relationship_change_requested", "payload": {"target": "vale", "delta": True}}],
                },
            }],
        }],
    }

    with pytest.raises(ValueError, match="Invalid relationship delta"):
        scenario_from_dict(data)


def test_character_loader_rejects_out_of_range_rating_and_unknown_skill() -> None:
    source = load_character(CHARACTER)
    data = {
        "id": source.id,
        "name": source.name,
        "attributes": dict(source.attributes),
        "skills": dict(source.skills),
    }
    data["attributes"]["Body"] = 5
    with pytest.raises(ValueError, match="Attribute ratings"):
        character_from_dict(data)

    data["attributes"]["Body"] = 1
    data["skills"]["Notise"] = 1
    with pytest.raises(ValueError, match="Unknown skills"):
        character_from_dict(data)


def test_scenario_loader_rejects_unknown_check_identifier() -> None:
    data = {
        "id": "bad_check",
        "title": "Bad check",
        "entry_scene": "room",
        "scenes": [{
            "id": "room",
            "title": "Room",
            "description": "A typo waits here.",
            "location": "Test Annex",
            "interactions": [{
                "id": "inspect",
                "label": "Inspect",
                "check": {"attribute": "Awereness", "skill": "Notice", "difficulty": 1},
                "outcomes": {"success": {"text": "Impossible to load."}},
            }],
        }],
    }

    with pytest.raises(ValueError, match="Unknown attribute"):
        scenario_from_dict(data)
