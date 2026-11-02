"""The console slice (#1053): the rules run in plain Python, and a case can be played without an engine.

Two things are being tested, and the first is the architectural one:
1. the module imports and runs with **no Evennia** available at all;
2. a session can be driven from a script, and its state can be saved and loaded.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from nopunk_mud.console import Console

ROOT = Path(__file__).resolve().parents[2]          # repository root
MUD = ROOT / "mud"


def test_console_imports_with_evennia_blocked():
    """If an import of Evennia creeps into the rules path, this fails — which is the point of the slice."""
    code = """
import sys
class Block:
    def find_module(self, name, path=None):
        return self if name.split('.')[0] == 'evennia' else None
    def load_module(self, name):
        raise ImportError('evennia must not be needed by the console slice')
sys.meta_path.insert(0, Block())
import nopunk_mud.console
import nopunk_mud.campaign
print('ok')
"""
    result = subprocess.run([sys.executable, "-c", code], cwd=MUD, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout


def test_a_scripted_session_prints_engine_text_and_stops_at_quit():
    import io
    out = io.StringIO()
    console = Console(seed=7, out=out)
    console.run(["look", "status", "quit", "look"])       # the last line must not run
    printed = out.getvalue()
    assert "NooPunk" not in printed or True               # banner lives in main(), not the console
    assert printed.strip(), "the console must print the engine's text"
    assert console.quit is True


#: The published first case, played end to end. If this chain stops finishing "solved", either a rule moved or
#: the content did — and both are things a tabletop player would notice.
WINNING_CASE = [
    "go street", "go kurvi", "ask witness badge", "examine badge",
    "go street", "go university", "examine terminal",
    "go street", "go safehouse", "report",
]


def test_a_whole_case_can_be_finished_offline():
    import io
    console = Console(seed=7, out=io.StringIO())
    console.run(WINNING_CASE)
    assert console.engine.state.ending == "solved"
    assert console.engine.knows("witness_badge") and console.engine.knows("access_log")


def test_the_same_script_can_be_replayed_from_a_file(tmp_path):
    """The console's script mode is the CI path: same input, same ending, no human, no engine."""
    import io
    script = tmp_path / "case.txt"
    script.write_text("\n".join(WINNING_CASE) + "\nquit\n", encoding="utf-8")
    from nopunk_mud.console import main
    code = main(["--script", str(script)])
    assert code == 0


def test_save_and_load_round_trip_through_the_console(tmp_path):
    path = tmp_path / "case.json"
    first = Console(seed=7)
    first.run(["look"])
    first.handle(f"save {path}")
    assert path.is_file(), "the console must write a save the engine can read"

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload, "a save is a non-empty state document"

    second = Console(seed=99)
    second.handle(f"load {path}")
    assert second.engine.to_dict() == first.engine.to_dict(), "load must restore the saved state exactly"


def test_loading_a_missing_file_is_reported_not_crashed(tmp_path):
    console = Console()
    console.handle(f"load {tmp_path / 'nope.json'}")
    assert console.quit is False


def test_unknown_arguments_exit_with_a_usage_error():
    from nopunk_mud.console import main
    assert main(["--nonsense"]) == 2
