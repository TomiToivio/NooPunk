# -*- coding: utf-8 -*-
"""Regression guard: RULEBOOK.md's precedence over the CWN chassis.

PR #21 landed `tests/test_issue19_cwn_chassis.py`, whose `PrecedenceTests` check
that the rule is stated in `docs/CWN_CHASSIS.md` and `AGENTS.md`. They never check
`RULEBOOK.md` — which is the **canonical rules source** for NoöPunk.

The consequence was verified by sabotage against a clean `main` (`3888fe2`)
before this file existed. Replacing RULEBOOK.md's sentence

    Existing NoöPunk rules in this rulebook take precedence over CWN defaults.

with the inverted claim

    CWN defaults take precedence over existing NoöPunk rules.

left the whole suite **green (128 passed)**. The load-bearing claim of #19 — that
adopting a third-party chassis must not displace author-specified NoöPunk rules —
was reversible in the one document that actually defines the rules.

This is a STRUCTURE guard: it constrains what RULEBOOK.md *says*, not how anyone
implements a rule. It deliberately does not pin the review table's rows, which are
DEFER-by-default and the author's to decide.
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = ROOT / "RULEBOOK.md"

#: U+2212 MINUS SIGN is used in the policy doc; RULEBOOK.md uses an ASCII hyphen.
_MINUS = "\u2212"


def _flat(path: Path) -> str:
    """Lowercased, whitespace-collapsed, minus-normalised text."""
    return " ".join(path.read_text(encoding="utf-8").split()).lower().replace(_MINUS, "-")


def _chassis_section() -> str:
    """RULEBOOK's chassis subsection (§18.1), so checks cannot be satisfied elsewhere."""
    text = RULEBOOK.read_text(encoding="utf-8")
    marker = "### 18.1 Open mechanical chassis"
    start = text.find(marker)
    if start == -1:
        raise AssertionError("RULEBOOK.md §18.1 'Open mechanical chassis' not found")
    rest = text[start + len(marker):]
    end = rest.find("\n## ")
    return (rest if end == -1 else rest[:end]).lower()


class RulebookPrecedenceTests(unittest.TestCase):
    """RULEBOOK.md must state precedence and must never state the inverse."""

    def test_rulebook_states_precedence(self) -> None:
        self.assertIn("take precedence over cwn defaults", _flat(RULEBOOK))

    def test_the_chassis_section_carries_the_rule(self) -> None:
        """It must be in the chassis section, not only somewhere else in the file."""
        self.assertIn("take precedence", _chassis_section())

    def test_rulebook_never_says_the_chassis_wins(self) -> None:
        text = _flat(RULEBOOK)
        for inverted in (
            "cwn defaults take precedence over existing noöpunk rules",
            "cwn takes precedence",
            "cwn overrides",
            "cwn supersedes",
            "cwn takes priority",
        ):
            with self.subTest(inverted=inverted):
                self.assertNotIn(inverted, text)

    def test_the_chassis_section_never_inverts_the_rule(self) -> None:
        section = _chassis_section()
        self.assertNotIn("cwn defaults take precedence", section)
        self.assertNotIn("cwn takes precedence", section)

    def test_rulebook_keeps_the_chassis_non_canonical(self) -> None:
        section = _chassis_section()
        self.assertIn("open mechanical", section)
        # it is a review reference, not an automatic source of the rule
        self.assertIn("not an automatic source", section)


class AuthorRulesStillGuardTests(unittest.TestCase):
    """The rules the chassis must not displace, asserted where they live."""

    def test_rulebook_preserves_the_modifier_range(self) -> None:
        self.assertIn("-3..+3", _flat(RULEBOOK))

    def test_rulebook_preserves_the_six_attributes(self) -> None:
        text = _flat(RULEBOOK)
        for attribute in ("fit", "ref", "int", "cha", "cyb", "psy"):
            with self.subTest(attribute=attribute):
                self.assertIn(f"({attribute})", text)


if __name__ == "__main__":
    unittest.main()
