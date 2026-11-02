"""Issue #1068: adapters must not modify or duplicate the CWN save formula."""
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from rules import cwn_save_adapter, wn_core


class CwnSaveInputParity(unittest.TestCase):
    SHEETS = (
        {"Strength": 10, "Dexterity": 14, "Constitution": 12, "Intelligence": 9, "Wisdom": 13, "Charisma": 11},
        {"STR": 10, "DEX": 14, "CON": 12, "INT": 9, "WIS": 13, "CHA": 11},
        {"strength": 10, "dexterity": 14, "constitution": 12, "intelligence": 9, "wisdom": 13, "charisma": 11},
    )

    def test_all_aliases_resolve_to_the_same_target(self):
        for level in (1, 5, 10):
            for kind in ("Physical", "Evasion", "Mental", "Luck"):
                results = [cwn_save_adapter.save_target(kind, level=level, attributes=s) for s in self.SHEETS]
                self.assertEqual(results, [results[0]] * len(results))
                self.assertEqual(results[0], wn_core.save_target(
                    kind, level=level,
                    modifiers=cwn_save_adapter.normalize_attribute_scores(self.SHEETS[0])))

    def test_example_targets(self):
        expected = {"Physical": 15, "Evasion": 14, "Mental": 15, "Luck": 15}
        for kind, target in expected.items():
            self.assertEqual(cwn_save_adapter.save_target(kind, level=1, attributes=self.SHEETS[0]), target)

    def test_missing_save_attribute_is_not_silently_zero(self):
        with self.assertRaises(wn_core.WnError):
            cwn_save_adapter.save_target("Physical", level=1, attributes={"STR": 10})

    def test_conflicting_aliases_are_rejected(self):
        with self.assertRaises(wn_core.WnError):
            cwn_save_adapter.save_target("Luck", level=1, attributes={"STR": 10, "Strength": 18})

    def test_bad_score_level_and_category_are_rejected(self):
        for sheet, kind, level in (({"STR": 19}, "Luck", 1),
                                   ({}, "Luck", 0), ({}, "Other", 1)):
            with self.subTest(sheet=sheet, kind=kind, level=level):
                with self.assertRaises(wn_core.WnError):
                    cwn_save_adapter.save_target(kind, level=level, attributes=sheet)


if __name__ == "__main__":
    unittest.main()
