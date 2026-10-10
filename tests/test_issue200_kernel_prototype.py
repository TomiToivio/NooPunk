"""Tests for the issue #200 kernel prototype.

Two jobs, in priority order:

1. **Prove the prototype stayed a prototype.** It must not have quietly become the
   engine. #200's numerical migration is an author decision; ``AGENTS.md`` sections 13.9
   and 15.2 fix the current 1-10 + 1d10 baseline and section 13.8 forbids silently
   redesigning it. So the canonical files are asserted *unchanged* here, not merely
   "still passing elsewhere".
2. **Pin the properties that hold whatever the author later chooses** — the ladder's
   bounds, the candidate ranges, the stacking cap, opposed-check symmetry, and the fact
   that the legacy benchmark still reproduces the probabilities recorded in
   ``data/rules/core.json``. If a number in
   ``docs/design/ISSUE_200_KERNEL_PROTOTYPE.md`` stops being true, that is a bug in this
   file's subject matter, not a docs nit.
"""

from __future__ import annotations

import json
import random
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import core
from rules import kernel_prototype as kp


class FixedDice:
    """Feeds exact 4dF rolls: values are consumed three at a time (0..2 → -1..+1)."""

    def __init__(self, faces: list[int]) -> None:
        self.faces = list(faces)

    def randint(self, a: int, b: int) -> int:
        return self.faces.pop(0)


class PrototypeBoundaryTests(unittest.TestCase):
    """The prototype must not be the engine."""

    def test_the_module_declares_itself_non_canonical(self) -> None:
        self.assertFalse(kp.IS_CANONICAL)

    def test_the_canonical_check_is_still_the_authored_d10(self) -> None:
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        self.assertEqual(canon["skill_check"]["dice"], "1d10")
        self.assertEqual(canon["skill_check"]["formula"], "STAT + Skill + 1d10")
        self.assertEqual(canon["_canon_revision"], "issue-111-d10-independent")

    def test_the_canonical_resolver_still_behaves_as_authored(self) -> None:
        """STAT 5 + Skill 5 + a fixed die 5 is 15, and 15 >= 15 succeeds. Unchanged."""
        result = core.resolve_check(stat=5, skill=5, target=15, die=5)
        self.assertEqual((result.total, result.success), (15, True))
        result = core.resolve_check(stat=5, skill=5, target=16, die=5)
        self.assertEqual((result.total, result.success), (15, False))

    def test_the_prototype_does_not_reimplement_the_legacy_check(self) -> None:
        """It delegates to the canonical engine, so the benchmark cannot drift."""
        self.assertIs(kp.resolve_legacy(stat=5, skill=5, target=15, die=5).success, True)
        self.assertEqual(kp.resolve_legacy(stat=5, skill=5, target=15, die=5).total, 15)


class LegacyBenchmarkTests(unittest.TestCase):
    """The benchmark must reproduce the canon's own recorded numbers."""

    def test_the_recorded_probability_examples_still_hold(self) -> None:
        """Every profile the canon recorded, not just the headline one.

        ``data/rules/core.json`` records five fixed STAT+Skill profiles against all seven
        authored DVs. Reproducing all of them is what makes the benchmark trustworthy as a
        migration baseline; reproducing one would be a sample.
        """
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        profiles = {
            key: value for key, value in canon["probability_examples"].items()
            if not key.startswith("_")
        }
        self.assertEqual(len(profiles), 5, "the recorded profiles moved")

        checked = 0
        for label, by_dv in profiles.items():
            match = re.search(r"STAT (\d+) \+ Skill (\d+)", label)
            self.assertIsNotNone(match, f"unparseable recorded profile {label!r}")
            stat, skill = (int(g) for g in match.groups())
            for dv_text, recorded in by_dv.items():
                measured = kp.p_success_legacy(
                    stat=stat, skill=skill, target=int(dv_text), trials=60_000, seed=99 + int(dv_text)
                )
                with self.subTest(profile=label, dv=dv_text):
                    self.assertAlmostEqual(measured, float(recorded), delta=0.012)
                checked += 1
        self.assertEqual(checked, 35, "expected 5 profiles x 7 difficulties")

    def test_the_benchmark_saturates_the_way_the_doc_claims(self) -> None:
        """A specialist auto-succeeds at Everyday; a weak character cannot at Professional."""
        specialist = kp.p_success_legacy(stat=8, skill=8, target=13, trials=4_000, seed=7)
        weak = kp.p_success_legacy(stat=2, skill=1, target=17, trials=4_000, seed=7)
        self.assertGreater(specialist, 0.98)
        self.assertLess(weak, 0.01)


class LadderTests(unittest.TestCase):
    def test_rating_mapping_is_monotonic_and_bounded(self) -> None:
        steps = [kp.rating_step(r) for r in range(1, 11)]
        self.assertEqual(steps, sorted(steps), "the step mapping must not go backwards")
        self.assertTrue(all(kp.LADDER_MIN <= s <= kp.LADDER_MAX for s in steps))
        self.assertEqual((steps[0], steps[-1]), (kp.LADDER_MIN, kp.LADDER_MAX))

    def test_ratings_outside_the_authored_range_are_rejected(self) -> None:
        for bad in (0, 11):
            with self.subTest(rating=bad), self.assertRaises(ValueError):
                kp.rating_step(bad)

    def test_every_candidate_keeps_attributes_and_skills_separate(self) -> None:
        """#200: the separate Attribute/Skill split is not optional."""
        for name, combine in kp.CANDIDATES.items():
            with self.subTest(candidate=name):
                # a Skill change must move the result; a STAT change must too
                self.assertNotEqual(combine(5, 2), combine(5, 9), "Skill stopped mattering")
                self.assertNotEqual(combine(2, 5), combine(9, 5), "STAT stopped mattering")

    def test_candidate_ranges_match_the_documented_claim(self) -> None:
        raws = {
            "A_additive": lambda s, k: kp.rating_step(s) + kp.rating_step(k),
            "C_skill_primary": lambda s, k: kp.rating_step(k) + max(-1, min(1, kp.rating_step(s))),
        }
        pairs = [(s, k) for s in range(1, 11) for k in range(1, 11)]
        # A is the wide one; C stays inside the ladder's own span
        a = [raws["A_additive"](s, k) for s, k in pairs]
        c = [raws["C_skill_primary"](s, k) for s, k in pairs]
        self.assertEqual((min(a), max(a)), (-6, 6))
        self.assertEqual((min(c), max(c)), (-4, 4))
        clipped = sum(1 for v in a if not kp.LADDER_MIN <= v <= kp.LADDER_MAX)
        self.assertGreaterEqual(clipped, 20, "A's clamping is the measured pathology")

    def test_the_averaged_candidate_is_within_range_by_construction(self) -> None:
        for s in range(1, 11):
            for k in range(1, 11):
                step = kp.combine_averaged(s, k)
                self.assertTrue(kp.LADDER_MIN <= step <= kp.LADDER_MAX)

    def test_the_averaged_tie_break_is_half_up_not_bankers(self) -> None:
        """round(5.5) and round(6.5) both give 6; this mapping must not inherit that."""
        # 4+6 averages 5 exactly; 5+6 averages 5.5 -> half up is 6 -> step 0
        self.assertEqual(kp.combine_averaged(5, 6), kp.rating_step(6))
        self.assertEqual(kp.combine_averaged(6, 7), kp.rating_step(7))

    def test_4df_is_centred_and_bounded(self) -> None:
        rng = random.Random(1)
        rolls = [kp.roll_4df(rng) for _ in range(30_000)]
        self.assertTrue(all(-kp.FDF_COUNT <= r <= kp.FDF_COUNT for r in rolls))
        self.assertAlmostEqual(sum(rolls) / len(rolls), 0.0, delta=0.06)
        exact = kp.expected_4df_distribution()
        self.assertAlmostEqual(exact[0], 0.2346, delta=0.001)
        self.assertAlmostEqual(exact[4], 0.0123, delta=0.001)
        self.assertAlmostEqual(sum(exact.values()), 1.0, delta=1e-9)

    def test_a_fixed_roll_is_deterministic(self) -> None:
        faces = [2, 1, 0, 2]  # +1, 0, -1, +1  ->  +1
        result = kp.resolve_ladder(candidate="C_skill_primary", stat=5, skill=5,
                                   difficulty=0, dice=kp.roll_4df(FixedDice(faces)))
        self.assertEqual(result.dice, 1)
        self.assertEqual(result.total, 1)

    def test_out_of_range_rolls_and_candidates_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            kp.resolve_ladder(candidate="nope", stat=5, skill=5, dice=0)
        with self.assertRaises(ValueError):
            kp.resolve_ladder(candidate="C_skill_primary", stat=5, skill=5, dice=9)


class StackingTests(unittest.TestCase):
    def test_the_cap_bounds_a_runaway_modifier(self) -> None:
        capped = kp.resolve_ladder(candidate="C_skill_primary", stat=5, skill=5,
                                   difficulty=0, situational=6, dice=0)
        uncapped = kp.resolve_ladder(candidate="C_skill_primary", stat=5, skill=5,
                                     difficulty=0, situational=6, dice=0, cap_situational=False)
        self.assertEqual(capped.situational, kp.MAX_SITUATIONAL_STEPS)
        self.assertEqual(uncapped.situational, 6)
        self.assertLessEqual(capped.total, kp.LADDER_MAX + kp.FDF_COUNT + kp.MAX_SITUATIONAL_STEPS)

    def test_an_uncapped_bonus_can_be_worth_more_than_every_die(self) -> None:
        """The measured reason the cap exists: +6 beats the entire 4dF range."""
        self.assertGreater(6, kp.FDF_COUNT)


class OpposedTests(unittest.TestCase):
    def test_equal_opponents_split_and_ties_are_a_real_band(self) -> None:
        rng = random.Random(11)
        wins = ties = 0
        trials = 20_000
        for _ in range(trials):
            _, _, winner = kp.opposed_ladder(candidate="A_additive", left=(5, 5),
                                             right=(5, 5), rng=rng)
            wins += winner == "left"
            ties += winner is None
        self.assertAlmostEqual(wins / trials, 0.42, delta=0.03)
        self.assertAlmostEqual(ties / trials, 0.167, delta=0.03)

    def test_skill_primary_makes_training_decisive(self) -> None:
        """The headline finding: an untrained brute does not keep parity under C."""
        rng = random.Random(3)
        wins = 0
        trials = 20_000
        for _ in range(trials):
            _, _, winner = kp.opposed_ladder(candidate="C_skill_primary", left=(10, 1),
                                             right=(5, 5), rng=rng)
            wins += winner == "left"
        self.assertLess(wins / trials, 0.25)

    def test_ties_are_unresolved_rather_than_silently_awarded(self) -> None:
        """Matches the canonical engine's deliberate 'tie is unresolved' stance."""
        _, _, winner = kp.opposed_ladder(candidate="B_averaged", left=(5, 5),
                                         right=(5, 5), left_dice=0, right_dice=0)
        self.assertIsNone(winner)


class LethalityTests(unittest.TestCase):
    def test_a_more_competent_character_ends_fights_no_slower(self) -> None:
        weak = kp.hits_to_takedown(candidate="C_skill_primary", stat=2, skill=1, defence=13,
                                   stress=4, trials=300, seed=5)
        top = kp.hits_to_takedown(candidate="C_skill_primary", stat=10, skill=10, defence=13,
                                  stress=4, trials=300, seed=5)
        self.assertGreater(weak, top)

    def test_losing_a_fight_is_always_possible(self) -> None:
        """No candidate should guarantee a takedown within a bounded number of exchanges."""
        exchanges = kp.hits_to_takedown(candidate="A_additive", stat=5, skill=5, defence=13,
                                        stress=4, trials=200, seed=5)
        self.assertGreater(exchanges, 1.0)


class DocumentedClaimTests(unittest.TestCase):
    """The document's headline numbers, kept honest with tolerances."""

    def test_the_mixed_profile_is_where_the_candidates_part(self) -> None:
        seeds = {"A_additive": 1, "B_averaged": 2, "C_skill_primary": 3}
        measured = {
            name: kp.p_success_ladder(candidate=name, stat=10, skill=1, difficulty=0,
                                      trials=20_000, seed=seed)
            for name, seed in seeds.items()
        }
        # A and B leave an untrained brute at roughly even odds; C does not.
        self.assertGreater(measured["A_additive"], 0.5)
        self.assertGreater(measured["B_averaged"], 0.5)
        self.assertLess(measured["C_skill_primary"], 0.3)

    def test_the_dv_calibration_clamps_the_top_of_the_authored_ladder(self) -> None:
        """Documented as a limitation: a 7-step ladder cannot carry 7 named DVs."""
        steps = [kp.legacy_dv_to_step(dv) for dv in core.DIFFICULTY_LADDER]
        self.assertEqual(len(steps), 7)
        self.assertEqual(steps[-1], kp.LADDER_MAX)
        self.assertGreaterEqual(len(steps) - len(set(steps)), 2, "the collision is the finding")

    def test_ladder_labels_are_our_own_wording_not_a_source_copy(self) -> None:
        """Fudge's ladder names are its expression; ours must be independently worded."""
        labels = set(kp.LADDER_LABELS.values())
        self.assertFalse(labels & {"Terrible", "Mediocre", "Fair", "Good", "Great", "Superb"})


class ExactProbabilityTests(unittest.TestCase):
    """The exact path, adopted from the sibling resolution lab (PR #207).

    A design number should not be blamable on a seed. These functions are rational and
    need no RNG at all, so they are checked exactly rather than with tolerances.
    """

    def setUp(self) -> None:
        self.counts = kp.fdf_outcome_counts()

    def test_the_outcome_counts_are_the_known_4df_triangle(self) -> None:
        from fractions import Fraction
        self.assertEqual(sum(self.counts.values()), 3 ** kp.FDF_COUNT)
        self.assertEqual(self.counts[0], 19)
        self.assertEqual(self.counts[kp.FDF_COUNT], 1)
        self.assertEqual(Fraction(self.counts[0], 81), Fraction(19, 81))
        # exactness: no float creeps in
        self.assertIsInstance(kp.exact_success_probability(
            candidate="A_additive", stat=5, skill=5, difficulty=0), Fraction)

    def test_exact_probabilities_are_seed_free_and_stable(self) -> None:
        first = kp.exact_success_probability(candidate="C_skill_primary", stat=5, skill=5, difficulty=0)
        second = kp.exact_success_probability(candidate="C_skill_primary", stat=5, skill=5, difficulty=0)
        self.assertEqual(first, second)

    def test_exact_and_sampled_agree(self) -> None:
        """The two methods are independent; if they diverge, one of them is wrong."""
        for candidate in kp.CANDIDATES:
            for stat, skill in ((2, 1), (5, 5), (10, 1), (8, 8)):
                with self.subTest(candidate=candidate, profile=(stat, skill)):
                    exact = float(kp.exact_success_probability(
                        candidate=candidate, stat=stat, skill=skill, difficulty=0))
                    sampled = kp.p_success_ladder(
                        candidate=candidate, stat=stat, skill=skill, difficulty=0,
                        trials=30_000, seed=4242)
                    self.assertAlmostEqual(exact, sampled, delta=0.015)

    def test_the_top_step_succeeds_almost_always_and_the_bottom_almost_never(self) -> None:
        from fractions import Fraction
        top = kp.exact_success_probability(candidate="A_additive", stat=10, skill=10, difficulty=0)
        bottom = kp.exact_success_probability(candidate="C_skill_primary", stat=2, skill=1, difficulty=0)
        self.assertEqual(top, Fraction(80, 81))  # all but the -4 tail
        self.assertEqual(bottom, Fraction(5, 81))

    def test_exact_opposed_is_symmetric_and_ties_are_real(self) -> None:
        left, tie, right = kp.exact_opposed_probabilities(
            candidate="A_additive", left=(5, 5), right=(5, 5))
        self.assertEqual(left, right)  # mirror-image opponents
        self.assertEqual(left + tie + right, 1)
        self.assertAlmostEqual(float(tie), 0.169, delta=0.002)

    def test_skill_primary_skews_opposed_play_toward_training(self) -> None:
        from fractions import Fraction
        additive, _, _ = kp.exact_opposed_probabilities(
            candidate="A_additive", left=(10, 1), right=(5, 5))
        primary, _, _ = kp.exact_opposed_probabilities(
            candidate="C_skill_primary", left=(10, 1), right=(5, 5))
        self.assertAlmostEqual(float(additive), 0.416, delta=0.002)
        self.assertAlmostEqual(float(primary), 0.141, delta=0.002)
        self.assertLess(primary, Fraction(1, 4), "an untrained brute should not be near parity")


if __name__ == "__main__":
    unittest.main()
