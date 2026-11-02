"""Contract tests for independent headless frontends, over the real case (#1053, #1054)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from portable_noopunk import Action, Game  # noqa: E402
from portable_noopunk.adapters import LocalAdapter  # noqa: E402

#: A legal sequence on the repository case: walk the graph, state a theory, read evidence, conclude.
SEQUENCE = ("look", "go:corridor", "go:reception", "go:patient_room",
            "theory:deliberate_falsification", "support:duty-roster", "support:record-1601",
            "conclude:deliberate_falsification")


class AdapterContractTests(unittest.TestCase):
    def test_same_actions_same_results(self) -> None:
        direct = Game()
        adapter = LocalAdapter(Game())
        for command in SEQUENCE:
            expected = direct.apply(Action(command))
            actual = adapter.dispatch(command)
            self.assertEqual(expected, actual)
            self.assertEqual(direct.to_json(), adapter.save())
        self.assertTrue(adapter.snapshot()["finished"])

    def test_save_round_trip_and_action_validation(self) -> None:
        adapter = LocalAdapter(Game())
        # An unreachable scene is refused (no lead has been found yet), and the refusal carries
        # no event: a rejected command must never look like progress.
        self.assertEqual(adapter.dispatch("go:patient_room").events, ())
        adapter.dispatch("go:corridor")
        saved = adapter.save()
        restored = LocalAdapter.load(saved)
        self.assertEqual(restored.available_actions(), adapter.available_actions())
        self.assertEqual(restored.snapshot(), adapter.snapshot())

    def test_an_unknown_command_is_refused(self) -> None:
        adapter = LocalAdapter(Game())
        self.assertEqual(adapter.dispatch("catalogue_record").events, ())
        self.assertIn("not available", adapter.dispatch("catalogue_record").message)

    def test_snapshot_is_a_copy(self) -> None:
        adapter = LocalAdapter(Game())
        snapshot = adapter.snapshot()
        before = list(snapshot["clues"])
        snapshot["clues"].append("injected")
        self.assertEqual(adapter.snapshot()["clues"], before)


if __name__ == "__main__":
    unittest.main()
