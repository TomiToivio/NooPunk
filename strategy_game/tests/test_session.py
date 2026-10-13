"""Executable contracts for the controller/GameMaster session protocol (issue #304).

Code-only, per `AGENTS.md` and issue #271. These exercise the **protocol** -- authorisation,
one-authority-per-leader, declaration/resolution separation, GM recording, determinism, save/load and
replay-log provenance separation -- and never any canonical prose.

The resolver used here is a **stub**, deliberately: this package must not invent a mechanic, so the
tests supply the rules engine exactly as a caller would.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_session.py"
"""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game import session as ses  # noqa: E402
from strategy_game.local_slice import MISSIONS  # noqa: E402
from strategy_game.provenance import ProvenanceKind  # noqa: E402
from strategy_game.session import (  # noqa: E402
    CONTROLLER_KINDS,
    GM_AUTHORITIES,
    MOVE_KINDS,
    RECORD_TYPES,
    Controller,
    MoveProposal,
    SessionError,
    SessionState,
)


def stub_resolver(proposal: MoveProposal, rng: random.Random):
    """A stand-in rules engine. Rolls one die and reports it; defines no threshold.

    This stands in for the approved engine -- the test supplies it, the package never does.
    """
    die = rng.randint(1, 6)
    return {"effect": f"{proposal.kind}@{proposal.location}", "die": die}, (die,)


class FakeTableTests(unittest.TestCase):
    """A two-controller table, one of them commanding two leaders."""

    def setUp(self) -> None:
        self.s = SessionState(scenario="ukweli_local", seed=2027)
        self.s.add_controller(Controller("alice", "human", "Alice"))
        self.s.add_controller(Controller("bob", "human", "Bob"))
        # Alice commands two leaders; Bob commands one. The issue's multi-leader case.
        self.s.assign("cpu1", "alice")
        self.s.assign("cpu2", "alice")
        self.s.assign("uip1", "bob")


class VocabularyTests(FakeTableTests):
    """One move vocabulary in the package, not two."""

    def test_move_kinds_are_reused_from_the_slice_not_redeclared(self) -> None:
        self.assertEqual(MOVE_KINDS, tuple(MISSIONS))

    def test_controller_kinds_are_declared(self) -> None:
        self.assertEqual(set(CONTROLLER_KINDS), {"human", "scripted", "llm"})

    def test_an_unknown_controller_kind_is_refused(self) -> None:
        with self.assertRaises(SessionError):
            Controller("x", "wizard")

    def test_record_types_keep_the_three_classes_apart(self) -> None:
        self.assertEqual(set(RECORD_TYPES), {"player_declaration", "gm_intervention", "rule_outcome"})


class AuthorityTests(FakeTableTests):
    """One authoritative controller per leader, and no cross-leader orders."""

    def test_a_leader_may_not_be_claimed_by_two_controllers(self) -> None:
        with self.assertRaises(SessionError):
            self.s.assign("cpu1", "bob")
        self.assertEqual(self.s.controller_of("cpu1"), "alice")

    def test_reassignment_must_be_explicit(self) -> None:
        self.s.assign("cpu1", "bob", reassign=True)
        self.assertEqual(self.s.controller_of("cpu1"), "bob")

    def test_a_controller_cannot_order_anothers_leader(self) -> None:
        result = self.s.submit(MoveProposal("uip1", "alice", "campaign", "civic", turn=0))
        self.assertFalse(result.accepted)
        self.assertIn("not authorised", result.reason)

    def test_an_unknown_controller_is_rejected(self) -> None:
        result = self.s.submit(MoveProposal("cpu1", "mallory", "campaign", "civic", turn=0))
        self.assertFalse(result.accepted)
        self.assertIn("unknown controller", result.reason)

    def test_a_leader_with_no_controller_is_rejected(self) -> None:
        result = self.s.submit(MoveProposal("ulp1", "alice", "campaign", "civic", turn=0))
        self.assertFalse(result.accepted)

    def test_an_out_of_vocabulary_move_is_rejected(self) -> None:
        result = self.s.submit(MoveProposal("cpu1", "alice", "conquer", "civic", turn=0))
        self.assertFalse(result.accepted)
        self.assertIn("move kind", result.reason)

    def test_a_proposal_from_the_wrong_turn_is_rejected(self) -> None:
        result = self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=7))
        self.assertFalse(result.accepted)

    def test_one_order_per_leader_per_turn(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        second = self.s.submit(MoveProposal("cpu1", "alice", "organize", "civic", turn=0))
        self.assertFalse(second.accepted)
        self.assertIn("already has an order", second.reason)
        self.assertEqual(len(self.s.pending), 1)

    def test_one_controller_may_order_several_leaders_separately(self) -> None:
        a = self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        b = self.s.submit(MoveProposal("cpu2", "alice", "organize", "harbor", turn=0))
        self.assertTrue(a.accepted and b.accepted)
        self.assertEqual(len(self.s.pending), 2)

    def test_rejections_are_recorded_not_dropped(self) -> None:
        self.s.submit(MoveProposal("uip1", "alice", "campaign", "civic", turn=0))
        self.assertEqual(len(self.s.submissions), 1)
        self.assertFalse(self.s.submissions[0].accepted)


class DeclarationVsResolutionTests(FakeTableTests):
    """A proposal is not an outcome, and only the engine commits."""

    def test_a_proposal_does_not_commit_anything(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        self.assertEqual(len(self.s.pending), 1)
        self.assertEqual(self.s.resolved, [])
        self.assertEqual(self.s.revision, 0)

    def test_resolve_refuses_without_a_rules_engine(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        with self.assertRaises(SessionError):
            self.s.resolve()

    def test_the_supplied_engine_commits_and_clears_the_queue(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        committed = self.s.resolve(stub_resolver)
        self.assertEqual(len(committed), 1)
        self.assertEqual(self.s.pending, [])
        self.assertEqual(len(self.s.resolved), 1)
        self.assertEqual(self.s.revision, 1)

    def test_a_resolved_move_is_provenanced_as_a_simulated_outcome(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        move = self.s.resolve(stub_resolver)[0]
        self.assertEqual(move.provenance().kind, ProvenanceKind.SIMULATED)
        self.assertEqual(move.provenance().source, "rules-engine")

    def test_a_declaration_is_provenanced_as_authored_by_its_controller(self) -> None:
        proposal = MoveProposal("cpu1", "alice", "campaign", "civic", turn=0)
        self.assertEqual(proposal.provenance().kind, ProvenanceKind.AUTHORED)
        self.assertEqual(proposal.provenance().source, "controller:alice")

    def test_advance_drops_unresolved_proposals(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        self.assertEqual(self.s.advance(), 1)
        self.assertEqual(self.s.pending, [])
        self.assertEqual(self.s.resolved, [])


class GMAuthorityTests(FakeTableTests):
    """A GM move is recorded, and cannot rewrite what happened."""

    def test_a_gm_move_records_authority_origin_and_rationale(self) -> None:
        move = self.s.gm_move("external_event", "global event deck", "the model release lands locally")
        self.assertEqual(move.authority, "external_event")
        self.assertTrue(move.rationale)
        self.assertTrue(move.origin)

    def test_a_gm_move_without_a_rationale_is_refused(self) -> None:
        with self.assertRaises(SessionError):
            self.s.gm_move("story", "improv", "   ")

    def test_a_gm_move_without_an_origin_is_refused(self) -> None:
        with self.assertRaises(SessionError):
            self.s.gm_move("story", "", "because I said so")

    def test_an_unknown_gm_authority_is_refused(self) -> None:
        with self.assertRaises(SessionError):
            self.s.gm_move("because_i_am_gm", "improv", "narrative control")
        self.assertEqual(set(GM_AUTHORITIES) - {"rules"} - {"npc_dialogue"} - {"external_event"},
                         {"story", "side_drama"})

    def test_a_gm_move_is_provenanced_as_a_recorded_intervention(self) -> None:
        move = self.s.gm_move("story", "improv", "cut to a side drama")
        self.assertEqual(move.provenance().kind, ProvenanceKind.AUTHORED)
        self.assertEqual(move.provenance().source, "gm:story")

    def test_a_gm_move_cannot_rewrite_a_previous_roll(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        before = self.s.resolve(stub_resolver)[0]
        self.s.gm_move("external_event", "deck", "an anomalous interruption")
        after = self.s.resolved[0]
        self.assertEqual(after.dice, before.dice)
        self.assertEqual(after.outcome, before.outcome)
        self.assertEqual(after.revision, before.revision)

    def test_a_resolved_move_is_frozen(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        move = self.s.resolve(stub_resolver)[0]
        with self.assertRaises(Exception):
            move.dice = (6, 6)  # type: ignore[misc]

    def test_no_api_mutates_the_resolved_list_in_place(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        self.s.resolve(stub_resolver)
        for name in ("set_dice", "override", "rewrite", "force_outcome", "inject"):
            self.assertFalse(hasattr(self.s, name), name)


class DeterminismTests(FakeTableTests):
    """Determinism is a requirement, not a preference: it makes the log inspectable."""

    def _run(self, seed: int):
        s = SessionState(scenario="ukweli_local", seed=seed)
        s.add_controller(Controller("alice", "human"))
        s.assign("cpu1", "alice")
        s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        return s.resolve(stub_resolver)[0]

    def test_the_same_seed_reproduces_the_same_dice(self) -> None:
        self.assertEqual(self._run(2027).dice, self._run(2027).dice)

    def test_a_different_seed_may_differ(self) -> None:
        first = self._run(2027).dice
        self.assertTrue(any(self._run(s).dice != first for s in range(1, 40)))

    def test_an_explicit_rng_stream_overrides_the_seed(self) -> None:
        s = SessionState(seed=1)
        s.add_controller(Controller("a", "scripted"))
        s.assign("cpu1", "a")
        s.submit(MoveProposal("cpu1", "a", "campaign", "civic", turn=0))
        move = s.resolve(stub_resolver, rng=random.Random(99))[0]
        self.assertEqual(move.dice, (random.Random(99).randint(1, 6),))


class ReplayLogTests(FakeTableTests):
    """The log keeps declarations, interventions and outcomes apart, with provenance."""

    def test_the_log_separates_the_three_record_classes(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        self.s.resolve(stub_resolver)
        self.s.gm_move("story", "improv", "side drama")
        kinds = {e["record_type"] for e in self.s.log()}
        self.assertEqual(kinds, {"player_declaration", "gm_intervention", "rule_outcome"})

    def test_every_log_entry_carries_provenance(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        self.s.resolve(stub_resolver)
        self.s.gm_move("story", "improv", "side drama")
        for entry in self.s.log():
            self.assertIn("provenance", entry)
            self.assertIn(entry["provenance"]["kind"], {"unknown", "evidence", "authored", "generated", "simulated"})

    def test_a_rule_outcome_is_not_logged_as_a_declaration(self) -> None:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        self.s.resolve(stub_resolver)
        outcomes = [e for e in self.s.log() if e["record_type"] == "rule_outcome"]
        self.assertEqual(len(outcomes), 1)
        self.assertEqual(outcomes[0]["provenance"]["kind"], "simulated")


class SaveLoadTests(FakeTableTests):
    """A save replays: dice, revisions and assignments survive the round trip."""

    def _played(self) -> SessionState:
        self.s.submit(MoveProposal("cpu1", "alice", "campaign", "civic", turn=0))
        self.s.submit(MoveProposal("cpu2", "alice", "organize", "harbor", turn=0))
        self.s.resolve(stub_resolver)
        self.s.gm_move("external_event", "deck", "an interruption")
        return self.s

    def test_round_trip_preserves_dice_and_revision(self) -> None:
        original = self._played()
        restored = SessionState.from_dict(original.to_dict())
        self.assertEqual([r.dice for r in restored.resolved], [r.dice for r in original.resolved])
        self.assertEqual(restored.revision, original.revision)
        self.assertEqual(restored.turn, original.turn)

    def test_round_trip_preserves_assignments_and_the_log_shape(self) -> None:
        original = self._played()
        restored = SessionState.from_dict(original.to_dict())
        self.assertEqual(restored.assignments, original.assignments)
        self.assertEqual([e["record_type"] for e in restored.log()],
                         [e["record_type"] for e in original.log()])

    def test_round_trip_preserves_controller_identity(self) -> None:
        restored = SessionState.from_dict(self._played().to_dict())
        self.assertEqual(restored.controllers["alice"].kind, "human")
        self.assertEqual(restored.controllers["bob"].label, "Bob")


class NoMechanicAndOfflineTests(FakeTableTests):
    """The two rules that shape the whole module."""

    def test_the_module_defines_no_threshold_cost_or_turn_duration(self) -> None:
        source = Path(ses.__file__).read_text(encoding="utf-8")
        for banned in ("THRESHOLD", "SUCCESS_VALUE", "DIFFICULTY", "TURN_LIMIT", "WIN_CONDITION", "COST"):
            self.assertNotIn(banned, source, banned)

    def test_the_module_rolls_no_dice_itself(self) -> None:
        source = Path(ses.__file__).read_text(encoding="utf-8")
        self.assertNotIn("randint", source)
        self.assertNotIn("choice(", source)

    def test_the_module_needs_no_llm_or_network(self) -> None:
        source = Path(ses.__file__).read_text(encoding="utf-8")
        for banned in ("ollama", "requests", "openai", "http", "socket"):
            self.assertNotIn(f"import {banned}", source)

    def test_the_module_imports_no_laclaugpt_code(self) -> None:
        self.assertNotIn("laclaugpt", Path(ses.__file__).read_text(encoding="utf-8").lower())

    def test_reuse_is_real_not_restated(self) -> None:
        source = Path(ses.__file__).read_text(encoding="utf-8")
        self.assertIn("from .local_slice import MISSIONS", source)
        self.assertIn("from .provenance import Provenance", source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
