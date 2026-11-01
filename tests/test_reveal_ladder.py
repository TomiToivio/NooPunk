"""The reveal ladder is data with a shape a scene can rely on (#1007).

NoöPunk begins as cyberpunk and earns its cosmology. That is a content rule, so it is not asserted here
as prose — but the *shape* the content depends on is: four ordered stages, each with what it may show
and what it must not, and a perspective block the writing has to obey. A quest tool can read that;
a reviewer can diff it.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LADDER = ROOT / "data" / "world" / "reveal_ladder.json"


class LadderShapeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(LADDER.read_text(encoding="utf-8"))
        self.stages = self.data["stages"]

    def test_the_ladder_opens_as_cyberpunk(self) -> None:
        first = min(self.stages, key=lambda s: s["order"])
        self.assertEqual(first["id"], "street")
        self.assertEqual(first["name"], "Cyberpunk")

    def test_stage_order_is_contiguous_and_unique(self) -> None:
        orders = [s["order"] for s in self.stages]
        self.assertEqual(orders, list(range(1, len(self.stages) + 1)))
        self.assertEqual(len({s["id"] for s in self.stages}), len(self.stages))

    def test_every_stage_says_what_it_allows_and_what_it_forbids(self) -> None:
        for stage in self.stages:
            self.assertTrue(stage["may_appear"], stage["id"])
            self.assertTrue(stage["may_not_appear"], stage["id"])

    def test_the_first_two_stages_withhold_the_cosmic_vocabulary(self) -> None:
        """Early play may not *use* the lexicon — not merely be told to avoid it."""
        early = [s for s in self.stages if s["order"] <= 2]
        for stage in early:
            allowed = " ".join(stage["may_appear"]).lower()
            self.assertNotIn("sto/sts", allowed, stage["id"])
            self.assertNotIn("nhi", allowed, stage["id"])
        opening = min(self.stages, key=lambda s: s["order"])
        self.assertIn("nhi", " ".join(opening["may_not_appear"]).lower())

    def test_a_later_stage_never_forbids_what_an_earlier_one_allows(self) -> None:
        """The ladder only widens: a rule that could un-teach a player would be a contradiction."""
        for i, stage in enumerate(sorted(self.stages, key=lambda s: s["order"])):
            inherited = {item for earlier in sorted(self.stages, key=lambda s: s["order"])[:i]
                         for item in earlier["may_appear"]}
            self.assertEqual(inherited & set(stage["may_not_appear"]), set(), stage["id"])

    def test_the_perspective_block_binds_the_writing(self) -> None:
        perspective = self.data["perspective"]
        self.assertIn("rookie", perspective["player_character"].lower())
        self.assertIn("Romppainen", perspective["mentor"])
        self.assertIn("never", perspective["forbidden"].lower())

    def test_romppainen_is_not_a_lore_dump(self) -> None:
        rule = " ".join(self.data["rules"]).lower()
        self.assertIn("never lectures the lore", rule)
        self.assertIn("never takes a decision", rule)


if __name__ == "__main__":
    unittest.main()
