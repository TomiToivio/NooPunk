"""Guard for issue #217 AC2's resolution semantics.

The two things worth guarding here are not "does the function return something" but:

 1. **Order** — the untrained penalty composes with all three candidates because it is applied
    *after* the combination. Folding it into one candidate would pass a naive test and silently
    make the rule candidate-specific.
 2. **Non-change** — the partial-success band is opt-in precisely so the shipped bands do not
    move. ``PARTIAL_OFF`` must reproduce the prototype's bands exactly, for every margin, or the
    "off" setting is a lie.
"""
from __future__ import annotations

import unittest
from fractions import Fraction
from typing import Any, cast

from src.rules import issue217_resolution as r
from src.rules import kernel_prototype as kp
from src.rules.core import resolve_check


class TrainedAndUntrainedTests(unittest.TestCase):
    def test_the_penalty_is_minus_one_and_the_module_is_not_canonical(self):
        self.assertEqual(r.UNTRAINED_STEP_PENALTY, -1)
        self.assertIs(r.IS_CANONICAL, False)

    def test_training_is_applied_after_the_combination_for_every_candidate(self):
        """Composition, not baked into one candidate."""
        for name in sorted(kp.CANDIDATES):
            with self.subTest(candidate=name):
                raw = kp.clamp_step(kp.CANDIDATES[name](5, 5))
                self.assertEqual(
                    r.combined_step(name, 5, 5, trained=False),
                    kp.clamp_step(raw + r.UNTRAINED_STEP_PENALTY),
                )
                self.assertEqual(r.combined_step(name, 5, 5, trained=True), raw)

    def test_untrained_never_raises_the_step(self):
        for name in sorted(kp.CANDIDATES):
            for stat in range(1, 11):
                for skill in range(1, 11):
                    with self.subTest(candidate=name, stat=stat, skill=skill):
                        self.assertLessEqual(
                            r.combined_step(name, stat, skill, trained=False),
                            r.combined_step(name, stat, skill, trained=True),
                        )

    def test_the_penalty_clamps_at_the_ladder_floor(self):
        low, _high = r.ladder_bounds()
        floor = min(
            r.combined_step("C_skill_primary", stat, skill, trained=True)
            for stat in range(1, 11) for skill in range(1, 11)
        )
        self.assertGreaterEqual(floor + r.UNTRAINED_STEP_PENALTY, low - 1)
        self.assertGreaterEqual(r.apply_training(low, trained=False), low)

    def test_untrained_never_improves_the_odds_and_the_measured_cost_matches(self):
        for name in sorted(kp.CANDIDATES):
            with self.subTest(candidate=name):
                trained = r.p_success_at_least(candidate=name, stat=5, skill=5, difficulty=0)
                untrained = r.p_success_at_least(
                    candidate=name, stat=5, skill=5, difficulty=0, trained=False
                )
                self.assertLessEqual(untrained, trained)
                self.assertEqual(
                    r.untrained_cost(candidate=name, stat=5, skill=5, difficulty=0),
                    trained - untrained,
                )
                self.assertGreater(r.untrained_cost(candidate=name), Fraction(0))


class PartialSuccessIsOptInTests(unittest.TestCase):
    def test_off_reproduces_the_prototype_bands_for_every_margin(self):
        """The 'off' setting must be the shipped behaviour, not a near-miss of it."""
        for margin in range(-8, 9):
            with self.subTest(margin=margin):
                if margin < 0:
                    expected = "failure"
                elif margin < kp.SUCCESS_WITH_STYLE_MARGIN:
                    expected = "success"
                else:
                    expected = "success_with_style"
                self.assertEqual(r.outcome_for(margin, partial=r.PARTIAL_OFF), expected)

    def test_at_minus_one_converts_only_a_one_step_miss(self):
        self.assertEqual(r.outcome_for(-1, partial=r.PARTIAL_AT_MINUS_ONE), "partial")
        for margin in (-2, -3, -8):
            with self.subTest(margin=margin):
                self.assertEqual(r.outcome_for(margin, partial=r.PARTIAL_AT_MINUS_ONE), "failure")
        for margin in (0, 1, 2, 3):
            with self.subTest(margin=margin):
                self.assertEqual(
                    r.outcome_for(margin, partial=r.PARTIAL_AT_MINUS_ONE),
                    r.outcome_for(margin, partial=r.PARTIAL_OFF),
                )

    def test_at_zero_moves_the_boundary_of_success_which_is_why_it_is_not_the_default(self):
        self.assertEqual(r.outcome_for(0, partial=r.PARTIAL_AT_ZERO), "partial")
        self.assertEqual(r.outcome_for(1, partial=r.PARTIAL_AT_ZERO), "success")
        # it makes full success strictly harder than the off policy does
        self.assertNotEqual(
            r.outcome_for(0, partial=r.PARTIAL_AT_ZERO),
            r.outcome_for(0, partial=r.PARTIAL_OFF),
        )

    def test_an_unknown_policy_is_refused(self):
        with self.assertRaises(ValueError):
            # Deliberately outside the union: the refusal must be runtime, not only static.
            r.outcome_for(0, partial=cast(Any, "whenever"))


class ExactProbabilityTests(unittest.TestCase):
    def test_the_4df_distribution_is_exact_and_well_formed(self):
        dist = r.FDF_DISTRIBUTION
        self.assertEqual(sum(dist.values()), Fraction(1))
        self.assertEqual(sum(dist.values()) * 81, Fraction(81))
        self.assertEqual(min(dist), -4)
        self.assertEqual(max(dist), 4)
        self.assertEqual(dist[0], Fraction(19, 81))
        for total in (-4, -3, -2, -1):
            with self.subTest(total=total):
                self.assertEqual(dist[total], dist[-total])

    def test_bands_sum_to_exactly_one_over_a_sweep(self):
        for difficulty in range(-4, 5):
            for trained in (True, False):
                with self.subTest(difficulty=difficulty, trained=trained):
                    dist = r.outcome_distribution(
                        candidate="C_skill_primary", stat=5, skill=5,
                        difficulty=difficulty, trained=trained,
                    )
                    self.assertEqual(sum(dist.values()), Fraction(1))
                    self.assertEqual(set(dist), set(r.OUTCOMES))

    def test_p_success_at_least_agrees_with_the_off_distribution(self):
        """Ties the threshold to the band definition: success or better, and no partial.

        Without this, the threshold itself is unpinned -- `>= 0` and `> 0` differ only in the
        margin-0 case, which a trained-vs-untrained comparison cannot see because both sides
        move together.
        """
        for difficulty in range(-3, 4):
            with self.subTest(difficulty=difficulty):
                dist = r.outcome_distribution(
                    candidate="C_skill_primary", stat=5, skill=5,
                    difficulty=difficulty, partial=r.PARTIAL_OFF,
                )
                self.assertEqual(
                    r.p_success_at_least(
                        candidate="C_skill_primary", stat=5, skill=5, difficulty=difficulty
                    ),
                    dist["success"] + dist["success_with_style"],
                )

    def test_probability_falls_as_difficulty_rises(self):
        previous = None
        for step in range(-4, 5):
            with self.subTest(difficulty=step):
                value = r.p_success_at_least(
                    candidate="C_skill_primary", stat=5, skill=5, difficulty=step
                )
                if previous is not None:
                    self.assertLessEqual(value, previous)
                previous = value


class NothingShippedWasChangedTests(unittest.TestCase):
    def test_the_canonical_1d10_check_is_still_the_shipped_engine(self):
        result = resolve_check(stat=5, skill=5, target=15, die=7)
        self.assertTrue(result.success)
        self.assertEqual(result.total, 17)
        self.assertFalse(resolve_check(stat=1, skill=1, target=15, die=1).success)

    def test_the_recommended_candidate_is_one_the_prototype_defines(self):
        self.assertIn(r.default_candidate(), kp.CANDIDATES)


if __name__ == "__main__":
    unittest.main()
