# -*- coding: utf-8 -*-
"""Guard for the #200 licence / NOTICE / attribution plan.

`docs/licenses/ISSUE_200_LICENSE_AND_NOTICE_PLAN.md` is the itemization #200 asks for, and the
part of it that can rot silently is its **coverage**: a new ledger entry whose attribution or
exclusion never reaches the plan is invisible, because nothing links the two documents.

So this guard pins the link: every source in `data/sources/game_system_rights.json` must appear
in the plan, and the mapping between them is counted against the ledger's own length — adding a
source without extending the plan is a failure, not a silence. (A hand-maintained list that is
never checked against its source is the defect class this repository has hit before.)

It also keeps the plan honest about being a plan: no `LICENSE` file, no claim that a licence was
selected, and the attribution obligations the licences actually impose.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "sources" / "game_system_rights.json"
PLAN = ROOT / "docs" / "licenses" / "ISSUE_200_LICENSE_AND_NOTICE_PLAN.md"

#: ledger id -> the name the plan must use for it. Length is checked against the ledger, so a
#: new source forces this map AND the plan to be extended together.
PLAN_NAMES = {
    "fate-core-srd": "Fate Core",
    "fudge-ogl-srd": "Fudge SRD",
    "fudge-1995-pdf": "Fudge 1995",
    "psi-punk": "Psi-Punk",
    "eclipse-phase-2e": "Eclipse Phase 2e",
    "transhumanitys-fate": "Transhumanity's Fate",
    "cities-without-number-srd": "Cities Without Number",
    "stars-without-number-srd": "Stars Without Number",
    "apocalypse-world": "Apocalypse World",
    "the-veil": "The Veil",
    "cyberpunk-red-2020": "Cyberpunk RED",
    "cy-borg": "CY_BORG",
    "shadowrun": "Shadowrun",
    "other-proprietary-tabletop": "GURPS",
    "computer-game-references": "Computer-game references",
}

#: Licences whose terms require an attribution block.
ATTRIBUTION_REQUIRED = ("CC BY", "CC BY-SA")


def ledger() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def plan_text() -> str:
    """Flattened plan text, with blockquote markers stripped.

    The attribution blocks are quoted (`> ...`), so joining lines without removing the marker
    produces "Evil Hat > Productions" and a correct needle silently misses.
    """
    raw = re.sub(r"(?m)^>[ \t]?", "", PLAN.read_text(encoding="utf-8"))
    return " ".join(raw.split())


class CoverageTests(unittest.TestCase):
    """A source that reaches the ledger must reach the plan."""

    def setUp(self) -> None:
        self.ids = [e["id"] for e in ledger()["sources"]]
        self.text = plan_text().lower()

    def test_the_plan_exists(self):
        self.assertTrue(PLAN.exists(), "the licence/NOTICE plan is missing")

    def test_the_name_map_covers_the_ledger_exactly(self):
        # The completeness check: a new ledger entry cannot slip past the plan.
        self.assertEqual(
            sorted(PLAN_NAMES), sorted(self.ids),
            "the ledger gained or lost a source; extend PLAN_NAMES and the plan together",
        )

    def test_every_ledger_source_is_named_in_the_plan(self):
        for key in self.ids:
            name = PLAN_NAMES.get(key, "")
            with self.subTest(source=key):
                self.assertTrue(name, f"no plan name mapped for {key}")
                self.assertIn(name.lower(), self.text, f"{name} is absent from the plan")


class AttributionTests(unittest.TestCase):
    """The plan must discharge the attribution the adaptable licences impose."""

    def setUp(self) -> None:
        self.entries = {e["id"]: e for e in ledger()["sources"]}
        self.text = plan_text()

    def test_attribution_required_sources_have_an_attribution_string(self):
        """Only ADAPTABLE sources carry an attribution obligation.

        A NonCommercial source is an EXCLUSION: no expression is imported from it, so it owes a
        credit line in the exclusions rather than an attribution block. Requiring a block for
        `CC BY-NC-SA` would confuse "we may adapt this" with "we may name this".
        """
        for key, entry in self.entries.items():
            if entry.get("decision") != "verified-permissive":
                continue
            lic = str(entry.get("license", ""))
            if not lic.startswith(ATTRIBUTION_REQUIRED):
                continue
            with self.subTest(source=key):
                self.assertTrue(
                    entry.get("attribution"),
                    f"{key} carries {lic}, which requires attribution, but records none",
                )

    def test_the_fate_attribution_names_the_publisher_and_the_licence(self):
        block = self.text
        self.assertIn("Evil Hat Productions", block)
        self.assertIn("Creative Commons Attribution 3.0 Unported", block)

    def test_the_shares_alike_consequence_is_stated(self):
        self.assertRegex(self.text, r"(?i)ShareAlike consequence")

    def test_the_veil_per_portion_exclusion_is_recorded(self):
        # Its own text lifts moves from Apocalypse World with permission granted to THAT
        # project; those portions are not covered by The Veil's licence.
        self.assertRegex(
            self.text,
            r"(?i)per-portion exclusion.{0,400}permission was granted \*\*to that project\*\*",
        )

    def test_cc0_sources_record_that_attribution_is_not_required(self):
        entry = self.entries["cities-without-number-srd"]
        self.assertIn("None required", str(entry.get("attribution")))


class PlanIsStillAPlanTests(unittest.TestCase):
    """Nothing here may quietly become a relicence."""

    def test_no_license_file_exists(self):
        for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
            with self.subTest(file=name):
                self.assertFalse(
                    (ROOT / name).exists(),
                    f"{name} exists: the licence selection is the author's, not an agent's",
                )

    def test_the_plan_is_marked_as_a_proposal(self):
        text = plan_text()
        self.assertIn("PROPOSAL", text)
        self.assertRegex(text, r"(?i)awaiting the author's selection")

    def test_the_plan_does_not_claim_a_selection_was_made(self):
        lowered = plan_text().lower()
        for forbidden in ("the licence has been selected", "released under cc by", "is now licensed"):
            with self.subTest(phrase=forbidden):
                self.assertNotIn(forbidden, lowered)

    def test_the_artifact_classes_are_itemized_and_code_is_separate(self):
        text = plan_text()
        for cls in ("Rulebook prose", "Game data", "Source code"):
            with self.subTest(artifact_class=cls):
                self.assertIn(cls, text)
        # data must travel with the rulebook, not with the code
        self.assertRegex(text, r"(?i)why the data files are grouped with the rulebook")

    def test_both_licence_options_and_the_cost_of_the_alternative(self):
        text = plan_text()
        self.assertIn("CC BY-SA 4.0", text)
        self.assertIn("CC BY 4.0", text)
        self.assertRegex(text, r"(?i)BY-SA pathway closes")

    def test_the_exclusions_carry_reasons(self):
        lowered = plan_text().lower()
        for reason in ("cannot be relabelled", "noncommercial cannot enter", "no cc grant",
                       "out of the rule bases"):
            with self.subTest(reason=reason):
                self.assertIn(reason, lowered)


if __name__ == "__main__":
    unittest.main()
