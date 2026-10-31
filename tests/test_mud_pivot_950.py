"""The headless solo smoke works, and the routing says so (#950).

The pivot is only real if the default game can be exercised without the things it is supposed to not need:
no LLM provider, no Mesa, no Godot, no second player, no network.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUD = ROOT / "mud"
sys.path.insert(0, str(MUD))

from nopunk_mud.cli import demo  # noqa: E402


def test_the_solo_smoke_runs_with_no_llm_and_no_other_players():
    report = demo()
    assert report["llm_calls"] == 0
    assert report["other_players"] == 0
    assert report["persisted"] is True
    assert report["faction"] == "unsa"
    assert report["room"] == "street"


def test_the_smoke_uses_published_arithmetic():
    report = demo()
    # Physical/Evasion/Mental/Luck are 16 - level(1) - best modifier (all 0 here) = 15
    assert report["saves"] == {"Physical": 15, "Evasion": 15, "Mental": 15, "Luck": 15}
    # Constitution 11 -> +0, one d6 showing 4 -> 4 hit points
    assert report["hp"] == 4
    assert report["strain"] == 11


def test_the_cli_runs_as_a_process():
    completed = subprocess.run([sys.executable, "-m", "nopunk_mud.cli", "--demo"],
                               cwd=MUD, capture_output=True, text=True, timeout=120)
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["character"] == "rookie"
    assert payload["persisted"] is True


def test_agents_guidance_names_the_mud_as_the_default_target():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "#950" in agents
    assert "default target" in agents.lower()
    assert "mud/" in agents
    assert "single-player" in agents.lower()

    mud_agents = (MUD / "AGENTS.md").read_text(encoding="utf-8")
    assert "#950" in mud_agents
    assert "default target" in mud_agents.lower()


def test_the_compliance_matrix_is_valid_and_honest():
    completed = subprocess.run([sys.executable, str(ROOT / "tools" / "check_cwn_compliance.py")],
                               cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    matrix = json.loads((ROOT / "data" / "rules" / "cwn_compliance_matrix.json").read_text())
    assert len(matrix["rows"]) >= 15
    # The linked SRD omits the antagonist section; claiming it would be the exact dishonesty the issue warns of.
    antagonists = [r for r in matrix["rows"] if r["id"] == "antagonists"][0]
    assert antagonists["coverage"] == "missing"
