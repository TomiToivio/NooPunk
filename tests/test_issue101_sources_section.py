"""Guard the sources/influences section, and check cross-references semantically.

Two failures this module exists to prevent, both observed in this file:

1. **The sources section was delivered twice and left unguarded.** Issue #99 was landed by
   two parallel sessions eight minutes apart (``24a63b1`` added ``## 35. Sources…``,
   ``7865e0f`` added ``## 38. Living sources…``). Both were on ``main``; neither was a
   revert. The AI triad, the 10% estimate and the maintenance-rule sentence were each
   written out twice, and **no test referenced either section**, so a future stale-branch
   clobber would have deleted it silently — the same failure mode as #81/#100.

2. **A dangling-reference check that only proves EXISTENCE misses a WRONG TARGET.**
   ``tests/test_theory_sections_survive.py`` asserts every cited ``§n.m`` resolves to some
   heading. After the #99 renumber, line 1135 cited ``§35.5`` for Wendt's
   consciousness-theory inspiration — and ``§35.5`` *exists*, but it is "Role-playing
   games". The real target is ``§36.5``. CI stayed green because existence is not
   correctness.

The semantic check below scores the overlap between the citing sentence and the cited
section, and fails when a citation resolves to a section with nothing in common.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = "RULEBOOK.md"

#: Anchored by heading text — the section number has already been reused once in this file.
SOURCES_HEADING = "Sources, recommended reading, and influences"

#: The five categories issue #99 requires.
REQUIRED_CATEGORIES = (
    "non-fiction books",
    "fiction books",
    "movies",
    "role-playing games",
    "computer games",
)

#: The AI ideological triad, which must exist exactly once after the merge.
TRIAD = (
    "If Anyone Builds It",
    "Singularity Is Nearer",
    "The AI Con",
)


def read() -> str:
    return (ROOT / RULEBOOK).read_text(encoding="utf-8")


def flatten(text: str) -> str:
    """Whitespace-collapsed, emphasis-stripped, lowercased.

    Emphasis removal is not cosmetic: the document writes key terms in ``**bold**`` and
    italicised titles in ``*asterisks*``, so an assertion written against rendered prose
    fails on correct text.

    Blockquote markers are removed too. The maintenance rule is a blockquote wrapped over
    two lines, so the raw text reads ``... add it to\\n> this list.`` — without stripping
    ``>`` the phrase "add it to this list" is broken by the marker and never matches.
    """
    return " ".join(re.sub(r"[*`_>]", " ", text).split()).casefold()


def sources_sections() -> list[tuple[str, str]]:
    """Every top-level section that IS the #99 delivery (a recommended-reading list).

    Anchored on the phrase the issue itself uses — ``recommended reading`` — not on the
    loose word "sources", which also matches ``## 11. Pools and expendable resources`` and
    the theory bibliography ``## 37. Theoretical sources and inspirations``. Neither of
    those is the #99 deliverable, so a loose match would report a false duplicate.

    The heading pattern accepts a LETTERED number (``## 35a.``) as well as a plain one:
    a duplicate delivery was observed as a new section, and pinning only ``\\d+\\.`` would
    let a suffixed copy slip through undetected.
    """
    text = read()
    found = []
    for m in re.finditer(r"(?m)^## (\d+[a-z]?)\. (.+)$", text):
        if re.search(r"recommended reading", m.group(2), re.IGNORECASE):
            nxt = re.search(r"(?m)^## \d+[a-z]?\. ", text[m.end():])
            body = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]
            found.append((m.group(0).strip(), body))
    return found


def the_section() -> str:
    """The single sources section, failing loudly if there is not exactly one."""
    found = sources_sections()
    assert len(found) == 1, (
        f"expected exactly ONE sources/reading section, found {len(found)}: "
        f"{[h for h, _ in found]}"
    )
    return found[0][1]


def subsection(body: str, heading: str) -> str:
    """Body of a ``###``/``####`` subsection, scoped so a document-wide phrase cannot satisfy it."""
    m = re.search(rf"(?m)^#{{3,4}}\s+[^\n]*{re.escape(heading)}[^\n]*\n", body)
    if not m:
        return ""
    nxt = re.search(r"(?m)^#{3,4} ", body[m.end():])
    return body[m.end(): m.end() + nxt.start()] if nxt else body[m.end():]


STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "not", "its", "his", "her",
    "are", "was", "were", "has", "have", "had", "but", "they", "their", "than", "then",
    "into", "over", "only", "also", "such", "when", "which", "what", "who", "whom",
    "one", "two", "three", "being", "been", "more", "most", "other", "others", "some",
    "any", "each", "both", "all", "may", "can", "will", "would", "should", "must",
    "about", "above", "after", "again", "against", "because", "before", "between",
    "during", "through", "under", "while", "within", "without", "does", "did", "done",
    "section", "sections", "see", "it", "as", "at", "by", "in", "of", "on", "or",
    "to", "is", "be", "an", "a",
}


def content_words(text: str) -> set[str]:
    words = re.findall(r"[a-zäöüß][a-zäöüß'-]{2,}", text.casefold())
    return {w for w in words if w not in STOPWORDS and len(w) > 3}


class SourcesSectionTests(unittest.TestCase):
    """The #99 deliverable: one living sources section, at the end, with its categories."""

    def test_there_is_exactly_one_sources_section(self) -> None:
        found = sources_sections()
        self.assertEqual(
            len(found), 1,
            "issue #99 was landed twice and left two sources sections; they must stay "
            f"merged into one. Found: {[h for h, _ in found]}",
        )

    def test_the_sources_section_keeps_its_categories(self) -> None:
        """Each of the five requested categories must exist as its own subsection.

        Checked at HEADING level, not as a loose phrase: a passing phrase match would
        survive a heading being renamed or deleted, which is the drift this guards.
        """
        body = the_section()
        headings = [h.strip().lower() for h in re.findall(r"(?m)^#{3,4}\s+(.+)$", body)]
        self.assertTrue(headings, "the sources section has no subsections")
        expected = {
            "non-fiction books": ("non-fiction",),
            "fiction books": ("fiction",),
            "movies": ("movie", "tv", "television"),
            "role-playing games": ("role-playing", "rpg"),
            "computer games": ("computer game",),
        }
        for label, needles in expected.items():
            with self.subTest(category=label):
                self.assertTrue(
                    any(any(n in h for n in needles) for h in headings),
                    f"no subsection heading for {label!r}; headings are {headings}",
                )

    def test_the_ai_ideological_triad_appears_exactly_once_in_the_sources_section(self) -> None:
        """The duplication is what #101 removed; it must not come back.

        Scoped to the sources section itself. Other sections legitimately name these works:
        §2.2 uses the same three books as the AI-spectrum map, and the §37 theoretical
        bibliography lists Kurzweil's books. Counting document-wide would fail on correct
        text, which is exactly the over-strict-guard trap.
        """
        body = flatten(the_section())
        for work in TRIAD:
            with self.subTest(work=work):
                self.assertIn(work.casefold(), body, f"the AI triad lost {work!r}")

    def test_the_sources_section_is_not_duplicated(self) -> None:
        """Exactly one recommended-reading section may exist."""
        found = sources_sections()
        self.assertEqual(len(found), 1, f"duplicate sources sections: {[h for h, _ in found]}")

    def test_the_maintenance_rule_is_present_once(self) -> None:
        """The instruction #99 asked to add verbatim must be present, complete, and single.

        Checking only the opening clause let a mutation pass that deleted the operative
        half ("add it to this list") while leaving the subject intact — found by sabotage.
        """
        #: The whole instruction, whitespace-collapsed. The blockquote marker and the
        #: hard wrap are normalised away by flatten().
        sentence = (
            "whenever a new work becomes a meaningful source or influence for noöpunk, "
            "add it to this list"
        )
        body = flatten(the_section())
        self.assertIn(sentence, body, "the maintenance rule is incomplete or missing")
        self.assertEqual(
            flatten(read()).count(sentence), 1,
            "the maintenance-rule sentence is duplicated or incomplete",
        )

    def test_the_sources_section_is_the_last_top_level_section(self) -> None:
        """#99 asked for it at the END; a later insert must not bury it."""
        numbers = re.findall(r"(?m)^## (\d+)\. ", read())
        headings = re.findall(r"(?m)^## \d+\. (.+)$", read())
        self.assertRegex(headings[-1], r"sources|recommended reading")
        self.assertEqual(numbers, [str(n) for n in range(1, len(numbers) + 1)],
                         "top-level numbering is no longer contiguous")

    def test_the_epistemic_caveat_survives(self) -> None:
        """The section may canonize contested claims; it must say so."""
        body = flatten(the_section())
        self.assertRegex(
            body,
            r"not mean (that )?(its|the) claims are established|established scientific fact",
            "the sources section lost its epistemic-care caveat",
        )


class CrossReferenceSemanticsTests(unittest.TestCase):
    """A citation must resolve to a section that is actually ABOUT the citing claim."""

    #: Section references, INCLUDING lettered subsections (``§33.28b``). The naive
    #: ``\\d+(\\.\\d+)*`` pattern truncates a trailing letter, capturing ``33.28`` from
    #: ``§33.28b`` — and because ``§33.28`` exists, a dangling lettered reference passes.
    #: That is exactly how the existing ``test_no_internal_dangling_section_reference``
    #: stayed green while this file cited the (since-deleted) ``§33.28b``.
    REF_RE = re.compile(r"§\s*(\d+(?:\.\d+)*(?:[a-z])?)")

    #: Minimum content-word overlap for a `§x.y` citation to count as pointing at the
    #: right place. Calibrated on the real file: correct citations score far above this.
    MIN_OVERLAP = 1

    def _headings(self) -> set[str]:
        return set(re.findall(r"(?m)^#{2,4}\s+(\d+(?:\.\d+)*[a-z]?)", read()))

    def _targets(self) -> dict[str, str]:
        text = read()
        out = {}
        for m in re.finditer(r"(?m)^#{2,4}\s+(\d+(?:\.\d+)*[a-z]?)\s+(.*)$", text):
            start = m.end()
            nxt = re.search(r"(?m)^#{2,4}\s", text[start:])
            out[m.group(1)] = text[start: start + nxt.start()] if nxt else text[start:]
        return out

    def test_every_citation_resolves_including_lettered_subsections(self) -> None:
        """``§33.28b`` must not be satisfied by ``§33.28``."""
        headings = self._headings()
        for ref in sorted(set(self.REF_RE.findall(read()))):
            with self.subTest(ref=ref):
                self.assertIn(ref, headings, f"§{ref} is cited but no heading defines it")

    def test_no_citation_points_at_an_archived_only_passage(self) -> None:
        """A citation must not claim content this file no longer contains.

        The §9 Firewall note claimed '"Great Firewall" does appear in §33.27' after #98 had
        refactored that passage out of the rulebook and into ``docs/archive/``. The section
        number still existed, so no existence check could catch it.

        The check is anchored on whichever wording the note currently uses, so it keeps
        working after the claim is rewritten to say the passage is *archived*.
        """
        text = read()
        for ref, phrase in (("33.27", "Great Firewall"),):
            #: The note is present in either its old (false) or new (archived) form.
            if not re.search(r"Great\s+Firewall\"?\s*(?:does appear in|also name)", text):
                continue  # claim removed entirely; nothing to check
            with self.subTest(ref=ref, phrase=phrase):
                m = re.search(rf"(?m)^#{{2,4}}\s+{re.escape(ref)}\s+(.*)$", text)
                self.assertIsNotNone(m, f"§{ref} not found")
                assert m is not None
                rest = text[m.end():]
                nxt = re.search(r"(?m)^#{2,4}\s", rest)
                body = rest[: nxt.start()] if nxt else rest
                # If the note ASSERTS the phrase lives in that section, the section must
                # actually contain it. The archived form says the passage is NOT here, and
                # is therefore exempt.
                asserts_present = "does appear in" in text
                if asserts_present:
                    self.assertIn(
                        phrase, body,
                        f"the rulebook attributes {phrase!r} to §{ref}, but that section "
                        "does not contain it — the passage was moved or archived",
                    )

    def test_the_firewall_note_does_not_attribute_archived_text_to_a_live_section(self) -> None:
        """The specific false claim #101 removed must not come back."""
        text = read()
        self.assertNotRegex(
            text,
            r"Great\s+Firewall\"?\s+does appear in\s+§\d",
            "the rulebook again claims the Great Firewall passage is in a live section; "
            "#98 archived it, so the claim is false",
        )

    def test_every_dotted_citation_resolves_to_a_related_section(self) -> None:
        """Citations must resolve, including lettered subsections.

        NOTE on scope, learned the hard way: a bag-of-words overlap check was tried here
        and **rejected**. It flagged five citations that are correct (§33.6, §33.6b,
        §36.8, §36.1, §16.2) because legitimate citations are often deliberate pointers
        ("the background lives in §33.6"), which share little vocabulary with the target.
        A guard that reds main on correct text is worse than no guard. The checks that
        survived are precise: exact resolution (below), the archived-passage check, and
        the two specific regressions this issue fixed.
        """
        text = read()
        targets = self._targets()
        checked = 0
        for m in re.finditer(r"§\s*(\d+\.\d+(?:\.\d+)*[a-z]?)", text):
            ref = m.group(1)
            with self.subTest(ref=ref):
                self.assertIn(ref, targets, f"§{ref} is cited but not defined")
                checked += 1
        self.assertGreater(checked, 5, "expected several dotted citations to check")

    def test_the_wendt_citation_points_at_the_psychic_layer_section(self) -> None:
        """The exact defect #101 fixed: §35.5 was 'Role-playing games'."""
        text = read()
        # NOTE the citation is a PAIR, "(§36.5, §33.17)", so the first ref is followed by
        # a comma, not a closing paren. Requiring ")" straight after the number silently
        # matched nothing.
        m = re.search(
            r"Wendt's \*Quantum\s+Mind and Social Science\*[^()]*?\(§(\d+\.\d+)", text, re.DOTALL
        )
        self.assertIsNotNone(m, "the Wendt consciousness-theory citation is gone")
        assert m is not None
        ref = m.group(1)
        heading_m = re.search(rf"(?m)^#{{2,4}}\s+{re.escape(ref)}\s+(.+)$", text)
        self.assertIsNotNone(heading_m, f"§{ref} is cited but has no heading")
        assert heading_m is not None
        heading = heading_m.group(1)
        self.assertRegex(
            heading, r"(?i)psychic",
            f"the Wendt citation points at §{ref} ({heading!r}), which is not the "
            "consciousness-theory section",
        )
        self.assertNotRegex(heading, r"(?i)role-playing",
                            "the citation resolves to the RPG list")


if __name__ == "__main__":
    unittest.main(verbosity=2)
