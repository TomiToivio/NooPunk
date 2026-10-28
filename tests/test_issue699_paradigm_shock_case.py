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
            assert branch["condition"].strip()
            assert branch["constrains"].strip()

    def test_the_branches_diverge(self, tmp_path):
        case = run_case(tmp_path)
        assert case["diverged"] is True
        assert case["conditions_differ"] is True
        assert case["branches"]["accept"]["state_after"] != case["branches"]["hold"]["state_after"]

    def test_both_layers_appear_in_the_journal(self, tmp_path):
        # D47: the event and the world view are recorded separately.
        branch = run_case(tmp_path)["branches"]["accept"]
        assert any(e.startswith("layer 1") for e in branch["events"])
        assert any(e.startswith("layer 3") for e in branch["events"])
        assert any(e.startswith("layer 4") for e in branch["events"])

    def test_the_same_case_twice_gives_the_same_journal(self, tmp_path):
        # D48 in one assertion: nothing in this path can roll.
        assert run_case(tmp_path) == run_case(tmp_path)

    def test_the_verdict_does_not_overclaim(self, tmp_path):
        verdict = run_case(tmp_path)["verdict"]
        assert verdict["d48_holds"] is True
        assert verdict["d46_exercised"] is False, (
            "this case is carried by the journal, not by play; claiming it tests D46 would be the "
            "overclaim the issue exists to prevent"
        )
        assert verdict["d49_triggered"] is False
        assert "second case" in verdict["next"]
