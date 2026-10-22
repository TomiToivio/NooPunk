"""End-to-end coverage for the release campaign boundary."""

from pathlib import Path

from src.game import GameState


ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_day_1.md"
DAY_1 = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"
DAY_2 = ROOT / "data/rpg/scenarios/day_2_kiimaiset_poliisit.json"


def play(state: GameState, choices: list[str]) -> None:
    for choice in choices:
        available = {item.id for item in state.rpg.available_interactions()}
        assert choice in available, f"{choice} unavailable in {state.rpg.scene.id}: {available}"
        state.perform_rpg_interaction(choice)


def test_two_day_campaign_is_playable_and_reloadable(tmp_path) -> None:
    state = GameState.from_files(CHARACTER, DAY_1, seed=1601)
    state.start()
    play(state, [
        "ask_android",
        "help_ingrid",
        "ask_side_effects",
        "shared_appointment",
        "clear_route",
        "stay_with_ingrid",
        "inspect_batch",
        "answer_signal",
    ])

    assert state.rpg.is_complete
    day_1_relationship = state.rpg.state.relationships["ingrid_falk"]
    state.transition_to_scenario(DAY_2)
    play(state, [
        "d2_check_mirror",
        "d2_greet_lotta",
        "d2_honest",
        "d2_flee_trauma",
        "d2_end_day",
    ])

    assert state.rpg.is_complete
    assert state.rpg.state.campaign_flags["day_1_complete"] is True
    assert state.rpg.state.campaign_flags["day_2_complete"] is True
    assert state.rpg.state.campaign_flags["day_3_available"] is True
    assert state.rpg.state.relationships["ingrid_falk"] > day_1_relationship
    assert any(event.type == "scenario_started" for event in state.rpg.events)

    save_path = tmp_path / "completed_campaign.json"
    state.save_to_file(save_path)
    restored = GameState.load_from_file(save_path, CHARACTER, DAY_2)

    assert restored.rpg.is_complete
    assert restored.rpg.state.campaign_flags == state.rpg.state.campaign_flags
    assert restored.social.to_dict() == state.social.to_dict()
