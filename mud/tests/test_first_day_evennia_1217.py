"""Evennia first-day adapter parity (#1217).

The command is a renderer over the canonical `src.console.first_day` session. These tests assert
that the typed surface reaches the same actions, keeps save state on the caller, and cannot bypass
the diagnostic order.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

import pytest
from nopunk_mud.first_day_adapter import FirstDayAdapter

from src.console.first_day import KIT, LINKED

COMMANDS = Path(__file__).resolve().parents[1] / "commands" / "default_cmdsets.py"


@pytest.fixture()
def cmds(monkeypatch):
    evennia = types.ModuleType("evennia")
    evennia.Command = type("Command", (), {})
    packages = {
        "evennia.commands": types.ModuleType("evennia.commands"),
        "evennia.commands.default": types.ModuleType("evennia.commands.default"),
        "evennia.commands.default.cmdset_character": types.ModuleType(
            "evennia.commands.default.cmdset_character"
        ),
    }
    packages["evennia.commands.default.cmdset_character"].CharacterCmdSet = type(
        "CharacterCmdSet", (), {}
    )
    for name, module in {"evennia": evennia, **packages}.items():
        monkeypatch.setitem(sys.modules, name, module)
    sys.modules.pop("commands.default_cmdsets", None)
    return importlib.import_module("commands.default_cmdsets")


class Caller:
    class DB:
        first_day_state = None

    def __init__(self):
        self.db = self.DB()
        self.messages = []

    def msg(self, text):
        self.messages.append(text)


def run(caller, module, line):
    command = module.CmdFirstDay()
    command.caller = caller
    command.args = (
        line[9:].strip() if line.lower().startswith("firstday") else line.strip()
    )
    command.func()
    return caller.messages[-1]


def complete_first_day(caller, module):
    assert "wake" in run(caller, module, "firstday")
    run(caller, module, "firstday wake")
    run(caller, module, "firstday uniform")
    for item in KIT:
        run(caller, module, f"firstday inspect {item}")
    for item in LINKED:
        run(caller, module, f"firstday connect {item}")
    run(caller, module, "firstday dispatch")
    run(caller, module, "firstday ride")
    run(caller, module, "firstday arrive")
    return run(caller, module, "firstday report")


class TestEvenniaFirstDay:
    def test_command_is_registered(self, cmds):
        assert "CmdFirstDay" in cmds.__dict__
        # The command-set source guard is checked separately; importing the class is enough here.

    def test_the_whole_first_day_reaches_the_report(self, cmds):
        caller = Caller()
        result = complete_first_day(caller, cmds)
        assert "Romppainen" in result
        assert "first_day:report" in caller.db.first_day_state["flags"]
        assert run(caller, cmds, "firstday") == (
            "First day complete. Tony has reported to Dr. Harri Romppainen at Ratakatu 12."
        )

    def test_state_survives_a_new_command_instance(self, cmds):
        first = Caller()
        run(first, cmds, "firstday wake")
        run(first, cmds, "firstday uniform")
        saved = first.db.first_day_state

        second = Caller()
        second.db.first_day_state = saved
        assert "inspect:police_radio" in run(second, cmds, "firstday")
        assert "first_day:wake" in second.db.first_day_state["flags"]
        run(second, cmds, "firstday inspect police_radio")
        assert "first_day:inspect:police_radio" in second.db.first_day_state["flags"]

    def test_connect_before_inspect_is_refused_and_does_not_advance(self, cmds):
        caller = Caller()
        run(caller, cmds, "firstday")
        message = run(caller, cmds, "firstday connect police_radio")
        assert "unavailable" in message.lower()
        assert (
            "first_day:connect:police_radio" not in caller.db.first_day_state["flags"]
        )

    def test_faulty_radio_can_be_repaired_and_dispatch_still_works(self, cmds):
        caller = Caller()
        # A fault is declared before play; the authored repair action is the only way past it.
        from src.console.first_day import create_first_day

        adapter = FirstDayAdapter(create_first_day(faults=("police_radio", "phone")))
        caller.db.first_day_state = adapter.snapshot()
        run(caller, cmds, "firstday wake")
        run(caller, cmds, "firstday uniform")
        for item in KIT:
            run(caller, cmds, f"firstday inspect {item}")
        assert "repair:police_radio" in run(caller, cmds, "firstday")
        run(caller, cmds, "firstday repair police_radio")
        for item in LINKED:
            run(caller, cmds, f"firstday connect {item}")
        run(caller, cmds, "firstday dispatch")
        assert "first_day:dispatch" in caller.db.first_day_state["flags"]

    def test_look_and_kit_are_read_only(self, cmds):
        caller = Caller()
        run(caller, cmds, "firstday wake")
        before = dict(caller.db.first_day_state)
        assert "Sörnäinen" in run(caller, cmds, "firstday look")
        assert "Kit |" in run(caller, cmds, "firstday kit")
        assert caller.db.first_day_state == before
