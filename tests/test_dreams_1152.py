"""Guards for the dream-writing worksheet (#1152).

Two properties are worth a test, and both are ones a later editor can destroy without noticing:

1. **One canonical home.** A second dream document is how the setting acquires two dreamologies.
2. **The narration never labels provenance.** The moment a scene says "this was astral projection", the
   mystery becomes a map and the player stops interpreting.

Also enforced: the file stays prose. Tomi writes dreams; he does not fill in a schema.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DREAMS = ROOT / "docs/campaign/DREAMS.md"
INDEX = ROOT / "docs/campaign/README.md"
CAMPAIGN = ROOT / "docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md"

RELATIVE_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class OneCanonicalHome(unittest.TestCase):
    def test_the_worksheet_exists(self):
        self.assertTrue(DREAMS.is_file(), "the dream worksheet is missing")

    def test_it_is_marked_a_template_not_canon(self):
        head = text(DREAMS)[:600].lower()
        self.assertIn("not canon", head)
        self.assertIn("template", head)
        self.assertIn("1152", text(DREAMS)[:900])

    def test_there_is_only_one_dream_writing_document(self):
        """Legacy snapshots are history; a *new* second dream document is the failure."""
        candidates = [p for p in (ROOT / "docs").rglob("*.md")
                      if p.name.upper().startswith("DREAMS")
                      and "legacy" not in p.parts]
        self.assertEqual([p.name for p in candidates], ["DREAMS.md"],
                         f"more than one dream document: {[p.name for p in candidates]}")

    def test_it_is_indexed_and_linked_from_the_campaign(self):
        self.assertIn("DREAMS.md", text(INDEX))
        self.assertIn("DREAMS.md", text(CAMPAIGN))


class TheWorksheetStaysProse(unittest.TestCase):
    def test_no_code_fences_or_schema(self):
        body = text(DREAMS)
        self.assertNotIn("```", body, "the author's worksheet must not contain code blocks")
        for key in ("site_id", "dream_id", "trigger_id", "spoiler_gate"):
            self.assertNotIn(key, body, f"field name {key} leaked into the author's file")

    def test_it_leaves_room_to_write_in_every_section(self):
        body = text(DREAMS)
        self.assertGreaterEqual(body.count("Tomi writes here"), 8,
                                "each section needs a place for the author to write")
        self.assertIn("EXAMPLE ONLY", body)
        self.assertIn("Unresolved", body + text(INDEX))


class AmbiguityIsPreserved(unittest.TestCase):
    def test_the_provenance_rule_is_stated(self):
        body = text(DREAMS).lower()
        self.assertIn("ambiguous", body)
        self.assertIn("never label", body + text(DREAMS).lower())

    def test_the_sources_are_listed_as_overlapping_not_options(self):
        body = text(DREAMS).lower()
        for source in ("subconscious", "collective unconscious", "astral", "time/space",
                       "telepath", "precognit"):
            self.assertIn(source, body, f"the worksheet omits {source}")

    def test_no_conscious_psi_is_required(self):
        body = text(DREAMS).lower()
        self.assertIn("no psi prerequisite", body)
        self.assertIn("never", body)
        self.assertIn("grant", body)

    def test_dream_actions_do_not_unlock_abilities(self):
        body = text(DREAMS).lower()
        self.assertIn("scene-bound", body)
        self.assertIn("do not unlock anything", body)

    def test_precognition_and_telepathy_are_bounded(self):
        body = text(DREAMS).lower()
        self.assertIn("no guaranteed prophecy", body)
        self.assertIn("lead, never a", body)
        self.assertIn("PSI_INVESTIGATION_BOUNDARY_1105.md", text(DREAMS))


class DreamHelsinkiRulesAreExplicit(unittest.TestCase):
    def test_the_dream_city_is_not_a_map_of_real_tunnels(self):
        body = text(DREAMS).lower()
        self.assertIn("dream helsinki", body)
        self.assertIn("not a claim that real tunnels are accessible", body)
        self.assertIn("licensed" if False else "investigation", body)

    def test_act_one_may_not_confirm_the_supernatural(self):
        body = text(DREAMS)
        section = body.split("## 11. Spoiler discipline")[1].split("## 12.")[0].lower()
        self.assertIn("must not", section)
        self.assertIn("confirm", section)


class LinksResolve(unittest.TestCase):
    def test_every_relative_link_resolves(self):
        broken = []
        for path in (DREAMS, INDEX, CAMPAIGN):
            for match in RELATIVE_LINK.finditer(text(path)):
                target = match.group(1)
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.name} -> {target}")
        self.assertEqual(broken, [], "broken links: " + "; ".join(broken))


if __name__ == "__main__":
    unittest.main()
