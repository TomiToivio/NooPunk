"""The WWN spell corpus and its learning procedure (#1044).

Two jobs: pin the catalogue counts so the "86 spells" claim cannot come back, and pin the learning
arithmetic — one week per spell level less one week per Magic skill level, floor one day — because a
naive subtraction makes learning free (or negative) exactly where the table notices.
"""
from __future__ import annotations

import unittest

from src.rules.wwn_spells import (
    FREE_SPELLS_PER_LEVEL,
    SPELLS,
    Spell,
    SpellError,
    can_learn,
    counts_by_level,
    find,
    free_spells_per_level,
    learning_days,
    rescribe_days,
    spells_of_level,
)


class CatalogueTests(unittest.TestCase):
    def test_the_srd_corpus_is_83_spells(self):
        self.assertEqual(len(SPELLS), 83,
                         "High Magic 52 + Elementalist 15 + Necromancer 16")

    def test_counts_per_tradition_match_the_srd_mirror(self):
        self.assertEqual(counts_by_level("high_magic"), {1: 13, 2: 12, 3: 11, 4: 9, 5: 7})
        self.assertEqual(counts_by_level("elementalist"), {1: 4, 2: 4, 3: 3, 4: 2, 5: 2})
        self.assertEqual(counts_by_level("necromancer"), {1: 4, 2: 4, 3: 4, 4: 2, 5: 2})

    def test_every_spell_has_a_level_and_a_tradition(self):
        for spell in SPELLS:
            self.assertIn(spell.level, (1, 2, 3, 4, 5))
            self.assertIn(spell.tradition, ("high_magic", "elementalist", "necromancer"))

    def test_high_magic_is_the_common_corpus(self):
        self.assertEqual(len(spells_of_level(1, "high_magic")), 13)
        self.assertIn(find("arcane spark").tradition, ("high_magic",))

    def test_lookup_accepts_an_id_or_a_printed_name(self):
        self.assertEqual(find("magic_bomb").name, "Magic Bomb")
        self.assertEqual(find("Magic Bomb").id, "magic_bomb")
        with self.assertRaises(SpellError):
            find("wall of plot convenience")

    def test_an_impossible_entry_is_refused(self):
        with self.assertRaises(SpellError):
            Spell("x", "X", 6, "high_magic")
        with self.assertRaises(SpellError):
            Spell("x", "X", 1, "bardic")


class LearningProcedureTests(unittest.TestCase):
    def test_one_week_per_spell_level_less_one_week_per_magic_skill(self):
        self.assertEqual(learning_days(3, 1), 14)   # 3 - 1 weeks
        self.assertEqual(learning_days(5, 2), 21)   # 5 - 2 weeks
        self.assertEqual(learning_days(1, 0), 7)

    def test_the_floor_is_one_day(self):
        self.assertEqual(learning_days(1, 1), 1)    # would be 0 days
        self.assertEqual(learning_days(1, 4), 1)    # would be negative
        self.assertEqual(learning_days(2, 3), 1)

    def test_rescribing_costs_the_same_as_learning(self):
        for level in range(1, 6):
            for skill in range(5):
                self.assertEqual(rescribe_days(level, skill), learning_days(level, skill))

    def test_impossible_inputs_are_refused(self):
        with self.assertRaises(SpellError):
            learning_days(6, 1)
        with self.assertRaises(SpellError):
            learning_days(1, -1)

    def test_a_caster_can_only_learn_what_they_can_cast(self):
        bomb = find("magic_bomb")                    # level 3
        self.assertFalse(can_learn(bomb, 2))
        self.assertTrue(can_learn(bomb, 3))
        with self.assertRaises(SpellError):
            can_learn(bomb, 0)

    def test_free_spells_per_level(self):
        self.assertEqual(free_spells_per_level("high_mage"), 2)
        self.assertEqual(free_spells_per_level("elementalist"), 1)
        self.assertEqual(free_spells_per_level("necromancer"), 1)
        self.assertEqual(set(FREE_SPELLS_PER_LEVEL), {
            "high_mage", "partial_high_mage", "elementalist", "necromancer"})
        with self.assertRaises(SpellError):
            free_spells_per_level("bard")


if __name__ == "__main__":
    unittest.main()
