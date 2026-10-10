"""Issue #200 cross-system conversion: scope, directionality and noncanonical safety."""
import unittest

from src.rules.issue200_cross_system_converter import (
    BANDS, compare_all, convert, conversion_loss
)
from src.rules.core import STAT_LIST


class CrosswalkTests(unittest.TestCase):
    def test_preserves_existing_character_stat_names(self):
        self.assertEqual(STAT_LIST, ("FIT", "REF", "INT", "SOC", "CYB", "PSY"))

    def test_identity_no_loss_for_every_anchor(self):
        for (family, kind), values in BANDS.items():
            for rating in values:
                with self.subTest(family=family, kind=kind, rating=rating):
                    outcome = convert(rating, family, family, kind)
                    self.assertEqual(outcome.target_value, rating)
                    self.assertFalse(outcome.lossy)

    def test_endpoint_mapping(self):
        for kind in ("attribute", "skill", "difficulty"):
            src = BANDS["noopunk", kind]
            for family in ("fudge", "fate", "eclipse_phase", "without_number"):
                target = BANDS[family, kind]
                with self.subTest(family=family, kind=kind):
                    self.assertEqual(convert(src[0], "noopunk", family, kind).target_value,
                                     target[-1] if family == "eclipse_phase" and kind == "difficulty" else target[0])
                    self.assertEqual(convert(src[-1], "noopunk", family, kind).target_value,
                                     target[0] if family == "eclipse_phase" and kind == "difficulty" else target[-1])

    def test_ep_difficulty_reverses_its_probability_threshold(self):
        self.assertEqual(convert(9, "noopunk", "eclipse_phase", "difficulty").target_value, 90)
        self.assertEqual(convert(29, "noopunk", "eclipse_phase", "difficulty").target_value, 10)

    def test_cwn_attribute_is_modifier_not_raw_score(self):
        self.assertEqual(BANDS["without_number", "attribute"], (-2, -1, 0, 1, 2))

    def test_fate_attribute_is_experimental_not_standard(self):
        self.assertTrue(convert(5, "noopunk", "fate", "attribute").lossy)

    def test_no_guarantee_of_reversibility(self):
        self.assertTrue(conversion_loss(2, "noopunk", "without_number", "attribute"))
        self.assertFalse(conversion_loss(1, "noopunk", "fudge", "attribute"))

    def test_all_five_families(self):
        self.assertEqual(len(compare_all(5, "skill")), 5)
        self.assertEqual(len(compare_all(17, "difficulty")), 5)

    def test_invalid_anchor_rejected_not_clamped(self):
        for bad in (-99, 100, True, 2.5):
            with self.subTest(bad=bad), self.assertRaises((TypeError, ValueError)):
                convert(bad, "noopunk", "fudge", "skill")

    def test_invalid_family_or_kind_rejected(self):
        for kwargs in (dict(target="shadowrun"), dict(kind="power")):
            options = dict(value=5, source="noopunk", target="fate", kind="skill")
            options.update(kwargs)
            with self.assertRaises(ValueError):
                convert(**options)


if __name__ == "__main__":
    unittest.main()
