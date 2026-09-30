# -*- coding: utf-8 -*-
"""Issue #17 — the human-user cyberspace and hacking modifier framework.

Documentation-only and tabletop-only, so the risks worth guarding are about what
the document must and must not say:

1. **The four modifier categories, with the exact values the author specified.**
   BCI and Compute and Infosec are `-1 / +0 / +1..+3`; Connection is `-1 / +0 / +1`
   and must NOT be given a `+2..+3` tier, because the author explicitly reserved
   further connection tiers.
2. **The framework staying a framework.** "A complete hacking subsystem" is the
   thing the issue forbids, so it is checked for: no ICE catalogs, no intrusion
   tables, no target-security model, no tool list, no cyberspace skill list.
3. **The character assumption staying human.** These modifiers are for human users;
   AI-native entities and uploaded humans are deferred. A test pins the deferral so
   it cannot be quietly absorbed into the general framework.
4. **Not every modifier applying to every check.** The single most likely way to
   misread the framework is as a fixed sum of four terms.
5. **No digital port.** No runtime schema, no Godot/Concordia implementation, and
   nothing added to `data/rules/core.json`.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = ROOT / "RULEBOOK.md"
AGENTS = ROOT / "AGENTS.md"
CORE_JSON = ROOT / "data" / "rules" / "core.json"
GODOT_ADAPTER = ROOT / "src" / "godot" / "core_rules.gd"
CONCORDIA_MECHANICS = ROOT / "src" / "concordia_runtime" / "mechanics.py"

#: The four categories, with the values the issue specifies. The third element is
#: the set of allowed modifier tiers and is asserted exactly, because Connection
#: deliberately has fewer tiers than the others.
CATEGORIES = {
    "bci": ("BCI modifier", -1, 0, 3),
    "compute": ("Compute modifier", -1, 0, 3),
    "connection": ("Connection modifier", -1, 0, 1),
    "infosec": ("Infosec defence modifier", -1, 0, 3),
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(path: Path) -> str:
    return " ".join(_text(path).split()).lower()


def _section(heading: str) -> str:
    """Return the body of a `####` subsection of 12.1, flattened and lowercased."""
    text = _text(RULEBOOK)
    start = text.index(heading)
    # next `####` heading, or the end of the section
    rest = text[start + len(heading):]
    match = re.search(r"\n#### ", rest)
    body = rest[: match.start()] if match else rest
    return " ".join(body.split()).lower()


class CategoryTests(unittest.TestCase):
    def test_all_four_categories_are_documented(self) -> None:
        flat = _flat(RULEBOOK)
        for key, (heading, *_rest) in CATEGORIES.items():
            with self.subTest(category=key):
                self.assertIn(
                    heading.lower(), flat,
                    f"RULEBOOK does not document the {key} category",
                )

    def test_bci_uses_minus_one_zero_and_plus_one_to_three(self) -> None:
        body = _section("#### BCI modifier")
        self.assertIn("**-1**", body)
        self.assertIn("**+0**", body)
        self.assertIn("**+1 to +3**", body)

    def test_compute_uses_minus_one_zero_and_plus_one_to_three(self) -> None:
        body = _section("#### Compute modifier")
        self.assertIn("**-1**", body)
        self.assertIn("**+0**", body)
        self.assertIn("**+1 to +3**", body)

    def test_connection_uses_minus_one_zero_and_plus_one_only(self) -> None:
        """Connection deliberately has no +2/+3 tier in this issue.

        The author reserved further connection tiers (fiber, satellite, mesh,
        tactical radio, air-gapped bridging, quantum) for later specification, so
        an invented +2/+3 tier would exceed the task.
        """
        body = _section("#### Connection modifier")
        self.assertIn("**-1**", body)
        self.assertIn("**+0**", body)
        self.assertIn("**+1**", body)
        self.assertNotIn("**+2", body)
        self.assertNotIn("**+3", body)
        self.assertNotIn("+1 to +3", body)

    def test_infosec_uses_minus_one_zero_and_plus_one_to_three(self) -> None:
        body = _section("#### Infosec defence modifier")
        self.assertIn("**-1**", body)
        self.assertIn("**+0**", body)
        self.assertIn("**+1 to +3**", body)


class CheckStructureTests(unittest.TestCase):
    def test_the_check_structure_combines_cyb_skill_and_modifiers(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("+ cyb attribute modifier", flat)
        self.assertIn("+ relevant skill modifier", flat)
        for _key, (heading, *_rest) in CATEGORIES.items():
            with self.subTest(category=heading):
                first_word = heading.split()[0].lower()
                self.assertIn(f"+ {first_word} modifier", flat)

    def test_the_structure_keeps_the_existing_formula_terms(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("total = 3d6", flat)
        self.assertIn("success = total >= difficulty target", flat)

    def test_not_every_category_applies_to_every_check(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("not every category applies to every check", flat)

    def test_infosec_is_described_as_primarily_defensive(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("primarily **defensive**", flat)

    def test_the_issue_named_examples_are_present_for_each_category(self) -> None:
        """Spot-check the author's own examples, not invented ones."""
        flat = _flat(RULEBOOK)
        for example in (
            "keyboard and monitor",       # BCI -1
            "mobile phone",               # BCI -1
            "cyberdeck",                  # Compute
            "cell phone",                 # Compute +0
            "mobile network",             # Connection -1
            "wlan",                       # Connection +0
            "physically wired",           # Connection +1
            "firewall",                   # Infosec -1
            "sandboxing",                 # Infosec -1
        ):
            with self.subTest(example=example):
                self.assertIn(example, flat)


class HumanOnlyTests(unittest.TestCase):
    def test_the_character_assumption_is_a_human_user(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("human characters operating in cyberspace", flat)

    def test_non_human_participants_are_explicitly_deferred(self) -> None:
        self.assertIn("deferred: non-human cyberspace participants", _flat(RULEBOOK))

    def test_the_deferral_names_the_categories_the_issue_lists(self) -> None:
        flat = _flat(RULEBOOK)
        for participant in (
            "ai-native entities",
            "uploaded humans",
            "autonomous software agents",
        ):
            with self.subTest(participant=participant):
                self.assertIn(participant, flat)

    def test_the_deferral_is_not_inferable_from_the_human_rules(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("must not be inferred from, the human-user modifiers", flat)

    def test_no_sentence_applies_the_modifiers_to_non_human_participants(self) -> None:
        """The gap sabotage found: presence of the deferral is not the property.

        Asserting only that the deferral sentence EXISTS lets a contradicting
        sentence sit next to it -- "These modifiers also apply to AI-native
        entities" passed every other test in this file.

        The check must be SENTENCE-scoped, not window-scoped: a 260-character
        window reaches back into the preceding deferral sentence, picks up its
        "not"/"deferred", and clears a contradictory sentence that follows it. That
        is exactly how the first version of this test failed to bite.
        """
        flat = _flat(RULEBOOK)
        section = flat[flat.index("### 12.1"):]
        section = section[: section.index("## 13.")]
        # Strip markdown emphasis first: the deferral sentence reads
        # "...are **not** generalized...", so a bare "not " marker misses it and
        # the test reports a correct sentence as a violation.
        section = section.replace("*", "")
        sentences = re.split(r"(?<=[.;]) ", section)
        markers = ("not ", "deferred", "separate future design task",
                   "must not be inferred", "does not", "do not", "no ")
        for participant in ("ai-native", "uploaded human", "autonomous software agent"):
            with self.subTest(participant=participant):
                mentions = [s_ for s_ in sentences if participant in s_]
                self.assertTrue(mentions, f"{participant!r} is never mentioned in 12.1")
                for sentence in mentions:
                    self.assertTrue(
                        any(m in sentence for m in markers),
                        f"a sentence mentions {participant!r} without deferral or "
                        f"negation, which claims the framework for it:\n  {sentence!r}",
                    )


class NoInventedSubsystemTests(unittest.TestCase):
    """Acceptance: no complete hacking subsystem, no cyberspace skill catalog."""

    #: Terms that would indicate an invented subsystem rather than a framework.
    BANNED_DEFINED_TERMS = (
        "ice catalog",
        "intrusion table",
        "target-system security",
        "target system security",
        "trace attempt",
        "neural malware",
        "brain damage",
        "mental status",
        "firewall product",
        "bandwidth value",
        "latency number",
        "flops",
    )

    def test_no_subsystem_content_is_defined(self) -> None:
        """These terms may appear ONLY in the explicit "not defined" lists."""
        raw = _text(RULEBOOK)
        flat = _flat(RULEBOOK)
        for term in self.BANNED_DEFINED_TERMS:
            with self.subTest(term=term):
                for match in re.finditer(re.escape(term), flat):
                    window = flat[max(0, match.start() - 400):match.end() + 120]
                    undeclared = any(
                        marker in window
                        for marker in (
                            "not defined here",
                            "deliberately left undefined",
                            "not to be inferred",
                            "remain for later author specification",
                            "later author specification",
                            "separate design pass",
                            "separate future design task",
                            "unspecified",
                            "do not invent",
                            "deferred",
                        )
                    )
                    self.assertTrue(
                        undeclared,
                        f"{raw.count(term)}x {term!r} is stated without a "
                        f"'not defined' context:\n...{window!r}",
                    )

    def test_no_cyberspace_skill_list_is_invented(self) -> None:
        flat = _flat(RULEBOOK)
        # the document states it as a list of things that are NOT defined
        self.assertIn("cyberspace skill list is defined", flat)
        self.assertIn("no hacking subsystem, tool catalog", flat)
        for invented in ("hacking skill", "cybercombat skill", "netrunning skill"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, flat)

    def test_cyberware_catalog_is_still_unresolved(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("cyberware rules and catalog", flat)


class ExistingRulesPreservedTests(unittest.TestCase):
    """#17 must not change the core rules it builds on."""

    def test_five_step_skill_levels_are_unchanged(self) -> None:
        flat = _flat(RULEBOOK)
        for level, name, modifier in (
            ("0", "unskilled", "special"),
            ("1", "basic", "+1"),
            ("2", "advanced", "+2"),
            ("3", "expert", "+3"),
        ):
            with self.subTest(level=level):
                self.assertRegex(flat, rf"\| {level} \| {name} \| {re.escape(modifier)} \|")

    def test_difficulty_ladder_is_unchanged(self) -> None:
        flat = _flat(RULEBOOK)
        for name, target in (("easiest", 3), ("easier", 6), ("easy", 9),
                             ("normal", 12), ("hard", 15), ("impossible", 18)):
            with self.subTest(difficulty=name):
                self.assertRegex(flat, rf"\| {name} \| {target} \|")

    def test_core_json_is_untouched(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        self.assertEqual(
            canon["difficulties"],
            {"Easiest": 3, "Easier": 6, "Easy": 9,
             "Normal": 12, "Hard": 15, "Impossible": 18},
        )
        self.assertEqual(canon["unskilled_penalty"], -1)
        self.assertEqual(canon["trained_only_without_skill"], "blocked")
        self.assertEqual(canon["opposed_rule"], "higher_total_wins")

    def test_opposed_checks_unchanged(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("higher final total wins", flat)
        self.assertIn("no tie-breaker rule is currently canonical", flat)


class NoDigitalPortTests(unittest.TestCase):
    """Acceptance: no runtime schema, no Godot/Concordia implementation."""

    def test_core_json_gains_no_modifier_or_cyberspace_schema(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        for key in canon:
            with self.subTest(key=key):
                lowered = key.lower()
                for forbidden in ("cyber", "hack", "bci", "infosec",
                                  "connection_modifier", "compute_modifier"):
                    self.assertNotIn(
                        forbidden, lowered,
                        f"data/rules/core.json gained {key!r}; #17 is tabletop only",
                    )
        flat = _text(CORE_JSON).lower()
        for tier in ("+1 to +3", "cyberdeck"):
            with self.subTest(tier=tier):
                self.assertNotIn(tier, flat)

    def test_godot_adapter_does_not_implement_the_modifiers(self) -> None:
        flat = _flat(GODOT_ADAPTER)
        for term in ("bci_modifier", "compute_modifier", "connection_modifier",
                     "infosec", "cyberspace"):
            with self.subTest(term=term):
                self.assertNotIn(term, flat)

    def test_concordia_mechanics_do_not_implement_the_modifiers(self) -> None:
        flat = _flat(CONCORDIA_MECHANICS)
        for term in ("bci_modifier", "compute_modifier", "connection_modifier",
                     "infosec", "cyberspace"):
            with self.subTest(term=term):
                self.assertNotIn(term, flat)

    def test_rulebook_defers_the_digital_port_explicitly(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("cyberspace and hacking modifiers in section 12.1", flat)
        self.assertIn("there is no runtime schema, modifier table", flat)

    def test_agents_md_records_the_deferral(self) -> None:
        flat = _flat(AGENTS)
        self.assertIn("cyberspace modifiers are tabletop-first and not yet ported", flat)
        self.assertIn("§5.3 and §12.1", flat)


if __name__ == "__main__":
    unittest.main()
