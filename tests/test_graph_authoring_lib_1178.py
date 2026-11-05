"""Markdown/YAML frontmatter authoring tests for issue #1178."""
import json
import unittest

from src.rules.graph_authoring import compile_graphs, read_record
from src.world.graphs import GraphError as GraphContractError


def doc(family: str, data: dict) -> str:
    return "---\n" + json.dumps({"record_id": "graph." + family,
                                 "graph_type": family, "data": data}) + (
        "\n---\n# Example author prose\nUse normal CWN rules here.\n"
    )


class AuthoringTests(unittest.TestCase):
    def test_json_frontmatter_is_valid_yaml_and_prose_is_retained(self):
        record = read_record(doc("physical", {
            "graph_type": "physical", "version": 1,
            "nodes": [{"id": "physical.home", "label": "Home"}],
            "edges": [],
            "positions": {"pc": "physical.home"},
        }))
        self.assertEqual(record["record_id"], "graph.physical")
        self.assertIn("Use normal CWN", record["description"])

    def test_compile_four_records_without_astral(self):
        inputs = {
            "physical": {"graph_type": "physical",
                         "nodes": [{"id": "physical.home", "label": "Home"}],
                         "edges": [], "occupants": {"pc": "physical.home"}},
            "cyber": {"graph_type": "cyber",
                      "nodes": [{"id": "cyber.camera", "label": "Camera",
                                 "device_type": "camera", "physical_location": "physical.home",
                                 "actions": ["record"]}],
                      "edges": [], "avatars": {"avatar": "cyber.camera"}},
            "social": {"graph_type": "social",
                       "nodes": [{"id": "pc", "label": "PC", "kind": "character"}],
                       "edges": []},
            "story": {"graph_type": "story",
                      "nodes": [{"id": "scene.home", "label": "Home arrival",
                                 "kind": "scene", "scene_types": ["Investigation"]}],
                      "edges": []},
        }
        records = [read_record(doc(family, data)) for family, data in inputs.items()]
        result = compile_graphs(records)
        self.assertEqual(result.physical.occupants["pc"], "physical.home")
        self.assertEqual(result.cyber.nodes["cyber.camera"].physical_location, "physical.home")
        self.assertEqual(result.story.nodes["scene.home"].scene_types, ("Investigation",))
        self.assertEqual(result.to_dict()["format"], "noopunk.world.graphs")
        self.assertEqual(result.cyber.avatars, {"avatar": "cyber.camera"})

    def test_rejects_invalid_records_and_astral(self):
        with self.assertRaises(GraphContractError):
            read_record("# no frontmatter")
        with self.assertRaises(GraphContractError):
            read_record("---\n[]\n---\n")
        with self.assertRaises(GraphContractError):
            compile_graphs([{"record_id": "a", "graph_type": "astral",
                             "data": {"graph_type": "astral"}}])
        with self.assertRaises(GraphContractError):
            compile_graphs([])


if __name__ == "__main__":
    unittest.main()
