"""Guards for the five-family tag layer and the #1283 tabletop reference."""

import re
import unittest
from pathlib import Path

from src.rules import scene_tags  # noqa: E402
from src.rules.scene_tags import (
    TAG_FAMILIES,
    AstralTag,
    PersonalityTag,
    PsycheTag,
)
from src.world.narrative_tags import AstralTag as NpcAstralTag
from src.world.narrative_tags import PersonalityTag as NpcPersonalityTag
from src.world.narrative_tags import PsycheTag as NpcPsycheTag
from src.world.narrative_tags import TagBook

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "tabletop" / "TAGS_AND_GRAPHS_1283.md"
REGISTER = ROOT / "docs" / "DOCUMENT_REGISTER.md"


class FiveTagFamiliesTest(unittest.TestCase):
    def test_the_author_families_are_exactly_the_five_starting_names(self):
        self.assertEqual(TAG_FAMILIES, ("Clue", "Social", "Goal", "Psyche", "Astral"))

    def test_psyche_is_the_new_name_for_the_serialized_personality_record(self):
        self.assertIs(PsycheTag, PersonalityTag)
        tag = PsycheTag("tony.german", "protective of sources", "#1217")
        self.assertIsInstance(tag, PersonalityTag)
        self.assertFalse(hasattr(tag, "modifier"))

    def test_astral_tag_is_a_fact_not_a_power_or_modifier(self):
        tag = AstralTag(
            "tony.german",
            "Someone is still waiting here",
            subject="loc.kurvi.stairwell",
            evidence="implant impression",
        )
        self.assertEqual(tag.subject, "loc.kurvi.stairwell")
        self.assertFalse(hasattr(tag, "effort"))
        self.assertFalse(hasattr(tag, "rank"))
        with self.assertRaises(ValueError):
            AstralTag("tony.german", "  ")

    def test_npc_tagbook_exposes_the_same_psyche_and_astral_families(self):
        self.assertIs(NpcPsycheTag, NpcPersonalityTag)
        book = TagBook()
        psyche = NpcPsycheTag(
            id="psyche.falk",
            npc="npc.falk",
            trait="procedural",
            lever="a clean paper trail",
            under_pressure="narrows the case",
        )
        astral = NpcAstralTag(
            id="astral.kurvi.stairwell",
            owner="pc.rookie",
            fact="Someone is still waiting here",
            subject="loc.kurvi.stairwell",
        )
        book.add_psyche(psyche)
        book.add_astral(astral)
        self.assertEqual(book.psyche_of("npc.falk"), psyche)
        self.assertEqual(book.astral_of("pc.rookie"), (astral,))
        restored = TagBook.from_dict(book.to_dict())
        self.assertEqual(restored.astral_of("pc.rookie"), (astral,))

    def test_document_names_the_five_families_four_graphs_and_open_ending(self):
        text = DOC.read_text(encoding="utf-8")
        flat = " ".join(text.split()).lower()
        for term in (
            "five starting tag families",
            "four graphs",
            "clue",
            "social",
            "goal",
            "psyche",
            "astral",
            "open-ended",
            "cities without number",
            "astral tags are not an astral graph",
            "no new resolver",
        ):
            with self.subTest(term=term):
                self.assertIn(term, flat)

    def test_document_example_records_a_clue_source(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Someone is still waiting here", text)
        self.assertIn("Picks up abandoned intentions", text)
        self.assertIn("Clue Tag", text)
        self.assertIn("source", text.lower())

    def test_register_row_exists(self):
        register = REGISTER.read_text(encoding="utf-8")
        self.assertIn("tabletop/TAGS_AND_GRAPHS_1283.md", register)
        self.assertIn("#1283", register)

    def test_links_resolve(self):
        text = DOC.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if link.startswith("#") or "://" in link:
                continue
            with self.subTest(link=link):
                self.assertTrue((DOC.parent / link).resolve().exists(), link)


class OpenFamilyListTests(unittest.TestCase):
    """The five are a starting vocabulary, not a closed list (#1283): the sixth must be expressible in code."""

    def test_every_starting_family_says_what_it_records(self):
        for name in ("clue", "social", "goal", "psyche", "astral"):
            self.assertTrue(scene_tags.TAG_FAMILY_MEANINGS[name].strip(), name)

    def test_a_new_family_can_be_added_by_name(self):
        before = scene_tags.TAG_FAMILIES
        added = scene_tags.register_family("debt", "An obligation someone can call in.")
        try:
            self.assertIn(added, scene_tags.TAG_FAMILY_MEANINGS)
            self.assertIn("Debt", scene_tags.TAG_FAMILIES)
        finally:
            scene_tags.TAG_FAMILY_MEANINGS.pop(added, None)
            scene_tags.TAG_FAMILIES = before

    def test_a_new_family_needs_a_name_and_a_meaning_and_a_free_slot(self):
        with self.assertRaises(scene_tags.TagFamilyError):
            scene_tags.register_family("   ", "something")
        with self.assertRaises(scene_tags.TagFamilyError):
            scene_tags.register_family("debt", "   ")
        with self.assertRaises(scene_tags.TagFamilyError):
            scene_tags.register_family("clue", "a second meaning for a taken name")


class PsycheDurationTests(unittest.TestCase):
    def test_an_enduring_trait_and_a_temporary_state_are_both_psyche_tags(self):
        enduring = PsycheTag("laura.wendt", "protective of sources")
        shaken = PsycheTag("tony.german", "shaken after the ambush", duration="temporary")
        self.assertEqual(enduring.duration, "enduring")
        self.assertEqual(shaken.duration, "temporary")

    def test_a_psyche_tag_is_a_word_not_a_timer(self):
        tag = PsycheTag("tony.german", "shaken", duration="temporary")
        self.assertFalse(hasattr(tag, "expires"))
        self.assertFalse(hasattr(tag, "roll"))

    def test_an_unknown_duration_is_refused(self):
        with self.assertRaises(ValueError):
            PsycheTag("tony.german", "shaken", duration="until-next-scene")


class AstralDomainTests(unittest.TestCase):
    def test_a_tag_states_which_of_three_things_it_affects(self):
        self.assertEqual(scene_tags.ASTRAL_DOMAINS, ("perceive", "attempt", "change"))
        tag = AstralTag("tony.german", "picks up abandoned intentions", domain="perceive")
        self.assertEqual(tag.domain, "perceive")

    def test_a_fourth_domain_is_refused(self):
        with self.assertRaises(ValueError):
            AstralTag("tony.german", "sees the future", domain="predict")


class StoreBridgeTests(unittest.TestCase):
    def test_the_campaign_store_projects_onto_the_portable_tag(self):
        stored = NpcPsycheTag(
            id="laura-protective", npc="laura.wendt", trait="protective of sources",
            lever="a witness she promised to protect", under_pressure="she will not trade a source",
        )
        portable = stored.to_family_tag()
        # Two import roots exist (`src.…` and `rules.…` with `src` on the path), so compare the shape, not the object.
        # `PsycheTag` is the #1283 name for a class that keeps `PersonalityTag` as its serialized name.
        self.assertIn(type(portable).__name__, {"PsycheTag", "PersonalityTag"})
        self.assertEqual(portable.owner_id, "laura.wendt")
        self.assertEqual(portable.trait, "protective of sources")


if __name__ == "__main__":
    unittest.main()
