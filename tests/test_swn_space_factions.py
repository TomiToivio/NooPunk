import unittest
from src.rules.swn_sector import Route, Ship, SectorError
from src.rules.swn_faction_turn import Asset, Faction, FactionTurnError


class SpaceAndFactionTests(unittest.TestCase):
    def test_travel_budget_and_hazard(self):
        ship = Ship("UNSA courier", "Earth", 2, 5, 10)
        route = Route("Earth", "Outpost", 2, 4, 3, 2, "Noospace distortion")
        self.assertEqual(ship.travel(route)["hazard"], "Noospace distortion")
        self.assertEqual((ship.location, ship.fuel, ship.days_elapsed), ("Outpost", 2, 4))
        with self.assertRaises(SectorError):
            ship.travel(route)
        ship.refuel(2)
        self.assertEqual(ship.fuel, 4)

    def test_drive_restriction(self):
        ship = Ship("Survey", "A", 1, 9, 9)
        with self.assertRaises(SectorError):
            ship.travel(Route("A", "B", 2, 3, 2, 2))
        self.assertEqual(ship.location, "A")

    def test_one_action_per_turn_and_assets(self):
        faction = Faction("UNSA", 8)
        faction.add_asset(Asset("team", "UNSA", "Helsinki", 3, 3), 4)
        event = faction.act("move", ("team",), target="Ukweli")
        self.assertFalse(event["resolved"])
        with self.assertRaises(FactionTurnError):
            faction.act("attack", ("team",))
        faction.next_turn(income=2)
        self.assertEqual((faction.credits, faction.turn), (6, 2))
        self.assertEqual(faction.act("attack", ("team",))["turn"], 2)

    def test_invalid_assets(self):
        faction = Faction("UNSA", 1)
        with self.assertRaises(FactionTurnError):
            faction.add_asset(Asset("bad", "Orion", "Earth", 1, 1), 1)
        with self.assertRaises(FactionTurnError):
            faction.act("attack", ("missing",))


if __name__ == "__main__":
    unittest.main()
