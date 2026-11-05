"""Guards for the gameplay-interface architecture and the Python GUI plan (#1184).

Two decisions in this issue are easy to undo by accident:

1. **The scene kind is called Action.** "Combat scene" is the older label; CWN *combat rules* are still
   the resolution mechanism, so the word cannot simply be banned — the scene-kind lists are what matter.
2. **The GUI is a renderer over a view state, not a second rules engine.** If a plan ever says the
   interface resolves a check, the architecture has already failed.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs/design/ARCHITECTURE_1184_GAMEPLAY_INTERFACES.md"
GUI = ROOT / "docs/design/PYTHON_GUI_PLAN_1184.md"
SCENES = ROOT / "docs/design/DRAFT_GRAPH_SCENES_1164.md"
GRAPH_README = ROOT / "design/graphs/README.md"
GRAPH_RULES = ROOT / "design/graphs/RULES.md"

LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(path: Path) -> str:
    return re.sub(r"\s+", " ", text(path))


class TheSceneKindIsAction(unittest.TestCase):
    def test_the_scene_list_names_action_not_combat(self):
        for path in (SCENES, GRAPH_README):
            body = flat(path)
            self.assertIn("Action", body, f"{path.name} does not name the Action scene kind")
            self.assertNotIn("Exploration, Cyber, Combat, Social", body,
                             f"{path.name} still lists Combat as a scene kind")

    def test_the_rules_note_is_updated(self):
        self.assertIn("Action", text(GRAPH_RULES))

    def test_the_architecture_explains_the_rename(self):
        body = text(ARCH).lower()
        self.assertIn("not combat", body, "the Action section must say what it replaces")
        self.assertIn("cwn combat rules still resolve", body)

    def test_finnish_policing_is_the_default_not_a_firefight(self):
        body = text(ARCH).lower()
        for phrase in ("arrest", "pursuit", "hill street blues", "exceptional"):
            self.assertIn(phrase, body, f"the Action section does not mention {phrase}")
        self.assertIn("not an american firefight", body)

    def test_cwn_combat_rules_are_not_renamed(self):
        # The rules keep their name; only the scene label changed.
        body = text(ARCH)
        self.assertIn("CWN combat", body)


class TheArchitectureIsComplete(unittest.TestCase):
    def test_the_six_invariants_are_present(self):
        body = text(ARCH)
        section = body.split("## 2. Design invariants")[1].split("## 3.")[0]
        self.assertEqual(len(re.findall(r"^\d+\. ", section, re.M)), 6)

    def test_the_interface_table_includes_action(self):
        body = text(ARCH)
        self.assertIn("| **Action** |", body)

    def test_the_five_knowledge_categories_are_named(self):
        body = text(ARCH).lower()
        for word in ("world truth", "source claims", "collected evidence", "player knowledge", "hypotheses"):
            self.assertIn(word, body)

    def test_psi_access_matrix_restricts_the_player(self):
        body = text(ARCH)
        self.assertIn("Telepathy and Telekinesis only", body)
        self.assertIn("NPC-only", body)
        self.assertIn("scripted", body.lower())

    def test_law_of_one_stays_lore(self):
        body = text(ARCH).lower()
        self.assertIn("law of one is lore, not rules", body)


class TheGuiPlanIsConcrete(unittest.TestCase):
    def test_it_names_the_stack(self):
        body = text(GUI)
        for tech in ("pygame-ce", "NetworkX"):
            self.assertIn(tech, body, f"the plan does not name {tech}")

    def test_it_names_the_references(self):
        body = text(GUI)
        for ref in ("Citizen Sleeper", "Hacknet", "Cyber Manhunt"):
            self.assertIn(ref, body, f"the plan does not reference {ref}")

    def test_it_has_an_art_direction_and_a_resolution(self):
        body = text(GUI)
        self.assertIn("960×540", body)
        self.assertIn("palette", body.lower())

    def test_the_renderer_is_pure_over_a_view_state(self):
        body = flat(GUI)
        self.assertIn("renderer draws a **view state**", body)
        self.assertIn("never computes a rule", body.replace("**", ""))

    def test_it_has_milestones_starting_from_a_static_mock(self):
        body = text(GUI)
        self.assertIn("| **M0** |", body)
        self.assertIn("Static mock", body)

    def test_it_does_not_add_dependencies_yet(self):
        body = flat(GUI).lower()
        self.assertIn("does not add", body)
        self.assertIn("dependency", body)


class LinksResolve(unittest.TestCase):
    def test_every_relative_link_resolves(self):
        broken = []
        for path in (ARCH, GUI):
            for match in LINK.finditer(text(path)):
                target = match.group(1)
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.name} -> {target}")
        self.assertEqual(broken, [], "broken links: " + "; ".join(broken))


if __name__ == "__main__":
    unittest.main()
