"""Scale migration is explicit and never mutates the existing d10 engine."""
import json
from pathlib import Path
import unittest

from src.rules import core
from src.rules.issue200_scale_migration import (
    STATS, RATING_MAP, DIFFICULTY_MAP, STEP_LABELS,
    attribute_level, skill_level, difficulty_level, difficulty_name, convert_character,
)
ROOT = Path(__file__).resolve().parents[1]


class SevenStepMigrationTests(unittest.TestCase):
    def test_all_legacy_ratings_mapped_monotonically_and_onto_all_seven_steps(self):
        self.assertEqual(set(RATING_MAP), set(range(1, 11)))
        values = [attribute_level(i) for i in range(1, 11)]
        self.assertEqual(values, sorted(values))
        self.assertEqual(set(values), set(range(-3, 4)))
        self.assertEqual(values, [-3, -2, -2, -1, 0, 0, 1, 1, 2, 3])

    def test_attribute_and_skill_remain_separate(self):
        self.assertEqual(STATS, ("FIT", "REF", "INT", "SOC", "CYB", "PSY"))
        stats = dict(zip(STATS, (1, 3, 5, 6, 8, 10)))
        result = convert_character(stats, {"Infosec": 9, "Telepathy": 2})
        self.assertEqual(result["attributes"], dict(zip(STATS, (-3, -2, 0, 0, 1, 3))))
        self.assertEqual(result["skills"], {"Infosec": 2, "Telepathy": -2})
        self.assertNotIn("Infosec", result["attributes"])

    def test_all_canonical_difficulties_map_to_unique_steps_and_keep_names(self):
        core_data = json.loads((ROOT / "data/rules/core.json").read_text())
        self.assertEqual(set(DIFFICULTY_MAP), {int(x) for x in core_data["difficulties"]})
        self.assertEqual([difficulty_level(x) for x in sorted(DIFFICULTY_MAP)], list(range(-3, 4)))
        for old, new in DIFFICULTY_MAP.items():
            self.assertEqual(difficulty_name(new), core_data["difficulties"][str(old)])

    def test_no_silent_clamp_or_unknown_stat_skill(self):
        for value in (0, 11, True, 5.0, -3):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    attribute_level(value)
        with self.assertRaises(ValueError):
            difficulty_level(16)
        with self.assertRaises(ValueError):
            difficulty_name(4)
        with self.assertRaises(ValueError):
            convert_character({"FIT": 5}, {})
        with self.assertRaises(ValueError):
            convert_character({k: 5 for k in STATS}, {"NotASkill": 5})

    def test_legacy_resolver_is_not_migrated_by_mapping(self):
        self.assertEqual(core.STAT_MIN, 1)
        self.assertEqual(core.STAT_MAX, 10)
        self.assertEqual(core.CHECK_DICE, "1d10")


if __name__ == "__main__":
    unittest.main()
