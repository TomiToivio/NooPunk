"""Tests for the Edge and Focus selection contract."""
import unittest

from src.rules.cwn_character import ATTRIBUTES
from src.rules.cwn_edges_foci import (
    Edge,
    Focus,
    TalentRulesError,
    TalentSheet,
    attribute_modifier_total,
    can_raise_attributes_with_skill_points,
    focus_slots,
    pick_edge,
    pick_focus,
    underdog_eligible,
)

AVERAGE = {a: 10 for a in ATTRIBUTES}          # every modifier 0
WEAK = {a: 6 for a in ATTRIBUTES}              # every modifier -1
MIXED = {"Strength": 10, "Dexterity": 10, "Constitution": 10,
         "Intelligence": 10, "Wisdom": 4, "Charisma": 10}


class UnderdogTest(unittest.TestCase):
    def test_an_average_character_is_not_an_underdog(self):
        self.assertFalse(underdog_eligible(AVERAGE))

    def test_a_character_at_minus_one_qualifies(self):
        self.assertTrue(underdog_eligible(MIXED))   # 0+0+0+0-1+0 = -1

    def test_the_total_is_the_thing_that_counts_not_any_single_score(self):
        self.assertEqual(attribute_modifier_total(MIXED), -1)

    def test_the_underdog_bonus_costs_later_attribute_raises(self):
        self.assertFalse(can_raise_attributes_with_skill_points(underdog_used=True))
        self.assertTrue(can_raise_attributes_with_skill_points(underdog_used=False))

    def test_the_bonus_gives_an_extra_edge_slot(self):
        self.assertEqual(TalentSheet().edge_slots(underdog_eligible=True), 3)


class EdgeTest(unittest.TestCase):
    def test_a_starting_character_has_two_edges(self):
        sheet = TalentSheet()
        pick_edge(sheet, Edge("a"))
        pick_edge(sheet, Edge("b"))
        self.assertEqual(len(sheet.edges), 2)
        with self.assertRaises(TalentRulesError):
            pick_edge(sheet, Edge("c"))

    def test_a_third_edge_is_available_at_fifth_level(self):
        sheet = TalentSheet(level=5)
        for name in ("a", "b", "c"):
            pick_edge(sheet, Edge(name))
        self.assertEqual(len(sheet.edges), 3)

    def test_an_edge_cannot_be_taken_twice(self):
        sheet = TalentSheet()
        pick_edge(sheet, Edge("alert"))
        with self.assertRaises(TalentRulesError):
            pick_edge(sheet, Edge("alert"))

    def test_a_repeatable_edge_may_be_taken_twice(self):
        sheet = TalentSheet()
        pick_edge(sheet, Edge("wealth", repeatable=True))
        pick_edge(sheet, Edge("wealth", repeatable=True))
        self.assertEqual(sheet.edges.count("wealth"), 2)

    def test_the_underdog_slot_cannot_buy_a_power_edge(self):
        sheet = TalentSheet()
        pick_edge(sheet, Edge("a"), underdog_eligible=True)
        pick_edge(sheet, Edge("b"), underdog_eligible=True)
        with self.assertRaises(TalentRulesError):
            pick_edge(sheet, Edge("psi", is_power=True), underdog_eligible=True)

    def test_using_the_underdog_slot_is_recorded(self):
        sheet = TalentSheet()
        pick_edge(sheet, Edge("a"), underdog_eligible=True)
        pick_edge(sheet, Edge("b"), underdog_eligible=True)
        self.assertFalse(sheet.underdog_used)
        pick_edge(sheet, Edge("c"), underdog_eligible=True)
        self.assertTrue(sheet.underdog_used)


class FocusTest(unittest.TestCase):
    def test_a_starting_character_has_one_focus(self):
        self.assertEqual(focus_slots(TalentSheet()), 1)

    def test_the_focused_edge_grants_a_second_focus(self):
        self.assertEqual(focus_slots(TalentSheet(), has_focused_edge=True), 2)

    def test_a_focus_taken_twice_reaches_level_two(self):
        sheet = TalentSheet()
        focus = Focus("ace_driver")
        self.assertEqual(pick_focus(sheet, focus), 1)
        self.assertEqual(pick_focus(sheet, focus, has_focused_edge=True), 2)

    def test_a_third_selection_is_refused(self):
        sheet = TalentSheet()
        focus = Focus("ace_driver")
        pick_focus(sheet, focus)
        pick_focus(sheet, focus, has_focused_edge=True)
        with self.assertRaises(TalentRulesError):
            pick_focus(sheet, focus, has_focused_edge=True)

    def test_a_single_level_focus_stops_at_one(self):
        sheet = TalentSheet()
        focus = Focus("one_level", levels=1)
        pick_focus(sheet, focus)
        with self.assertRaises(TalentRulesError):
            pick_focus(sheet, focus, has_focused_edge=True)

    def test_a_second_focus_needs_the_focused_edge(self):
        sheet = TalentSheet()
        pick_focus(sheet, Focus("first"))
        with self.assertRaises(TalentRulesError):
            pick_focus(sheet, Focus("second"))

    def test_a_focus_prerequisite_must_be_an_edge_the_character_has(self):
        sheet = TalentSheet()
        gated = Focus("gated", requires=("some_edge",))
        with self.assertRaises(TalentRulesError):
            pick_focus(sheet, gated)
        sheet.edges.append("some_edge")
        self.assertEqual(pick_focus(sheet, gated), 1)


if __name__ == "__main__":
    unittest.main()
