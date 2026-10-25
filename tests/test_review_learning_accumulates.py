"""Regression tests: learning must actually advance, and training must accumulate.

Found by review on 2026-10-25 (second pass).

1. `NoopunkExtensions.NaturalPsi.learn` returns 0 on the first call, which *looks* like
   an off-by-one. It is not: 0 means "known but unrated" -- the discipline is in the
   dict, so it can hold Effort, but it has no rating yet, and the climb is 0,1,2,3,4.
   The original test asserts this, so the behaviour was left alone and only described.
   (Recorded because the temptation to "fix" it was real.)

2. `natural_psi.practice` computed `training_after` from the block's own hours only, so
   the report was wrong for anyone who had already trained: 100 accumulated hours plus a
   30-hour block is 130 hours (mastered), but it reported the tier for 30 hours alone.
   A player following the procedure would be told they were still merely practised.
"""
import unittest

from src.rules import natural_psi as psi
from src.rules import noopunk_extensions as ext


class LearnAdvancesTests(unittest.TestCase):
    """A discipline enters at 0 = known-but-unrated, then climbs to the cap."""

    def test_the_first_learn_unlocks_at_zero(self) -> None:
        p = ext.NaturalPsi()
        self.assertEqual(p.learn("telepathy"), 0)
        self.assertEqual(p.disciplines["telepathy"], 0,
                         "0 is the documented 'known but unrated' state, not a failure")

    def test_learning_climbs_one_step_at_a_time(self) -> None:
        p = ext.NaturalPsi()
        seen = [p.learn("telepathy") for _ in range(5)]
        self.assertEqual(seen, [0, 1, 2, 3, 4])

    def test_a_sixth_learn_is_refused(self) -> None:
        p = ext.NaturalPsi()
        for _ in range(5):
            p.learn("telepathy")
        with self.assertRaises(ValueError):
            p.learn("telepathy")

    def test_a_discipline_learned_once_can_hold_effort(self) -> None:
        p = ext.NaturalPsi(capacity=2)
        p.learn("telepathy")
        p.commit("link-1", "telepathy", 1)   # presence, not rating, is what gates Effort
        self.assertEqual(p.used, 1)


class PracticeAccumulatesTests(unittest.TestCase):
    def test_training_is_computed_from_prior_hours_plus_the_block(self) -> None:
        block = psi.practice(psi.Discipline.ESP, hours=30, prior_hours=100)
        self.assertEqual(block["hours"], 30)
        self.assertEqual(block["training_after"], psi.Training.MASTERED.value,
                         "100 + 30 hours is past the mastery threshold, not merely practised")

    def test_prior_hours_alone_can_carry_a_short_block_over_the_threshold(self) -> None:
        below = psi.practice(psi.Discipline.ESP, hours=10, prior_hours=0)
        above = psi.practice(psi.Discipline.ESP, hours=10, prior_hours=15)
        self.assertEqual(below["training_after"], psi.Training.UNTRAINED.value)
        self.assertEqual(above["training_after"], psi.Training.PRACTISED.value)

    def test_unsupervised_hours_still_count_half_on_top_of_prior_hours(self) -> None:
        block = psi.practice(psi.Discipline.ESP, hours=40, supervised=False, prior_hours=0)
        self.assertEqual(block["hours"], 20)
        self.assertEqual(block["training_after"], psi.Training.PRACTISED.value)

    def test_prior_hours_must_not_be_negative(self) -> None:
        with self.assertRaises(psi.PsiError):
            psi.practice(psi.Discipline.ESP, hours=1, prior_hours=-1)

    def test_defaults_still_work_with_no_prior_hours(self) -> None:
        block = psi.practice(psi.Discipline.ESP, hours=psi.TUNING_MIN_PRACTICE)
        self.assertEqual(block["training_after"], psi.Training.PRACTISED.value)


if __name__ == "__main__":
    unittest.main()
