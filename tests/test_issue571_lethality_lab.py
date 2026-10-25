"""Executable contracts for the issue #571 lethality lab.

Code-only, per `AGENTS.md` and issue #271: these tests exercise the **measurement tool**,
not the prose of the design record and not any rulebook text.

The lab exists because #571 asks for a lethality comparison that is *measured* rather than
asserted. That only helps if the measurement itself is pinned:

* every distribution is a distribution (sums to exactly one, exact arithmetic, no sampling),
* the tool is deterministic — two calls cannot disagree,
* the two properties `rulebook/3_PHYSICAL.md` claims are preserved by the measurement
  (armour only ever softens; severity is monotonic in the margin),
* and the findings the record quotes are reproducible: layer A's removal probability falls
  as the target number rises and reaches **zero** above the attacker's reachable margin,
  while CWN's removal probability rises with damage and falls with Soak.

Run:
    python -m unittest discover -s tests -p "test_issue571_lethality_lab.py"
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

import issue571_lethality_lab as lab  # noqa: E402


def _total(distribution: dict) -> Fraction:
    return sum(distribution.values(), Fraction(0))


class ExactnessTests(unittest.TestCase):
    def test_layer_a_distributions_sum_to_one(self) -> None:
        for target in (9, 13, 15, 17, 21):
            self.assertEqual(_total(lab.layer_a_distribution(10, target)), Fraction(1))

    def test_layer_a_opposed_distribution_sums_to_one(self) -> None:
        distribution = lab.layer_a_opposed_distribution(10, defender_ref=5, defender_fray=5)
        self.assertEqual(_total(distribution), Fraction(1))

    def test_cwn_damage_is_a_probability_given_a_hit(self) -> None:
        for weapon in lab.CWN_WEAPONS:
            for target in lab.CWN_TARGETS:
                self.assertEqual(_total(lab.cwn_damage_distribution(weapon, target)), Fraction(1))

    def test_layer_b_outcomes_sum_to_one(self) -> None:
        self.assertEqual(_total(lab.layer_b_outcome_distribution(3, 2)), Fraction(1))

    def test_the_tool_is_deterministic(self) -> None:
        first = lab.build_report()
        second = lab.build_report()
        self.assertEqual(first, second)


class LadderPropertyTests(unittest.TestCase):
    """The two properties `rulebook/3_PHYSICAL.md` claims, measured rather than asserted."""

    def test_armour_never_makes_a_wound_more_severe(self) -> None:
        for target in (9, 13, 15, 17):
            bare = lab.layer_a_distribution(10, target)
            armoured = lab.layer_a_distribution(10, target, armor_steps_applied=1)
            self.assertGreaterEqual(lab.layer_a_removal_probability(armoured),
                                    Fraction(0))
            self.assertLessEqual(lab.layer_a_removal_probability(armoured),
                                 lab.layer_a_removal_probability(bare))

    def test_severity_falls_as_the_target_number_rises(self) -> None:
        removals = [
            lab.layer_a_removal_probability(lab.layer_a_distribution(10, target))
            for target in (9, 13, 15, 17, 21, 24, 29)
        ]
        self.assertEqual(removals, sorted(removals, reverse=True))

    def test_removal_becomes_impossible_above_the_reachable_margin(self) -> None:
        """`Down` needs margin >= 9, and `Critical` >= 5.

        A +10 attacker rolls 11..20, so at DV 17 the best reachable margin is 3 — a
        `Wounded`, never a removal. This is the measured form of the record's finding that
        layer A's lethality is *inverse* to difficulty.
        """
        self.assertEqual(lab.layer_a_removal_probability(lab.layer_a_distribution(10, 17)), Fraction(0))
        self.assertGreater(lab.layer_a_removal_probability(lab.layer_a_distribution(10, 15)), Fraction(0))
        self.assertGreater(lab.layer_a_removal_probability(lab.layer_a_distribution(10, 13)),
                           lab.layer_a_removal_probability(lab.layer_a_distribution(10, 15)))

    def test_a_miss_still_lands_on_the_least_severe_rung(self) -> None:
        """Layer A already carries a Shock-like idea: failure is not harmless."""
        distribution = lab.layer_a_distribution(0, 29)  # hopeless check
        self.assertEqual(_total(distribution), Fraction(1))
        self.assertEqual(distribution.get(lab.LADDER[0]), Fraction(1))


class CwnModelTests(unittest.TestCase):
    def test_soak_reduces_expected_damage(self) -> None:
        weapon = lab.CWN_WEAPONS[0]
        unarmoured, armoured = lab.CWN_TARGETS[0], lab.CWN_TARGETS[1]
        self.assertGreater(
            lab.cwn_expected_damage_per_attack(weapon, unarmoured, attack_bonus=3),
            lab.cwn_expected_damage_per_attack(weapon, armoured, attack_bonus=3),
        )

    def test_a_target_that_soaks_everything_is_never_removed(self) -> None:
        weapon = lab.CWN_WEAPONS[0]
        invulnerable = lab.CwnTarget("Invulnerable", ranged_ac=10, soak=100)
        self.assertIsNone(
            lab.cwn_expected_attacks_to_down(weapon, invulnerable, attack_bonus=3, hp=5)
        )
        self.assertEqual(
            lab.cwn_down_in_one_hit_probability(weapon, invulnerable, attack_bonus=3, hp=5),
            Fraction(0),
        )

    def test_a_single_heavy_hit_can_remove_a_one_hit_point_target(self) -> None:
        weapon = lab.CWN_WEAPONS[0]
        self.assertGreater(
            lab.cwn_down_in_one_hit_probability(
                weapon, lab.CWN_TARGETS[0], attack_bonus=3, hp=1
            ),
            Fraction(0),
        )

    def test_expected_attacks_are_finite_and_at_least_one(self) -> None:
        for weapon in lab.CWN_WEAPONS:
            for target in lab.CWN_TARGETS:
                attacks = lab.cwn_expected_attacks_to_down(
                    weapon, target, attack_bonus=3, hp=5
                )
                self.assertIsNotNone(attacks, f"{weapon.name} vs {target.label} is unkillable")
                self.assertGreaterEqual(attacks, Fraction(1))

    def test_soak_order_is_an_explicit_input_not_a_hidden_default(self) -> None:
        weapon, target = lab.CWN_WEAPONS[1], lab.CWN_TARGETS[1]
        after = lab.cwn_expected_damage_per_attack(
            weapon, target, attack_bonus=3, soak_before_trauma=False
        )
        before = lab.cwn_expected_damage_per_attack(
            weapon, target, attack_bonus=3, soak_before_trauma=True
        )
        self.assertNotEqual(after, before)


class HybridImportTests(unittest.TestCase):
    """The matrix's row 7 proposes CWN's Trauma Die as ladder adjudication. Measure it."""

    def test_trauma_on_the_ladder_only_ever_adds_severity(self) -> None:
        for target in (13, 15, 17):
            plain = lab.layer_a_removal_probability(lab.layer_a_distribution(10, target))
            trauma = lab.layer_a_removal_probability(lab.layer_a_with_trauma(10, target))
            self.assertGreaterEqual(trauma, plain)

    def test_trauma_creates_removals_the_ladder_cannot_produce(self) -> None:
        """At DV 17 the plain ladder cannot remove anyone; with Trauma it can."""
        plain = lab.layer_a_removal_probability(lab.layer_a_distribution(10, 17))
        trauma = lab.layer_a_removal_probability(lab.layer_a_with_trauma(10, 17))
        self.assertEqual(plain, Fraction(0))
        self.assertGreater(trauma, Fraction(0))


if __name__ == "__main__":
    unittest.main()
