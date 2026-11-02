"""AWN cross-scale P1 contract. No CWN or SWN rule may be modified here."""
import unittest
from src.rules.awn_world import (Enclave, Site, Crisis, WorldEvent,
                                 WorldLedger, WorldModelError)


class WorldTests(unittest.TestCase):
    def setUp(self):
        self.world = WorldLedger(region_ids={"helsinki"})
        self.world.add_enclave(Enclave("kurvi", "helsinki", "Kurvi"))
        self.world.add_site(Site("tunnel", "helsinki", "kurvi",
                                 tags=("anomaly",), hazards=("unmapped",)))
        self.world.add_crisis(Crisis("blackout", "helsinki", "Communications emergency"))

    def test_cross_scale_references_are_explicit(self):
        self.world.link_faction_asset("relay", "unsa", "kurvi")
        self.assertEqual(self.world.faction_assets["relay"], ("unsa", "kurvi"))
        with self.assertRaises(WorldModelError):
            self.world.link_faction_asset("x", "unsa", "not-here")
        with self.assertRaises(WorldModelError):
            self.world.add_site(Site("unknown", "not-here"))

    def test_only_events_change_crises(self):
        self.world.record(WorldEvent("e1", "2045-01-01", "crisis", "blackout",
                                     "relay damaged", pressure_change=2))
        self.assertEqual(self.world.crises["blackout"].pressure, 2)
        self.world.record(WorldEvent("e2", "2045-01-02", "crisis", "blackout",
                                     "relay restored", pressure_change=-2,
                                     outcome="resolved"))
        self.assertFalse(self.world.crises["blackout"].active)
        with self.assertRaises(WorldModelError):
            self.world.record(WorldEvent("e3", "2045-01-03", "crisis", "blackout",
                                         "unjustified further escalation", pressure_change=1))

    def test_no_automatic_apocalypse_or_turn(self):
        before = self.world.to_dict()
        self.assertEqual(self.world.to_dict(), before)
        self.assertEqual(self.world.crises["blackout"].pressure, 0)

    def test_evidence_provenance_required_for_missions(self):
        with self.assertRaises(WorldModelError):
            self.world.record(WorldEvent("e1", "2045-01-01", "mission", "case-1", "completed"))
        self.world.record(WorldEvent("e1", "2045-01-01", "mission", "case-1",
                                     "completed", source="campaign:case-1"))
        with self.assertRaises(WorldModelError):
            self.world.record(WorldEvent("e1", "2045-01-02", "mission", "case-1",
                                         "duplicate", source="campaign:case-1"))

    def test_serialization_and_integrity(self):
        self.world.link_faction_asset("relay", "unsa", "kurvi")
        self.world.record(WorldEvent("e1", "2045-01-01", "crisis", "blackout",
                                     "damaged", pressure_change=2))
        self.assertEqual(WorldLedger.from_dict(self.world.to_dict()).to_dict(),
                         self.world.to_dict())
        with self.assertRaises(WorldModelError):
            self.world.add_enclave(Enclave("alien", "unknown", "Unplaced"))

    def test_no_time_travel_and_no_negative_pressure(self):
        self.world.record(WorldEvent("e1", "2045-01-02", "crisis", "blackout",
                                     "damaged", pressure_change=1))
        with self.assertRaises(WorldModelError):
            self.world.record(WorldEvent("e2", "2045-01-01", "crisis", "blackout",
                                         "older", pressure_change=1))
        with self.assertRaises(WorldModelError):
            self.world.record(WorldEvent("e2", "2045-01-03", "crisis", "blackout",
                                         "underflow", pressure_change=-3))


if __name__ == "__main__":
    unittest.main()
