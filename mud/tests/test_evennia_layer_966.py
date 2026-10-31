"""The Evennia command layer boots and plays the arc (#966).

This is the test the issue asked for: not "the arc works" (already tested headless) but "a logged-in player can
reach it". It runs inside Evennia's own test harness — real typeclasses, real attributes, real cmdsets — so if
the game directory is broken, this fails.

Commands are invoked the way the parser invokes them (`caller`, `args`, `func()`), because Evennia 5's
`EvenniaTest.call()` helper takes a command instance rather than a typed line.

Skipped when Evennia is not installed, which is the case in the repository's CI. Run it with an Evennia-enabled
interpreter:

    cd mud && /path/to/evennia-python -m django test tests.test_evennia_layer_966 \
        --settings=server.conf.settings

The bridge itself is tested without Evennia in `tests/test_evennia_bridge_966.py`.
"""
from __future__ import annotations

import unittest

try:  # Evennia is a game-server dependency, not a CI dependency.
    from evennia.utils.test_resources import EvenniaTest
    HAVE_EVENNIA = True
except Exception:  # pragma: no cover - exercised only where Evennia is absent
    HAVE_EVENNIA = False
    EvenniaTest = object  # type: ignore[assignment,misc]


@unittest.skipUnless(HAVE_EVENNIA, "Evennia is not installed in this interpreter")
class CommandLayer(EvenniaTest):
    def play(self, verb: str, args: str = "") -> None:
        from commands.solo_arc_cmds import CmdAssignment

        cmd = CmdAssignment()
        cmd.caller = self.char1
        cmd.args = args
        cmd.func()

    def merged_keys(self) -> set[str]:
        keys: set[str] = set()
        for cmdset in self.char1.cmdset.get():
            keys.update(cmd.key for cmd in cmdset.commands)
        return keys

    def test_the_commands_are_registered_on_a_character(self):
        keys = self.merged_keys()
        self.assertIn("assignment", keys)
        self.assertIn("case", keys)
        self.assertIn("recruitsheet", keys)

    def test_a_player_can_play_the_arc_through_the_command(self):
        self.play("assignment", "accept")
        self.play("assignment", "interview")
        self.play("assignment", "leave")
        self.play("assignment", "records")
        self.play("assignment", "press")
        self.play("assignment", "submit")
        arc = dict(self.char1.db.solo_arc)   # Evennia hands back a _SaverDict, not a dict
        self.assertEqual(arc["stage"], "complete")
        self.assertTrue(arc["ending"])

    def test_state_is_persisted_on_the_character_between_commands(self):
        self.play("assignment", "accept")
        self.assertEqual(self.char1.db.solo_arc["stage"], "kurvi")
        self.char1.db.solo_arc = None
        self.play("assignment", "accept")
        self.assertEqual(self.char1.db.solo_arc["stage"], "kurvi")

    def test_an_unavailable_action_does_not_advance_the_stage(self):
        self.play("assignment", "submit")   # submit belongs to the report stage
        self.assertEqual((self.char1.db.solo_arc or {}).get("stage", "briefing"), "briefing")


if __name__ == "__main__":
    unittest.main()
