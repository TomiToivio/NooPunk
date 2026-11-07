"""The audit's one missing question: can an ending be reached without its evidence? (#1310)

The merged audit (#1320) answers *"can this be reached at all"*: scenes, clues, endings, hypotheses and
contradictions, as a fixed point. It does not answer *"can this be skipped"* — and a case where one route finds the
evidence and another route ends without it passes a union check while stranding the player in a story they cannot
honestly close.

These tests are the smallest cases that exhibit the difference, so the refusal is demonstrated rather than
asserted.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "NooPunk-Simulator" / "Code"
FIXTURE = ROOT / "NooPunk-Simulator" / "Graphs" / "fixtures" / "romppainen_development_case.json"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from case_audit import audit, ending_reachable_without  # noqa: E402


def probe(*, gate: bool) -> dict:
    """Two routes to one ending; the second skips the evidence unless it is gated behind it."""
    shortcut = {"label": "Skip the work", "to": "ending"}
    if gate:
        shortcut["requires"] = ["evidence"]
    return {
        "id": "audit.probe",
        "title": "Audit probe",
        "source": "synthetic",
        "start": "briefing",
        "essential_clues": ["evidence"],
        "clues": {"evidence": "The thing that makes the ending honest."},
        "scenes": {
            "briefing": {
                "title": "Briefing",
                "text": "Two ways to the same ending.",
                "choices": [
                    {"label": "Do the work", "to": "ending", "adds": ["evidence"]},
                    shortcut,
                ],
            },
            "ending": {"title": "Ending", "text": "The case closes.", "choices": [], "ending": True},
        },
    }


class EssentialEvidenceTests(unittest.TestCase):
    def test_the_development_case_carries_its_evidence(self):
        case = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertTrue(case["essential_clues"])
        self.assertEqual([f for f in audit(case) if "without essential clue" in f], [])

    def test_a_shortcut_past_the_evidence_is_refused(self):
        findings = audit(probe(gate=False))
        self.assertTrue(
            any("without essential clue 'evidence'" in finding for finding in findings),
            findings,
        )

    def test_the_same_case_passes_once_the_shortcut_is_gated(self):
        self.assertEqual(audit(probe(gate=True)), [])

    def test_the_check_is_per_route_not_per_scene(self):
        """The union of clues available at the ending includes 'evidence'; the shortcut does not."""
        case = probe(gate=False)
        self.assertTrue(ending_reachable_without(case, "ending", "evidence"))
        self.assertFalse(ending_reachable_without(probe(gate=True), "ending", "evidence"))

    def test_an_essential_clue_that_does_not_exist_is_reported(self):
        case = probe(gate=True)
        case["essential_clues"] = ["clue.that.does.not.exist"]
        findings = audit(case)
        self.assertTrue(any("essential_clues names unknown clue" in finding for finding in findings), findings)

    def test_declaring_no_essential_clues_leaves_the_case_alone(self):
        """Optional: a case may not want to promise anything, and the audit must not invent a promise."""
        case = probe(gate=False)
        case.pop("essential_clues")
        self.assertEqual(audit(case), [])


class CliTests(unittest.TestCase):
    def run_cli(self, case_path):
        return subprocess.run(
            [sys.executable, str(CODE / "case_audit.py"), "--case", str(case_path)],
            cwd=ROOT, capture_output=True, text=True,
        )

    def test_the_cli_reports_a_softlock_with_a_nonzero_exit(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "probe.json"
            path.write_text(json.dumps(probe(gate=False)), encoding="utf-8")
            result = self.run_cli(path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("without essential clue", result.stderr)

    def test_the_cli_passes_the_development_case(self):
        result = self.run_cli(FIXTURE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no softlock", result.stdout)


if __name__ == "__main__":
    unittest.main()
