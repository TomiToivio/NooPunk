"""Scripted real CLI sessions for issue #561.

These exercise the public launcher, command loop, persistent saves and both endings.
They intentionally do not assert prose, lore, or copyright clearance.
"""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from strategy_game.casework.session import load_session
from strategy_game.casework.ubiquitous_maniacs import CASE
from strategy_game.rpg.__main__ import main


class UbiquitousManiacsCLIPlaythroughTests(unittest.TestCase):
    def run_cli(self, save, commands, *, new=False):
        argv = ["--scenario", "ubiquitous-maniacs", "--seed", "12",
                "--save", str(save)]
        if new:
            argv.append("--new")
        transcript = io.StringIO()
        with patch("builtins.input", side_effect=[*commands, "quit"]), contextlib.redirect_stdout(transcript):
            result = main(argv)
        self.assertEqual(result, 0, transcript.getvalue())
        return transcript.getvalue()

    def test_evidence_ending_from_fresh_session(self):
        with tempfile.TemporaryDirectory() as directory:
            save = Path(directory) / "evidence.json"
            output = self.run_cli(save, [
                "help", "status", "act pc_leader inspect_register", "next",
                "act harri_romppainen compare_traces",
                "act laura_falk interview_patient",
                "assemble", "resolve closed_by_evidence",
            ], new=True)
            session = load_session(save, CASE)
            self.assertTrue(session.finished)
            self.assertEqual(session.chain_progress, (3, 3))
            self.assertIn("Case closed", output)

    def test_referral_after_early_departure_and_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            save = Path(directory) / "referral.json"
            self.run_cli(save, ["act pc_leader question_orderly", "save"], new=True)
            midway = load_session(save, CASE)
            self.assertFalse(midway.finished)
            self.assertEqual(midway.scene_spec.id, "arrival")
            self.run_cli(save, ["next", "resolve closed_by_withdrawal"])
            finished = load_session(save, CASE)
            self.assertTrue(finished.finished)
            self.assertEqual(finished.scene_spec.id, "records")
            self.assertEqual(finished.chain_progress[0], 1)
            self.run_cli(save, ["status"])
            self.assertTrue(load_session(save, CASE).finished)

    def test_invalid_commands_do_not_crash_or_consume_action(self):
        with tempfile.TemporaryDirectory() as directory:
            save = Path(directory) / "errors.json"
            output = self.run_cli(save, [
                "act", "act no_such_seat inspect_register",
                "resolve closed_by_evidence", "assemble",
                "act pc_leader no_such_action",
                "act pc_leader inspect_register", "act pc_leader question_orderly",
                "next", "next", "resolve closed_by_withdrawal",
            ], new=True)
            self.assertIn("Unknown command", output)
            self.assertIn("Cannot do that", output)
            self.assertTrue(load_session(save, CASE).finished)

    def test_corrupt_save_is_rejected_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            save = Path(directory) / "corrupt.json"
            save.write_text("{not-json", encoding="utf-8")
            before = save.read_bytes()
            with patch("builtins.input", side_effect=AssertionError("should not prompt")), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    main(["--scenario", "ubiquitous-maniacs", "--save", str(save)])
            self.assertEqual(save.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
