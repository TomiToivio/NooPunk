"""Every command defined for the MUD must actually be reachable (#985).

`CmdAssess` — the Romppainen consciousness assessment — was written, tested and imported, but never added to
`NoopunkCharacterCmdSet`, so the whole procedure was unreachable in play. Tests passed because they called
`run_case()` directly; nothing checked that a player could type the command.

This reads the command-set source with `ast` rather than importing it, so the guard needs no Evennia install
and cannot be defeated by an import error.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

COMMANDS = Path(__file__).resolve().parents[1] / "commands" / "default_cmdsets.py"


def _module() -> ast.Module:
    return ast.parse(COMMANDS.read_text(encoding="utf-8"), filename=str(COMMANDS))


def defined_commands() -> set[str]:
    """Every `class Cmd*` in the command-set module."""
    return {node.name for node in ast.walk(_module())
            if isinstance(node, ast.ClassDef) and node.name.startswith("Cmd")}


def registered_commands() -> set[str]:
    """Every `self.add(Cmd*())` call in the command-set module."""
    added = set()
    for node in ast.walk(_module()):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute) or func.attr != "add":
            continue
        for argument in node.args:
            if (isinstance(argument, ast.Call) and isinstance(argument.func, ast.Name)
                    and argument.func.id.startswith("Cmd")):
                added.add(argument.func.id)
    return added


class CommandRegistrationTests(unittest.TestCase):
    def test_the_module_defines_commands(self) -> None:
        self.assertTrue(defined_commands(), "the command-set module should define commands")

    def test_every_defined_command_is_registered(self) -> None:
        missing = defined_commands() - registered_commands()
        self.assertEqual(missing, set(),
                         f"defined but never added to the command set, so unreachable in play: "
                         f"{sorted(missing)}")

    def test_every_registered_command_is_defined(self) -> None:
        """The reverse direction: adding a command that does not exist would be a NameError at load."""
        unknown = registered_commands() - defined_commands()
        self.assertEqual(unknown, set(), f"added but not defined: {sorted(unknown)}")

    def test_the_consciousness_assessment_is_reachable(self) -> None:
        """#985: the procedure was implemented and unreachable. Pin it."""
        self.assertIn("CmdAssess", registered_commands())


if __name__ == "__main__":
    unittest.main()
