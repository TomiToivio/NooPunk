"""Issue #1310, P5: the case audit proves "no softlocks" instead of asserting it.

A guard that has only ever passed proves nothing, so every test below pairs the shipped case (sound)
with a case broken in exactly one way, and asserts the audit names that defect. Clue acquisition is
monotone in this runner, so the reachability fixed point is exact — a gate whose evidence cannot be
collected is reported as an unreachable scene, which is what a softlock looks like statically.
"""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "NooPunk-Simulator" / "Code"
AUDIT_PATH = CODE / "case_audit.py"
ADVENTURE_PATH = CODE / "adventure.py"
FIXTURE = ROOT / "NooPunk-Simulator" / "Graphs" / "fixtures" / "romppainen_development_case.json"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, path
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CaseAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit_module = _load("case_audit_1310", AUDIT_PATH)
        cls.adventure = _load("adventure_1310_audit", ADVENTURE_PATH)
        cls.case = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def broken(self):
        case = copy.deepcopy(self.case)
        return case

    def test_the_shipped_development_case_is_sound(self):
        self.assertEqual(self.audit_module.audit(self.case), [])
        scenes, clues = self.audit_module.reachable(self.case)
        self.assertEqual(scenes, set(self.case["scenes"]))
        self.assertEqual(clues, set(self.case["clues"]))

    def test_a_gate_that_cannot_be_satisfied_strands_the_scene_it_guards(self):
        case = self.broken()
        case["scenes"]["message"]["choices"][0]["requires"].append("confession")
        case["clues"]["confession"] = "A clue nothing can produce."
        findings = self.audit_module.audit(case)
        self.assertTrue(any("'decision' is unreachable" in f for f in findings), findings)
        self.assertTrue(any("'confession' can never be collected" in f for f in findings), findings)

    def test_an_unreachable_ending_is_named(self):
        case = self.broken()
        case["scenes"]["decision"]["choices"][1]["requires"] = ["confession"]
        case["clues"]["confession"] = "A clue nothing can produce."
        findings = self.audit_module.audit(case)
        self.assertTrue(any("'review_end' is unreachable" in f for f in findings), findings)
        self.assertTrue(any("'review_end' can never be reached" in f for f in findings), findings)

    def test_a_clue_no_choice_adds_is_named(self):
        case = self.broken()
        case["clues"]["orphan"] = "A clue no scene offers."
        self.assertTrue(any("'orphan' can never be collected" in f
                            for f in self.audit_module.audit(case)))

    def test_a_scene_that_is_neither_ending_nor_choice_is_a_dead_end(self):
        case = self.broken()
        case["scenes"]["witness"]["choices"] = []
        findings = self.audit_module.audit(case)
        self.assertTrue(any("'witness' is neither an ending nor offers a choice" in f
                            for f in findings), findings)

    def test_a_case_without_any_ending_cannot_be_finished(self):
        case = self.broken()
        for scene in case["scenes"].values():
            scene.pop("ending", None)
        self.assertTrue(any("has no ending" in f for f in self.audit_module.audit(case)))

    def test_a_hypothesis_resting_on_impossible_evidence_is_named(self):
        case = self.broken()
        case["hypotheses"].append({"id": "h9", "text": "An unreachable theory.", "requires": ["ghost"]})
        case["clues"]["ghost"] = "A clue nothing can produce."
        findings = self.audit_module.audit(case)
        self.assertTrue(any("hypothesis 'h9' can never become available" in f for f in findings),
                        findings)

    def test_a_contradiction_resting_on_impossible_evidence_is_named(self):
        case = self.broken()
        case["contradictions"].append({"id": "c9", "between": ["missing", "ghost"],
                                       "text": "Unprovable conflict."})
        case["clues"]["ghost"] = "A clue nothing can produce."
        findings = self.audit_module.audit(case)
        self.assertTrue(any("contradiction 'c9' can never surface" in f for f in findings), findings)

    def test_a_dangling_reference_is_refused_before_the_audit(self):
        case = self.broken()
        case["contradictions"][0]["between"] = ["roster", "ghost"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dangling.json"
            path.write_text(json.dumps(case), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.adventure.load_case(path)


class CaseAuditCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, str(AUDIT_PATH), *arguments],
                              capture_output=True, text=True, check=False)

    def test_the_cli_reports_a_sound_case(self):
        completed = self.run_cli("--case", str(FIXTURE))
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("no softlock", completed.stdout)

    def test_the_cli_fails_a_case_with_a_softlock(self):
        case = json.loads(FIXTURE.read_text(encoding="utf-8"))
        case["scenes"]["message"]["choices"][0]["requires"].append("confession")
        case["clues"]["confession"] = "A clue nothing can produce."
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken_case.json"
            path.write_text(json.dumps(case), encoding="utf-8")
            completed = self.run_cli("--case", str(path))
        self.assertEqual(completed.returncode, 1)
        self.assertIn("unreachable", completed.stderr)

    def test_the_cli_reports_an_unreadable_case_rather_than_passing(self):
        completed = self.run_cli("--case", str(ROOT / "no-such-case.json"))
        self.assertEqual(completed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
