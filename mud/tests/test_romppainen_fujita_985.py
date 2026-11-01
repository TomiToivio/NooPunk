"""Romppainen–Fujita overlay: safety, persistence, investigation (#985)."""
import itertools

import pytest

from nopunk_mud.case_consciousness import SCENES, run_case
from nopunk_mud.romppainen_fujita import (
    DAILY_LIMIT, DeviceUnavailable, Use, available, perform,
)


def take(record=None, day=1, office="Helsinki", a=True, s=True):
    return perform(record, day=day, office=office,
                   administrator_helmet=a, subject_helmet=s)


def test_two_helmets_are_required_and_refusal_spends_nothing():
    with pytest.raises(DeviceUnavailable, match="Both"):
        take(a=False)
    with pytest.raises(DeviceUnavailable, match="Both"):
        take(s=False)
    assert available(None, day=1) == DAILY_LIMIT


def test_helsinki_only():
    with pytest.raises(DeviceUnavailable, match="Helsinki"):
        take(office="Tampere")


def test_four_tests_and_daily_reset_and_serialized_state():
    record = None
    for n in range(1, 5):
        use = take(record)
        assert use.count == n
        record = use.to_dict()
        assert Use.from_dict(record, day=1) == use
    with pytest.raises(DeviceUnavailable, match="Four"):
        take(record)
    assert available(record, day=1) == 0
    assert available(record, day=2) == 4
    assert take(record, day=2).count == 1


def test_no_clock_rollback_or_corrupted_state():
    with pytest.raises(DeviceUnavailable):
        take({"day": 2, "count": 1}, day=1)
    with pytest.raises(DeviceUnavailable):
        take({"day": 1, "count": 5})
    with pytest.raises(DeviceUnavailable):
        take({"day": 1, "count": True})
    with pytest.raises(DeviceUnavailable):
        take(day=-1)


def test_rejected_test_never_removes_investigative_clues():
    record = {"day": 1, "count": 4}
    with pytest.raises(DeviceUnavailable):
        take(record)
    for choices in itertools.product(*(scene["choices"] for scene in SCENES)):
        case = run_case(choices)
        assert len(case.clues) == len(SCENES)
        assert case.assessment.core_clue


def test_protocol_is_named_without_claiming_metaphysical_certainty():
    result = run_case()
    assert result.assessment.protocol == "romppainen_fujita"
    assert any("not proof" in note.lower() for note in result.assessment.caveats)
