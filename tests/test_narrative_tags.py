"""The four fictional tag families (#1164, #1184)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.world.narrative_tags import (  # noqa: E402
    EVIDENCE_LADDER,
    ClueTag,
    GoalState,
    GoalTag,
    NarrativeTagError,
    PersonalityTag,
    Polarity,
    SocialTag,
    TagBook,
)


def social(tag_id: str = "social.1", **kw) -> SocialTag:
    base = dict(id=tag_id, holder="npc.falk", target="pc.rookie",
                fact="owes a favour", polarity=Polarity.FAVOURABLE)
    base.update(kw)
    return SocialTag(**base)


def goal(tag_id: str = "goal.1", **kw) -> GoalTag:
    base = dict(id=tag_id, text="Find the courier", owner="pc.rookie")
    base.update(kw)
    return GoalTag(**base)


def clue(tag_id: str = "clue.1", **kw) -> ClueTag:
    base = dict(id=tag_id, clue_id="clue.warehouse_log", holder="pc.rookie",
                fact="A pallet left after midnight", route="document", reliability="public")
    base.update(kw)
    return ClueTag(**base)


class SocialTagTests(unittest.TestCase):
    def test_a_social_tag_relates_two_different_parties(self):
        with self.assertRaises(NarrativeTagError):
            social(holder="pc.rookie", target="pc.rookie")

    def test_polarity_must_be_from_the_vocabulary(self):
        with self.assertRaises(NarrativeTagError):
            social(polarity="good")

    def test_a_tag_needs_a_fact(self):
        with self.assertRaises(NarrativeTagError):
            social(fact="  ")


class GoalTagTests(unittest.TestCase):
    def test_a_blocked_goal_must_name_its_blocker(self):
        with self.assertRaises(NarrativeTagError):
            goal(state=GoalState.BLOCKED)

    def test_an_open_goal_may_not_carry_blockers(self):
        with self.assertRaises(NarrativeTagError):
            goal(blocked_by=("goal.other",))

    def test_a_blocked_goal_with_a_blocker_is_valid(self):
        tag = goal(state=GoalState.BLOCKED, blocked_by=("goal.warrant",))
        self.assertEqual(tag.state, GoalState.BLOCKED)


class ClueTagTests(unittest.TestCase):
    def test_route_must_be_from_the_vocabulary(self):
        with self.assertRaises(NarrativeTagError):
            clue(route="psychic")

    def test_reliability_must_be_a_rung(self):
        with self.assertRaises(NarrativeTagError):
            clue(reliability="certain")

    def test_the_rung_orders_the_ladder(self):
        weak = clue(reliability="witness")
        strong = clue(reliability="authenticated")
        self.assertLess(weak.rung, strong.rung)
        self.assertEqual(EVIDENCE_LADDER[0], "witness")


class PersonalityTagTests(unittest.TestCase):
    def test_a_personality_tag_says_what_moves_them_and_what_they_will_not_do(self):
        tag = PersonalityTag(id="personality.falk", npc="npc.falk", trait="procedural",
                             lever="a clean paper trail", under_pressure="narrows the case",
                             taboo="cover for a colleague")
        self.assertEqual(tag.lever, "a clean paper trail")

    def test_a_trait_without_a_lever_is_not_a_personality_tag(self):
        with self.assertRaises(NarrativeTagError):
            PersonalityTag(id="personality.x", npc="npc.falk", trait="procedural",
                           lever="  ", under_pressure="waits")


class TagBookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.book = TagBook()
        self.book.add_social(social())
        self.book.add_goal(goal())
        self.book.add_clue(clue())
        self.book.add_personality(PersonalityTag(
            id="personality.falk", npc="npc.falk", trait="procedural",
            lever="a clean paper trail", under_pressure="narrows the case"))

    def test_has_leverage_reads_social_tags(self):
        self.assertTrue(self.book.has_leverage("pc.rookie", "npc.falk"))

    def test_has_leverage_is_false_for_a_stranger(self):
        self.assertFalse(self.book.has_leverage("pc.rookie", "npc.stranger"))

    def test_a_clue_about_a_person_is_leverage_over_them(self):
        self.book.add_clue(clue("clue.2", bears_on=("npc.stranger",)))
        self.assertTrue(self.book.has_leverage("pc.rookie", "npc.stranger"))

    def test_a_clue_about_nobody_is_not_leverage_over_anyone(self):
        self.assertFalse(self.book.has_leverage("pc.rookie", "npc.stranger"))

    def test_completed_goals_have_the_shape_the_story_graph_expects(self):
        self.assertEqual(self.book.completed_goal_ids(), frozenset())
        self.book.goals["goal.done"] = goal("goal.done", state=GoalState.DONE)
        self.assertEqual(self.book.completed_goal_ids(), frozenset({"goal.done"}))

    def test_strongest_rung_reports_the_best_evidence_held(self):
        self.assertEqual(self.book.strongest_rung("pc.rookie"), EVIDENCE_LADDER.index("public"))
        self.assertEqual(self.book.strongest_rung("pc.nobody"), -1)

    def test_a_goal_blocked_by_an_unknown_goal_is_refused(self):
        with self.assertRaises(NarrativeTagError):
            self.book.add_goal(goal("goal.x", state=GoalState.BLOCKED, blocked_by=("goal.ghost",)))

    def test_duplicate_ids_are_refused(self):
        with self.assertRaises(NarrativeTagError):
            self.book.add_social(social())

    def test_roundtrip_preserves_all_four_families(self):
        restored = TagBook.from_dict(self.book.to_dict())
        self.assertEqual(restored.to_dict(), self.book.to_dict())

    def test_validate_catches_an_unknown_character(self):
        with self.assertRaises(NarrativeTagError):
            self.book.validate(known_characters={"pc.rookie"})


if __name__ == "__main__":
    unittest.main()
