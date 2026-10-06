"""Guard for issue #145: the genre-mix framing in the rulebook introduction.

Issue #145 asks the introduction to describe NoöPunk as a deliberate mix of several
science-fiction traditions rather than a single subgenre, naming the genre families it
lists, keeping cyberpunk and post-apocalyptic SF foregrounded, and making the point that
these are layers of one setting rather than competing labels.

Before this change ``post-apocalyptic`` and ``post-holocaust`` had **zero** hits in
``RULEBOOK.md``, although #145 names post-apocalyptic / post-holocaust SF as one of the two
most immediately recognizable foundations.

Scope note: ``RULEBOOK.md`` currently carries **two conflicting section-number series**
(``## 1. Introduction to NoöPunk`` ... ``## 8. Psychic Systems``, then a second
``## 1. What this document is`` ...), so ``§1`` is ambiguous. This guard therefore locates
the introduction by its stable HEADING TEXT rather than by number, and asserts the genre
framing inside that section only. A document-wide substring test would be satisfied by the
same words appearing anywhere else in the 5,000-line rulebook.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = "RULEBOOK.md"

INTRO_HEADING = "Introduction to NoöPunk"
GENRE_HEADING = "Genre mix"

#: The genre families issue #145 names, as (label, distinctive phrase present in the prose).
GENRES = (
    ("cyberpunk", "cyberpunk"),
    ("post-apocalyptic / post-holocaust SF", "post-apocalyptic / post-holocaust sf"),
    ("first contact", "first contact"),
    ("alien invasion and infiltration", "alien invasion and infiltration"),
    ("ufological / conspiracy", "ufological conspiracy"),
    ("military / tactical alien contact", "x-com"),
    ("psi-fi / psychotronic", "psi-fi"),
    ("transhumanist / posthuman", "transhumanist and posthuman sf"),
    ("metaphysical / interdimensional", "metaphysical and interdimensional sf"),
    ("weird / occult", "weird and occult sf"),
    ("science-fiction / cosmic / body horror", "body horror"),
)

#: The works the issue names as its examples. All are the author's, none invented here.
NAMED_WORKS = ("Contact", "Arrival", "2001", "The War of the Worlds",
               "X-Files", "Men in Black", "X-COM", "Alien", "The Thing")


def raw(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def flatten(text: str) -> str:
    """Collapse whitespace and strip markdown structural markers, preserving case."""
    return " ".join(re.sub(r"[*`>]", " ", text).split())


def heading_section(text: str, heading: str) -> str:
    """Body of the section whose heading text contains `heading`, at ANY heading level.

    Bound stops at the next heading of the SAME OR HIGHER level. Matching only ``##`` here
    would make the ``#### Genre mix`` subsection leak into ``### 1.2`` and beyond.
    """
    # `{{2,4}}` and NOT `{2,4}`: inside an rf-string a single brace pair is a FORMAT
    # FIELD, so `{2,4}` would compose the literal heading prefix "(2, 4)" and never match.
    pattern = re.compile(rf"(?m)^(#{{2,4}})\s+[^\n]*{re.escape(heading)}[^\n]*$")
    match = pattern.search(text)
    if match is None:
        return ""
    level = len(match.group(1))
    rest = text[match.end():]
    nxt = re.search(rf"(?m)^#{{2,{level}}}\s+", rest)
    return rest[: nxt.start()] if nxt else rest


class GenreMixSectionTests(unittest.TestCase):
    """The genre framing must exist, inside the introduction."""

    def test_the_genre_mix_subsection_exists_in_the_introduction(self) -> None:
        text = raw(RULEBOOK)
        intro = heading_section(text, INTRO_HEADING)
        self.assertTrue(intro, f"{RULEBOOK} no longer has a '{INTRO_HEADING}' section")
        self.assertIn(
            "genre mix",
            flatten(intro).casefold(),
            "the genre-mix passage is not inside the introduction",
        )
        self.assertTrue(
            heading_section(text, GENRE_HEADING),
            f"{RULEBOOK} no longer has a '{GENRE_HEADING}' subsection",
        )

    def test_the_introduction_says_noopunk_is_a_mix_not_one_subgenre(self) -> None:
        body = flatten(heading_section(raw(RULEBOOK), GENRE_HEADING)).casefold()
        self.assertIn("deliberate mix of several science-fiction traditions", body)
        self.assertIn("rather than a member of one subgenre", body)

    def test_every_genre_family_the_issue_names_is_present(self) -> None:
        body = flatten(heading_section(raw(RULEBOOK), GENRE_HEADING)).casefold()
        missing = [label for label, phrase in GENRES if phrase not in body]
        self.assertEqual(missing, [], f"genre families missing from the introduction: {missing}")

    def test_the_issue_summary_line_is_recorded_verbatim(self) -> None:
        body = flatten(heading_section(raw(RULEBOOK), GENRE_HEADING))
        self.assertIn(
            "Cyberpunk + post-apocalyptic SF + first contact + ufological conspiracy "
            "+ psi-fi + weird/interdimensional SF + science-fiction horror.",
            body,
        )

    def test_the_named_example_works_survive(self) -> None:
        body = flatten(heading_section(raw(RULEBOOK), GENRE_HEADING))
        for work in NAMED_WORKS:
            with self.subTest(work=work):
                self.assertIn(work, body)


class ForegroundedFoundationsTests(unittest.TestCase):
    """The acceptance criteria: cyberpunk and post-apocalyptic SF stay foregrounded."""

    def test_cyberpunk_and_post_apocalyptic_are_the_stated_foundations(self) -> None:
        body = flatten(heading_section(raw(RULEBOOK), GENRE_HEADING)).casefold()
        self.assertIn("two most immediately recognizable foundations", body)
        marker = body.index("two most immediately recognizable foundations")
        window = body[marker:marker + 400]
        self.assertIn("cyberpunk", window)
        self.assertIn("post-apocalyptic / post-holocaust sf", window)

    def test_the_genre_families_are_not_listed_as_a_taxonomy(self) -> None:
        """The issue asks for evocative prose, not a 12-item bullet list.

        A bulleted enumeration of the families would satisfy every phrase check above while
        failing the actual acceptance criterion, so assert the absence of a list item per
        genre rather than only the presence of the words.
        """
        body = heading_section(raw(RULEBOOK), GENRE_HEADING)
        bullets = [l for l in body.splitlines() if re.match(r"\s*[-*]\s+\*\*", l)]
        self.assertLessEqual(
            len(bullets), 2,
            f"the genre mix has grown into a taxonomy ({len(bullets)} bullet entries)",
        )


class LayersNotLabelsTests(unittest.TestCase):
    """Issue #145: the genres describe layers of one setting, not competing labels."""

    def test_the_genres_are_layers_of_one_setting(self) -> None:
        body = flatten(heading_section(raw(RULEBOOK), GENRE_HEADING)).casefold()
        self.assertIn("layers of one setting, not competing labels", body)

    def test_the_cross_genre_scenario_example_survives(self) -> None:
        """All four escalation beats AND their order.

        Asserting the beats as a set let a mutation drop the X-COM step and still pass on
        the other three; the point of the sentence is the progression, so assert the
        sequence, not merely the vocabulary.
        """
        body = flatten(heading_section(raw(RULEBOOK), GENRE_HEADING)).casefold()
        for beat in ("begin as cyberpunk", "x-files", "x-com", "cosmic-horror"):
            with self.subTest(beat=beat):
                self.assertIn(beat, body)
        # Assert the escalation IN ORDER, on the sentence that carries it. Scoping matters:
        # "x-files" and "x-com" also appear earlier as genre names, so positions taken over
        # the whole section do not describe the progression.
        start = body.index("a scenario can begin as cyberpunk")
        escalation = body[start:start + 260]
        positions = [escalation.index(b) for b in
                     ("begin as cyberpunk", "x-files", "x-com", "cosmic-horror")]
        self.assertEqual(positions, sorted(positions),
                         "the cross-genre escalation lost its order")
        self.assertIn("intentionally crosses genre boundaries", body)


class NoInventionTests(unittest.TestCase):
    """The passage must not import lore or mechanics the issue did not ask for."""

    def test_no_mechanics_smuggled_into_the_introduction(self) -> None:
        body = flatten(heading_section(raw(RULEBOOK), GENRE_HEADING)).casefold()
        for mechanic in ("1d10", "2d6", "-100", "dice", "skill check", "difficulty value"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, body)

    #: The two sentences that carry the framing. A second copy anywhere is the fork defect.
    SINGLE_TELLING = (
        ("the mix framing",
         "NoöPunk is a deliberate mix of several science-fiction traditions "
         "rather than a member of one subgenre."),
        ("the genre summary line",
         "Cyberpunk + post-apocalyptic SF + first contact + ufological conspiracy "
         "+ psi-fi + weird/interdimensional SF + science-fiction horror."),
    )

    def test_each_framing_sentence_is_told_exactly_once(self) -> None:
        """A count check, not a presence check.

        `assertIn` passes happily with two tellings of the same fact, which is exactly how a
        canon forks into two accounts that later drift apart. Measured on the whole document
        so a duplicate pasted into a neighbouring section is caught, not just one in §1.1.
        """
        text = flatten(raw(RULEBOOK))
        for label, sentence in self.SINGLE_TELLING:
            with self.subTest(sentence=label):
                hits = text.count(sentence)
                self.assertEqual(
                    hits, 1,
                    f"{label} is told {hits} times; expected exactly one telling",
                )

    #: Sections the genre framing must NOT leak into: §1's siblings and the §2 statement.
    NEIGHBOURING_SECTIONS = (
        "Social science inspiration",
        "The paradigm shifts",
        "Current project description",
    )

    def test_the_genre_framing_stays_out_of_the_neighbouring_sections(self) -> None:
        """One telling, in §1.1.

        The genre framing belongs to the introduction. Copying it into a neighbouring
        section forks the canon, so assert it ABSENT from each neighbour rather than only
        present once document-wide -- a duplicate placed beside §1.2 would otherwise count
        as the single telling.
        """
        text = raw(RULEBOOK)
        for heading in self.NEIGHBOURING_SECTIONS:
            body = flatten(heading_section(text, heading)).casefold()
            with self.subTest(section=heading):
                self.assertTrue(body, f"{heading!r} section not found")
                for forbidden in ("genre mix",
                                  "deliberate mix of several science-fiction traditions",
                                  "body horror",
                                  "ufological conspiracy"):
                    self.assertNotIn(forbidden, body,
                                     f"the genre framing leaked into {heading!r}")


if __name__ == "__main__":
    unittest.main()
