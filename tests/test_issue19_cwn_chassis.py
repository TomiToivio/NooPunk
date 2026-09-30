# -*- coding: utf-8 -*-
"""Issue #19 — the Cities Without Number SRD chassis: licence boundary and restraint.

Main's `docs/CWN_CHASSIS.md` (merged via PR #20) records the policy. What it did not
carry was any **enforcement** and any **licence verification**, so those are what
this file guards.

Two kinds of check:

1. **Licence-boundary guards.** The policy's legal line is "reuse only what is in
   the SRD", and the failure mode is someone deciding a piece of text looks
   generic enough to reuse. The guards pin the licence (CC0), pin the exclusions
   (setting, megacorps, NPCs, GM tool text), and pin the fact that the reading
   mirror is unofficial — so "I couldn't find it on the mirror" cannot be read as
   permission.
2. **Restraint guards.** #19 is policy only, and the easiest way to "complete" it
   while breaking it is to adopt a subsystem. The strongest check parses the review
   status table and asserts that exactly one row is decided.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

POLICY = ROOT / "docs" / "CWN_CHASSIS.md"
AGENTS = ROOT / "AGENTS.md"
RULEBOOK = ROOT / "RULEBOOK.md"
README = ROOT / "README.md"
PRINCIPLES = ROOT / "docs" / "DESIGN_PRINCIPLES.md"
CORE_JSON = ROOT / "data" / "rules" / "core.json"
GODOT_ADAPTER = ROOT / "src" / "godot" / "core_rules.gd"
CONCORDIA_MECHANICS = ROOT / "src" / "concordia_runtime" / "mechanics.py"

#: The decisions author work has actually recorded in the review-status table.
#: `attributes` predates the chassis (#19); `skills` was reviewed under it (#22).
#: Everything else must still read DEFER.
DECIDED_ROWS = {"attributes": "REPLACE", "skills": "MODIFY"}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(path: Path) -> str:
    """Lowercased, whitespace-collapsed, emphasis stripped.

    Emphasis has to go: the documents write claims like "is **not** a clone" and
    "does **not** override", so a plain substring search misses the very sentences
    that carry the rule.
    """
    return " ".join(_text(path).replace("*", "").split()).lower()


class LicenceBoundaryTests(unittest.TestCase):
    """The legal line: reuse only what is actually in the SRD."""

    def test_the_licence_is_named(self) -> None:
        """The doc previously asserted 'public domain' with no source.

        The verified position is a CC0 waiver by the author. Naming the licence is
        what lets a contributor check the claim instead of trusting it.
        """
        flat = _flat(POLICY)
        self.assertIn("cc0", flat)
        self.assertIn("waiver", flat)
        self.assertIn("creative commons", flat)

    def test_the_licence_covers_mechanics_and_trivially_derived_content(self) -> None:
        flat = _flat(POLICY)
        self.assertIn("mechanics of the game", flat)
        self.assertIn("trivially-derived content", flat)
        self.assertIn("weapon damage dice", flat)

    def test_the_licence_explicitly_excludes_the_setting(self) -> None:
        flat = _flat(POLICY)
        for excluded in ("specific setting", "megacorp", "individual npcs",
                         "gm tool text"):
            with self.subTest(excluded=excluded):
                self.assertIn(excluded, flat)

    def test_the_reading_mirror_is_recorded_as_unofficial(self) -> None:
        """The boundary must not rest on a fan mirror's own claim.

        cwn.quadrifons.com omits sections and may contain transcription errors, so
        the policy has to point at the publisher's file as authoritative.
        """
        flat = _flat(POLICY)
        self.assertIn("cwn.quadrifons.com", flat)
        self.assertIn("unofficial", flat)
        self.assertIn("sine nomine", flat)
        self.assertIn("authoritative", flat)

    def test_an_absence_from_the_mirror_is_not_permission(self) -> None:
        """The precise misreading this guard exists to prevent."""
        flat = _flat(POLICY)
        self.assertIn(
            "an absence from the mirror is not an absence from the srd", flat
        )

    def test_direct_reuse_is_limited_to_the_srd(self) -> None:
        flat = _flat(POLICY)
        self.assertIn("actually present in the cwn srd", flat)
        self.assertIn("rules source", flat)
        self.assertIn("is not a setting source", flat)

    def test_the_other_five_systems_are_references_only(self) -> None:
        flat = _flat(POLICY)
        for influence in ("cyberpunk 2020", "eclipse phase", "shadowrun",
                          "the sprawl", "cy_borg"):
            with self.subTest(influence=influence):
                self.assertIn(influence, flat)
        self.assertIn("design references only", flat)

    def test_no_presented_claim_of_official_status(self) -> None:
        """CC0 needs no attribution, but NoöPunk must not imply endorsement."""
        flat = _flat(POLICY)
        self.assertIn("not a sine nomine product", flat)
        self.assertIn("official or sanctioned", flat)

    def test_every_doc_naming_the_chassis_also_names_the_srd(self) -> None:
        """The SRD-vs-full-book distinction is the whole boundary.

        A document that says only "Cities Without Number" blurs it, so each
        contributor-facing doc must name the SRD.
        """
        for doc in (POLICY, AGENTS, RULEBOOK, README):
            with self.subTest(doc=doc.name):
                flat = _flat(doc)
                self.assertIn("cities without number", flat)
                self.assertIn("srd", flat,
                              f"{doc.name} names the game but not the SRD boundary")


class RestraintTests(unittest.TestCase):
    """#19 converts nothing. This is the load-bearing guard."""

    def test_no_keep_decision_exists_yet(self) -> None:
        """KEEP would adopt a CWN subsystem; no author has decided one."""
        text = _text(POLICY)
        status = text[text.index("### Review status"):text.index("## NoöPunk decisions")]
        rows = [ln for ln in status.splitlines() if ln.strip().startswith("|")]
        for row in rows:
            cells = [c.strip().replace("*", "") for c in row.strip("|").split("|")]
            if len(cells) < 2:
                continue
            decision = cells[1].strip().upper()
            with self.subTest(row=cells[0]):
                self.assertNotEqual(
                    decision, "KEEP",
                    f"{cells[0]!r} is KEEP, adopting a CWN subsystem without an "
                    f"author decision",
                )

    def test_only_the_attribute_row_is_decided(self) -> None:
        """Exactly one subsystem may be decided, and it predates the chassis."""
        text = _text(POLICY)
        status = text[text.index("### Review status"):text.index("## NoöPunk decisions")]
        decided = {}
        for line in status.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip().replace("*", "") for c in line.strip("|").split("|")]
            if len(cells) < 2 or set(cells[0]) <= set("-: "):
                continue
            label = cells[0].strip().lower()
            decision = cells[1].strip().upper()
            if not decision or decision == "DECISION":
                continue
            if decision != "DEFER":
                decided[label] = decision
        self.assertEqual(
            decided, DECIDED_ROWS,
            "the set of decided subsystems changed; #19 must not resolve a DEFER row",
        )

    def test_unreviewed_rows_still_read_defer(self) -> None:
        flat = _flat(POLICY)
        self.assertIn("every row not marked otherwise stays defer", flat)
        self.assertIn("a defer is not a decision to keep cwn", flat)

    def test_defer_is_not_permission_for_an_agent_to_choose(self) -> None:
        flat = _flat(AGENTS)
        self.assertIn("subsystem decisions belong to the author", flat)
        self.assertIn("a defer is an open question, not permission", flat)

    def test_policy_states_it_converts_nothing(self) -> None:
        flat = _flat(POLICY)
        self.assertIn("policy and roadmap only", flat)
        self.assertIn("does not convert", flat)


class PrecedenceTests(unittest.TestCase):
    """Existing NoöPunk rules take precedence over CWN defaults."""

    def test_precedence_is_stated_in_policy_and_agent_rules(self) -> None:
        for doc in (POLICY, AGENTS):
            with self.subTest(doc=doc.name):
                self.assertIn("take precedence", _flat(doc))
        # the "not a higher authority" phrasing lives in the policy; AGENTS.md
        # states the same rule as a direct instruction instead
        self.assertIn("not a higher authority", _flat(POLICY))

    def test_rules_are_not_to_be_redesigned_back_toward_cwn(self) -> None:
        self.assertIn("not be redesigned back toward", _flat(POLICY))
        self.assertIn("do not redesign them back toward cwn", _flat(AGENTS))

    def test_six_attributes_are_preserved(self) -> None:
        text = _text(RULEBOOK)
        section = text[text.index("### 5.1 Attributes"):text.index("### 5.2")]
        for code in ("**Fitness (FIT):**", "**Reflexes (REF):**", "**Intelligence (INT):**",
                     "**Charisma (CHA):**", "**Cybernetics (CYB):**", "**Psyche (PSY):**"):
            with self.subTest(attribute=code):
                self.assertIn(code, section, f"{code} is missing from the attribute list")
        self.assertIn("Do not add alternate names or additional attributes", section)

    def test_cwn_attribute_names_never_became_noopunk_attributes(self) -> None:
        """CWN names may appear only as a mapping, never as list entries."""
        text = _text(RULEBOOK)
        section = text[text.index("### 5.1 Attributes"):text.index("### 5.2")]
        for cwn_name in ("Strength", "Constitution", "Wisdom", "Dexterity"):
            with self.subTest(cwn_name=cwn_name):
                self.assertNotRegex(
                    section, rf"\*\*{cwn_name} \(",
                    f"the attribute list gained CWN's {cwn_name}",
                )

    def test_modifier_range_and_generation_are_preserved(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("| 3 | -3 |", flat)
        self.assertIn("| 18 | +3 |", flat)
        self.assertIn("ordinary-human -3..+3 range", flat)

    def test_cwn_core_mechanic_did_not_leak_into_canon(self) -> None:
        """CWN's 2d6 core check must not appear as a NoöPunk rule."""
        self.assertNotIn("2d6", _text(RULEBOOK))
        self.assertNotIn("2d6", _text(CORE_JSON))

    def test_difficulty_ladder_and_3d6_core_are_preserved(self) -> None:
        flat = _flat(RULEBOOK)
        for name, target in (("easiest", 3), ("easier", 6), ("easy", 9),
                             ("normal", 12), ("hard", 15), ("impossible", 18)):
            with self.subTest(difficulty=name):
                self.assertRegex(flat, rf"\| {name} \| {target} \|")
        self.assertIn("total = 3d6", flat)


class TabletopFirstTests(unittest.TestCase):
    """Tabletop-first sequencing stays binding; runtimes stay deferred."""

    def test_policy_states_the_five_step_sequence(self) -> None:
        flat = _flat(POLICY)
        for step in ("review the cwn srd version", "compare it with noöpunk's goals",
                     "define or modify the tabletop rule", "stabilize it",
                     "only then create digital specifications and ports"):
            with self.subTest(step=step):
                self.assertIn(step, flat)

    def test_bulk_porting_is_forbidden(self) -> None:
        flat = _flat(POLICY) + " " + _flat(AGENTS)
        self.assertIn("tabletop first. godot and concordia later", flat)
        self.assertIn("do not bulk-port cwn mechanics", flat)

    def test_core_json_gained_no_cwn_derived_schema(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        self.assertEqual(
            canon["difficulties"],
            {"Easiest": 3, "Easier": 6, "Easy": 9,
             "Normal": 12, "Hard": 15, "Impossible": 18},
        )
        self.assertEqual(canon["unskilled_penalty"], -1)
        self.assertEqual(canon["trained_only_without_skill"], "blocked")
        for key in canon:
            with self.subTest(key=key):
                lowered = key.lower()
                for forbidden in ("cwn", "cities_without_number", "saving_throw",
                                  "strain", "background", "focus", "edge"):
                    self.assertNotIn(
                        forbidden, lowered,
                        f"data/rules/core.json gained {key!r}; #19 ports nothing",
                    )

    def test_runtimes_gained_no_cwn_mechanics(self) -> None:
        for path in (GODOT_ADAPTER, CONCORDIA_MECHANICS):
            with self.subTest(path=path.name):
                flat = _flat(path)
                for forbidden in ("2d6", "saving_throw", "saving throw",
                                  "cities_without_number", "cwn"):
                    self.assertNotIn(forbidden, flat,
                                     f"{path.name} gained a CWN mechanic")


class SiteAndDocParityTests(unittest.TestCase):
    """The site and the docs must agree about the chassis.

    This repo has already had one doc/site drift defect of exactly this kind, which
    survived because nothing checked the published site.
    """

    def test_the_site_mentions_the_chassis(self) -> None:
        site = ROOT / "docs" / "index.html"
        flat = _flat(site)
        self.assertTrue("cities without number" in flat or "cwn" in flat,
                        "the published site does not mention the chassis")

    def test_the_site_does_not_call_noopunk_a_clone(self) -> None:
        """Only an AFFIRMATIVE clone claim is a defect.

        A bare substring check is wrong here: the correct sentence is "it is NOT a
        Cities Without Number clone", which contains the phrase this guard is
        looking for. Match the claim, then require the negation in front of it.
        """
        site = ROOT / "docs" / "index.html"
        flat = _flat(site)
        for phrase in ("cities without number clone", "cwn clone", "cwn retroclone"):
            with self.subTest(phrase=phrase):
                for match in re.finditer(re.escape(phrase), flat):
                    window = flat[max(0, match.start() - 60):match.start()]
                    negated = any(m in window for m in ("not ", "never ", "no longer "))
                    self.assertTrue(
                        negated,
                        f"the site describes NoöPunk as a {phrase!r} without negation:\n"
                        f"  ...{window}{phrase}...",
                    )

    def test_design_principles_still_govern(self) -> None:
        """The chassis must not displace the three balances as higher authority."""
        flat = _flat(POLICY)
        self.assertIn("design_principles.md", flat)
        self.assertIn("higher authority on design intent", flat)


if __name__ == "__main__":
    unittest.main()
