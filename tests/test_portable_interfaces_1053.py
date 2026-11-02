"""Presentation must not become a second rules implementation (#1053, #1054)."""

from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from portable_noopunk import Action, Game  # noqa: E402
from portable_noopunk.adapters import LocalAdapter  # noqa: E402

SEQUENCE = ("look", "go:corridor", "go:reception", "go:patient_room",
            "theory:deliberate_falsification", "support:duty-roster", "support:record-1601",
            "conclude:deliberate_falsification")


class InterfaceContractTests(unittest.TestCase):
    def test_all_frontends_import_without_optional_dependencies(self) -> None:
        for name in ("web", "nicegui", "textual"):
            importlib.import_module("portable_noopunk.interfaces." + name)

    def test_browser_renders_escaped_state_and_allowed_actions(self) -> None:
        from portable_noopunk.interfaces.web import render

        adapter = LocalAdapter(Game())
        page = render(adapter, '<script>alert("x")</script>')
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn('<script>alert', page)
        # The first offered action is the real case's own first verb, not an invented briefing.
        self.assertIn('name="action" value="look"', page)

    def test_no_frontend_invents_case_content(self) -> None:
        from portable_noopunk.interfaces.web import render

        page = render(LocalAdapter(Game()))
        for invented in ("unsa_hq", "catalogue_record", "examine_room", "interview_witness",
                         "sidequest"):
            self.assertNotIn(invented, page)

    def test_browser_actions_match_direct_library_outcomes(self) -> None:
        from portable_noopunk.interfaces.web import render

        direct = Game()
        adapter = LocalAdapter(Game())
        for command in SEQUENCE:
            self.assertEqual(adapter.dispatch(command), direct.apply(Action(command)))
            self.assertEqual(adapter.save(), direct.to_json())
            render(adapter)
        self.assertTrue(adapter.snapshot()["finished"])


if __name__ == "__main__":
    unittest.main()
