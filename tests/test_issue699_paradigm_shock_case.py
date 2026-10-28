"""The #699 case runs headless, both branches are asserted, and it is deterministic.

Stdlib unittest only — the repository's CI has no pytest.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "paradigm_shock_case.py"


def run_case(directory: str) -> dict:
    out = Path(directory) / "case.json"
    result = subprocess.run(
        [sys.executable, str(TOOL), "--json", str(out)],
        capture_output=True, text=True, timeout=120, check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(out.read_text(encoding="utf-8"))


class TestTheCaseRunsHeadless(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.case = run_case(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_both_branches_reach_a_conclusion(self):
        self.assertEqual(set(self.case["branches"]), {"accept", "hold"})
        for branch in self.case["branches"].values():
            self.assertIn(branch["state_after"], {"reframed", "fractured"})
            self.assertTrue(branch["condition"].strip())
            self.assertTrue(branch["constrains"].strip())

    def test_the_branches_diverge(self):
        self.assertTrue(self.case["diverged"])
        self.assertTrue(self.case["conditions_differ"])
        self.assertNotEqual(
            self.case["branches"]["accept"]["state_after"],
            self.case["branches"]["hold"]["state_after"],
        )

    def test_both_layers_appear_in_the_journal(self):
        # D47: the event and the world view are recorded separately.
        events = self.case["branches"]["accept"]["events"]
        self.assertTrue(any(e.startswith("layer 1") for e in events))
        self.assertTrue(any(e.startswith("layer 3") for e in events))
        self.assertTrue(any(e.startswith("layer 4") for e in events))

    def test_the_same_case_twice_gives_the_same_journal(self):
        # D48 in one assertion: nothing in this path can roll.
        with tempfile.TemporaryDirectory() as other:
            self.assertEqual(self.case, run_case(other))

    def test_the_verdict_does_not_overclaim(self):
        verdict = self.case["verdict"]
        self.assertTrue(verdict["d48_holds"])
        self.assertFalse(
            verdict["d46_exercised"],
            "this case is carried by the journal, not by play; claiming it tests D46 would be the "
            "overclaim the issue exists to prevent",
        )
        self.assertFalse(verdict["d49_triggered"])
        self.assertIn("second case", verdict["next"])


if __name__ == "__main__":
    unittest.main()
