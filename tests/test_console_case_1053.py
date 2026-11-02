"""The offline console slice runs a whole UNSA case without an engine, and stays replayable (#1053).

#1053's acceptance conditions are behavioural, so they are tested as behaviour: a complete case runs
from the console and finishes, a half-played case is saved and resumed, the same seed and commands
replay identically, and the domain layer imports with every engine blocked.

Nothing here needs Evennia, a database, a network or a model. If any of those creeps into the domain
layer, `test_the_domain_layer_imports_with_every_engine_blocked` fails first and names it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUD = ROOT / "mud"

#: The shortest legal path through the authored case: two evidence clues, then the report.
SOLVE = ("go street,go university,examine terminal,go street,go kurvi,"
         "talk witness,ask witness badge,examine woman in the raincoat,"
         "go street,go safehouse,report")
#: The same case, stopped after the first clue.
PARTIAL = "go street,go university,examine terminal"
#: The rest of the path, played on from the saved state.
RESUME = ("go street,go kurvi,talk witness,ask witness badge,"
          "examine woman in the raincoat,go street,go safehouse,report")


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "nopunk_mud.cli", *args], cwd=MUD,
                          capture_output=True, text=True, timeout=180, check=False)


def summary(completed: subprocess.CompletedProcess) -> dict:
    """The CLI prints a JSON report last; parse it rather than scraping prose."""
    return json.loads(completed.stdout[completed.stdout.rindex("\n{") + 1:])


class ConsoleCaseTests(unittest.TestCase):
    def test_a_complete_case_is_played_and_finished_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            save = Path(tmp) / "case.json"
            completed = run("--campaign", "--save", str(save), "--script", SOLVE)
            saved = save.exists() and bool(json.loads(save.read_text())["clues"])

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = summary(completed)
        self.assertEqual(report["ending"], "solved")
        self.assertEqual(set(report["clues"]), {"access_log", "witness_badge"})
        self.assertTrue(saved, "the run must leave a resumable saved state behind")

    def test_an_unfinished_case_reports_failure_and_saves_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            save = Path(tmp) / "partial.json"
            completed = run("--campaign", "--save", str(save), "--script", PARTIAL)
            self.assertEqual(completed.returncode, 1, "an unfinished case must not claim success")
            self.assertEqual(summary(completed)["ending"], "")
            self.assertTrue(save.exists())
            self.assertIn("access_log", json.loads(save.read_text())["clues"])

    def test_a_saved_case_resumes_where_it_stopped(self):
        with tempfile.TemporaryDirectory() as tmp:
            save = Path(tmp) / "case.json"
            run("--campaign", "--save", str(save), "--script", PARTIAL)
            resumed = run("--campaign", "--load", str(save), "--script", RESUME)

        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        report = summary(resumed)
        self.assertEqual(report["ending"], "solved")
        self.assertEqual(set(report["clues"]), {"access_log", "witness_badge"})

    def test_the_same_seed_and_commands_replay_exactly(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = run("--campaign", "--seed", "11", "--save", str(Path(tmp) / "a.json"),
                        "--script", SOLVE)
            second = run("--campaign", "--seed", "11", "--save", str(Path(tmp) / "b.json"),
                         "--script", SOLVE)

        # The save path is runner state, not game state: compare the run itself.
        first_run = {k: v for k, v in summary(first).items() if k != "save"}
        second_run = {k: v for k, v in summary(second).items() if k != "save"}
        self.assertEqual(first_run, second_run, "seeded play must be reproducible")

    def test_a_different_seed_is_allowed_to_differ_but_stays_a_valid_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = run("--campaign", "--seed", "3", "--save", str(Path(tmp) / "a.json"), "--script", SOLVE)
            b = run("--campaign", "--seed", "4", "--save", str(Path(tmp) / "b.json"), "--script", SOLVE)
        self.assertIn(summary(a)["ending"], {"solved", "incomplete", "killed"})
        self.assertIn(summary(b)["ending"], {"solved", "incomplete", "killed"})


class BoundaryTests(unittest.TestCase):
    def test_the_engine_boundary_check_passes(self):
        completed = subprocess.run([sys.executable, str(ROOT / "tools" / "check_engine_boundary.py"),
                                    "--check"], capture_output=True, text=True, timeout=120,
                                   check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_the_boundary_check_would_catch_a_violation(self):
        """The check must bite: a fake module importing Evennia has to be reported."""
        sys.path.insert(0, str(ROOT / "tools"))
        try:
            import check_engine_boundary as boundary
        finally:
            sys.path.pop(0)
        with tempfile.TemporaryDirectory() as tmp:
            tree = Path(tmp) / "src" / "rules"
            tree.mkdir(parents=True)
            (tree / "leaky.py").write_text("import evennia\nfrom mesa import Model\n")
            violations = boundary.scan(Path(tmp))
        self.assertEqual({item["import"] for item in violations}, {"evennia", "mesa"})

    def test_the_domain_layer_imports_with_every_engine_blocked(self):
        """A subprocess whose import hook refuses each engine proves the claim, not a comment."""
        blocked = ("evennia", "twisted", "pygame", "mesa", "streamlit", "openai", "anthropic",
                   "sqlalchemy", "pymongo", "redis")
        script = textwrap.dedent(f"""
            import importlib, sys
            BLOCKED = {blocked!r}
            class Wall:
                def find_module(self, name, path=None):
                    return self if name.split('.')[0] in BLOCKED else None
                def load_module(self, name):
                    raise ImportError(f"engine import blocked: {{name}}")
            sys.meta_path.insert(0, Wall())
            for name in ("src.rules.wwn_high_mage", "src.rules.swn_faction_engine",
                         "src.rules.swn_psionics", "src.rules.cwn_character",
                         "nopunk_mud.campaign", "nopunk_mud.cli"):
                importlib.import_module(name)
            print("imported without any engine")
        """)
        completed = subprocess.run([sys.executable, "-c", script], cwd=ROOT, capture_output=True,
                                   text=True, timeout=180, check=False,
                                   env={**dict(os.environ), "PYTHONPATH": str(MUD)})
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("imported without any engine", completed.stdout)


if __name__ == "__main__":
    unittest.main()
