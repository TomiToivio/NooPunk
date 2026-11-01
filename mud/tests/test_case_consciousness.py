"""The deterministic consciousness-assessment case (#985)."""
from __future__ import annotations

import itertools

import pytest

from nopunk_mud.case_consciousness import SCENES, run_case


def test_default_interview_yields_an_assessment_and_three_clues():
    result = run_case()
    assert result.assessment.classification in {
        "baseline_human", "uncertain", "atypical", "nonconscious_pattern", "nhi_nonanthropocentric"}
    assert len(result.clues) == 3
    assert result.assessment.core_clue
    assert len(result.transcript) == 3


def test_every_choice_path_keeps_the_core_clue_and_progress():
    options = [list(scene["choices"]) for scene in SCENES]
    for combo in itertools.product(*options):
        result = run_case(combo)
        assert len(result.clues) == 3
        assert result.assessment.core_clue
        assert result.transcript


def test_deterministic():
    first, second = run_case(("press", "confront", "conceal")), run_case(("press", "confront", "conceal"))
    assert first == second


def test_invalid_choice_and_length_are_refused():
    with pytest.raises(ValueError):
        run_case(("press", "mirror"))
    with pytest.raises(ValueError):
        run_case(("press", "nonsense", "show"))
