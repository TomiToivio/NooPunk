"""Guard against the issue #101 regression: two competing sources sections.

Issue #99 asked for **one** living sources list, but two parallel sessions appended it
twice (``24a63b1`` wrote ``## 35. Sources…``; ``7865e0f`` wrote ``## 38. Living sources…``),
so ``main`` briefly carried two sections answering the same issue. The renumber that
followed also left ``§35.5`` pointing at "Role-playing games" when the cited Wendt theory
note had moved to ``§36.5``.

Both defects were invisible to CI: no test referenced either sources section, and
``test_theory_sections_survive::test_no_internal_dangling_section_reference`` only checks
that a cited ``§n.m`` resolves to *some* heading — ``§35.5`` resolved, to the wrong one.

This guard pins the state by **heading text** (section numbers get reused across commits),
and asserts the two things that were actually wrong:

* exactly one living-sources section exists, and it is the surviving one;
* the Wendt citation resolves to the section that really carries the Wendt theory note.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = "RULEBOOK.md"

#: The surviving sources section, and the duplicate that must not return.
SURVIVING = "Sources, recommended reading, and influences"
DUPLICATE = "Living sources, recommended reading, and influences"

#: The unique sentence in §33.2 whose citation was left off-by-one by the renumber.
WENDT_CITE = r"consciousness-theory inspirations\s*\(§(\d+\.\d+),\s*§33\.17\)"


def read() -> str:
    return (ROOT / RULEBOOK).read_text(encoding="utf-8")


def headings() -> list[str]:
    return re.findall(r"(?m)^##\s+\d+\.\s+(.*)", read())


def section_by_heading(needle: str) -> str:
    """Body of the top-level ``##`` section whose heading text contains `needle`."""
    match = re.search(
        rf"(?ms)^##\s+\d+\.\s+[^\n]*{re.escape(needle)}[^\n]*\n(.*?)(?=^##\s+\d+\.|\Z)",
        read(),
    )
    return match.group(1) if match else ""


class OneSourcesSectionTests(unittest.TestCase):
    def test_exactly_one_living_sources_section_exists(self) -> None:
        """The core of #101: #99 was delivered twice, so there must be one, not two."""
        tops = headings()
        matching = [h for h in tops if "sources" in h.lower() and "influences" in h.lower()]
        self.assertEqual(
            len(matching), 1,
            f"expected exactly one sources/influences section, found {len(matching)}: {matching}",
        )

    def test_the_surviving_section_is_present(self) -> None:
        self.assertIn(SURVIVING, "\n".join(headings()))

    def test_the_duplicate_section_does_not_return(self) -> None:
        self.assertNotIn(
            DUPLICATE, read(),
            "the duplicate #99 section was re-added; merge into one instead of appending again",
        )

    def test_no_two_sections_share_a_normalised_heading(self) -> None:
        """Generic catch: two headings that differ only by a leading adjective."""
        seen: dict[str, int] = {}
        for h in headings():
            key = " ".join(sorted(re.findall(r"[a-zöä]+", h.lower())))
            seen[key] = seen.get(key, 0) + 1
        dupes = {k: v for k, v in seen.items() if v > 1}
        self.assertEqual(dupes, {}, f"top-level headings duplicate the same words: {dupes}")


class MergedContentSurvivesTests(unittest.TestCase):
    """The merge must keep both sides, not just delete one of them."""

    def test_the_maintenance_rule_sentence_is_present(self) -> None:
        self.assertIn("Whenever a new work becomes a meaningful source", read())

    def test_the_ai_triad_is_present(self) -> None:
        body = section_by_heading(SURVIVING)
        for name in ("If Anyone Builds It", "Singularity Is Nearer", "The AI Con"):
            with self.subTest(work=name):
                self.assertIn(name, body)

    def test_the_fiction_entries_from_both_copies_survive(self) -> None:
        body = section_by_heading(SURVIVING)
        for novel in (
            "_Ubik_", "_VALIS_", "_A Scanner Darkly_",
            "_Do Androids Dream of Electric Sheep?_",
            "_The Three Stigmata of Palmer Eldritch_", "_Neuromancer_",
        ):
            with self.subTest(novel=novel):
                self.assertIn(novel, body)

    def test_the_rpg_entries_from_both_copies_survive(self) -> None:
        body = section_by_heading(SURVIVING)
        for entry in ("Eclipse Phase", "Cyberpunk 2013", "Shadowrun", "The Sprawl", "CY_BORG"):
            with self.subTest(entry=entry):
                self.assertIn(entry, body)

    def test_the_section_cross_references_the_theory_bibliography(self) -> None:
        """The merge makes the surviving section the design-side map next to §37."""
        self.assertRegex(section_by_heading(SURVIVING), r"§37")


class WendtCitationTests(unittest.TestCase):
    """Defect 2: the renumber left §35.5 pointing at 'Role-playing games'."""

    def test_the_citation_resolves_to_the_section_that_carries_the_wendt_note(self) -> None:
        match = re.search(WENDT_CITE, read())
        assert match is not None, "the §33.2 Wendt citation sentence moved or was rewritten"
        target = match.group(1)

        # the referenced subsection's parent section must actually hold the theory note
        body = section_by_heading("The four NoöPunk systems")
        self.assertIn(
            "Quantum Mind and Social Science", body,
            f"§{target} is cited for Wendt's Quantum Mind, but the four-systems section "
            "no longer carries that note",
        )

    def test_the_citation_is_not_left_on_the_renumbered_offset(self) -> None:
        """§35.5 is 'Role-playing games'; citing it for consciousness theory is wrong."""
        match = re.search(WENDT_CITE, read())
        assert match is not None
        self.assertNotEqual(
            match.group(1), "35.5",
            "the §33.2 citation is back on §35.5 (Role-playing games) — an off-by-one",
        )

    def test_the_rpg_subsection_is_still_where_the_bad_ref_pointed(self) -> None:
        """Pins the reason §35.5 is the wrong target, so the guard message stays true."""
        self.assertRegex(read(), r"(?m)^###\s+35\.5\s+Role-playing games")


class RulebookShapeTests(unittest.TestCase):
    def test_top_level_numbering_is_contiguous(self) -> None:
        numbers = [int(n) for n in re.findall(r"(?m)^##\s+(\d+)\.", read())]
        self.assertEqual(numbers, list(range(1, max(numbers) + 1)),
                         f"section numbering has a gap: {numbers}")

    def test_the_theory_bibliography_and_ontology_still_follow_the_sources_section(self) -> None:
        """The surviving section sits where it was written; the restored pair follows it."""
        tops = headings()

        def at(needle: str) -> int:
            matches = [i for i, h in enumerate(tops) if needle in h]
            self.assertEqual(len(matches), 1, f"expected one heading containing {needle!r}")
            return matches[0]

        src = at(SURVIVING)
        self.assertLess(src, at("The four NoöPunk systems"))
        self.assertLess(src, at("Theoretical sources and inspirations"))


if __name__ == "__main__":
    unittest.main()
