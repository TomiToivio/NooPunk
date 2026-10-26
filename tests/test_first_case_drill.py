"""The first case must exercise every ported Without Number procedure.

This is the guard behind the sentence "we need all CWN rules and psionics from SWN
in the first scenario". It reads the drill script, runs it twice, and asserts:

* no required subsystem is missing (the claim is falsifiable);
* every tag a beat claims is a real subsystem word, so a typo cannot fake coverage;
* every beat id has a handler and every handler has a beat (no dead coverage);
* two runs on one seed agree exactly, and a different seed really does move dice;
* the sheet's skills are CWN skills plus SWN psionic disciplines — a rename that
  would silently resolve every check as untrained fails here.

Code-only, per AGENTS.md and #271.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules import first_case_drill as drill

SCRIPT = drill.load_drill()
REQUIRED = frozenset(SCRIPT["required_subsystems"])
DISCIPLINES = {"Biopsionics", "Metapsionics", "Precognition", "Telepathy",
               "Telekinesis", "Teleportation"}


def canonical_skills() -> set[str]:
    raw = json.loads((ROOT / "data" / "rules" / "without_number.json").read_text(encoding="utf-8"))
    return set(raw["skills"]["names"])


class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.drill_run = drill.run_drill()

    def test_every_required_subsystem_appears(self):
        self.assertEqual(self.drill_run.coverage_gaps(REQUIRED), frozenset())

    def test_every_claimed_tag_is_a_required_subsystem(self):
        for beat in self.drill_run.beats:
            for tag in beat.tags:
                self.assertIn(tag, REQUIRED, f"{beat.id} claims an unknown subsystem {tag!r}")

    def test_every_beat_id_has_a_handler(self):
        for beat in SCRIPT["beats"]:
            self.assertIn(beat["id"], drill.HANDLERS, beat["id"])

    def test_every_handler_is_used_by_a_beat(self):
        used = {beat["id"] for beat in SCRIPT["beats"]}
        self.assertEqual(set(drill.HANDLERS) - used, set())

    def test_a_beat_with_no_handler_is_refused(self):
        script = json.loads(json.dumps(SCRIPT))
        script["beats"].append({"id": "not_a_real_beat", "tags": ["combat"], "params": {}})
        import tempfile
        path = Path(tempfile.mkdtemp()) / "drill.json"
        path.write_text(json.dumps(script), encoding="utf-8")
        with self.assertRaises(drill.DrillError):
            drill.run_drill(path)


class DeterminismTests(unittest.TestCase):
    def test_one_seed_reproduces_the_whole_log(self):
        self.assertEqual(drill.run_drill(seed=7).log(), drill.run_drill(seed=7).log())

    def test_a_different_seed_moves_the_dice(self):
        self.assertNotEqual(drill.run_drill(seed=7).log(), drill.run_drill(seed=8).log())

    def test_the_dice_bearing_beats_are_actually_dice_bearing(self):
        by_id = {beat.id: beat.outcome for beat in drill.run_drill().beats}
        self.assertIn("dice", by_id["briefing_notice"])
        self.assertIn("attack_total", by_id["stair_ambush"])


class RuleBehaviourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.beats = {beat.id: beat.outcome for beat in drill.run_drill().beats}

    def test_the_ward_terminal_is_hacked_at_minus_three_connection_penalty(self):
        # Wireless (-2) and a VR crown (-1) are flat, not circumstances.
        self.assertEqual(self.beats["ward_terminal"]["connection_penalty"], -3)

    def test_the_access_pool_is_a_pool_not_a_bonus(self):
        # INT 14 (+1) and Program-1 give an Access pool of 2.
        self.assertEqual(self.beats["ward_terminal"]["access_pool"], 2)

    def test_a_committed_technique_returns_when_the_scene_ends(self):
        psi = self.beats["mirror_effort"]
        self.assertTrue(psi["gated"])
        self.assertTrue(psi["committed"])
        self.assertEqual(psi["duration"], "scene")
        self.assertLess(psi["free_after"], psi["capacity"])
        self.assertEqual(psi["free_next_scene"], psi["capacity"])

    def test_the_hull_carries_its_armour_after_the_trauma_multiplier(self):
        self.assertEqual(self.beats["crash_landing"]["damage_after_armor"], 31 - 6)

    def test_a_crash_that_breaks_one_save_is_half_maximum_hit_points(self):
        crash = self.beats["crash_landing"]
        self.assertFalse(crash["unscathed"])
        self.assertEqual(crash["damage_fraction"], 0.5)

    def test_the_modified_longcoat_soaks_ten_per_fight(self):
        self.assertEqual(self.beats["gunfire_with_mods"]["armor_soak"], 10)
        self.assertGreaterEqual(self.beats["gunfire_with_mods"]["soak_absorbed"], 0)

    def test_zero_hit_points_produced_a_real_injury_row(self):
        zero = self.beats["zero_hp"]
        self.assertTrue(zero["mortally_wounded"])
        self.assertTrue(zero["risked_major_injury"])
        self.assertIsNotNone(zero["injury"])
        self.assertIn("roll", zero["injury"])

    def test_stabilising_cost_rises_with_each_round_elapsed(self):
        self.assertEqual(self.beats["stabilise"]["difficulty"], 10)

    def test_the_kit_is_overloaded_at_this_strength(self):
        # STR 8: 8 stowed and 4 readied is past both caps but inside the first push.
        self.assertEqual(self.beats["kit_load"]["tier"], "heavy")
        self.assertLess(self.beats["kit_load"]["move_metres"], 10)

    def test_the_drone_out_past_a_kilometre_is_hijackable_not_lost(self):
        self.assertEqual(self.beats["drone_recon"]["range_status"], "safe")
        self.assertEqual(self.beats["drone_recon"]["control_penalty"], 0)

    def test_a_night_without_shelter_costs_no_strain_but_blocks_recovery(self):
        watch = self.beats["rain_watch"]
        self.assertEqual(watch["strain_gained"], 0)
        self.assertTrue(watch["recovery_blocked"])
        self.assertFalse(watch["needs_physical_save"])

    def test_the_referral_project_is_not_free_and_not_modelled_for_cash(self):
        project = self.beats["referral_project"]
        self.assertGreater(project["difficulty"], 1)
        self.assertEqual(project["remaining"], project["difficulty"] - 4)
        self.assertFalse(project["money_ladder_modelled"])

    def test_advancement_reads_the_cwn_track(self):
        advance = self.beats["advancement"]
        self.assertGreaterEqual(advance["level"], 1)
        self.assertGreater(advance["next_level_xp"], 0)

    def test_modding_reports_the_cap_and_the_maintenance_score(self):
        modding = self.beats["modding_kit"]
        self.assertLessEqual(modding["weapon_hit_bonus"], 3)
        self.assertEqual(modding["weapon_magazine_multiplier"], 2)
        self.assertGreater(modding["maintenance_score"], 0)


class SheetContractTests(unittest.TestCase):
    def test_every_skill_on_the_sheet_is_a_cwn_skill_or_a_psionic_discipline(self):
        known = canonical_skills() | DISCIPLINES
        for skill in SCRIPT["sheet"]["skills"]:
            self.assertIn(skill, known, skill)

    def test_the_sheet_can_actually_make_the_checks_the_drill_asks_for(self):
        # A skill the sheet lacks would resolve as untrained (-1) and nothing else would warn.
        sheet = SCRIPT["sheet"]
        for beat in SCRIPT["beats"]:
            skill = (beat.get("params") or {}).get("skill")
            if skill:
                self.assertIn(skill, sheet["skills"], beat["id"])

    def test_the_sheet_has_six_attributes_in_the_cwn_range(self):
        attributes = SCRIPT["sheet"]["attributes"]
        self.assertEqual(set(attributes), {"STR", "DEX", "CON", "INT", "WIS", "CHA"})
        for value in attributes.values():
            self.assertTrue(3 <= value <= 18)

    def test_the_case_file_the_drill_names_exists(self):
        self.assertTrue((ROOT / SCRIPT["case"]).is_file())

    def test_the_psionic_block_declares_a_real_package_and_discipline(self):
        block = SCRIPT["sheet"]["psionics"]
        self.assertTrue(set(block["packages"]) & {"swn_psychic", "swn_partial_psychic"})
        for discipline in block["disciplines"]:
            self.assertIn(discipline, DISCIPLINES)


if __name__ == "__main__":
    unittest.main()
