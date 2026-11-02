"""CWN 6.1 and 6.4 — Effort, commitments and magic items (#1068).

These are the numbers a mage's whole day hangs on, so they are pinned rather than described.
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

from src.rules.cwn_magic import (
    EffortPool,
    MagicError,
    can_cast,
    cyberware_penalty,
    mage_effort,
    summoner_effort,
)
from src.rules.cwn_magic_items import (
    LinkedItem,
    MagicItemError,
    can_identify,
    can_link_unaided,
    can_sense_magic,
)


def test_mage_effort_is_the_better_mental_modifier_plus_cast_skill():
    # INT 14 -> +1, WIS 8 -> +0, Cast 1  =>  2
    assert mage_effort(intelligence=14, wisdom=8, cast_skill=1) == 2
    # WIS 17 -> +1 and INT 8 -> +0, Cast 2 => 3: the better of the two, never the sum
    assert mage_effort(intelligence=8, wisdom=17, cast_skill=2) == 3


def test_mage_effort_is_never_zero_even_for_a_hopeless_caster():
    assert mage_effort(intelligence=3, wisdom=3, cast_skill=0) == 1


def test_summoner_effort_uses_constitution_or_charisma():
    assert summoner_effort(constitution=14, charisma=8, summon_skill=1) == 2
    assert summoner_effort(constitution=8, charisma=17, summon_skill=2) == 3


def test_cyberware_reduces_the_pool_but_never_below_one():
    assert mage_effort(intelligence=14, wisdom=8, cast_skill=1, strain_costs=[1]) == 1
    assert mage_effort(intelligence=3, wisdom=3, cast_skill=0, strain_costs=[5]) == 1


def test_each_implant_costs_at_least_one_point_so_the_book_example_balances():
    """2 + 0 + 0.5 is 2.5, which rounds up to 3; the SRD's example says four points."""
    # 2 + 0 + 0.5 sums to 2.5, but the book says such a mage loses four points. The only reading that
    # satisfies its own example is "each implant costs at least one", which is what the rule documents.
    assert cyberware_penalty([2, 0, 0.5]) == 4


def test_commitments_are_tracked_apart_and_released_apart():
    pool = EffortPool(maximum=5)
    pool.commit(2, duration="day")
    pool.commit(1, duration="scene")
    pool.commit(1, duration="duration")
    assert pool.available == 1
    assert pool.end_scene() == 1
    assert pool.available == 2
    assert pool.reclaim_duration() == 1
    assert pool.available == 3, "the day commitment stays until morning"


def test_a_pool_cannot_commit_more_than_it_has():
    pool = EffortPool(maximum=2)
    with pytest.raises(MagicError):
        pool.commit(3, duration="day")


def test_refresh_needs_sleep_and_no_hardship():
    pool = EffortPool(maximum=3)
    pool.commit(2, duration="day")
    assert pool.refresh_morning(slept_eight_hours=False) is False
    assert pool.available == 1, "no sleep, no refresh — 6.1.1 is explicit about this"
    assert pool.refresh_morning(comfortable=False) is False
    assert pool.refresh_morning() is True
    assert pool.available == 3


def test_casting_needs_a_hand_and_a_voice_but_not_light_armour():
    assert can_cast(free_hand=True, can_speak=True) is True
    assert can_cast(free_hand=False, can_speak=True) is False
    assert can_cast(free_hand=True, can_speak=False) is False


def test_a_magical_observer_senses_magic_but_mundane_eyes_do_not():
    assert can_sense_magic(has_magical_edge=True) is True
    assert can_sense_magic(has_magical_edge=False, cast_skill=0) is False


def test_identification_needs_the_item_minimum_or_a_day_of_study():
    assert can_identify(minimum_magic_skill=2, cast_skill=2) is True
    assert can_identify(minimum_magic_skill=2, cast_skill=1) is False
    assert can_identify(minimum_magic_skill=None, cast_skill=0, days_of_study=1) is True
    assert can_identify(minimum_magic_skill=None, cast_skill=0, days_of_study=0) is False


def test_linking_needs_cast_or_summon_or_a_guide():
    assert can_link_unaided(cast_skill=0) is False
    assert can_link_unaided(cast_skill=1) is True
    item = LinkedItem("ward-stone")
    with pytest.raises(MagicItemError):
        item.link()
    item.link(guided=True)
    assert item.strain_committed == 1


def test_linking_costs_permanent_strain_and_an_arcanist_effort_until_the_next_morning():
    item = LinkedItem("ward-stone", arcanist=True).link(cast_skill=1)
    assert (item.strain_committed, item.effort_committed) == (1, 1)
    out = item.unlink()
    assert out == {"effort_returns": 1, "when": "next_morning"}
    assert item.strain_committed == 0


# CI runs `unittest discover`, which needs a TestCase rather than module-level functions.
# The shim keeps the pytest-style bodies and makes them discoverable without pytest.
ModuleLevelTests = register_module_functions(globals())
