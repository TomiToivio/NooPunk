import unittest

from src.rules.swn_faction_turn import Asset, Faction, FactionTurnError
from src.rules.swn_faction_operations import resolve_action, relocate_asset


class FactionOperationsTests(unittest.TestCase):
    def setUp(self):
        self.a = Faction("UNSA", 4, {"unit": Asset("unit", "UNSA", "Helsinki", 3, 3)})
        self.b = Faction("Orion", 4, {"cell": Asset("cell", "Orion", "Helsinki", 2, 2)})

    def test_attack_and_no_double_resolution(self):
        self.a.act("attack", ("unit",), target="Orion")
        result = resolve_action(self.a, self.b, action="attack", acting_asset="unit",
                                target_asset="cell", die=14, bonus=0,
                                difficulty=12, damage=1)
        self.assertTrue(result.success)
        self.assertEqual(self.b.assets["cell"].hp, 1)
        with self.assertRaises(FactionTurnError):
            resolve_action(self.a, self.b, action="attack", acting_asset="unit",
                           target_asset="cell", die=20)
        self.assertEqual(self.b.assets["cell"].hp, 1)

    def test_bad_attack_keeps_state(self):
        self.a.act("attack", ("unit",), target="Orion")
        with self.assertRaises(FactionTurnError):
            resolve_action(self.a, self.b, action="attack", acting_asset="unit",
                           target_asset="cell", die=21)
        self.assertFalse(self.a.history[-1]["resolved"])
        self.assertEqual(self.b.assets["cell"].hp, 2)

    def test_natural_one_fails_and_twenty_succeeds(self):
        self.a.act("attack", ("unit",), target="Orion")
        result = resolve_action(self.a, self.b, action="attack", acting_asset="unit",
                                target_asset="cell", die=1, bonus=100, difficulty=2)
        self.assertFalse(result.success)
        self.a.next_turn()
        self.a.act("attack", ("unit",), target="Orion")
        result = resolve_action(self.a, self.b, action="attack", acting_asset="unit",
                                target_asset="cell", die=20, bonus=-100,
                                difficulty=40, damage=2)
        self.assertTrue(result.destroyed)

    def test_movement_requires_explicit_route(self):
        self.a.act("move", ("unit",), target="Ukweli")
        with self.assertRaises(FactionTurnError):
            relocate_asset(self.a, asset_id="unit", destination="Ukweli",
                           allowed_destinations={"Tallinn"})
        self.assertEqual(self.a.assets["unit"].location, "Helsinki")
        relocate_asset(self.a, asset_id="unit", destination="Ukweli",
                       allowed_destinations={"Ukweli"})
        self.assertEqual(self.a.assets["unit"].location, "Ukweli")
        with self.assertRaises(FactionTurnError):
            relocate_asset(self.a, asset_id="unit", destination="Ukweli",
                           allowed_destinations={"Ukweli"})

    def test_location_constraint(self):
        self.b.assets["cell"].location = "Ukweli"
        self.a.act("attack", ("unit",), target="Orion")
        with self.assertRaises(FactionTurnError):
            resolve_action(self.a, self.b, action="attack", acting_asset="unit",
                           target_asset="cell", die=20)
        self.assertFalse(self.a.history[-1]["resolved"])


if __name__ == "__main__":
    unittest.main()
