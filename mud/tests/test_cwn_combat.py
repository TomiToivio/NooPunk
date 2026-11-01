"""CWN action economy, Trauma and Shock (#950 item 3).

Each test pins one sentence of the SRD: one Main per round, a second Move paid for with the Main,
Trauma only on a lethal hit and only at or above the Trauma Target, and Shock only on a miss and only
at or below the weapon's Shock AC.
"""
from __future__ import annotations

import pytest

from nopunk_mud.cwn import CwnError
from nopunk_mud.cwn.combat import CombatTurn, shock_damage, trauma_hit


# --- action economy -----------------------------------------------------------------------

def test_one_main_action_per_round() -> None:
    turn = CombatTurn()
    turn.spend_main()
    with pytest.raises(CwnError):
        turn.spend_main()


def test_one_move_action_then_a_second_paid_with_the_main() -> None:
    turn = CombatTurn()
    turn.spend_move()
    assert turn.moves_used == 1
    assert turn.main_available is True, "the second move has not been taken yet"
    turn.spend_move()
    assert turn.moves_used == 2
    assert turn.main_available is False, "the second move spends the main action"
    with pytest.raises(CwnError):
        turn.spend_move()


def test_a_second_move_is_refused_when_the_main_is_already_spent() -> None:
    turn = CombatTurn()
    turn.spend_main()
    turn.spend_move()
    with pytest.raises(CwnError):
        turn.spend_move()


def test_on_turn_and_instant_actions_are_not_capped_by_the_rules() -> None:
    turn = CombatTurn()
    for _ in range(5):
        turn.spend_on_turn()
    for _ in range(5):
        turn.spend_instant()
    assert turn.on_turn_used == 5
    assert turn.instant_used == 5
    assert turn.main_available is True, "neither on-turn nor instant actions consume the main"


def test_reset_starts_a_new_round() -> None:
    turn = CombatTurn()
    turn.spend_main()
    turn.spend_move()
    turn.spend_instant()
    turn.reset()
    assert (turn.main_used, turn.moves_used, turn.instant_used, turn.used) == (False, 0, 0, [])
    turn.spend_main()


# --- trauma -------------------------------------------------------------------------------

@pytest.mark.parametrize("roll", [6, 7, 8, 9, 10])
def test_a_trauma_die_at_or_above_the_target_multiplies_damage(roll: int) -> None:
    result = trauma_hit(damage=9, trauma_die=10, die_roll=roll, trauma_rating=3)
    assert result["traumatic"] is True
    assert result["damage"] == 27, "a x3 rating turns 9 into 27"


@pytest.mark.parametrize("roll", [1, 2, 3, 4, 5])
def test_below_the_trauma_target_is_not_traumatic(roll: int) -> None:
    result = trauma_hit(damage=9, trauma_die=10, die_roll=roll, trauma_rating=3)
    assert result["traumatic"] is False
    assert result["damage"] == 9


def test_the_boundary_roll_equal_to_the_target_is_traumatic() -> None:
    assert trauma_hit(damage=5, trauma_die=6, die_roll=6, trauma_rating=2)["traumatic"] is True


def test_a_non_lethal_attack_does_not_roll_the_trauma_die() -> None:
    result = trauma_hit(damage=9, trauma_die=10, die_roll=10, trauma_rating=3, lethal=False)
    assert result == {"traumatic": False, "damage": 9, "die": None}


def test_a_higher_trauma_target_reduces_traumatic_hits() -> None:
    assert trauma_hit(damage=9, trauma_die=8, die_roll=7, trauma_rating=2, trauma_target=8)["traumatic"] is False
    assert trauma_hit(damage=9, trauma_die=8, die_roll=8, trauma_rating=2, trauma_target=8)["traumatic"] is True


@pytest.mark.parametrize("kwargs", [
    {"trauma_die": 7, "die_roll": 1, "trauma_rating": 2},
    {"trauma_die": 10, "die_roll": 0, "trauma_rating": 2},
    {"trauma_die": 10, "die_roll": 11, "trauma_rating": 2},
    {"trauma_die": 10, "die_roll": 5, "trauma_rating": 1},
    {"trauma_die": 10, "die_roll": 5, "trauma_rating": 2, "trauma_target": 0},
])
def test_invalid_trauma_inputs_are_refused(kwargs: dict) -> None:
    with pytest.raises(CwnError):
        trauma_hit(damage=5, **kwargs)


# --- shock --------------------------------------------------------------------------------

def test_shock_applies_on_a_miss_at_or_below_the_shock_ac() -> None:
    assert shock_damage(shock=2, shock_ac=15, missed=True, target_melee_ac=13) == 2
    assert shock_damage(shock=2, shock_ac=15, missed=True, target_melee_ac=15) == 2


def test_shock_does_not_apply_to_a_better_armoured_target() -> None:
    assert shock_damage(shock=2, shock_ac=15, missed=True, target_melee_ac=16) == 0


def test_shock_does_not_apply_on_a_hit() -> None:
    assert shock_damage(shock=2, shock_ac=15, missed=False, target_melee_ac=10) == 0


def test_negative_shock_is_refused() -> None:
    with pytest.raises(CwnError):
        shock_damage(shock=-1, shock_ac=15, missed=True, target_melee_ac=10)
