"""Vanilla CWN reaction, morale and Heat procedures (#1025)."""
from __future__ import annotations

import pytest

from src.rules.cwn_heat import HeatError, HeatTrack, heat_band
from src.rules.cwn_npcs import NpcRuleError, morale_check, reaction_band, reaction_roll


@pytest.mark.parametrize("total,band", [(2, "violent_hostile"), (3, "hostile"), (5, "hostile"),
                                         (6, "neutral"), (8, "neutral"), (9, "friendly"),
                                         (11, "friendly"), (12, "helpful")])
def test_reaction_table_boundaries(total, band):
    assert reaction_band(total) == band


def test_reaction_roll_applies_charisma_and_keeps_total_in_band_range():
    assert reaction_roll(3, 3, 0).band == "neutral"
    assert reaction_roll(1, 1, 2).total == 4
    assert reaction_roll(1, 1, 2).band == "hostile"
    assert reaction_roll(6, 6, 2).total == 12
    assert reaction_roll(6, 6, 2).band == "helpful"


def test_reaction_rejects_impossible_dice_and_modifiers():
    with pytest.raises(NpcRuleError):
        reaction_roll(0, 3)
    with pytest.raises(NpcRuleError):
        reaction_roll(3, 3, 3)
    with pytest.raises(NpcRuleError):
        reaction_band(13)


def test_morale_equal_or_higher_breaks_and_lower_holds():
    assert morale_check(6, 6, 12).broken is True
    assert morale_check(6, 5, 12).broken is False
    assert morale_check(2, 2, 4).broken is True
    assert morale_check(2, 1, 4).broken is False


def test_morale_is_two_to_twelve():
    with pytest.raises(NpcRuleError):
        morale_check(3, 3, 1)
    with pytest.raises(NpcRuleError):
        morale_check(3, 3, 13)


@pytest.mark.parametrize("score,band", [(0, "avoided"), (1, "low"), (3, "low"), (4, "significant"),
                                         (5, "significant"), (6, "hunted"), (7, "hunted"),
                                         (8, "overwhelmed"), (9, "overwhelmed"),
                                         (10, "megacorp_enemy"), (30, "megacorp_enemy")])
def test_heat_band_boundaries(score, band):
    assert heat_band(score)[0] == band


def test_heat_is_team_wide_and_never_negative():
    track = HeatTrack()
    assert track.add(5) == 5
    assert track.band == "significant"
    assert track.reduce(2) == 3
    assert track.reduce(99) == 0
    with pytest.raises(HeatError):
        HeatTrack(-1)
    with pytest.raises(HeatError):
        track.add(-1)
