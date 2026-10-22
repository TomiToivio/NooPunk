from __future__ import annotations

from pathlib import Path

import pytest

from src.rpg import RPGSession, ResultTier, load_character, load_scenario

ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_narkkari.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1.json"


def session(die=lambda: 0) -> RPGSession:
    return RPGSession(load_character(CHARACTER), load_scenario(SCENARIO), fate_die=die)


# ── Character loads ──────────────────────────────────────────────


def test_romppainen_narkkari_loads() -> None:
    character = load_character(CHARACTER)
    assert character.name == "Sven-Olof Romppainen"
    assert character.attributes["Charisma"] == 2
    assert character.skills["Deceive"] == 3
    assert "UFAB Hunger" in character.aspects
    assert "narkkari_persona" in character.tags
    assert "disoriented" in character.conditions


# ── Scenario loads ───────────────────────────────────────────────


def test_day_1_scenario_loads() -> None:
    scenario = load_scenario(SCENARIO)
    assert scenario.id == "day_1"
    assert scenario.entry_scene == "d1_arrival"
    assert len(scenario.scenes) >= 10


def test_day_1_has_no_broken_scene_references() -> None:
    scenario = load_scenario(SCENARIO)
    all_scene_ids = set(scenario.scenes.keys())
    for scene in scenario.scenes.values():
        for interaction in scene.interactions.values():
            if interaction.automatic_outcome and interaction.automatic_outcome.next_scene:
                assert interaction.automatic_outcome.next_scene in all_scene_ids, (
                    f"Broken ref in {scene.id}.{interaction.id} -> {interaction.automatic_outcome.next_scene}"
                )
            for outcome in interaction.outcomes.values():
                if outcome.next_scene:
                    assert outcome.next_scene in all_scene_ids, (
                        f"Broken ref in {scene.id}.{interaction.id} -> {outcome.next_scene}"
                    )


# ── Happy path (cooperative, die=0) ─────────────────────────────


HAPPY_PATH = [
    "check_forms",
    "ask_android",
    "ask_virus",
    "accept_plainly",
    "take_forms",
    "say_hi_ingrid",
    "ingrid_small_talk",
    "go_to_lecture",
    "ask_about_ufab",
    "take_ufab",
    "watch_news",
    "follow_ingrid",
    "lotta_check",
    "help_elsa",
    "watch_horror",
    "wake_up_therapy",
    "tell_truth",
    "explore_room",
    "tell_agi_mantid",
    "investigate_ufab",
    "true_self_moment",
    "review_day",
    "think_ingrid",
    "just_sleep",
    "kiimainen_poliisi",
    "end_day_1",
]


def test_happy_path_completes_day_1() -> None:
    game = session()
    for step in HAPPY_PATH:
        available = {i.id for i in game.available_interactions()}
        assert step in available, f"{step} not available at {game.scene.id}/{game.state.current_dialogue}"
        game.perform_interaction(step)
    assert game.scene.id == "DAY_2_NOT_IMPLEMENTED"
    assert game.state.campaign_flags["day_1_complete"] is True


# ── Alternate path (failure die, different choices) ──────────────


ALTERNATE_PATH = [
    "craving",
    "check_forms",
    "ask_android",
    "inspect_device",
    "ask_why",
    "take_forms",
    "stare_ingrid",
    "ingrid_ufab",
    "go_to_lecture",
    "ask_joke",
    "take_ufab",
    "smoke_with_ingrid",
    "freeze_panic",
    "lotta_panic",
    "basilisk_check",
    "try_board",
    "wake_up_therapy",
    "tell_nothing",
    "wait_alone",
    "dont_trust_agi",
    "refuse_ufab",
    "stay_narkkari",
    "just_sleep",
    "resist_dream",
    "end_day_1",
]


def test_alternate_path_completes_day_1() -> None:
    game = session(die=lambda: -1)
    for step in ALTERNATE_PATH:
        available = {i.id for i in game.available_interactions()}
        assert step in available, f"{step} not available at {game.scene.id}/{game.state.current_dialogue}"
        game.perform_interaction(step)
    assert game.scene.id == "DAY_2_NOT_IMPLEMENTED"
    assert game.state.campaign_flags["day_1_complete"] is True


# ── State persistence ────────────────────────────────────────────


def test_relationship_changes_persist() -> None:
    game = session()
    game.perform_interaction("check_forms")
    game.perform_interaction("ask_android")
    rel_events = [e for e in game.events if e.type == "relationship_change_requested"]
    assert len(rel_events) >= 1
    # Continue further and verify events are not lost
    game.perform_interaction("ask_virus")
    game.perform_interaction("accept_plainly")
    game.perform_interaction("take_forms")
    rel_events_after = [e for e in game.events if e.type == "relationship_change_requested"]
    assert len(rel_events_after) > len(rel_events)
    assert game.state.relationships
    assert any(event.type == "relationship_changed" for event in game.events)


def test_clue_discovery_persists() -> None:
    game = session()
    game.perform_interaction("check_forms")  # -> d1_reception
    # Complete reception
    game.perform_interaction("ask_android")
    game.perform_interaction("ask_virus")
    game.perform_interaction("accept_plainly")
    game.perform_interaction("take_forms")
    # known_information should contain intake-related info
    assert "enrolled_in_trial" in game.state.known_information
    # Continue to investigation scene and find UFAB evidence
    game.perform_interaction("say_hi_ingrid")
    game.perform_interaction("ingrid_small_talk")
    game.perform_interaction("go_to_lecture")
    game.perform_interaction("ask_about_ufab")
    game.perform_interaction("take_ufab")
    game.perform_interaction("watch_news")
    game.perform_interaction("follow_ingrid")
    game.perform_interaction("lotta_check")
    game.perform_interaction("help_elsa")
    game.perform_interaction("watch_horror")
    game.perform_interaction("wake_up_therapy")
    game.perform_interaction("tell_truth")
    game.perform_interaction("explore_room")
    game.perform_interaction("tell_agi_mantid")
    game.perform_interaction("investigate_ufab")
    # NHI evidence should be in known_information
    assert "ufab_nhi_warning" in game.state.known_information


def test_intake_therapy_flags_persist() -> None:
    game = session()
    game.perform_interaction("check_forms")
    game.perform_interaction("ask_android")
    game.perform_interaction("ask_virus")
    game.perform_interaction("accept_plainly")
    game.perform_interaction("take_forms")
    assert game.state.campaign_flags["intake_accepted"] is True
    # Continue to therapy
    game.perform_interaction("say_hi_ingrid")
    game.perform_interaction("ingrid_small_talk")
    game.perform_interaction("go_to_lecture")
    game.perform_interaction("ask_about_ufab")
    game.perform_interaction("take_ufab")
    game.perform_interaction("watch_news")
    game.perform_interaction("follow_ingrid")
    game.perform_interaction("lotta_check")
    game.perform_interaction("help_elsa")
    game.perform_interaction("watch_horror")
    game.perform_interaction("wake_up_therapy")
    assert game.state.campaign_flags["therapy_completed"] is True
    # Intake flag should still be there
    assert game.state.campaign_flags["intake_accepted"] is True


# ── Scene transitions ────────────────────────────────────────────


def test_day_1_reaches_day_2_placeholder() -> None:
    game = session()
    for step in HAPPY_PATH:
        game.perform_interaction(step)
    assert game.scene.id == "DAY_2_NOT_IMPLEMENTED"


def test_day_2_placeholder_is_a_safe_terminal() -> None:
    game = session()
    for step in HAPPY_PATH:
        game.perform_interaction(step)
    assert game.scene.id == "DAY_2_NOT_IMPLEMENTED"
    assert game.state.campaign_flags["day_1_complete"] is True
    # restart should be available so the player isn't trapped
    interactions = game.available_interactions()
    assert any(i.id == "restart" for i in interactions)


def test_day_2_restart_resets_progress_and_reopens_day_1() -> None:
    game = session()
    for step in HAPPY_PATH:
        game.perform_interaction(step)

    assert game.state.completed_interactions
    assert game.state.campaign_flags
    assert game.state.relationships

    game.perform_interaction("restart")

    assert game.scene.id == "d1_arrival"
    assert not game.is_complete
    assert game.state.completed_interactions == set()
    assert game.state.campaign_flags == {}
    assert game.state.relationships == {}
    assert game.state.known_information == set()
    assert {item.id for item in game.available_interactions()} == {"craving", "look_around", "check_forms"}
    assert [event.type for event in game.events] == ["session_restarted", "interaction_completed"]


def test_all_scenes_dialogue_and_interactions_are_structurally_reachable() -> None:
    scenario = load_scenario(SCENARIO)
    reachable = {scenario.entry_scene}
    while True:
        discovered = set(reachable)
        for scene_id in reachable:
            for interaction in scenario.scenes[scene_id].interactions.values():
                outcomes = list(interaction.outcomes.values())
                if interaction.automatic_outcome is not None:
                    outcomes.append(interaction.automatic_outcome)
                discovered.update(outcome.next_scene for outcome in outcomes if outcome.next_scene)
        if discovered == reachable:
            break
        reachable = discovered

    assert reachable == set(scenario.scenes)
    for scene in scenario.scenes.values():
        if not scene.opening_dialogue:
            continue
        referenced = {
            choice.interaction_id
            for node in scene.dialogue.values()
            for choice in node.choices
        }
        assert referenced == set(scene.interactions), f"Unreachable interaction in {scene.id}"


# ── Skill checks work ────────────────────────────────────────────


def test_check_forms_uses_notice_skill() -> None:
    game = session(die=lambda: 0)
    result = game.perform_interaction("check_forms")
    assert result.check is not None
    assert result.check.tier == ResultTier.SUCCESS  # Awareness(2)+Notice(2)+0 vs 3 = margin 1


def test_failure_die_produces_failure_outcome() -> None:
    game = session(die=lambda: -1)
    result = game.perform_interaction("check_forms")
    assert result.check is not None
    # Awareness(2)+Notice(2)+(-4) = 0 vs 3 -> margin -3 -> FAILURE
    assert result.check.tier in (ResultTier.FAILURE, ResultTier.COSTLY_SUCCESS)
