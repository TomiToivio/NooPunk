"""Pin the measured numbers the narrative layer's safety rules rest on (#697).

These tests recompute the numbers from the repository's own calibration tool rather than restating
them, and pin the code-level vocabulary the bands use.

**No rulebook assertions here:** issue #271 makes automated tests the business of executable game code
only. The rulebook's prose is Tomi's to review editorially, so whether it states the DV-14 pricing is a
reading task, not a test.

Stdlib unittest only — the repository's CI has no pytest.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _load_calibration():
    path = ROOT / "tools" / "narrative_layer_2d6_calibration.py"
    spec = importlib.util.spec_from_file_location("nl_calibration", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cal = _load_calibration()


class TestTheCalibrationNumbers(unittest.TestCase):
    def test_standard_difficulty_is_15_of_36(self):
        row = cal.table()[8]
        self.assertAlmostEqual(row["base"], 41.7, places=1)
        self.assertEqual(round(row["base"] * 36 / 100), 15)

    def test_a_step_is_16_7_points_at_dv_8(self):
        row = cal.table()[8]
        self.assertAlmostEqual(row["shift1"], 16.7, places=1)

    def test_two_steps_are_30_6_not_30_5(self):
        # The tool rounds from unrounded probabilities: 72.22 - 41.67 = 30.56 -> 30.6.
        self.assertAlmostEqual(cal.table()[8]["shift2"], 30.6, places=1)

    def test_a_step_is_worth_nothing_at_dv_14(self):
        row = cal.table()[14]
        self.assertEqual(row["base"], 0.0)
        self.assertEqual(row["shift1"], 0.0)

    def test_the_curve_is_monotonic(self):
        values = [cal.table()[d]["shift1"] for d in (8, 10, 12, 14)]
        self.assertEqual(values, sorted(values, reverse=True))


class TestTheRetiredVocabularyIsGone(unittest.TestCase):
    def test_d10_band_names_are_not_keys_of_the_band_map(self):
        from src.rules import narrative_layer as nl

        for retired in ("brutal", "severe", "solid", "glancing"):
            self.assertNotIn(retired, nl.BAND_TO_MOVE)

    def test_the_band_map_uses_the_wn_bands(self):
        from src.rules import narrative_layer as nl

        self.assertEqual(set(nl.BAND_TO_MOVE), {"miss", "cost", "clean", "style"})

    def test_one_invoke_per_roll_is_still_the_cap(self):
        from src.rules import narrative_layer as nl

        self.assertEqual(nl.MAX_INVOCATIONS_PER_ROLL, 1)


if __name__ == "__main__":
    unittest.main()
