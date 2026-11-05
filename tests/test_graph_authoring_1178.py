"""The YAML front door must accept what the model accepts and refuse what it refuses (#1178).

Behaviour tests of `tools/graph_authoring.py`, not of prose: the tool exists so an author can edit
YAML and get the same `noopunk.world.graphs` snapshot the runtime reads. A tool that silently
accepted a broken record would be worse than no tool, so the negative cases matter more than the
positive ones.

Since the #1178 graph merge there is one model — `src/world/graphs.py` — and this tool is its front
door, not a second schema.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
_spec = importlib.util.spec_from_file_location("graph_authoring", ROOT / "tools" / "graph_authoring.py")
assert _spec is not None and _spec.loader is not None
graph_authoring = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(graph_authoring)


def run(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = graph_authoring.main(argv)
    return code, out.getvalue(), err.getvalue()


class ExampleTest(unittest.TestCase):
    def test_the_shipped_example_validates(self) -> None:
        """The starter file an author is given must itself pass --check."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example.yaml"
            path.write_text(graph_authoring.EXAMPLE, encoding="utf-8")
            code, out, err = run(["--check", str(path)])

        self.assertEqual(code, 0, err)
        self.assertIn("2 physical", out)
        self.assertIn("2 social", out)

    def test_the_example_is_a_world_graph_snapshot(self) -> None:
        data = __import__("yaml").safe_load(graph_authoring.EXAMPLE)
        self.assertEqual(data["format"], "noopunk.world.graphs")
        self.assertEqual(data["version"], 1)
        for family in ("physical", "cyber", "social", "story"):
            self.assertIn(family, data)
        self.assertNotIn("astral", data)

    def test_example_prints_without_a_path(self) -> None:
        code, out, err = run(["--example"])
        self.assertEqual(code, 0, err)
        self.assertIn("noopunk.world.graphs", out)


class RejectionTest(unittest.TestCase):
    def _check(self, text: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.yaml"
            path.write_text(text, encoding="utf-8")
            code, _out, err = run(["--check", str(path)])
        return code, err

    def test_a_social_score_outside_the_range_is_refused(self) -> None:
        code, err = self._check(graph_authoring.EXAMPLE.replace("score: 3", "score: 9"))
        self.assertEqual(code, 1)
        self.assertIn("relationship score", err)

    def test_a_cyber_device_in_a_missing_place_is_refused(self) -> None:
        code, err = self._check(
            graph_authoring.EXAMPLE.replace("physical_location: loc.ratakatu.hq",
                                            "physical_location: loc.nowhere")
        )
        self.assertEqual(code, 1)
        self.assertIn("unknown physical location", err)

    def test_a_missing_family_is_refused(self) -> None:
        broken = graph_authoring.EXAMPLE.replace("social:\n  graph_type: social", "ssocial:\n  graph_type: social")
        code, err = self._check(broken)
        self.assertEqual(code, 1)
        self.assertIn("social", err)

    def test_an_actor_used_as_a_place_is_refused(self) -> None:
        """The corrected node semantics: occupancy is not a node."""
        broken = graph_authoring.EXAMPLE.replace(
            '    - id: loc.ratakatu.hq\n      label: "Europol HQ, Ratakatu"',
            '    - id: act.rookie\n      label: "Europol HQ, Ratakatu"',
        )
        code, err = self._check(broken)
        self.assertEqual(code, 1)
        self.assertTrue(err.startswith("INVALID:"), err)

    def test_a_combat_scene_is_refused(self) -> None:
        """Action is the scene kind; the old word is not an accepted alias (#1184)."""
        broken = graph_authoring.EXAMPLE.replace("scene_types: [Social]", "scene_types: [Combat]")
        code, err = self._check(broken)
        self.assertEqual(code, 1)
        self.assertIn("Action is the scene kind, not Combat", err)


class SnapshotTest(unittest.TestCase):
    def test_json_output_is_the_canonical_snapshot(self) -> None:
        from src.world.graphs import WorldGraphs

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example.yaml"
            path.write_text(graph_authoring.EXAMPLE, encoding="utf-8")
            code, out, err = run(["--json", str(path)])

        self.assertEqual(code, 0, err)
        graphs = WorldGraphs.from_dict(json.loads(out))
        self.assertIn("loc.ratakatu.hq", graphs.physical.nodes)
        self.assertEqual(graphs.physical.occupants, {"act.rookie": "loc.ratakatu.hq"})
        self.assertEqual(len(graphs.cyber.nodes["cyber.hq.camera"].actions), 2)
        self.assertEqual(graphs.to_dict()["format"], "noopunk.world.graphs")


if __name__ == "__main__":
    unittest.main()
