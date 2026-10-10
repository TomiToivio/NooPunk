# -*- coding: utf-8 -*-
"""Guard for the #232 rulebook part map.

`docs/rulebook_map.json` assigns every section of `RULEBOOK.md` to exactly one part. The
failure mode that matters is not a wrong assignment — a human can argue about those — it is a
section that quietly stops being assigned at all: the document gains a `##` section, no map
entry follows, and nothing says so.

So this guard **re-derives the section list from `RULEBOOK.md` itself** and requires an exact
match, including byte offsets. It never trusts the map's own claim about what the document
contains. It also pins the measured evidence in the scheme document, so the prose cannot drift
away from the numbers it was derived from.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"
MAP = ROOT / "docs" / "rulebook_map.json"
SCHEME = ROOT / "docs" / "design" / "RULEBOOK_PART_MAP_2026-10-10.md"

CORE_MARKER = "# Extended canon and reference material"

#: The document's measured shape at the time the map was written. If a section is genuinely
#: added, these numbers change WITH the map and the scheme document, in one deliberate change.
EXPECTED_SECTIONS = 64
EXPECTED_CORE = 10
EXPECTED_LEDGER = 54
EXPECTED_LENGTH = 320640
EXPECTED_TOTAL_MAPPED_CHARS = 318136

#: The nine parts, in reading order. Eight are the author's functional scheme; `reference`
#: is the apparatus the seven do not cover.
EXPECTED_PARTS = [
    "basic_rules", "character_generation", "physical", "cybernetic", "psychic",
    "social", "lore", "gm_toolkit", "reference",
]


def derive_sections() -> list[dict]:
    """Re-derive the section list from the canonical document. Never reads the map."""
    src = RULEBOOK.read_text(encoding="utf-8")
    mi = src.find(CORE_MARKER)
    assert mi > 0, "the core/ledger marker is missing from RULEBOOK.md"
    out: list[dict] = []
    for tag, text, base in (("core", src[:mi], 0), ("ledger", src[mi:], mi)):
        hs = list(re.finditer(r"(?m)^## (.+)$", text))
        for k, m in enumerate(hs):
            end = hs[k + 1].start() if k + 1 < len(hs) else len(text)
            out.append({
                "key": f"{tag}:{m.group(1).strip()}",
                "title": m.group(1).strip(),
                "half": tag,
                "start": base + m.start(),
                "size": end - m.start(),
            })
    return out


def load_map() -> dict:
    return json.loads(MAP.read_text(encoding="utf-8"))


class MapCoversTheDocumentTests(unittest.TestCase):
    """The map must describe the document that exists, not the one it was written against."""

    def setUp(self) -> None:
        self.derived = derive_sections()
        self.data = load_map()
        self.mapped = self.data["sections"]

    def test_the_map_and_the_scheme_exist(self):
        self.assertTrue(MAP.is_file(), "docs/rulebook_map.json is missing")
        self.assertTrue(SCHEME.is_file(), "the split scheme document is missing")

    def test_the_canonical_length_is_the_file_length(self):
        self.assertEqual(self.data["canonical"], "RULEBOOK.md")
        self.assertEqual(
            self.data["canonical_length"],
            len(RULEBOOK.read_text(encoding="utf-8")),
        )
        self.assertEqual(self.data["canonical_length"], EXPECTED_LENGTH)

    def test_the_section_list_is_exactly_the_document_s(self):
        """The completeness check: derived and mapped must agree key-for-key, in order."""
        self.assertEqual(
            [s["key"] for s in self.mapped],
            [s["key"] for s in self.derived],
            "the map's section list no longer matches RULEBOOK.md",
        )

    def test_every_offset_and_size_matches_the_document(self):
        for want, got in zip(self.derived, self.mapped):
            with self.subTest(section=want["key"]):
                self.assertEqual(got["start"], want["start"])
                self.assertEqual(got["size"], want["size"])
                self.assertEqual(got["title"], want["title"])
                self.assertEqual(got["half"], want["half"])

    def test_the_shape_is_pinned(self):
        self.assertEqual(len(self.mapped), EXPECTED_SECTIONS)
        core = [s for s in self.mapped if s["half"] == "core"]
        ledger = [s for s in self.mapped if s["half"] == "ledger"]
        self.assertEqual(len(core), EXPECTED_CORE)
        self.assertEqual(len(ledger), EXPECTED_LEDGER)

    def test_the_marker_offset_is_recorded_and_correct(self):
        read = RULEBOOK.read_text(encoding="utf-8")
        self.assertEqual(self.data["core_marker"], CORE_MARKER)
        self.assertEqual(self.data["core_marker_offset"], read.find(CORE_MARKER))


class EverySectionHasExactlyOneHomeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load_map()
        self.mapped = self.data["sections"]

    def test_no_section_is_unassigned(self):
        unassigned = [s["key"] for s in self.mapped if s["part"] == "UNASSIGNED"]
        self.assertEqual(unassigned, [], f"sections with no part: {unassigned}")

    def test_every_part_is_a_declared_part(self):
        declared = set(self.data["parts"])
        for s in self.mapped:
            with self.subTest(section=s["key"]):
                self.assertIn(s["part"], declared)

    def test_the_parts_are_the_nine_in_reading_order(self):
        self.assertEqual(list(self.data["parts"]), EXPECTED_PARTS)
        self.assertEqual(len(self.data["parts"]), 9)

    def test_every_part_owns_at_least_one_section(self):
        owned = {s["part"] for s in self.mapped}
        for part in self.data["parts"]:
            with self.subTest(part=part):
                self.assertIn(part, owned, f"part {part} owns nothing")

    def test_a_part_is_never_claimed_by_a_section_outside_it(self):
        # each section carries exactly one part field, and the aggregate is reproducible
        totals: dict[str, int] = {}
        for s in self.mapped:
            totals[s["part"]] = totals.get(s["part"], 0) + s["size"]
        self.assertEqual(sum(totals.values()), EXPECTED_TOTAL_MAPPED_CHARS)


class TheSchemeDocumentStaysTrueTests(unittest.TestCase):
    """The prose must not drift from the numbers it was derived from."""

    def setUp(self) -> None:
        self.text = " ".join(SCHEME.read_text(encoding="utf-8").split())
        self.data = load_map()

    def test_it_is_marked_non_destructive_and_proposed(self):
        self.assertIn("PROPOSED, non-destructive", self.text)
        self.assertIn("RULEBOOK.md` remains the single canonical source", self.text)

    def test_it_names_every_part_including_the_provisional_ones(self):
        for part in self.data["parts"].values():
            with self.subTest(part=part):
                self.assertIn(part, self.text)

    def test_it_defers_to_the_landed_seven_book_architecture(self):
        """It must be the executable form of the merged README, not a competing scheme."""
        self.assertIn("docs/rulebook_segments/README.md", self.text)
        self.assertIn("executable form", self.text)
        self.assertIn("The seven books are adopted unchanged", self.text)

    def test_the_two_provisional_parts_are_flagged_in_both_documents(self):
        self.assertEqual(self.data["provisional_parts"], ["gm_toolkit", "reference"])
        self.assertRegex(self.text, r"(?i)two provisional parts")
        self.assertIn("Both are the author's call.", self.text)

    def test_the_headline_measurement_is_still_true(self):
        # lore is the largest part, by a wide margin
        totals: dict[str, int] = {}
        for s in self.data["sections"]:
            totals[s["part"]] = totals.get(s["part"], 0) + s["size"]
        largest = max(totals, key=lambda k: totals[k])
        self.assertEqual(largest, "lore")
        self.assertGreater(totals["lore"], 2 * totals["reference"])
        self.assertIn("45.0%", self.text)

    def test_it_states_the_citation_and_numbering_constraints(self):
        for fact in ("cited **by link, never by their own §-numbers**",
                     "**Do not renumber.**",
                     "tests/test_theory_sections_survive.py"):
            with self.subTest(fact=fact[:40]):
                self.assertIn(fact, self.text)

    def test_it_does_not_claim_a_licence_decision(self):
        self.assertIn("does not select a licence", self.text)


if __name__ == "__main__":
    unittest.main()
