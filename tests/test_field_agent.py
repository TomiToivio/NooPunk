"""NoöPunk field-agent generation (#809): CWN attributes, NoöPunk agency choice, deterministic.

The point of these tests is the boundary: attributes and the swap are CWN's and must not drift; the
agency is NoöPunk's and must actually do something; the same seed must rebuild the same agent.
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules.field_agent import (  # noqa: E402
    AGENCIES,
    ATTRIBUTES,
    ATTRIBUTE_MAX,
    ATTRIBUTE_MIN,
    STARTING_LEVEL,
    GenerationError,
    generate_field_agent,
    is_field_agent_record,
    roll_attributes,
    swap_attributes,
)


def agent(seed: int = 1, agency: str = "supo", **kwargs):
    return generate_field_agent(name="Aino Virtanen", agency=agency, rng=random.Random(seed), **kwargs)


class AttributeTest(unittest.TestCase):
    def test_attributes_are_3d6_in_order(self):
        rng = random.Random(7)
        expected = {attr: sum(rng.randint(1, 6) for _ in range(3)) for attr in ATTRIBUTES}
        self.assertEqual(roll_attributes(random.Random(7)), expected)

    def test_every_attribute_is_inside_the_cwn_range(self):
        for seed in range(50):
            attributes = roll_attributes(random.Random(seed))
            self.assertEqual(set(attributes), set(ATTRIBUTES))
            for value in attributes.values():
                self.assertGreaterEqual(value, ATTRIBUTE_MIN)
                self.assertLessEqual(value, ATTRIBUTE_MAX)

    def test_one_swap_is_applied(self):
        base = {attribute: 10 for attribute in ATTRIBUTES}
        base["STR"], base["INT"] = 8, 15
        swapped = swap_attributes(base, "STR", "INT")
        self.assertEqual((swapped["STR"], swapped["INT"]), (15, 8))

    def test_a_swap_needs_two_known_different_attributes(self):
        base = {attribute: 10 for attribute in ATTRIBUTES}
        with self.assertRaises(GenerationError):
            swap_attributes(base, "STR", "STR")
        with self.assertRaises(GenerationError):
            swap_attributes(base, "STR", "LUK")


class AgencyTest(unittest.TestCase):
    def test_the_three_services_exist(self):
        self.assertEqual(set(AGENCIES), {"supo", "europol", "unsa"})

    def test_each_agency_grants_its_skill(self):
        self.assertIn("Investigate", agent(agency="supo").skills)
        self.assertIn("Connect", agent(agency="europol").skills)
        self.assertIn("Know", agent(agency="unsa").skills)

    def test_agency_does_not_change_attributes(self):
        """A background choice must not become a stealth stat bonus."""
        a = agent(seed=5, agency="supo")
        b = agent(seed=5, agency="unsa")
        self.assertEqual(a.attributes, b.attributes)

    def test_unknown_agency_is_refused(self):
        with self.assertRaises(GenerationError):
            agent(agency="kansainvalinen")

    def test_blank_name_is_refused(self):
        with self.assertRaises(GenerationError):
            generate_field_agent(name="   ", agency="supo", rng=random.Random(1))


class DeterminismTest(unittest.TestCase):
    def test_same_seed_same_agent(self):
        self.assertEqual(agent(seed=42).to_dict(), agent(seed=42).to_dict())

    def test_different_seeds_differ(self):
        self.assertNotEqual(agent(seed=1).attributes, agent(seed=2).attributes)

    def test_a_starting_agent_is_level_one(self):
        self.assertEqual(agent().level, STARTING_LEVEL)


class RoleTest(unittest.TestCase):
    def test_a_generated_agent_is_the_player_character(self):
        self.assertTrue(agent().is_player_character)

    def test_no_psionics_are_granted(self):
        """Romppainen is not psychic by default, and neither is the player."""
        record = agent().to_dict()
        self.assertNotIn("psionics", record)
        self.assertNotIn("disciplines", record)

    def test_save_guard_rejects_a_non_agent_record(self):
        self.assertTrue(is_field_agent_record(agent().to_dict()))
        self.assertFalse(is_field_agent_record({"is_player_character": True, "agency": "romppainen"}))


if __name__ == "__main__":
    unittest.main()
