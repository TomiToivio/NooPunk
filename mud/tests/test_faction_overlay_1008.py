"""Boundary and save tests for #1008, runnable without Evennia."""
import json
import pytest
from nopunk_mud.faction_overlay import FactionOverlay, Membership, Goal, NETWORKS


def test_rookie_and_rank_authority():
    overlay = FactionOverlay.rookie()
    member = overlay.memberships["UNSA"]
    assert member.rank == 0 and member.can_lead(1) and not member.can_lead(2)
    with pytest.raises(PermissionError):
        overlay.promote("UNSA", 1, authorized=False, evidence="case", actor="supervisor")
    overlay.promote("UNSA", 1, authorized=True, evidence="case closed", actor="Romppainen")
    assert member.can_lead(2) and not member.can_lead(4)
    overlay.promote("UNSA", 2, authorized=True, evidence="command", actor="Romppainen")
    assert member.can_lead(4) and not member.can_lead(5)
    member.suspended = True
    assert not member.can_lead(1)


def test_scoped_reputation_and_nonstacking():
    overlay = FactionOverlay.rookie()
    assert len(NETWORKS) == 5
    overlay.set_reputation("network", "UNSA", -3, evidence="reprimand")
    overlay.set_reputation("network", "SipuliVerkko", 2, evidence="favor")
    overlay.set_reputation("npc", "Romppainen", 4, evidence="trusted")
    assert overlay.reaction_modifier([("network", "UNSA")]) == -2
    assert overlay.reaction_modifier([("network", "SipuliVerkko")]) == 2
    assert overlay.reaction_modifier([("npc", "Romppainen"), ("network", "UNSA")]) == 2
    assert overlay.reaction_modifier([("network", "SuomiNet")]) == 0
    assert overlay.reaction_modifier([], max_magnitude=4) == 0
    with pytest.raises(ValueError):
        overlay.set_reputation("network", "UNSA", 5, evidence="illegal")
    with pytest.raises(ValueError):
        overlay.set_reputation("network", "UNSA", 0, evidence="")


def test_private_and_secret_visibility():
    overlay = FactionOverlay.rookie()
    overlay.set_reputation("network", "Internet", -4, visibility="secret",
                           evidence="classified", actor="admin")
    assert not overlay.visible_reputations()
    assert not overlay.visible_reputations(include_private=True)
    assert overlay.visible_reputations(admin=True)
    with pytest.raises(PermissionError):
        overlay.set_reputation("network", "Internet", 0, evidence="reset")


def test_goals_and_roundtrip():
    overlay = FactionOverlay.rookie()
    overlay.add_goal(Goal("case", "Investigate records", "rookie", progress=10))
    with pytest.raises(ValueError):
        overlay.add_goal(Goal("case", "Repeat", "rookie"))
    encoded = json.dumps(overlay.snapshot(), ensure_ascii=False)
    restored = FactionOverlay.from_snapshot(json.loads(encoded))
    assert restored.snapshot() == overlay.snapshot()
    assert restored.memberships["UNSA"].rank == 0
    with pytest.raises(ValueError):
        FactionOverlay.from_snapshot({"version": 22})
