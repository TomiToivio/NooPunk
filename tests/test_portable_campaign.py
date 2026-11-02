"""The portable surface must be a façade over the canonical case, not a second game.

These tests replaced the ones that pinned an invented prototype (`unsa_hq`, `hospital`,
`anomalous_clock`, and a sidequest that exists nowhere in the case material). They now pin the property
that matters for #1053/#1054: one case, one rules implementation, one save format, reached through the
`Game`/`Action`/`Outcome` vocabulary the frontends use.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from console import session as case_session  # noqa: E402
from portable_noopunk import Action, Game  # noqa: E402
from rules import investigation  # noqa: E402

SCENES = {"entrance", "corridor", "reception", "patient_room"}


class RealCaseTests(unittest.TestCase):
    def test_the_game_plays_the_repository_case(self) -> None:
        game = Game()
        self.assertEqual(game.state.case_id, "lakkahaltia")
        self.assertIn(game.state.location, SCENES)
        # No invented location survives: every reachable scene is in the case graph.
        for action in game.available_actions():
            if action.startswith("go:"):
                self.assertIn(action.split(":", 1)[1], SCENES)

    def test_discovery_grants_the_case_clues(self) -> None:
        self.assertIn("sign-in-sheet", Game().state.clues)

    def test_the_same_rules_function_is_used(self) -> None:
        self.assertIs(case_session.discover, investigation.discover)
        self.assertIs(Game().session.__class__, case_session.CaseSession)

    def test_a_full_playthrough_concludes_the_case(self) -> None:
        game = Game()
        for action in ("go:corridor", "go:reception", "go:patient_room",
                       "theory:deliberate_falsification",
                       "support:duty-roster", "support:record-1601"):
            game.apply(Action(action))
        outcome = game.apply(Action("conclude:deliberate_falsification"))
        self.assertIn("case_completed", outcome.events)
        self.assertTrue(game.state.finished)
        self.assertFalse(game.session.conclusion["case_solved_by_program"])

    def test_an_unavailable_action_is_refused_without_events(self) -> None:
        outcome = Game().apply(Action("go:patient_room"))
        self.assertEqual(outcome.events, ())
        self.assertIn("not available", outcome.message)

    def test_save_round_trip_keeps_the_case_state(self) -> None:
        game = Game()
        game.apply(Action("go:corridor"))
        restored = Game.from_json(game.to_json())
        self.assertEqual(restored.state.clues, game.state.clues)
        self.assertEqual(restored.state.location, game.state.location)
        self.assertEqual(restored.to_json(), game.to_json())

    def test_a_foreign_save_version_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            Game.from_json('{"state_version": 99}')

    def test_a_narrative_prototype_save_is_refused(self) -> None:
        """The old invented state has no place in the real case, so it must not load."""
        old = ('{"version": 1, "location": "unsa_hq", "clues": [], '
               '"sidequest_done": false, "finished": false}')
        with self.assertRaises(ValueError):
            Game.from_json(old)

    def test_repeated_actions_do_not_duplicate_clues(self) -> None:
        game = Game()
        game.apply(Action("take:sign-in-sheet"))
        game.apply(Action("look"))
        self.assertEqual(len(game.state.clues), len(set(game.state.clues)))

    def test_seeded_dice_replay(self) -> None:
        first, second = Game(), Game()
        self.assertEqual(first.apply(Action("risk:8")), second.apply(Action("risk:8")))


if __name__ == "__main__":
    unittest.main()
