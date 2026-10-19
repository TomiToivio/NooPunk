"""The playable case, end to end (issue #502, Phase 1): behaviour, not prose.

What is pinned here is what the slice claims: the five seats take one action each per scene, three
different resolutions are reachable, a failed check advances the case at a price instead of stopping
it, a clue chain has to be assembled, a case saved mid-play resumes into the same run, completion is
idempotent, the same seed produces the same record, and every persistent change went through the
campaign's one writer.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from random import Random

from strategy_game.campaign.state import load_campaign, save_campaign
from strategy_game.casework import kallio
from strategy_game.casework.session import CaseSession, CaseworkError, load_session
from strategy_game.rpg.fate import Outcome

CASE = kallio.CASE

#: ``(seat, action)`` steps; ``None`` means "leave the scene".
SCRIPT: tuple[tuple[str, str] | None, ...] = (
    ("harri_romppainen", "read_the_duty_log"),
    ("pc_leader", "take_the_liaison_aside"),
    None,
    ("laura_falk", "interview_nila"),
    ("harri_romppainen", "scan_the_stack"),
    None,
    ("sebastian_virtanen", "read_the_stairwell"),
    ("laura_falk", "search_the_landing"),
    None,
    ("laura_univaara", "supervise_the_reading"),
    ("harri_romppainen", "check_the_thermal_record"),
    None,
    ("pc_leader", "assemble_the_chain"),
    ("harri_romppainen", "pull_the_batch_signout"),
)


class _MinusOne(Random):
    """Four Fate dice that always come up -1: a deterministic, guaranteed bad roll."""

    def choice(self, seq):  # type: ignore[override]
        return seq[0]


class _PlusOne(Random):
    """Four Fate dice that always come up +1: a deterministic, guaranteed good roll."""

    def choice(self, seq):  # type: ignore[override]
        return seq[-1]


class _Scripted(Random):
    """A fixed queue of die faces, so an opposed exchange can be lost on purpose."""

    def __new__(cls, *args, **kwargs):  # type: ignore[no-untyped-def]
        # ``_random.Random.__new__`` hands its arguments to the C constructor, so a list argument
        # is rejected before ``__init__`` runs. Build the instance bare and fill the queue after.
        return super().__new__(cls)

    def __init__(self, values: list[int]) -> None:
        super().__init__(0)
        self._values = list(values)

    def choice(self, seq):  # type: ignore[override]
        return self._values.pop(0) if self._values else seq[0]


def _session(seed: int = 461, rng: Random | None = None) -> CaseSession:
    return kallio.build_session(seed=seed, rng=rng)


def _play(session: CaseSession, steps=SCRIPT) -> None:
    for step in steps:
        if step is None:
            session.end_scene()
        else:
            result = session.act(*step)
            if not result.ok:
                raise AssertionError(f"{step} was refused: {result.reason}")


def _gather_without_psi(session: CaseSession) -> None:
    """Two chain fragments only: the physical routes, no reading and no thermal check."""
    session.act("harri_romppainen", "read_the_duty_log")
    session.end_scene()
    session.act("laura_falk", "interview_nila")
    session.act("harri_romppainen", "scan_the_stack")
    session.end_scene()
    session.act("sebastian_virtanen", "read_the_stairwell")
    session.end_scene()


class RosterAndSceneTests(unittest.TestCase):
    def test_each_character_acts_once_per_scene(self) -> None:
        session = _session()
        first = session.act("pc_leader", "take_the_liaison_aside")
        self.assertTrue(first.ok)
        second = session.act("pc_leader", "hold_the_attribution")
        self.assertFalse(second.ok)
        self.assertIn("already acted", second.reason)
        session.end_scene()
        third = session.act("pc_leader", "interview_nila")
        self.assertTrue(third.ok)

    def test_the_leader_and_all_four_agents_can_act(self) -> None:
        self.assertEqual(len(_session().seats), 5)
        seats = [seat.character_id for seat in _session().seats]
        self.assertEqual(seats[0], kallio.LEADER_ID)
        self.assertEqual(tuple(seats[1:]), kallio.AGENT_IDS)
        for character_id in seats:
            with self.subTest(character=character_id):
                session = _session()
                self.assertTrue(session.act(character_id, "read_the_duty_log").ok)
                self.assertIn("raid-log", session.clues)

    def test_no_action_is_locked_to_one_character(self) -> None:
        one = _session()
        two = _session()
        self.assertTrue(one.act("harri_romppainen", "read_the_duty_log").ok)
        self.assertTrue(two.act("laura_falk", "read_the_duty_log").ok)
        self.assertIn("raid-log", one.clues)
        self.assertIn("raid-log", two.clues)

    def test_a_scene_advances_when_the_party_leaves_it(self) -> None:
        session = _session()
        self.assertEqual(session.scene_spec.id, "briefing")
        session.end_scene()
        self.assertEqual(session.scene_spec.id, "victim")
        self.assertEqual(session.turn, 1)
        self.assertEqual(session.seats_available(), tuple(seat.id for seat in session.seats))


class FailForwardTests(unittest.TestCase):
    def test_a_failed_check_yields_its_clue_and_charges_a_price(self) -> None:
        session = _session(rng=_MinusOne())
        result = session.act("laura_falk", "read_the_duty_log")
        self.assertTrue(result.ok)
        self.assertIs(result.outcome, Outcome.FAILURE)
        self.assertIn("raid-log", result.clues)
        self.assertIn("raid-log", session.clues)
        self.assertTrue(any("duty-log-incomplete" in cost for cost in result.costs), result.costs)
        self.assertTrue(session.campaign.sheets["laura_falk"].mental_stress[0])
        # The case goes on: the next action in the same scene still resolves.
        self.assertTrue(session.act("pc_leader", "take_the_liaison_aside").ok)

    def test_a_tie_pays_the_minor_price_and_still_yields_the_clue(self) -> None:
        # Without the duty log there is no camera clock to pull the mesh log against: the refusal
        # costs the action nothing and is returned with its reason.
        session = _session(rng=_MinusOne())
        session.end_scene()
        session.end_scene()
        refused = session.act("harri_romppainen", "pull_the_mesh_log")
        self.assertFalse(refused.ok)
        self.assertIn("requires", refused.reason)
        self.assertEqual(session.ledger.acted, {})
        # A scripted run: the interview passes (+4), the scan rolls -1 in total (COG 4 -> 3 against
        # Good 3), which is Fate's tie: the clue is granted at the minor price.
        session2 = _session(rng=_Scripted([1, 1, 1, 1, -1, 0, 0, 0]))
        session2.end_scene()
        session2.act("laura_falk", "interview_nila")
        tie = session2.act("harri_romppainen", "scan_the_stack")
        self.assertTrue(tie.ok)
        self.assertIs(tie.outcome, Outcome.TIE)
        self.assertIn("stack-manifest", session2.clues)
        self.assertTrue(any("clinic-logged-the-scan" in cost for cost in tie.costs), tie.costs)

    def test_a_failed_create_advantage_grants_no_aspect(self) -> None:
        session = _session(rng=_MinusOne())
        session.end_scene()
        result = session.act("laura_univaara", "promise_protection")
        self.assertTrue(result.ok)
        self.assertIs(result.outcome, Outcome.FAILURE)
        self.assertEqual(result.aspect, "")
        self.assertEqual(session.scene.aspects, {})

    def test_a_failure_never_stops_the_chain(self) -> None:
        session = _session(rng=_MinusOne())
        _play(session)
        self.assertEqual(session.chain_progress, (3, 3))
        self.assertIn("finding-empty-sleeve", session.findings)


class ChainTests(unittest.TestCase):
    def test_the_finding_cannot_be_assembled_from_nothing(self) -> None:
        session = _session()
        result = session.assemble("finding-empty-sleeve")
        self.assertFalse(result.ok)
        self.assertEqual(set(result.missing), set(CASE.chain))
        self.assertIn("cannot be assembled", result.reason)

    def test_two_fragments_assembled_partially_and_carry_the_shortfall(self) -> None:
        session = _session()
        _gather_without_psi(session)
        self.assertEqual(session.chain_progress, (2, 3))
        result = session.assemble("finding-empty-sleeve")
        self.assertTrue(result.ok)
        self.assertTrue(result.partial)
        self.assertIn("unproven-chain", session.complications)
        self.assertIn("finding-empty-sleeve", session.findings)
        again = session.assemble("finding-empty-sleeve")
        self.assertTrue(again.already)
        self.assertTrue(again.partial)

    def test_three_fragments_assemble_cleanly(self) -> None:
        session = _session()
        _play(session)
        result = session.assemble("finding-empty-sleeve")
        self.assertTrue(result.ok)
        self.assertFalse(result.partial)
        self.assertNotIn("unproven-chain", session.complications)


class ResolutionTests(unittest.TestCase):
    def _solved(self) -> CaseSession:
        session = _session(rng=_PlusOne())
        _play(session)
        return session

    def test_closing_on_the_record(self) -> None:
        session = self._solved()
        result = session.resolve("closed_by_evidence", seat_id="pc_leader")
        self.assertEqual(result.resolution_id, "closed_by_evidence")
        self.assertIs(result.outcome, Outcome.SUCCESS_WITH_STYLE)
        self.assertIn("Kallio raid case closed on the record", result.applied.objectives_completed)
        faction = session.campaign.faction()
        self.assertIn("Kallio raid case closed on the record", faction.objectives)
        self.assertIn("unsa-field-office-trust", faction.reputation_labels)
        self.assertIn("finding-empty-sleeve", faction.intelligence_ids)

    def test_closing_by_confrontation_with_words(self) -> None:
        session = self._solved()
        result = session.resolve(
            "closed_by_confrontation", seat_id="pc_leader", approach="pressure"
        )
        self.assertEqual(result.resolution_id, "closed_by_confrontation")
        faction = session.campaign.faction()
        self.assertIn("Kallio raid case closed with a detention", faction.objectives)
        self.assertIn("lahtinen-in-custody", faction.intelligence_ids)
        self.assertIn("kallio-residents-wary", faction.reputation_labels)

    def test_closing_by_confrontation_with_force(self) -> None:
        session = self._solved()
        result = session.resolve(
            "closed_by_confrontation", seat_id="laura_univaara", approach="force"
        )
        self.assertEqual(result.resolution_id, "closed_by_confrontation")
        self.assertIn("grey-sleeve-controller", session.campaign.faction().resources)

    def test_walking_away_needs_no_chain(self) -> None:
        session = _session(rng=_PlusOne())
        result = session.resolve("closed_by_withdrawal", seat_id="pc_leader")
        self.assertEqual(result.resolution_id, "closed_by_withdrawal")
        faction = session.campaign.faction()
        self.assertIn("Kallio raid case referred to Internal Affairs", faction.objectives)
        self.assertIn("internal-affairs-referral", faction.reputation_labels)

    def test_the_three_endings_are_genuinely_different(self) -> None:
        objectives = set()
        for resolution, approach in (
            ("closed_by_evidence", ""),
            ("closed_by_confrontation", "pressure"),
            ("closed_by_withdrawal", ""),
        ):
            session = self._solved() if resolution != "closed_by_withdrawal" else _session(rng=_PlusOne())
            result = session.resolve(resolution, seat_id="pc_leader", approach=approach)
            objectives.add(result.applied.objectives_completed[0])
        self.assertEqual(len(objectives), 3)

    def test_the_record_cannot_be_closed_without_the_finding(self) -> None:
        session = _session()
        with self.assertRaises(CaseworkError):
            session.resolve("closed_by_evidence")

    def test_a_confrontation_needs_the_name_to_confront(self) -> None:
        session = _session(rng=_PlusOne())
        _play(session, SCRIPT[:12])  # everything except the assembled chain and the requisition
        session.act("pc_leader", "assemble_the_chain")
        with self.assertRaises(CaseworkError) as caught:
            session.resolve("closed_by_confrontation", approach="pressure")
        self.assertIn("batch-signature", str(caught.exception))

    def test_a_lost_fight_is_dangerous_and_the_case_still_ends(self) -> None:
        # Nine guaranteed passes carry the investigation; then the leader's attack rolls four -1s
        # and Lahtinen's defence rolls four +1s, which takes the leader out.
        rng = _Scripted([1] * 36 + [-1] * 4 + [1] * 4)
        session = _session(rng=rng)
        _play(session)
        result = session.resolve(
            "closed_by_confrontation", seat_id="pc_leader", approach="force"
        )
        self.assertTrue(result.degraded)
        self.assertEqual(result.resolution_id, "closed_by_withdrawal")
        leader = session.campaign.sheets[kallio.LEADER_ID]
        self.assertIn(
            "Cutter wound, left forearm", [item.name for item in leader.consequences]
        )
        self.assertTrue(session.finished)
        self.assertIn(
            "Kallio raid case referred to Internal Affairs",
            session.campaign.faction().objectives,
        )

    def test_a_failed_closing_check_still_closes_on_the_weaker_record(self) -> None:
        session = _session(rng=_PlusOne())
        _play(session)
        session._dice = _MinusOne()  # the closing roll alone, forced to fail
        result = session.resolve("closed_by_evidence", seat_id="pc_leader")
        self.assertIs(result.outcome, Outcome.FAILURE)
        self.assertEqual(result.resolution_id, "closed_by_evidence")
        self.assertIn("unsa-field-office-doubt", session.campaign.faction().reputation_labels)
        self.assertNotIn("unsa-field-office-trust", session.campaign.faction().reputation_labels)


class PersistenceTests(unittest.TestCase):
    def _solved(self) -> CaseSession:
        session = _session(rng=_PlusOne())
        _play(session)
        return session

    def test_completion_writes_every_book_once_and_is_idempotent(self) -> None:
        session = self._solved()
        first = session.resolve("closed_by_evidence", seat_id="pc_leader")
        notes = len(session.campaign.campaign_notes)
        evidence = list(session.campaign.cases[kallio.CASE_ID].evidence_ids)
        second = session.resolve("closed_by_evidence", seat_id="pc_leader")
        self.assertTrue(second.idempotent)
        self.assertEqual(first.applied, second.applied)
        self.assertEqual(len(session.campaign.campaign_notes), notes)
        self.assertEqual(session.campaign.cases[kallio.CASE_ID].evidence_ids, evidence)
        self.assertEqual(notes, 1)
        self.assertEqual(set(evidence), set(session.clues))

    def test_the_record_reports_what_persisted(self) -> None:
        session = self._solved()
        session.resolve("closed_by_evidence", seat_id="pc_leader")
        report = session.report()
        self.assertTrue(report["finished"])
        self.assertEqual(report["chain"], {"held": 3, "of": 3})
        self.assertEqual(report["persisted"]["campaign_notes"], 1)
        self.assertIn(
            "Kallio raid case closed on the record", report["persisted"]["objectives"]
        )
        self.assertIn("finding-empty-sleeve", report["persisted"]["intelligence_ids"])
        self.assertEqual(
            set(report["persisted"]["case_evidence"]), set(session.clues)
        )
        self.assertEqual(len(report["party"]), 5)

    def test_a_case_saved_mid_play_resumes_into_the_same_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            uninterrupted = _session(seed=77)
            _play(uninterrupted)
            uninterrupted.resolve("closed_by_evidence", seat_id="pc_leader")

            resumed = _session(seed=77)
            _play(resumed, SCRIPT[:5])
            resumed.save(path)
            reloaded = load_session(path, CASE)
            self.assertEqual(reloaded.clues, resumed.clues)
            self.assertEqual(reloaded.turn, resumed.turn)
            _play(reloaded, SCRIPT[5:])
            reloaded.resolve("closed_by_evidence", seat_id="pc_leader")

            self.assertEqual(reloaded.clues, uninterrupted.clues)
            self.assertEqual(reloaded.findings, uninterrupted.findings)
            self.assertEqual(reloaded.report()["resolution"], uninterrupted.report()["resolution"])
            self.assertEqual(reloaded.campaign.to_dict(), uninterrupted.campaign.to_dict())

    def test_the_same_seed_produces_the_same_record(self) -> None:
        first = _session(seed=461)
        second = _session(seed=461)
        _play(first)
        _play(second)
        first.resolve("closed_by_evidence", seat_id="pc_leader")
        second.resolve("closed_by_evidence", seat_id="pc_leader")
        self.assertEqual(first.events, second.events)
        self.assertEqual(first.report(), second.report())

    def test_injuries_survive_a_campaign_save(self) -> None:
        # Nine guaranteed passes carry the investigation; then the leader's attack rolls four -1s
        # and Lahtinen's defence rolls four +1s, which takes the leader out.
        rng = _Scripted([1] * 36 + [-1] * 4 + [1] * 4)
        session = _session(rng=rng)
        _play(session)
        session.resolve("closed_by_confrontation", seat_id="pc_leader", approach="force")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "campaign.json"
            save_campaign(session.campaign, path)
            restored = load_campaign(path)
        leader = restored.sheets[kallio.LEADER_ID]
        self.assertIn("Cutter wound, left forearm", [item.name for item in leader.consequences])
        self.assertIn(
            "Kallio raid case referred to Internal Affairs", restored.faction().objectives
        )

    def test_a_foreign_or_mismatched_save_is_refused(self) -> None:
        session = _session()
        payload = session.to_dict()
        broken = dict(payload, schema_version="case-session-99")
        with self.assertRaises(CaseworkError):
            CaseSession.from_dict(broken, CASE)
        wrong_case = dict(payload, case_id="some-other-case")
        with self.assertRaises(CaseworkError):
            CaseSession.from_dict(wrong_case, CASE)
        with self.assertRaises(CaseworkError):
            CaseSession.from_dict(dict(payload, scene_index=99), CASE)

    def test_the_save_file_is_json_and_contains_the_campaign(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            session = _session()
            session.act("harri_romppainen", "read_the_duty_log")
            session.save(path)
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], "case-session-1")
        self.assertEqual(payload["case_id"], CASE.id)
        self.assertIn("campaign", payload)
        self.assertEqual(payload["clues"], ["raid-log"])
        self.assertEqual(len(payload["rng_state"]), 3)

    def test_a_closed_case_refuses_further_actions(self) -> None:
        session = _session(rng=_PlusOne())
        session.resolve("closed_by_withdrawal", seat_id="pc_leader")
        with self.assertRaises(CaseworkError):
            session.act("pc_leader", "read_the_duty_log")
        with self.assertRaises(CaseworkError):
            session.end_scene()


class DemoTests(unittest.TestCase):
    def test_each_route_reaches_its_own_ending(self) -> None:
        from strategy_game.casework.demo import render_text, run_demo

        expected = {
            "investigate": ("closed_by_evidence", "Kallio raid case closed on the record"),
            "confront": (
                "closed_by_confrontation",
                "Kallio raid case closed with a detention",
            ),
            "refer": (
                "closed_by_withdrawal",
                "Kallio raid case referred to Internal Affairs",
            ),
        }
        for route, (resolution, objective) in expected.items():
            with self.subTest(route=route), tempfile.TemporaryDirectory() as directory:
                result = run_demo(route, save_to=Path(directory) / "demo.json")
                self.assertEqual(result["case"]["resolution"], resolution)
                self.assertIn(objective, result["persisted"]["objectives"])
                self.assertTrue(result["reload"]["finished_after_reload"])
                self.assertEqual(result["reload"]["resolution_after_reload"], resolution)
                text = render_text(result)
                self.assertIn("Persisted in the campaign", text)
                self.assertIn(resolution, text)

    def test_the_module_entrypoint_plays_the_case(self) -> None:
        from strategy_game.casework.__main__ import main

        with tempfile.TemporaryDirectory() as directory:
            code = main(["--route", "refer", "--save", str(Path(directory) / "c.json")])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
