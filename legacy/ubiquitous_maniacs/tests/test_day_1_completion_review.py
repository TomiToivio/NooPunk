from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.rpg import RPGSession, load_character, load_scenario, scenario_from_dict


ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_day_1.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"


def session(die=lambda: 0) -> RPGSession:
    return RPGSession(load_character(CHARACTER), load_scenario(SCENARIO), fate_die=die)


def play(game: RPGSession, choices: list[str]) -> None:
    for choice in choices:
        assert choice in {item.id for item in game.available_interactions()}
        game.perform_interaction(choice)


def test_complete_route_persists_therapy_clue_and_relationship_state() -> None:
    game = session()
    play(game, [
        "ask_android", "help_ingrid", "ask_side_effects", "shared_appointment",
        "clear_route", "stay_with_ingrid", "inspect_batch", "answer_signal",
    ])

    assert game.is_complete
    assert game.scene.id == "d1_complete"
    assert game.state.campaign_flags["day_1_complete"] is True
    assert "entangled_assemblage" in game.state.campaign_flags
    assert game.state.known_information
    assert game.state.relationships["ingrid_falk"] > 0
    assert any(event.type == "relationship_changed" for event in game.events)


def test_nondefault_route_and_failed_checks_still_reach_safe_endpoint() -> None:
    game = session(die=lambda: -1)
    game.character.skills.clear()
    game.character.aspects.clear()
    game.character.tags.clear()
    play(game, [
        "ask_free_pills", "flirt_badly", "make_ingrid_laugh", "follow_mantid",
        "question_memory", "stay_with_ingrid", "steal_pills", "embrace_cop",
    ])

    assert game.is_complete
    assert game.available_interactions() == []
    assert game.state.campaign_flags["day_2_persona"] == "kiimainen_poliisi"
    assert game.state.relationships["ingrid_falk"] < 0


def test_loader_rejects_missing_day_1_transition() -> None:
    data = json.loads(SCENARIO.read_text(encoding="utf-8"))
    data["scenes"][0]["interactions"][0]["outcomes"]["success"]["next_scene"] = "missing"
    with pytest.raises(ValueError, match="Unknown next scene"):
        scenario_from_dict(data)


def test_post_session_debrief_closes_source_script_plot_hole() -> None:
    scene = load_scenario(SCENARIO).scenes["d1_ufab_heist"]
    assert {"Dr. Yuki Tanaka", "Dr. Søren Pilgrim", "C.G. Jung"} <= set(scene.participants)
    assert "jälkihaastatteluun" in scene.description
    assert "avoimen lääkekaapin" in scene.description
    assert "Uppsalan toimivan opetussairaalan" in scene.description
    assert "aktiivisen nanokaranteenin" in scene.description
    assert "milloin The Fall päättyi" in scene.description


def test_80mg_is_never_presented_as_standalone_therapy() -> None:
    game = session()
    play(game, [
        "ask_android", "help_ingrid", "ask_side_effects", "shared_appointment",
        "clear_route", "stay_with_ingrid", "inspect_batch",
    ])

    assert "ufab_80mg_is_prep_not_treatment" in game.state.known_information
    assert "uncontrolled_80mg_strengthens_pathological_attractors" in game.state.known_information


def test_kallio_contact_failure_remains_an_afterimage_on_day_1() -> None:
    game = session()
    play(game, [
        "ask_android", "help_ingrid", "ask_side_effects", "shared_appointment",
        "clear_route", "stay_with_ingrid", "inspect_batch", "answer_signal",
    ])

    assert game.state.campaign_flags["kallio_checkin_afterimage"] is True
    assert "kallio_checkin_suppressed" in game.character.tags


def test_loader_rejects_duplicate_ids_before_they_hide_content() -> None:
    data = json.loads(SCENARIO.read_text(encoding="utf-8"))
    data["scenes"].append(dict(data["scenes"][0]))
    with pytest.raises(ValueError, match="Duplicate scene id"):
        scenario_from_dict(data)

    data = json.loads(SCENARIO.read_text(encoding="utf-8"))
    duplicate = dict(data["scenes"][0]["interactions"][0])
    data["scenes"][1]["interactions"].append(duplicate)
    with pytest.raises(ValueError, match="scenario-wide unique"):
        scenario_from_dict(data)
