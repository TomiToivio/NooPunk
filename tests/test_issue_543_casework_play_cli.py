"""The interactive case CLI must play the same case with the same rules as the headless demo.

These are behavioural tests of *executable code* (issue #271): the CLI drives the real
:class:`~strategy_game.casework.session.CaseSession`, so the contract is that the human surface
adds no rule of its own — it exposes the session's actions, the session's refusals, the session's
save file and the session's resolution, and nothing else.

What is pinned:

* the CLI starts the same case the headless demo starts, and shows the seat ids a player types;
* a refusal is reported with the session's reason and changes nothing;
* an action spends exactly one character's action, and the second attempt by the same character
  is refused;
* ``end`` advances the scene;
* ``resolve`` closes the case, and refuses an unknown resolution id and a confrontation without
  an approach;
* the save file written by the CLI reloads into an equal session.
"""
from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from strategy_game.casework import kallio
from strategy_game.casework import play as play_cli
from strategy_game.casework.session import CaseSession, load_session


def _reader(commands: list[str]):
    """A reader that hands the loop the given lines, then stops."""
    pending = list(commands)

    def read(prompt: str = "") -> str:
        if not pending:
            raise EOFError
        return pending.pop(0)

    return read


def _run(commands: list[str], session: CaseSession | None = None, save_to: Path | None = None) -> str:
    """Feed commands to the CLI's loop and capture what it printed."""
    buffer = io.StringIO()
    if session is None:
        with redirect_stdout(buffer):
            play_cli.main(["--non-interactive"])
        return buffer.getvalue()
    with redirect_stdout(buffer):
        play_cli._run(session, save_to, _reader(commands))
    return buffer.getvalue()


class InteractiveCliTests(unittest.TestCase):
    """The CLI is a surface over the session, not a second implementation of it."""

    def test_the_non_interactive_view_shows_the_scene_and_the_actions(self) -> None:
        out = _run([])
        self.assertIn("The Kallio stairwell", out)
        self.assertIn("read_the_duty_log", out)
        self.assertIn("Party", out)
        # The party ids the player types must be visible.
        for seat in ("leader", "agent_1", "agent_2", "agent_3", "agent_4"):
            self.assertIn(seat, out)

    def test_the_view_shows_the_difficulty_band_behind_a_check(self) -> None:
        out = _run([])
        self.assertIn("Fair", out)

    def test_an_action_is_resolved_by_the_session(self) -> None:
        session = kallio.build_session(seed=502)
        out = _run(["act agent_2 read_the_duty_log", "quit"], session=session)
        self.assertIn("read_the_duty_log", out)
        self.assertIn("clue(s) raid-log", out)
        self.assertEqual(session.clues, ("raid-log",))

    def test_a_refused_action_reports_the_sessions_reason_and_costs_nothing(self) -> None:
        session = kallio.build_session(seed=502)
        before = (len(session.clues), len(session.intel), session.turn)
        # An action that belongs to a later scene: the session refuses it and says what is on offer.
        out = _run(["act agent_2 scan_the_stack", "quit"], session=session)
        self.assertIn("refused", out)
        self.assertIn("read_the_duty_log", out)
        self.assertEqual((len(session.clues), len(session.intel), session.turn), before)

    def test_a_character_may_act_once_and_the_second_attempt_is_refused(self) -> None:
        session = kallio.build_session(seed=502)
        out = _run(
            ["act agent_2 read_the_duty_log", "act agent_2 read_the_duty_log", "quit"],
            session=session,
        )
        self.assertIn("refused", out)
        # The action was spent by the first attempt and not twice.
        self.assertEqual(session.clues.count("raid-log"), 1)

    def test_an_unknown_action_is_refused_rather_than_raising(self) -> None:
        session = kallio.build_session(seed=502)
        out = _run(["act agent_2 open_the_pod_bay_doors", "quit"], session=session)
        self.assertIn("refused", out)

    def test_ending_a_scene_advances_to_the_next(self) -> None:
        session = kallio.build_session(seed=502)
        first = session.scene_spec.id
        _run(["end", "quit"], session=session)
        self.assertNotEqual(session.scene_spec.id, first)

    def test_resolve_closes_the_case(self) -> None:
        session = kallio.build_session(seed=502)
        out = _run(["resolve closed_by_evidence", "quit"], session=session)
        # The session refuses a resolution whose finding is not assembled yet — a refusal,
        # not a crash.
        self.assertIn("refused", out)
        self.assertFalse(session.finished)

    def test_resolve_closes_the_case_once_the_finding_is_assembled(self) -> None:
        session = kallio.build_session(seed=502)
        out = _run(
            [
                "act agent_2 read_the_duty_log",
                "act leader take_the_liaison_aside",
                "end",
                "act agent_1 interview_nila",
                "act agent_2 scan_the_stack",
                "end",
                "act agent_3 read_the_stairwell",
                "end",
                "act agent_4 supervise_the_reading",
                "end",
                "act leader assemble_the_chain",
                "resolve closed_by_evidence",
            ],
            session=session,
        )
        self.assertIn("closed_by_evidence", out)
        self.assertTrue(session.finished)

    def test_an_unknown_resolution_is_refused(self) -> None:
        session = kallio.build_session(seed=502)
        out = _run(["resolve closed_by_coffee", "quit"], session=session)
        self.assertIn("unknown resolution", out)
        self.assertFalse(session.finished)

    def test_the_confrontation_resolution_needs_an_approach(self) -> None:
        session = kallio.build_session(seed=502)
        out = _run(["resolve closed_by_confrontation", "quit"], session=session)
        self.assertIn("approach", out)
        self.assertFalse(session.finished)

    def test_the_save_file_the_cli_writes_reloads_into_an_equal_session(self) -> None:
        session = kallio.build_session(seed=502)
        with tempfile.TemporaryDirectory() as workdir:
            target = Path(workdir) / "case.json"
            _run(["act agent_2 read_the_duty_log", "save", "quit"], session=session, save_to=target)
            self.assertTrue(target.exists())
            reloaded = load_session(target, kallio.CASE)
            self.assertEqual(reloaded.scene_spec.id, session.scene_spec.id)
            self.assertEqual(reloaded.clues, session.clues)
            self.assertEqual(reloaded.intel, session.intel)

    def test_quitting_leaves_the_case_unresolved_and_says_so(self) -> None:
        session = kallio.build_session(seed=502)
        out = _run(["quit"], session=session)
        self.assertIn("Left without resolving", out)
        self.assertFalse(session.finished)

    def test_the_cli_declares_the_content_non_canonical(self) -> None:
        out = _run([])
        self.assertIn("Not canon", out)


if __name__ == "__main__":
    unittest.main()
