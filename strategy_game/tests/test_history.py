"""Executable history-log contracts, not canon or prose checks."""
import unittest
from strategy_game.tabletop.history import HistoryEntry, HistoryLog


class HistoryTests(unittest.TestCase):
    def test_empty_and_roundtrip(self):
        log = HistoryLog()
        self.assertEqual(HistoryLog.from_json(log.to_json()).to_dict(), log.to_dict())

    def test_order_provenance_and_replayable_json(self):
        log = HistoryLog()
        log.append("choice", "Selected option", actor_id="person-1", provenance="player")
        log.append("roll", "Observed roll", source_id="roll-1", details={"faces": [1, 2]})
        restored = HistoryLog.from_json(log.to_json())
        self.assertEqual(restored.to_json(), log.to_json())
        self.assertEqual([item.sequence for item in restored.entries], [0, 1])
        self.assertEqual(restored.entries[0].provenance, "player")

    def test_mutable_details_cannot_rewrite_the_log(self):
        details = {"faces": [1]}
        log = HistoryLog()
        recorded = log.append("roll", "recorded", details=details)
        before = log.to_json()
        details["faces"].append(6)
        recorded.details["faces"].append(5)
        log.entries[0].details["faces"].append(4)
        self.assertEqual(log.to_json(), before)

    def test_bad_sequence_and_version_are_rejected(self):
        with self.assertRaises(ValueError):
            HistoryLog([HistoryEntry(2, "event", "out of order")])
        with self.assertRaises(ValueError):
            HistoryLog.from_dict({"schema_version": 2, "entries": []})
        with self.assertRaises(ValueError):
            HistoryLog.from_dict({"schema_version": 1, "entries": {}})
        with self.assertRaises(ValueError):
            HistoryLog().append("  ", "invalid")


if __name__ == "__main__":
    unittest.main()
