"""The Goal tag (#1119): four demonstrations, one XP economy, no second ruleset.

Each class below is one of the issue's required demonstrations — short completion, medium progress,
long-horizon contribution, faction outcome — plus the guards that keep a tag from becoming a second
economy (anti-farming, no faction XP, no reward for deletion) and the round-trip that keeps paper and
JSON saying the same thing.
"""
from __future__ import annotations

import json
import unittest

from src.rules import cwn_advancement
from src.rules.goals import (
    Goal,
    GoalError,
    GoalLog,
    Progress,
)


def _goal(identifier="g1", owner="romppainen", kind="character", horizon="short", text="Arrest Roy Batty"):
    return Goal(id=identifier, owner=owner, owner_kind=kind, description=text, horizon=horizon,
                created="2026-11-04")


class ShortGoalTests(unittest.TestCase):
    """Demonstration 1: a one-shot goal completes, retires, and pays via CWN's XP table."""

    def test_completion_retires_the_tag_and_pays_one_point(self):
        log = GoalLog()
        log.add(_goal())
        self.assertEqual([g.id for g in log.active()], ["g1"])

        finished = log.record("g1", "completed", "case:lakkahaltia", note="custody established")
        self.assertEqual(finished.status, "completed")
        self.assertEqual(log.active(), [], "a retired goal is no longer a tag on the sheet")
        self.assertEqual(len(log.retired()), 1, "but the history is kept")

        award = log.award_xp("g1", "case:lakkahaltia")
        self.assertEqual((award.xp, award.level), (1, 1))

    def test_three_completed_goals_reach_the_srd_second_level(self):
        log = GoalLog()
        for index in range(3):
            identifier = f"g{index}"
            log.add(_goal(identifier, text=f"job {index}"))
            log.record(identifier, "completed", f"case:{index}")
            log.award_xp(identifier, f"case:{index}")
        self.assertEqual(log.xp_for("romppainen"), 3)
        self.assertEqual(log.level_for("romppainen"),
                         cwn_advancement.level_for_xp(3),
                         "the level comes from the existing CWN table, not a second one")
        self.assertEqual(log.level_for("romppainen"), 2)

    def test_abandoning_or_failing_pays_nothing(self):
        log = GoalLog()
        log.add(_goal("g-fail", text="Arrest Roy Batty"))
        log.record("g-fail", "failed", "case:lakkahaltia")
        self.assertEqual(log.active(), [])
        with self.assertRaises(GoalError):
            log.award_xp("g-fail", "case:lakkahaltia")
        self.assertEqual(log.xp_for("romppainen"), 0, "deleting a tag is not a reward")

    def test_abandoning_is_not_a_status_you_can_reopen(self):
        log = GoalLog()
        log.add(_goal())
        log.record("g1", "abandoned", "case:lakkahaltia")
        with self.assertRaises(GoalError):
            log.record("g1", "completed", "case:lakkahaltia")


class MediumGoalTests(unittest.TestCase):
    """Demonstration 2: several scenarios of real progress, one completion, one award."""

    def test_progress_is_recorded_without_paying(self):
        log = GoalLog()
        log.add(_goal("promo", horizon="medium", text="Get a Promotion"))
        for case in ("case:1", "case:2", "case:3"):
            log.record("promo", "progress", case, note=f"closed {case} with both clues")
        self.assertEqual(log.xp_for("romppainen"), 0, "ordinary incremental steps do not pay")
        self.assertEqual(len(log.active()), 1, "the tag stays active while the goal is in progress")

        log.record("promo", "completed", "board:2026-11-04", note="promotion signed")
        award = log.award_xp("promo", "board:2026-11-04")
        self.assertEqual(award.level, 1)
        self.assertEqual(log.active(), [])

    def test_a_contribution_is_reserved_for_long_horizons(self):
        log = GoalLog()
        log.add(_goal("promo", horizon="medium", text="Get a Promotion"))
        with self.assertRaises(GoalError):
            log.record("promo", "contribution", "case:1",
                       note="we did something impressive")


class LongGoalTests(unittest.TestCase):
    """Demonstration 3: a direction of action that pays for distinct contributions and never closes."""

    def test_a_contribution_pays_and_the_goal_stays_active(self):
        log = GoalLog()
        log.add(_goal("x-risk", owner="unsa-field-office", kind="faction", horizon="long",
                      text="Prevent Human Extinction"))
        log.record("x-risk", "contribution", "case:rogue-asi",
                   note="stopped a breakout and preserved the containment evidence")
        self.assertEqual(len(log.active()), 1, "a long goal is not retired by progress")

    def test_the_same_event_cannot_be_paid_twice_on_one_goal(self):
        log = GoalLog()
        log.add(_goal(horizon="long", text="Prevent Human Extinction"))
        log.record("g1", "contribution", "case:rogue-asi")
        log.award_xp("g1", "case:rogue-asi")
        with self.assertRaises(GoalError):
            log.award_xp("g1", "case:rogue-asi")
        self.assertEqual(log.xp_for("romppainen"), 1)

    def test_one_event_pays_its_owner_once_even_across_two_goals(self):
        log = GoalLog()
        log.add(_goal("a", horizon="long", text="Prevent Human Extinction"))
        log.add(_goal("b", horizon="long", text="Expose the Orion infiltration"))
        log.record("a", "contribution", "case:rogue-asi")
        log.record("b", "contribution", "case:rogue-asi")
        log.award_xp("a", "case:rogue-asi")
        with self.assertRaises(GoalError) as caught:
            log.award_xp("b", "case:rogue-asi")
        self.assertIn("already been paid", str(caught.exception))

    def test_a_different_contribution_pays_again(self):
        log = GoalLog()
        log.add(_goal(horizon="long", text="Prevent Human Extinction"))
        log.record("g1", "contribution", "case:rogue-asi")
        log.record("g1", "contribution", "case:cult-cell")
        log.award_xp("g1", "case:rogue-asi")
        log.award_xp("g1", "case:cult-cell")
        self.assertEqual(log.xp_for("romppainen"), 2)


class FactionGoalTests(unittest.TestCase):
    """Demonstration 4: factions earn standing and assets, never character experience."""

    def test_a_faction_outcome_refuses_character_xp(self):
        log = GoalLog()
        log.add(_goal("memo", owner="unsa-field-office", kind="faction", horizon="medium",
                      text="Secure an institutional mandate"))
        log.record("memo", "completed", "board:2026-11-04")
        with self.assertRaises(GoalError) as caught:
            log.award_xp("memo", "board:2026-11-04")
        self.assertIn("faction rewards are assets", str(caught.exception))
        self.assertEqual(log.xp_for("unsa-field-office"), 0)

    def test_a_faction_perk_is_written_down(self):
        log = GoalLog()
        log.add(_goal("memo", owner="unsa-field-office", kind="faction", horizon="medium",
                      text="Secure an institutional mandate"))
        log.record("memo", "completed", "board:2026-11-04")
        perk = log.award_perk("memo", "two additional field agents and a Europol liaison",
                              "board:2026-11-04")
        self.assertEqual(perk["owner"], "unsa-field-office")
        self.assertEqual(len(log.perks_for("unsa-field-office")), 1)

    def test_a_character_award_does_not_transfer_to_the_faction(self):
        log = GoalLog()
        log.add(_goal("g1", horizon="short", text="Arrest Roy Batty"))
        log.record("g1", "completed", "case:1")
        log.award_xp("g1", "case:1")
        self.assertEqual(log.xp_for("unsa-field-office"), 0)

    def test_a_perk_cannot_be_recorded_twice_for_one_event(self):
        log = GoalLog()
        log.add(_goal("memo", owner="unsa", kind="faction", horizon="medium", text="mandate"))
        with self.assertRaises(GoalError):
            log.award_perk("memo", "a liaison", "board:1")
            log.award_perk("memo", "a liaison", "board:1")


class GuardTests(unittest.TestCase):
    def test_an_award_needs_recorded_evidence(self):
        log = GoalLog()
        log.add(_goal())
        with self.assertRaises(GoalError):
            log.award_xp("g1", "case:invented")

    def test_an_award_is_one_to_three_points(self):
        log = GoalLog()
        log.add(_goal())
        log.record("g1", "completed", "case:1")
        for bad in (0, 4):
            with self.assertRaises(GoalError):
                log.award_xp("g1", "case:1", xp=bad)
        self.assertEqual(log.award_xp("g1", "case:1", xp=3).xp, 3)

    def test_a_progress_entry_must_name_the_event(self):
        with self.assertRaises(GoalError):
            Progress(goal="g1", kind="progress", event="  ")

    def test_ids_are_permanent_and_unknown_ids_are_refused(self):
        log = GoalLog()
        log.add(_goal())
        with self.assertRaises(GoalError):
            log.add(_goal())
        with self.assertRaises(GoalError):
            log.goal("nope")

    def test_owner_kind_and_horizon_are_closed_vocabularies(self):
        with self.assertRaises(GoalError):
            Goal(id="x", owner="o", owner_kind="institution", description="d", horizon="short")
        with self.assertRaises(GoalError):
            Goal(id="x", owner="o", owner_kind="character", description="d", horizon="epic")
        with self.assertRaises(GoalError):
            Goal(id="x", owner="o", owner_kind="character", description="  ", horizon="short")


class PersistenceTests(unittest.TestCase):
    def _log(self):
        log = GoalLog()
        log.add(_goal("g1"))
        log.record("g1", "completed", "case:1", date="2026-11-04", note="custody")
        log.award_xp("g1", "case:1", date="2026-11-04")
        log.add(_goal("memo", owner="unsa", kind="faction", horizon="medium", text="mandate"))
        log.award_perk("memo", "a liaison", "board:1", date="2026-11-04")
        return log

    def test_the_log_round_trips_through_json(self):
        log = self._log()
        again = GoalLog.from_dict(json.loads(json.dumps(log.to_dict())))
        self.assertEqual(again.to_dict(), log.to_dict())
        self.assertEqual(again.paper("g1"), log.paper("g1"))

    def test_an_absent_log_is_an_empty_log(self):
        self.assertEqual(GoalLog.from_dict(None).to_dict()["goals"], [])
        self.assertEqual(GoalLog.from_dict({}).goals, [])

    def test_a_foreign_log_is_refused(self):
        with self.assertRaises(GoalError):
            GoalLog.from_dict({"format": "someone-else"})

    def test_disabling_the_tag_hides_the_active_list_and_erases_nothing(self):
        log = self._log()
        log.add(_goal("g2", text="Have Sex Tonight"))
        log.enabled = False
        self.assertEqual(log.active(), [])
        self.assertEqual(len(log.goals), 3, "history survives the off switch")
        self.assertEqual(len(log.awards), 1)
        log.enabled = True
        self.assertEqual(len(log.active()), 2, "the faction mandate is still active too")


class PaperTests(unittest.TestCase):
    def test_the_sheet_line_matches_the_issue_wording(self):
        log = GoalLog()
        log.add(_goal("promo", horizon="medium", text="Get a Promotion"))
        self.assertEqual(log.paper("promo"),
                         "Goal: Get a Promotion | owner: romppainen | horizon: medium | status: in progress")
        log.record("promo", "progress", "case:1", note="closed two cases with both clues")
        self.assertEqual(log.paper("promo").split("| status: ")[1], "closed two cases with both clues")


class CwnUntouchedTests(unittest.TestCase):
    def test_goals_add_no_attribute_save_or_hit_point_to_the_record(self):
        fields = set(Goal.__dataclass_fields__)
        self.assertEqual(fields, {"id", "owner", "owner_kind", "description", "horizon", "status",
                                  "created"})
        self.assertFalse({"strength", "hit_points", "ac", "save", "attack_bonus"} & fields)

    def test_the_only_rules_dependency_is_the_existing_xp_table(self):
        source = (__import__("pathlib").Path(__file__).resolve().parents[1]
                  / "src/rules/goals.py").read_text(encoding="utf-8")
        self.assertIn("from src.rules import cwn_advancement", source)
        for forbidden in ("cwn_core", "wn_core", "cwn_combat", "cwn_saves"):
            self.assertNotIn(forbidden, source)

    def test_the_award_level_is_the_advancement_module_s_answer(self):
        for xp in (0, 1, 3, 6, 12, 93):
            self.assertEqual(cwn_advancement.level_for_xp(xp),
                             cwn_advancement.level_for_xp(xp, track="fast"))


if __name__ == "__main__":
    unittest.main()
