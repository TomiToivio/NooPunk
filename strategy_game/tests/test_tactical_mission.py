"""Executable contracts for the mission-data schema and its renderer independence (issue #515).

Code-only, per ``AGENTS.md``: nothing here asserts prose. It exercises the loader — what a mission
document may and may not say, and why an unplayable one is refused by name — and it proves the
package has no rendering dependency: an import-graph scan, a subprocess whose ``site`` is disabled,
and a recursive check that no presentation field can survive in mission data.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap
    sys.path.insert(0, str(ROOT))

from strategy_game.tactical import mission as mission_module
from strategy_game.tactical.grid import Grid
from strategy_game.tactical.mission import (
    MISSION_DATA_PATH,
    MISSION_FORMAT,
    MISSION_SCHEMA_VERSION,
    InteractionKind,
    MissionError,
    load_mission,
    mission_from_dict,
)

PACKAGE = Path(mission_module.__file__).resolve().parent

#: Field names that would mean presentation had leaked into mission data. The schema refuses unknown
#: keys, so this list is a second, explicit statement of the same rule.
PRESENTATION_KEYS = (
    "sprite", "spritesheet", "tileset", "tile_id", "tileid", "texture", "pixel", "pixels",
    "px", "colour", "color", "camera", "layer", "z_index", "animation", "font",
)


def document() -> dict:
    """The packaged fixture, parsed but not yet validated, so a test can mutate a copy."""
    return json.loads(MISSION_DATA_PATH.read_text(encoding="utf-8"))


def refused(payload: dict) -> str:
    """Load a mutated document and return the refusal text; fail if it loads."""
    try:
        mission_from_dict(payload)
    except MissionError as exc:
        return str(exc)
    raise AssertionError("the document loaded, but the test expected a refusal")


class FixtureSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = load_mission()

    def test_the_packaged_fixture_declares_the_format_and_is_marked_a_fixture(self):
        doc = document()
        self.assertEqual(doc["format"], MISSION_FORMAT)
        self.assertEqual(doc["schema_version"], MISSION_SCHEMA_VERSION)
        self.assertEqual(doc["status"], "SPIKE_FIXTURE")
        self.assertIn("not scenario canon", doc["note"])

    def test_the_fixture_carries_all_three_interaction_kinds(self):
        kinds = {item.kind for item in self.spec.interactions}
        self.assertEqual(kinds, set(InteractionKind))

    def test_the_fixture_has_two_required_objectives(self):
        required = [o.id for o in self.spec.required_objectives]
        self.assertEqual(required, ["interview_witness", "read_ledger"])

    def test_the_fixture_has_no_schema_problems(self):
        self.assertEqual(self.spec.problems(), ())

    def test_the_fixture_separates_the_clue_from_the_dialogue(self):
        witness = self.spec.interaction("interview_witness")
        clue = self.spec.interaction("read_ledger")
        self.assertFalse(witness.has_check)
        self.assertTrue(clue.has_check)
        self.assertEqual(clue.requires, ("interview_witness",))

    def test_a_mission_round_trips_through_its_json_form(self):
        self.assertEqual(mission_from_dict(self.spec.to_dict()), self.spec)

    def test_the_only_map_representation_is_the_grid_section(self):
        self.assertEqual(set(self.spec.to_dict()["grid"]), {"width", "height", "legend", "rows"})
        self.assertEqual(Grid.from_dict(self.spec.to_dict()["grid"]), self.spec.grid)

    def test_no_presentation_key_appears_anywhere_in_the_document(self):
        def walk(value, path="mission"):
            if isinstance(value, dict):
                for key, item in value.items():
                    self.assertNotIn(
                        str(key).lower(), PRESENTATION_KEYS,
                        f"presentation field {key!r} at {path}",
                    )
                    walk(item, f"{path}.{key}")
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    walk(item, f"{path}[{index}]")

        walk(self.spec.to_dict())


class RefusalTests(unittest.TestCase):
    def test_an_unknown_top_level_field_is_refused(self):
        doc = document()
        doc["tile_size"] = 16
        self.assertIn("does not define", refused(doc))

    def test_a_sprite_on_an_interaction_is_refused(self):
        doc = document()
        doc["interactions"][0]["sprite"] = "clerk.png"
        message = refused(doc)
        self.assertIn("sprite", message)
        self.assertIn("presentation fields", message)

    def test_a_missing_format_is_refused(self):
        doc = document()
        del doc["format"]
        self.assertIn("expected 'noopunk.tactical.mission'", refused(doc))

    def test_a_foreign_schema_version_is_refused(self):
        doc = document()
        doc["schema_version"] = "tactical-mission-0"
        self.assertIn("unsupported mission schema_version", refused(doc))

    def test_a_different_squad_size_is_refused(self):
        doc = document()
        doc["deploy_cells"] = doc["deploy_cells"][:3]
        message = refused(doc)
        self.assertIn("exactly 4 agents", message)

    def test_duplicate_deployment_cells_are_refused(self):
        doc = document()
        doc["deploy_cells"][1] = list(doc["deploy_cells"][0])
        self.assertIn("same cell", refused(doc))

    def test_deploying_onto_a_wall_is_refused(self):
        doc = document()
        doc["deploy_cells"][0] = [0, 0]
        self.assertIn("cannot be stood on", refused(doc))

    def test_an_objective_no_interaction_completes_is_refused(self):
        doc = document()
        doc["objectives"].append({"id": "unreachable_goal", "label": "spike:nothing", "required": True})
        self.assertIn("completed by no interaction", refused(doc))

    def test_a_required_objective_completed_only_by_an_optional_hook_is_refused(self):
        doc = document()
        doc["objectives"].append({"id": "signed", "label": "spike:signed", "required": True})
        doc["interactions"][2]["objectives"] = ["signed"]
        self.assertIn("only completed by an optional hook", refused(doc))

    def test_a_dialogue_may_not_declare_a_check(self):
        doc = document()
        doc["interactions"][0].update({"action": "overcome", "skill": "SAV", "difficulty": 1})
        self.assertIn("talking carries no Fate check", refused(doc))

    def test_a_clue_needs_an_action_a_skill_and_a_difficulty(self):
        doc = document()
        del doc["interactions"][1]["difficulty"]
        self.assertIn("needs an action, a skill and a difficulty", refused(doc))

    def test_an_unknown_fate_action_is_refused(self):
        doc = document()
        doc["interactions"][1]["action"] = "shoot"
        self.assertIn("expected one of", refused(doc))

    def test_a_strategic_skill_is_refused_on_an_individual_check(self):
        doc = document()
        doc["interactions"][1]["skill"] = "fieldcraft"
        message = refused(doc)
        self.assertIn("individual", message)
        self.assertIn("COG", message)

    def test_an_optional_flag_on_a_clue_is_refused(self):
        doc = document()
        doc["interactions"][1]["optional"] = True
        self.assertIn("only a confrontation", refused(doc))

    def test_an_unknown_prerequisite_is_refused(self):
        doc = document()
        doc["interactions"][1]["requires"] = ["a_dialogue_that_does_not_exist"]
        self.assertIn("requires unknown interaction", refused(doc))

    def test_a_prerequisite_cycle_is_refused(self):
        doc = document()
        doc["interactions"][0]["requires"] = ["read_ledger"]
        self.assertIn("prerequisite cycle", refused(doc))

    def test_an_interaction_behind_a_shut_door_is_unreachable_and_refused(self):
        doc = document()
        doc["grid"]["closed_doors"] = [[6, 10]]
        message = refused(doc)
        self.assertIn("unreachable from deployment cell", message)
        self.assertIn("closed", message)

    def test_a_mission_without_a_status_is_refused(self):
        doc = document()
        doc["status"] = ""
        self.assertIn("declares its status", refused(doc))

    def test_a_missing_file_is_refused_by_path(self):
        with self.assertRaises(MissionError) as raised:
            load_mission(Path(tempfile.gettempdir()) / "no-such-mission-515.json")
        self.assertIn("not found", str(raised.exception))

    def test_invalid_json_is_refused_with_the_reason(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(MissionError) as raised:
                load_mission(path)
        self.assertIn("not valid JSON", str(raised.exception))


class RendererIndependenceTests(unittest.TestCase):
    def test_the_package_imports_only_the_standard_library_and_its_own_project(self):
        allowed = set(sys.stdlib_module_names) | {"strategy_game"}
        offenders: list[str] = []
        for path in sorted(PACKAGE.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if node.level:  # a relative import stays inside the package
                        continue
                    roots = [(node.module or "").split(".")[0]]
                else:
                    continue
                offenders.extend(
                    f"{path.name}: {root}" for root in roots if root and root not in allowed
                )
        self.assertEqual(offenders, [], "the mission layer gained a third-party import")

    def test_no_rendering_library_is_named_anywhere_in_the_package(self):
        blocked = (
            "pygame", "pyglet", "arcade", "moderngl", "opengl", "tkinter", "PIL", "godot",
            "numpy", "pysdl2", "sdl2",
        )
        for path in sorted(PACKAGE.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            for name in blocked:
                self.assertNotIn(
                    f"import {name}", source, f"{path.name} imports {name}"
                )

    def test_the_package_imports_with_site_packages_disabled(self):
        completed = subprocess.run(
            [sys.executable, "-S", "-c",
             "import strategy_game.tactical as t; print(len(t.__all__))"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertGreater(int(completed.stdout.strip()), 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
