from pathlib import Path

import pytest

from src.rpg import RPGSession, load_character, load_scenario, session_from_dict, session_to_dict


ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_day_1.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"


def make_session(seed: int = 1601) -> RPGSession:
    return RPGSession(load_character(CHARACTER), load_scenario(SCENARIO), seed=seed)


def test_save_round_trip_preserves_shared_day_1_state() -> None:
    game = make_session()
    game.perform_interaction("ask_android")
    game.perform_interaction("help_ingrid")

    restored = session_from_dict(
        session_to_dict(game), load_character(CHARACTER), load_scenario(SCENARIO)
    )

    assert restored.state.current_scene == game.state.current_scene
    assert restored.state.relationships == game.state.relationships
    assert restored.state.graph_effects == game.state.graph_effects
    assert restored.state.known_information == game.state.known_information
    assert restored.events == game.events


def test_loaded_seed_continues_the_same_fate_sequence() -> None:
    uninterrupted = make_session(42)
    uninterrupted.perform_interaction("ask_android")
    uninterrupted.perform_interaction("help_ingrid")
    save = session_to_dict(uninterrupted)

    restored = session_from_dict(save, load_character(CHARACTER), load_scenario(SCENARIO))
    expected = uninterrupted.perform_interaction("ask_side_effects")
    actual = restored.perform_interaction("ask_side_effects")

    assert actual.check is not None and expected.check is not None
    assert actual.check.dice == expected.check.dice
    assert actual.check.tier == expected.check.tier


def test_seeded_sessions_are_reproducible() -> None:
    game_a = make_session(99)
    game_b = make_session(99)
    game_a.perform_interaction("ask_android")
    game_b.perform_interaction("ask_android")
    first = game_a.perform_interaction("help_ingrid")
    second = game_b.perform_interaction("help_ingrid")

    assert first.check is not None and second.check is not None
    assert first.check.dice == second.check.dice


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda save: save["state"].update(current_character="intruder"), "state character"),
        (lambda save: save.update(random_draws=1_000_001), "random_draws"),
        (lambda save: save.update(seed="not-an-integer"), "seed"),
        (lambda save: save.update(state=[]), "state must be"),
    ],
)
def test_loader_rejects_tampered_or_pathological_save_data(mutate, message: str) -> None:
    save = session_to_dict(make_session())
    mutate(save)

    with pytest.raises(ValueError, match=message):
        session_from_dict(save, load_character(CHARACTER), load_scenario(SCENARIO))


def test_rejected_save_does_not_mutate_supplied_character() -> None:
    save = session_to_dict(make_session())
    save["character"]["tags"] = ["injected_by_corrupt_save"]
    save["state"]["current_scene"] = "missing_scene"
    character = load_character(CHARACTER)
    original_tags = set(character.tags)

    with pytest.raises(ValueError, match="unknown scene"):
        session_from_dict(save, character, load_scenario(SCENARIO))

    assert character.tags == original_tags


def test_corrupt_graph_effects_do_not_mutate_character() -> None:
    """If graph_effects contain invalid data, character must not be mutated."""
    save = session_to_dict(make_session())
    save["character"]["tags"] = ["injected_by_corrupt_save"]
    save["state"]["graph_effects"] = [{"domain": "noetic", "operation": "bogus"}]
    character = load_character(CHARACTER)
    original_tags = set(character.tags)

    with pytest.raises((ValueError, TypeError)):
        session_from_dict(save, character, load_scenario(SCENARIO))

    assert character.tags == original_tags


def test_corrupt_events_do_not_mutate_character() -> None:
    """If events contain invalid data, character must not be mutated."""
    save = session_to_dict(make_session())
    save["character"]["tags"] = ["injected_by_corrupt_save"]
    save["events"] = [{"missing_type": True}]
    character = load_character(CHARACTER)
    original_tags = set(character.tags)

    with pytest.raises((ValueError, KeyError, TypeError)):
        session_from_dict(save, character, load_scenario(SCENARIO))

    assert character.tags == original_tags
