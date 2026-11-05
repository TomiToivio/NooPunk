"""#1184: the interface architecture and the GUI plan, guarded at their boundaries.

The failure mode this guards against is not a missing paragraph. It is drift: an interface quietly
growing its own rules, "combat" creeping back in as the default scene, or the GUI importing pygame
into the core. These tests pin the boundaries, not the prose.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "design" / "GAMEPLAY_INTERFACES_1184.md"
GUI = ROOT / "docs" / "design" / "GUI_PYTHON_GRAPH_1184.md"
SCENES = ROOT / "docs" / "design" / "DRAFT_GRAPH_SCENES_1164.md"
REGISTER = ROOT / "docs" / "DOCUMENT_REGISTER.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(path: Path) -> str:
    raw = re.sub(r"(?m)^\s*>\s?", "", text(path))
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", raw))


class Architecture(unittest.TestCase):
    def test_genre_is_settled_and_fantasy_is_out(self):
        body = flat(ARCH)
        self.assertIn("apocalyptic cyberpunk science fiction", body)
        self.assertIn("not a fantasy RPG", body)
        self.assertIn("CWN is the immutable core", body)

    def test_action_replaces_combat_as_the_scene_kind(self):
        body = flat(ARCH)
        self.assertIn("Action scenes, not combat scenes", body)
        self.assertIn("Hill Street Blues", body)
        self.assertIn("Finnish police story", body)
        for verb in ("Arrest", "Pursuit", "Containment"):
            self.assertIn(verb, body)
        # "combat" may survive only as CWN's rules chapter name.
        self.assertIn("CWN combat rules", body)

    def test_the_five_evidence_registers_are_distinct(self):
        body = flat(ARCH)
        for register in ("World truth", "Source claim", "Collected evidence",
                         "Player knowledge", "Hypothesis"):
            self.assertIn(register, body)
        self.assertIn("never auto-promoted to truth", body)

    def test_psi_access_matrix_keeps_the_player_limits(self):
        body = flat(ARCH)
        self.assertIn("Telepathy and Telekinesis only", body)
        self.assertIn("NPC only", body)
        self.assertIn("Mutants", body)
        self.assertIn("Law of One is lore, not rules", body)

    def test_no_interface_invents_a_mechanic(self):
        body = flat(ARCH)
        self.assertIn("An interface never invents a mechanic", body)

    def test_the_1164_draft_now_says_action(self):
        body = text(SCENES)
        self.assertIn("Exploration, Cyber, **Action**, Social, Investigation and Astral", body)
        self.assertNotIn("Exploration, Cyber, Combat, Social", body)


class GuiPlan(unittest.TestCase):
    def test_stack_is_optional_and_named(self):
        body = flat(GUI)
        self.assertIn("pygame-ce", body)
        self.assertIn("networkx", body)
        self.assertIn("optional extra", body)
        self.assertIn("dependencies = []", body)

    def test_the_gui_cannot_become_a_second_engine(self):
        body = flat(GUI)
        self.assertIn("never rolls dice", body)
        self.assertIn("parity test", body)
        self.assertIn("src/gui/", body)

    def test_the_palette_is_borrowed_not_invented(self):
        body = flat(GUI)
        for colour in ("#201d31", "#f9e9bd", "#9dd9bc", "#f6a55b", "#b29be7"):
            self.assertIn(colour, body)
        self.assertIn("ISSUE_447_RETRO_UI_PROTOTYPE.html", text(GUI))

    def test_graph_semantics_never_depend_on_colour_alone(self):
        body = flat(GUI)
        self.assertIn("never colour alone", body)
        self.assertIn("dashed", body)

    def test_there_are_milestones_and_a_deferred_list(self):
        body = flat(GUI)
        for milestone in ("M0", "M1", "M2", "M3", "M4", "M5"):
            self.assertIn(milestone, body)
        self.assertIn("Explicitly deferred", body)


class RegisterAndLinks(unittest.TestCase):
    def test_both_documents_are_registered(self):
        body = text(REGISTER)
        self.assertIn("GAMEPLAY_INTERFACES_1184.md", body)
        self.assertIn("GUI_PYTHON_GRAPH_1184.md", body)

    def test_relative_links_resolve(self):
        broken = []
        for path in (ARCH, GUI):
            for target in re.findall(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", text(path)):
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.name} -> {target}")
        self.assertEqual(broken, [], "broken links: " + "; ".join(broken))


if __name__ == "__main__":
    unittest.main()
