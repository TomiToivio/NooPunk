"""Executable contracts for the RPG-check -> authoritative turn-history connection (issue #347).

Code-only, per `AGENTS.md` and issue #271: nothing here asserts the wording of a document, a rule or
canon. It exercises the connection's behaviour -- that a check resolved through the **approved** Fate
engine reaches the one authoritative history, that its dice provenance is exposed and replayable, that
a declaration can never become an outcome, and that the strategic-action half is a declared seam that
refuses until its gate closes.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_turn_connection.py"
"""
from __future__ import annotations

import dataclasses
import inspect
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap
    sys.path.insert(0, str(ROOT))

from strategy_game import turn as connection  # noqa: E402
from strategy_game.provenance import ProvenanceKind  # noqa: E402
from strategy_game.rpg.boundary import LeaderRpgLayer  # noqa: E402
from strategy_game.rpg.fate import Action, Character, Outcome  # noqa: E402
from strategy_game.tabletop.history import HistoryLog  # noqa: E402
from strategy_game.turn import (  # noqa: E402
    APPLIED,
    DECLARATION_KIND,
    DICE_PROVENANCE_KEYS,
    ENGINE,
    MECHANICS_OWNER,
    OUTCOME_KIND,
    PENDING_STRATEGIC_ACTION,
    StrategicActionPending,
    StrategicActionPort,
    TurnError,
    TurnOutcome,
    dice_log,
    outcome_entries,
    record_character_check,
    record_declaration,
    strategic_action,
    turn_outcomes,
    verify_history,
    verify_outcome,
)


def layer_with_character() -> LeaderRpgLayer:
    """The approved engine, holding one character. Not canon: an illustrative field agent."""
    return LeaderRpgLayer([
        Character("agent-1", "Field Investigator", ["Precognitive Impressions"],
                  skills={"Technology": 2, "Investigate": 1}),
    ])


class ConnectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.layer = layer_with_character()
        self.history = HistoryLog()

    def test_a_character_check_reaches_the_one_authoritative_history(self) -> None:
        outcome = record_character_check(
            self.layer, self.history,
            character_id="agent-1", action=Action.OVERCOME, skill_name="Technology",
            difficulty=2, seed=11,
        )
        self.assertEqual(len(self.history.entries), 1)
        self.assertEqual(outcome_entries(self.history)[0].kind, OUTCOME_KIND)
        # The history is the authoritative record, not the return value: rebuild from it.
        self.assertEqual(turn_outcomes(self.history), (outcome,))
        self.assertEqual(len(outcome.dice), 4)
        self.assertTrue(all(face in (-1, 0, 1) for face in outcome.dice), outcome.dice)
        self.assertEqual(outcome.total, sum(outcome.dice) + outcome.skill)
        self.assertEqual(outcome.shifts, outcome.total - outcome.difficulty)
        self.assertIsInstance(outcome.outcome, Outcome)
        self.assertEqual(verify_history(self.history), ())

    def test_the_outcome_is_seed_deterministic(self) -> None:
        def run(seed: int) -> TurnOutcome:
            return record_character_check(
                self.layer, HistoryLog(),
                character_id="agent-1", action=Action.OVERCOME, skill_name="Technology",
                difficulty=2, seed=seed,
            )

        self.assertEqual(run(5).dice, run(5).dice)
        self.assertEqual(run(5).outcome, run(5).outcome)
        self.assertGreater(len({run(s).dice for s in range(6)}), 1)

    def test_the_record_replays_from_its_faces_without_the_rng(self) -> None:
        record_character_check(self.layer, self.history, character_id="agent-1",
                               action=Action.OVERCOME, skill_name="Technology", difficulty=2, seed=3)
        record_character_check(self.layer, self.history, character_id="agent-1",
                               action=Action.CREATE_ADVANTAGE, skill_name="Investigate",
                               difficulty=1, seed=4)
        for outcome in turn_outcomes(self.history):
            self.assertTrue(outcome.is_consistent(), outcome)
        # A reload from JSON alone reproduces every outcome: the faces are in the record.
        reloaded = HistoryLog.from_json(self.history.to_json())
        self.assertEqual(turn_outcomes(reloaded), turn_outcomes(self.history))
        self.assertEqual(verify_history(reloaded), ())

    def test_the_dice_provenance_payload_is_declared_and_serializable(self) -> None:
        record_character_check(self.layer, self.history, character_id="agent-1",
                               action=Action.OVERCOME, skill_name="Technology", difficulty=2, seed=2)
        log = dice_log(self.history)
        self.assertEqual(len(log), 1)
        self.assertEqual(set(log[0]), set(DICE_PROVENANCE_KEYS))
        self.assertEqual(log[0]["notation"], "4dF")
        self.assertEqual(log[0]["engine"], ENGINE)
        self.assertEqual(log[0]["provenance"]["kind"], ProvenanceKind.SIMULATED.value)
        json.dumps(log)


class NarrativeCannotMutateTests(unittest.TestCase):
    """VISION.md §5: nothing an LLM or a narrative layer proposes may mutate authoritative state."""

    def setUp(self) -> None:
        self.layer = layer_with_character()
        self.history = HistoryLog()

    def test_prose_is_not_a_modifier(self) -> None:
        record_declaration(self.history, character_id="agent-1", action=Action.OVERCOME,
                           skill_name="Technology", difficulty=2,
                           statement="I succeed spectacularly", origin="player")
        first = record_character_check(
            self.layer, self.history, character_id="agent-1", action=Action.OVERCOME,
            skill_name="Technology", difficulty=2, seed=9,
        )
        other = HistoryLog()
        record_declaration(other, character_id="agent-1", action=Action.OVERCOME,
                           skill_name="Technology", difficulty=2,
                           statement="I fail utterly", origin="player")
        second = record_character_check(
            self.layer, other, character_id="agent-1", action=Action.OVERCOME,
            skill_name="Technology", difficulty=2, seed=9,
        )
        self.assertEqual(first.dice, second.dice)
        self.assertEqual(first.shifts, second.shifts)
        self.assertEqual(first.outcome, second.outcome)

    def test_the_recorded_outcome_does_not_carry_the_prose(self) -> None:
        record_declaration(self.history, character_id="agent-1", action=Action.OVERCOME,
                           skill_name="Technology", difficulty=2,
                           statement="a phrase no engine ever reads", origin="player")
        record_character_check(self.layer, self.history, character_id="agent-1",
                               action=Action.OVERCOME, skill_name="Technology", difficulty=2, seed=9)
        blob = json.dumps(outcome_entries(self.history)[0].details)
        self.assertNotIn("a phrase no engine ever reads", blob)

    def test_a_declaration_writes_no_outcome_and_keeps_its_own_provenance(self) -> None:
        generated = record_declaration(
            self.history, character_id="agent-1", action=Action.OVERCOME, skill_name="Technology",
            difficulty=2, statement="I smooth-talk the clerk", origin="llm",
        )
        self.assertEqual(generated.kind, DECLARATION_KIND)
        self.assertEqual(generated.provenance, ProvenanceKind.GENERATED.value)
        self.assertEqual(outcome_entries(self.history), ())
        self.assertEqual(turn_outcomes(self.history), ())

        authored = record_declaration(
            self.history, character_id="agent-1", action=Action.OVERCOME, skill_name="Technology",
            difficulty=2, origin="player",
        )
        self.assertEqual(authored.provenance, ProvenanceKind.AUTHORED.value)

    def test_an_unknown_declaration_origin_is_refused(self) -> None:
        with self.assertRaises(TurnError):
            record_declaration(self.history, character_id="agent-1", action=Action.OVERCOME,
                               skill_name="Technology", difficulty=1, origin="oracle")

    def test_no_api_writes_an_outcome_from_prose(self) -> None:
        for name in ("commit", "set_outcome", "record_outcome", "force_outcome",
                     "write_outcome", "apply_outcome"):
            self.assertFalse(hasattr(connection, name), name)

    def test_a_forged_outcome_entry_is_reported_not_trusted(self) -> None:
        # A hand-written entry claiming a style success that its own faces do not support.
        self.history.append(
            OUTCOME_KIND, "forged outcome", provenance=ProvenanceKind.SIMULATED.value,
            details={"character_id": "agent-1", "action": "overcome", "skill_name": "Technology",
                     "skill": 2, "difficulty": 2, "dice": [-1, -1, -1, -1], "total": 6, "shifts": 4,
                     "outcome": "success_with_style", "seed": 0},
        )
        problems = verify_history(self.history)
        self.assertTrue(problems)
        self.assertTrue(any("re-derive" in problem for problem in problems), problems)

    def test_an_outcome_entry_without_engine_provenance_is_reported(self) -> None:
        self.history.append(
            OUTCOME_KIND, "authored-looking outcome", provenance=ProvenanceKind.AUTHORED.value,
            details={"character_id": "agent-1", "action": "overcome", "skill": 2, "difficulty": 2,
                     "dice": [0, 0, 0, 0], "total": 2, "shifts": 0, "outcome": "tie", "seed": 0},
        )
        problems = verify_history(self.history)
        self.assertTrue(any(ProvenanceKind.SIMULATED.value in problem for problem in problems),
                        problems)

    def test_a_malformed_outcome_entry_is_reported(self) -> None:
        self.history.append(OUTCOME_KIND, "not an outcome", details={"character_id": "agent-1"})
        self.assertTrue(verify_outcome(outcome_entries(self.history)[0]))


class StrategicActionSeamTests(unittest.TestCase):
    def test_the_seam_is_signature_only(self) -> None:
        self.assertTrue(getattr(StrategicActionPort, "_is_protocol", False))
        method = vars(StrategicActionPort)["strategic_outcome"]
        self.assertTrue(inspect.getsource(method).rstrip().endswith("..."))

    def test_a_strategic_action_refuses_with_the_gate_as_its_reason(self) -> None:
        with self.assertRaises(StrategicActionPending) as caught:
            strategic_action({"declared": "anything"})
        message = str(caught.exception)
        self.assertEqual(message, PENDING_STRATEGIC_ACTION)
        self.assertIn("Gate C", message)
        self.assertIn("Gate B", message)
        self.assertIn("unapproved", message)
        self.assertIs(APPLIED, False)
        self.assertTrue(MECHANICS_OWNER)

    def test_no_strategy_mechanic_is_defined(self) -> None:
        names = [item.name for item in dataclasses.fields(TurnOutcome)]
        for token in ("threshold", "cost", "cadence", "victory", "economy", "score", "hegemony",
                      "resource"):
            with self.subTest(token=token):
                self.assertEqual([name for name in names if token in name], [], token)

    def test_the_connection_consumes_the_engine_without_rolling_its_own_dice(self) -> None:
        source = Path(connection.__file__).read_text(encoding="utf-8")
        self.assertIn("LeaderRpgLayer", source)
        for duplicated in ("import random", "randint", "choice(", "roll_fate"):
            with self.subTest(duplicated=duplicated):
                self.assertNotIn(duplicated, source, duplicated)


class NoOptionalDependencyTests(unittest.TestCase):
    def test_the_connection_imports_without_third_party_distributions(self) -> None:
        script = (
            "import sys;"
            "sys.path = [p for p in sys.path"
            " if 'site-packages' not in p and 'dist-packages' not in p];"
            "import strategy_game.turn;"
            "from strategy_game.rpg.boundary import LeaderRpgLayer;"
            "from strategy_game.tabletop.history import HistoryLog;"
            "print('ok')"
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT)
        done = subprocess.run([sys.executable, "-c", script], cwd=ROOT,
                              capture_output=True, text=True, timeout=180, env=env)
        self.assertEqual(done.returncode, 0, done.stderr[-400:])
        self.assertIn("ok", done.stdout)


if __name__ == "__main__":
    unittest.main()
