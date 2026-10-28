"""Pin the measured numbers the narrative layer's safety rules rest on (#697).

The rulebook claims a one-step invoke is worth "+16.7 pp at difficulty 8" and "+0.0 pp at 14". Those
are load-bearing claims: if they drift, the text is lying and the difficulty-dependence argument
collapses. This test recomputes them from the calibration tool by exact enumeration and pins them, so
a change to either the tool or the prose fails here rather than in a session.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


calibration = _load(ROOT / "tools" / "narrative_layer_2d6_calibration.py", "calibration_2d6")
narrative = _load(ROOT / "src" / "rules" / "narrative_layer.py", "narrative_layer_pinned")


class TestCalibrationIsExact:
    def test_the_die_is_two_d6_over_36_outcomes(self):
        dist = calibration.distribution()
        assert sum(dist.values()) == pytest.approx(1.0)
        assert min(dist) == 2 and max(dist) == 12
        assert dist[7] == pytest.approx(6 / 36)

    def test_success_at_the_standard_difficulty(self):
        # The rulebook states 15 of 36 (41.7%) at difficulty 8.
        assert calibration.success_probability(0, 8, calibration.distribution()) == pytest.approx(15 / 36)

    def test_one_step_is_worth_16_7_points_at_dv_8(self):
        table = calibration.table()
        assert table[8]["shift1"] == pytest.approx(16.7)

    def test_one_step_is_worth_nothing_at_dv_14(self):
        # The claim the rulebook now makes: an invoke cannot rescue an impossible check.
        table = calibration.table()
        assert table[12]["shift1"] == pytest.approx(5.6)
        assert table[14]["base"] == pytest.approx(0.0)
        assert table[14]["shift1"] == pytest.approx(0.0)

    def test_two_steps_at_dv_8_would_be_30_6_points(self):
        # Why the stacking cap exists, measured. The tool round from unrounded probabilities,
        # so 72.22 - 41.67 = 30.56 reports as 30.6, not 30.5.
        table = calibration.table()
        assert table[8]["shift2"] == pytest.approx(30.6)


class TestBandsMatchTheCalibration:
    def test_the_band_boundaries_are_the_ones_the_rulebook_names(self):
        assert narrative.band_for(0) == "cost"
        assert narrative.band_for(1) == "cost"
        assert narrative.band_for(2) == "clean"
        assert narrative.band_for(-1) == "miss"

    def test_the_retired_d10_vocabulary_is_gone(self):
        retired = {"brutal", "severe", "solid", "glancing"}
        assert retired.isdisjoint(set(narrative.BAND_TO_MOVE)), (
            "the d10 band names must not survive the 2d6 re-anchoring"
        )
        assert set(narrative.BAND_TO_MOVE) == set(narrative.OUTCOME_BANDS)

    def test_one_invoke_per_roll_is_enforced(self):
        assert narrative.MAX_INVOCATIONS_PER_ROLL == 1
        assert narrative.can_invoke(0) is True
        assert narrative.can_invoke(1) is False
        assert narrative.invoke_step() == 1

    def test_the_rulebook_states_the_difficulty_dependence(self):
        text = (ROOT / "rulebook" / "19_NARRATIVE_LAYER.md").read_text(encoding="utf-8")
        assert "+16.7 pp at difficulty 8" in text
        assert "+0.0 pp at difficulty 14" in text
