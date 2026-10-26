"""The CWN equipment catalogue, and the scenario's numbers against it.

The interesting test here is the last one: the first case's sheet and NPC stat lines carry decomposed
damage numbers (count/sides/bonus/shock/trauma), which is exactly how a typo hides. The catalogue is the
source row, so every hand-typed number in the scenario must equal the profile derived from it.
"""
import json
import pathlib
import unittest

from src.rules.cwn_equipment import (
    EquipmentError,
    armor_piece,
    damage_profile,
    find_weapon,
    load_equipment,
    parse_damage,
    weapon,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "godot/scenarios/lakkahaltia/scenario.json"
LEVEL = ROOT / "godot/scenarios/lakkahaltia/level_hospital.json"


class CatalogueTests(unittest.TestCase):
    def test_the_srd_tables_are_all_there(self):
        catalogue = load_equipment()
        self.assertGreaterEqual(len(catalogue["weapons"]), 35)
        self.assertGreaterEqual(len(catalogue["armor"]), 15)
        kinds = {row["kind"] for row in catalogue["weapons"].values()}
        self.assertEqual(kinds, {"firearm", "heavy", "melee"})

    def test_every_row_points_at_its_srd_page(self):
        catalogue = load_equipment()
        for row in list(catalogue["weapons"].values()) + list(catalogue["armor"].values()):
            with self.subTest(entry=row["id"]):
                self.assertTrue(str(row["srd"]).startswith("gear-vehicles-cyberware/"))
                self.assertTrue(str(row["name"]).strip())

    def test_a_firearm_keeps_its_srd_numbers(self):
        pistol = weapon("light_pistol")
        self.assertEqual(pistol["damage"], "1d6")
        self.assertEqual(pistol["range"], "10/80")
        self.assertEqual(pistol["cost"], 200)
        self.assertEqual(pistol["magazine"], 15)
        self.assertEqual(pistol["trauma_die"], "1d8")
        self.assertEqual(pistol["trauma_rating"], "x2")
        self.assertIsNone(pistol["shock"])

    def test_a_melee_weapon_keeps_its_shock(self):
        knife = weapon("knife")
        self.assertEqual(knife["shock"], {"damage": 1, "max_ac": 15})
        self.assertIsNone(knife["magazine"])

    def test_armour_keeps_both_armour_classes_and_soak(self):
        clothing = armor_piece("reinforced_clothing")
        self.assertEqual((clothing["ac_ranged"], clothing["ac_melee"]), (13, 10))
        self.assertEqual(clothing["damage_soak"], 2)
        self.assertTrue(clothing["subtle"])

    def test_unknown_ids_are_refused(self):
        with self.assertRaises(EquipmentError):
            weapon("plasma_katana")
        with self.assertRaises(EquipmentError):
            armor_piece("plot_armour")
        with self.assertRaises(EquipmentError):
            find_weapon("Vibro-blade of destiny")


class ParsingTests(unittest.TestCase):
    def test_damage_expressions_including_srd_markers(self):
        self.assertEqual(parse_damage("1d10+2"), (1, 10, 2))
        self.assertEqual(parse_damage("3d6#!"), (3, 6, 0))
        self.assertEqual(parse_damage("1d2^"), (1, 2, 0))
        self.assertEqual(parse_damage("1d8-1"), (1, 8, -1))
        with self.assertRaises(EquipmentError):
            parse_damage("Gren.")

    def test_the_profile_is_the_shape_the_kernel_takes(self):
        self.assertEqual(damage_profile("light_pistol"), {
            "id": "light_pistol", "label": "Light Pistol", "damage_count": 1, "damage_sides": 6,
            "damage_bonus": 0, "attribute": "DEX", "shock": 0, "shock_ac": -1,
            "trauma_die": 8, "trauma_rating": 2,
        })
        knife = damage_profile("knife")
        self.assertEqual((knife["shock"], knife["shock_ac"], knife["trauma_die"]), (1, 15, 6))

    def test_names_resolve_case_insensitively(self):
        self.assertEqual(find_weapon("Light pistol")["id"], "light_pistol")
        self.assertEqual(find_weapon("unarmed attack")["id"], "unarmed_attack")


class ScenarioContractTests(unittest.TestCase):
    """Every weapon a scenario names must exist, and its numbers must match the catalogue row."""

    def _check(self, entry: dict, where: str, rows: list[str]) -> None:
        # A sheet entry names an id; an NPC stat line may only carry the printed name ("Unarmed").
        weapon_id = entry.get("id") or find_weapon(str(entry.get("label", "")))["id"]
        expected = damage_profile(weapon_id)
        fields = ("damage_count", "damage_sides", "damage_bonus", "attribute",
                  "shock", "shock_ac", "trauma_die", "trauma_rating")
        fields = ("label", *fields) if entry.get("id") else fields
        for field in fields:
            actual, wanted = entry.get(field), expected[field]
            if field == "label" and isinstance(actual, str):
                # Display text only: a stat line may print the SRD's "Unarmed Attack" as "Unarmed".
                actual = actual.casefold().removesuffix(" attack")
                wanted = str(wanted).casefold().removesuffix(" attack")
            if field in entry and actual != wanted:
                rows.append(f"{where}: {weapon_id}.{field} is {entry[field]!r}, catalogue says {expected[field]!r}")

    def test_the_sheet_matches_the_catalogue(self):
        sheet = json.loads(SCENARIO.read_text(encoding="utf-8"))["player_sheet"]
        problems: list[str] = []
        for entry in sheet.get("weapons", []):
            self._check(entry, "player_sheet", problems)
        self.assertEqual(problems, [])

    def test_every_npc_stat_line_matches_the_catalogue(self):
        level = json.loads(LEVEL.read_text(encoding="utf-8"))
        problems: list[str] = []
        for npc in level.get("npcs", []):
            stat_line = npc.get("stat_line", {})
            entry = stat_line.get("weapon")
            if entry:
                self._check(entry, f"npc {npc.get('id')}", problems)
        self.assertEqual(problems, [])
        self.assertTrue(level.get("npcs"), "the level must have NPCs to check")


if __name__ == "__main__":
    unittest.main()
