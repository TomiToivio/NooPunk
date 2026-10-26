import unittest

from src.rules.swn_starships import (
    Hull, Fitting, Vessel, ShipWeapon, StarshipError, resolve_attack
)


class SWNStarshipTests(unittest.TestCase):
    def setUp(self):
        self.hull = Hull("courier", 8, 7, 2, 12, 2, 13)
        self.a = Vessel("UNSA A", self.hull)
        self.a.install(Fitting("laser", 3, 2, 1))
        self.b = Vessel("Orion B", self.hull)

    def test_fitting_capacity_and_atomic_failure(self):
        with self.assertRaises(StarshipError):
            self.a.install(Fitting("oversized", 9, 1))
        self.assertEqual(set(self.a.fittings), {"laser"})
        with self.assertRaises(StarshipError):
            self.a.install(Fitting("laser", 1, 1))

    def test_save_roundtrip(self):
        data = self.a.snapshot()
        self.assertEqual(Vessel.from_snapshot(data).snapshot(), data)
        data["hp"] = 200
        with self.assertRaises(StarshipError):
            Vessel.from_snapshot(data)

    def test_hit_miss_armor_and_disabled(self):
        gun = ShipWeapon("laser", 9, 1)
        miss = resolve_attack(self.a, self.b, gun, d20=1, attack_bonus=99)
        self.assertFalse(miss.hit)
        self.assertEqual(self.b.hp, 12)
        hit = resolve_attack(self.a, self.b, gun, d20=20, attack_bonus=-99)
        self.assertEqual(hit.damage, 8)
        self.assertEqual(self.b.hp, 4)
        resolve_attack(self.a, self.b, gun, d20=20)
        self.assertFalse(self.b.operational)
        with self.assertRaises(StarshipError):
            resolve_attack(self.a, self.b, gun, d20=20)

    def test_weapon_must_be_fitted(self):
        with self.assertRaises(StarshipError):
            resolve_attack(self.a, self.b, ShipWeapon("not-equipped", 5), d20=20)


if __name__ == "__main__":
    unittest.main()
