"""Presentation must not become a second rules implementation."""
import importlib
import unittest
from portable_noopunk import Game, Action
from portable_noopunk.adapters import LocalAdapter

SEQUENCE = ("briefing", "go_library", "catalogue_record", "go_hq",
            "go_hospital", "examine_room", "interview_witness", "conclude")


class InterfaceContractTests(unittest.TestCase):
    def test_all_frontends_import_without_optional_dependencies(self):
        for name in ("web", "nicegui", "textual"):
            importlib.import_module("portable_noopunk.interfaces." + name)

    def test_browser_renders_escaped_state_and_allowed_actions(self):
        from portable_noopunk.interfaces.web import render
        adapter = LocalAdapter(Game())
        page = render(adapter, '<script>alert("x")</script>')
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn('<script>alert', page)
        self.assertIn('name="action" value="briefing"', page)

    def test_browser_actions_match_direct_library_outcomes(self):
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
