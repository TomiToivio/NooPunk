"""Romppainen consciousness assessment (#985): deterministic, honest, never blocks the clue."""
from __future__ import annotations

import pytest

from nopunk_mud.consciousness import AssessmentError, Signals, assess


def test_consistent_human_baseline():
    result = assess(Signals(affect=2, coherence=2, bci=2, empathy=2))
    assert result.score == 100
    assert result.classification == "baseline_human"
    assert 0.5 <= result.confidence <= 0.95


def test_simulated_affect_without_interior_account():
    result = assess(Signals(affect=1, coherence=-2, bci=0, empathy=-2))
    assert result.classification == "nonconscious_pattern"


def test_coherent_nhi_fails_anthropocentric_empathy():
    result = assess(Signals(affect=0, coherence=2, bci=0, empathy=-2))
    assert result.classification == "nhi_nonanthropocentric"
    assert "anthropocentric" in " ".join(result.caveats).lower()


def test_uncertain_band_when_signals_mixed():
    result = assess(Signals(affect=1, coherence=0, bci=1, empathy=0))
    assert result.classification == "uncertain"
    assert result.confidence <= 0.6


def test_core_clue_is_never_empty_whatever_the_score():
    for signals in (Signals(2, 2, 2, 2), Signals(-2, -2, -2, -2), Signals(0, 0, 0, 0)):
        result = assess(signals)
        assert result.core_clue
        assert result.strongest_channel in {"affect", "coherence", "bci", "empathy"}


def test_deterministic_for_same_signals():
    signals = Signals(1, -1, 2, 0)
    assert assess(signals) == assess(signals)


def test_invalid_signals_are_refused():
    with pytest.raises(AssessmentError):
        assess(Signals(3, 0, 0, 0))
    with pytest.raises(AssessmentError):
        assess(Signals(0, 0, 0, 0, psi=5))


def test_psi_channel_adds_a_caveat_not_a_requirement():
    without = assess(Signals(1, 1, 1, 1))
    with_psi = assess(Signals(1, 1, 1, 1, psi=1))
    assert any("No psychotronic" in caveat for caveat in without.caveats)
    assert not any("No psychotronic" in caveat for caveat in with_psi.caveats)
