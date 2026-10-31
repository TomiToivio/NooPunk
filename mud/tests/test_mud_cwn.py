"""The MUD has no rules of its own (#946, milestone 3).

These tests are the executable form of the boundary: the MUD's sheet must *call* the
shared Cities Without Number kernel, not a copy of it. Identity — not equality — is the
assertion, because two implementations of the same formula would pass an equality check
for as long as nobody edited one of them.
"""
from __future__ import annotations

import unittest

from world import cwn  # noqa: I001 - importing the adapter first puts <repo>/src on sys.path
from rules import wn_core


class SharedKernelTests(unittest.TestCase):
    def test_the_check_is_literally_the_kernel_function(self) -> None:
        self.assertIs(cwn.skill_check, wn_core.skill_check)
        self.assertIs(cwn.attribute_modifier, wn_core.attribute_modifier)

    def test_a_sheet_check_equals_the_kernel_check(self) -> None:
        sheet = cwn.Sheet()
        mine = sheet.check("Survive", difficulty="significant", dice=(3, 4))
        theirs = wn_core.skill_check(
            attribute_score=sheet.attributes[cwn.ATTRIBUTE_FOR_SKILL["Survive"]],
            skill_level=sheet.skills.get("Survive"),
            difficulty=wn_core.DIFFICULTY_SIGNIFICANT,
            dice=(3, 4),
        )
        self.assertEqual(mine.total, theirs.total)
        self.assertEqual(mine.success, theirs.success)
        self.assertEqual(mine.margin, theirs.margin)

    def test_an_untrained_skill_carries_the_kernel_penalty(self) -> None:
        sheet = cwn.Sheet(skills={"Survive": 1})
        check = sheet.check("Program", difficulty="simple", dice=(1, 1))
        self.assertTrue(check.untrained)
        self.assertEqual(check.total, 2 + check.attribute_modifier - 1)

    def test_the_mud_names_a_band_rather_than_a_number(self) -> None:
        sheet = cwn.Sheet()
        with self.assertRaises(cwn.SheetError):
            sheet.check("Survive", difficulty=9)
        with self.assertRaises(cwn.SheetError):
            sheet.check("Astrogate")

    def test_a_sheet_survives_a_round_trip(self) -> None:
        sheet = cwn.Sheet(skills={"Notice": 1, "Trade": 0})
        restored = cwn.Sheet.from_dict(sheet.to_dict())
        self.assertEqual(restored.attributes, sheet.attributes)
        self.assertEqual(restored.skills, sheet.skills)

    def test_an_illegal_attribute_spread_is_refused(self) -> None:
        with self.assertRaises(cwn.SheetError):
            cwn.Sheet(attributes=dict.fromkeys(cwn.ATTRIBUTES, 18))
        self.assertIsNotNone(cwn.Sheet())


if __name__ == "__main__":
    unittest.main()
