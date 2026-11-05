"""The YAML front door must accept what the model accepts and refuse what it refuses (#1178).

These are behaviour tests of `tools/graph_authoring.py`, not of prose: the tool exists so an author
can edit YAML and get the same `noopunk.four_graphs` snapshot the engine reads. A tool that silently
accepted a broken record would be worse than no tool, so the negative cases matter more than the
positive ones.
"""

from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
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

    def test_the_example_is_a_four_graph_snapshot(self) -> None:
        data = __import__("yaml").safe_load(graph_authoring.EXAMPLE)
        self.assertEqual(data["format"], "noopunk.four_graphs")
        self.assertEqual(data["version"], 1)
        for family in ("physical", "cyber", "social", "story"):
            self.assertIn(family, data)

    def test_example_prints_without_a_path(self) -> None:
        code, out, err = run(["--example"])
        self.assertEqual(code, 0, err)
        self.assertIn("noopunk.four_graphs", out)


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
        self.assertIn("-4..+4", err)

    def test_a_cyber_device_in_a_missing_place_is_refused(self) -> None:
        code, err = self._check(
            graph_authoring.EXAMPLE.replace("physical_ref: loc.ratakatu.hq", "physical_ref: loc.nowhere")
        )
        self.assertEqual(code, 1)
        self.assertIn("unknown Physical location", err)

    def test_a_missing_family_is_refused(self) -> None:
        broken = graph_authoring.EXAMPLE.replace("social:\n  graph_type: social", "ssocial:\n  graph_type: social")
        code, err = self._check(broken)
        self.assertEqual(code, 1)
        self.assertIn("social", err)

    def test_an_actor_used_as_a_place_is_refused(self) -> None:
        """The corrected node semantics: occupancy is not a node."""
        broken = graph_authoring.EXAMPLE.replace(
            "    - id: loc.ratakatu.hq\n      label: \"Europol HQ, Ratakatu\"",
            "    - id: act.rookie\n      label: \"Europol HQ, Ratakatu\"",
        )
        code, err = self._check(broken)
        self.assertEqual(code, 1)
        self.assertTrue(err.startswith("INVALID:"))


class SnapshotTest(unittest.TestCase):
    def test_json_output_is_the_canonical_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example.yaml"
            path.write_text(graph_authoring.EXAMPLE, encoding="utf-8")
            code, out, err = run(["--json", str(path)])

        self.assertEqual(code, 0, err)
        graphs = graph_authoring.FourGraphs.from_json(out)
        self.assertIn("loc.ratakatu.hq", graphs.physical.nodes)
        self.assertEqual(graphs.physical.positions, {"act.rookie": "loc.ratakatu.hq"})
        self.assertEqual(len(graphs.cyber.nodes["cyber.hq.camera"].device_actions), 2)


if __name__ == "__main__":
    unittest.main()
