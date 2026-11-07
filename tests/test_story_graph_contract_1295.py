"""The Story Graph contract: the delta on the merged #1295 skeleton.

The skeleton (#1297/#1296) created the folders, the boundary rule and the templates. What it left open is the
part the issue calls the *common contract*: stable identifiers, a canonical document format, schema versioning
and validation adapters. This file tests exactly that:

* a graph document declares its schema version;
* every node says where it came from, and an unsourced node is refused unless Tomi approved it by hand;
* a choice is a labelled edge, not an unlabelled adjacency;
* the RPG consumes the validated graph through its own existing `StoryGraph`, not a second one.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH_ROOT = ROOT / "NooPunk-Story" / "Graph"
EXAMPLE = GRAPH_ROOT / "examples" / "demo_story_graph.json"


def example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def validate(document: dict) -> list:
    from src.contracts.story_graph_contract import validate as check

    return check(document, story_root=GRAPH_ROOT)


class ContractShapeTests(unittest.TestCase):
    def test_the_contract_file_names_both_schemas(self):
        contract = json.loads((ROOT / "data" / "schema" / "subproject_contracts_1295.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["story_graph"]["schema"], "noopunk.story_graph/1")
        self.assertEqual(contract["tag_graph"]["schema"], "noopunk.tag_graph/1")
        self.assertIn("story", [s["id"] for s in contract["subprojects"]])
        self.assertIn("simulator", [s["id"] for s in contract["subprojects"]])
        self.assertIn("rpg", [s["id"] for s in contract["subprojects"]])

    def test_the_directions_never_point_back_at_the_manuscript(self):
        contract = json.loads((ROOT / "data" / "schema" / "subproject_contracts_1295.json").read_text(encoding="utf-8"))
        directions = {(d["from"], d["to"]) for d in contract["directions"]}
        self.assertIn(("story", "story_graph"), directions)
        self.assertIn(("story_graph", "rpg"), directions)
        self.assertNotIn(("rpg", "story"), directions)
        self.assertNotIn(("story_graph", "story"), directions)


class ValidationTests(unittest.TestCase):
    def test_the_example_validates(self):
        self.assertEqual(validate(example()), [])

    def test_an_unsourced_scene_is_refused(self):
        document = example()
        document["nodes"].append(
            {"id": "scene.invented", "kind": "scene", "label": "An invented scene",
             "source_ref": "does/not/exist.md", "parent_id": "episode.demo.01"}
        )
        problems = validate(document)
        self.assertTrue(any("not in the manuscript" in problem for problem in problems), problems)

    def test_an_hand_approved_node_may_stand_outside_the_manuscript(self):
        document = example()
        document["nodes"].append(
            {"id": "scene.approved", "kind": "scene", "label": "Approved elsewhere",
             "source_ref": "nowhere.md", "parent_id": "episode.demo.01", "authored": True}
        )
        self.assertEqual(validate(document), [])

    def test_a_duplicate_id_is_refused(self):
        document = example()
        document["nodes"].append(dict(document["nodes"][0]))
        self.assertTrue(any("duplicate node id" in p for p in validate(document)))

    def test_a_choice_without_a_label_is_refused(self):
        document = example()
        document["edges"][0].pop("label")
        self.assertTrue(any("choice without a label" in p for p in validate(document)))

    def test_an_unknown_scene_type_is_refused(self):
        document = example()
        document["nodes"][2]["scene_types"] = ["Space Opera"]
        self.assertTrue(any("unknown scene type" in p for p in validate(document)))

    def test_a_wrong_schema_version_is_refused(self):
        document = example()
        document["schema"] = "noopunk.story_graph/0"
        self.assertTrue(any("schema must be" in p for p in validate(document)))

    def test_choices_are_edges_with_labels(self):
        from src.contracts.story_graph_contract import choices

        self.assertEqual([edge["label"] for edge in choices(example(), "scene.demo.corridor")],
                         ["Open the door and go in"])


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


if __name__ == "__main__":
    unittest.main()
