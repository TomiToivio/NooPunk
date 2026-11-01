"""Regression tests for issue #1008's pure-Python, additive social tags."""
import pytest

from nopunk_mud.faction_tags import (
    NETWORKS, initial_state, normalize, rank, can_command, promote,
    set_reputation, reputation_modifier, reaction, set_goal, visible_goals,
    visible_reputations,
)


def test_new_character_is_unsa_rookie_and_has_five_network_names():
    s = initial_state()
    assert rank(s) == 0
    assert len(NETWORKS) == 5
    assert can_command(s, "individual")
    assert not can_command(s, "partner", available_agents=2)
    assert not can_command(s, "team", available_agents=4)


def test_rank_authorization_requires_staff_and_approval():
    s = initial_state()
    assert promote(s, "UNSA", 1, approved=True)["equipment"] == "field issue"
    assert can_command(s, "partner", available_agents=2)
    assert not can_command(s, "partner", available_agents=1)
    with pytest.raises(ValueError):
        promote(s, "UNSA", 4, approved=True)
    with pytest.raises(ValueError):
        promote(s, "UNSA", 2, approved=False)
    assert promote(s, "UNSA", 2, approved=True)["xp_award_pending"] == 0
    assert can_command(s, "team", available_agents=4)
    assert not can_command(s, "team", available_agents=3)
    assert not can_command(s, "team", available_agents=4, authorized=False)


def test_scoped_reputation_nonstacking_and_private_visibility():
    s = initial_state()
    set_reputation(s, "network", "UNSA", -3)
    set_reputation(s, "network", "SipuliVerkko", 2)
    set_reputation(s, "person", "Romppainen", 4, visibility="private")
    assert reputation_modifier(s, "network", "UNSA", npc_knows=True) == -3
    assert reputation_modifier(s, "network", "SipuliVerkko", npc_knows=True) == 2
    assert reputation_modifier(s, "network", "UNSA", npc_knows=False) == 0
    assert reputation_modifier(s, "person", "Romppainen", npc_knows=True) == 4
    assert "person:Romppainen" not in visible_reputations(s)
    assert "person:Romppainen" in visible_reputations(s, viewer="owner")
    assert normalize(s) == s


@pytest.mark.parametrize("bad", [-5, 5, 2.5, True])
def test_bad_reputation_rejected(bad):
    with pytest.raises(ValueError):
        set_reputation(initial_state(), "network", "UNSA", bad)


@pytest.mark.parametrize(("score", "category"), [
    (2, "hostile/violent"), (3, "hostile/unfriendly"), (5, "hostile/unfriendly"),
    (6, "neutral"), (8, "neutral"), (9, "friendly/cooperative"),
    (11, "friendly/cooperative"), (12, "very helpful"),
])
def test_reaction_categories(score, category):
    assert reaction(score)[1] == category


def test_reaction_modifier_and_goals():
    assert reaction(7, charisma_modifier=1, reputation=-4)[0] == 4
    s = initial_state()
    set_goal(s, "case", "Solve the missing-person case")
    set_goal(s, "secret", "Find the source", visibility="secret")
    assert "case" not in visible_goals(s, viewer="public")
    assert "secret" in visible_goals(s, viewer="owner")
    assert s["audit"][-1]["action"] == "goal"
