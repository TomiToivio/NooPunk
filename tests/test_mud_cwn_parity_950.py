"""The MUD's CWN core agrees with the repository's Python rules, case by case (#950).

A port is only a port if it produces the same answers. This test compares `mud/nopunk_mud/cwn` against
`src/rules/` on the procedures both implement — attributes, saves, skill arithmetic, hit points and strain —
using fixed inputs, so a divergence is a failing test rather than a later surprise at a table.

It lives at the repository root on purpose: `mud/` must stay importable without the rest of the repository, and
this comparison is the place where the two are allowed to meet.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))
sys.path.insert(0, str(ROOT))

from nopunk_mud import cwn  # noqa: E402
from src.rules import cwn_advancement, cwn_core, wn_core  # noqa: E402

SHEETS = [
    {"Strength": 12, "Dexterity": 15, "Constitution": 9, "Intelligence": 11, "Wisdom": 13,
     "Charisma": 8},
    {"Strength": 3, "Dexterity": 18, "Constitution": 14, "Intelligence": 7, "Wisdom": 10,
     "Charisma": 17},
]


@pytest.mark.parametrize("sheet", SHEETS)
@pytest.mark.parametrize("score", list(range(3, 19)))
def test_attribute_modifiers_match(sheet, score):
    assert cwn.attribute_modifier(score) == wn_core.attribute_modifier(score)


@pytest.mark.parametrize("sheet", SHEETS)
@pytest.mark.parametrize("kind", ["Physical", "Evasion", "Mental", "Luck"])
@pytest.mark.parametrize("level", [1, 3, 7, 10])
def test_save_targets_match(sheet, kind, level):
    assert cwn.save_target(kind, level=level, attributes=sheet) == \
        cwn_core.save_target(kind, level=level, attributes=sheet)


@pytest.mark.parametrize("sheet", SHEETS)
@pytest.mark.parametrize("die", [1, 2, 10, 19, 20])
def test_saving_throws_match(sheet, die):
    theirs = cwn_core.saving_throw("Physical", level=2, attributes=sheet, die=die, bonus=1)
    ours = cwn.saving_throw("Physical", level=2, attributes=sheet, die=die, bonus=1)
    assert ours["target"] == theirs.target
    assert ours["success"] == theirs.success
    assert ours["natural"] == theirs.natural


@pytest.mark.parametrize("level", [1, 2, 5])
@pytest.mark.parametrize("dice", [(1,), (3,), (6, 6), (1, 4, 2, 6, 5)])
def test_hit_points_match(level, dice):
    if len(dice) != level:
        pytest.skip("dice count must equal level")
    con_mod = 1
    assert cwn.hit_points(level, con_mod, dice=dice) == \
        cwn_advancement.hit_points_rolled(level, con_mod, dice=dice)


@pytest.mark.parametrize("constitution", [3, 9, 14, 18])
@pytest.mark.parametrize("lifestyle", ["squatter", "slum", "ordinary", "fine", "luxury"])
def test_strain_maximum_matches(constitution, lifestyle):
    assert cwn.strain_maximum(constitution, lifestyle=lifestyle) == \
        cwn_core.strain_maximum(constitution, lifestyle=lifestyle)


def test_rank_zero_is_trained_on_both_sides():
    """The one rule that is easy to get wrong, asserted against itself and against the canonical value."""
    assert cwn.skill_modifier(0) == 0
    assert cwn.skill_modifier(-1) == -1


@pytest.mark.parametrize("rank", [-1, 0, 1, 4])
@pytest.mark.parametrize("dice", [(1, 1), (3, 4), (6, 6)])
def test_skill_check_arithmetic(rank, dice):
    sheet = SHEETS[0]
    result = cwn.skill_check(rank=rank, attribute=sheet["Intelligence"], difficulty=10, dice=dice)
    expected = dice[0] + dice[1] + (cwn.UNTRAINED_MODIFIER if rank < 0 else rank) \
        + wn_core.attribute_modifier(sheet["Intelligence"])
    assert result.total == expected
    assert result.success == (expected >= 10)


def test_an_illegal_sheet_is_refused_not_repaired():
    with pytest.raises(cwn.CwnError):
        cwn.create_character("rookie", attributes={**SHEETS[0], "Strength": 22})
    with pytest.raises(cwn.CwnError):
        cwn.create_character("rookie", attributes={"Strength": 10})
    with pytest.raises(cwn.CwnError):
        cwn.create_character("", attributes=SHEETS[0])
