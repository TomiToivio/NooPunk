"""Equipment-granted PSI stays inside SWN accounting without granting new disciplines (#1196)."""
import unittest

from src.rules.psi_access import PsiAccessError, device_grant, discipline_decision
from src.rules.swn_psionics import Duration, Psychic, PsiRulesError


class DevicePsiAccountingTests(unittest.TestCase):
    def setUp(self):
        self.psychic = Psychic(wisdom=14, constitution=12, disciplines={"Telepathy": 1})
        self.grant = device_grant("Biopsionics medical effect", source="med-implant-01")

    def test_explicit_equipment_grant_uses_existing_effort_pool(self):
        before = self.psychic.free
        self.psychic.commit_device_grant(
            "med-activation", self.grant,
            active_sources={"med-implant-01"}, amount=1, duration=Duration.SCENE,
        )
        self.assertEqual(self.psychic.free, before - 1)
        self.assertNotIn("Biopsionics", self.psychic.disciplines)
        self.assertFalse(discipline_decision("Biopsionics").allowed)
        self.psychic.end_scene()
        self.assertEqual(self.psychic.free, before)

    def test_missing_inactive_equipment_refuses_grant(self):
        with self.assertRaises(PsiAccessError):
            self.psychic.commit_device_grant(
                "med-activation", self.grant,
                active_sources=set(), amount=1, duration=Duration.SCENE,
            )

    def test_invalid_cost_and_duration_are_not_invented(self):
        for amount in (0, -1, True):
            with self.subTest(amount=amount), self.assertRaises(PsiRulesError):
                self.psychic.commit_device_grant(
                    "med", self.grant, active_sources={"med-implant-01"},
                    amount=amount, duration=Duration.SCENE,
                )
        with self.assertRaises(PsiRulesError):
            self.psychic.commit_device_grant(
                "med", self.grant, active_sources={"med-implant-01"},
                amount=1, duration="scene",
            )

    def test_duplicate_keys_and_overspending_are_rejected(self):
        self.psychic.commit_device_grant(
            "med", self.grant, active_sources={"med-implant-01"},
            amount=1, duration=Duration.DAY,
        )
        with self.assertRaises(PsiRulesError):
            self.psychic.commit_device_grant(
                "med", self.grant, active_sources={"med-implant-01"},
                amount=1, duration=Duration.DAY,
            )
        with self.assertRaises(PsiRulesError):
            self.psychic.commit_device_grant(
                "other", self.grant, active_sources={"med-implant-01"},
                amount=999, duration=Duration.SCENE,
            )
        restored = Psychic.from_snapshot(self.psychic.snapshot())
        self.assertEqual(restored.free, self.psychic.free)
        restored.rest()
        self.assertEqual(restored.free, restored.capacity)


if __name__ == "__main__":
    unittest.main()
