"""Deterministic NPC autonomy in the integrated social graph."""

from pathlib import Path

from src.game import GameState, plan_npc_action


ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_narkkari.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1.json"


def make_state(seed: int = 42) -> GameState:
    state = GameState.from_files(CHARACTER, SCENARIO, seed=seed)
    state.start()
    return state


def test_lotta_acts_from_mood_goal_and_existing_relationships():
    state = make_state()
    action = plan_npc_action(state.social, "lotta_kallio")

    assert action is not None
    assert action.target == "romppainen"
    assert action.dimension == "trust"
    assert action.delta == 1
    assert action.mood == "alarmed"
    assert "kadonnut partnerinsa" in action.goal


def test_npc_turn_changes_graph_and_records_auditable_memories():
    state = make_state()
    old_turn = state.social.turn

    actions = state.perform_npc_turn(max_actions=3)

    assert state.social.turn == old_turn + 1
    assert len(actions) == 3
    assert all(action.actor != "romppainen" for action in actions)
    changes = state.social.recent_changes(3)
    assert all(change["reason"].startswith("NPC autonomy:") for change in changes)
    for action in actions:
        newest = state.social.memories(action.actor, limit=1)[0]
        assert "npc_autonomy" in newest["tags"]
        assert newest["scene"] == state.rpg.scene.id
        assert action.target in state.social.graph


def test_npc_turn_is_deterministic_for_equivalent_states():
    first = make_state(seed=7)
    second = make_state(seed=7)

    first_actions = first.perform_npc_turn(max_actions=4)
    second_actions = second.perform_npc_turn(max_actions=4)

    assert first_actions == second_actions
    assert first.social.to_dict() == second.social.to_dict()


def test_zero_action_turn_does_not_advance_time():
    state = make_state()
    before = state.social.to_dict()

    assert state.perform_npc_turn(max_actions=0) == []
    assert state.social.to_dict() == before
