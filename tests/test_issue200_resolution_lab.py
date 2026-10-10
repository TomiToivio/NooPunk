"""Issue #200: exact experimental roll probabilities, no canonical migration."""
import unittest
from fractions import Fraction

from src.rules.core import STAT_LIST
from src.rules.issue200_resolution_lab import DICE, Trial, success_probability, curve


class ProbabilityLabTests(unittest.TestCase):
    def test_six_existing_stats_only(self):
        self.assertEqual(STAT_LIST, ("FIT", "REF", "INT", "SOC", "CYB", "PSY"))
        for stat in STAT_LIST:
            self.assertEqual(success_probability(Trial(stat, 5, 5, 10, "d10")), 1)

    def test_dice_probabilities_normalized(self):
        for distribution in DICE.values():
            self.assertEqual(sum(distribution.values()), Fraction(1))
        self.assertEqual(DICE["four_fudge"][0], Fraction(19, 81))
        self.assertEqual(DICE["four_fudge"][-4], Fraction(1, 81))
        self.assertEqual(DICE["four_fudge"][4], Fraction(1, 81))

    def test_exact_flat_d10_distribution(self):
        self.assertEqual(success_probability(Trial("INT", 5, 5, 16, "d10")), Fraction(1, 2))
        self.assertEqual(success_probability(Trial("INT", 5, 5, 20, "d10")), Fraction(1, 10))
        self.assertEqual(success_probability(Trial("INT", 5, 5, 21, "d10")), 0)

    def test_fudge_distribution(self):
        self.assertEqual(success_probability(Trial("PSY", 5, 5, 10, "four_fudge")), Fraction(50, 81))
        self.assertEqual(success_probability(Trial("PSY", 5, 5, 14, "four_fudge")), Fraction(1, 81))
        self.assertEqual(success_probability(Trial("PSY", 5, 5, 15, "four_fudge")), 0)

    def test_skill_remains_independent_of_stat(self):
        a = Trial("CYB", 5, 2, 11, "four_fudge")
        b = Trial("CYB", 5, 6, 11, "four_fudge")
        self.assertLess(success_probability(a), success_probability(b))
        self.assertEqual(len(curve("d10", 5, 5, range(8, 12))), 4)

    def test_invalid_inputs(self):
        for kwargs in ({"attribute": "CHA"}, {"stat": 0}, {"skill": 11},
                       {"mode": "d20"}, {"stat": True}):
            options = dict(attribute="INT", stat=5, skill=5, target=12, mode="d10")
            options.update(kwargs)
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Trial(**options)


if __name__ == "__main__":
    unittest.main()
