# -*- coding: utf-8 -*-
"""Issue #200 item 1 — no closed-system DERIVATION claim survives in rule content.

The author's direction (2026-10-10) is that NoöPunk's rulebook must be licensable under
Creative Commons, and that closed/proprietary systems "must not remain bases or
implementation sources for NoöPunk rules". Naming a system as an *influence* stays
(and is honest); claiming the rules are *derived from* one does not.

This guard pins the absence of the derivation claims that were found and reworded, and
the positive properties that replaced them. It deliberately does NOT assert the absence
of the system names themselves: `RULEBOOK.md` legitimately records them as influences and
as things NoöPunk explicitly does NOT inherit, and the rights ledger's own tests require
the inventory to keep naming them.

Author-owned sites are excluded on purpose. `AGENTS.md` section 13.2 still fixes the old
CY_BORG / Cyberpunk 2020 / The Sprawl poles, and the rights ledger records that as
AUTHOR-OWNED; #200 says locked rules move "by author-approved process". A guard that
failed on AGENTS.md would be demanding the silent redesign section 13.8 forbids.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Release rule content: what a CC reader would receive as the rules.
RULE_CONTENT = (
    "RULEBOOK.md",
    "README.md",
    "rulebook/2_ATTRIBUTES.md",
    "rulebook/4_SOCIAL.md",
)

#: Closed/proprietary systems, and the phrases that used to assert derivation from them.
CLOSED_SYSTEMS = (
    "Cyberpunk RED",
    "Cyberpunk 2020",
    "Cyberpunk 2013",
    "Shadowrun",
    "CY_BORG",
    "GURPS",
    "Neon City Overdrive",
    "Otherscape",
    "The Sprawl",
)

#: Verbatim claims removed by this change. A regression guard, not a paraphrase test.
REMOVED_CLAIMS = (
    "inspired by the high-level choose-or-roll structure of Cyberpunk RED",
    "inspired by Cyberpunk RED social hooks",
    "Cyberpunk 2020/RED is an important reference for readable STAT + Skill + d10 resolution",
    "for the clarity and feel of STAT + Skill + d10 resolution",
    "and the old-school mechanical sensibility that NoöPunk often simplifies from",
    "EP2 is an influence and legacy implementation source",
    "which remain close to Cyberpunk 2020/RED",
)

#: A closed system may not be credited with a MECHANICAL contribution in rule content.
MECHANICAL_CREDIT = re.compile(
    r"mechanical (?:sensibility|source|parent|template|baseline|dependence)", re.IGNORECASE
)


NEGATION = re.compile(r"\b(?:not|no|never|without|nor|neither|no single)\b", re.IGNORECASE)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def sentences(text: str) -> list[str]:
    """Sentence-ish units, whitespace-collapsed so wrapping cannot hide a phrase."""
    flat = " ".join(text.split())
    return [s.strip() for s in re.split(r"(?<=[.;])\s+", flat) if s.strip()]


class RemovedClaimsStayRemovedTests(unittest.TestCase):
    def test_the_reworded_derivation_claims_are_gone(self) -> None:
        for relative in RULE_CONTENT:
            flat = " ".join(read(relative).split())
            for claim in REMOVED_CLAIMS:
                with self.subTest(file=relative, claim=claim[:48]):
                    self.assertNotIn(claim, flat)

    def test_a_closed_system_is_never_credited_with_a_mechanical_role(self) -> None:
        """A mechanical CREDIT, not the words themselves.

        `RULEBOOK.md` says "no external RPG is its mechanical parent" — the document
        obeys the rule, so an absence check on the phrase would fail on correct text.
        The clause up to the match is scanned for a negation; if the document already
        denies the claim, there is nothing to flag.
        """
        flagged: list[str] = []
        for relative in RULE_CONTENT:
            for sentence in sentences(read(relative)):
                if not any(system in sentence for system in CLOSED_SYSTEMS):
                    continue
                match = MECHANICAL_CREDIT.search(sentence)
                if match is None:
                    continue
                if NEGATION.search(sentence[: match.end()]):
                    continue  # already denied in this clause
                flagged.append(f"{relative}: {sentence[:120]}")
        self.assertEqual(flagged, [], "a closed system is credited mechanically:\n" + "\n".join(flagged))


class PositiveReplacementTests(unittest.TestCase):
    """Assert the replacement claim exists, not merely that the old words vanished."""

    def test_the_kernel_is_stated_as_noopunk_s_own(self) -> None:
        self.assertIn("kernel is NoöPunk's own", read("README.md"))

    def test_the_character_generation_framework_is_stated_as_original(self) -> None:
        flat = " ".join(read("RULEBOOK.md").split())
        self.assertIn("It copies no other game's tables, text or structure.", flat)

    def test_the_interop_tables_are_stated_as_non_derivative(self) -> None:
        flat = " ".join(read("rulebook/2_ATTRIBUTES.md").split())
        self.assertIn("make any external system a parent of these rules", flat)
        self.assertIn("RPG_CONVERSION_REFERENCE.md", flat)

    def test_the_ep2_prototype_is_marked_quarantined(self) -> None:
        flat = " ".join(read("RULEBOOK.md").split())
        self.assertIn("quarantined from the intended CC release surface", flat)


class MachineReadableClaimTests(unittest.TestCase):
    def test_core_json_lists_no_closed_system_as_an_influence(self) -> None:
        canon = json.loads(read("data/rules/core.json"))
        influences = canon["system_identity"]["influences"]
        self.assertGreaterEqual(len(influences), 5, "the influence list may not be emptied")
        for system in CLOSED_SYSTEMS:
            with self.subTest(system=system):
                self.assertFalse(
                    any(system in entry for entry in influences),
                    f"{system} is still listed as an influence on the kernel",
                )

    def test_core_json_still_states_independence_and_the_comparisons(self) -> None:
        canon = json.loads(read("data/rules/core.json"))
        identity = canon["system_identity"]
        self.assertTrue(identity["independent"])
        # A NEGATIVE claim ("not a conversion of") is the honest form and must stay.
        self.assertIn("Eclipse Phase", identity["not_a_conversion_of"])
        self.assertIn("issue #200", canon["_note"].lower())

    def test_the_tech_matrix_benchmarks_against_no_reference_game(self) -> None:
        text = read("data/world/tech_matrix.json")
        self.assertNotIn("Cyberpunk 2020/RED", text)
        self.assertIn("relative, not calibrated to any reference game", text)

    def test_the_conversion_matrix_separates_proprietary_from_usable(self) -> None:
        matrix = json.loads(read("data/rules/conversion_matrix.json"))
        blob = json.dumps(matrix)
        self.assertIn("proprietary comparisons kept separate", blob)


class LedgerMovesWithTheStateTests(unittest.TestCase):
    """An audit that still says 'reword' after the reword is stale."""

    def setUp(self) -> None:
        self.ledger = json.loads(read("data/sources/game_system_rights.json"))

    def test_every_actionable_site_records_the_rewording(self) -> None:
        live = self.ledger["closed_system_claim_inventory"]["live"]
        self.assertTrue(live)
        for claim in live:
            with self.subTest(file=claim["file"], line=claim.get("line")):
                action = claim["action"]
                if "AUTHOR-OWNED" in action or "may stay" in action:
                    # AUTHOR-OWNED: locked rules move by author-approved process.
                    # "may stay": the audit already judged the site compatible with #200.
                    continue
                self.assertIn(
                    "DONE 2026-10-10",
                    action,
                    f"{claim['file']}:{claim.get('line')} still reads as an open task",
                )

    def test_the_author_owned_sites_were_not_silently_changed(self) -> None:
        agents = read("AGENTS.md")
        self.assertIn("CY_BORG", agents)
        self.assertIn("Cyberpunk 2020", agents)

    def test_the_audit_still_records_the_boundary_it_promised(self) -> None:
        doc = read("docs/sources/GAME_SYSTEM_RIGHTS.md")
        self.assertIn("audit before deleting", doc.lower())
        self.assertIn("RPG_CONVERSION_REFERENCE.md", doc)


if __name__ == "__main__":
    unittest.main()
