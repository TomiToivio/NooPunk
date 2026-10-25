import unittest
from src.rules.noopunk_social_extensions import LocalCrisis, NHIContact


class LocalCrisisTests(unittest.TestCase):
    def test_only_affected_locality_changes(self):
        helsinki = LocalCrisis()
        ukweli = LocalCrisis()
        helsinki.apply(lost_supplies=2, cooperation=-1, hazard=3)
        self.assertEqual((helsinki.scarcity, helsinki.trust, helsinki.exposure), (2, 2, 3))
        self.assertEqual((ukweli.scarcity, ukweli.trust, ukweli.exposure), (0, 3, 0))
        self.assertEqual(LocalCrisis.from_dict(helsinki.to_dict()), helsinki)

    def test_tracks_are_bounded(self):
        crisis = LocalCrisis()
        crisis.apply(lost_supplies=30, cooperation=-20, hazard=10)
        self.assertEqual((crisis.scarcity, crisis.trust, crisis.exposure), (6, 0, 6))


class NHIContactTests(unittest.TestCase):
    def test_reciprocal_trade_can_undermine_autonomy(self):
        relationship = NHIContact()
        relationship.exchange(mutual_benefit=2, imposed_dependency=2)
        self.assertEqual((relationship.reciprocity, relationship.autonomy), (2, 1))
        self.assertEqual(NHIContact.from_dict(relationship.to_dict()), relationship)

    def test_constraints_fail_closed(self):
        with self.assertRaises(ValueError):
            NHIContact(reciprocity=100)
        with self.assertRaises(ValueError):
            LocalCrisis(scarcity=-1)


if __name__ == "__main__":
    unittest.main()
