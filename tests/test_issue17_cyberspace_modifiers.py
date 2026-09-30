# -*- coding: utf-8 -*-
"""Regression guard for the issue #17 cyberspace-modifier experiment after #25.

Issue #25 explicitly withdraws the BCI / Compute / Connection / Infosec modifier
tables from active canon and returns hacking / cyberspace to DEFER while the later
CWN-derived hacking subsystem is designed.

The old concepts remain design history, not active mechanics.
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


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(path: Path) -> str:
    return " ".join(_text(path).replace("*", "").split()).lower()


class WithdrawnFrameworkTests(unittest.TestCase):
    def test_hacking_is_deferred(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("hacking / cyberspace is deferred", flat)
        self.assertIn("later cwn-based subsystem review", _flat(AGENTS))

    def test_old_modifier_tables_are_not_active_rules(self) -> None:
        text = _text(RULEBOOK)
        for heading in (
            "#### BCI modifier",
            "#### Compute modifier",
            "#### Connection modifier",
            "#### Infosec defence modifier",
        ):
            with self.subTest(heading=heading):
                self.assertNotIn(heading, text)

    def test_concepts_are_not_rejected(self) -> None:
        flat = _flat(RULEBOOK)
        for term in ("bci quality", "local compute", "connection quality", "infosec hardening"):
            with self.subTest(term=term):
                self.assertIn(term, flat)
        self.assertIn("concepts are not rejected", flat)

    def test_chassis_row_is_defer(self) -> None:
        text = _text(POLICY)
        status = text[text.index("### Review status"):text.index("## NoöPunk decisions")]
        self.assertRegex(status, r"(?m)^\| Hacking / cyberspace \| \*\*DEFER\*\* \|")

    def test_ai_and_uploaded_humans_remain_deferred(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("ai-native entities", flat)
        self.assertIn("uploaded humans", flat)
        self.assertIn("autonomous software agents", flat)


class NoDigitalPortTests(unittest.TestCase):
    def test_core_json_has_no_cyberspace_modifier_schema(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        for key in canon:
            lowered = key.lower()
            for forbidden in ("bci", "infosec", "connection_modifier", "compute_modifier"):
                with self.subTest(key=key, forbidden=forbidden):
                    self.assertNotIn(forbidden, lowered)

    def test_godot_does_not_implement_withdrawn_modifiers(self) -> None:
        flat = _flat(GODOT_ADAPTER)
        for term in ("bci_modifier", "compute_modifier", "connection_modifier", "infosec"):
            with self.subTest(term=term):
                self.assertNotIn(term, flat)

    def test_concordia_does_not_implement_withdrawn_modifiers(self) -> None:
        flat = _flat(CONCORDIA_MECHANICS)
        for term in ("bci_modifier", "compute_modifier", "connection_modifier", "infosec"):
            with self.subTest(term=term):
                self.assertNotIn(term, flat)


if __name__ == "__main__":
    unittest.main()
