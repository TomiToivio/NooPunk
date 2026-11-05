"""Scene types are interface shapes, and "Action" is the one this setting means (#1184).

The rename is not cosmetic. The old word imports a genre the setting does not have: Finland is not the
United States, a Finnish police action scene is an arrest, a pursuit, a forced entry, a standoff or a
containment, and the people in it are usually not shooting at each other. The scene type names what the
interface shows and what the player does; the rules layer still resolves the uncertainty inside it.

The negative case is pinned too: the old name must not quietly come back as an accepted type, because a
synonym that validates is a second vocabulary nobody documented.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.world.graphs import SCENE_TYPES, StoryNode
from src.world.graphs import GraphError as GraphContractError


class ActionSceneTypeTests(unittest.TestCase):
    def test_action_replaces_combat(self):
        self.assertIn("Action", SCENE_TYPES)
        self.assertNotIn("Combat", SCENE_TYPES)

    def test_the_other_five_are_unchanged(self):
        self.assertEqual(set(SCENE_TYPES),
                         {"Investigation", "Exploration", "Action", "Social", "Cyber", "Astral"})

    def test_a_scene_may_declare_action(self):
        StoryNode(id="scene.arrest", kind="scene", label="Arrest at Kurvi",
                  scene_types=("Action", "Social"))

    def test_the_old_name_is_refused(self):
        with self.assertRaises(GraphContractError):
            StoryNode(id="scene.firefight", kind="scene", label="Old vocabulary",
                      scene_types=("Combat",))



class TextInterfaceFirstTests(unittest.TestCase):
    """The terminal is a first-class interface, and the docs say so (#1184 + README)."""

    def test_both_design_documents_name_hackmud(self):
        for name in ("ARCHITECTURE_1184_GAMEPLAY_INTERFACES.md",
                     "GUI_PYTHON_1184_MINIMAL_GRAPH_UI.md"):
            body = (ROOT / "docs" / "design" / name).read_text(encoding="utf-8")
            self.assertIn("hackmud", body, f"{name} must carry the README's text-interface reference")

    def test_the_readme_has_no_escaped_newlines(self):
        body = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("\\n\\n", body, "a literal backslash-n was pasted instead of a paragraph break")

if __name__ == "__main__":
    unittest.main()
