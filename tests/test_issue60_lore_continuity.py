"""Continuity guard for the pre-Fall timeline and the four #60 lore gaps.

Two jobs, in one module because they guard the same property: a continuity fact
stated in one canonical document must not be silently missing from the other.

1. `docs/PRE_FALL_ALTERNATE_TIMELINE.md` had **no test coverage at all** before
   this module. That is how the stargate canon went missing once already (#73):
   the fact lived in one document and nothing failed when it drifted out of the
   other. The guard below asserts the shared continuity facts appear in BOTH the
   timeline document and the canonical `RULEBOOK.md`.

2. Issue #60's divergence table names two Eclipse Phase concepts that NoöPunk
   carries as *deliberately undecided* rather than mapped -- `Firewall` and
   `TITANs`. The valuable property is not that the words appear; it is that they
   appear **as undecided**. A later contributor resolving them by inventing an
   organisation or a history must fail the build, so the assertions check the
   surrounding claim, not just the token.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"
TIMELINE = ROOT / "docs" / "PRE_FALL_ALTERNATE_TIMELINE.md"


def flat(path: Path) -> str:
    """Whitespace-collapsed text.

    Both documents are hard-wrapped, so a phrase that reads as one string is
    often split across a newline. Only whitespace is collapsed; markdown
    emphasis is left intact because several assertions require it.

    NOTE: collapsing newlines destroys line anchors, so a ``^``-anchored regex
    will NOT match against this. Extract sections from the RAW text (see
    ``section_of``) and flatten only the extracted body.
    """
    return " ".join(path.read_text(encoding="utf-8").split())


def raw(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_of(document: Path, heading: str) -> str:
    """Return the flattened body of a `##`/`###`/`####` section.

    Extracts from RAW text (so the line anchor works), then collapses whitespace.
    Scoping matters: a document-wide substring assertion is satisfied by the same
    phrase appearing anywhere else in the file, which is how a guard reports
    success after the passage it meant to protect was deleted.
    """
    text = raw(document)
    match = re.search(rf"^#{{2,4}}\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if match is None:
        raise AssertionError(f"section not found: {heading!r}")
    rest = text[match.end():]
    nxt = re.search(r"^#{2,4}\s", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(body.split())


class PreFallContinuityTests(unittest.TestCase):
    """Continuity facts must be present in both canonical documents."""

    def setUp(self) -> None:
        self.book = flat(RULEBOOK)
        self.timeline = flat(TIMELINE)

    def test_timeline_document_exists_and_is_not_empty(self) -> None:
        self.assertTrue(TIMELINE.exists(), "docs/PRE_FALL_ALTERNATE_TIMELINE.md is missing")
        self.assertGreater(len(self.timeline), 500, "timeline doc is suspiciously short")

    def test_timeline_doc_has_a_guard_at_all(self) -> None:
        """Before this module the timeline document had no test coverage.

        Asserting the document is reachable from the suite makes the missing-guard
        regression itself detectable: deleting this module removes the coverage and
        the suite count drops.
        """
        # The title capitalises "Pre-Fall"; the body lowercase-hyphenates it.
        self.assertRegex(self.timeline, r"[Pp]re-[Ff]all")
        self.assertIn("canonical Fall is not predetermined", self.timeline)

    def test_the_timeline_premise_section_states_the_pre_fall_boundary(self) -> None:
        """Scoped to the premise section, not the document.

        A document-wide check passes on the TITLE alone ("Pre-Fall Eclipse Phase
        Alternate Timeline"), so deleting the actual premise sentence left the guard
        green -- a false "MISSED" that sabotage testing caught.
        """
        premise = section_of(TIMELINE, "Canonical premise")
        self.assertRegex(
            premise,
            r"[Pp]re-[Ff]all|before the Fall",
            "the timeline's premise section no longer states the pre-Fall boundary",
        )
        self.assertRegex(
            premise,
            r"Fall:?\**\s*has not happened|not happened",
            "the premise section no longer states that the Fall has not happened",
        )

    def test_both_documents_state_the_pre_fall_premise(self) -> None:
        for label, text in (("timeline", self.timeline), ("rulebook", self.book)):
            with self.subTest(document=label):
                self.assertRegex(
                    text,
                    r"[Pp]re-[Ff]all",
                    f"{label} does not state the pre-Fall premise",
                )

    def test_both_documents_deny_a_determined_fall(self) -> None:
        for label, text in (("timeline", self.timeline), ("rulebook", self.book)):
            with self.subTest(document=label):
                self.assertTrue(
                    re.search(
                        r"(Fall|fall) (has )?not (happened|occurred)"
                        r"|not predetermined"
                        r"|Nothing comparable to the canonical[^.]{0,40}Fall has happened",
                        text,
                    ),
                    f"{label} does not deny that the canonical Fall has occurred",
                )

    def test_both_documents_carry_the_neofeudal_axis(self) -> None:
        """The #60 theme 'neofeudal cybercapitalism vs the Multitude' — gap 3.

        It lived in the timeline doc and paradigm_shifts.yaml but not in the
        canonical ledger, which is exactly the drift this guard exists to stop.
        """
        for label, text in (("timeline", self.timeline), ("rulebook", self.book)):
            with self.subTest(document=label):
                self.assertRegex(
                    text.lower(),
                    r"neofeudal",
                    f"{label} does not carry the neofeudal/Multitude axis",
                )
                self.assertRegex(
                    text,
                    r"Multitude",
                    f"{label} does not name the Multitude",
                )


class ConversionGapTests(unittest.TestCase):
    """The two #60 concepts carried as deliberately undecided — gaps 1 and 2."""

    def setUp(self) -> None:
        self.mapping = section_of(RULEBOOK, "9. Characters and identity")

    def test_firewall_is_recorded_as_undecided(self) -> None:
        self.assertIn("Firewall", self.mapping, "Firewall is absent from the mapping section")
        # The decision is the openness: it must not be described as formed.
        firewall_block = re.search(
            r"\*\*Firewall\.\*\*(.{0,600})", self.mapping, re.DOTALL
        )
        if firewall_block is None:
            self.fail("no Firewall paragraph in the mapping section")
        body = firewall_block.group(1)
        self.assertRegex(
            body,
            r"may \*\*exist differently, emerge\s*differently, or not yet exist\*\*"
            r"|deliberately undecided",
            "Firewall is not recorded as undecided",
        )
        for settled in ("Firewall was founded", "Firewall exists and", "Firewall is organised"):
            self.assertNotIn(settled, body, f"Firewall reads as settled: {settled!r}")

    def test_titans_are_recorded_as_undecided(self) -> None:
        self.assertIn("TITANs", self.mapping, "TITANs absent from the mapping section")
        titans_block = re.search(r"\*\*TITANs\.\*\*(.{0,700})", self.mapping, re.DOTALL)
        if titans_block is None:
            self.fail("no TITANs paragraph in the mapping section")
        body = titans_block.group(1)
        self.assertRegex(
            body,
            r"not decided|\*\*not\*\* decided|deliberately undecided",
            "TITANs is not recorded as undecided",
        )
        # The pre-Fall relationship must be stated, not assumed away.
        self.assertRegex(
            body,
            r"pre-Fall",
            "the TITAN paragraph omits the pre-Fall relationship the issue asks for",
        )

    def test_the_two_ambiguous_names_are_distinguished(self) -> None:
        """'Great Firewall' (China) is a different thing from EP's Firewall."""
        self.assertIn("Great Firewall", self.mapping)
        self.assertRegex(
            self.mapping,
            r"unrelated use of the words|not this organisation",
            "the mapping does not distinguish EP Firewall from the Great Firewall",
        )


class WendtAttributionTests(unittest.TestCase):
    """Gap 4: §33.2 must name Wendt, as its sibling inspiration sections do."""

    def setUp(self) -> None:
        self.book = flat(RULEBOOK)
        self.s332 = section_of(RULEBOOK, "33.2 Ontological shock and human division")

    def test_wendt_is_named_in_the_division_section(self) -> None:
        # Anchor on the attribution SENTENCE, not the bare surname: §33.2 also
        # cross-references "(§34.5, §33.17)" in the same paragraph, so a bare
        # "Wendt" in the section is satisfied by a dangling reference even after
        # the attribution itself is deleted (found by sabotage testing).
        self.assertRegex(
            self.s332,
            r"draws this specifically from \*\*Alexander Wendt",
            "§33.2 does not attribute the fragmentation thesis to Wendt",
        )

    def test_the_attribution_carries_the_disclosure_politics_idea(self) -> None:
        self.assertRegex(
            self.s332,
            r"no single shared human reaction|politics of UFO",
            "§33.2 names Wendt without his idea (the issue asks for the disclosure politics)",
        )

    def test_the_real_scholar_is_not_presented_as_established_science(self) -> None:
        """The section names a real scholar; the framing must not read as a claim.

        The house convention for naming real theorists is the one §33.24 and §34.5
        use: the work is an inspiration for a fictional setting, not an assertion
        that the theory is true.
        """
        self.assertRegex(
            self.s332,
            r"fictional|not (a claim|presented as|treated as)",
            "§33.2 names a real scholar without the fictional/inspiration framing",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
