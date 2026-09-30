# -*- coding: utf-8 -*-
"""Regression guard for the Cities Without Number SRD chassis policy (issue #19).

The policy landed as documentation only, so the risk is not behaviour — it is that
the *policy* silently stops being true. Three claims are load-bearing and were
each unguarded when this test was written:

1. **The canonical document exists and is referenced.** `docs/CWN_CHASSIS.md` is
   the single source for the chassis policy; four other documents link to it.
   Deleting it left CI green.
2. **Precedence runs the right way.** The whole point of #19 is that adopting a
   third-party chassis must not displace author-specified NoöPunk rules. The
   docs said so in several places and *nothing asserted it*, so inverting the
   sentence ("CWN defaults take precedence over existing NoöPunk rules") left CI
   green.
3. **The ninth design invariant is carried.** Landing #19 added a ninth
   invariant to `docs/DESIGN_PRINCIPLES.md` and `AGENTS.md`, but
   `test_design_principles.py` still asserted `range(1, 9)`. Removing invariant 9
   from `AGENTS.md` left CI green.

The remaining classes here are the issue's own acceptance criteria: the chassis
is the *SRD*, NoöPunk is not a clone, the decision model is complete, only SRD
material may be reused, tabletop-first survives, and **no subsystem or mechanic
was implemented or ported**.

This is a STRUCTURE guard. It constrains what the policy documents say, not how
anyone implements a rule. It deliberately does not enumerate the review table's
rows: those are DEFER-by-default and are the author's to decide, so pinning them
here would make the author's later decisions fail the build.
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
DESIGN_PRINCIPLES = ROOT / "docs" / "DESIGN_PRINCIPLES.md"
CORE_JSON = ROOT / "data" / "rules" / "core.json"
GODOT_ADAPTER = ROOT / "src" / "godot" / "core_rules.gd"
CONCORDIA_MECHANICS = ROOT / "src" / "concordia_runtime" / "mechanics.py"

#: Documents that must reference the canonical chassis policy.
REFERRING_DOCS = ("AGENTS.md", "README.md", "RULEBOOK.md", "docs/DESIGN_PRINCIPLES.md")

#: The five decisions the author specified.
DECISIONS = ("keep", "modify", "replace", "omit", "defer")

#: The six canonical attributes, which the chassis must not replace.
ATTRIBUTES = ("FIT", "REF", "INT", "CHA", "CYB", "PSY")

#: Systems that stay comparative influences, never sources to copy.
COMPARATIVE_INFLUENCES = (
    "cyberpunk 2020",
    "eclipse phase",
    "shadowrun",
    "the sprawl",
    "cy_borg",
)

#: U+2212 MINUS SIGN appears in the policy doc; RULEBOOK.md uses an ASCII hyphen.
#: Normalising both avoids a guard that breaks on typography rather than meaning.
_MINUS = "\u2212"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(path: Path) -> str:
    """Lowercased, whitespace-collapsed, minus-normalised text."""
    flat = " ".join(_text(path).split()).lower()
    return flat.replace(_MINUS, "-")


class CanonicalDocumentTests(unittest.TestCase):
    """The policy must exist and be reachable from the documents that cite it."""

    def test_policy_document_exists(self) -> None:
        self.assertTrue(POLICY.is_file(), "docs/CWN_CHASSIS.md is missing")

    def test_every_referring_document_links_the_policy(self) -> None:
        for doc in REFERRING_DOCS:
            with self.subTest(doc=doc):
                self.assertIn(
                    "CWN_CHASSIS.md",
                    _text(ROOT / doc),
                    f"{doc} does not reference the canonical chassis policy",
                )

    def test_no_second_chassis_document_exists(self) -> None:
        """One source of truth: no competing chassis doc under docs/."""
        candidates = [
            p.name for p in (ROOT / "docs").glob("*.md")
            if re.search(r"chassis|cwn|cities", p.name, re.I)
        ]
        self.assertEqual(
            candidates, ["CWN_CHASSIS.md"],
            f"expected exactly one canonical chassis doc, found {sorted(candidates)}",
        )


class ChassisIsTheSrdTests(unittest.TestCase):
    def test_names_cities_without_number(self) -> None:
        self.assertIn("cities without number", _flat(POLICY))

    def test_names_the_srd_not_the_commercial_book(self) -> None:
        text = _flat(POLICY)
        self.assertIn("srd", text)
        self.assertIn("full commercial", text)

    def test_states_nopunk_is_not_a_clone(self) -> None:
        """Tolerate the markdown emphasis between 'not' and the name."""
        self.assertRegex(
            _flat(POLICY),
            r"not\*{0,2} a cities without number clone",
        )
        self.assertIn("retroclone", _flat(POLICY))


class DecisionModelTests(unittest.TestCase):
    def test_documents_all_five_decisions(self) -> None:
        text = _flat(POLICY)
        for decision in DECISIONS:
            with self.subTest(decision=decision):
                self.assertIn(decision, text)

    def test_does_not_assume_any_subsystem_survives(self) -> None:
        self.assertIn("do not assume any subsystem survives unchanged", _flat(POLICY))

    def test_documents_the_review_scaffold(self) -> None:
        text = _flat(POLICY)
        for subsystem in ("attributes", "skills", "combat", "cyberware",
                          "hacking / cyberspace", "advancement"):
            with self.subTest(subsystem=subsystem):
                self.assertIn(subsystem, text)


class PrecedenceTests(unittest.TestCase):
    """The load-bearing claim: author intent outranks the chassis."""

    def test_policy_states_precedence(self) -> None:
        self.assertIn("noöpunk decisions take precedence", _flat(POLICY))

    def test_policy_denies_the_chassis_is_a_higher_authority(self) -> None:
        self.assertIn("not a higher authority", _flat(POLICY))

    def test_rulebook_states_precedence(self) -> None:
        self.assertIn("take precedence over cwn defaults", _flat(RULEBOOK))

    def test_agents_md_states_precedence(self) -> None:
        self.assertIn("noöpunk decisions take precedence", _flat(AGENTS))

    def test_design_principles_states_precedence(self) -> None:
        self.assertIn("take precedence over cwn defaults", _flat(DESIGN_PRINCIPLES))

    def test_rulebook_never_says_the_chassis_wins(self) -> None:
        """The inversion that was previously undetectable."""
        text = _flat(RULEBOOK)
        for inverted in (
            "cwn defaults take precedence over existing noöpunk rules",
            "cwn takes precedence",
            "cwn overrides",
        ):
            with self.subTest(inverted=inverted):
                self.assertNotIn(inverted, text)


class ExistingRulesSurviveTests(unittest.TestCase):
    """Adopting the chassis must not change the rules already author-specified."""

    def test_core_json_still_carries_the_author_attributes(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        self.assertEqual([a["id"] for a in canon["attributes"]], list(ATTRIBUTES))

    def test_core_json_modifier_scale_is_unchanged(self) -> None:
        table = json.loads(_text(CORE_JSON))["human_3d6_modifier"]
        self.assertEqual(table["3"], -3)
        self.assertEqual(table["18"], 3)

    def test_no_chassis_attribute_replaced_a_author_attribute(self) -> None:
        ids = {a["id"].lower() for a in json.loads(_text(CORE_JSON))["attributes"]}
        for chassis_attribute in ("str", "con", "wis", "dex"):
            with self.subTest(attribute=chassis_attribute):
                self.assertNotIn(chassis_attribute, ids)

    def test_rulebook_preserves_the_modifier_range(self) -> None:
        self.assertIn("-3..+3", _flat(RULEBOOK))

    def test_policy_records_the_range_as_deliberate(self) -> None:
        text = _flat(POLICY)
        self.assertIn("-3..+3", text)
        self.assertIn("deliberate", text)


class LegalBoundaryTests(unittest.TestCase):
    def test_direct_reuse_is_limited_to_the_srd(self) -> None:
        self.assertIn("actually present in the cwn srd", _flat(POLICY))

    def test_full_book_setting_material_is_excluded(self) -> None:
        text = _flat(POLICY)
        self.assertIn("not a source at all", text)
        self.assertIn("protected megacorps", text)

    def test_comparative_influences_are_not_sources(self) -> None:
        text = _flat(POLICY)
        for influence in COMPARATIVE_INFLUENCES:
            with self.subTest(influence=influence):
                self.assertIn(influence, text)
        self.assertIn("design references only", text)

    def test_unsure_material_is_treated_as_outside_the_srd(self) -> None:
        self.assertIn("treat it as **not** in the srd", _flat(POLICY))


class NoSubsystemImplementedTests(unittest.TestCase):
    """#19 is policy only: nothing converted, nothing ported, no mechanics added."""

    def test_policy_scopes_itself_to_policy(self) -> None:
        text = _flat(POLICY)
        self.assertIn("does not convert", text)
        self.assertIn("policy and roadmap only", text)

    def test_core_json_gained_no_chassis_keys(self) -> None:
        for key in json.loads(_text(CORE_JSON)):
            with self.subTest(key=key):
                for forbidden in ("chassis", "cwn", "cities", "srd", "keep_modify"):
                    self.assertNotIn(
                        forbidden, key.lower(),
                        f"data/rules/core.json gained {key!r}; #19 is policy only",
                    )

    def test_no_digital_port_was_created(self) -> None:
        for path in (GODOT_ADAPTER, CONCORDIA_MECHANICS):
            flat = _flat(path)
            for term in ("chassis", "cities_without_number", "cwn_srd"):
                with self.subTest(path=path.name, term=term):
                    self.assertNotIn(term, flat)

    def test_tabletop_first_survives(self) -> None:
        self.assertIn("tabletop first. godot and concordia later", _flat(POLICY))


class DesignPrinciplesIntegrationTests(unittest.TestCase):
    """#19 added a ninth invariant; the drift guard must cover it."""

    def test_the_ninth_invariant_exists_in_both_documents(self) -> None:
        for doc in DESIGN_PRINCIPLES, AGENTS:
            with self.subTest(doc=doc.name):
                text = _flat(doc)
                self.assertIn("cities without number srd", text)

    def test_the_drift_guard_covers_every_invariant(self) -> None:
        """`test_design_principles.py` still checked `range(1, 9)` after #19.

        The loop's argument is exclusive, so asserting n invariants needs
        `range(1, n + 1)`. The count is read from each document's own invariant
        section rather than hard-coded, so adding a tenth invariant fails here
        until the drift guard follows.
        """
        cases = (
            (DESIGN_PRINCIPLES, r"(?ms)^## 5\. Invariants.*?(?=\n## |\Z)"),
            (AGENTS, r"(?ms)^### 13\. Preserve the three design balances.*?(?=\n### |\Z)"),
        )
        for doc, section_re in cases:
            with self.subTest(doc=doc.name):
                section = re.search(section_re, _text(doc))
                self.assertIsNotNone(section, f"{doc.name}: invariant section not found")
                assert section is not None
                listed = len(re.findall(r"(?m)^(\d+)\. ", section.group(0)))
                self.assertGreater(listed, 0, f"{doc.name}: no numbered invariants found")
                source = _text(ROOT / "tests" / "test_design_principles.py")
                match = re.search(r"for number in range\(1,\s*(\d+)\)", source)
                self.assertIsNotNone(match, "the invariant-count loop was removed")
                assert match is not None  # narrowed for type checkers
                self.assertGreaterEqual(
                    int(match.group(1)), listed + 1,
                    f"{doc.name} states {listed} invariants but the drift guard "
                    f"only checks range(1, {match.group(1)})",
                )

    def test_the_ninth_invariant_is_not_cwn_only(self) -> None:
        """Invariant 9 must keep precedence in the same sentence as the chassis."""
        text = _flat(DESIGN_PRINCIPLES)
        self.assertIn("take precedence over cwn defaults", text)


if __name__ == "__main__":
    unittest.main()
