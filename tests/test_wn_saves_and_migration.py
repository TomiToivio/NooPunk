"""Issue #615 base-system contract, second half: saving throws, untrained skill use, and migration.

The first half (`tests/test_wn_core.py`) pins the attribute bands, the check arithmetic and the
difficulty ladder. This file pins what the SRD says *besides* those, because each of them was either
missing from the merged kernel or wrong against the source:

* **saving throws** — `1d20 >= 16 - level - the higher of the two listed attribute modifiers`, with a
  natural 1 always failing and a natural 20 always succeeding (CWN SRD 2.02). The canon file said
  `base 15` and dropped the level term; both are corrected here and asserted below.
* **untrained skills** — no level-0 means **-1**; level-0 is basic competence and carries no penalty.
* **migration** — the legacy 1..10 STAT and skill scales onto 3..18 and 0..4.

Every value asserted here is read from the SRD, so this file is the contract between the repository and
the source. A change to a target base, a level term or a penalty has to be argued for here.
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules import wn_core as wn  # noqa: E402


class SavingThrowTests(unittest.TestCase):
    def test_the_four_srd_categories_exist(self) -> None:
        self.assertEqual(wn.SAVE_TYPES, ("physical", "evasion", "mental", "luck"))
        self.assertEqual(wn.SAVE_TARGET_BASE, 16)
        self.assertEqual(wn.SAVE_DIE, 20)

    def test_the_target_is_sixteen_minus_level_minus_the_better_of_the_pair(self) -> None:
        # Physical: STR or CON. 16 - 2 - max(+1, -1) = 13.
        self.assertEqual(wn.save_target("physical", level=2, modifiers={"STR": 1, "CON": -1}), 13)
        # Evasion: DEX or INT. 16 - 1 - max(+2, 0) = 13.
        self.assertEqual(wn.save_target("evasion", level=1, modifiers={"DEX": 2, "INT": 0}), 13)
        # Mental: WIS or CHA. 16 - 3 - max(-2, +1) = 12.
        self.assertEqual(wn.save_target("mental", level=3, modifiers={"WIS": -2, "CHA": 1}), 12)

    def test_the_level_term_is_real(self) -> None:
        """A veteran saves more easily than a beginner with the same attributes."""
        beginner = wn.save_target("physical", level=1, modifiers={"STR": 0})
        veteran = wn.save_target("physical", level=6, modifiers={"STR": 0})
        self.assertEqual(beginner - veteran, 5)

    def test_luck_has_no_attribute_modifiers(self) -> None:
        self.assertEqual(wn.save_target("luck", level=2, modifiers={"DEX": 2, "STR": 2}), 14)

    def test_a_natural_one_always_fails_even_against_a_trivial_target(self) -> None:
        result = wn.roll_save("physical", level=10, modifiers={"STR": 2}, die=1)
        self.assertTrue(result.natural)
        self.assertFalse(result.success, "natural 1 fails regardless of the target")

    def test_a_natural_twenty_always_succeeds_even_against_an_impossible_target(self) -> None:
        result = wn.roll_save("mental", level=1, modifiers={"WIS": -2}, die=20)
        self.assertTrue(result.natural)
        self.assertTrue(result.success, "natural 20 succeeds regardless of the target")

    def test_an_ordinary_roll_is_compared_with_the_target(self) -> None:
        target = wn.save_target("evasion", level=1, modifiers={"DEX": 0})   # 15
        self.assertFalse(wn.roll_save("evasion", level=1, modifiers={"DEX": 0}, die=target - 1).success)
        self.assertTrue(wn.roll_save("evasion", level=1, modifiers={"DEX": 0}, die=target).success)

    def test_the_die_and_the_category_are_validated(self) -> None:
        for bad in (0, 21):
            with self.subTest(die=bad), self.assertRaises(wn.WnError):
                wn.roll_save("physical", die=bad)
        with self.assertRaises(wn.WnError):
            wn.roll_save("psychic", die=10)

    def test_a_seeded_save_replays(self) -> None:
        first = wn.roll_save("mental", level=2, modifiers={"WIS": 1}, rng=random.Random(615))
        second = wn.roll_save("mental", level=2, modifiers={"WIS": 1}, rng=random.Random(615))
        self.assertEqual(first, second)


class UntrainedTests(unittest.TestCase):
    def test_no_level_zero_carries_the_minus_one(self) -> None:
        trained = wn.skill_check(attribute_score=10, skill_level=0, difficulty=8, dice=(2, 3))
        untrained = wn.skill_check(attribute_score=10, skill_level=None, difficulty=8, dice=(2, 3))
        self.assertFalse(trained.untrained)
        self.assertTrue(untrained.untrained)
        self.assertEqual(untrained.total, trained.total + wn.UNSKILLED_PENALTY)

    def test_level_zero_is_competence_not_a_penalty(self) -> None:
        result = wn.skill_check(attribute_score=10, skill_level=0, difficulty=8, dice=(4, 4))
        self.assertEqual(result.total, 8)
        self.assertTrue(result.success)

    def test_a_negative_level_is_still_refused(self) -> None:
        for bad in (-1, -3):
            with self.subTest(level=bad), self.assertRaises(wn.WnError):
                wn.skill_check(attribute_score=10, skill_level=bad, difficulty=8, dice=(3, 3))


class MigrationTests(unittest.TestCase):
    def test_the_legacy_stat_stretch_is_monotonic_and_hits_both_ends(self) -> None:
        stretched = [wn.from_legacy_stat(value) for value in range(1, 11)]
        self.assertEqual(stretched[0], wn.ATTRIBUTE_MIN)
        self.assertEqual(stretched[-1], wn.ATTRIBUTE_MAX)
        self.assertEqual(stretched, sorted(stretched))
        self.assertTrue(all(wn.ATTRIBUTE_MIN <= v <= wn.ATTRIBUTE_MAX for v in stretched))

    def test_the_legacy_skill_mapping_covers_the_whole_scale(self) -> None:
        self.assertEqual({v: wn.from_legacy_skill(v) for v in range(1, 11)},
                         {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4})

    def test_every_legacy_stat_has_a_home_among_the_six(self) -> None:
        self.assertEqual(set(wn.LEGACY_STAT_MAP), {"FIT", "REF", "INT", "SOC", "CYB", "PSY"})
        self.assertTrue(set(wn.LEGACY_STAT_MAP.values()) <= set(wn.ATTRIBUTE_CODES))

    def test_the_canon_file_agrees_with_the_code_about_saves(self) -> None:
        import json

        canon = json.loads((ROOT / "data" / "rules" / "wn_core.json").read_text(encoding="utf-8"))
        saves = canon["saves"]
        self.assertEqual(int(saves["base_target"]), wn.SAVE_TARGET_BASE)
        self.assertIn("level", saves["formula"])
        self.assertEqual(tuple(k for k in saves["attributes"]), wn.SAVE_TYPES)
        self.assertEqual(saves["natural_one"], "always fails")
        self.assertEqual(saves["natural_twenty"], "always succeeds")

    def test_out_of_range_legacy_values_are_refused(self) -> None:
        for bad in (0, 11):
            with self.subTest(value=bad), self.assertRaises(wn.WnError):
                wn.from_legacy_stat(bad)
            with self.subTest(value=bad), self.assertRaises(wn.WnError):
                wn.from_legacy_skill(bad)


if __name__ == "__main__":
    unittest.main()
