"""WWN spell effects, batch 1 (#1085): the resolver computes formulas, never dice.

The invariants worth pinning: damage scales with caster level, a made save halves only when the row
says half, the GM-dependent spells are marked `manual` instead of pretending to be mechanical, and an
untranscribed spell is refused rather than resolved to a plausible-looking nothing.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.rules.wwn_spell_effects import (
    EFFECTS,
    EffectError,
    effect,
    load_effects,
    resolve,
    transcribed,
    untranscribed,
)
from src.rules.wwn_spells import SPELLS, spells_of_level

ROOT = Path(__file__).resolve().parents[1]


class BatchCoverageTests(unittest.TestCase):
    def test_the_batch_is_the_thirteen_high_magic_level_one_spells(self):
        expected = {spell.id for spell in spells_of_level(1, "high_magic")}
        self.assertEqual(set(transcribed()), expected)
        self.assertEqual(len(EFFECTS), 13)

    def test_every_row_matches_a_catalogued_spell(self):
        catalogued = {spell.id for spell in SPELLS}
        self.assertEqual(set(EFFECTS) - catalogued, set())

    def test_the_source_block_records_what_is_still_missing(self):
        data = json.loads((ROOT / "data/rules/wwn_spell_effects.json").read_text(encoding="utf-8"))
        self.assertEqual(data["source"]["transcribed"], 13)
        self.assertEqual(data["source"]["remaining"],
                         {"high_magic": 39, "elementalist": 15, "necromancer": 16})

    def test_untranscribed_names_the_batch_boundary(self):
        everything = [spell.id for spell in SPELLS]
        missing = untranscribed(everything)
        self.assertEqual(len(missing), 83 - 13)
        self.assertIn("gate", missing)          # level-5 High Magic
        self.assertNotIn("arcane_spark", missing)


class RefusalTests(unittest.TestCase):
    def test_an_untranscribed_spell_is_refused_by_name(self):
        with self.assertRaises(EffectError) as caught:
            effect("gate")
        self.assertIn("gate", str(caught.exception))
        self.assertIn("#1085", str(caught.exception))

    def test_an_unknown_spell_is_refused(self):
        with self.assertRaises(EffectError):
            effect("wall_of_plot_convenience")

    def test_a_broken_catalogue_is_refused(self):
        bad = ROOT / "tests" / "_bad_effects.json"
        bad.write_text(json.dumps({"format": "nope", "effects": []}), encoding="utf-8")
        try:
            with self.assertRaises(EffectError):
                load_effects(bad)
        finally:
            bad.unlink()


class DamageFormulaTests(unittest.TestCase):
    def test_arcane_spark_scales_one_die_per_caster_level(self):
        level_three = resolve("arcane_spark", caster_level=3, roll_total=11)
        self.assertEqual(level_three["damage"]["dice"], 3)
        self.assertEqual(level_three["damage"]["applied_total"], 11)
        self.assertTrue(level_three["damage"]["per"] == "caster_level")

    def test_a_made_save_halves_when_the_row_says_half(self):
        result = resolve("arcane_spark", caster_level=2, roll_total=9, save_made=True)
        self.assertEqual(result["damage"]["applied_total"], 4, "floor division: 9 // 2")
        missed = resolve("arcane_spark", caster_level=2, roll_total=9, save_made=False)
        self.assertEqual(missed["damage"]["applied_total"], 9)

    def test_destroy_earth_only_damages_plant_creatures(self):
        result = resolve("destroy_earth", caster_level=4, roll_total=20)
        self.assertEqual(result["damage"]["dice"], 4)
        self.assertEqual(result["damage"]["applies_to"], "plant-based monsters")
        self.assertEqual(result["save"]["category"], "physical")

    def test_an_unrolled_damage_spell_says_what_it_needs(self):
        result = resolve("arcane_spark", caster_level=1)
        self.assertIn("damage roll", result["needs"])
        self.assertIsNone(result["damage"]["applied_total"])


class StructuredEffectTests(unittest.TestCase):
    def test_a_control_spell_reports_its_save_and_penalty(self):
        result = resolve("dominate_person", caster_level=5)
        self.assertEqual(result["kind"], "control")
        self.assertEqual(result["save"]["category"], "mental")
        self.assertIn("Magic skill", result["save"]["penalty"])
        self.assertTrue(result["manual"])

    def test_a_buff_reports_its_cost(self):
        speed = resolve("speed", caster_level=2)
        self.assertEqual(speed["kind"], "buff")
        self.assertEqual(speed["cost"]["system_strain"], 1)
        self.assertFalse(speed["manual"])

    def test_incapacitation_has_no_damage_formula(self):
        result = resolve("the_wind_of_final_repose", caster_level=3)
        self.assertEqual(result["kind"], "incapacitate")
        self.assertNotIn("damage", result)
        self.assertIn("4 or fewer hit dice", result["note"])

    def test_manual_effects_say_why_they_are_manual(self):
        for identifier in ("create_illusion", "control_animal", "detect_thoughts"):
            row = effect(identifier)
            self.assertTrue(row["manual"], identifier)
            self.assertTrue(row["note"], identifier)

    def test_caster_level_zero_is_refused(self):
        with self.assertRaises(EffectError):
            resolve("arcane_spark", caster_level=0)


if __name__ == "__main__":
    unittest.main()
