"""The Python AWN Stress tracker (#1083): same contract, same save, no dice of its own.

Two properties matter most and both are asserted here: the module reads every number from
`data/rules/awn_stress.json` (so a corrected table changes behaviour without a code edit), and its
save document has the same shape as the GDScript tracker's, so a campaign can move a character
between the MUD and the plain-Python library without a migration.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.rules.awn_stress import (
    TRACKER_FORMAT,
    TRACKER_VERSION,
    Stress,
    StressError,
    load_contract,
    new_tracker,
)

ROOT = Path(__file__).resolve().parents[1]


class ContractSourceTests(unittest.TestCase):
    def test_the_contract_is_the_only_source_of_numbers(self):
        contract = load_contract()
        self.assertEqual(contract["format"], "noopunk.rules.awn_stress")
        self.assertTrue(contract["module"]["optional"])
        self.assertFalse(contract["module"]["default_enabled"])

    def test_a_tracker_is_disabled_unless_the_table_turns_it_on(self):
        tracker = Stress(wisdom=10)
        self.assertFalse(tracker.enabled)
        self.assertEqual(tracker.award("kill_human"), {"ok": True, "enabled": False,
                                                       "applied": 0, "pending": 0})
        self.assertEqual(tracker.end_scene(), {"ok": True, "enabled": False})

    def test_an_unknown_contract_file_is_refused(self):
        with self.assertRaises(StressError):
            load_contract(ROOT / "data/rules/awn_region_contract.json")


class ThresholdAndGainTests(unittest.TestCase):
    def test_the_ceiling_is_wisdom_and_equality_is_safe(self):
        tracker = new_tracker(3, enabled=True)
        tracker.scene["raw"] = 3
        tracker.end_scene()
        self.assertEqual(tracker.stress, 3)
        self.assertFalse(tracker.is_over)
        self.assertEqual(tracker.over_by, 0)

    def test_stress_is_gained_at_the_end_of_the_scene(self):
        tracker = new_tracker(10, enabled=True)
        tracker.award("kill_human")
        self.assertEqual(tracker.stress, 0, "nothing moves until the scene closes")
        result = tracker.end_scene()
        self.assertEqual(result["applied"], 2)
        self.assertEqual(tracker.stress, 2)

    def test_mere_presence_is_not_participation(self):
        tracker = new_tracker(10, enabled=True)
        self.assertEqual(tracker.award("kill_human", participated=False)["skipped"],
                         "not_a_participant")

    def test_a_dice_modifier_must_be_supplied_by_the_caller(self):
        tracker = new_tracker(10, enabled=True)
        with self.assertRaises(StressError):
            tracker.award("kill_human", modifiers=["first_kill"])
        rolled = tracker.award("kill_human", modifiers=["first_kill"], rolls={"first_kill": 4})
        self.assertEqual(rolled["modifiers"], [{"id": "first_kill", "value": 4}])

    def test_an_unknown_event_is_reported_rather_than_guessed(self):
        result = new_tracker(10, enabled=True).award("witnessed_a_picnic")
        self.assertFalse(result["ok"])

    def test_a_breakdown_suppresses_further_stress(self):
        tracker = new_tracker(3, enabled=True)
        tracker.award("kill_human", modifiers=["several_in_scene", "helpless"])
        tracker.end_scene()
        tracker.resolve_save(False)
        tracker.choose_breakdown("withdrawal")
        self.assertEqual(tracker.award("kill_human")["suppressed"], "breakdown")

    def test_a_bloodthirsty_scar_suppresses_kill_stress(self):
        tracker = new_tracker(10, enabled=True, scars=["bloodthirsty"])
        self.assertEqual(tracker.award("kill_human")["suppressed"], "bloodthirsty")
        self.assertTrue(tracker.award("steal_from_non_enemy")["ok"])


class CheckAndHardeningTests(unittest.TestCase):
    def test_the_penalty_stacks_and_a_success_does_not_heal(self):
        tracker = new_tracker(3, enabled=True)
        tracker.award("kill_human", modifiers=["several_in_scene", "helpless"])
        result = tracker.end_scene()
        self.assertTrue(result["save"]["required"])
        self.assertEqual(result["save"]["penalty"], -2)
        after_first = tracker.resolve_save(True)
        self.assertEqual(after_first["next_penalty"], -4, "a further check is worse, not better")
        self.assertEqual(tracker.stress, 5, "holding the line removes nothing")

    def test_a_failed_check_owes_a_breakdown_and_offers_hardening(self):
        tracker = new_tracker(3, enabled=True)
        tracker.award("kill_human", modifiers=["several_in_scene", "helpless"])
        tracker.end_scene()
        result = tracker.resolve_save(False)
        self.assertTrue(result["awaiting_breakdown"])
        self.assertIn("nightmares", result["scars"])

    def test_hardening_clears_stress_adds_a_scar_and_is_irreversible(self):
        tracker = new_tracker(3, enabled=True)
        tracker.award("kill_human", modifiers=["several_in_scene", "helpless"])
        tracker.end_scene()
        tracker.resolve_save(False)
        result = tracker.harden("nightmares")
        self.assertEqual(result["stress"], 0)
        self.assertEqual(tracker.hardening_count, 1)
        self.assertEqual(result["scene_resistance"], 1)
        self.assertTrue(result["irreversible"])
        self.assertEqual(tracker.choose_breakdown("withdrawal")["ok"], False,
                         "hardening and a breakdown are alternatives, not both")

    def test_a_scar_can_only_be_taken_once(self):
        tracker = new_tracker(3, enabled=True, scars=["nightmares"])
        tracker.award("kill_human", modifiers=["several_in_scene", "helpless"])
        tracker.end_scene()
        tracker.resolve_save(False)
        self.assertFalse(tracker.harden("nightmares")["ok"])


class ResistanceTests(unittest.TestCase):
    def test_hardening_resists_one_point_per_scene_and_stacks(self):
        tracker = new_tracker(10, enabled=True)
        # Two hardenings: resistance 2.
        tracker.hardening_count = 2
        tracker.award("kill_human", modifiers=["several_in_scene", "first_kill"],
                      rolls={"first_kill": 6})
        result = tracker.end_scene()
        self.assertEqual(result["raw"], 9)
        self.assertEqual(result["resisted"], 2)
        self.assertEqual(result["applied"], 7)

    def test_the_dependent_scar_exempts_a_friend_mortal_wound(self):
        # One hardening resists 1 point per scene. A friend's mortal wound is exempt from it, so
        # the whole dose lands; an ordinary wound would be blunted.
        exempt = new_tracker(10, enabled=True, scars=["dependent"])
        exempt.hardening_count = 1
        exempt.award("friend_mortal_wound", modifiers=["then_dies"])
        self.assertEqual(exempt.end_scene()["resisted"], 0)

        blunted = new_tracker(10, enabled=True)
        blunted.hardening_count = 1
        blunted.award("friend_mortal_wound", modifiers=["then_dies"])
        self.assertEqual(blunted.end_scene()["resisted"], 1)


class RecoveryTests(unittest.TestCase):
    def test_recovery_reduces_stress_and_ends_a_breakdown_at_the_ceiling(self):
        tracker = new_tracker(3, enabled=True)
        tracker.award("kill_human", modifiers=["several_in_scene"])
        tracker.end_scene()
        tracker.resolve_save(False)
        tracker.choose_breakdown("withdrawal")
        tracker.recover("safe_day")
        tracker.recover("talk", check_success=True, value=2)
        tracker.recover("major_goal", value=3)
        self.assertEqual(tracker.stress, 0)
        self.assertEqual(tracker.active_breakdown, "")

    def test_a_per_day_limit_is_enforced(self):
        tracker = new_tracker(10, enabled=True, stress=5)
        tracker.recover("talk")
        self.assertFalse(tracker.recover("talk")["ok"], "talk is once a day")
        tracker.new_day()
        self.assertEqual(tracker.recovered_today, {})
        self.assertTrue(tracker.recover("talk")["ok"])

    def test_a_diced_recovery_takes_the_callers_roll(self):
        tracker = new_tracker(10, enabled=True, stress=5)
        with self.assertRaises(StressError):
            tracker.recover("major_goal")
        self.assertEqual(tracker.recover("major_goal", value=4)["recovered"], 4)

    def test_a_scar_can_lock_out_a_recovery(self):
        # The Loner scar cannot use Talk; the contract names the blocker, not the code.
        tracker = new_tracker(10, enabled=True, stress=3, scars=["loner"])
        self.assertFalse(tracker.can_recover("talk"))
        self.assertNotEqual(tracker.recover("talk")["ok"], True)


class AddictionTests(unittest.TestCase):
    def _addicted(self):
        tracker = new_tracker(10, enabled=True, stress=6)
        tracker.enable_addiction("kohina")
        return tracker

    def test_addiction_is_its_own_submodule(self):
        plain = new_tracker(10, enabled=True)
        self.assertFalse(plain.addiction_enabled())
        self.assertFalse(plain.indulge()["ok"])
        self.assertTrue(self._addicted().addiction_enabled())

    def test_indulgence_removes_stress_and_a_missed_day_adds_one(self):
        tracker = self._addicted()
        removed = tracker.indulge(rolls={"daily": 3})
        self.assertEqual(removed["removed"], 3)
        missed = tracker.miss_indulgence()
        self.assertEqual(missed["gained"], 1)
        self.assertTrue(tracker.rest_recovery_blocked(), "a missed dose blocks rest recovery")

    def test_a_monthly_failure_is_system_strain(self):
        tracker = self._addicted()
        self.assertEqual(tracker.monthly_check(False)["gained_strain"], 1)
        self.assertEqual(tracker.monthly_check(True)["success"], True)

    def test_breaking_the_addiction_takes_a_successful_check(self):
        tracker = self._addicted()
        self.assertEqual(tracker.break_addiction("kohina", False)["weeks_clean"], 1)
        self.assertEqual(tracker.break_addiction("kohina", True)["addictions"], [])
        self.assertEqual(tracker.addiction["addictions"], [],
                         "the submodule stays open; the addiction is gone")


class SaveFormatTests(unittest.TestCase):
    def test_the_save_document_matches_the_godot_tracker_shape(self):
        """The GDScript writer and this one must produce the same keys, or a save cannot move."""
        tracker = new_tracker(9, enabled=True)
        data = tracker.to_dict()
        self.assertEqual(data["format"], TRACKER_FORMAT)
        self.assertEqual(data["version"], TRACKER_VERSION)
        expected = {"format", "version", "enabled", "wisdom", "level", "stress",
                    "hardening_count", "scars", "active_breakdown", "checks_made",
                    "awaiting_breakdown", "pending_save", "last_check", "day",
                    "recovered_today", "scene", "addiction", "audit", "seq"}
        self.assertEqual(set(data), expected)
        godot = (ROOT / "mods/noopunk/stress.gd").read_text(encoding="utf-8")
        for key in ("enabled", "wisdom", "level", "stress", "hardening_count", "scars",
                    "active_breakdown", "checks_made", "awaiting_breakdown", "pending_save",
                    "last_check", "day", "recovered_today", "scene", "addiction", "audit", "seq"):
            self.assertIn(f'"{key}"', godot, f"the Godot tracker no longer writes {key}")

    def test_a_tracker_round_trips_through_json(self):
        tracker = new_tracker(4, enabled=True)
        tracker.award("kill_human", modifiers=["several_in_scene"])
        tracker.end_scene()
        tracker.resolve_save(False)
        tracker.harden("loner")
        again = Stress.from_dict(json.loads(json.dumps(tracker.to_dict())))
        self.assertEqual(again.to_dict(), tracker.to_dict())

    def test_a_foreign_save_yields_a_disabled_tracker_rather_than_an_error(self):
        tracker = Stress.from_dict({"schema": "someone-else", "wisdom": 12})
        self.assertFalse(tracker.enabled)
        self.assertEqual(tracker.wisdom, 12)

    def test_the_audit_log_is_capped_and_ordered(self):
        tracker = new_tracker(10, enabled=True)
        for _ in range(250):
            tracker.begin_scene()
        self.assertEqual(len(tracker.audit), 200)
        self.assertLess(tracker.audit[0]["seq"], tracker.audit[-1]["seq"])


if __name__ == "__main__":
    unittest.main()
