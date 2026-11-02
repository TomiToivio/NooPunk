"""CWN pharmaceutical source examples and boundary cases (#1068)."""
import unittest

from src.rules.cwn_pharmaceuticals import (
    PharmaceuticalError, administer, strongest_bonus, panacea_first_aid,
    trauma_patch_difficulty, trauma_patch_works,
)


class PharmaceuticalTests(unittest.TestCase):
    def test_untrained_chem(self):
        x = administer("Boneshaker", heal_rank=None, system_strain=0, strain_maximum=5)
        self.assertTrue(x.benefit_allowed)
        self.assertEqual(x.main_actions, 1)

    def test_heal_requirement(self):
        self.assertFalse(administer("Panacea", heal_rank=0, system_strain=0, strain_maximum=5).eligible)

    def test_lurch_escalation(self):
        for prior in range(3):
            result = administer("Lurch", heal_rank=prior, system_strain=0,
                                strain_maximum=4, lurch_doses_today=prior)
            self.assertTrue(result.eligible)
            if prior:
                self.assertFalse(administer("Lurch", heal_rank=prior - 1,
                    system_strain=0, strain_maximum=4,
                    lurch_doses_today=prior).eligible)

    def test_strain_max_prevents_benefit(self):
        x = administer("Boneshaker", heal_rank=None, system_strain=4,
                       strain_maximum=5, strain_cost=2)
        self.assertTrue(x.eligible)
        self.assertFalse(x.benefit_allowed)

    def test_only_highest_bonus(self):
        self.assertEqual(strongest_bonus(1, 2, 2), 2)
        self.assertEqual(strongest_bonus(), 0)

    def test_panacea(self):
        self.assertEqual(panacea_first_aid(2), 6)
        self.assertEqual(panacea_first_aid(5), 10)

    def test_trauma_patch_timing(self):
        self.assertEqual(trauma_patch_difficulty(0), 6)
        self.assertEqual(trauma_patch_difficulty(5), 11)
        self.assertIsNone(trauma_patch_difficulty(6))
        self.assertTrue(trauma_patch_works(rounds_elapsed=2, check_total=8))
        self.assertFalse(trauma_patch_works(rounds_elapsed=2, check_total=7))
        self.assertFalse(trauma_patch_works(rounds_elapsed=0, check_total=20,
                                            poison_or_disease=True))

    def test_bad_input(self):
        with self.assertRaises(PharmaceuticalError):
            administer("missing", heal_rank=0, system_strain=0, strain_maximum=5)


if __name__ == "__main__":
    unittest.main()
