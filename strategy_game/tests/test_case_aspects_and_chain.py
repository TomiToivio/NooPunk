"""Aspects, withheld fragments and the two unused skills: executable contracts.

What is pinned here is that the case's *mechanics* can do what the playtest evidence said they could
not, and that doing it did not cost the properties the case already claimed:

* an aspect on the scene can be invoked on an action check — free, or for a Fate point — and the +2
  is what turns the outcome;
* a free invocation is honoured on the **opposed** closing paths (a contest and an exchange), not
  only on a passive overcome;
* a fragment a failed check does not obtain leaves a **recorded** gap: the finding is partial, the
  resolution carries the missing fragments, and the case still closes (fail-forward);
* ``REF`` and ``SOM`` are in a scene's action set, are rolled, and what they produce is spent;
* the shipped declaration keeps the confrontation options **off** — the alternatives live in
  :mod:`strategy_game.casework.options` and are measured, not chosen.

Nothing here asserts a difficulty, an ending distribution or an author decision. Every number in
this file is a fixture that makes one contract observable.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from random import Random

from strategy_game.casework import kallio, options
from strategy_game.casework.session import CaseSession, CaseworkError, load_session
from strategy_game.rpg.fate import Action, Outcome

CASE = kallio.CASE

#: The chain's own fragments, as the case declares them.
CHAIN = set(CASE.chain)

#: The declared situation aspect of each scene, for the invocation tests.
BRIEFING_ASPECT = CASE.scene("briefing").aspects[0]


class _Queue(Random):
    """A fixed queue of die faces, so one roll in a run can be pinned exactly."""

    def __new__(cls, *args, **kwargs):  # type: ignore[no-untyped-def]
        # ``_random.Random.__new__`` hands its arguments to the C constructor, which rejects a list.
        return super().__new__(cls)

    def __init__(self, faces: list[int]) -> None:
        super().__init__(0)
        self._faces = list(faces)

    def choice(self, seq):  # type: ignore[override]
        return self._faces.pop(0) if self._faces else seq[-1]


class _Plus(Random):
    """Every Fate die comes up +1: a deterministic, guaranteed good roll."""

    def choice(self, seq):  # type: ignore[override]
        return seq[-1]


class _Minus(Random):
    """Every Fate die comes up -1: a deterministic, guaranteed bad roll."""

    def choice(self, seq):  # type: ignore[override]
        return seq[0]


def _session(seed: int = 11, rng: Random | None = None) -> CaseSession:
    return kallio.build_session(seed=seed, rng=rng)


def _gathered() -> CaseSession:
    """A session holding the whole chain: one route to each fragment, all of them succeeding.

    With ``withhold_on_failure`` the routes matter, so this takes the *cheapest* route to each
    fragment and never relies on a failure handing anything over.
    """
    session = _session(rng=_Plus())
    session.act("harri_romppainen", "read_the_duty_log")
    session.end_scene()
    session.act("laura_falk", "interview_nila")
    session.act("harri_romppainen", "scan_the_stack")
    session.end_scene()
    session.act("sebastian_virtanen", "read_the_stairwell")
    session.end_scene()
    session.act("laura_univaara", "supervise_the_reading")
    session.end_scene()
    session.act("pc_leader", "assemble_the_chain")
    session.act("harri_romppainen", "pull_the_batch_signout")
    return session


class SceneAspectTests(unittest.TestCase):
    def test_a_scene_is_playable_with_its_declared_situation_aspects(self) -> None:
        session = _session()
        self.assertEqual(
            list(session.scene.aspects), list(CASE.scene("briefing").aspects)
        )
        self.assertEqual(session.scene.aspects[BRIEFING_ASPECT].free_invocations, 0)
        self.assertIn(BRIEFING_ASPECT, session.report()["aspects"])

    def test_a_paid_invocation_on_an_action_check_turns_a_tie_into_a_success(self) -> None:
        # COG 4 against Fair (2): four -1s and two 0s total 2, which is a tie.
        plain = _session(rng=_Queue([-1, -1, 0, 0]))
        tied = plain.act("harri_romppainen", "read_the_duty_log")
        self.assertIs(tied.outcome, Outcome.TIE)
        self.assertEqual(tied.total, 2)
        self.assertEqual(tied.invoked, "")

        invoked = _session(rng=_Queue([-1, -1, 0, 0]))
        sheet = invoked.sheet("harri_romppainen")
        before = sheet.fate_points
        won = invoked.act(
            "harri_romppainen", "read_the_duty_log", invoke=BRIEFING_ASPECT
        )
        self.assertIs(won.outcome, Outcome.SUCCESS)
        self.assertEqual(won.shifts, tied.shifts + 2)
        self.assertEqual(won.invoked, BRIEFING_ASPECT)
        self.assertFalse(won.free_invocation)
        self.assertEqual(sheet.fate_points, before - 1, "a paid invocation costs a Fate point")
        # A declared situation aspect carries no free invocation: that is a create-advantage reward.
        self.assertEqual(invoked.scene.aspects[BRIEFING_ASPECT].free_invocations, 0)

    def test_a_free_invocation_from_create_advantage_is_spent_on_the_next_check(self) -> None:
        session = _session(rng=_Queue([1, 1, 0, 0, -1, -1, 0, 0]))
        made = session.act("pc_leader", "hold_the_attribution")
        self.assertIs(made.outcome, Outcome.SUCCESS_WITH_STYLE)
        self.assertEqual(made.aspect, "Room to work")
        self.assertEqual(session.scene.aspects["Room to work"].free_invocations, 2)

        spent = session.act(
            "harri_romppainen", "read_the_duty_log", free_invoke="Room to work"
        )
        # The same dice that tie without an aspect are a success with one, and it cost no Fate point.
        self.assertIs(spent.outcome, Outcome.SUCCESS)
        self.assertTrue(spent.free_invocation)
        self.assertEqual(session.scene.aspects["Room to work"].free_invocations, 1)
        self.assertEqual(session.sheet("harri_romppainen").fate_points, 3)

    def test_a_free_invocation_that_does_not_exist_is_refused_not_downgraded(self) -> None:
        session = _session(rng=_Queue([-1, -1, 0, 0]))
        refused = session.act(
            "harri_romppainen", "read_the_duty_log", free_invoke=BRIEFING_ASPECT
        )
        self.assertFalse(refused.ok)
        self.assertIn("no free invocation", refused.reason)
        # Refused before the action was spent: the seat and the clue are untouched.
        self.assertEqual(session.ledger.acted, {})
        self.assertEqual(session.clues, ())

    def test_a_character_without_a_fate_point_cannot_pay_for_an_invocation(self) -> None:
        session = _session()
        sheet = session.sheet("harri_romppainen")
        sheet.fate_points = 0
        refused = session.act(
            "harri_romppainen", "read_the_duty_log", invoke=BRIEFING_ASPECT
        )
        self.assertFalse(refused.ok)
        self.assertIn("no Fate point", refused.reason)

    def test_one_check_carries_at_most_one_invocation(self) -> None:
        session = _session(rng=_Plus())
        session.act("pc_leader", "hold_the_attribution")
        refused = session.act(
            "harri_romppainen",
            "read_the_duty_log",
            free_invoke="Room to work",
            invoke=BRIEFING_ASPECT,
        )
        self.assertFalse(refused.ok)
        self.assertIn("at most one invocation", refused.reason)


class OpposedInvocationTests(unittest.TestCase):
    """The two opposed closing paths: the finding the playtest measured as ignoring ``free_invoke``."""

    def _with_bay_aspect(self) -> CaseSession:
        session = _gathered()
        made = session.act("laura_falk", "get_to_the_bay_first")
        self.assertIs(made.outcome, Outcome.SUCCESS_WITH_STYLE, made.outcome)
        self.assertEqual(session.scene.aspects["First to the loading bay"].free_invocations, 2)
        return session

    def test_the_contest_honours_a_free_invocation(self) -> None:
        # The leader's SAV 4 against Lahtinen's SAV 3: 4 vs 5 is a failure, and +2 makes it a success.
        plain = self._with_bay_aspect()
        plain._dice = _Queue([0, 0, 0, 0, 1, 1, 0, 0])  # type: ignore[attr-defined]
        lost = plain.resolve("closed_by_confrontation", seat_id="pc_leader", approach="pressure")
        self.assertIs(lost.outcome, Outcome.FAILURE)
        self.assertTrue(lost.degraded)
        self.assertEqual(lost.resolution_id, "closed_by_withdrawal")

        invoked = self._with_bay_aspect()
        invoked._dice = _Queue([0, 0, 0, 0, 1, 1, 0, 0])  # type: ignore[attr-defined]
        won = invoked.resolve(
            "closed_by_confrontation",
            seat_id="pc_leader",
            approach="pressure",
            free_invoke="First to the loading bay",
        )
        self.assertIs(won.outcome, Outcome.SUCCESS)
        self.assertFalse(won.degraded)
        self.assertEqual(won.resolution_id, "closed_by_confrontation")
        self.assertIn("Invoked 'First to the loading bay'", won.detail)
        self.assertEqual(
            invoked.scene.aspects["First to the loading bay"].free_invocations, 1,
            "the free invocation was consumed by the closing check",
        )

    def test_the_exchange_honours_a_free_invocation(self) -> None:
        # A standoff at 4 vs 4; with the aspect it is a 2-shift hit and a detention.
        plain = self._with_bay_aspect()
        plain._dice = _Queue([0, 0, 0, 0, 1, 1, 0, 0])  # type: ignore[attr-defined]
        standoff = plain.resolve("closed_by_confrontation", seat_id="pc_leader", approach="force")
        self.assertIs(standoff.outcome, Outcome.TIE)
        self.assertTrue(standoff.degraded)

        invoked = self._with_bay_aspect()
        invoked._dice = _Queue([0, 0, 0, 0, 1, 1, 0, 0])  # type: ignore[attr-defined]
        won = invoked.resolve(
            "closed_by_confrontation",
            seat_id="pc_leader",
            approach="force",
            free_invoke="First to the loading bay",
        )
        self.assertIs(won.outcome, Outcome.SUCCESS)
        self.assertFalse(won.degraded)
        self.assertIn("grey-sleeve-controller", invoked.campaign.faction().resources)

    def test_a_paid_invocation_reaches_the_opposed_path_too(self) -> None:
        session = _gathered()
        # The resolution scene declares two situation aspects; pay for one of them instead.
        declared = CASE.scene("resolution").aspects[0]
        self.assertEqual(session.scene.aspects[declared].free_invocations, 0)
        session._dice = _Queue([0, 0, 0, 0, 1, 1, 0, 0])  # type: ignore[attr-defined]
        before = session.sheet("pc_leader").fate_points
        won = session.resolve(
            "closed_by_confrontation",
            seat_id="pc_leader",
            approach="pressure",
            invoke=declared,
        )
        self.assertIs(won.outcome, Outcome.SUCCESS)
        self.assertFalse(won.degraded)
        self.assertEqual(session.sheet("pc_leader").fate_points, before - 1)

    def test_an_invocation_the_closing_check_cannot_afford_is_refused(self) -> None:
        session = _gathered()
        with self.assertRaises(CaseworkError) as caught:
            session.resolve(
                "closed_by_confrontation",
                seat_id="pc_leader",
                approach="pressure",
                free_invoke=CASE.scene("resolution").aspects[0],
            )
        self.assertIn("no free invocation", str(caught.exception))
        self.assertFalse(session.finished, "a refused invocation does not close the case")


class LossyChainTests(unittest.TestCase):
    """A fragment a failed check does not obtain leaves a gap the record can name."""

    def test_two_fragments_assemble_a_partial_finding_with_the_gap_named(self) -> None:
        session = _session(rng=_Plus())
        session.act("harri_romppainen", "read_the_duty_log")
        session.end_scene()
        session.act("laura_falk", "interview_nila")
        session.act("harri_romppainen", "scan_the_stack")
        session.end_scene()
        session.act("sebastian_virtanen", "read_the_stairwell")
        session.end_scene()
        # The witness scene is played with every die at -1: both routes to the impression fail, and
        # the fragment is withheld rather than handed over.
        session._dice = _Minus()  # type: ignore[attr-defined]
        psi = session.act("laura_univaara", "supervise_the_reading")
        self.assertIs(psi.outcome, Outcome.FAILURE)
        self.assertEqual(psi.withheld, ("impression-double",))
        self.assertNotIn("impression-double", session.clues)
        thermal = session.act("harri_romppainen", "check_the_thermal_record")
        self.assertEqual(thermal.withheld, ("impression-double",))
        # Fail-forward: the failure charged its price, the other route was still on offer, and the
        # scene ends with the party able to leave rather than stuck.
        self.assertTrue(thermal.costs)
        self.assertGreater(len(session.actions()), 0)

        session.end_scene()
        session._dice = _Plus()  # type: ignore[attr-defined]
        assembled = session.act("pc_leader", "assemble_the_chain")
        self.assertTrue(assembled.ok, assembled.reason)
        self.assertEqual(session.chain_progress, (2, 3))
        self.assertEqual(session.chain_gaps, ("impression-double",))
        finding = session.report()["findings"][0]
        self.assertTrue(finding["partial"])
        self.assertEqual(finding["missing"], ["impression-double"])
        self.assertIn("unproven-chain", session.complications)

        closed = session.resolve("closed_by_evidence", seat_id="pc_leader")
        self.assertEqual(closed.resolution_id, "closed_by_evidence")
        self.assertEqual(closed.gaps, ("impression-double",))
        self.assertIn("never obtained", closed.detail)
        self.assertIn("case-chain-incomplete", session.campaign.faction().reputation_labels)

    def test_below_the_partial_floor_the_case_still_closes_and_names_what_is_missing(self) -> None:
        session = _session(rng=_Plus())
        session.act("harri_romppainen", "read_the_duty_log")
        session.end_scene()
        session.act("laura_falk", "interview_nila")
        session._dice = _Minus()  # type: ignore[attr-defined]
        failed = session.act("harri_romppainen", "scan_the_stack")
        self.assertEqual(failed.withheld, ("stack-manifest",))
        session.act("laura_univaara", "ask_the_clinic")
        self.assertNotIn("stack-manifest", session.clues)
        session.end_scene()
        session._dice = _Plus()  # type: ignore[attr-defined]
        session.act("sebastian_virtanen", "read_the_stairwell")
        session.end_scene()
        session.act("laura_univaara", "supervise_the_reading")
        session.end_scene()
        self.assertEqual(session.chain_progress, (2, 3))

        # A party that loses a *second* fragment has nothing to assemble, and the refusal says so.
        session._dice = _Minus()  # type: ignore[attr-defined]
        lost = _session(rng=_Minus())
        for _ in range(6):
            acts = [item for item in lost.actions() if item["available"]]
            if not acts or not lost.ledger.seats_available:
                try:
                    lost.end_scene()
                except CaseworkError:
                    break
                continue
            lost.act(lost.ledger.seats_available[0], acts[0]["id"])
        refused = lost.assemble("finding-empty-sleeve")
        self.assertFalse(refused.ok)
        self.assertEqual(set(refused.missing), CHAIN)
        with self.assertRaises(CaseworkError):
            lost.resolve("closed_by_evidence")

        closed = lost.resolve("closed_by_withdrawal", seat_id="pc_leader")
        self.assertEqual(closed.resolution_id, "closed_by_withdrawal")
        self.assertEqual(set(closed.gaps), CHAIN)
        self.assertEqual(lost.report()["chain"]["missing"], list(CASE.chain))

    def test_the_withhold_setting_is_one_option_call_away(self) -> None:
        always = options.with_chain_withholding(CASE, enabled=False)
        session = kallio.build_session(seed=11, rng=_Minus(), spec=always)
        session.act("harri_romppainen", "read_the_duty_log")
        session.end_scene()
        session.act("laura_falk", "interview_nila")
        result = session.act("harri_romppainen", "scan_the_stack")
        self.assertIs(result.outcome, Outcome.FAILURE)
        self.assertEqual(result.withheld, ())
        self.assertIn("stack-manifest", result.clues)

    def test_a_tie_still_grants_the_fragment_and_a_failure_is_what_costs_it(self) -> None:
        # The line between the two bands is the whole mechanic: a tie is success at a minor cost.
        session = _session(rng=_Queue([1, 1, 1, 1, -1, 0, 0, 0]))
        session.end_scene()
        session.act("laura_falk", "interview_nila")
        tie = session.act("harri_romppainen", "scan_the_stack")
        self.assertIs(tie.outcome, Outcome.TIE)
        self.assertEqual(tie.withheld, ())
        self.assertIn("stack-manifest", tie.clues)


class SkillUseTests(unittest.TestCase):
    def test_ref_and_som_are_in_a_scene_action_set_and_are_rolled(self) -> None:
        skills = {
            (scene.id, action.id): action.check.skill
            for scene in CASE.scenes
            for action in scene.actions
            if action.check is not None
        }
        self.assertIn("REF", skills.values())
        self.assertIn("SOM", skills.values())
        session = _session(rng=_Plus())
        session.act("harri_romppainen", "read_the_duty_log")
        session.end_scene()
        session.act("laura_falk", "interview_nila")
        session.end_scene()
        session.act("sebastian_virtanen", "hold_the_hatch")
        self.assertEqual(session.scene.aspects["A shoulder under the hatch"].free_invocations, 2)
        session.end_scene()
        session.end_scene()
        session.act("laura_falk", "get_to_the_bay_first")
        self.assertEqual(session.scene.aspects["First to the loading bay"].free_invocations, 2)
        rolled = {
            event["check"]["skill"]
            for event in session.events
            if event["kind"] == "case_action" and event.get("check")
        }
        self.assertTrue({"SOM", "REF"} <= rolled, rolled)

    def test_the_two_skills_are_natural_tools_not_chain_bearers(self) -> None:
        # Giving REF or SOM a use must not quietly move the chain: the finding still comes from
        # COG/INT/SAV/WIL actions, so the SAV finding stands as evidence rather than being erased.
        givers = {
            clue
            for scene in CASE.scenes
            for action in scene.actions
            if action.check is not None and action.check.skill in ("REF", "SOM")
            for clue in action.gives
        }
        self.assertEqual(givers, set())
        for scene in CASE.scenes:
            for action in scene.actions:
                if action.check is not None and action.check.skill in ("REF", "SOM"):
                    with self.subTest(action=action.id):
                        self.assertEqual(action.check.action, Action.CREATE_ADVANTAGE)
                        self.assertTrue(action.aspect)


class ShippedOptionTests(unittest.TestCase):
    def test_the_shipped_case_leaves_the_confrontation_options_off(self) -> None:
        confrontation = CASE.resolution("closed_by_confrontation")
        self.assertEqual(confrontation.force_attack_skill, "")
        self.assertFalse(confrontation.tie_is_not_total_failure)
        for resolution in CASE.resolutions:
            self.assertEqual(resolution.force_attack_skill, "")
            self.assertFalse(resolution.tie_is_not_total_failure)

    def test_the_force_skill_option_changes_what_the_attack_reads(self) -> None:
        variant = options.with_force_attack_skill(CASE, "REF")
        self.assertEqual(variant.resolution("closed_by_confrontation").force_attack_skill, "REF")
        self.assertEqual(variant.resolution("closed_by_evidence").force_attack_skill, "")
        self.assertEqual(variant.structural_problems(), ())

        # The leader's SAV 4 against Lahtinen's REF 2 is a standoff at 4 vs 4; the same dice read as
        # the leader's REF 2 are a 2-shift loss. That is the whole of finding F2, measured.
        def exchange(spec):
            session = _gathered() if spec is CASE else _gathered_with(spec)
            session._dice = _Queue([0, 0, 0, 0, 1, 1, 0, 0])  # type: ignore[attr-defined]
            return session.resolve(
                "closed_by_confrontation", seat_id="pc_leader", approach="force"
            )

        shipped = exchange(CASE)
        self.assertIs(shipped.outcome, Outcome.TIE)
        self.assertIn("opposed attack (SAV)", shipped.detail)

        document = exchange(variant)
        self.assertIs(document.outcome, Outcome.FAILURE)
        self.assertIn("opposed attack (REF)", document.detail)
        self.assertTrue(document.degraded)

    def test_a_confrontation_option_on_a_passive_ending_is_a_structural_problem(self) -> None:
        from dataclasses import replace

        passive = replace(CASE.resolution("closed_by_evidence"), tie_is_not_total_failure=True)
        self.assertEqual(passive.opposed_by, "")
        broken = options.variant(CASE, tie_is_not_total_failure=True)
        self.assertEqual(
            [item.id for item in broken.resolutions if item.tie_is_not_total_failure],
            ["closed_by_confrontation"],
            "the helper only touches the opposed resolution",
        )
        # The declaration refuses the dead option rather than carrying a flag nothing can read.
        from strategy_game.casework.spec import CaseSpecError

        with self.assertRaises(CaseSpecError):
            replace(CASE, resolutions=(passive,)).validate()

    def test_the_tie_option_changes_whether_a_tie_ends_the_attempt(self) -> None:
        stands = options.with_tie_policy(CASE, not_total_failure=True)

        def tie_run(spec):
            session = _gathered() if spec is CASE else _gathered_with(spec)
            session._dice = _Queue([0, 0, 0, 0, 1, 1, 0, 0])  # type: ignore[attr-defined]
            result = session.resolve(
                "closed_by_confrontation", seat_id="pc_leader", approach="force"
            )
            return result

        shipped = tie_run(CASE)
        self.assertIs(shipped.outcome, Outcome.TIE)
        self.assertTrue(shipped.degraded)
        self.assertEqual(shipped.resolution_id, "closed_by_withdrawal")

        allowed = tie_run(stands)
        self.assertIs(allowed.outcome, Outcome.TIE)
        self.assertFalse(allowed.degraded)
        self.assertEqual(allowed.resolution_id, "closed_by_confrontation")


def _gathered_with(spec) -> CaseSession:
    """The same solved position, played on a variant declaration."""
    session = kallio.build_session(seed=11, rng=_Plus(), spec=spec)
    session.act("harri_romppainen", "read_the_duty_log")
    session.end_scene()
    session.act("laura_falk", "interview_nila")
    session.act("harri_romppainen", "scan_the_stack")
    session.end_scene()
    session.act("sebastian_virtanen", "read_the_stairwell")
    session.end_scene()
    session.act("laura_univaara", "supervise_the_reading")
    session.end_scene()
    session.act("pc_leader", "assemble_the_chain")
    session.act("harri_romppainen", "pull_the_batch_signout")
    return session


class FailForwardAndDeterminismTests(unittest.TestCase):
    def test_a_failing_party_never_reaches_a_state_it_cannot_leave(self) -> None:
        for seed in range(12):
            with self.subTest(seed=seed):
                session = _session(seed=seed)
                guard = 0
                while not session.finished and guard < 40:
                    guard += 1
                    acts = [item for item in session.actions() if item["available"]]
                    if not acts or not session.ledger.seats_available:
                        try:
                            session.end_scene()
                        except CaseworkError:
                            break
                        continue
                    result = session.act(session.ledger.seats_available[0], acts[0]["id"])
                    self.assertTrue(result.ok, result.reason)
                endings = [item["id"] for item in session.resolutions() if item["available"]]
                self.assertTrue(endings, "some ending is always available")
                session.resolve(endings[0], seat_id="pc_leader", approach="pressure")
                self.assertTrue(session.finished)

    def test_the_same_seed_with_an_invocation_is_the_same_record(self) -> None:
        def play() -> dict:
            session = _session(seed=29, rng=_Queue([-1, -1, 0, 0] + [1] * 40))
            session.act("harri_romppainen", "read_the_duty_log", invoke=BRIEFING_ASPECT)
            session.end_scene()
            return session.report()

        self.assertEqual(play(), play())

    def test_a_saved_case_keeps_its_scene_aspects_and_its_invocations(self) -> None:
        session = _session(rng=_Plus())
        session.act("pc_leader", "hold_the_attribution")
        self.assertEqual(session.scene.aspects["Room to work"].free_invocations, 2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            session.save(path)
            resumed = load_session(path, CASE)
        self.assertEqual(
            resumed.scene.aspects["Room to work"].free_invocations, 2, "the aspect survives a save"
        )
        self.assertIn(BRIEFING_ASPECT, resumed.scene.aspects)
        result = resumed.act(
            "harri_romppainen", "read_the_duty_log", free_invoke="Room to work"
        )
        self.assertTrue(result.ok)
        self.assertTrue(result.free_invocation)


if __name__ == "__main__":
    unittest.main()
