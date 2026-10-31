"""Issue #950: Evennia-facing solo case persists without LLM, server, or Godot.

Stub only the Evennia command framework; exercise the actual command and engine.
"""
import importlib.util
import sys
import types
from pathlib import Path


def _load_commands(monkeypatch):
    evennia = types.ModuleType("evennia")
    evennia.Command = type("Command", (), {})
    cmdpkg = types.ModuleType("evennia.commands")
    defaultpkg = types.ModuleType("evennia.commands.default")
    character = types.ModuleType("evennia.commands.default.cmdset_character")
    character.CharacterCmdSet = type("CharacterCmdSet", (), {})
    for name, module in (
        ("evennia", evennia), ("evennia.commands", cmdpkg),
        ("evennia.commands.default", defaultpkg),
        ("evennia.commands.default.cmdset_character", character),
    ):
        monkeypatch.setitem(sys.modules, name, module)
    # Stub imports not used by CmdSolo to keep the test independent of Evennia.
    cwn = types.ModuleType("systems.cwn")
    cwn.skill_check = lambda **kw: None
    cwn.attribute_modifier = lambda x: 0
    cwn.ATTRIBUTES = ()
    cwn.SKILLS = ()
    monkeypatch.setitem(sys.modules, "systems.cwn", cwn)
    from nopunk_mud import solo_campaign
    pkg = types.ModuleType("nopunk_mud.solo_campaign")
    pkg.Campaign = solo_campaign.Campaign
    pkg.advance = solo_campaign.advance
    monkeypatch.setitem(sys.modules, "nopunk_mud.solo_campaign", pkg)
    path = Path(__file__).resolve().parents[1] / "commands" / "default_cmdsets.py"
    spec = importlib.util.spec_from_file_location("mud_cmdsets_950_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_evennia_solo_case_retains_clues_across_commands(monkeypatch):
    module = _load_commands(monkeypatch)
    class DB:
        unsa_solo_state = None
    class Caller:
        db = DB()
        messages = []
        def msg(self, value):
            self.messages.append(value)
    caller = Caller()
    def invoke(action):
        command = module.CmdSolo()
        command.caller, command.args = caller, action
        command.func()
        return caller.messages[-1]
    assert "Exits" in invoke("look")
    assert caller.db.unsa_solo_state["location"] == "safehouse"
    invoke("go street")
    invoke("go university")
    invoke("examine terminal")
    state = caller.db.unsa_solo_state
    assert state["location"] == "university"
    assert state["turns"] >= 4
    assert state["clues"]
    old = dict(state)
    assert "saved automatically" in invoke("save /tmp/should-not-be-written.json")
    assert caller.db.unsa_solo_state == old


def test_evennia_solo_corrupt_save_is_not_overwritten(monkeypatch):
    module = _load_commands(monkeypatch)
    class DB:
        unsa_solo_state = {"schema_version": -1}
    class Caller:
        db = DB()
        messages = []
        def msg(self, value):
            self.messages.append(value)
    caller = Caller()
    cmd = module.CmdSolo()
    cmd.caller, cmd.args = caller, "look"
    cmd.func()
    assert "could not be loaded" in caller.messages[-1]
    assert caller.db.unsa_solo_state == {"schema_version": -1}
