"""Acceptance guard for issue #197 §2: UNSA identity, institutional history and diplomacy.

The issue directs a specific canon fact — the agency's official expansion — and the canon
carried the wrong one ("United Nations Security Agency"). Four older guards pinned that
string, so the rename lands here *with* those guards re-baselined onto the new fact rather
than deleted.

Assertion discipline (per the content-line skill):

* the official expansion and the former name are **canon constants**, so exactness IS the
  fact and they are matched literally;
* everything else is **prose**, so it is matched with narrow regexes against a
  **whitespace-flattened** copy — the rulebook hard-wraps at ~90 columns, and a multi-word
  needle that spans a line break matches nothing while looking perfectly correct;
* absence checks run over the canon prose with the `## 27. Change ledger` span excluded,
  because the ledger legitimately quotes superseded tokens.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
SOCIAL = (ROOT / "rulebook" / "4_SOCIAL.md").read_text(encoding="utf-8")
FACTIONS = (ROOT / "FACTIONS.md").read_text(encoding="utf-8")
XENO = (ROOT / "rulebook" / "15_XENOPOLITICS.md").read_text(encoding="utf-8")
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")

OFFICIAL = "United Nations Security Administration"
FORMER = "UN X-Risk Administration"
OLD_OFFICIAL = "United Nations Security Agency"
OLD_FORMER = "UN X-Risk Agency"


def _flat(text: str) -> str:
    """Collapse all whitespace, so a hard-wrapped sentence is still one string."""
    return re.sub(r"\s+", " ", text).strip()


def _canon_prose(document: str) -> str:
    """Canonical prose, excluding the Change ledger section (it quotes superseded tokens)."""
    before, sep, rest = document.partition("## 27. Change ledger")
    if not sep:
        return document
    after = rest.partition("\n## ")[2]
    return before + after


def _section(document: str, number: int) -> str:
    """Body of top-level section ``## <number>.``, sliced to the next ``## ``.

    Anchored on the line start and on the dot, so ``## 38.`` cannot be satisfied by a
    demoted ``### 38.`` or by ``## 380.``.
    """
    match = re.search(rf"(?m)^## {number}\.[ \t]", document)
    if match is None:
        raise AssertionError(f"## {number}. section not found")
    rest = document[match.end():]
    nxt = re.search(r"(?m)^## ", rest)
    return rest[: nxt.start()] if nxt else rest


def _sub_block(section: str, heading: str) -> str:
    """Body of a ``#### <heading>`` inside a section, sliced to the next ``#### ``."""
    match = re.search(rf"(?m)^#### {re.escape(heading)}\s*$", section)
    if match is None:
        raise AssertionError(f"#### {heading} not found")
    rest = section[match.end():]
    nxt = re.search(r"(?m)^#### ", rest)
    return rest[: nxt.start()] if nxt else rest


SEC38 = _section(BOOK, 38)
NAME_BLOCK = _sub_block(SEC38, "Name and identity")
DIPLO = _sub_block(SEC38, "Diplomacy and the emerging NHI cold war")
NAME_FLAT = _flat(NAME_BLOCK)
DIPLO_FLAT = _flat(DIPLO)


class UnsanNameTests(unittest.TestCase):
    def test_official_name_is_the_administration_expansion(self):
        self.assertIn(f"**{OFFICIAL} (UNSA)**", NAME_BLOCK)

    def test_the_old_agency_expansion_is_gone_from_live_canon(self):
        live = _canon_prose(BOOK)
        for label, text in (
            ("RULEBOOK live prose", live),
            ("rulebook/4_SOCIAL.md", SOCIAL),
            ("FACTIONS.md", FACTIONS),
            ("organizations.yaml", ORG),
        ):
            with self.subTest(document=label):
                self.assertNotIn(OLD_OFFICIAL, text)
                self.assertNotIn(OLD_FORMER, text)
                # the looser noun too, so the acronym cannot silently reattach to a variant
                self.assertNotIn("Security Agency", text)
                self.assertNotIn("X-Risk Agency", text)

    def test_the_former_name_is_history_not_the_current_name(self):
        # The directive keeps the X-Risk name, but as institutional history. Both facts:
        self.assertIn(FORMER, NAME_FLAT)
        self.assertRegex(NAME_FLAT, r"(?i)early formation")
        # and the sentence declaring the official name must not carry the former name
        official_sentence = next(line for line in NAME_BLOCK.splitlines() if OFFICIAL in line)
        self.assertNotIn(FORMER, official_sentence)

    def test_nicknames_are_informal_culture_not_official_designations(self):
        self.assertRegex(NAME_FLAT, r"(?i)informal institutional culture")
        self.assertRegex(NAME_FLAT, r"not official designations")
        for nickname in ("X-COM", "X-Files", "Men in Black"):
            with self.subTest(nickname=nickname):
                self.assertIn(nickname, NAME_FLAT)
        # the recurring institutional-culture bit the issue asks for
        self.assertRegex(NAME_FLAT, r"Academy graduates")
        # the explicit non-affiliation disclaimer
        self.assertRegex(NAME_FLAT, r"(?i)franchise")
        # official register stays formal
        self.assertRegex(NAME_FLAT, r"(?i)Official briefings, protocol and legal documents")

    def test_mj12_is_still_rejected(self):
        self.assertIn("MJ-12 is not an acceptable nickname", NAME_FLAT)

    def test_the_machine_readable_model_agrees_with_canon(self):
        self.assertIn(f"canonical_name: {OFFICIAL}", ORG)
        self.assertIn(f"- {FORMER}", ORG)
        for alias in ("X-COM", "X-Files", "Men in Black"):
            with self.subTest(alias=alias):
                self.assertIn(f"- {alias}", ORG)


class UnsanDiplomacyTests(unittest.TestCase):
    def test_early_posture_was_diplomatic_toward_both_blocs(self):
        self.assertRegex(DIPLO_FLAT, r"(?i)diplomatic toward both")
        self.assertRegex(DIPLO_FLAT, r"(?i)Confederacy and Orion")

    def test_orion_is_a_hybrid_cold_proxy_conflict_not_an_invasion(self):
        self.assertRegex(DIPLO_FLAT, r"hybrid, cold and proxy conflict")
        self.assertRegex(DIPLO_FLAT, r"rather than open invasion")

    def test_confederacy_is_friendly_and_conditional(self):
        self.assertRegex(DIPLO_FLAT, r"broadly \*\*friendly\*\*")
        self.assertRegex(DIPLO_FLAT, r"\*\*conditional\*\*")
        self.assertRegex(DIPLO_FLAT, r"(?i)Friendly is not the same as settled")
        self.assertRegex(DIPLO_FLAT, r"(?i)not above criticism")

    def test_human_politics_are_not_a_mirror_of_the_nhi_divide(self):
        self.assertRegex(DIPLO_FLAT, r"not a mirror of the NHI divide")
        self.assertRegex(DIPLO_FLAT, r"(?i)modelling error")

    def test_the_case_load_is_investigation_and_uncertainty(self):
        self.assertRegex(DIPLO_FLAT, r"(?i)investigation rather than battle")
        self.assertRegex(DIPLO_FLAT, r"(?i)diplomatic incidents")
        self.assertRegex(DIPLO_FLAT, r"(?i)ordinary human deception")

    def test_the_diplomacy_citations_resolve(self):
        # House convention: a modular chapter is referenced by link, never by its own
        # §-numbers, and every §x.y cited here must resolve inside RULEBOOK.md.
        # Counted, not merely present: both citations carry the link, so dropping one
        # must fail rather than hide behind the other (the recurring-token trap).
        link = "[rulebook/15_XENOPOLITICS.md](rulebook/15_XENOPOLITICS.md)"
        self.assertEqual(DIPLO_FLAT.count(link), 2, "both diplomacy citations must link the chapter")
        self.assertIn("§40.3", DIPLO_FLAT)
        self.assertRegex(BOOK, r"(?m)^### 40\.3[ \t]")
        headings = set(re.findall(r"(?m)^#{2,4}\s+(\d+(?:\.\d+)*)", BOOK))
        for ref in sorted(set(re.findall(r"§\s*(\d+(?:\.\d+)*)", DIPLO))):
            if "." not in ref:
                continue
            with self.subTest(ref=ref):
                self.assertIn(ref, headings, f"§{ref} is cited but no RULEBOOK heading defines it")


class UnsanFictionBoundaryTests(unittest.TestCase):
    def test_wendt_is_an_influence_not_evidence(self):
        block = _flat(_sub_block(SEC38, "Disclosure shock: fragmentation and unification"))
        self.assertIn("Wendt", block)
        self.assertRegex(block, r"\*\*NoöPunk fiction\*\*")
        self.assertIn("§37", block)  # the interpretation rule is cited, not implied

    def test_the_interpretation_rule_still_exists(self):
        section37 = _section(BOOK, 37)
        self.assertRegex(_flat(section37), r"(?i)fictional extrapolation")


if __name__ == "__main__":
    unittest.main()
