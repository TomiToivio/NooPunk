"""Major Injury outcomes — assertions traced to the CWN SRD d12 table."""
import unittest

from src.rules import cwn_major_injury as injury


class TableTests(unittest.TestCase):
    def test_every_roll_from_one_to_twelve_resolves(self) -> None:
        for roll in range(1, 13):
            with self.subTest(roll=roll):
                outcome = injury.resolve_major_injury(roll)
                self.assertEqual(outcome.roll, roll)

    def test_rolls_below_one_count_as_one(self) -> None:
        self.assertEqual(injury.resolve_major_injury(0).id, "instant_death")
        self.assertEqual(injury.resolve_major_injury(-5).id, "instant_death")

    def test_rolls_above_twelve_count_as_twelve(self) -> None:
        self.assertEqual(injury.resolve_major_injury(13).id, "flesh_wound")
        self.assertEqual(injury.resolve_major_injury(40).id, "flesh_wound")

    def test_a_modifier_moves_the_row_and_still_clamps(self) -> None:
        self.assertEqual(injury.resolve_major_injury(5, modifier=1).roll, 6)
        self.assertEqual(injury.resolve_major_injury(5, modifier=-9).roll, 1)
        self.assertEqual(injury.resolve_major_injury(10, modifier=9).roll, 12)

    def test_eleven_and_twelve_are_the_same_flesh_wound(self) -> None:
        self.assertEqual(injury.resolve_major_injury(11).id, injury.resolve_major_injury(12).id)
        self.assertTrue(injury.resolve_major_injury(11).flesh_wound)


class ConsequenceTests(unittest.TestCase):
    def test_only_row_one_is_lethal(self) -> None:
        lethal = [roll for roll in range(1, 13) if injury.resolve_major_injury(roll).lethal]
        self.assertEqual(lethal, [1])

    def test_internal_damage_and_gut_wound_kill_within_an_hour_without_care(self) -> None:
        for roll in (2, 5):
            with self.subTest(roll=roll):
                self.assertEqual(injury.dies_without_care_within(injury.resolve_major_injury(roll)), 1)
        self.assertIsNone(injury.dies_without_care_within(injury.resolve_major_injury(3)))

    def test_coma_rows_need_prosthetic_cyber(self) -> None:
        for roll in (2, 3):
            with self.subTest(roll=roll):
                outcome = injury.resolve_major_injury(roll)
                self.assertTrue(outcome.coma_until_prosthetic)
                self.assertTrue(injury.requires_prosthetic(outcome))

    def test_eye_damage_blinds_until_cybereyes(self) -> None:
        outcome = injury.resolve_major_injury(4)
        self.assertTrue(outcome.blinded_until_cybereyes)
        self.assertTrue(injury.requires_prosthetic(outcome))

    def test_limb_rows_name_the_limb_and_its_cyber(self) -> None:
        expected = {6: "right leg", 7: "left leg", 8: "right arm", 9: "left arm"}
        for roll, limb in expected.items():
            with self.subTest(roll=roll):
                outcome = injury.resolve_major_injury(roll)
                self.assertEqual(outcome.ruined_limb, limb)
                self.assertIn(limb, injury.damaged_cyber_locations(outcome))
                self.assertTrue(injury.requires_prosthetic(outcome))

    def test_brain_and_internal_damage_name_their_cyber_locations(self) -> None:
        self.assertEqual(set(injury.damaged_cyber_locations(injury.resolve_major_injury(2))),
                         {"Body", "Nerves"})
        self.assertEqual(set(injury.damaged_cyber_locations(injury.resolve_major_injury(3))),
                         {"Head", "Nerves"})

    def test_system_damage_targets_the_most_strain_expensive_implant(self) -> None:
        outcome = injury.resolve_major_injury(10)
        self.assertTrue(outcome.damaged_most_expensive_implant)
        self.assertIsNone(outcome.ruined_limb)

    def test_a_flesh_wound_needs_no_treatment(self) -> None:
        outcome = injury.resolve_major_injury(12)
        self.assertFalse(outcome.is_permanent_without_treatment)
        self.assertFalse(injury.requires_prosthetic(outcome))

    def test_stabilisation_alone_does_not_restore_a_permanent_injury(self) -> None:
        self.assertTrue(injury.resolve_major_injury(6).is_permanent_without_treatment)
        self.assertFalse(injury.resolve_major_injury(12).is_permanent_without_treatment)


if __name__ == "__main__":
    unittest.main()
