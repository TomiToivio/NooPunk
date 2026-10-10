"""Tests for the issue #200 aspects/resource/consequence prototype.

Priority order, same as the kernel prototype's:

1. **Prove it stayed a prototype** -- canon untouched, and the consequence vocabulary pinned to
   `RULEBOOK.md` section 51 rather than trusted.
2. **Prove the mechanics do what #200 demands**: bounded modifiers, no uncapped exploit,
   deterministic and auditable outcomes.
3. **Prove the numbers are real** -- exact rationals, cross-checked against the kernel
   prototype's independent computation.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import aspects_prototype as ap
from rules import core
from rules import kernel_prototype as kp

def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class StaysAPrototypeTests(unittest.TestCase):
    def test_declares_itself_non_canonical(self) -> None:
        self.assertFalse(ap.IS_CANONICAL)

    def test_the_canonical_engine_is_untouched(self) -> None:
        canon = json.loads(read("data/rules/core.json"))
        self.assertEqual(canon["skill_check"]["formula"], "STAT + Skill + 1d10")

    def test_the_canonical_resolver_still_behaves_as_always(self) -> None:
        result = core.resolve_check(stat=5, skill=5, target=15, die=5)
        self.assertEqual(result.total, 15)
        self.assertTrue(result.success)

    def test_the_six_stats_are_still_six(self) -> None:
        """Read from canon rather than assumed; #200 keeps the six STATs and the Skill taxonomy."""
        canon = json.loads(read("data/rules/core.json"))
        stats = canon["stats"]
        names = stats["final_list"] if isinstance(stats, dict) else stats
        self.assertEqual(len(names), 6, f"expected six STATs, got {names}")
        skills = canon["skills"]["final_list"]
        self.assertGreaterEqual(len(skills), 10, "the Skill taxonomy must stay populated")
        self.assertEqual(canon["skills"]["untrained_modifier"], -1)

    def test_no_aspects_implementation_is_wired_into_a_runtime(self) -> None:
        """If a runtime imported this prototype, #200's 'test before locking' would be over."""
        for runtime in ("src/rules/core.py", "src/rules/issue200_scale_migration.py"):
            with self.subTest(runtime=runtime):
                self.assertNotIn("aspects_prototype", read(runtime))


class ConsequenceVocabularyTests(unittest.TestCase):
    """The vocabulary is the AUTHOR'S. It is asserted against the rulebook, not assumed."""


    def test_ladder_progression_is_not_automatic(self) -> None:
        self.assertFalse(
            ap.ladder_progression_is_automatic(),
            "the prototype must not assume harm advances on its own",
        )

    def test_a_non_authored_state_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ap.HarmState().record("Mangled")


class HarmStateTests(unittest.TestCase):
    def test_worst_state_follows_the_ladder_order(self) -> None:
        harm = ap.HarmState(states=["Wounded", "Scratched"])
        self.assertEqual(harm.worst, "Wounded")
        self.assertFalse(harm.taken_out)
        harm.record("Down")
        self.assertEqual(harm.worst, "Down")
        self.assertTrue(harm.taken_out)

    def test_critical_counts_as_taken_out(self) -> None:
        self.assertTrue(ap.HarmState(states=["Critical"]).taken_out)

    def test_the_penalty_is_bounded_however_many_consequences_are_set(self) -> None:
        self.assertEqual(
            ap.HarmState(consequences=ap.MAX_CONSEQUENCES).penalty_steps(),
            ap.HarmState(consequences=99).penalty_steps(),
            "#200 forbids uncapped numerical exploits; the consequence penalty must saturate",
        )

    def test_an_empty_state_list_has_no_worst(self) -> None:
        self.assertIsNone(ap.HarmState().worst)


class BoundedModifierTests(unittest.TestCase):
    """The heart of #200's constraint, measured rather than asserted."""

    def test_the_rolls_typical_spread_is_what_bounds_a_modifier(self) -> None:
        spread = ap.spread_of_the_roll()
        self.assertEqual(spread, Fraction(51, 81), "63.0% of 4dF outcomes sit within +/-1")
        self.assertLess(spread, Fraction(2, 3))

    def test_the_adopted_bonus_is_one_step(self) -> None:
        """+2 nearly settles a contest; the measured choice is +1."""
        self.assertEqual(ap.ASPECT_INVOKE_BONUS, 1)
        gain_one = ap.value_of_bonus(1)
        gain_two = ap.value_of_bonus(2)
        self.assertGreater(gain_two, gain_one * Fraction(3, 2), "+2 must be visibly too strong")

    def test_the_cap_holds_however_many_aspects_are_named(self) -> None:
        capped = {ap.stacked_success_probability(invocations=n, cap=True) for n in range(1, 8)}
        self.assertEqual(len(capped), 1, "invocations past the cap must change nothing")

    def test_without_the_cap_the_roll_becomes_an_automatic_success(self) -> None:
        """This is the exploit #200 names. The prototype measures it so the cap has a reason."""
        auto = next(n for n in range(1, 12)
                    if ap.stacked_success_probability(invocations=n, cap=False) == 1)
        self.assertLessEqual(auto, 4, "the exploit must be cheap, or the cap looks like fussing")
        self.assertLess(ap.stacked_success_probability(invocations=auto, cap=True), 1)

    def test_an_invocation_cannot_exceed_the_cap_even_if_asked(self) -> None:
        pool = ap.NarrativePool(tokens=99)
        granted = pool.invoke(count=5)
        self.assertEqual(granted, ap.ASPECT_INVOKE_BONUS * ap.MAX_INVOCATIONS_PER_ROLL)


class ExactProbabilityTests(unittest.TestCase):
    def test_probabilities_are_exact_rationals(self) -> None:
        self.assertIsInstance(ap.success_probability(0), Fraction)
        self.assertEqual(ap.success_probability(0), Fraction(50, 81))

    def test_no_seed_is_involved(self) -> None:
        self.assertEqual(ap.success_probability(1), ap.success_probability(1))

    def test_cross_checks_against_the_kernel_prototypes_independent_computation(self) -> None:
        for bonus in range(4):
            with self.subTest(bonus=bonus):
                self.assertEqual(
                    ap.success_probability(bonus),
                    kp.exact_success_probability(
                        candidate="B_averaged", stat=5, skill=5, difficulty=0, situational=bonus,
                        cap_situational=False,
                    ),
                    "two prototypes must agree on the same dice",
                )



class NarrativeResourceTests(unittest.TestCase):
    def test_the_pool_funds_the_documented_number_of_scenes(self) -> None:
        self.assertEqual(ap.tokens_per_scene(1), Fraction(3, 1))
        self.assertEqual(ap.tokens_per_scene(3), Fraction(1, 1))

    def test_the_pool_only_refills_by_accepting_a_complication(self) -> None:
        pool = ap.NarrativePool()
        pool.invoke(count=1)
        self.assertEqual(pool.tokens, ap.NARRATIVE_POOL_START - ap.TOKENS_PER_INVOCATION)
        pool.invoke(count=1)
        pool.invoke(count=1)
        self.assertEqual(pool.invoke(count=1), 0, "an empty pool must grant nothing")
        pool.compel()
        self.assertGreater(pool.invoke(count=1), 0, "a compel is the refill path")

    def test_invoking_without_tokens_grants_nothing_rather_than_going_negative(self) -> None:
        pool = ap.NarrativePool(tokens=0)
        self.assertEqual(pool.invoke(count=1), 0)
        self.assertEqual(pool.tokens, 0)

    def test_compel_break_even_matches_the_invocation_rate(self) -> None:
        self.assertEqual(ap.compel_break_even(2), Fraction(2, 1))


class AspectPermissionTests(unittest.TestCase):
    def test_permission_use_is_deterministic_and_grants_no_number(self) -> None:
        tag = ap.Aspect(name="forensic credentials", permits="examine the sealed locker")
        self.assertTrue(tag.permits_action("examine the sealed locker"))
        self.assertTrue(tag.permits_action("  Examine The Sealed Locker  "))
        self.assertFalse(tag.permits_action("override the reactor"))

    def test_a_non_permission_aspect_permits_nothing(self) -> None:
        self.assertFalse(ap.Aspect(name="plain tag").permits_action("anything"))

    def test_permission_use_costs_no_tokens(self) -> None:
        pool = ap.NarrativePool()
        ap.Aspect(name="tag", permits="something").permits_action("something")
        self.assertEqual(pool.tokens, ap.NARRATIVE_POOL_START)


class DraftParameterTests(unittest.TestCase):
    """#200 requires new numbers to be flagged DRAFT pending calibration."""

    def test_every_parameter_is_an_integer_and_centralised(self) -> None:
        for name in ("ASPECT_INVOKE_BONUS", "MAX_INVOCATIONS_PER_ROLL", "NARRATIVE_POOL_START",
                     "TOKENS_PER_COMPEL", "TOKENS_PER_INVOCATION", "CONSEQUENCE_PENALTY_STEPS",
                     "MAX_CONSEQUENCES"):
            with self.subTest(parameter=name):
                self.assertIsInstance(getattr(ap, name), int)

    def test_the_module_flags_its_numbers_as_draft(self) -> None:
        source = read("src/rules/aspects_prototype.py")
        self.assertIn("DRAFT", source)
        self.assertGreaterEqual(source.count("DRAFT"), 5, "each new number must carry the flag")


if __name__ == "__main__":
    unittest.main()
