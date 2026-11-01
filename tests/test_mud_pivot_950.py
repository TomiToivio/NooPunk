"""The headless solo smoke works, and the routing says so (#950).

Written with `unittest`: CI discovers with `unittest` and does not install pytest.

The pivot is only real if the default game can be exercised without the things it is supposed to not need:
no LLM provider, no Mesa, no Godot, no second player, no network.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUD = ROOT / "mud"
sys.path.insert(0, str(MUD))

from nopunk_mud.cli import demo  # noqa: E402


class SoloSmoke(unittest.TestCase):
    def test_it_runs_with_no_llm_and_no_other_players(self):
        report = demo()
        self.assertEqual(report["llm_calls"], 0)
        self.assertEqual(report["other_players"], 0)
        self.assertTrue(report["persisted"])
        self.assertEqual(report["faction"], "unsa")
        self.assertEqual(report["room"], "street")

    def test_it_uses_published_arithmetic(self):
        report = demo()
        self.assertEqual(report["saves"],
                         {"Physical": 15, "Evasion": 15, "Mental": 15, "Luck": 15})
        self.assertEqual(report["hp"], 4)      # Con 11 -> +0, one d6 showing 4
        self.assertEqual(report["strain"], 11)  # Con 11, ordinary lifestyle

    def test_the_cli_runs_as_a_process(self):
        completed = subprocess.run([sys.executable, "-m", "nopunk_mud.cli", "--demo"],
                                   cwd=MUD, capture_output=True, text=True, timeout=120)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["character"], "rookie")
        self.assertTrue(payload["persisted"])


class Routing(unittest.TestCase):
    def test_agents_guidance_names_the_mud_as_the_default_target(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("#950", agents)
        self.assertIn("default target", agents.lower())
        self.assertIn("mud/", agents)
        self.assertIn("single-player", agents.lower())

        mud_agents = (MUD / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("#950", mud_agents)
        self.assertIn("primary", mud_agents.lower())

    def test_the_897_lock_is_still_in_the_first_screen(self):
        # Sections, not bytes. #990 added a binding design-workflow section at the top, which pushed #897
        # past a 4000-character window and failed this guard for a reason unrelated to the rule it protects.
        # Agents read sections, so the guard reads sections.
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        head = "\n".join("# " + part for part in re.split(r"(?m)^# ", agents)[:5] if part.strip())
        self.assertIn("#897", head)
        self.assertIn("mods/noopunk", head)


class ComplianceMatrix(unittest.TestCase):
    def test_the_matrix_validates(self):
        completed = subprocess.run([sys.executable, str(ROOT / "tools" / "check_cwn_compliance.py")],
                                   cwd=ROOT, capture_output=True, text=True, timeout=120)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_it_does_not_claim_the_omitted_sections(self):
        matrix = json.loads((ROOT / "data" / "rules" / "cwn_compliance_matrix.json").read_text())
        self.assertGreaterEqual(len(matrix["rows"]), 15)
        antagonists = [row for row in matrix["rows"] if row["id"] == "antagonists"][0]
        self.assertEqual(antagonists["coverage"], "missing")


if __name__ == "__main__":
    unittest.main()
