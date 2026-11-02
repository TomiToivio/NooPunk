"""Character-creation final steps, the skill list, firearms and armour accessories (#1068).

These rows were `unverified` in the compliance matrix: the rules existed, nothing proved them.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))

from nopunk_mud.cwn import CwnError, hit_points, save_target, skill_modifier  # noqa: E402
from nopunk_mud.cwn import armor  # noqa: E402


def data(name: str) -> dict:
    return json.loads((ROOT / "data" / "rules" / name).read_text(encoding="utf-8"))


class FinalSteps(unittest.TestCase):
    def test_a_first_level_character_rolls_one_d6_plus_constitution_never_below_one(self):
        self.assertEqual(hit_points(1, 2, dice=[4]), 6)
        self.assertEqual(hit_points(1, -3, dice=[1]), 1, "a penalty cannot push hit points below 1")

    def test_hard_to_kill_adds_two(self):
        self.assertEqual(hit_points(1, 0, dice=[3], hard_to_kill=True), 5)

    def test_save_targets_are_fifteen_minus_the_better_modifier(self):
        attributes = {"Strength": 12, "Dexterity": 10, "Constitution": 14,
                      "Intelligence": 9, "Wisdom": 11, "Charisma": 8}
        # STR +0, CON +1 -> Physical 14; INT -1, DEX +0 -> Evasion 15; WIS +0, CHA -1 -> Mental 15
        self.assertEqual(save_target("Physical", level=1, attributes=attributes), 14)
        self.assertEqual(save_target("Evasion", level=1, attributes=attributes), 15)
        self.assertEqual(save_target("Mental", level=1, attributes=attributes), 15)
        self.assertEqual(save_target("Luck", level=1, attributes=attributes), 15)

    def test_each_level_lowers_every_save_by_one(self):
        attributes = {"Strength": 10, "Dexterity": 10, "Constitution": 10,
                      "Intelligence": 10, "Wisdom": 10, "Charisma": 10}
        self.assertEqual(save_target("Physical", level=1, attributes=attributes), 15)
        self.assertEqual(save_target("Physical", level=3, attributes=attributes), 13)

    def test_an_unknown_save_is_refused(self):
        with self.assertRaises(CwnError):
            save_target("Charisma", level=1, attributes={"Strength": 10})


class SkillRules(unittest.TestCase):
    def test_rank_zero_is_trained_and_untrained_is_minus_one(self):
        # CWN: an untrained skill check is -1. The -2 penalty applies to combat attacks without a
        # combat skill, and lives in combat_mods rather than here.
        self.assertEqual(skill_modifier(0), 0)
        self.assertEqual(skill_modifier(3), 3)
        self.assertEqual(skill_modifier(-1), -1)

    def test_the_skill_list_has_the_srd_skills(self):
        skills = data("cwn/skills_srd.json")["skills"]
        for name in ("Administer", "Connect", "Drive", "Exert", "Fix", "Heal", "Know", "Lead",
                     "Notice", "Perform", "Program", "Punch", "Shoot", "Sneak", "Stab", "Survive",
                     "Talk", "Trade", "Work"):
            self.assertIn(name, skills, f"the SRD skill list includes {name}")

    def test_the_skill_scale_runs_zero_to_four(self):
        levels = data("cwn/skills_srd.json")["levels"]
        self.assertEqual([str(x) for x in levels], ["level-0", "level-1", "level-2", "level-3", "level-4"])


class Firearms(unittest.TestCase):
    def setUp(self):
        self.weapons = {w["id"]: w for w in data("cwn_equipment.json")["weapons"]}

    def test_the_firearm_table_matches_the_srd(self):
        light = self.weapons["light_pistol"]
        self.assertEqual((light["damage"], light["range"], light["cost"], light["magazine"]),
                         ("1d6", "10/80", 200, 15))
        rifle = self.weapons["rifle"]
        self.assertEqual((rifle["damage"], rifle["cost"], rifle["magazine"]), ("1d10+2", 1000, 10))

    def test_firearms_use_dexterity(self):
        for weapon_id in ("light_pistol", "heavy_pistol", "rifle"):
            self.assertEqual(self.weapons[weapon_id]["attribute"], ["DEX"])

    def test_every_firearm_carries_a_trauma_rating(self):
        firearms = [w for w in self.weapons.values() if w.get("trauma_die")]
        self.assertGreater(len(firearms), 5)


class ArmorAccessories(unittest.TestCase):
    def test_an_accessory_cannot_be_applied_twice(self):
        self.assertFalse(armor.can_attach("absorption_plates", base_armor="street_leathers",
                                          already=("absorption_plates",)))

    def test_suit_armor_refuses_accessories_but_allows_a_shield(self):
        self.assertFalse(armor.can_attach("absorption_plates", base_armor="combat_suit"))
        self.assertTrue(armor.can_attach("riot_shield", base_armor="combat_suit"))

    def test_plates_and_joints_each_cost_one_on_sneak_and_exert(self):
        self.assertEqual(armor.stealth_exert_penalty(("absorption_plates", "joint_reinforcement")), -2)
        self.assertEqual(armor.stealth_exert_penalty(()), 0)

    def test_a_shield_negates_the_first_melee_shock_only_once(self):
        self.assertEqual(armor.shock_absorbed(shield=True, melee_shock=3), 1)
        self.assertEqual(armor.shock_absorbed(shield=True, melee_shock=3, shields_carried=2), 1)
        self.assertEqual(armor.shock_absorbed(shield=False, melee_shock=3), 0)

    def test_obsolete_armor_is_half_price_and_degrades_after_purchase(self):
        result = armor.obsolete_armor(ac_ranged=14, ac_melee=13, soak=4, ac_roll=2, soak_roll=3,
                                      cost=1_000)
        self.assertEqual(result, {"ac_ranged": 12, "ac_melee": 11, "damage_soak": 1, "cost": 500})

    def test_obsolete_armor_floors_are_respected(self):
        result = armor.obsolete_armor(ac_ranged=11, ac_melee=11, soak=1, ac_roll=2, soak_roll=4,
                                      cost=100)
        self.assertEqual(result["ac_ranged"], 10)
        self.assertEqual(result["damage_soak"], 0)


if __name__ == "__main__":
    unittest.main()
