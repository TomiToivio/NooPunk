"""Executable tests for research clocks and technology prerequisites (#506)."""
import json
from random import Random
import unittest

from strategy_game.research import (
    ResearchError, ResearchProject, ResearchState, TechNode,
    advance_research, validate_catalog,
)
from strategy_game.rpg.fate import Character


def lead(skill=4):
    return Character("scientist", "Scientist", ["Careful"], strategic_skills={"SCIENCE": skill})


def scenario(capacity=3, difficulty=0):
    node = TechNode(
        "alien_principles", "Alien principles", ("alien-derived", "quantumpunk"),
        required_evidence=("fragment",), unlocks=("field_inspection",),
    )
    return ResearchState(
        nodes={"alien_principles": node},
        projects={"p": ResearchProject("p", "alien_principles", "scientist", difficulty, 12, allocated_capacity=capacity)},
    )


class ResearchClockTests(unittest.TestCase):
    def test_missing_evidence_blocks_even_great_scientist(self):
        s = scenario()
        self.assertEqual(advance_research(s, "p", lead(), rng=Random(1)).outcome, "blocked")
        self.assertEqual(s.projects["p"].progress, 0)

    def test_failed_check_preserves_progress(self):
        s = scenario(difficulty=20)
        s.add_evidence("fragment")
        s.projects["p"].progress = 3
        r = advance_research(s, "p", lead(), rng=Random(2))
        self.assertEqual((r.outcome, r.gained, r.progress), ("stalled", 0, 3))

    def test_success_is_capacity_limited_and_idempotent(self):
        s = scenario()
        s.add_evidence("fragment")
        for expected in (3, 6, 9, 12):
            r = advance_research(s, "p", lead(), rng=Random(1))
            self.assertEqual(r.progress, expected)
        self.assertEqual(r.outcome, "completed")
        self.assertEqual(s.known, {"alien_principles"})
        self.assertIn("field_inspection", s.unlocked_rpg_options)
        self.assertEqual(advance_research(s, "p", lead(), rng=Random(1)).outcome, "already_completed")

    def test_capacity_changes_throughput_not_roll(self):
        s = scenario(capacity=5)
        s.add_evidence("fragment")
        self.assertEqual(advance_research(s, "p", lead(), rng=Random(1)).gained, 5)

    def test_pause_reassignment_and_no_capacity(self):
        s = scenario(capacity=0)
        s.add_evidence("fragment")
        self.assertEqual(advance_research(s, "p", lead(), rng=Random(1)).outcome, "unfunded")
        s.projects["p"].allocated_capacity = 2
        s.projects["p"].paused = True
        self.assertEqual(advance_research(s, "p", lead(), rng=Random(1)).outcome, "paused")
        s.projects["p"].paused = False
        with self.assertRaises(ResearchError):
            advance_research(s, "p", Character("other", "Other", [], strategic_skills={"SCIENCE": 4}), rng=Random(1))
        s.projects["p"].leader_id = "other"
        r = advance_research(s, "p", Character("other", "Other", [], strategic_skills={"SCIENCE": 4}), rng=Random(1))
        self.assertEqual(r.gained, 2)

    def test_persistence_round_trip(self):
        s = scenario()
        s.add_evidence("fragment")
        advance_research(s, "p", lead(), rng=Random(1))
        loaded = ResearchState.from_dict(json.loads(json.dumps(s.to_dict())))
        self.assertEqual(s.to_dict(), loaded.to_dict())
        self.assertEqual(advance_research(loaded, "p", lead(), rng=Random(1)).progress, 6)

    def test_ideology_and_dependency(self):
        first = TechNode("principles", "Principles", ("cyberpunk",))
        second = TechNode("prototype", "Prototype", ("cyberpunk", "biopunk"),
                          prerequisites=("principles",), forbidden_policies=("no_augmentation",),
                          stage="prototype")
        s = ResearchState(nodes={"principles": first, "prototype": second}, policies={"no_augmentation"})
        project = ResearchProject("p", "prototype", "scientist", 0, 2, allocated_capacity=2)
        s.projects["p"] = project
        self.assertFalse(s.eligible(project))
        s.known.add("principles")
        self.assertFalse(s.eligible(project))
        s.policies.clear()
        self.assertTrue(s.eligible(project))

    def test_invalid_graph_and_clock(self):
        with self.assertRaises(ResearchError):
            validate_catalog({"a": TechNode("a", "A", ("x",), prerequisites=("missing",))})
        with self.assertRaises(ResearchError):
            validate_catalog({
                "a": TechNode("a", "A", ("x",), prerequisites=("b",)),
                "b": TechNode("b", "B", ("x",), prerequisites=("a",)),
            })
        with self.assertRaises(ResearchError):
            ResearchProject("p", "a", "agent", 0, 4, progress=5)


if __name__ == "__main__":
    unittest.main()
