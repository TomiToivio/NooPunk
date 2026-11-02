"""Cross-adapter parity for the typed campaign session (#1053, #1054).

The architecture decision says an adapter may render state but may not decide it. These
tests replay one seeded UNSA case through three surfaces — the campaign engine directly,
the typed `CampaignSession`, and the Evennia `CmdSolo` command — and compare **state
documents**, not prose. If an adapter ever holds a rule the others do not, the documents
diverge and this fails.

Runs without Evennia installed: the command module is imported with a minimal stub, the
same technique the existing `test_evennia_solo_bridge_950.py` uses.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

import pytest
from nopunk_mud.campaign import CampaignEngine
from nopunk_mud.session import Action, CampaignSession

#: The authored shortest legal path: two independent clues, then the report.
SOLVE = (
    "go street", "go university", "examine terminal", "go street", "go kurvi",
    "talk witness", "ask witness badge", "examine woman in the raincoat",
    "go street", "go safehouse", "report",
)


@pytest.fixture()
def evennia_cmds(monkeypatch):
    """Import the Evennia command module with the framework stubbed out."""
    evennia = types.ModuleType("evennia")
    evennia.Command = type("Command", (), {})
    commands_pkg = types.ModuleType("evennia.commands")
    default_pkg = types.ModuleType("evennia.commands.default")
    character = types.ModuleType("evennia.commands.default.cmdset_character")
    character.CharacterCmdSet = type("CharacterCmdSet", (), {})
    for name, module in (
        ("evennia", evennia),
        ("evennia.commands", commands_pkg),
        ("evennia.commands.default", default_pkg),
        ("evennia.commands.default.cmdset_character", character),
    ):
        monkeypatch.setitem(sys.modules, name, module)
    sys.modules.pop("commands.default_cmdsets", None)
    return importlib.import_module("commands.default_cmdsets")


class _Caller:
    class _DB:
        unsa_solo_state = None

    def __init__(self) -> None:
        self.db = self._DB()
        self.messages: list[str] = []

    def msg(self, text: str) -> None:
        self.messages.append(text)


def _play_evennia(module, script) -> tuple[_Caller, list[str]]:
    caller = _Caller()
    for line in script:
        command = module.CmdSolo()
        command.caller = caller
        command.args = line
        command.func()
    return caller, caller.messages


class TestEngineAndSessionAgree:
    def test_the_same_script_gives_identical_text_and_state(self):
        engine = CampaignEngine(seed=7)
        expected = [engine.command(line) for line in SOLVE]

        session = CampaignSession()
        results = [session.execute(Action(line)) for line in SOLVE]

        assert [result.text for result in results] == expected
        assert dict(results[-1].state) == engine.to_dict()
        assert results[-1].finished is True

    def test_a_saved_session_resumes_where_the_engine_stopped(self, tmp_path: Path):
        session = CampaignSession()
        for line in SOLVE[:3]:
            session.execute(Action(line))
        save = tmp_path / "case.json"
        session.save(save)

        restored = CampaignSession.load(save)
        assert restored.state == session.state
        for line in SOLVE[3:]:
            restored.execute(Action(line))

        engine = CampaignEngine(seed=7)
        for line in SOLVE:
            engine.command(line)
        assert restored.state == engine.to_dict()

    def test_a_state_document_is_a_snapshot_not_a_live_view(self):
        """A session result or save callback must not watch the engine rewrite its history."""
        engine = CampaignEngine(seed=7)
        document = engine.to_dict()
        engine.command("go street")
        assert document["location"] == "safehouse"
        assert document["clues"] == []
        assert engine.to_dict()["location"] == "street"

    def test_a_rejected_command_does_not_change_state(self):
        session = CampaignSession()
        before = session.state
        result = session.execute(Action("dance wildly"))
        assert [event.kind for event in result.events] == ["rejected"]
        assert dict(result.state) == before


class TestEvents:
    def test_movement_emits_a_location_event(self):
        session = CampaignSession()
        result = session.execute(Action("go street"))
        moved = [event for event in result.events if event.kind == "location_changed"]
        assert moved and moved[0].detail["to"] == "street"

    def test_a_new_clue_and_the_ending_are_events_not_guesses(self):
        session = CampaignSession()
        clue_events = []
        ending_events = []
        for line in SOLVE:
            result = session.execute(Action(line))
            clue_events += [e for e in result.events if e.kind == "clue_gained"]
            ending_events += [e for e in result.events if e.kind == "ending_reached"]

        assert [event.detail["clue"] for event in clue_events] == ["access_log", "witness_badge"]
        assert ending_events and ending_events[0].detail["ending"] == "solved"


class TestEvenniaAdapterParity:
    def test_the_mud_command_produces_the_same_state_document(self, evennia_cmds):
        session = CampaignSession()
        for line in SOLVE:
            session.execute(Action(line))

        caller, messages = _play_evennia(evennia_cmds, SOLVE)

        assert messages  # the adapter rendered text
        assert caller.db.unsa_solo_state is not None
        assert caller.db.unsa_solo_state == session.state
        assert caller.db.unsa_solo_state["ending"] == "solved"

    def test_the_mud_command_refuses_a_player_supplied_save_path(self, evennia_cmds, tmp_path: Path):
        caller = _Caller()
        target = tmp_path / "should-not-exist.json"
        command = evennia_cmds.CmdSolo()
        command.caller = caller
        command.args = f"save {target}"
        command.func()

        assert not target.exists()
        assert "saved automatically" in caller.messages[-1]
        assert caller.db.unsa_solo_state is None


def test_the_session_module_imports_no_engine():
    """The typed boundary belongs to the domain layer, so it imports no front-end."""
    import subprocess

    root = Path(__file__).resolve().parents[2]
    code = (
        "import sys;"
        "import nopunk_mud.session;"
        "blocked=[m for m in sys.modules if m.split('.')[0] in "
        "{'evennia','twisted','django','pygame','mesa','concordia'}];"
        "print(blocked);"
        "raise SystemExit(1 if blocked else 0)"
    )
    completed = subprocess.run([sys.executable, "-c", code], cwd=root / "mud",
                               capture_output=True, text=True, timeout=120, check=False)
    assert completed.returncode == 0, completed.stdout + completed.stderr
