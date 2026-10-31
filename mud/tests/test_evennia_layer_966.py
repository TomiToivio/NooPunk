"""The Evennia command layer boots and plays the solo case (#966).

The issue's first item is not "the engine works" — that is tested headless — but "a logged-in player can reach
it". This runs inside Evennia's own harness: real typeclasses, real attributes, real cmdsets, real command
dispatch. If the game directory is broken, this fails.

Commands are invoked the way the parser invokes them (`caller`, `args`, `func()`); Evennia 5's `EvenniaTest.call`
helper takes a command instance, not a typed line.

Skipped when Evennia is not installed, which is the case in the repository's CI:

    cd mud && /path/to/evennia-python -m django test tests.test_evennia_layer_966 \
        --settings=server.conf.settings

`pip install evennia && mkdir -p server/logs && evennia migrate` is what makes this runnable.
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
    def play(self, line: str) -> None:
        """Invoke the real command the way the parser does."""
        from commands.default_cmdsets import CmdSolo

        cmd = CmdSolo()
        cmd.caller = self.char1
        cmd.args = line
        cmd.func()

    def merged_keys(self) -> set[str]:
        keys: set[str] = set()
        for cmdset in self.char1.cmdset.get():
            keys.update(cmd.key for cmd in cmdset.commands)
        return keys

    def test_the_solo_command_is_registered_on_a_character(self):
        keys = self.merged_keys()
        self.assertIn("solo", keys)
        self.assertIn("case", keys)

    def test_a_player_can_take_the_first_step_of_the_case(self):
        self.play("look")
        self.play("status")
        state = self.char1.db.unsa_solo_state
        self.assertIsNotNone(state, "the solo state was not persisted on the character")

    def test_state_survives_between_commands(self):
        self.play("look")
        first = dict(self.char1.db.unsa_solo_state)
        self.play("status")
        second = dict(self.char1.db.unsa_solo_state)
        self.assertEqual(first.get("location"), second.get("location"))

    def test_the_command_layer_refuses_to_write_files(self):
        """`save <path>` exists in the CLI; from a player connection it would be a server-file write."""
        import os
        import tempfile

        target = os.path.join(tempfile.gettempdir(), f"should-not-exist-966-{os.getpid()}.json")
        if os.path.exists(target):
            os.remove(target)   # a previous failed run must not make this test lie
        self.play(f"save {target}")
        self.assertFalse(os.path.exists(target), "the command wrote a server-side file from player input")

    def test_an_unknown_verb_does_not_crash_the_session(self):
        self.play("dance wildly")


if __name__ == "__main__":
    unittest.main()
