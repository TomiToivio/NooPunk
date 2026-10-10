"""First #226 investigator evidence ledger tests, without inventing game canon."""
import json
import unittest

from src.rules.investigation_evidence import Evidence, EvidenceLedger


def sample(provenance="physical", id="E1"):
    return Evidence(id, "sealed object", provenance, "Helsinki case scene", "officer-1", "case-1")


class EvidenceLedgerTests(unittest.TestCase):
    def test_collect_and_append_only_history(self):
        ledger = EvidenceLedger()
        original = ledger.collect(sample())
        self.assertEqual(original.ordinal, 1)
        self.assertEqual(ledger.custodians["E1"], "officer-1")
        self.assertEqual(len(ledger.history("E1")), 1)
        with self.assertRaises(ValueError):
            ledger.collect(sample())

    def test_transfer_changes_custodian_but_preserves_history(self):
        ledger = EvidenceLedger()
        ledger.collect(sample())
        with self.assertRaises(PermissionError):
            ledger.event("E1", "stranger", "transfer", "unauthorized", recipient="lab")
        with self.assertRaises(ValueError):
            ledger.event("E1", "officer-1", "transfer", "missing recipient")
        ledger.event("E1", "officer-1", "transfer", "sealed handover", recipient="lab")
        ledger.event("E1", "lab", "analyze", "forensic examination")
        self.assertEqual([x.ordinal for x in ledger.history("E1")], [1, 2, 3])
        self.assertEqual(ledger.custodians["E1"], "lab")
        with self.assertRaises(PermissionError):
            ledger.event("E1", "officer-1", "seal", "attempted by prior custodian")

    def test_lead_is_not_automatically_proof(self):
        ledger = EvidenceLedger()
        ledger.collect(sample("psi_lead"))
        ledger.collect(sample("digital", "E2"))
        self.assertTrue(ledger.lead_only("E1"))
        self.assertFalse(ledger.lead_only("E2"))
        # No method promotes a PSI lead into a confirmed fact.
        self.assertEqual(ledger.items["E1"].provenance, "psi_lead")

    def test_serialization_and_immutable_custody_events(self):
        ledger = EvidenceLedger()
        ledger.collect(sample())
        ledger.event("E1", "officer-1", "question", "witness disputes identity")
        snapshot = json.loads(json.dumps(ledger.export()))
        self.assertEqual(snapshot["events"][1]["kind"], "question")
        self.assertEqual(snapshot["events"][1]["ordinal"], 2)
        with self.assertRaises(Exception):
            ledger.history("E1")[0].actor = "spoofed"

    def test_reject_invalid_reference_and_blank_fields(self):
        ledger = EvidenceLedger()
        with self.assertRaises(KeyError):
            ledger.history("missing")
        with self.assertRaises(ValueError):
            sample(id=" ")
        ledger.collect(sample())
        with self.assertRaises(ValueError):
            ledger.event("E1", "officer-1", "analyze", "")


if __name__ == "__main__":
    unittest.main()
