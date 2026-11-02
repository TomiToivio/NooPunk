"""CWN 6.2 Summoning, implemented from the SRD (#1068).

Until this change the rules library contained the words "summon", "spirit", "spellcasting" and "graced" zero
times: chapter 6 of the CWN SRD was entirely absent, while chapters 1-5 were covered. These tests pin the rules
that the SRD states in plain numbers, and they are written to fail if someone "simplifies" one.
"""
from __future__ import annotations

try:  # `unittest discover -s tests` puts tests/ on sys.path
    from _pytest_compat import pytest, register_module_functions
except ModuleNotFoundError:  # pytest.ini uses --import-mode=importlib, which does not
    import importlib.util as _ilu
    import pathlib as _pl

    _spec = _ilu.spec_from_file_location(
        "_pytest_compat", _pl.Path(__file__).with_name("_pytest_compat.py"))
    assert _spec and _spec.loader
    _compat = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_compat)
    pytest, register_module_functions = _compat.pytest, _compat.register_module_functions

from src.rules.cwn_summoning import (
    MANIFESTATIONS,
    Spirit,
    SummoningError,
    banish_damage,
    banish_target,
    command_difficulty,
    effort_cost,
    form_tier,
    may_summon,
    summon,
)


def test_form_tiers_unlock_at_1_5_and_9():
    assert [form_tier(level) for level in (1, 4, 5, 8, 9, 20)] == [1, 1, 2, 2, 3, 3]


def test_effort_cost_is_powers_minus_skill_but_never_free():
    assert effort_cost(power_count=3, summon_skill=1) == 2
    assert effort_cost(power_count=1, summon_skill=0) == 1
    # A generous Summon skill can never make a summon cost zero Effort.
    assert effort_cost(power_count=2, summon_skill=5) == 1


def test_successive_summons_in_one_scene_cost_more_each_time():
    assert effort_cost(power_count=2, summon_skill=1, prior_summons_this_scene=0) == 1
    assert effort_cost(power_count=2, summon_skill=1, prior_summons_this_scene=1) == 2
    assert effort_cost(power_count=2, summon_skill=1, prior_summons_this_scene=3) == 4


def test_total_spirit_hit_dice_may_not_exceed_character_level():
    assert may_summon(character_level=5, current_spirit_hd=0, new_spirit_hd=5) is True
    assert may_summon(character_level=5, current_spirit_hd=5, new_spirit_hd=1) is False


def test_a_level_one_summoner_cannot_take_a_second_tier_form():
    spirit = Spirit("Ember", "Fire", form="spirit", tier=2)
    with pytest.raises(SummoningError):
        summon(summoner_level=1, summon_skill=1, spirit=spirit)


def test_summoning_at_level_five_allows_tier_two_and_commits_effort():
    spirit = Spirit("Ember", "Fire", form="spirit", tier=2, powers=("Flicker", "Kindle"))
    out = summon(summoner_level=5, summon_skill=1, spirit=spirit)
    assert out.effort_committed == 1
    assert out.hp == 15 and out.hd == 3


def test_command_difficulties_are_9_11_and_13():
    assert command_difficulty("routine") == 9
    assert command_difficulty("contrary_inclination") == 11
    assert command_difficulty("against_nature") == 13
    with pytest.raises(SummoningError):
        command_difficulty("because I said so")


def test_banishing_damage_is_one_d8_per_summon_skill_level():
    assert banish_damage(summon_skill=2, rolls=(4, 7)) == 11
    with pytest.raises(SummoningError):
        banish_damage(summon_skill=2, rolls=(4,))          # too few dice
    with pytest.raises(SummoningError):
        banish_damage(summon_skill=1, rolls=(9,))          # not a d8


def test_banishing_an_uncontrolled_spirit_targets_skill_plus_two():
    assert banish_target(spirit_controlled=True, summoner_summon_skill=3) == 13
    assert banish_target(spirit_controlled=False, spirit_skill_bonus=2) == 14


def test_a_spirit_at_zero_hit_points_vanishes():
    spirit = Spirit("Ember", "Fire")
    assert spirit.damage(4) is False
    assert spirit.damage(1) is True
    assert spirit.hp == 0


def test_manifestation_statistics_match_the_published_table():
    assert MANIFESTATIONS[("spirit", 1)]["hp"] == 5
    assert MANIFESTATIONS[("physical", 3)]["hp"] == 40
    assert MANIFESTATIONS[("physical", 3)]["ac"] == 18
    assert MANIFESTATIONS[("spirit", 3)]["attack"] is None, "spirit forms cannot directly harm creatures"


# CI runs `unittest discover`, which needs a TestCase rather than module-level functions.
# The shim keeps the pytest-style bodies and makes them discoverable without pytest.
ModuleLevelTests = register_module_functions(globals())
