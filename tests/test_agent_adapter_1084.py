"""The agent adapter (#1084): a model may propose an action; only the session may change anything.

The failure these tests exist to prevent is the one an LLM adapter invites: a proposal arrives with a
confident sentence attached ("I already have the badge"), the adapter believes it, and the game state
drifts away from the rules. Every assertion here is about the gate refusing to be that.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from console.agent import Proposal, load_gate

CASE = ROOT / "data" / "scenarios" / "lakkahaltia" / "case_graph.json"


class ObservationTests(unittest.TestCase):
    def test_the_observation_is_the_players_knowledge_only(self):
        gate = load_gate(CASE)
        observation = gate.observation()
        self.assertEqual(observation["scene"]["id"], "entrance")
        # Entering the first scene grants its core clue — the engine did that, not the adapter.
        self.assertEqual(observation["discovered"], ["sign-in-sheet"])
        self.assertFalse(observation["concluded"])
        self.assertIn("go", observation["verbs"])
        # Nothing that would answer the case for the model.
        for forbidden in ("solution", "answer", "correct_hypothesis", "is_guilty"):
            self.assertNotIn(forbidden, observation)

    def test_the_observation_grows_only_because_the_engine_recorded_something(self):
        gate = load_gate(CASE)
        before = gate.observation()
        gate.act("look")
        after = gate.observation()
        self.assertEqual(after["discovered"], before["discovered"],
                         "looking without a search adds nothing the engine did not grant")


class ValidationTests(unittest.TestCase):
    def test_an_unknown_verb_is_refused_with_a_reason_and_no_state_change(self):
        gate = load_gate(CASE)
        before = gate.session.to_dict()
        result = gate.act("teleport to the answer")
        self.assertFalse(result["accepted"])
        self.assertIn("unknown verb", result["reason"])
        self.assertEqual(result["changed"], [])
        self.assertEqual(gate.session.to_dict(), before)

    def test_arity_is_enforced(self):
        gate = load_gate(CASE)
        self.assertFalse(gate.act("go")["accepted"], "go needs a scene")
        self.assertFalse(gate.act("look now")["accepted"], "look takes no argument")
        self.assertFalse(gate.act("risk eight Notice Notice")["accepted"])

    def test_a_non_numeric_difficulty_is_refused(self):
        gate = load_gate(CASE)
        result = gate.act("risk brutal Notice")
        self.assertFalse(result["accepted"])
        self.assertIn("numeric difficulty", result["reason"])

    def test_an_empty_proposal_changes_nothing(self):
        gate = load_gate(CASE)
        self.assertFalse(gate.act("   ")["accepted"])


class NoRuleInTheAdapterTests(unittest.TestCase):
    def test_the_adapter_reports_the_engines_diff_not_its_own(self):
        gate = load_gate(CASE)
        result = gate.act("theory deliberate_falsification")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["changed"], ["events", "theory", "turns"],
                         "the diff is the session's own before/after, nothing the adapter computed")

    def test_a_fabricated_clue_cannot_be_taken(self):
        gate = load_gate(CASE)
        result = gate.act("take access_log")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["changed"], [])
        self.assertNotIn("access_log", gate.session.discovered)

    def test_a_claimed_result_is_not_a_result(self):
        gate = load_gate(CASE)
        before = dict(gate.session.discovered)
        result = gate.act("I rolled a 12 and found the badge")
        self.assertFalse(result["accepted"])
        self.assertEqual(gate.session.discovered, before)

    def test_the_dice_for_a_risk_come_from_the_engine_and_replay(self):
        first = load_gate(CASE, seed=7)
        second = load_gate(CASE, seed=7)
        one = first.act("risk 8 Notice")
        two = second.act("risk 8 Notice")
        self.assertEqual(one["output"], two["output"])
        self.assertEqual(first.session.to_dict(), second.session.to_dict())


class LoopTests(unittest.TestCase):
    def test_the_loop_stops_on_a_concluding_action(self):
        gate = load_gate(CASE)
        proposals = iter(["theory deliberate_falsification", "conclude deliberate_falsification"])

        seen: list[dict] = []

        def proposer(observation):
            seen.append(observation)
            return next(proposals, "")

        results = gate.run(proposer)
        self.assertEqual(len(results), 2)
        self.assertTrue(results[-1]["concluded"])
        self.assertTrue(any(observation["theory"] for observation in seen),
                        "a theory the engine recorded must reach the agent's observation")

    def test_the_loop_is_bounded(self):
        gate = load_gate(CASE)
        results = gate.run(lambda _observation: "look", max_turns=3)
        self.assertEqual(len(results), 3, "a model with no stopping condition must not spin forever")

    def test_an_empty_proposal_ends_the_loop(self):
        gate = load_gate(CASE)
        self.assertEqual(gate.run(lambda _observation: ""), [])

    def test_a_raising_action_does_not_kill_the_loop(self):
        gate = load_gate(CASE)
        result = gate.act("go nowhere")
        self.assertFalse(result["accepted"])
        self.assertIn("SessionError", result["reason"])
        self.assertEqual(result["changed"], [])


class HistoryTests(unittest.TestCase):
    def test_every_proposal_is_recorded_with_its_author(self):
        gate = load_gate(CASE)
        gate.act(Proposal("look", author="llm:test"))
        gate.act("nonsense")
        self.assertEqual([row["author"] for row in gate.history], ["llm:test", "agent"])
        self.assertEqual(gate.history[0]["proposal"], "look")
        self.assertEqual(gate.history[1]["changed"], [])


if __name__ == "__main__":
    unittest.main()
