# -*- coding: utf-8 -*-
"""Guard for the #187 xenopolitics chapter.

Pins the properties that matter and could silently rot:

1. the chapter exists at its ledger number, is contiguous with the rest of the ledger, and
   is linked from the rulebook and from the §36.9 reference table;
2. the **canon reconciliation** holds: the chapter says the Crisis was a catastrophe with
   regional holocausts **and** that the Fall has not happened. A later edit must not
   silently upgrade it to a planet-destroying Fall (which would contradict §33.1/§33.28) or
   soften it to a non-event;
3. the **both-sides-help** premise and the moral axis sentence survive — they are the point
   of the section;
4. the **ambiguity** is preserved: the chapter must not resolve whether the two factions are
   genuinely distinct;
5. the chapter keeps its no-mechanics bound (no statistics, no faction mechanics).

Asserts structure and presence only, never wording beyond the required invariants.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"
CHAPTER = ROOT / "rulebook" / "15_XENOPOLITICS.md"
MARKER = "# Extended canon and reference material"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(text: str) -> str:
    return " ".join(text.split())


class XenopoliticsChapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rb = read(RULEBOOK)
        self.ch = read(CHAPTER)
        self.ch_flat = flat(self.ch)

    def test_the_modular_chapter_exists_with_its_heading(self) -> None:
        self.assertIn("# Xenopolitics after the NHI Crisis", self.ch)

    def test_the_ledger_chapter_exists_and_the_ledger_is_contiguous(self) -> None:
        core, appendix = self.rb.split(MARKER, 1)
        core_nums = [int(n) for n in re.findall(r"(?m)^##\s+(\d+)\.", core)]
        led = [int(n) for n in re.findall(r"(?m)^##\s+(\d+)\.", appendix)]
        self.assertEqual(core_nums, list(range(1, 10)),
                         "core chapter numbering drifted")
        self.assertEqual(led, list(range(1, max(led) + 1)),
                         f"ledger has a gap: {led}")
        # ANCHORED: '### 53. …' must NOT satisfy a '## 53. …' claim. An unanchored
        # substring check passes on a demoted heading (the #120 lesson).
        self.assertRegex(
            appendix,
            r"(?m)^## 53\. Xenopolitics after the NHI Crisis \(#187\)$",
            "§53 is missing or has been demoted below the ledger's top level",
        )

    def test_the_chapter_is_linked_from_the_rulebook(self) -> None:
        """A chapter nobody links is a chapter nobody reads.

        The chapter is linked from §53 (the pointer) and from the §36.9 table. A blanket
        'is the filename present' check is too weak: the §36.9 row alone satisfies it, so
        breaking the §53 pointer would go unnoticed. Assert the §53 SITE specifically.
        """
        # isolate the §53 chapter body in the ledger
        _, appendix = self.rb.split(MARKER, 1)
        m = re.search(r"(?ms)^## 53\. .*?(?=^## \d+\. |\Z)", appendix)
        if m is None:
            self.fail("ledger §53 chapter not found")
        self.assertIn("rulebook/15_XENOPOLITICS.md", m.group(0),
                      "§53 does not point at the modular chapter")

    def test_the_chapter_is_linked_from_the_reference_table(self) -> None:
        row_area = self.rb[self.rb.find("### 36.9"): self.rb.find("### 36.10")]
        self.assertIn("15_XENOPOLITICS.md", row_area,
                      "the §36.9 reference table does not list the chapter")


class CanonReconciliationTests(unittest.TestCase):
    """The chapter must hold BOTH halves of the reading it proposes."""

    def setUp(self) -> None:
        self.ch_flat = flat(read(CHAPTER))

    def test_it_keeps_the_no_fall_invariant(self) -> None:
        """Canon says the Fall has not happened; the chapter must not erase that."""
        self.assertRegex(
            self.ch_flat,
            r"[Tt]he Fall,? in the Eclipse Phase sense,? \*{0,2}has not happened",
            "the chapter no longer restates the no-Fall invariant",
        )

    def test_it_states_the_catastrophe_scale(self) -> None:
        """It must not soften the event into a non-event either."""
        self.assertRegex(
            self.ch_flat,
            r"near-extinction event",
            "the chapter no longer states the near-extinction scale",
        )
        self.assertIn("regional holocausts", self.ch_flat)
        # COUNT, don't just detect: the phrase occurs twice (the thesis blockquote and the
        # sequence list). Softening only one occurrence left the other behind and passed a
        # presence test, so the count is asserted instead.
        raw = read(CHAPTER)
        self.assertEqual(
            raw.count("near-extinction"), 2,
            "the near-extinction framing must survive in BOTH the thesis and the sequence",
        )

    def test_it_cites_the_canon_it_reconciles(self) -> None:
        self.assertIn("§33.28", self.ch_flat)
        self.assertIn("§33.1", self.ch_flat)


class PremiseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ch_flat = flat(read(CHAPTER))

    def test_both_factions_want_a_living_earth(self) -> None:
        # 'Both' is capitalised in the blockquote; flat() preserves case.
        self.assertRegex(
            self.ch_flat,
            r"[Bb]oth major NHI blocs want Earth to remain a living world",
            "the shared-interest premise is missing",
        )

    def test_the_moral_axis_survives(self) -> None:
        """Saving lives and coercive goals must coexist in the same actor."""
        self.assertRegex(
            self.ch_flat,
            r"save millions of lives and still hold deeply coercive long-term goals",
            "the moral-axis sentence is missing",
        )

    def test_neither_faction_is_flattened(self) -> None:
        # the Confederacy is explicitly not simply good; Orion is not demonised
        self.assertIn("not be treated as \"the good aliens\"", self.ch_flat)
        self.assertIn("genuine relief and reconstruction", self.ch_flat)

    def test_the_sovereignty_question_is_present(self) -> None:
        self.assertRegex(
            self.ch_flat,
            r"Who has legitimate sovereignty over Earth",
        )

    def test_the_hybrid_panic_and_the_paranoia_problem_are_present(self) -> None:
        self.assertIn("hybrid panic", self.ch_flat)
        self.assertRegex(self.ch_flat, r"xenophobic paranoia")
        self.assertRegex(self.ch_flat, r"all hybrids Orion-aligned")


class AmbiguityPreservationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ch_flat = flat(read(CHAPTER))

    def test_the_faction_reality_question_stays_open(self) -> None:
        """The chapter must present the divide WITHOUT settling it."""
        self.assertIn("whether **the two factions are genuinely distinct**", self.ch_flat)
        # and it must say plainly that it is unresolved / structural
        self.assertRegex(
            self.ch_flat,
            r"investigator cannot resolve it|stays contested|resolves none of this",
        )

    def test_it_does_not_assert_the_factions_are_identical(self) -> None:
        """A later edit must not 'answer' the question in either direction."""
        for verdict in ("are the same faction", "are one and the same",
                        "do not actually exist", "are proven real enemies"):
            with self.subTest(verdict=verdict):
                self.assertNotIn(verdict, self.ch_flat)

    def test_the_religious_movement_questions_stay_questions(self) -> None:
        self.assertRegex(self.ch_flat, r"Is this spontaneous religious conversion")
        self.assertRegex(self.ch_flat, r"memetic or psychic influence")


class NoMechanicsTests(unittest.TestCase):
    #: tokens that must not appear as a *definition*. 'stat blocks' appears in this chapter
    #: only inside explicit prohibitions ("No faction stat blocks", "no … stat blocks"), so
    #: the check is negation-aware rather than a bare substring test.
    FORBIDDEN = ("2d6", "1d10", "d100", "damage:", "hit points", "initiative",
                 "price:", "cost:", "reputation points", "stat block")
    _NEGATORS = ("no ", "not ", "never ", "defines no", "without ", "remain")

    def test_the_chapter_defines_no_mechanics(self) -> None:
        for tok in self.FORBIDDEN:
            with self.subTest(token=tok):
                for line in read(CHAPTER).split("\n"):
                    low = line.lower()
                    if tok not in low:
                        continue
                    if any(n in low for n in self._NEGATORS):
                        continue          # a prohibition, not a definition
                    self.fail(f"#187 chapter defines {tok!r}: {line.strip()[:90]}")

    def test_the_chapter_states_its_no_mechanics_bound(self) -> None:
        # strip markdown backticks: the chapter writes `AGENTS.md`, not AGENTS.md
        ch = flat(read(CHAPTER)).lower().replace("`", "")
        self.assertIn("defines no mechanics", ch)
        self.assertIn("agents.md §4", ch)

    def test_no_concrete_year(self) -> None:
        years = [y for y in re.findall(r"\b(?:19|20)\d{2}\b", read(CHAPTER))
                 if y != "20XX"]
        self.assertEqual(years, [], f"#187 chapter assigns concrete years: {years}")


if __name__ == "__main__":
    unittest.main()
