"""Executable guards for the two strategy-game CLIs' **output surface** (CodeQL CWE-312).

Why this file exists
--------------------

GitHub code scanning raises ``py/clear-text-logging-sensitive-data`` against
``strategy_game/__main__.py`` and ``strategy_game/render/__main__.py``. The rule's taint source is
the *field name* ``latitude``/``longitude`` on the board's ``Location`` record: CodeQL's shared
``maybePrivate()`` heuristic lists ``latitude|longitude`` among patterns for personal-location data,
so every dataclass field with that name is a taint source for every downstream ``print()``.

The rule fires on a **shape**, not on a value. These tests pin the two runtime facts that decide
whether the shape can carry anything sensitive in this repository, so the answer is checkable
rather than asserted in a review comment:

1. **There is no log-file surface.** Nothing in the package imports ``logging`` or configures a
   file handler, and neither CLI writes a file. The only sinks are ``print()`` to the caller's own
   stdout, which is what the tools are for. A world payload in a *log file* would be a real
   finding; the same payload on the terminal that asked for it is not.
2. **The scaffold CLI's output is constant.** ``python -m strategy_game`` takes no argument, reads
   no environment variable and opens no file, so it prints one fixed 118-byte empty board that
   carries no coordinate value at all.

Both are runtime properties of the code, so they are code tests under AGENTS.md and #271. Nothing
here asserts the wording of a rule, a document or a canon.

The one thing this file deliberately does **not** do is assert that the board's coordinates are
absent from the render CLI's output: that CLI exists to draw a board, the coordinates are the board,
and the renderer is expected to print them to the terminal that asked for a rendering. The guard is
that they go to stdout and nowhere else.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "strategy_game"

#: The CLI entrypoints whose output surface these guards cover.
SCAFFOLD_CLI = [sys.executable, "-m", "strategy_game"]
RENDER_CLI = [sys.executable, "-m", "strategy_game.render"]


def _package_sources() -> list[Path]:
    """Every module of the package, excluding the test tree itself."""
    return sorted(
        path
        for path in PACKAGE.rglob("*.py")
        if "tests" not in path.relative_to(PACKAGE).parts
        and "__pycache__" not in path.parts
    )


#: The keys that carry a position value. ``latitude``/``longitude`` are the names CodeQL's
#: ``maybePrivate()`` heuristic matches (issue #186); ``grid_row``/``grid_column`` are the names
#: this repository now uses for the same board position, because the board is a fictional map and
#: a grid reference is what it actually holds. Both are listed so the guard keeps its original
#: intent whichever name the payload carries.
POSITION_KEYS = {"latitude", "longitude", "grid_row", "grid_column"}


def _coordinates_in(payload: object) -> list[object]:
    """Every position value anywhere in a payload, under the keys CodeQL matches on."""
    found: list[object] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if str(key) in POSITION_KEYS:
                found.append(value)
            found.extend(_coordinates_in(value))
    elif isinstance(payload, list):
        for item in payload:
            found.extend(_coordinates_in(item))
    return found


def _snapshot_files(root: str) -> set[str]:
    """The paths of every *file* under ``root``.

    Used to notice a CLI that wrote somewhere other than its own working directory. The caller
    points ``TMPDIR`` at a fresh directory, so a concurrent process's scratch files cannot make
    the comparison noisy, and any file that appears there was written by the run under test.
    """
    return {str(path) for path in Path(root).rglob("*") if path.is_file()}


class NoLogFileSurfaceTests(unittest.TestCase):
    """Guard 1: the package never writes the board payload into a log file."""

    def test_no_module_imports_the_logging_framework(self) -> None:
        offenders: list[str] = []
        for path in _package_sources():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module or ""]
                else:
                    continue
                if any(name == "logging" or name.startswith("logging.") for name in names):
                    offenders.append(f"{path.relative_to(REPO)}:{node.lineno}")
        self.assertEqual(
            offenders, [],
            "the package must not import the logging framework: a log file holding the board "
            "payload would be a real CWE-312 finding, and stdout is the only intended sink",
        )

    def test_neither_cli_writes_a_file(self) -> None:
        for label, command in (("scaffold", SCAFFOLD_CLI), ("render", RENDER_CLI)):
            with self.subTest(cli=label), \
                    tempfile.TemporaryDirectory() as workdir, \
                    tempfile.TemporaryDirectory() as scratch:
                env = dict(os.environ)
                env["PYTHONPATH"] = str(REPO)
                env["PYTHONDONTWRITEBYTECODE"] = "1"
                # A private temp directory: anything the run writes there was written by it.
                env["TMPDIR"] = scratch
                before = _snapshot_files(scratch)
                done = subprocess.run(
                    [*command, "--empty"],
                    cwd=workdir,
                    capture_output=True,
                    text=True,
                    timeout=180,
                    env=env,
                    check=False,
                )
                self.assertEqual(done.returncode, 0, done.stderr[-500:])
                self.assertEqual(
                    sorted(os.listdir(workdir)),
                    [],
                    f"the {label} CLI wrote a file; its output must go to stdout only",
                )
                self.assertEqual(
                    _snapshot_files(scratch) - before,
                    set(),
                    f"the {label} CLI created a file outside its working directory; its "
                    "output must go to stdout only",
                )

    def test_the_two_flagged_modules_write_no_file(self) -> None:
        """The two modules CodeQL flagged must not write a file of their own.

        The package *does* have file-writing code, and it is legitimate: ``save_campaign``,
        the casework and investigation ``save`` methods, ``save_table`` and the playtest's
        ``--json`` output all take an explicit path **from the caller** and are the save
        features the tools are built around. A user asking the game to save its state is not a
        CWE-312 finding.

        What *is* the finding is a module that writes on its own initiative, with no path the
        caller chose — that is how a board payload ends up in a log file. So this guard is
        scoped to the two entrypoints the alerts name, where there is no such path: the
        scaffold CLI and the render module that draws for it.
        """
        offenders: list[str] = []
        for path in (PACKAGE / "__main__.py", PACKAGE / "render" / "text.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func = node.func
                    name = func.attr if isinstance(func, ast.Attribute) else (
                        func.id if isinstance(func, ast.Name) else ""
                    )
                    if name in {"write_text", "write_bytes"}:
                        offenders.append(f"{path.relative_to(REPO)}:{node.lineno} ({name})")
                    if name == "open":
                        mode = ""
                        for keyword in node.keywords:
                            if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
                                mode = str(keyword.value.value)
                        positional = node.args[1] if len(node.args) > 1 else None
                        if isinstance(positional, ast.Constant):
                            mode = str(positional.value)
                        if set(mode) & set("wax+"):
                            offenders.append(f"{path.relative_to(REPO)}:{node.lineno} (open {mode!r})")
        self.assertEqual(
            offenders, [],
            "the scaffold CLI and the render module must not write files: a board payload written "
            "to disk on the program's own initiative is the real CWE-312 shape, and stdout is the "
            "only intended sink for a view",
        )


class ScaffoldCliOutputTests(unittest.TestCase):
    """Guard 2: ``python -m strategy_game`` prints one constant, data-free payload."""

    def _run(
        self,
        *args: str,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess:
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(REPO)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        if env:
            environment.update(env)
        return subprocess.run(
            [*SCAFFOLD_CLI, *args],
            cwd=cwd or str(REPO),
            capture_output=True,
            text=True,
            timeout=180,
            env=environment,
            check=False,
        )

    def test_the_output_is_a_constant_across_runs_and_working_directories(self) -> None:
        first = self._run()
        self.assertEqual(first.returncode, 0, first.stderr[-500:])
        with tempfile.TemporaryDirectory() as workdir:
            second = self._run(cwd=workdir)
            self.assertEqual(second.returncode, 0, second.stderr[-500:])
        self.assertEqual(
            first.stdout,
            second.stdout,
            "the scaffold CLI's output must not depend on where it runs",
        )
        self.assertEqual(
            first.stdout,
            self._run().stdout,
            "the scaffold CLI's output must not vary between runs",
        )

    def test_the_payload_carries_no_coordinate_value(self) -> None:
        done = self._run()
        self.assertEqual(done.returncode, 0, done.stderr[-500:])
        payload = json.loads(done.stdout)
        self.assertEqual(
            _coordinates_in(payload),
            [],
            "the scaffold CLI prints the empty board, so no coordinate or board-position value "
            "may appear in its output at all",
        )

    def test_the_cli_reads_no_argument_environment_or_file(self) -> None:
        """The sink is constant because nothing can reach it: no argv, no env, no file."""
        done = self._run("--world", "/nonexistent/world.json")
        self.assertEqual(done.returncode, 0, done.stderr[-500:])
        self.assertEqual(
            json.loads(done.stdout),
            json.loads(self._run().stdout),
            "the scaffold CLI ignores its arguments; a world file must not be able to change it",
        )
        # An environment that names a real world file must not change the output either. The
        # point of this assertion is that it would FAIL if the CLI ever grew an env-var input
        # path, which is what makes it a guard rather than a restatement of the current shape.
        with tempfile.TemporaryDirectory() as workdir:
            world_path = Path(workdir) / "world.json"
            world_path.write_text(
                json.dumps(
                    {
                        "schema_version": "scaffold-1",
                        "locations": [
                            {
                                "identifier": "loc1",
                                "label": "Helsinki",
                                "grid_row": 60.17,
                                "grid_column": 24.94,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            polluted = self._run(env={"NOOPUNK_WORLD": str(world_path)})
            self.assertEqual(polluted.returncode, 0, polluted.stderr[-500:])
            self.assertEqual(
                json.loads(polluted.stdout),
                json.loads(self._run().stdout),
                "the scaffold CLI's payload must not depend on the environment",
            )

    def test_the_entrypoint_source_declares_no_input_path(self) -> None:
        """The strongest form of the same claim: the module has no input mechanism at all.

        Asserted on the *source* of the entrypoint rather than on one invocation, because a
        behavioural probe can only show that the paths it tried did not work. This shows that no
        such path exists: no ``argv``, no ``environ``, no file read.
        """
        source = (PACKAGE / "__main__.py").read_text(encoding="utf-8")
        tree = ast.parse(source, filename="strategy_game/__main__.py")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            self.assertNotIn(
                "argparse",
                names,
                "the scaffold CLI must not gain an argument parser: its output is pinned as a "
                "constant empty board by CI and by the view model's key set",
            )
            self.assertNotIn(
                "os",
                names,
                "the scaffold CLI must not gain an environment input path",
            )
        self.assertNotIn("environ", source, "the scaffold CLI must not read the environment")
        self.assertNotIn("argv", source, "the scaffold CLI must not read its arguments")
        self.assertNotIn(
            "open(",
            source,
            "the scaffold CLI must not read a file: it has no world-file flag",
        )


class RenderCliOutputTests(unittest.TestCase):
    """Guard 3: the render CLI's board data reaches stdout and nowhere else."""

    def test_a_loaded_world_reaches_stdout_and_writes_no_file(self) -> None:
        world = {
            "schema_version": "scaffold-1",
            "locations": [
                {"identifier": "loc1", "label": "Helsinki", "grid_row": 60.17, "grid_column": 24.94},
            ],
        }
        with tempfile.TemporaryDirectory() as workdir:
            world_path = Path(workdir) / "world.json"
            world_path.write_text(json.dumps(world), encoding="utf-8")
            env = dict(os.environ)
            env["PYTHONPATH"] = str(REPO)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            done = subprocess.run(
                [*RENDER_CLI, "--world", str(world_path), "--json"],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=180,
                env=env,
                check=False,
            )
            self.assertEqual(done.returncode, 0, done.stderr[-500:])
            payload = json.loads(done.stdout)
            self.assertEqual(
                _coordinates_in(payload),
                [60.17, 24.94],
                "the render CLI is expected to draw the board's coordinates to stdout",
            )
            self.assertEqual(
                sorted(p.name for p in Path(workdir).iterdir()),
                ["world.json"],
                "the render CLI must not write any file of its own",
            )


if __name__ == "__main__":
    unittest.main()
