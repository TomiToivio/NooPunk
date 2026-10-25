"""The interpreter gate must explain itself, and must not lie about the version.

Issue #561's first acceptance criterion is that a player can launch the scenario from a clean
checkout using the documented commands. On an older interpreter the game could not start at all,
and said so with a bare ``ImportError: cannot import name 'StrEnum'`` raised from inside the rules
layer — a message that names neither the interpreter nor a remedy.

These tests check the gate's own behaviour, which is executable code, not prose:

* it refuses a version below the minimum and says the version it found;
* it allows the minimum and anything above it;
* the explanation names the minimum, the tested version and at least one concrete command.

The gate is exercised with an explicit minimum rather than by pretending to be on an old
interpreter, because the point is the comparison, not the process it runs in.
"""
from __future__ import annotations

import sys
import unittest

from strategy_game import interpreter


class GateTests(unittest.TestCase):
    """`require` compares the running interpreter against a minimum."""

    def test_an_impossible_minimum_is_refused(self) -> None:
        with self.assertRaises(interpreter.UnsupportedInterpreter):
            interpreter.require((99, 0))

    def test_the_supported_minimum_is_allowed(self) -> None:
        self.assertGreaterEqual(sys.version_info[:2], interpreter.MINIMUM,
                                "this test must run on a supported interpreter")
        interpreter.require(interpreter.MINIMUM)  # must not raise

    def test_an_ancient_minimum_is_allowed(self) -> None:
        interpreter.require((3, 0))  # must not raise

    def test_the_refusal_names_the_version_found(self) -> None:
        try:
            interpreter.require((99, 0))
        except interpreter.UnsupportedInterpreter as exc:
            self.assertEqual(exc.found, interpreter.found_version())
            self.assertIn(f"{exc.found[0]}.{exc.found[1]}", str(exc))
        else:  # pragma: no cover
            self.fail("the gate did not refuse an impossible minimum")


class MessageTests(unittest.TestCase):
    """The explanation has to be actionable, not just accurate."""

    def test_the_message_names_the_minimum_and_the_tested_version(self) -> None:
        text = interpreter.message()
        minimum = f"{interpreter.MINIMUM[0]}.{interpreter.MINIMUM[1]}"
        self.assertIn(minimum, text)
        self.assertIn(interpreter.TESTED, text)

    def test_the_message_explains_the_missing_symbols(self) -> None:
        """A player should learn *why*, not only that it failed."""
        text = interpreter.message()
        self.assertIn("StrEnum", text)

    def test_the_message_gives_a_concrete_command(self) -> None:
        """At least one runnable line, whatever the platform."""
        text = interpreter.message()
        self.assertTrue(
            "python3.12 -m venv" in text or "py -3.12 -m venv" in text,
            "the remedy must name a command the player can paste",
        )
        self.assertIn("--scenario ubiquitous-maniacs", text)

    def test_the_message_for_a_specific_error_uses_that_error(self) -> None:
        error = interpreter.UnsupportedInterpreter((3, 8))
        self.assertIn("3.8", interpreter.message(error))


if __name__ == "__main__":
    unittest.main()
