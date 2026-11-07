"""The three subprojects, their contract, and the manuscript boundary (#1295).

The structural half of the architecture pivot, tested so that "independent subprojects" is not a diagram in a
document: directories exist, the Story Graph contract refuses an unsourced scene, the RPG adapter feeds the
graph structure the RPG already had, and the manuscript boundary fails closed.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "NooPunk-Story" / "Graph" / "examples" / "demo_story_graph.json"
TOOL = ROOT / "tools" / "check_story_boundary.py"


GRAPH_ROOT = ROOT / "NooPunk-Story" / "Graph"


def example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def validate_example(document: dict) -> list:
    from src.contracts.story_graph_contract import validate

    return validate(document, story_root=GRAPH_ROOT)


class StructureTests(unittest.TestCase):
    def test_the_three_subprojects_exist_with_readmes(self):
        for name in ("NooPunk-Story", "NooPunk-Simulator", "NooPunk-RPG"):
            path = ROOT / name
            self.assertTrue(path.is_dir(), name)
            self.assertTrue((path / "README.md").is_file(), f"{name} has no README")

    def test_story_is_split_into_manuscript_and_graph(self):
        self.assertTrue((ROOT / "NooPunk-Story" / "Story").is_dir())
        self.assertTrue((ROOT / "NooPunk-Story" / "Graph").is_dir())

    def test_the_manuscript_policy_is_written_down(self):
        policy = (ROOT / "NooPunk-Story" / "Story" / "POLICY.md").read_text(encoding="utf-8")
        self.assertIn("Tomi only", policy)
        self.assertIn("may not", policy.lower())

    def test_author_templates_are_prompts_not_prose(self):
        for name in ("BRANCHING_SCENE.md", "NOVEL_CHAPTER.md"):
            text = (ROOT / "NooPunk-Story" / "Graph" / "templates" / name).read_text(encoding="utf-8")
            self.assertIn("Tomi writes here", text)
            self.assertNotIn("AGENT-GENERATED", text.upper())


class ContractTests(unittest.TestCase):
    def test_the_example_validates(self):
        self.assertEqual(validate_example(example()), [])

    def test_an_unsourced_scene_is_refused(self):
        document = example()
        document["nodes"].append(
            {"id": "scene.invented", "kind": "scene", "label": "An invented scene",
             "source_ref": "does/not/exist.md", "parent_id": "episode.demo.01"}
        )
        problems = validate_example(document)
        self.assertTrue(any("not in the manuscript" in problem for problem in problems), problems)

    def test_an_authored_node_may_stand_outside_the_manuscript(self):
        """`authored: true` is the only legal way to add a scene Tomi approved by hand."""
        document = example()
        document["nodes"].append(
            {"id": "scene.approved", "kind": "scene", "label": "Approved elsewhere",
             "source_ref": "nowhere.md", "parent_id": "episode.demo.01", "authored": True}
        )
        self.assertEqual(validate_example(document), [])

    def test_a_duplicate_id_is_refused(self):
        document = example()
        document["nodes"].append(dict(document["nodes"][0]))
        self.assertTrue(any("duplicate node id" in p for p in validate_example(document)))

    def test_a_choice_without_a_label_is_refused(self):
        document = example()
        document["edges"][0].pop("label")
        self.assertTrue(any("choice without a label" in p for p in validate_example(document)))

    def test_an_unknown_scene_type_is_refused(self):
        document = example()
        document["nodes"][2]["scene_types"] = ["Space Opera"]
        self.assertTrue(any("unknown scene type" in p for p in validate_example(document)))

    def test_choices_are_returned_by_source(self):
        from src.contracts.story_graph_contract import choices

        self.assertEqual(len(choices(example(), "scene.demo.corridor")), 1)


class RpgAdapterTests(unittest.TestCase):
    def test_the_graph_becomes_the_rpgs_own_structure(self):
        from src.contracts.rpg_scene_adapter import to_story_graph
        from src.world.graphs import StoryGraph

        graph = to_story_graph(example(), story_root=GRAPH_ROOT)
        self.assertIsInstance(graph, StoryGraph)
        self.assertIn("scene.demo.corridor", graph.nodes)
        self.assertEqual(graph.nodes["scene.demo.office"].prerequisites, ("corridor_door_opened",))
        self.assertEqual(len(graph.links), 2)

    def test_the_adapter_refuses_an_invalid_hierarchy(self):
        from src.contracts.rpg_scene_adapter import to_story_graph
        from src.world.graphs import GraphError

        document = example()
        document["nodes"][3]["parent_id"] = "scene.demo.corridor"  # a scene under a scene
        with self.assertRaises(GraphError):
            to_story_graph(document, story_root=GRAPH_ROOT)


class BoundaryToolTests(unittest.TestCase):
    def run_tool(self, *args, env=None):
        return subprocess.run(
            [sys.executable, str(TOOL), *args],
            cwd=ROOT, capture_output=True, text=True,
            env={**os.environ, **(env or {})},
        )

    def test_the_static_check_passes_on_a_clean_tree(self):
        result = self.run_tool("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK", result.stdout)

    def test_the_change_check_refuses_an_agent_story_edit(self):
        """A changed manuscript file fails unless the human-authorisation variable is set."""
        story = ROOT / "NooPunk-Story" / "Story" / "BOUNDARY_PROBE.md"
        try:
            story.write_text("probe\n", encoding="utf-8")
            refused = self.run_tool("--changed", "--base", "HEAD")
            self.assertNotEqual(refused.returncode, 0, "an agent story edit must fail")
            self.assertIn("human-only", refused.stderr)
            allowed = self.run_tool("--changed", "--base", "HEAD", env={"NOOPUNK_STORY_HUMAN_AUTHOR": "1"})
            self.assertEqual(allowed.returncode, 0, allowed.stderr)
        finally:
            story.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
