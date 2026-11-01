"""Phase 1 of #1008, tested against its own acceptance list."""
from __future__ import annotations

import json

import pytest

from mud.nopunk_mud.social import (Goal, Membership, Reputation, SocialError, SocialRecord,
                                   reaction, reaction_modifier)


def test_a_rookie_may_act_alone_but_not_command_a_team():
    rookie = Membership("UNSA", rank=0)
    assert rookie.may_command(1) is True
    assert rookie.may_command(4) is False
    assert rookie.max_agents == 1


def test_promotion_unlocks_team_command_and_is_audited():
    m = Membership("UNSA", rank=0)
    m = m.promote(reason="closed the Missing Researcher case", authorized_by="Romppainen")
    assert m.rank == 1 and m.may_command(2) is True and m.may_command(4) is False
    m = m.promote(reason="led Kurvi operation", authorized_by="UNSA Helsinki")
    assert m.rank == 2 and m.may_command(4) is True
    assert len(m.promotions) == 2


def test_a_promotion_cannot_be_anonymous():
    with pytest.raises(SocialError):
        Membership("UNSA", rank=0).promote(reason="", authorized_by="Romppainen")


def test_rank_outside_the_track_is_refused():
    with pytest.raises(SocialError):
        Membership("UNSA", rank=5)


def test_reputation_is_bounded_to_minus_four_through_plus_four():
    assert Reputation("UNSA", -4).value == -4
    assert Reputation("UNSA", 4).value == 4
    with pytest.raises(SocialError):
        Reputation("UNSA", 5)


def test_zero_means_unknown_not_hostile():
    r = Reputation("SipuliVerkko", 0)
    out = reaction((3, 4), charisma_modifier=0, reputation_value=r.value, known=True)
    assert out["band"] == "neutral"
    assert out["overlay_applied"] == 0


def test_the_same_name_in_two_scopes_stays_two_records():
    rec = SocialRecord(reputations=[Reputation("UNSA", -3), Reputation("npc:romppainen", 2)])
    assert reaction_modifier(rec.reputations, chosen_scope="UNSA") == -3
    assert reaction_modifier(rec.reputations, chosen_scope="npc:romppainen") == 2


def test_reputation_never_stacks_across_networks():
    """The abuse case: +2 in four networks must not become +8 on a 2d6 roll."""
    reps = [Reputation(n, 2) for n in ("UNSA", "SuomiNet", "MarsNet Hype", "SipuliVerkko")]
    modifier = reaction_modifier(reps, chosen_scope="UNSA")
    assert modifier == 2, "one scope applies, whatever the others say"
    out = reaction((3, 4), charisma_modifier=0, reputation_value=modifier)
    assert out["total"] == 9, "7 + 2, never 7 + 8"


def test_an_unknown_scope_is_an_error_not_a_zero():
    with pytest.raises(SocialError):
        reaction_modifier([Reputation("UNSA", 1)], chosen_scope="SuomiNet")


def test_duplicate_records_for_one_scope_are_ambiguous():
    with pytest.raises(SocialError):
        reaction_modifier([Reputation("UNSA", 1), Reputation("UNSA", -1)], chosen_scope="UNSA")


def test_reaction_bands_follow_the_published_thresholds():
    assert reaction((1, 1), 0)["band"] == "as hostile as plausible"
    assert reaction((2, 3), 0)["band"] == "hostile/unfriendly"
    assert reaction((3, 4), 0)["band"] == "neutral"
    assert reaction((5, 5), 0)["band"] == "unusually friendly/cooperative"
    assert reaction((6, 6), 0)["band"] == "as friendly/helpful as plausible"


def test_an_unknown_reputation_does_not_change_the_roll():
    known = reaction((3, 4), 1, 3, known=True)
    unknown = reaction((3, 4), 1, 3, known=False)
    assert known["overlay_applied"] == 3 and unknown["overlay_applied"] == 0
    assert unknown["total"] == 8


def test_secret_reputation_is_not_visible_to_an_outside_scope():
    secret = Reputation("UNSA", -4, visibility="secret")
    assert secret.known_to("SuomiNet") is False
    assert secret.known_to("UNSA") is True
    private = Reputation("npc:romppainen", 2, visibility="private")
    assert private.known_to("UNSA") is False


def test_goals_carry_state_not_bonuses():
    g = Goal(owner="rookie", text="find the researcher", kind="faction")
    assert g.status == "open"
    with pytest.raises(SocialError):
        Goal(owner="rookie", text="be excellent", status="vibing")


def test_the_record_survives_a_json_round_trip():
    rec = SocialRecord(memberships=[Membership("UNSA", 1)], reputations=[Reputation("UNSA", -3)],
                       goals=[Goal("rookie", "close the case")])
    restored = SocialRecord.from_dict(json.loads(json.dumps(rec.to_dict())))
    assert restored == rec
