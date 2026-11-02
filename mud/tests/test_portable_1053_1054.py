"""Golden campaign and framework-independent API checks for #1053/#1054."""
from __future__ import annotations

import importlib
import tempfile
import unittest
from pathlib import Path

from nopunk_mud.portable import Command, PortableSession, resolve_cwn_check


class PortableTests(unittest.TestCase):
    def test_complete_and_save_resume(self):
        game = PortableSession()
        self.assertFalse(game.execute(Command("accept", "UNSA safehouse")).finished)
        game.execute(Command("interview", "Kurvi"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "save.json"
            game.save(path)
            resumed = PortableSession.restore(path)
            self.assertEqual(game.state, resumed.state)
            resumed.execute(Command("report", "UNSA safehouse"))
            result = resumed.execute(Command("submit", "UNSA safehouse"))
            self.assertTrue(result.finished)
            self.assertEqual(result.state["campaign"]["completed"], ["Missing Researcher"])

    def test_invalid_actions_do_not_mutate(self):
        session = PortableSession()
        before = session.state
        session.execute(Command("submit", "Kurvi"))
        self.assertEqual(before, session.state)

    def test_published_check_delegation(self):
        from nopunk_mud.cwn_core import skill_check
        a = resolve_cwn_check(1, 12, 8, dice=(3, 4))
        b = skill_check(1, 12, 8, dice=(3, 4))
        self.assertEqual(a, b)

    def test_no_optional_framework_imports(self):
        import nopunk_mud.portable as portable
        import inspect
        source = inspect.getsource(portable)
        for framework in ("import evennia", "import pygame", "import concordia"):
            self.assertNotIn(framework, source)

    def test_importable_api(self):
        self.assertIsNotNone(importlib.import_module("nopunk_mud.portable").PortableSession)


if __name__ == "__main__":
    unittest.main()
