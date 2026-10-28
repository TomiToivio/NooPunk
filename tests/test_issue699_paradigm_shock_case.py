"""The #699 case runs headless, both branches are asserted, and it is deterministic."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "paradigm_shock_case.py"


def run_case(tmp_path: Path) -> dict:
    out = tmp_path / "case.json"
    result = subprocess.run(
        [sys.executable, str(TOOL), "--json", str(out)],
        capture_output=True, text=True, timeout=120, check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(out.read_text(encoding="utf-8"))


class TestTheCaseRunsHeadless:
    def test_both_branches_reach_a_conclusion(self, tmp_path):
        case = run_case(tmp_path)
        assert set(case["branches"]) == {"accept", "hold"}
        for branch in case["branches"].values():
            assert branch["state_after"] in {"reframed", "fractured"}
            assert branch["cost"].strip()

    def test_the_branches_diverge(self, tmp_path):
        case = run_case(tmp_path)
        assert case["diverged"] is True
        assert case["costs_differ"] is True
        assert case["branches"]["accept"]["state_after"] != case["branches"]["hold"]["state_after"]

    def test_the_same_case_twice_gives_the_same_journal(self, tmp_path):
        # D48 in one assertion: nothing in this path can roll.
        first = run_case(tmp_path)
        second = run_case(tmp_path)
        assert first == second

    def test_the_verdict_does_not_overclaim(self, tmp_path):
        verdict = run_case(tmp_path)["verdict"]
        assert verdict["d48_holds"] is True
        assert verdict["d46_exercised"] is False, (
            "this case is carried by layer 4; claiming it tests D46 would be the overclaim the "
            "issue exists to prevent"
        )
        assert "second case" in verdict["next"]
