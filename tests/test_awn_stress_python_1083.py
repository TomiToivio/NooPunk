"""AWN Stress in Python (#1083): same contract, no second copy of the numbers.

The parity that matters is not "the Python prints the same text as the Godot" — it is that both read
`data/rules/awn_stress.json` and neither owns a rule value of its own.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from src.rules.awn_stress_tracker import (CONTRACT, StressError, apply_event, event_ids, harden, is_over,
                                          new_tracker, over_by, penalty, recover, recovery_ids, stress,
                                          threshold)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "src/rules/awn_stress_tracker.py"


def test_the_module_carries_no_rule_deltas_of_its_own():
    """0 and 1 are structure (clamping, indices). A literal -2 or similar would be a second contract."""
    source = MODULE.read_text(encoding="utf-8")
    body = source.split('"""', 2)[2]
    negatives = re.findall(r"(?<![\w.])-\d+", body)
    assert negatives == [], f"hard-coded negative rule values: {negatives}"
    # and the rule values must be read from the contract, not restated
    for accessor in ('CONTRACT["threshold"]', 'rule["first_penalty"]', 'rule["penalty_step"]',
                     'CONTRACT["hardening"]'):
        assert accessor in body, f"{accessor} should come from the contract"


def test_the_event_and_recovery_ids_come_from_the_contract():
    assert event_ids() == [e["id"] for e in CONTRACT["gaining"]["events"]]
    assert recovery_ids() == [e["id"] for e in CONTRACT["recovery"]["events"]]


def test_the_ceiling_is_wisdom_and_equality_is_safe():
    t = new_tracker(wisdom=10, stress=10)
    assert threshold(t) == 10
    assert is_over(t) is False
    assert penalty(t) == 0
    t = new_tracker(wisdom=10, stress=11)
    assert is_over(t) is True and over_by(t) == 1


def test_the_penalty_steps_with_every_point_over_and_resets_when_safe():
    first = CONTRACT["threshold"]["first_penalty"]
    step = CONTRACT["threshold"]["penalty_step"]
    assert penalty(new_tracker(wisdom=10, stress=11)) == first
    assert penalty(new_tracker(wisdom=10, stress=12)) == first + step
    assert penalty(new_tracker(wisdom=10, stress=10)) == 0


def test_gaining_stress_above_wisdom_flags_a_save_instead_of_rolling_one():
    t = new_tracker(wisdom=10, stress=9)
    apply_event(t, event_ids()[0], amount=2)
    assert t["awaiting_breakdown"] is True
    assert t["pending_save"]["required"] is True
    assert t["pending_save"]["kind"] == CONTRACT["threshold"]["save"], "the save belongs to CWN core"


def test_stress_never_goes_below_zero():
    t = new_tracker(wisdom=10, stress=0)
    recover(t, recovery_ids()[0])
    assert stress(t) == 0


def test_a_recovery_respects_its_per_day_limit():
    t = new_tracker(wisdom=10, stress=5)
    row = CONTRACT["recovery"]["events"][0]
    recover(t, row["id"])
    if row.get("per_day") == 1:
        with pytest.raises(StressError):
            recover(t, row["id"])
    assert t["recovered_today"][row["id"]] >= 1


def test_hardening_is_a_choice_that_clears_stress_and_leaves_a_scar():
    t = new_tracker(wisdom=10, stress=14)
    harden(t, "scar_of_the_first_case")
    assert stress(t) == CONTRACT["hardening"]["clears_stress_to"]
    assert t["hardening_count"] == 1
    assert t["scars"] == ["scar_of_the_first_case"]
    assert t["awaiting_breakdown"] is False


def test_an_unknown_event_is_an_error_not_a_zero():
    with pytest.raises(StressError):
        apply_event(new_tracker(wisdom=10), "had_a_bad_day")
