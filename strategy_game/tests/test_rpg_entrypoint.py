"""Executable checks for the RPG layer's runnable worked scene (issue #389).

Issue #389's worked example is one short investigation resolving a **cyber** check and a **PSI** check
through the same Fate engine. These are the checks that the example is *runnable as code*: the entry
point exists, the seed reproduces the report, the two domains really do share one engine, and the
payload states both the table's part and this layer's exclusions.

Code-only, per `AGENTS.md` and issue #271: nothing here asserts anything about prose, lore or canon.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
    python -m unittest strategy_game.tests.test_rpg_entrypoint
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game.rpg import (  # noqa: E402
    DEFAULT_SEED,
    ENGINE_DOES_NOT_DECIDE,
    FATE_NOTATION,
    SCENE_REPORT_VERSION,
    Action,
    render_report,
    scene_report,
)
from strategy_game.rpg import boundary, run  # noqa: E402
from strategy_game.rpg.fate import Resolution  # noqa: E402

#: The three demos resolve six checks in total, and every one of them is a Fate check.
CHECK_COUNT = 6


class SceneReportTests(unittest.TestCase):
    """The worked scene: a cyber check and a PSI check, one engine, one seed."""

    def test_the_report_is_deterministic_in_its_seed(self) -> None:
        self.assertEqual(scene_report(3), scene_report(3))
        self.assertEqual(json.dumps(scene_report(3), sort_keys=True),
                         json.dumps(scene_report(3), sort_keys=True))

    def test_a_different_seed_can_be_a_different_scene(self) -> None:
        shapes = {json.dumps(scene_report(seed)["checks"], sort_keys=True) for seed in range(1, 8)}
        self.assertGreater(len(shapes), 1, "the seed must actually drive the dice")

    def test_the_investigation_runs_a_cyber_and_a_psi_check_on_one_engine(self) -> None:
        report = scene_report(DEFAULT_SEED)
        checks = {(check["scene"], check["check"]): check for check in report["checks"]}
        self.assertIs(checks[("investigation", "cyber")]["action"], Action.OVERCOME.value)
        self.assertIs(checks[("investigation", "psi")]["action"], Action.CREATE_ADVANTAGE.value)
        # One engine means one resolution shape: four Fate dice, a skill, and a shift count.
        self.assertEqual(len(report["checks"]), CHECK_COUNT)
        self.assertEqual(report["dice"], FATE_NOTATION)
        for check in report["checks"]:
            self.assertEqual(len(check["dice"]), 4)
            self.assertTrue(all(face in (-1, 0, 1) for face in check["dice"]))
            self.assertEqual(check["total"], sum(check["dice"]) + check["skill"])
            self.assertEqual(check["shifts"], check["total"] - check["difficulty"])
        self.assertEqual({check["action"] for check in report["checks"]},
                         {Action.OVERCOME.value, Action.CREATE_ADVANTAGE.value, Action.DEFEND.value})

    def test_every_reported_check_is_a_resolution_the_demos_produced(self) -> None:
        scenes = {
            "investigation": run._scenes(DEFAULT_SEED)["investigation"],
            "netrunning": run._scenes(DEFAULT_SEED)["netrunning"],
            "foothold": run._scenes(DEFAULT_SEED)["foothold"],
        }
        for scene, check in run._CHECK_ORDER:
            candidate = scenes[scene].get(check)
            with self.subTest(scene=scene, check=check):
                self.assertIsInstance(candidate, Resolution)

    def test_the_report_states_what_the_engine_does_not_decide(self) -> None:
        report = scene_report(2)
        self.assertEqual(report["engine_does_not_decide"], list(ENGINE_DOES_NOT_DECIDE))
        self.assertIn("scene pacing and turn order", report["engine_does_not_decide"])
        self.assertIn("anything belonging to faction strategy or political simulation",
                      report["engine_does_not_decide"])
        self.assertEqual(report["schema_version"], SCENE_REPORT_VERSION)

    def test_the_report_reuses_the_boundarys_declared_exclusions(self) -> None:
        """The seam is read, not restated: one declaration, one place to change it."""
        self.assertEqual(scene_report(2)["boundary_excludes"], list(boundary.NOT_THIS_LAYER))
        self.assertTrue(scene_report(2)["boundary_excludes"])

    def test_the_text_rendering_shows_every_check_and_the_table_s_part(self) -> None:
        report = scene_report(DEFAULT_SEED)
        text = render_report(report)
        for check in report["checks"]:
            self.assertIn(f"{check['scene']}/{check['check']}", text)
            self.assertIn(check["outcome"], text)
        self.assertIn(f"checks resolved: {CHECK_COUNT}", text)
        self.assertIn("The table keeps:", text)
        self.assertIn("This layer excludes:", text)

    def test_the_report_module_imports_only_this_package(self) -> None:
        """The runnable report adds no cross-layer coupling: it reaches up to nothing at all."""
        import importlib

        entrypoint = importlib.import_module("strategy_game.rpg.__main__")
        for module in (run, entrypoint):
            source = Path(module.__file__).read_text(encoding="utf-8")
            self.assertEqual(re.findall(r"^\s*from\s+(\.\.+)", source, re.MULTILINE), [],
                             f"{Path(module.__file__).name} imports from a parent package")


class EntrypointTests(unittest.TestCase):
    """``python -m strategy_game.rpg`` runs the report, and the pinned scaffold surface is untouched."""

    def test_the_entrypoint_emits_the_scene_report(self) -> None:
        result = subprocess.run([sys.executable, "-m", "strategy_game.rpg"], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], SCENE_REPORT_VERSION)
        self.assertEqual(payload["rolls_made"], CHECK_COUNT)
        self.assertEqual(list(payload), sorted(payload))
        self.assertEqual(payload["boundary_excludes"], list(boundary.NOT_THIS_LAYER))

    def test_the_entrypoint_accepts_a_seed_and_a_text_mode(self) -> None:
        as_json = subprocess.run([sys.executable, "-m", "strategy_game.rpg", "--seed", "7"],
                                 cwd=ROOT, capture_output=True, text=True, check=False)
        as_text = subprocess.run([sys.executable, "-m", "strategy_game.rpg", "--seed", "7", "--text"],
                                 cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(as_json.returncode, 0, as_json.stderr)
        self.assertEqual(as_text.returncode, 0, as_text.stderr)
        self.assertEqual(json.loads(as_json.stdout)["seed"], 7)
        self.assertIn(f"checks resolved: {CHECK_COUNT}", as_text.stdout)
        # Text, not JSON: the first line is the scene heading rather than a brace.
        self.assertFalse(as_text.stdout.lstrip().startswith("{"))

    def test_the_rpg_package_declares_its_own_exports(self) -> None:
        import strategy_game
        import strategy_game.rpg as package

        self.assertGreater(len(package.__all__), 15)
        for name in package.__all__:
            with self.subTest(export=name):
                self.assertTrue(hasattr(package, name))
        # Its own surface only: nothing leaks into, or out of, the pinned scaffold export list.
        self.assertEqual(set(package.__all__) & set(strategy_game.__all__), set())
        with self.assertRaises(ImportError):
            from strategy_game import Character  # noqa: F401

    def test_the_pinned_scaffold_surface_is_unchanged(self) -> None:
        import strategy_game

        self.assertEqual(set(strategy_game.__all__),
                         {"WorldState", "Provenance", "ProvenanceKind",
                          "PoliticalField", "SignifierRole", "PowerMode"})
        result = subprocess.run([sys.executable, "-m", "strategy_game"], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(json.loads(result.stdout)),
                         {"schema_version", "locations", "network_nodes", "network_edges", "assets"})


if __name__ == "__main__":
    unittest.main()
