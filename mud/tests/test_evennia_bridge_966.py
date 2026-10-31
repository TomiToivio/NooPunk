"""The bridge between Evennia and the arc, tested without Evennia (#966).

The command layer runs inside the server; this module is the part that can be tested anywhere — including CI,
where Evennia is not installed. It covers the bug the server found: Evennia's `db` dicts are `_SaverDict`
mappings, not `dict` subclasses, and a bridge that tests `isinstance(..., dict)` loses the player's progress on
every command.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import sys
import unittest
from collections.abc import MutableMapping
from pathlib import Path

MUD = Path(__file__).resolve().parents[1]
ROOT = MUD.parent
sys.path.insert(0, str(MUD))

from nopunk_mud import kernel_resolver  # noqa: E402
from nopunk_mud.evennia_bridge import ArcBridge  # noqa: E402


class SaverDict(MutableMapping):
    """Stands in for Evennia's `_SaverDict`: a Mapping that is deliberately not a dict subclass."""

    def __init__(self, data=None):
        self._data = dict(data or {})

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class FakeDB:
    def __init__(self):
        self.solo_arc = None


class FakeCharacter:
    def __init__(self):
        self.db = FakeDB()


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.character = FakeCharacter()
        self.bridge = ArcBridge(self.character, kernel_resolver.Resolver.for_recruit())

    def play(self, *lines):
        for line in lines:
            self.bridge.handle(line)

    def test_a_fresh_character_starts_at_the_briefing(self):
        self.assertIn("[briefing]", self.bridge.prompt())

    def test_progress_survives_a_saverdict(self):
        """The exact failure the server found: Mapping, not dict."""
        self.play("accept")
        self.character.db.solo_arc = SaverDict(self.character.db.solo_arc)
        self.play("interview")
        self.assertIn(self.character.db.solo_arc["stage"], ("records",))

    def test_the_whole_arc_can_be_played_and_the_ending_recorded(self):
        self.play("accept", "interview", "leave", "records", "press", "submit")
        arc = dict(self.character.db.solo_arc)
        self.assertEqual(arc["stage"], "complete")
        self.assertIn(arc["ending"], {"corroborated", "corroborated_with_gaps", "partial", "unsolved"})

    def test_an_unavailable_action_is_refused_without_moving(self):
        before = dict(self.character.db.solo_arc or {"stage": "briefing"})
        reply = self.bridge.handle("submit")
        self.assertIn("unavailable", reply.lower())
        after = dict(self.character.db.solo_arc or {"stage": "briefing"})
        self.assertEqual(before["stage"], after["stage"])

    def test_a_finished_case_offers_no_actions(self):
        self.play("accept", "interview", "leave", "records", "press", "submit")
        self.assertNotIn("Available:", self.bridge.prompt())

    def test_the_sheet_is_the_sheet_the_checks_use(self):
        text = self.bridge.handle("sheet")
        self.assertIn("INT 13", text)
        self.assertIn("Notice", text)

    def test_nonsense_does_not_raise(self):
        for line in ("", "   ", "dance", "interview now please"):
            self.bridge.handle(line)

    def test_the_bridge_imports_no_evennia(self):
        source = (MUD / "nopunk_mud" / "evennia_bridge.py").read_text()
        self.assertNotIn("import evennia", source.replace("imports **no Evennia**", ""))
        self.assertNotIn("from evennia", source)


if __name__ == "__main__":
    unittest.main()
