"""Regression tests for CWN/solo arc integration (#966)."""
import pytest

from nopunk_mud.solo_arc import Arc, advance
from nopunk_mud.solo_resolver import make_resolver


SHEET = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 14, "CHA": 10}


def test_published_cwn_dice_and_rank_are_used():
    resolve = make_resolver(SHEET, {"notice": 1})
    assert resolve("Notice", "routine", (3, 3))  # 6 + 1 skill + 1 WIS >= 8
    assert not make_resolver(SHEET, {"notice": -1})("Notice", "routine", (3, 3))


def test_arc_runs_on_real_cwn_resolver_and_preserves_failure_consequence():
    resolve = make_resolver(SHEET, {"notice": -1})
    arc, _ = advance(Arc(), "accept", resolve)
    arc, _ = advance(arc, "interview", resolve, dice=(1, 1))
    assert arc.stage == "records"
    assert "witness_uncooperative" in arc.consequences
    arc, _ = advance(arc, "records", resolve, dice=(6, 6))
    assert arc.stage == "confrontation"
    arc, _ = advance(arc, "press", resolve)
    arc, _ = advance(arc, "submit", resolve)
    assert arc.stage == "complete"
    assert arc.ending in {"partial", "unsolved", "corroborated_with_gaps", "corroborated"}


@pytest.mark.parametrize("skill,difficulty,dice", [
    ("invented", "routine", (3, 3)),
    ("Notice", "unpublished", (3, 3)),
    ("Notice", "routine", (7, 1)),
    ("Notice", "routine", (1,)),
])
def test_invalid_mechanics_cannot_be_silently_accepted(skill, difficulty, dice):
    with pytest.raises(ValueError):
        make_resolver(SHEET, {}) (skill, difficulty, dice)
