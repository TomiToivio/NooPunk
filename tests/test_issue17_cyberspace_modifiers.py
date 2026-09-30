# -*- coding: utf-8 -*-
"""Issue #17 — the human-user cyberspace modifier framework, as **withdrawn**.

#17 specified a situational modifier stack for human cyberspace actions: **BCI**,
**Compute**, **Connection** and **Infosec**. Issue #25 **withdrew that framework
from active canon** and returned hacking / cyberspace to **DEFER**, pending a later
conversion onto CWN's own hacking subsystem.

The guards are therefore inverted rather than removed. Deleting the file that
noticed the stack would be how a withdrawn rule quietly comes back, so what is
pinned here is:

1. **The withdrawal exists and is explicit.** The rulebook must still *name* the four
   categories — as withdrawn — rather than silently dropping them, so a reader
   arriving from #17 learns what happened instead of assuming the rules never
   existed.
2. **It is a withdrawal, not a rejection.** The concepts are explicitly kept
   available as future design ideas.
3. **Hacking is DEFER, not solved.** The withdrawal must not be misread as an author
   decision that hacking is designed.
4. **The modifiers cannot come back silently** — not into a check, not into
   `data/rules/core.json`, not into any adapter.
5. **The non-human deferral survives**, independent of the human-user stack.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = ROOT / "RULEBOOK.md"
AGENTS = ROOT / "AGENTS.md"
POLICY = ROOT / "docs" / "CWN_CHASSIS.md"
CORE_JSON = ROOT / "data" / "rules" / "core.json"
GODOT_ADAPTER = ROOT / "src" / "godot" / "core_rules.gd"
CONCORDIA_MECHANICS = ROOT / "src" / "concordia_runtime" / "mechanics.py"
CORE_PY = ROOT / "src" / "rules" / "core.py"

#: The four categories #17 introduced. They must still be *named* in the withdrawal.
CATEGORIES = ("bci", "compute", "connection", "infosec")

#: Terms that would indicate the withdrawn tier tables were re-canonised.
WITHDRAWN_TIER_TERMS = ("**+1 to +3**", "quality | modifier", "poor / obsolete")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(path: Path) -> str:
    """Lowercased, whitespace-collapsed, emphasis stripped.

    Emphasis must go: the withdrawal writes phrases like \"is **no longer**
    canonical\", and a naive substring search misses the sentence carrying the rule.
    """
    return " ".join(_text(path).replace("*", "").split()).lower()


def _section_12_1() -> str:
    text = _text(RULEBOOK)
    start = text.index("### 12.1")
    end = text.index("## 13.")
    return " ".join(text[start:end].replace("*", "").split()).lower()


class WithdrawalTests(unittest.TestCase):
    """The framework must be documented as withdrawn, by name."""

    def test_the_withdrawal_is_stated(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("withdrawn", flat)
        self.assertIn("no longer canonical", flat)

    def test_every_category_is_still_named(self) -> None:
        """A reader arriving from #17 must learn what happened to the four categories."""
        section = _section_12_1()
        for category in CATEGORIES:
            with self.subTest(category=category):
                self.assertIn(category, section)

    def test_the_section_heading_marks_it_withdrawn(self) -> None:
        self.assertIn("withdrawn", _text(RULEBOOK)[
            _text(RULEBOOK).index("### 12.1"):_text(RULEBOOK).index("## 13.")
        ].lower())

    def test_the_original_issue_is_referenced(self) -> None:
        self.assertIn("#17", _text(RULEBOOK))

    def test_the_withdrawn_tier_tables_are_gone(self) -> None:
        """The tier tables were the operative part; they must not survive."""
        section = _text(RULEBOOK)[
            _text(RULEBOOK).index("### 12.1"):_text(RULEBOOK).index("## 13.")
        ]
        for term in WITHDRAWN_TIER_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, section)

    def test_no_check_still_combines_the_four_modifiers(self) -> None:
        """The withdrawn formula must not survive as an active check structure."""
        flat = _flat(RULEBOOK)
        for term in ("+ bci modifier", "+ compute modifier",
                     "+ connection modifier", "+ infosec modifier"):
            with self.subTest(term=term):
                self.assertNotIn(term, flat)


class NotRejectionTests(unittest.TestCase):
    """Withdrawn from canon, but explicitly available as future design."""

    def test_concepts_are_kept_as_future_design(self) -> None:
        section = _section_12_1()
        self.assertIn("future design", section)
        self.assertIn("not a rejection", section)

    def test_the_concepts_are_named_as_possible_returnees(self) -> None:
        section = _section_12_1()
        self.assertIn("may return later", section)

    def test_the_withdrawal_names_where_the_old_wording_lives(self) -> None:
        """The history is kept in git, and the doc says so."""
        self.assertIn("git history", _section_12_1())


class HackingStillDeferredTests(unittest.TestCase):
    """Withdrawing the stack is not deciding hacking."""

    def test_hacking_is_still_unspecified(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("hacking is unspecified", flat)

    def test_hacking_is_marked_defer(self) -> None:
        policy = _flat(POLICY)
        self.assertIn("hacking", policy)
        self.assertIn("defer", policy)

    def test_the_chassis_matrix_has_a_hacking_row(self) -> None:
        text = _text(POLICY)
        status = text[text.index("### Review status"):text.index("## NoöPunk decisions")]
        rows = {}
        for line in status.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip().replace("*", "") for c in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0]:
                rows[cells[0].lower()] = cells[1].upper()
        hacking = {k: v for k, v in rows.items() if "hacking" in k}
        self.assertEqual(len(hacking), 1, f"expected one hacking row, got {hacking}")
        self.assertEqual(next(iter(hacking.values())), "DEFER")

    def test_the_chassis_row_records_the_withdrawal(self) -> None:
        flat = _flat(POLICY)
        self.assertIn("withdrawn from active canon", flat)
        self.assertIn("bci", flat)

    def test_hacking_is_not_claimed_as_designed(self) -> None:
        section = _section_12_1()
        self.assertIn("hacking itself remains", section)


class NonHumanDeferralTests(unittest.TestCase):
    """The non-human deferral is separate from the human-user stack."""

    def test_deferral_heading_survives(self) -> None:
        self.assertIn("deferred: non-human cyberspace participants", _flat(RULEBOOK))

    def test_the_deferral_names_the_participants(self) -> None:
        flat = _flat(RULEBOOK)
        for participant in ("ai-native entities", "uploaded humans",
                            "autonomous software agents"):
            with self.subTest(participant=participant):
                self.assertIn(participant, flat)

    def test_the_deferral_is_not_inferable(self) -> None:
        self.assertIn("must not be inferred", _section_12_1())


class NoReEntryTests(unittest.TestCase):
    """The withdrawn modifiers must not reappear in canon or a runtime."""

    def test_core_json_has_no_cyberspace_modifier_schema(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        for key in canon:
            with self.subTest(key=key):
                lowered = key.lower()
                for forbidden in ("bci", "compute", "connection", "infosec"):
                    self.assertNotIn(forbidden, lowered)

    def test_no_runtime_implements_the_modifiers(self) -> None:
        for path in (GODOT_ADAPTER, CONCORDIA_MECHANICS, CORE_PY):
            with self.subTest(path=path.name):
                flat = _flat(path)
                for forbidden in ("bci", "infosec"):
                    self.assertNotIn(forbidden, flat,
                                     f"{path.name} implements a withdrawn modifier")

    def test_agents_rules_forbid_reintroduction(self) -> None:
        flat = _flat(AGENTS)
        self.assertIn("withdrawn", flat)
        self.assertIn("do not add those modifiers", flat)

    def test_the_withdrawal_forbids_runtime_reintroduction(self) -> None:
        section = _section_12_1()
        self.assertIn("do not", section)
        self.assertIn("reintroduce", section)


class PortDebtTests(unittest.TestCase):
    """#17's old 'not yet ported' guarantee is replaced by explicit port debt."""

    def test_rulebook_records_the_port_debt(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("port debt", flat)

    def test_agents_records_the_port_debt(self) -> None:
        self.assertIn("port debt", _flat(AGENTS))


if __name__ == "__main__":
    unittest.main()
