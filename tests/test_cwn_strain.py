"""System Strain — every assertion traced to the CWN SRD section.

SRD: ``rules-of-the-game/injury-healing-system-strain/system-strain/``
"""
import unittest

from src.rules.cwn_strain import (
    FORCED_OVERFLOW_UNCONSCIOUS_HOURS,
    RECOVERY_PER_NIGHT,
    StrainError,
    SystemStrain,
)


class MaximumTests(unittest.TestCase):
    def test_the_maximum_is_the_constitution_score(self) -> None:
        self.assertEqual(SystemStrain(constitution=11).maximum, 11)

    def test_a_healthy_character_starts_at_zero(self) -> None:
        strain = SystemStrain(constitution=11)
        self.assertEqual(strain.total, 0)
        self.assertEqual(strain.available, 11)

    def test_strain_can_never_be_constructed_above_the_maximum(self) -> None:
        with self.assertRaises(StrainError):
            SystemStrain(constitution=5, temporary=4, permanent=2)


class AbsorbTests(unittest.TestCase):
    def test_an_addition_within_the_maximum_is_taken(self) -> None:
        strain = SystemStrain(constitution=10)
        self.assertTrue(strain.absorb(4))
        self.assertEqual(strain.total, 4)
        self.assertEqual(strain.available, 6)

    def test_an_addition_that_would_pass_the_maximum_is_refused(self) -> None:
        strain = SystemStrain(constitution=10, temporary=8)
        self.assertFalse(strain.absorb(3))
        self.assertEqual(strain.total, 8, "a refused addition changes nothing")

    def test_the_exact_maximum_is_allowed(self) -> None:
        strain = SystemStrain(constitution=10, temporary=8)
        self.assertTrue(strain.absorb(2))
        self.assertEqual(strain.total, 10)
        self.assertEqual(strain.available, 0)

    def test_a_forced_overflow_knocks_the_character_out_and_clamps(self) -> None:
        strain = SystemStrain(constitution=10, temporary=9)
        self.assertFalse(strain.absorb(5, forced=True))
        self.assertEqual(strain.total, 10, "the total cannot exceed the maximum")
        self.assertEqual(strain.unconscious_hours, FORCED_OVERFLOW_UNCONSCIOUS_HOURS)

    def test_negative_additions_are_a_programming_error(self) -> None:
        with self.assertRaises(StrainError):
            SystemStrain(constitution=10).absorb(-1)


class RestTests(unittest.TestCase):
    def test_one_point_is_recovered_per_qualifying_night(self) -> None:
        strain = SystemStrain(constitution=10, temporary=5)
        self.assertEqual(strain.rest_night(), RECOVERY_PER_NIGHT)
        self.assertEqual(strain.temporary, 4)

    def test_a_short_night_recovers_nothing(self) -> None:
        strain = SystemStrain(constitution=10, temporary=5)
        self.assertEqual(strain.rest_night(hours=6), 0)
        self.assertEqual(strain.temporary, 5)

    def test_a_cold_or_hungry_night_recovers_nothing(self) -> None:
        strain = SystemStrain(constitution=10, temporary=5)
        self.assertEqual(strain.rest_night(warm_fed_comfortable=False), 0)
        self.assertEqual(strain.temporary, 5)

    def test_rest_does_not_recover_permanent_cyberware_strain(self) -> None:
        strain = SystemStrain(constitution=10)
        self.assertTrue(strain.install_cyber(3))
        self.assertEqual(strain.rest_night(), 0, "nothing temporary to recover")
        self.assertEqual(strain.permanent, 3)

    def test_rest_clears_the_forced_unconsciousness(self) -> None:
        strain = SystemStrain(constitution=10, temporary=9.5)
        strain.absorb(2, forced=True)
        self.assertGreater(strain.unconscious_hours, 0)
        strain.rest_night()
        self.assertEqual(strain.unconscious_hours, 0)


class CyberwareTests(unittest.TestCase):
    def test_installation_adds_permanent_strain(self) -> None:
        strain = SystemStrain(constitution=10)
        self.assertTrue(strain.install_cyber(2.5))
        self.assertEqual(strain.permanent, 2.5, "permanent Strain may be fractional")
        self.assertEqual(strain.available, 7.5)

    def test_the_body_cannot_support_more_than_the_maximum(self) -> None:
        strain = SystemStrain(constitution=6, temporary=2)
        self.assertFalse(strain.install_cyber(5))
        self.assertEqual(strain.permanent, 0)

    def test_removing_the_cyber_removes_its_permanent_strain(self) -> None:
        strain = SystemStrain(constitution=10)
        strain.install_cyber(3)
        strain.remove_cyber(3)
        self.assertEqual(strain.permanent, 0)
        self.assertEqual(strain.available, 10)

    def test_removal_never_goes_below_zero(self) -> None:
        strain = SystemStrain(constitution=10)
        strain.install_cyber(1)
        strain.remove_cyber(4)
        self.assertEqual(strain.permanent, 0)

    def test_cyberware_can_fill_the_last_point(self) -> None:
        strain = SystemStrain(constitution=8, temporary=6)
        self.assertTrue(strain.install_cyber(2))
        self.assertEqual(strain.total, 8)


if __name__ == "__main__":
    unittest.main()
