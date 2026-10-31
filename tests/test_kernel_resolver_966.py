"""The arc runs on the published CWN numbers, not on a stub (#966).

`solo_arc` takes a resolver as a callable precisely so the story tests can inject `_always`/`_never`. This suite
checks the other half: that the resolver a real game injects produces the kernel's arithmetic — and that combat
and hacking use the same kernel rather than a second set of rules.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))

from nopunk_mud import cwn_core, kernel_resolver  # noqa: E402
from nopunk_mud.kernel_resolver import Resolver, ResolverError  # noqa: E402
from nopunk_mud.solo_arc import Arc, advance  # noqa: E402


class DifficultyMapping(unittest.TestCase):
    def test_names_map_to_published_bands(self):
        self.assertEqual(kernel_resolver.difficulty_number("routine"), 8)
        self.assertEqual(kernel_resolver.difficulty_number("hard"), 10)
        self.assertEqual(kernel_resolver.difficulty_number("VERY_HARD"), 12)

    def test_an_unknown_name_is_refused(self):
        with self.assertRaises(ResolverError):
            kernel_resolver.difficulty_number("sporting")

    def test_every_name_is_a_published_band(self):
        for number in kernel_resolver.DIFFICULTY_NAMES.values():
            self.assertIn(number, cwn_core.DIFFICULTIES)


class PublishedArithmetic(unittest.TestCase):
    def test_the_resolver_matches_the_kernel_exactly(self):
        resolver = Resolver.for_recruit()
        # Notice rank 1, INT 13 (+0), dice 3+4 = 7 -> 7 + 1 + 0 = 8 against routine 8: a success.
        check = resolver.check("Notice", "routine", dice=(3, 4))
        expected = cwn_core.skill_check(1, 13, 8, dice=(3, 4))
        self.assertEqual(check.total, expected.total)
        self.assertEqual(check.success, expected.success)
        self.assertTrue(check.success)

    def test_one_point_short_fails(self):
        resolver = Resolver.for_recruit()
        check = resolver.check("Notice", "routine", dice=(3, 3))
        self.assertEqual(check.total, 7)
        self.assertFalse(check.success)

    def test_an_untrained_skill_takes_the_untrained_penalty(self):
        resolver = Resolver.for_recruit()
        # Program is not on the recruit's sheet: rank -1, INT 13 (+0), dice 6+6 -> 12 - 1 = 11 vs hard 10.
        check = resolver.check("Program", "hard", dice=(6, 6))
        self.assertEqual(check.total, 11)

    def test_callable_form_is_what_the_arc_injects(self):
        resolver = Resolver.for_recruit()
        self.assertTrue(callable(resolver))
        self.assertTrue(resolver("Notice", "routine", (3, 4)))
        self.assertFalse(resolver("Notice", "routine", (3, 3)))

    def test_three_dice_are_refused_rather_than_ignored(self):
        with self.assertRaises(ResolverError):
            Resolver.for_recruit().check("Notice", "routine", dice=(1, 2, 3))


class ArcOnTheKernel(unittest.TestCase):
    def test_a_full_run_with_real_numbers(self):
        """The whole arc, resolved by the kernel, with dice supplied so the run is reproducible."""
        resolver = Resolver.for_recruit()
        arc = Arc()
        arc, _ = advance(arc, "accept", resolver)
        arc, _ = advance(arc, "interview", resolver, dice=(3, 4))   # 8 vs 8: success
        arc, _ = advance(arc, "leave", resolver)
        arc, _ = advance(arc, "records", resolver, dice=(4, 4))     # 9 vs 8: success
        arc, _ = advance(arc, "press", resolver)
        arc, text = advance(arc, "submit", resolver)
        self.assertEqual(arc.stage, "complete")
        self.assertEqual(arc.ending, "corroborated")
        self.assertEqual(set(arc.clues), {"witness", "records"})
        self.assertIn("Case closed", text)

    def test_a_failed_check_degrades_the_ending_but_does_not_stop_the_case(self):
        resolver = Resolver.for_recruit()
        arc = Arc()
        arc, _ = advance(arc, "accept", resolver)
        arc, _ = advance(arc, "interview", resolver, dice=(2, 3))   # 5 + 1 = 6 vs 8: failure
        self.assertIn("witness_uncooperative", arc.consequences)
        arc, _ = advance(arc, "leave", resolver)
        arc, _ = advance(arc, "records", resolver, dice=(4, 4))
        arc, _ = advance(arc, "press", resolver)
        arc, _ = advance(arc, "submit", resolver)
        self.assertEqual(arc.stage, "complete")
        # One clue and a recorded failure: the case closes, but thinner. That is the designed degradation.
        self.assertEqual(arc.ending, "partial")


class CombatOnTheKernel(unittest.TestCase):
    def test_a_hit_and_a_miss_follow_the_kernel(self):
        resolver = Resolver.for_recruit()
        # d20 20 + 0 + DEX +1 + rank 0 = 21 against AC 12: a hit. d20 2: a miss.
        self.assertTrue(kernel_resolver.attack(resolver, armor_class=12, die=20)["hit"])
        self.assertFalse(kernel_resolver.attack(resolver, armor_class=12, die=2)["hit"])

    def test_damage_is_weapon_die_plus_dexterity_and_never_negative(self):
        resolver = Resolver.for_recruit()
        # DEX 12 is in the 8-13 band: +0, so a 4 stays a 4.
        self.assertEqual(kernel_resolver.strike(resolver, weapon_die=6, roll=4), 4)
        weak = Resolver(attributes={"DEX": 3, "INT": 10, "CHA": 10, "STR": 10, "CON": 10, "WIS": 10},
                        skills={}, rng=resolver.rng)
        self.assertEqual(kernel_resolver.strike(weak, weapon_die=6, roll=1), 0)

    def test_an_absurd_armour_class_is_refused(self):
        with self.assertRaises(ValueError):
            kernel_resolver.attack(Resolver.for_recruit(), armor_class=0)


class HackingOnTheKernel(unittest.TestCase):
    def test_a_consumer_node_is_easy_and_a_government_node_is_hard(self):
        resolver = Resolver.for_recruit()
        easy = kernel_resolver.hack(resolver, security="consumer", dice=(5, 5))
        hard = kernel_resolver.hack(resolver, security="government", dice=(5, 5))
        self.assertTrue(easy["success"])
        self.assertEqual(easy["difficulty"], 6)
        self.assertEqual(hard["difficulty"], 10)
        self.assertFalse(hard["success"])

    def test_a_failed_intrusion_spends_trace_and_raises_the_alarm(self):
        result = kernel_resolver.hack(Resolver.for_recruit(), security="government", dice=(1, 1))
        self.assertFalse(result["success"])
        self.assertTrue(result["alarm"])
        self.assertEqual(result["trace_spent"], 1)
        self.assertEqual(result["trace_remaining"], 2)

    def test_an_unknown_security_class_is_refused(self):
        with self.assertRaises(ResolverError):
            kernel_resolver.hack(Resolver.for_recruit(), security="alien")


if __name__ == "__main__":
    unittest.main()
