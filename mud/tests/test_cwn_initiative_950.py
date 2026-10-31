"""SRD boundary and replay tests for #950 initiative."""
import pytest

from nopunk_mud.cwn import CwnError
from nopunk_mud.cwn.initiative import InitiativeEntry as Side
from nopunk_mud.cwn.initiative import initiative_order, surprise_round


def names(entries):
    return [entry.name for entry in entries]


def test_highest_side_first_and_order_stable_between_rounds():
    sides = [Side("UNSA", 3, 2, True), Side("security", 7), Side("patrol", 2)]
    assert names(initiative_order(sides)) == ["security", "UNSA", "patrol"]
    assert initiative_order(sides) == initiative_order(sides)


def test_player_side_wins_exact_ties():
    assert names(initiative_order([Side("guard", 6), Side("UNSA", 5, 1, True)])) == [
        "UNSA", "guard"
    ]


def test_automatic_initiative_beats_even_higher_roll():
    assert names(initiative_order([Side("guard", 8), Side("agent", 1, pc=True, automatic=True)])) == [
        "agent", "guard"
    ]


def test_multiple_automatic_actors_roll_against_each_other():
    assert names(initiative_order([
        Side("agent", 3, pc=True, automatic=True),
        Side("guard", 8),
        Side("cyborg", 4, automatic=True),
    ])) == ["cyborg", "agent", "guard"]


def test_optional_individual_mode_uses_same_ordering():
    assert names(initiative_order([
        Side("agent A", 1, 2, True),
        Side("agent B", 7, -1, True),
        Side("guard", 5),
    ])) == ["agent B", "guard", "agent A"]


def test_surprise_gives_unaware_side_no_free_round_actions():
    sides = [Side("UNSA", 4, pc=True), Side("ambushers", 5)]
    assert names(surprise_round(sides, ["UNSA"])) == ["ambushers"]
    assert names(initiative_order(sides)) == ["ambushers", "UNSA"]


@pytest.mark.parametrize("entry", [
    Side("", 5), Side("bad", 0), Side("bad", 9),
    Side("bad", True), Side("bad", 4, 0.5),
])
def test_invalid_inputs_are_rejected(entry):
    with pytest.raises(CwnError):
        initiative_order([entry])


def test_duplicate_names_and_unknown_surprise_are_rejected():
    with pytest.raises(CwnError):
        initiative_order([Side("A", 1), Side("A", 2)])
    with pytest.raises(CwnError):
        surprise_round([Side("A", 1)], ["B"])
    with pytest.raises(CwnError):
        surprise_round([Side("A", 1)], ["A", "A"])


def test_no_combatants():
    assert initiative_order([]) == ()
    assert surprise_round([], []) == ()
