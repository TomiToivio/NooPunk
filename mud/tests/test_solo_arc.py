"""The phase-1 acceptance claim, made checkable (#950).

"If the solo campaign is playable" is not something a directory listing can prove. These tests play it.
"""
from __future__ import annotations

import json

from mud.nopunk_mud.solo_arc import Arc, advance


def _always(skill, difficulty, dice):
    return True


def _never(skill, difficulty, dice):
    return False


def test_a_full_run_reaches_a_corroborated_ending():
    a = Arc()
    a, _ = advance(a, "accept", _always)
    a, _ = advance(a, "interview", _always, dice=(3, 4))
    a, _ = advance(a, "leave", _always)
    a, _ = advance(a, "records", _always, dice=(3, 4))
    a, _ = advance(a, "press", _always)
    a, _ = advance(a, "submit", _always)
    assert a.stage == "complete"
    assert a.ending == "corroborated"
    assert set(a.clues) == {"witness", "records"}
    assert a.consequences == []


def test_failed_checks_never_dead_end_the_case():
    """A GUMSHOE core clue cannot be missed. A scripted GM must not invent a wall either."""
    a = Arc()
    a, _ = advance(a, "accept", _never)
    a, _ = advance(a, "interview", _never)
    assert a.stage == "records", "a failed interview must still open the next scene"
    a, _ = advance(a, "records", _never)
    assert a.stage == "confrontation"
    a, _ = advance(a, "press", _never)
    a, _ = advance(a, "submit", _never)
    assert a.stage == "complete", "the case ends somewhere even when everything goes wrong"
    assert a.ending == "unsolved"


def test_consequences_change_the_ending_rather_than_the_wording():
    a = Arc()
    a, _ = advance(a, "accept", _always)
    a, _ = advance(a, "interview", _always, dice=(3, 4))
    a, _ = advance(a, "leave", _always)
    a, _ = advance(a, "records", _never)          # one clue, one consequence
    a, _ = advance(a, "press", _always)
    a, _ = advance(a, "submit", _always)
    assert a.ending == "partial"
    assert a.consequences == ["records_incomplete"]


def test_rejected_actions_do_not_mutate_state():
    a = Arc()
    before = a.to_dict()
    a, text = advance(a, "submit", _always)
    assert a.to_dict() == before
    assert "unavailable" in text


def test_state_survives_a_json_round_trip_mid_case():
    a = Arc()
    a, _ = advance(a, "accept", _always)
    a, _ = advance(a, "interview", _never)
    blob = json.dumps(a.to_dict())
    restored = Arc.from_dict(json.loads(blob))
    assert restored == a
    restored, _ = advance(restored, "records", _always, dice=(3, 4))
    assert restored.stage == "confrontation"
