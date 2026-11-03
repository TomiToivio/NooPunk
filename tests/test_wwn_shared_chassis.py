"""The WWN chassis that NoöPunk does **not** reimplement, pinned against the printed book (#1101).

WWN and CWN are both Without Number games, so a great deal of the fantasy book's character-scale machinery is
literally the same arithmetic. The #1101 rule is "verified reuse, not reimplementation": one resolver serves
both, and the only honest way to say that is a test that takes the WWN numbers *from the book's own page* and
shows the shared function returns them.

The pages cited are from the authorised Deluxe copy (`WorldsWithoutNumber_DeluxePDF_040221.pdf`), whose
section index is `data/rules/wwn_sections.json`. Only values and page numbers are recorded here — no book
text is copied, and the PDF itself is neither stored nor redistributable.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules.wn_core import UNSKILLED_PENALTY, attribute_modifier, skill_check  # noqa: E402


class AttributesAreSharedTests(unittest.TestCase):
    """WWN p.8, "Attributes": 3 → −2, 4–7 → −1, 8–13 → 0, 14–17 → +1, 18 → +2."""

    #: Every band boundary the book prints, including both ends of each band.
    PRINTED_BANDS = ((3, -2), (4, -1), (7, -1), (8, 0), (13, 0), (14, 1), (17, 1), (18, 2))

    def test_the_printed_bands_are_the_shared_table(self) -> None:
        for score, expected in self.PRINTED_BANDS:
            self.assertEqual(attribute_modifier(score), expected, f"WWN p.8: score {score}")

    def test_every_score_in_the_printed_range_falls_in_its_band(self) -> None:
        for score in range(3, 19):
            if score == 3:
                expected = -2
            elif 4 <= score <= 7:
                expected = -1
            elif 8 <= score <= 13:
                expected = 0
            elif 14 <= score <= 17:
                expected = 1
            else:
                expected = 2
            self.assertEqual(attribute_modifier(score), expected, f"score {score}")


class SkillChecksAreSharedTests(unittest.TestCase):
    """WWN pp.9 and 41: 2d6 + skill level + attribute modifier, −1 if untrained, success on ≥ difficulty."""

    def test_two_dice_plus_skill_plus_modifier(self) -> None:
        # A skilled hero: 2d6 (3+4) + Skill-1 + a 14 (+1) = 9 against difficulty 9.
        check = skill_check(attribute_score=14, skill_level=1, difficulty=9, dice=(3, 4))
        self.assertEqual(check.total, 9)
        self.assertTrue(check.success, "WWN p.41: equal or higher than the difficulty is a success")

    def test_the_unskilled_penalty_is_minus_one(self) -> None:
        # WWN p.9: "If they have no relevant skill at all, they subtract 1 from their roll."
        self.assertEqual(UNSKILLED_PENALTY, -1)
        untrained = skill_check(attribute_score=10, skill_level=None, difficulty=9, dice=(4, 4))
        trained = skill_check(attribute_score=10, skill_level=0, difficulty=9, dice=(4, 4))
        self.assertTrue(untrained.untrained)
        self.assertEqual(untrained.total, trained.total - 1)

    def test_a_negative_margin_is_a_failure_not_a_near_miss(self) -> None:
        check = skill_check(attribute_score=3, skill_level=0, difficulty=15, dice=(1, 1))
        self.assertFalse(check.success)
        self.assertEqual(check.margin, check.total - 15)

    def test_the_dice_may_be_real_dice_or_a_seeded_roll(self) -> None:
        """Tabletop play passes the dice that landed; a replay passes a seeded rng. Same procedure."""
        import random

        seeded = skill_check(attribute_score=10, skill_level=2, difficulty=10,
                             rng=random.Random(7))
        replay = skill_check(attribute_score=10, skill_level=2, difficulty=10,
                             rng=random.Random(7))
        self.assertEqual(seeded.total, replay.total)


class NotClaimedTests(unittest.TestCase):
    """Where the reuse claim stops: the register must not pretend these are verified."""

    def test_saving_throws_are_not_claimed_as_verified_reuse(self) -> None:
        """CWN's saves are `16 - level - attribute modifier`; WWN prints its own values on p.40.

        Until somebody compares them row by row, `data/rules/wwn_traceability.json` must say `unverified` —
        this test exists so the gap cannot be closed by wishful editing.
        """
        import json

        register = json.loads((ROOT / "data/rules/wwn_traceability.json").read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in register["rows"]}
        self.assertEqual(rows["time-and-saving-throws"]["status"], "unverified")


if __name__ == "__main__":
    unittest.main()
