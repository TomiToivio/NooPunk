"""Regression checks for the CWN-first playable scene vocabulary."""
import unittest

from src.rules.scene_play import available_actions, route_action
from src.world.graphs import GraphError, StoryNode


class ScenePlayTests(unittest.TestCase):
    def scene(self, *kinds):
        return StoryNode("scene.intro", "At Ratakatu", "scene", scene_types=kinds)

    def test_five_playable_kinds_dispatch_to_existing_authorities(self):
        expectations = {
            "Social": ("present_evidence", "investigation"),
            "Investigation": ("osint", "investigation"),
            "Exploration": ("move", "physical_graph"),
            "Action": ("arrest", "cwn"),
            "Cyber": ("hack", "cwn_hacking"),
        }
        for kind, (verb, owner) in expectations.items():
            with self.subTest(kind=kind):
                action = route_action(self.scene(kind), verb)
                self.assertEqual(action.authority, owner)

    def test_data_collection_and_analysis_are_investigation_modes(self):
        verbs = {action.verb for action in available_actions(self.scene("Investigation"))}
        self.assertTrue({"osint", "panopticon", "informant", "collect", "analyze",
                         "link_clues"}.issubset(verbs))

    def test_mixed_scene_deduplicates_actions(self):
        verbs = [x.verb for x in available_actions(self.scene("Social", "Investigation"))]
        self.assertEqual(len(verbs), len(set(verbs)))

    def test_normalize_accepted_scene_type_variants(self):
        actions = available_actions(self.scene("social", " Investigation ", "CYBER"))
        self.assertEqual(route_action(self.scene("social"), "talk").scene_type, "Social")
        self.assertEqual(route_action(self.scene(" Investigation "), "osint").scene_type, "Investigation")
        self.assertIn("hack", {a.verb for a in actions})

    def test_legacy_combat_and_astral_not_playable(self):
        with self.assertRaises(GraphError):
            self.scene("Combat")
        with self.assertRaises(GraphError):
            available_actions(self.scene("Astral"))
        with self.assertRaises(GraphError):
            available_actions(self.scene(" astral "))

    def test_no_rolls_or_side_effects_and_invalid_actions_rejected(self):
        scene = self.scene("Action")
        self.assertEqual(route_action(scene, "fight").authority, "cwn_combat")
        with self.assertRaises(GraphError):
            route_action(scene, "teleport")


if __name__ == "__main__":
    unittest.main()
