"""Regression tests for psychic load recovery."""
import unittest

from src.rules.natural_psi import Practitioner, PsiError


class RecoveryTests(unittest.TestCase):
    def test_negative_scenes_rejected_without_mutation(self):
        practitioner = Practitioner(psy=6)
        practitioner.psyche_load = 4
        with self.assertRaises(PsiError):
            practitioner.recover(scenes=-1)
        self.assertEqual(practitioner.psyche_load, 4)

    def test_normal_recovery_never_goes_below_zero(self):
        practitioner = Practitioner(psy=6)
        practitioner.psyche_load = 1
        practitioner.recover(scenes=100)
        self.assertEqual(practitioner.psyche_load, 0)


if __name__ == "__main__":
    unittest.main()
