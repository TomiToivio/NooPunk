from __future__ import annotations

import pytest

from src.therapy import (
    CheckResult,
    Choice,
    AttributeCheck,
    TherapyScene,
    build_empty_therapy_session,
    evaluate_check,
)


def test_check_uses_fate_result_levels() -> None:
    assert evaluate_check(2, -4, 2) is CheckResult.FAILURE
    assert evaluate_check(2, 0, 2) is CheckResult.TIE
    assert evaluate_check(2, 1, 2) is CheckResult.SUCCESS
    assert evaluate_check(2, 3, 2) is CheckResult.SUCCESS_WITH_STYLE


def test_choice_routes_check_results_without_story_content() -> None:
    choice = Choice(
        id="choice_a",
        text="[toimintavaihtoehto]",
        attribute_check=AttributeCheck("Awareness", 2),
        result_scenes={
            CheckResult.FAILURE: "branch_failure",
            CheckResult.SUCCESS: "branch_success",
        },
    )

    assert choice.destination_for(CheckResult.FAILURE) == "branch_failure"
    assert choice.destination_for(CheckResult.SUCCESS) == "branch_success"
    assert choice.destination_for(CheckResult.TIE) is None


def test_empty_day_one_session_has_no_scripted_content() -> None:
    session = build_empty_therapy_session()
    assert session.day == 1
    assert session.first_scene() is None

    session.add_scene(TherapyScene("scene", "[otsikko]", "[tilanne]"))
    with pytest.raises(ValueError, match="jo käytössä"):
        session.add_scene(TherapyScene("scene", "[otsikko]", "[tilanne]"))
