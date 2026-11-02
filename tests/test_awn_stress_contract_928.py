"""Reconciliation of the AWN Stress overlay (#928) against the book, and the rule that there is ONE
contract (#1045).

Background: two sessions produced stress material in different places — `data/rules/awn_stress.json`
plus `mods/noopunk/stress.gd` (#928) on one side, and a note in the AWN inventory on the other. The
inventory's first backlog item was "reconcile stress with #928 before any second tracker exists".
This module is that reconciliation made executable: the single JSON contract is the source of the
numbers, every number below was read off *Ashes Without Number* printed pp. 56–58, and both the
Godot overlay and any future Python tracker must read this file rather than restate it.

AWN has no verified open licence in this repository, so the contract carries the procedure in
NoöPunk wording and no book text. Numbers are facts about a mechanic; sentences are not copied.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "rules" / "awn_stress.json"
GODOT_MOD = ROOT / "mods" / "noopunk" / "stress.gd"


def contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def _options(section: str) -> dict[str, dict]:
    return {row["id"]: row for row in contract()[section]["options"]}


class ContractShapeTests(unittest.TestCase):
    def test_the_contract_is_a_single_optional_overlay_on_cwn(self):
        data = contract()
        self.assertEqual(data["format"], "noopunk.rules.awn_stress")
        self.assertTrue(data["module"]["optional"])
        self.assertFalse(data["module"]["default_enabled"],
                         "a table that does not want moral drift must be able to leave it off")
        self.assertEqual(data["module"]["layer"], "character")

    def test_the_core_keeps_the_dice(self):
        data = contract()
        self.assertEqual(data["threshold"]["save_owner"],
                         "CWN core - the caller resolves the save and passes the outcome in",
                         "the overlay never rolls: it consumes a CWN Mental save result")
        self.assertEqual(data["threshold"]["save"], "mental")
        self.assertEqual(data["source"]["licence"].startswith("no verified open licence"), True)
        self.assertTrue((ROOT / data["source"]["rights_record"]).exists(),
                        "the rights record the contract points at must exist")

    def test_only_one_contract_exists(self):
        duplicates = [p.relative_to(ROOT).as_posix()
                      for p in (ROOT / "data").rglob("*stress*.json")
                      if p != CONTRACT]
        self.assertEqual(duplicates, [], "a second stress contract is the drift this test prevents")

    def test_every_implementation_reads_that_contract(self):
        godot = GODOT_MOD.read_text(encoding="utf-8")
        self.assertIn('"res://data/rules/awn_stress.json"', godot,
                      "the Godot overlay must load the shared contract, not restate its numbers")
        self.assertIn("CONTRACT_PATH", godot)


class ThresholdTests(unittest.TestCase):
    """Printed p. 57: Stress above Wisdom, Mental save at -2, a further stacking -2 per check."""

    def test_the_ceiling_is_wisdom(self):
        threshold = contract()["threshold"]
        self.assertEqual(threshold["attribute"], "WIS")
        self.assertEqual(threshold["crosses_when"], "above")
        self.assertTrue(threshold["equality_is_safe"])

    def test_the_penalty_starts_at_minus_two_and_stacks(self):
        threshold = contract()["threshold"]
        self.assertEqual(threshold["first_penalty"], -2)
        self.assertEqual(threshold["penalty_step"], -2)
        self.assertTrue(threshold["penalty_stacks_while_over"])
        self.assertIsNone(threshold["penalty_cap"])
        self.assertEqual(threshold["penalty_resets_when"], "stress_at_or_below_wisdom")

    def test_a_successful_check_does_not_heal(self):
        self.assertTrue(contract()["threshold"]["success_does_not_reduce_stress"],
                        "holding the line is not recovery; only the recovery table removes Stress")

    def test_stress_is_gained_at_the_end_of_the_scene_by_participants(self):
        gaining = contract()["gaining"]
        self.assertEqual(gaining["timing"], "end_of_scene")
        self.assertEqual(gaining["applies_to"], "active_participants_only")
        self.assertFalse(gaining["presence_is_participation"])


class BreakdownTests(unittest.TestCase):
    """Printed p. 57: the five Breakdowns and exactly what each forbids."""

    def test_the_five_printed_breakdowns_exist(self):
        self.assertEqual(sorted(_options("breakdowns")),
                         ["confusion", "cowardice", "deathwish", "indulgence", "withdrawal"])

    def test_each_breakdown_carries_its_printed_effect(self):
        rows = _options("breakdowns")
        self.assertEqual(rows["deathwish"]["effects"],
                         {"cannot_willingly_retreat": True, "hp_per_level": -2,
                          "hp_per_level_minimum": 1})
        self.assertEqual(rows["withdrawal"]["effects"],
                         {"fights_only_in_self_defence": True, "cannot_use_skill_checks": True,
                          "can_handle_simple_tasks": True})
        self.assertEqual(rows["indulgence"]["effects"]["skill_check_penalty"], -2)
        self.assertTrue(rows["cowardice"]["effects"]["cannot_fight"])
        self.assertTrue(rows["confusion"]["effects"]["cannot_act_on_own_initiative"])

    def test_a_breakdown_stops_further_stress_and_ends_at_the_ceiling(self):
        rows = contract()["breakdowns"]
        self.assertTrue(rows["blocks_further_stress"],
                        "while a Breakdown is in effect the PC gains no more Stress")
        self.assertTrue(rows["player_picks"])
        self.assertEqual(rows["ends_when"], "stress_at_or_below_wisdom")


class HardeningAndScarTests(unittest.TestCase):
    """Printed pp. 57–58: Hardening clears Stress, resists one point per scene, and is permanent."""

    def test_hardening_clears_stress_and_resists_one_point_per_scene(self):
        hardening = contract()["hardening"]
        self.assertEqual(hardening["clears_stress_to"], 0)
        self.assertEqual(hardening["scene_resistance"], 1)
        self.assertEqual(hardening["resistance_scope"], "per_scene")
        self.assertTrue(hardening["resistance_stacks"])
        self.assertTrue(hardening["irreversible"])
        self.assertTrue(hardening["grants_psychic_scar"])

    def test_the_five_printed_scars_carry_their_printed_numbers(self):
        rows = _options("scars")
        self.assertEqual(rows["nightmares"]["effects"],
                         {"con_modifier": -1, "con_modifier_floor": -2, "save_penalty": -2})
        self.assertEqual(rows["delusional"]["effects"]["wis_penalty"], -3)
        self.assertEqual(rows["delusional"]["effects"]["wis_floor"], 3)
        self.assertTrue(rows["bloodthirsty"]["effects"]["no_stress_from_killing"])
        self.assertEqual(rows["bloodthirsty"]["effects"]["recovery_fails_chance"], 0.5)
        self.assertEqual(rows["penitent"]["effects"]["taboo_breach"]["sets_stress_to"],
                         "wisdom_plus_2")
        self.assertEqual(rows["dependent"]["effects"]["extra_stress_on_friend_death"], "1d6")
        self.assertEqual(rows["dependent"]["effects"]["cha_penalty"], -3)

    def test_a_scar_is_taken_once_and_never_traded(self):
        self.assertTrue(contract()["scars"]["one_each"])


class AddictionTests(unittest.TestCase):
    """Printed p. 58: an hour a day, one dose, and a missed day is its own stress."""

    def test_an_addiction_costs_an_hour_and_a_dose_each_day(self):
        daily = contract()["addiction"]["daily"]
        self.assertEqual(daily["hours_indulging"], 1)
        self.assertEqual(daily["doses"], 1)
        self.assertTrue(daily["one_hour_per_addiction"])

    def test_a_missed_day_is_privation_and_cannot_be_hardened_away(self):
        missed = contract()["addiction"]["missed_day"]
        self.assertEqual(missed["stress"], 1)
        self.assertTrue(missed["counts_as_privation"])
        self.assertFalse(missed["negated_by_hardening"])

    def test_addiction_is_off_unless_the_table_opts_in(self):
        self.assertFalse(contract()["addiction"]["enabled_by_default"])


if __name__ == "__main__":
    unittest.main()
