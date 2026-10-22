"""Testit Elin Dahlin testihuonekohtaukselle."""

from __future__ import annotations

import random

from src.interaction import EnrollmentStatus, ReceptionGame, Choice, apply_choice, get_node, perform_check
from src.interaction.state import Player, Receptionist


def test_player_has_canonical_attributes() -> None:
    player = Player()
    assert list(player.attributes) == [
        "Intelligence",
        "Awareness",
        "Reflexes",
        "Body",
        "Charisma",
        "Willpower",
        "Cybernetics",
    ]
    assert player.get_attribute("Intelligence") == 4
    assert player.get_attribute("Charisma") == 3
    assert player.get_attribute("Psyche") == 0


def test_receptionist_state_clamps() -> None:
    dahl = Receptionist()
    dahl.adjust_suspicion(20)
    dahl.adjust_trust(-20)
    assert dahl.suspicion == 10
    assert dahl.trust == -5
    dahl.adjust_suspicion(-20)
    dahl.adjust_trust(30)
    assert dahl.suspicion == 0
    assert dahl.trust == 10


def test_game_starts_in_test_room_with_elin_dahl() -> None:
    game = ReceptionGame()
    assert game.scene.current_node == "test_room"
    assert game.receptionist.name == "Dr. Elin Dahl"
    assert not game.is_finished


def test_outcome_thresholds_remain_available() -> None:
    game = ReceptionGame()
    assert game.resolve_outcome() == EnrollmentStatus.ACCEPTED
    game.receptionist.suspicion = 5
    assert game.resolve_outcome() == EnrollmentStatus.ADDITIONAL_SCREENING
    game.receptionist.suspicion = 8
    assert game.resolve_outcome() == EnrollmentStatus.REJECTED


def test_perform_check_uses_d6_plus_skill() -> None:
    game = ReceptionGame()
    random.seed(42)
    result = perform_check(game, "Intelligence", 8)
    assert 1 <= result.roll <= 6
    assert result.total == result.roll + 4
    assert result.success == (result.total >= 8)


def test_dialogue_nodes_exist() -> None:
    for node_id in ("test_room", "second_silence", "green_light", "forms", "resolution", "end"):
        assert get_node(node_id) is not None


def test_test_room_has_three_choices() -> None:
    node = get_node("test_room")
    assert node is not None
    assert len(node.choices) == 3


def test_canonical_opening_line_advances_and_builds_trust() -> None:
    game = ReceptionGame()
    node = get_node("test_room")
    assert node is not None
    text, success = apply_choice(game, node.choices[0])
    assert success is None
    assert "Ei kulmakarvan liikettä" in text
    assert game.scene.current_node == "second_silence"
    assert game.receptionist.trust == 1


def test_checked_choice_always_advances() -> None:
    game = ReceptionGame()
    node = get_node("test_room")
    assert node is not None
    choice = next(c for c in node.choices if c.id == "observe_dahl")
    _, success = apply_choice(game, choice)
    assert success in (True, False)
    assert game.scene.current_node == "second_silence"


def test_choice_has_check() -> None:
    assert Choice(id="a", text="b", attribute="Awareness", difficulty=5).has_check()
    assert not Choice(id="a", text="b").has_check()


def test_canonical_finish_overrides_suspicion_with_acceptance() -> None:
    game = ReceptionGame()
    game.receptionist.suspicion = 10
    node = get_node("resolution")
    assert node is not None
    apply_choice(game, node.choices[0])
    assert game.is_finished
    assert game.scene.enrollment_status == EnrollmentStatus.ACCEPTED


def test_full_canonical_playthrough_stops_before_pod() -> None:
    game = ReceptionGame()

    node = get_node("test_room")
    assert node is not None
    apply_choice(game, node.choices[0])

    node = get_node("second_silence")
    assert node is not None
    apply_choice(game, node.choices[0])

    node = get_node("green_light")
    assert node is not None
    assert node.npc_text == "Onneksi olkoon. Teidät on valittu kokeeseen."
    apply_choice(game, node.choices[0])

    node = get_node("forms")
    assert node is not None
    assert "podiinne" in node.npc_text
    apply_choice(game, node.choices[0])

    node = get_node("resolution")
    assert node is not None
    assert "Podiin ei mennä" in node.narration
    apply_choice(game, node.choices[0])

    assert game.is_finished
    assert game.scene.enrollment_status == EnrollmentStatus.ACCEPTED
