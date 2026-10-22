"""The playtest harness itself (issue #516 evidence): behaviour, not prose.

The harness is the thing that produces the numbers the playtest document quotes, so what is pinned
here is that it measures what it claims: the same seed is the same run, a failing party still gets
the whole chain, dropping a skill that carries a clue costs the clean finding, an arbitrary party
never reaches a state with no legal action, and the one "taken out" path still closes the case.

Nothing here asserts a rule, a difficulty or an outcome distribution. A change to any of those is the
author's decision and shows up in the report's tables, not as a failing test.
"""
from __future__ import annotations

import contextlib
import io
import unittest

from strategy_game.casework import kallio
from strategy_game.tools.playtest_second_shadow import (
    ENDINGS,
    _Fixed,
    main,
    play_demo_route,
    play_minimal,
    play_random,
    play_thorough,
    render_markdown,
    summarise,
)


class RouteTests(unittest.TestCase):
    def test_every_shipped_route_reaches_an_ending(self) -> None:
        for route, approach in (
            ("investigate", ""),
            ("confront", "pressure"),
            ("confront", "force"),
            ("refer", ""),
        ):
            with self.subTest(route=route, approach=approach):
                run = play_demo_route(11, route, approach)
                self.assertTrue(run.applied)
                self.assertFalse(run.degraded)
                self.assertEqual(run.blocked_states, 0)

    def test_the_same_seed_is_the_same_run_and_the_same_transcript(self) -> None:
        first = play_demo_route(5, "confront", "force")
        second = play_demo_route(5, "confront", "force")
        self.assertEqual(first.fingerprint, second.fingerprint)
        self.assertEqual(first.as_dict(), second.as_dict())

    def test_two_seeds_differ_somewhere(self) -> None:
        # Not a rule: just that the seed is actually driving the dice in a run that rolls 15 checks.
        first = play_demo_route(0, "investigate", "")
        second = play_demo_route(1, "investigate", "")
        self.assertNotEqual(first.fingerprint, second.fingerprint)


class PolicyTests(unittest.TestCase):
    def test_the_minimal_party_reaches_the_evidence_ending_at_the_floor(self) -> None:
        run = play_minimal(3, requested="evidence")
        self.assertEqual(run.applied, "closed_by_evidence")
        self.assertEqual(run.checks, 5)  # four case checks plus the closing check
        self.assertEqual(run.chain_held, 3)
        self.assertFalse(run.partial)

    def test_walking_away_can_be_the_first_thing_the_party_does(self) -> None:
        run = play_minimal(3, requested="refer")
        self.assertEqual(run.applied, "closed_by_withdrawal")
        self.assertEqual(len(run.scenes), 0)  # no scene was left: the case closed in the first one
        self.assertEqual(run.checks, 1)  # the withdrawal's own WIL check
        self.assertEqual(run.chain_held, 0)

    def test_a_party_that_fails_every_check_still_reaches_an_ending(self) -> None:
        # The shipped chain withholds a fragment on a failure, so every check failing leaves nothing
        # to assemble. Fail-forward means the *case* still closes and the record names the gap — not
        # that a failing party is handed the whole chain.
        run = play_thorough(0, requested="evidence", rng=_Fixed(-1))
        self.assertEqual(run.chain_held, 0)
        self.assertFalse(run.partial)
        self.assertEqual(run.applied, "closed_by_withdrawal")
        self.assertEqual(set(run.chain_missing), set(kallio.CASE.chain))
        self.assertEqual(run.blocked_states, 0)
        # The price is real: failures charge complications and stress on the way.
        self.assertTrue(run.complications)
        self.assertGreater(sum(run.stress.values()), 0)

    def test_the_same_all_fail_run_withholds_nothing_when_the_option_is_off(self) -> None:
        # The control: the previous behaviour is one option call away, which is what lets the
        # document report the difference instead of asserting a preference.
        from strategy_game.casework import options

        always = options.with_chain_withholding(kallio.CASE, enabled=False)
        run = play_thorough(0, requested="evidence", rng=_Fixed(-1), spec=always)
        self.assertEqual(run.chain_held, 3)
        self.assertFalse(run.partial)
        self.assertEqual(run.applied, "closed_by_evidence")

    def test_a_party_that_never_asks_the_one_question_loses_the_clean_finding(self) -> None:
        # SAV is the only skill that can obtain the registration card, so without it both routes to
        # the manifest are gone, the chain stops at two fragments and the finding is partial.
        run = play_thorough(0, requested="evidence", skip_skills=("SAV",))
        self.assertEqual(run.chain_held, 2)
        self.assertTrue(run.partial)
        self.assertIn("unproven-chain", run.complications)
        self.assertEqual(set(run.chain_missing), {"stack-manifest"})

    def test_every_individual_skill_is_rolled_somewhere_in_the_case(self) -> None:
        # No skill is decorative: all six appear in the case's action sets, and a thorough run rolls
        # all six. REF and SOM do it through the actions that give the closing check its aspects.
        declared = {
            action.check.skill
            for scene in kallio.CASE.scenes
            for action in scene.actions
            if action.check is not None
        }
        self.assertEqual(declared, {"COG", "INT", "REF", "SAV", "SOM", "WIL"})
        run = play_thorough(0, requested="evidence")
        for skill in ("REF", "SOM"):
            self.assertGreater(run.skills.get(skill, 0), 0, run.skills)
        # And dropping one of them is no longer free: the check load falls.
        without_ref = play_thorough(0, requested="evidence", skip_skills=("REF",))
        self.assertLess(without_ref.checks, run.checks)
        without_som = play_thorough(0, requested="evidence", skip_skills=("SOM",))
        self.assertLess(without_som.checks, run.checks)

    def test_the_two_fragment_path_assembles_a_partial_finding(self) -> None:
        full = play_thorough(0, requested="evidence", rng=_Fixed(1))
        partial = play_thorough(
            0, requested="evidence", skip_scenes=("witness",), rng=_Fixed(1)
        )
        self.assertFalse(full.partial)
        self.assertTrue(partial.partial)
        self.assertEqual(partial.chain_held, 2)
        self.assertEqual(partial.applied, "closed_by_evidence")

    def test_one_fragment_is_not_enough_for_the_strong_ending(self) -> None:
        run = play_thorough(
            0,
            requested="evidence",
            skip_scenes=("witness", "stairwell"),
            rng=_Fixed(1),
        )
        self.assertEqual(run.chain_held, 1)
        self.assertFalse(run.finding)
        self.assertEqual(run.applied, "closed_by_withdrawal")


class StateTests(unittest.TestCase):
    def test_an_arbitrary_party_never_reaches_a_state_with_no_legal_action(self) -> None:
        for seed in range(40):
            with self.subTest(seed=seed):
                run = play_random(seed, abandon=0.05)
                self.assertEqual(run.blocked_states, 0)
                self.assertTrue(run.applied)

    def test_a_character_can_be_taken_out_and_the_case_still_closes(self) -> None:
        run = play_minimal(0, requested="confront", approach="force", force_loss=True)
        self.assertTrue(run.party_taken_out)
        self.assertEqual(run.applied, "closed_by_withdrawal")
        self.assertTrue(run.degraded)
        self.assertEqual(run.blocked_states, 0)
        # The injury is a named consequence on the sheet, not a number on a faction book.
        self.assertIn("Cutter wound, left forearm", run.consequences[kallio.LEADER_ID])

    def test_the_case_is_deterministic_across_policies(self) -> None:
        for requested in ENDINGS:
            with self.subTest(requested=requested):
                first = play_thorough(7, requested=requested)
                second = play_thorough(7, requested=requested)
                self.assertEqual(first.fingerprint, second.fingerprint)


class ReportTests(unittest.TestCase):
    def test_summarise_counts_what_it_is_given(self) -> None:
        runs = [play_minimal(seed, requested="evidence").as_dict() for seed in range(5)]
        stats = summarise({"evidence": runs})
        self.assertEqual(stats["evidence"]["n"], 5)
        self.assertEqual(stats["evidence"]["checks"]["mean"], 5.0)
        self.assertEqual(sum(stats["evidence"]["endings"].values()), 5)

    def test_the_entrypoint_prints_tables(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(["--seeds", "2"])
        self.assertEqual(code, 0)
        text = buffer.getvalue()
        self.assertIn("### Route replays", text)
        self.assertIn("### Determinism", text)

    def test_rendering_is_pure(self) -> None:
        # The renderer reads the measured record and nothing else: rendering twice is identical.
        import json

        runs = {"evidence": [play_minimal(0, requested="evidence").as_dict()]}
        record = {
            "method": {
                "seeds_per_run": 1,
                "seed_range": [0, 0],
                "routes": [],
                "policies": [],
                "skill_probes": [],
                "case_id": kallio.CASE_ID,
            },
            "routes": {},
            "policies": runs,
            "skills": {},
            "extremes": {},
            "determinism": {
                "runs_compared": 0,
                "mismatched": [],
                "reload_compared": 0,
                "reload_mismatched": [],
            },
        }
        first = render_markdown(record)
        second = render_markdown(json.loads(json.dumps(record)))
        self.assertEqual(first, second)
        self.assertIn("`evidence`", first)


if __name__ == "__main__":
    unittest.main()
