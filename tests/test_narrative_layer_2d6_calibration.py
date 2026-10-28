"""Pins the 2d6 calibration numbers the design note relies on (#689).

The note's argument is arithmetic: if the table shifts, what it claims about the aspect
layer's safety rules may no longer hold. These tests are the load-bearing numbers.

unittest rather than pytest, because the repository's CI discovers with unittest and does
not install pytest.
"""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "narrative_layer_2d6_calibration.py"


def _module():
    spec = importlib.util.spec_from_file_location("calib", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DistributionTest(unittest.TestCase):
    def test_distribution_is_exact(self):
        dist = _module().distribution()
        self.assertAlmostEqual(sum(dist.values()), 1.0, places=9)
        self.assertAlmostEqual(dist[7], 6 / 36, places=9)   # the mode
        self.assertAlmostEqual(dist[2], 1 / 36, places=9)   # the extreme

    def test_every_total_from_two_to_twelve_is_present(self):
        self.assertEqual(sorted(_module().distribution()), list(range(2, 13)))


class CalibrationTest(unittest.TestCase):
    def test_standard_difficulty_plus_two_stays_near_the_retired_4df_figure(self):
        """The note's headline: +30.6 pp on 2d6 against +32.1 pp on 4dF."""
        self.assertAlmostEqual(_module().table()[8]["shift2"], 30.6, places=1)

    def test_one_step_is_worth_most_at_the_standard_difficulty(self):
        table = _module().table()
        self.assertGreater(table[8]["shift1"], table[10]["shift1"])

    def test_the_hardest_difficulty_cannot_be_rescued_by_one_step(self):
        self.assertAlmostEqual(_module().table()[14]["shift1"], 0.0, places=1)

    def test_stacking_four_does_not_reach_certainty(self):
        """91.7% is the finding: near-certain, so failure looks like bad luck."""
        self.assertAlmostEqual(_module().table()[8]["plus4"], 91.7, places=1)

    def test_easy_difficulty_is_above_seventy_percent_without_aspects(self):
        self.assertAlmostEqual(_module().table()[6]["base"], 72.2, places=1)


if __name__ == "__main__":
    unittest.main()
