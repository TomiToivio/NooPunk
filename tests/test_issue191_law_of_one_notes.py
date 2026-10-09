# -*- coding: utf-8 -*-
"""Structure guard for the #191 Law-of-One research notes and the chapter they feed.

Issue #191 is a *living lore tracker* with a source discipline that is easy to lose on the
next edit: every element carries (A) a Ra claim with a `session.question` citation, (B) the
NoöPunk reading, and (C) what the source does not support; and the deliverable must not
smuggle in mechanics, because `AGENTS.md` §4 reserves psionic mechanics, derived statistics
and equipment statistics.

This file guards three properties, all of which a well-meaning rewrite can quietly destroy:

1. **Citation presence** — the notes doc cites the primary text in `session.question` form.
   A notes file that loses its citations is an opinion piece wearing a source's name.
2. **Three-register separation** — the (A)/(B)/(C) labels exist and are used repeatedly, not
   once in a header. A document that states one label and then writes a flowing argument has
   lost the discipline it claims.
3. **The no-mechanics bound** — neither the notes nor the chapter introduces a numeric
   rating where the source and the author's granularity ("light description, not full stats")
   forbid one.

Assertion shapes follow `references/structure-guard-assertion-discipline.md`: each distinct
fact is asserted separately (never as one alternation), the count of a required structure is
pinned (a presence check cannot see an addition or a deletion of one of N), and the
chapter's own pointer into the ledger is anchored at its site.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "research" / "LAW_OF_ONE_LORE_NOTES.md"
CHAPTER = ROOT / "rulebook" / "17_NOETIC_PRACTICE_AND_CRYSTAL_TECH.md"
RULEBOOK = ROOT / "RULEBOOK.md"

#: `session.question` — the house citation format. A bare integer is not a citation, so the
#: pattern requires the dotted form (29.30, 12.21) and a bounded session number.
_CITATION = re.compile(r"\b(\d{1,3})\.(\d{1,3})\b")


def _flat(path: Path) -> str:
    """Whitespace-collapsed, blockquote-marker-stripped text — for prose assertions."""
    lines = [re.sub(r"^\s*>\s?", "", ln) for ln in path.read_text(encoding="utf-8").splitlines()]
    return " ".join(" ".join(lines).split())


def citations(text: str) -> set[str]:
    """Every dotted citation candidate, excluding the years and decimals that are not ones."""
    return {f"{m.group(1)}.{m.group(2)}" for m in _CITATION.finditer(text)}


class LawOfOneNotesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.notes = _flat(NOTES)
        self.chapter = _flat(CHAPTER)
        self.rulebook = RULEBOOK.read_text(encoding="utf-8")

    # ---- 1. the notes exist and cite the primary text -------------------------------

    def test_the_notes_document_exists(self) -> None:
        self.assertTrue(NOTES.is_file(), f"{NOTES} is missing")

    def test_the_notes_cite_the_primary_text_in_session_question_form(self) -> None:
        """The whole point of the tracker is that a claim is traceable to one turn."""
        found = citations(self.notes)
        # The anchors this pass verified directly against lawofone.info.
        for anchor in ("29.30", "29.23", "6.5", "6.8", "12.3", "12.5", "12.9", "12.21",
                       "15.12", "5.2", "42.9", "51.4", "13.16"):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, found, f"the notes no longer cite {anchor}")

    def test_the_notes_carry_many_distinct_citations(self) -> None:
        """One citation would satisfy a presence check; a corpus pass needs a corpus."""
        found = citations(self.notes)
        self.assertGreaterEqual(len(found), 40,
                                f"only {len(found)} distinct citations remain")

    # ---- 2. three-register separation ------------------------------------------------

    def test_the_three_registers_are_declared(self) -> None:
        for label in ("(A) RA CLAIM", "(B) NOÖPUNK READING", "(C) NOT SUPPORTED"):
            with self.subTest(label=label):
                self.assertIn(label, self.notes, f"the {label} register is not declared")

    def test_the_registers_are_used_repeatedly_not_once(self) -> None:
        """A header stating three registers, then one flowing argument, is the failure mode.

        REQUIRED MULTIPLICITY: each register must appear as a working label more than once.
        """
        for label in ("(A)", "(B)", "(C)"):
            with self.subTest(label=label):
                hits = len(re.findall(rf"\({label}\)", self.notes))
                self.assertGreaterEqual(
                    hits, 5, f"register {label} is used only {hits} time(s) — not a discipline")

    def test_the_register_ordering_is_stated(self) -> None:
        """The registers are ranked evidence classes, and the doc says which is which."""
        self.assertIn("what the channeled text actually says", self.notes)
        self.assertIn("the setting's fictional reinterpretation", self.notes)
        self.assertIn("overreach the primary text does not carry", self.notes)

    # ---- 3. the no-mechanics bound ---------------------------------------------------

    def test_the_notes_state_that_the_ra_material_is_not_real_world_evidence(self) -> None:
        self.assertIn("It is not evidence about the real world", self.notes)

    def test_the_notes_flag_the_inferential_gap(self) -> None:
        """The single most important honesty rule in the whole document."""
        self.assertIn("The inferential gap", self.notes)

    def test_the_silicon_ai_seed_is_marked_as_a_noopunk_invention(self) -> None:
        """The honest answer to the seed idea, which a later edit is tempted to 'fix'."""
        self.assertIn("no mineral-to-machine pathway is described anywhere in the corpus",
                      self.notes)
        self.assertIn("is a NoöPunk invention, not a source claim", self.notes)

    def test_the_council_of_saturn_correction_survives(self) -> None:
        """6.8 DOES place the Council at Saturn; a sibling note claimed the text was silent.

        The correction is load-bearing: if a later edit reverts to the sibling's claim, the
        setting loses a citation and gains a false statement about the source. Pin the
        CITATION as well as the quote, or renumbering 6.8 to a session that says no such
        thing leaves the guard green.
        """
        self.assertIn("**6.8**", self.notes)
        self.assertIn("This Council is located in the octave, or eight[h] dimension", self.notes)
        self.assertIn("[corrected]", self.notes)

    def test_no_numeric_power_or_balance_scale_is_introduced(self) -> None:
        """The granularity the author set: light description, not full stats.

        A bare absence check would false-FAIL on the two documents' OWN prohibitions ("no PSI
        point economy", a "balance score" named as a *misreading*). Per
        `references/structure-guard-assertion-discipline.md` the exemption is scoped to the
        **clause** that owns the token, never to a character window: a clause stating a real
        mechanic passes a window scan whenever a negator happens to sit nearby, which is how
        a real mechanic can be smuggled in beside a prohibition.
        """
        for pattern in (r"\bPSI points?\b", r"\benergy[- ]center rating\b", r"\bbalance score\b"):
            with self.subTest(pattern=pattern):
                self._assert_only_ever_denied(self.notes, pattern)
                self._assert_only_ever_denied(self.chapter, pattern)

    #: Words that mark a clause as DENYING or REJECTING the token, not asserting it.
    _DENIAL = (
        "no ", "not ", "nothing", "never", "does not", "do not", "cannot", "without",
        "misreading", "not supported", "rather than", "instead of",
    )

    def _assert_only_ever_denied(self, text: str, pattern: str) -> None:
        """Fail if `pattern` occurs in ANY sentence that does not deny/reject it.

        Judged per SENTENCE, never per character window: the sentence that OWNS the token must
        carry the negation. A real mechanic in its own sentence fails even when an unrelated
        sentence nearby says "no …". The split is on sentence ends only — splitting on `;`
        too would strand a list item from the rejection label that governs it ("**Not
        supported:** …; a "balance score" that grows."), a false FAIL the sweep caught.
        """
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if not re.search(pattern, sentence, flags=re.IGNORECASE):
                continue
            self.assertTrue(
                any(n in sentence.lower() for n in self._DENIAL),
                f"{pattern!r} is asserted in a sentence that does not deny it: {sentence!r}",
            )

    # ---- 4. the chapter's own bounds and linkage -------------------------------------

    def test_the_chapter_exists_and_states_its_no_statistics_bound(self) -> None:
        self.assertIn("It defines no new numeric subsystem", self.chapter)
        self.assertIn("## 17.9 What this chapter deliberately does NOT define", self.chapter)

    def test_the_chapter_keeps_the_operator_precondition(self) -> None:
        """The one rule that defines the crystal technology family."""
        self.assertRegex(
            self.chapter,
            r"No lattice in this setting works without an attuned operator")

    def test_the_chapter_keeps_the_personhood_rule(self) -> None:
        self.assertRegex(
            self.chapter, r"(?i)no classification may settle personhood")

    def test_the_rulebook_links_the_chapter(self) -> None:
        """Assert the link TARGET, not a token also present as the label."""
        self.assertIn("rulebook/17_NOETIC_PRACTICE_AND_CRYSTAL_TECH.md", self.rulebook)

    def test_the_ledger_carries_the_new_section_at_its_own_site(self) -> None:
        """Anchored level + end, so a demotion to ### cannot satisfy it.

        The POINTER must be pinned as the link, not as a bare filename: §54 mentions the
        chapter path twice (the pointer and a later cross-reference), so a filename check is
        satisfied by the second mention after the pointer itself is gutted.
        """
        appendix = self.rulebook.split("# Extended canon and reference material", 1)[1]
        self.assertRegex(appendix, r"(?m)^## 54\. Noetic practice, crystal technology and the craft question \(#191\)$")
        m = re.search(r"(?ms)^## 54\. .*?(?=^## \d+\. |\Z)", appendix)
        self.assertIsNotNone(m, "ledger §54 not found")
        self.assertIn(
            "[`rulebook/17_NOETIC_PRACTICE_AND_CRYSTAL_TECH.md`](rulebook/17_NOETIC_PRACTICE_AND_CRYSTAL_TECH.md)",
            m.group(0) if m else "",
            "ledger §54 does not carry the markdown link that makes it a pointer",
        )

    def test_the_ledger_remains_contiguous(self) -> None:
        appendix = self.rulebook.split("# Extended canon and reference material", 1)[1]
        nums = [int(n) for n in re.findall(r"(?m)^##\s+(\d+)\.", appendix)]
        self.assertEqual(nums, list(range(1, max(nums) + 1)),
                         f"compatibility-ledger numbering has a gap: {nums}")


if __name__ == "__main__":
    unittest.main()
