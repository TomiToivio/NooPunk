"""Pins the 2d6 calibration numbers the design note relies on (#689).

The point of these tests is that the note's argument is arithmetic: if the table shifts,
the argument in `docs/design/NARRATIVE_LAYER_2D6_CALIBRATION.md` may no longer hold.
"""
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "narrative_layer_2d6_calibration.py"


def _module():
    spec = importlib.util.spec_from_file_location("calib", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_distribution_is_exact() -> None:
    module = _module()
    dist = module.distribution()
    assert abs(sum(dist.values()) - 1.0) < 1e-9
    assert dist[7] == pytest.approx(6 / 36)      # the mode
    assert dist[2] == pytest.approx(1 / 36)      # the extreme


def test_standard_difficulty_plus_two_stays_near_the_retired_4df_figure() -> None:
    """The note's headline: +30.6 pp on 2d6 vs +32.1 pp on 4dF."""
    module = _module()
    row = module.table()[8]
    assert row["shift2"] == pytest.approx(30.6, abs=0.1)


def test_one_step_is_worth_most_at_the_standard_difficulty() -> None:
    module = _module()
    table = module.table()
    assert table[8]["shift1"] > table[10]["shift1"]
    assert table[14]["shift1"] == pytest.approx(0.0, abs=0.1)


def test_stacking_four_does_not_reach_certainty() -> None:
    module = _module()
    assert module.table()[8]["plus4"] == pytest.approx(91.7, abs=0.1)


def test_hardest_difficulty_cannot_be_rescued_by_aspects() -> None:
    module = _module()
    assert module.table()[14]["plus2"] < 5.0
