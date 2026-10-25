"""Executable contracts for the issue #564 kernel comparison (D40 / #566 input).

Code-only, per `AGENTS.md` and issue #271: these tests exercise the **measurement tool**, not the
prose of the design record and not any rulebook text.

The tool exists because D40 asks which kernel NoöPunk should use and that question has only ever been
argued from familiarity. What is pinned here is that the measurement is *exact* and that the three
qualitative claims the record makes are properties of the tools, not opinions:

* `1d10` is **flat** — every point of competence is worth exactly 10 percentage points;
* `2d6` is a **bell** — a point is worth 5.6–16.7 points depending on where the contest sits, and the
  extremes compress (a master rarely botches);
* `4dF` is a **triangle** — the steepest point is the middle, and its four bands put ~20 % of typical
  contests on a tie, which `1d10` and `2d6` cannot express without an extra rule.

Run:
    python -m unittest discover -s tests -p "test_issue564_kernel_comparison.py"
"""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import issue564_kernel_comparison as lab  # noqa: E402


class ExactnessTests(unittest.TestCase):
    def test_dice_distributions_have_the_right_totals(self) -> None:
        self.assertEqual(sum(lab.d_sums(1, 10).values()), 10)
        self.assertEqual(sum(lab.d_sums(2, 6).values()), 36)
        self.assertEqual(sum(lab.fate_sums().values()), 81)

    def test_probabilities_are_confined_to_zero_and_one(self) -> None:
        for kernel in lab.KERNELS:
            for delta, p in lab.delta_curve(kernel).items():
                self.assertGreaterEqual(p, Fraction(0), f"{kernel} {delta}")
                self.assertLessEqual(p, Fraction(1), f"{kernel} {delta}")

    def test_the_tool_is_deterministic(self) -> None:
        self.assertEqual(lab.build_report(), lab.build_report())


class KernelShapeTests(unittest.TestCase):
    def test_1d10_is_flat(self) -> None:
        """The property that makes layer A transparent — and gives a novice a 10 % chance."""
        low, high = lab.uncertain_window("layer_a_1d10")
        for delta in range(low, high):
            self.assertEqual(lab.marginal_gain("layer_a_1d10", delta), Fraction(1, 10))

    def test_2d6_is_a_bell(self) -> None:
        low, high = lab.uncertain_window("wn_2d6")
        gains = [lab.marginal_gain("wn_2d6", d) for d in range(low, high)]
        self.assertGreater(max(gains), min(gains))
        self.assertEqual(max(gains), Fraction(6, 36))  # the +1 that turns "8+" into "7+"

    def test_4dF_gains_follow_its_triangle(self) -> None:
        """A +1 is worth the probability of the single outcome it exactly adds: the 4dF pmf."""
        low, high = lab.uncertain_window("fate_4dF")
        gains = [lab.marginal_gain("fate_4dF", d) for d in range(low, high)]
        peak = gains.index(max(gains))
        self.assertEqual(gains[:peak], sorted(gains[:peak]))            # rising to the middle
        self.assertEqual(gains[peak:], sorted(gains[peak:], reverse=True))  # falling after it
        self.assertEqual(max(gains), Fraction(19, 81))                  # the tie band's weight

    def test_bells_compress_the_far_tail_more_than_the_flat_die(self) -> None:
        """The flat die always gives the underdog 10 %; the bell gives 2.8 % and the triangle 1.2 %."""
        smallest = {}
        for kernel in ("layer_a_1d10", "wn_2d6", "fate_4dF"):
            low, _ = lab.uncertain_window(kernel)
            smallest[kernel] = lab.success_probability(kernel, 0, -low)
        self.assertEqual(smallest["layer_a_1d10"], Fraction(1, 10))
        self.assertEqual(smallest["wn_2d6"], Fraction(1, 36))
        self.assertEqual(smallest["fate_4dF"], Fraction(1, 81))


class PublishedValueTests(unittest.TestCase):
    """Known values, so a future edit cannot quietly change the dice."""

    def test_2d6_known_values(self) -> None:
        self.assertEqual(lab.success_probability("wn_2d6", 0, 7), Fraction(21, 36))
        self.assertEqual(lab.success_probability("wn_2d6", 0, 8), Fraction(15, 36))
        self.assertEqual(lab.success_probability("wn_2d6", 0, 12), Fraction(1, 36))

    def test_fate_known_values(self) -> None:
        self.assertEqual(lab.fate_sums()[4], 1)
        self.assertEqual(lab.success_probability("fate_4dF", 0, 4), Fraction(1, 81))
        self.assertEqual(lab.success_probability("fate_4dF", 0, 0), Fraction(50, 81))  # tie counts

    def test_fate_tie_band_is_a_fifth_of_a_matched_contest(self) -> None:
        bands = lab.fate_bands_at(3, 2)
        self.assertEqual(bands["tie — succeed at a minor cost"], Fraction(16, 81))
        self.assertAlmostEqual(sum(bands.values()), 1.0)


class LadderFitTests(unittest.TestCase):
    def test_layer_a_ladder_exceeds_what_the_die_can_reach(self) -> None:
        """At `+10` the top three rungs of the authored ladder are unreachable — the #571 finding."""
        impossible = [row["target"] for row in lab.success_curve("layer_a_1d10", 10) if row["impossible"]]
        self.assertEqual(impossible, [21, 24, 29])

    def test_the_without_number_ladder_fits_inside_its_die(self) -> None:
        curve = lab.success_curve("wn_2d6", 2)
        self.assertTrue(all(0 < row["probability"] < 1 for row in curve),
                        "every WN rung should be contested at a typical bonus")


if __name__ == "__main__":
    unittest.main()
