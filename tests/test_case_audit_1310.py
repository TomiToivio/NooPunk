"""The detective case must not be able to softlock, and the audit has to prove it (#1310).

A case can pass a playtest and still be broken: a route that reaches an ending without the evidence that makes
the ending honest. These tests build the smallest graphs that exhibit each failure, so the audit's refusals are
demonstrated rather than asserted — and one test takes a clue away from the fixture and watches the audit fire.

The fixture is **synthetic and noncanonical**; it is a development case, not Tomi's manuscript.
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

from adventure import Adventure  # noqa: E402
from case_audit import audit, ending_reachable_without, endings, reachable_clues, reachable_scenes  # noqa: E402


def case() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def codes(findings, severity="error"):
    return {finding.code for finding in findings if finding.severity == severity}


class FixtureAuditTests(unittest.TestCase):
    def test_the_development_case_passes(self):
        findings = audit(case())
        self.assertEqual([f.message for f in findings if f.severity == "error"], [])

    def test_the_case_declares_what_must_survive(self):
        document = case()
        self.assertTrue(document["essential_clues"])
        self.assertEqual(sorted(endings(document)), sorted(reachable_scenes(document) & endings(document)))

    def test_no_ending_can_be_reached_without_an_essential_clue(self):
        document = case()
        for ending in endings(document):
            for clue in document["essential_clues"]:
                self.assertFalse(
                    ending_reachable_without(document, ending, clue),
                    f"{ending} can be reached without {clue}",
                )

    def test_every_declared_clue_can_be_picked_up_somewhere(self):
        document = case()
        self.assertEqual(set(document["clues"]), reachable_clues(document))


class SoftlockTests(unittest.TestCase):
    def test_an_ending_reachable_without_essential_evidence_is_an_error(self):
        """The smallest possible softlock: a second route to the ending that skips the evidence."""

        def document(**overrides):
            base = {
                "id": "audit.probe",
                "title": "Audit probe",
                "start": "briefing",
                "essential_clues": ["evidence"],
                "clues": {"evidence": "The thing that makes the ending honest."},
                "scenes": {
                    "briefing": {
                        "title": "Briefing",
                        "text": "Two ways to the same ending.",
                        "choices": [
                            {"label": "Do the work", "to": "ending", "adds": ["evidence"]},
                            {"label": "Skip the work", "to": "ending"},
                        ],
                    },
                    "ending": {"title": "Ending", "text": "The case closes.", "choices": [], "ending": True},
                },
            }
            base.update(overrides)
            return base

        self.assertIn("ending-without-essential-evidence", codes(audit(document())))

        # And the same case is clean once the shortcut is gated behind the evidence.
        gated = document()
        gated["scenes"]["briefing"]["choices"][1]["requires"] = ["evidence"]
        self.assertNotIn("ending-without-essential-evidence", codes(audit(gated)))

    def test_an_unobtainable_clue_is_an_error(self):
        document = case()
        document["clues"]["phantom"] = "A clue nobody can find."
        self.assertIn("unobtainable-clue", codes(audit(document)))

    def test_a_dangling_choice_is_an_error(self):
        document = case()
        first = next(iter(document["scenes"].values()))
        first["choices"].append({"label": "Go nowhere", "to": "scene.that.does.not.exist"})
        self.assertIn("dangling-choice", codes(audit(document)))

    def test_an_unreachable_ending_is_an_error(self):
        document = case()
        document["scenes"]["orphan_ending"] = {"title": "Orphan", "text": "Nobody arrives.", "choices": [],
                                               "ending": True}
        self.assertIn("unreachable-ending", codes(audit(document)))

    def test_a_choice_requiring_an_unknown_clue_is_an_error(self):
        document = case()
        first = next(iter(document["scenes"].values()))
        first["choices"][0]["requires"] = ["clue.that.does.not.exist"]
        self.assertIn("unknown-requirement", codes(audit(document)))

    def test_one_ending_is_a_warning_not_a_pass(self):
        document = case()
        for scene_id in list(endings(document))[1:]:
            document["scenes"][scene_id].pop("ending", None)
        findings = audit(document)
        self.assertIn("single-ending", codes(findings, "warning"))

    def test_an_unreachable_optional_scene_is_only_a_warning(self):
        document = case()
        document["scenes"]["side_room"] = {"title": "Side room", "text": "Optional.", "choices": []}
        findings = audit(document)
        self.assertIn("unreachable-scene", codes(findings, "warning"))
        self.assertEqual([f.message for f in findings if f.severity == "error"], [])


class NotebookTests(unittest.TestCase):
    def test_deductions_appear_only_when_the_evidence_supports_them(self):
        document = case()
        game = Adventure(document)
        self.assertNotIn("What the evidence supports", game.notebook())
        game.state["clues"] = ["missing", "roster"]
        self.assertIn("What the evidence supports", game.notebook())

    def test_a_contradiction_is_shown_as_disagreement_not_as_proof(self):
        document = case()
        game = Adventure(document)
        game.state["clues"] = ["witness", "message"]
        notebook = game.notebook()
        self.assertIn("Accounts that do not agree", notebook)
        self.assertIn("incomplete", notebook.lower())

    def test_the_notebook_never_calls_a_hypothesis_a_fact(self):
        document = case()
        game = Adventure(document)
        game.state["clues"] = ["missing", "roster", "witness", "message"]
        self.assertIn("not established facts", game.notebook())


class CommandTests(unittest.TestCase):
    def test_the_audit_cli_passes_the_development_case(self):
        result = subprocess.run(
            [sys.executable, str(CODE / "case_audit.py"), "--check"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_the_audit_cli_fails_a_broken_case(self):
        import tempfile

        document = case()
        document["scenes"]["dangling"] = {"title": "x", "text": "y", "choices": [{"label": "z", "to": "nope"}]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CODE / "case_audit.py"), "--case", str(path), "--check"],
                cwd=ROOT, capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("dangling-choice", result.stdout)


if __name__ == "__main__":
    unittest.main()
