"""#1283: five tag families, an open list, and four graphs — the author's decision, checked in code.

The decision is a *design* decision, so most of it is prose. What can be enforced is the part that would otherwise be
quietly renegotiated: the five families exist, Psyche has replaced Personality without breaking older code, an Astral
tag cannot claim a fourth kind of effect, the list can grow by name, and the graph families have not multiplied.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

# Import through `src.` on purpose: `world` also names the MUD package, so a bare `import world` can resolve to
# `mud/world` and then find no `narrative_tags` (the trap recorded in docs/rules/WORLD_GRAPHS_1178.md).
from src.rules import scene_tags  # noqa: E402
from src.world import narrative_tags  # noqa: E402
from src.world.graphs import (  # noqa: E402
    CyberGraph, PhysicalGraph, SocialGraph, StoryGraph, WorldGraphs,
)


class FamilyListTests(unittest.TestCase):
    def test_the_five_starting_families_exist(self):
        self.assertEqual(set(scene_tags.TAG_FAMILIES), {"clue", "social", "goal", "psyche", "astral"})

    def test_each_family_says_what_it_records(self):
        for name, meaning in scene_tags.TAG_FAMILIES.items():
            self.assertTrue(meaning.strip(), name)

    def test_psyche_replaces_personality(self):
        self.assertIn("psyche", scene_tags.TAG_FAMILIES)
        self.assertNotIn("personality", scene_tags.TAG_FAMILIES)
        self.assertIs(scene_tags.PersonalityTag, scene_tags.PsycheTag)

    def test_the_list_is_open(self):
        name = scene_tags.register_family("debt", "An obligation someone can call in.")
        try:
            self.assertIn(name, scene_tags.TAG_FAMILIES)
        finally:
            del scene_tags.TAG_FAMILIES[name]

    def test_a_new_family_needs_a_name_and_a_meaning(self):
        with self.assertRaises(scene_tags.TagFamilyError):
            scene_tags.register_family("  ", "something")
        with self.assertRaises(scene_tags.TagFamilyError):
            scene_tags.register_family("debt", "  ")
        with self.assertRaises(scene_tags.TagFamilyError):
            scene_tags.register_family("clue", "a second meaning for a taken name")


class PsycheTests(unittest.TestCase):
    def test_an_enduring_trait_and_a_temporary_state_are_both_psyche(self):
        enduring = scene_tags.PsycheTag("laura.wendt", "protective of sources")
        shaken = scene_tags.PsycheTag("tony.german", "shaken after the ambush", duration="temporary")
        self.assertEqual(enduring.duration, "enduring")
        self.assertEqual(shaken.duration, "temporary")

    def test_a_psyche_tag_is_a_word_not_a_timer(self):
        """Nothing in the tag expires itself; #1283 says the state fades 'as events unfold', which is the table's job."""
        tag = scene_tags.PsycheTag("tony.german", "shaken", duration="temporary")
        self.assertFalse(hasattr(tag, "expires"))
        self.assertFalse(hasattr(tag, "roll"))

    def test_the_campaign_store_bridges_into_the_portable_record(self):
        stored = narrative_tags.PsycheTag(
            id="laura-protective", npc="laura.wendt", trait="protective of sources",
            lever="a witness she promised to protect", under_pressure="she will not trade a source",
        )
        portable = stored.to_family_tag()
        # The repository supports two import roots (`src.…` and, with `src` on the path, `rules.…`), so the bridge's
        # class object is not necessarily *this* module's class object. Compare the shape it must have instead.
        self.assertEqual(type(portable).__name__, "PsycheTag")
        self.assertEqual(portable.owner_id, "laura.wendt")
        self.assertEqual(portable.trait, "protective of sources")

    def test_the_store_keeps_the_old_name_working(self):
        self.assertIs(narrative_tags.PersonalityTag, narrative_tags.PsycheTag)
        book = narrative_tags.TagBook()
        self.assertEqual(book.personality, book.psyche)


class AstralTagTests(unittest.TestCase):
    def test_an_astral_tag_records_a_fact_and_what_it_affects(self):
        tag = scene_tags.AstralTag(
            owner_id="tony.german", fact="picks up abandoned intentions",
            domain="perceive", source="the implant's own testimony",
        )
        self.assertEqual(tag.domain, "perceive")

    def test_only_three_domains_are_allowed(self):
        self.assertEqual(scene_tags.ASTRAL_DOMAINS, ("perceive", "attempt", "change"))
        with self.assertRaises(ValueError):
            scene_tags.AstralTag("tony.german", "sees the future", domain="predict")

    def test_a_fact_needs_an_owner_and_a_source_field(self):
        with self.assertRaises(ValueError):
            scene_tags.AstralTag("", "something")
        tag = scene_tags.AstralTag("tony.german", "someone is still waiting here")
        self.assertEqual(tag.source, "", "the source may be empty, but the field exists because #1283 asks for it")


class GraphFamilyTests(unittest.TestCase):
    def test_there_are_four_graphs_and_no_astral_graph(self):
        graphs = WorldGraphs(PhysicalGraph(), CyberGraph(), SocialGraph(), StoryGraph())
        for attribute in ("physical", "cyber", "social", "story"):
            self.assertTrue(hasattr(graphs, attribute), attribute)
        self.assertFalse(hasattr(graphs, "astral"), "the Astral graph is deferred (#1178, #1230)")

    def test_a_social_tag_can_describe_a_tie(self):
        """The Social graph's edges are ties; a Social tag says what a tie means today."""
        tag = scene_tags.SocialTag(
            source="tony.german", target="laura.wendt", score=2, kind="owes a favour",
        )
        self.assertEqual(tag.kind, "owes a favour")


if __name__ == "__main__":
    unittest.main()
