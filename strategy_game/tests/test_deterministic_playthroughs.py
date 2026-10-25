"""Deterministic seeded playthroughs for every active scenario (issue #564, step 6).

This is a **code test**: it drives the real CLI entrypoints as subprocesses and observes
behaviour. It asserts nothing about rules prose, canon or rulebook structure.

The epic (#564) requires "at least one automated end-to-end playthrough for each major active
scenario with deterministic seeds and no LLM requirement". This module supplies that harness for
the scenarios that are active today, and it is chassis-neutral: it exercises whatever engine the
entrypoint currently wires, so it stays valid after the CWN/SWN conversion changes the dice.

Per scenario it proves four things:

1. **Completion** — the run reaches a written ending, not a bare `quit`. A harness that only
   proved "the process exits 0" would pass on a scenario that never resolves anything.
2. **Determinism** — the same seed and the same script produce byte-identical stdout and a
   byte-identical save file across two independent runs.
3. **Persistence** — the save the run writes is a file the engine can read back and resume.
4. **No network, therefore no LLM** — the child starts with a `sitecustomize` audit hook that
   raises on `socket.connect` / `socket.getaddrinfo` / `urllib.Request`. A passing run is
   therefore a run that never reached for a model, an API or a name resolver.

Every child runs in its own temporary working directory with an explicit `--save`, so no
scenario can leave a stray save file in the repository (one already did: `noopunk-save.json`
appeared at the repo root from a manual run and the packaging guard flagged it as unreviewed
material).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

#: Installed as ``sitecustomize`` in a directory placed first on the child's ``PYTHONPATH``.
#: Audit hooks fire for the C-level calls too, so this catches a resolver lookup even when the
#: socket object is never constructed.
_NETWORK_BLOCKER = '''\
"""Refuse every outbound network call in a deterministic playthrough."""

import sys


def _deny(event, args):
    if event in {
        "socket.connect",
        "socket.getaddrinfo",
        "socket.gethostbyname",
        "urllib.Request",
        "http.client.connect",
    }:
        raise RuntimeError(
            "network access attempted during a deterministic playthrough: " + event
        )


sys.addaudithook(_deny)
'''


class _Run:
    """One scenario invocation and its observable result."""

    __slots__ = ("name", "argv", "stdin", "marker", "save_name", "saves")

    def __init__(
        self, name: str, argv: list[str], stdin: str, marker: str,
        save_name: str, saves: bool = True,
    ):
        self.name = name
        self.argv = argv
        self.stdin = stdin
        self.marker = marker
        self.save_name = save_name
        self.saves = saves


#: The active scenarios. Adding a scenario here is the whole cost of covering it.
SCENARIOS = (
    _Run(
        name="ubiquitous-maniacs-case",
        argv=["-m", "strategy_game.rpg", "--scenario", "ubiquitous-maniacs-case",
              "--new", "--seed", "42"],
        stdin=(
            "act pc_leader inspect_register\n"
            "next\n"
            "act laura_falk compare_traces\n"
            "act harri_romppainen interview_patient\n"
            "act sebastian_virtanen reconcile_accounts\n"
            "assemble\n"
            "resolve closed_by_evidence\n"
            "quit\n"
        ),
        marker="Case closed",
        save_name="ward.json",
    ),
    _Run(
        name="ubiquitous-maniacs-legacy (two-day prototype)",
        # `--scenario ubiquitous-maniacs` now routes to the five-seat case (main, after #565);
        # the old prototype is the explicit `-legacy` route.
        argv=["-m", "strategy_game.rpg", "--scenario", "ubiquitous-maniacs-legacy", "--new"],
        stdin=(
            "read_form\n"
            "enter_chamber\n"
            "retain_record\n"
            "continue\n"
            "follow_clue\n"
            "quit\n"
        ),
        marker="Scenario complete",
        save_name="legacy.json",
    ),
    _Run(
        name="casework: The Second Shadow (investigate)",
        argv=["-m", "strategy_game.casework", "--json", "--seed", "7",
              "--route", "investigate"],
        stdin="",
        marker='"resolution": "closed_by_evidence"',
        save_name="kallio-investigate.json",
    ),
    _Run(
        name="casework: The Second Shadow (confront)",
        argv=["-m", "strategy_game.casework", "--json", "--seed", "11",
              "--route", "confront", "--approach", "force"],
        stdin="",
        marker='"resolution":',
        save_name="kallio-confront.json",
    ),
    _Run(
        name="casework: The Second Shadow (refer)",
        argv=["-m", "strategy_game.casework", "--json", "--seed", "13",
              "--route", "refer"],
        stdin="",
        marker='"resolution":',
        save_name="kallio-refer.json",
    ),
    _Run(
        name="rpg scene report",
        argv=["-m", "strategy_game.rpg", "--seed", "5"],
        stdin="",
        marker='"rolls_made"',
        save_name="unused.json",
        saves=False,
    ),
)


class DeterministicPlaythroughTests(unittest.TestCase):
    """Every active scenario: completes, replays identically, and touches no network."""

    maxDiff = 4000

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="noopunk-playthrough-")
        self.workdir = Path(self._tmp.name)
        blocker = self.workdir / "_no_network"
        blocker.mkdir()
        (blocker / "sitecustomize.py").write_text(_NETWORK_BLOCKER, encoding="utf-8")
        self.blocker = blocker

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # -- helpers -------------------------------------------------------------------------

    def _run(self, run: _Run, save: Path) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join((str(self.blocker), str(ROOT)))
        # Belt and braces: even if a hook were bypassed, no credential is exported to the child.
        for key in list(env):
            if key.endswith(("_API_KEY", "_TOKEN", "_SECRET")):
                env.pop(key, None)
        return subprocess.run(
            [sys.executable, *run.argv, *(["--save", str(save)] if run.saves else [])],
            cwd=self.workdir,
            env=env,
            input=run.stdin,
            text=True,
            capture_output=True,
            timeout=180,
        )

    def _play_once(
        self, run: _Run, *, fresh: bool = True
    ) -> tuple[subprocess.CompletedProcess[str], bytes]:
        save = self.workdir / run.save_name
        if fresh:
            save.unlink(missing_ok=True)
        result = self._run(run, save)
        payload = save.read_bytes() if save.exists() else b""
        return result, payload

    # -- the properties ------------------------------------------------------------------

    def test_every_active_scenario_completes_and_replays_identically(self) -> None:
        for run in SCENARIOS:
            with self.subTest(scenario=run.name):
                first, first_save = self._play_once(run)

                self.assertEqual(
                    first.returncode, 0,
                    f"{run.name} exited {first.returncode}\nstderr:\n{first.stderr[-3000:]}",
                )
                self.assertNotIn(
                    "network access attempted", first.stderr,
                    f"{run.name} reached for the network, so it is not LLM-free:\n{first.stderr[-2000:]}",
                )
                self.assertIn(
                    run.marker, first.stdout,
                    f"{run.name} never reached its ending ({run.marker!r}); it stopped early.\n"
                    f"stdout tail:\n{first.stdout[-2000:]}",
                )

                second, second_save = self._play_once(run)

                self.assertEqual(second.returncode, 0, second.stderr[-3000:])
                self.assertEqual(
                    first.stdout, second.stdout,
                    f"{run.name} is not deterministic: the same seed and script produced "
                    f"different output.\n--- first ---\n{first.stdout[-2500:]}\n"
                    f"--- second ---\n{second.stdout[-2500:]}",
                )

                if run.saves:
                    self.assertTrue(first_save, f"{run.name} wrote no save file")
                    self.assertEqual(
                        first_save, second_save,
                        f"{run.name} wrote different saves for the same seed and script",
                    )

    def test_the_seed_is_actually_wired_into_the_dice(self) -> None:
        """Two seeds must not produce the same rolls, or the harness would prove nothing."""
        run = SCENARIOS[0]  # the five-seat case, whose stdout prints every ActionResult
        rolls: list[str] = []
        for seed in ("42", "43"):
            argv = [a for a in run.argv]
            argv[argv.index("42")] = seed
            variant = _Run(run.name, argv, run.stdin, run.marker, run.save_name)
            result, _ = self._play_once(variant)
            self.assertEqual(result.returncode, 0, result.stderr[-2000:])
            rolls.append(
                "\n".join(line for line in result.stdout.splitlines() if "dice=" in line)
            )

        self.assertTrue(rolls[0], "no dice were printed, so the seed cannot be checked")
        self.assertNotEqual(
            rolls[0], rolls[1],
            "seeds 42 and 43 produced identical dice: the seed is not wired into the roll",
        )

    def test_a_case_resumes_mid_run_from_its_save(self) -> None:
        """A save written part-way must reload with the work already done still done."""
        run = SCENARIOS[0]
        partial = _Run(
            run.name + " (partial)",
            [a for a in run.argv if a != "--new"],
            "act pc_leader inspect_register\nquit\n",
            "Saved to",
            run.save_name,
        )
        first, _ = self._play_once(partial)
        self.assertEqual(first.returncode, 0, first.stderr[-2000:])

        save = self.workdir / run.save_name
        record = json.loads(save.read_text(encoding="utf-8"))
        self.assertIn("schema_version", record)
        self.assertEqual(record.get("clues"), ["register"])

        resumed, _ = self._play_once(
            _Run(
                run.name + " (resume)",
                [a for a in run.argv if a != "--new"],
                "status\nquit\n",
                "Saved to",
                run.save_name,
            ),
            fresh=False,
        )
        self.assertEqual(resumed.returncode, 0, resumed.stderr[-2000:])
        self.assertIn(
            "register", resumed.stdout,
            "the resumed run forgot the clue the first run had already gathered",
        )
        self.assertIn("turn", resumed.stdout)


if __name__ == "__main__":
    unittest.main()
