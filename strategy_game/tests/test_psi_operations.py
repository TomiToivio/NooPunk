"""Executable validation of the declaration-only PSI operation boundary (#345)."""
import unittest

from strategy_game.psi_operations import PsiFinding, PsiOperation, PsiOperationError, PsiOperationLedger


class PsiOperationTests(unittest.TestCase):
    def setUp(self):
        self.ledger = PsiOperationLedger()
        self.operation = PsiOperation("rv-1", "leader", "suspected_site", "district", "verify_before_action", ("team",))

    def test_agent_led_assets_and_recorded_location(self):
        self.ledger.declare(self.operation, agents={"leader": object()}, assets={"team": object()})
        record = self.ledger.to_dict()["operations"][0]
        self.assertEqual((record["agent_id"], record["location_id"], record["asset_ids"]),
                         ("leader", "district", ["team"]))

    def test_asset_alone_cannot_act(self):
        with self.assertRaises(PsiOperationError):
            self.ledger.declare(self.operation, agents={}, assets={"team": object()})
        self.assertEqual(self.ledger.operations, {})

    def test_unknown_asset_refused(self):
        with self.assertRaises(PsiOperationError):
            self.ledger.declare(self.operation, agents={"leader": object()}, assets={})

    def test_duplicate_missions_refused(self):
        self.ledger.declare(self.operation, agents={"leader": object()}, assets={"team": object()})
        with self.assertRaises(PsiOperationError):
            self.ledger.declare(self.operation, agents={"leader": object()}, assets={"team": object()})

    def test_findings_remain_uncertain_and_do_not_resolve_the_world(self):
        self.ledger.declare(self.operation, agents={"leader": object()}, assets={"team": object()})
        finding = PsiFinding("rv-1", "possible signal near site", alternative_explanations=("misidentification",))
        self.ledger.report(finding)
        self.assertEqual(self.ledger.to_dict()["findings"]["rv-1"][0]["verification"], "unverified")
        self.assertNotIn("success", self.ledger.to_dict())
        self.assertNotIn("world_state", self.ledger.to_dict())

    def test_corroboration_requires_evidence(self):
        with self.assertRaises(PsiOperationError):
            PsiFinding("rv-1", "site confirmed", verification="corroborated")
        self.assertEqual(PsiFinding("rv-1", "site confirmed", "corroborated", ("physical-survey-12",)).verification, "corroborated")

    def test_invalid_and_unlinked_records_refused(self):
        with self.assertRaises(PsiOperationError):
            PsiOperation("", "leader", "target", "district", "observe")
        with self.assertRaises(PsiOperationError):
            self.ledger.report(PsiFinding("unknown", "signal"))
        with self.assertRaises(PsiOperationError):
            PsiOperation("x", "leader", "target", "district", "observe", ("team", "team"))


if __name__ == "__main__":
    unittest.main()
