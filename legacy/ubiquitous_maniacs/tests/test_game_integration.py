"""Tests for the integrated game state module."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.rpg import GraphEffect
from src.game import GameState, MultiDimensionalSocialGraph, NPCMemory
from src.game.state import HackingState


ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_narkkari.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1.json"
DAY_1_CHARACTER = ROOT / "data/rpg/characters/romppainen_day_1.md"
DAY_1_SCENARIO = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"
DAY_2_SCENARIO = ROOT / "data/rpg/scenarios/day_2_kiimaiset_poliisit.json"


def make_state(seed: int = 42) -> GameState:
    state = GameState.from_files(CHARACTER, SCENARIO, seed=seed)
    state.start()
    return state


# ── MultiDimensionalSocialGraph ────────────────────────────────


def test_social_graph_creates_with_characters():
    graph = MultiDimensionalSocialGraph()
    graph.add_character("a", "Alice", "patient", ["survive"], "calm")
    graph.add_character("b", "Bob", "staff", ["help"], "neutral")
    assert graph.graph.number_of_nodes() == 2
    assert graph.graph.nodes["a"]["name"] == "Alice"
    assert graph.graph.nodes["a"]["mood"] == "calm"
    assert graph.graph.nodes["a"]["goals"] == ["survive"]


def test_social_graph_sets_and_gets_relationship():
    graph = MultiDimensionalSocialGraph()
    graph.add_character("a", "Alice", "patient")
    graph.add_character("b", "Bob", "staff")
    graph.set_relationship("a", "b", {"trust": 10, "suspicion": -5})
    rel = graph.get_relationship("a", "b")
    assert rel.trust == 10
    assert rel.suspicion == -5
    assert rel.attraction == 0


def test_social_graph_changes_relationship():
    graph = MultiDimensionalSocialGraph()
    graph.add_character("a", "Alice", "patient")
    graph.add_character("b", "Bob", "staff")
    graph.set_relationship("a", "b", {"trust": 10})
    record = graph.change_relationship("a", "b", "trust", 5, "helped")
    assert record.delta == 5
    assert record.new_value == 15
    assert graph.get_relationship("a", "b").trust == 15
    assert len(graph.history) == 1


def test_social_graph_clamps_values():
    graph = MultiDimensionalSocialGraph()
    graph.add_character("a", "Alice", "patient")
    graph.add_character("b", "Bob", "staff")
    graph.set_relationship("a", "b", {"trust": 90})
    graph.change_relationship("a", "b", "trust", 50)
    assert graph.get_relationship("a", "b").trust == 100
    graph.change_relationship("a", "b", "trust", -200)
    assert graph.get_relationship("a", "b").trust == -100


def test_social_graph_hidden_edges():
    graph = MultiDimensionalSocialGraph()
    graph.add_character("a", "Alice", "patient")
    graph.add_character("b", "Bob", "staff")
    graph.set_relationship("a", "b", {"trust": 5}, hidden=True)
    assert graph.is_hidden("a", "b")
    rels = graph.visible_relationships(observer="a")
    assert len(rels) == 0
    rels_all = graph.visible_relationships()
    assert len(rels_all) == 1
    graph.reveal_edge("a", "b")
    assert not graph.is_hidden("a", "b")


def test_social_graph_recent_changes():
    graph = MultiDimensionalSocialGraph()
    graph.add_character("a", "Alice", "patient")
    graph.add_character("b", "Bob", "staff")
    graph.set_relationship("a", "b", {"trust": 0})
    graph.change_relationship("a", "b", "trust", 5)
    graph.change_relationship("a", "b", "familiarity", 3)
    changes = graph.recent_changes(2)
    assert len(changes) == 2
    assert changes[0]["dimension"] == "trust"
    assert changes[1]["dimension"] == "familiarity"


def test_social_graph_serialization():
    graph = MultiDimensionalSocialGraph()
    graph.add_character("a", "Alice", "patient", ["survive"], "calm")
    graph.add_character("b", "Bob", "staff")
    graph.set_relationship("a", "b", {"trust": 10, "fear": -3}, hidden=True)
    graph.change_relationship("a", "b", "trust", 5)

    data = graph.to_dict()
    restored = MultiDimensionalSocialGraph.from_dict(data)
    assert restored.graph.number_of_nodes() == 2
    assert restored.get_relationship("a", "b").trust == 15
    assert restored.is_hidden("a", "b")
    assert len(restored.history) == 1


def test_npc_memory_is_deduplicated_and_serialized():
    graph = MultiDimensionalSocialGraph()
    graph.add_character("npc", "NPC")
    memory = NPCMemory(
        1, "scene", "choice", "player", "Player kept the promise.", 2, ("promise",)
    )

    assert graph.remember("npc", memory)
    assert not graph.remember("npc", memory)
    restored = MultiDimensionalSocialGraph.from_dict(graph.to_dict())

    assert restored.memories("npc") == [memory.to_dict()]
    assert restored.to_dict() == graph.to_dict()


# ── GameState integration ───────────────────────────────────────


def test_game_state_initializes():
    state = make_state()
    assert state.rpg.scene.id == "d1_arrival"
    assert state.social.graph.number_of_nodes() == 8
    assert state.social.graph.number_of_edges() >= 10


def test_game_state_populates_default_cast():
    state = make_state()
    char_ids = set(state.social.graph.nodes)
    expected = {"romppainen", "ingrid_falk", "elin_dahl", "yuki_tanaka",
                "soren_pilgrim", "ufab_ragnarok", "irungu_wakini",
                "lotta_kallio"}
    assert expected <= char_ids


def test_game_state_hidden_relationships_exist():
    state = make_state()
    assert state.social.hidden_edge_count >= 2


def test_game_state_rpg_interaction_advances_social_turn():
    state = make_state()
    initial_turn = state.social.turn
    state.perform_rpg_interaction("check_forms")
    assert state.social.turn == initial_turn + 1


def test_game_state_hacking_unlocks_through_play():
    state = make_state()
    assert not state.hacking.available
    # check_forms -> strange_forms info -> hacking should unlock
    state.perform_rpg_interaction("check_forms")
    assert state.hacking.available


def test_new_day_1_unlocks_hacking_when_ufab_heist_begins():
    state = GameState.from_files(DAY_1_CHARACTER, DAY_1_SCENARIO, seed=42)
    state.start()

    for interaction_id in (
        "ask_android",
        "help_ingrid",
        "ask_side_effects",
        "shared_appointment",
        "clear_route",
    ):
        state.perform_rpg_interaction(interaction_id)

    assert state.rpg.scene.id == "d1_collision"
    assert not state.hacking.available

    state.perform_rpg_interaction("stay_with_ingrid")

    assert state.rpg.scene.id == "d1_ufab_heist"
    assert state.hacking.available


def test_game_state_hacking_state_from_play():
    state = make_state()
    # Play through to investigation scene
    steps = ["check_forms", "ask_android", "ask_virus", "accept_plainly",
             "take_forms", "say_hi_ingrid", "ingrid_small_talk", "go_to_lecture",
             "ask_about_ufab", "take_ufab", "watch_news", "follow_ingrid",
             "lotta_check", "help_elsa", "watch_horror", "wake_up_therapy",
             "tell_truth", "explore_room"]
    for step in steps:
        state.perform_rpg_interaction(step)
    assert state.rpg.scene.id == "d1_investigation"
    assert state.hacking.available


def test_game_state_hack_terminal_available_in_investigation():
    state = make_state()
    steps = ["check_forms", "ask_android", "ask_virus", "accept_plainly",
             "take_forms", "say_hi_ingrid", "ingrid_small_talk", "go_to_lecture",
             "ask_about_ufab", "take_ufab", "watch_news", "follow_ingrid",
             "lotta_check", "help_elsa", "watch_horror", "wake_up_therapy",
             "tell_truth", "explore_room"]
    for step in steps:
        state.perform_rpg_interaction(step)
    available_ids = {i.id for i in state.rpg.available_interactions()}
    assert "hack_terminal" in available_ids


def test_game_state_save_and_restore():
    state = make_state(seed=42)
    state.perform_rpg_interaction("check_forms")
    state.perform_rpg_interaction("ask_android")

    save_path = ROOT / "saves" / "test_save.json"
    save_path.parent.mkdir(exist_ok=True)
    state.save_to_file(save_path)

    restored = GameState.load_from_file(save_path, CHARACTER, SCENARIO)
    assert restored.rpg.scene.id == state.rpg.scene.id
    assert restored.rpg.state.conditions == state.rpg.state.conditions
    assert restored.social.graph.number_of_nodes() == state.social.graph.number_of_nodes()
    assert restored.hacking.available == state.hacking.available

    save_path.unlink()


def test_game_state_rejects_unknown_integrated_save_version():
    save = make_state(seed=42).to_save()
    save.version = 99

    with pytest.raises(ValueError, match="Unsupported integrated save version"):
        GameState.from_save(save, CHARACTER, SCENARIO)


def test_campaign_transition_preserves_cross_day_state_and_rng_position():
    state = GameState.from_files(DAY_1_CHARACTER, DAY_1_SCENARIO, seed=42)
    state.start()
    state.rpg.state.campaign_flags["day_1_choice"] = "escape_line"
    state.rpg.state.known_information.add("noetic_firewall")
    state.rpg.state.conditions.add("ontological_drift")
    state.rpg.state.relationships["ingrid_falk"] = 3
    state.rpg.restore_random_draws(8)
    social = state.social
    hacking = state.hacking

    state.transition_to_scenario(DAY_2_SCENARIO)

    assert state.rpg.scenario.id == "day_2_kiimaiset_poliisit"
    assert state.rpg.scene.id == "d2_helsinki_arrival"
    assert state.rpg.state.campaign_flags["day_1_choice"] == "escape_line"
    assert "noetic_firewall" in state.rpg.state.known_information
    assert "ontological_drift" in state.rpg.state.conditions
    assert state.rpg.state.relationships["ingrid_falk"] == 3
    assert state.rpg.random_draws == 8
    assert state.social is social
    assert state.hacking is hacking
    assert state.rpg.events[-1].type == "scenario_started"


def test_game_state_npc_state():
    state = make_state()
    ingrid = state.get_npc_state("ingrid_falk")
    assert ingrid["name"] == "Ingrid Falk"
    assert ingrid["mood"] == "grieving"
    # Goals are localized to Finnish (Romppainen's internal language).
    assert "Selviytyä Elsan kuolemasta" in ingrid["goals"]


def test_player_relationships_visible_after_id_mapping():
    """Regression: play.py used RPG char ID as observer, but social graph
    uses mapped ID ('romppainen'). Player's own relationships were invisible."""
    state = make_state()
    # Play to generate relationship changes
    state.perform_rpg_interaction("check_forms")
    state.perform_rpg_interaction("ask_android")
    # The mapped ID should see relationships; the raw RPG ID should not
    mapped_id = state._id_map.get(state.rpg.character.id, state.rpg.character.id)
    visible = state.social.visible_relationships(mapped_id)
    own_rels = [r for r in visible if r["source"] == mapped_id]
    assert len(own_rels) > 0, "Player should have visible relationships after play"


def test_relationship_choice_becomes_npc_memory_and_survives_save_round_trip():
    state = make_state(seed=42)
    state.perform_rpg_interaction("check_forms")
    state.perform_rpg_interaction("ask_android")

    memories = state.social.memories("elin_dahl")
    assert len(memories) == 1
    assert memories[0]["interaction"] == "ask_android"
    assert memories[0]["summary"] == "'Tutkitteko, olenko kone?'"
    assert memories[0]["valence"] == 1
    assert "player_choice" in memories[0]["tags"]

    restored = GameState.from_save(state.to_save(), CHARACTER, SCENARIO)
    assert restored.social.memories("elin_dahl") == memories


def test_explicit_npc_memory_overrides_automatic_relationship_summary():
    state = make_state(seed=42)
    state.perform_rpg_interaction("check_forms")
    interaction = state.rpg.scene.interactions["ask_android"]
    interaction.automatic_outcome.events.append({
        "type": "npc_memory",
        "payload": {
            "target": "elin_dahl",
            "summary": "Dahl noticed that the joke concealed a diagnostic question.",
            "valence": 2,
            "tags": ["diagnostic", "humor"],
        },
    })

    state.perform_rpg_interaction("ask_android")

    memories = state.social.memories("elin_dahl")
    assert len(memories) == 1
    assert memories[0]["summary"].startswith("Dahl noticed")
    assert memories[0]["tags"] == ["diagnostic", "humor"]


def test_sync_social_consumes_only_social_effects() -> None:
    state = make_state()
    state.rpg.state.graph_effects = [
        GraphEffect("social", "adjust_edge", "romppainen_narkkari", "ingrid_falk", "trust", 2),
        GraphEffect("cyber", "adjust_edge", "node_a", "node_b", "signal", 1),
    ]

    before = state.social.get_relationship("romppainen", "ingrid_falk").trust
    state._sync_social_from_rpg()

    after = state.social.get_relationship("romppainen", "ingrid_falk").trust
    assert after == before + 2
    assert len(state.rpg.state.graph_effects) == 1
    assert state.rpg.state.graph_effects[0].domain == "cyber"


def test_hacking_state_serialization():
    hs = HackingState(available=True, attempts=3, successes=2, alert_level=2)
    hs.discovered_nodes.add("clinical_terminal")
    data = hs.to_dict()
    restored = HackingState.from_dict(data)
    assert restored.available
    assert restored.attempts == 3
    assert restored.successes == 2
    assert restored.alert_level == 2
    assert "clinical_terminal" in restored.discovered_nodes


def test_hack_terminal_critical_success_reveals_information():
    state = make_state(seed=42)
    steps = ["check_forms", "ask_android", "ask_virus", "accept_plainly",
             "take_forms", "say_hi_ingrid", "ingrid_small_talk", "go_to_lecture",
             "ask_about_ufab", "take_ufab", "watch_news", "follow_ingrid",
             "lotta_check", "help_elsa", "watch_horror", "wake_up_therapy",
             "tell_truth", "explore_room"]
    for step in steps:
        state.perform_rpg_interaction(step)
    # Use deterministic die that gives high results
    # Intelligence(2) + Infosec(1) + roll vs difficulty 4
    # Need margin >= 3 for critical success, so roll >= 4
    die_values = iter([1, 1, 1, 1])  # 4dF = +4
    state.rpg._fate_die = lambda: next(die_values)
    result = state.perform_rpg_interaction("hack_terminal")
    assert result.check is not None
    assert "hacking_can_network" in state.rpg.state.known_information
    assert "hacking_romppainen_ingrid_link" in state.rpg.state.known_information
