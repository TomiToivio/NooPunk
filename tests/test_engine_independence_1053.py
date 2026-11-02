"""The rules and the campaign run without an engine (#1053, #1054).

The architecture decision is only real if a machine can prove it: no Evennia, no Godot, no database,
no LLM, no network — a plain Python interpreter running the first playable UNSA case to an ending.

This test drives the console slice in a **clean subprocess** and checks three things:

1. it finishes with a known ending and the expected clues;
2. the same script produces byte-identical output twice (deterministic — no clock, no RNG drift);
3. importing the rules/campaign packages does not pull Evennia into `sys.modules`.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUD = ROOT / "mud"

SOLVE = (
    "go street,go university,examine terminal,go street,go kurvi,"
    "talk witness,ask witness badge,examine woman,go street,go safehouse,report"
)


def run_cli(script: str) -> subprocess.CompletedProcess:
    """Run the console slice with an environment that contains nothing but a PATH."""
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", "/tmp"), "PYTHONPATH": str(MUD)}
    return subprocess.run(
        [sys.executable, "-m", "nopunk_mud.cli", "--campaign", "--script", script],
        cwd=MUD, env=env, capture_output=True, text=True, timeout=300,
    )


def final_json(stdout: str) -> dict:
    start = stdout.rfind("{\n")
    if start < 0:
        raise AssertionError(f"no JSON summary in output:\n{stdout[-500:]}")
    return json.loads(stdout[start:])


class TheConsoleSliceIsPlayable(unittest.TestCase):
    def test_the_case_runs_to_an_ending_without_any_engine(self):
        result = run_cli(SOLVE)
        self.assertEqual(result.returncode, 0, result.stderr[-800:])
        summary = final_json(result.stdout)
        self.assertEqual(summary["ending"], "solved")
        self.assertEqual(set(summary["clues"]), {"access_log", "witness_badge"})

    def test_the_same_script_produces_identical_output(self):
        first, second = run_cli(SOLVE), run_cli(SOLVE)
        self.assertEqual(first.stdout, second.stdout, "the slice is not deterministic")

    def test_a_fresh_run_starts_clean(self):
        summary = final_json(run_cli("look").stdout)
        self.assertEqual(summary["ending"], "")
        self.assertEqual(summary["clues"], [])
        self.assertEqual(summary["turns"], 1)


class NoEngineIsImported(unittest.TestCase):
    def test_importing_the_rules_and_campaign_pulls_no_engine(self):
        probe = (
            "import sys; sys.path.insert(0, %r)\n"
            "from nopunk_mud import cwn\n"
            "from nopunk_mud.campaign import CampaignEngine\n"
            "from nopunk_mud import cli\n"
            "engines = [m for m in sys.modules if m.split('.')[0] in "
            "('evennia', 'django', 'godot', 'concordia', 'pygame', 'pymongo', 'redis')]\n"
            "print(','.join(engines))\n"
        ) % str(MUD)
        env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", "/tmp")}
        result = subprocess.run([sys.executable, "-c", probe], env=env,
                                capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr[-800:])
        self.assertEqual(result.stdout.strip(), "", "the portable core imported an engine")

    def test_the_portable_modules_do_not_name_an_engine_in_their_imports(self):
        banned = ("import evennia", "from evennia", "import django", "from godot", "res://")
        for path in sorted((MUD / "nopunk_mud" / "cwn").glob("*.py")) + [
            MUD / "nopunk_mud" / "campaign" / "engine.py",
            MUD / "nopunk_mud" / "campaign" / "content.py",
            MUD / "nopunk_mud" / "social.py",
            MUD / "nopunk_mud" / "ideology.py",
            MUD / "nopunk_mud" / "discourse_network.py",
        ]:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            for needle in banned:
                with self.subTest(file=path.name, needle=needle):
                    self.assertNotIn(needle, text)


if __name__ == "__main__":
    unittest.main()
