"""Lore must not outrun the rules (#1255).

`docs/research/HIA_DOSSIER_1255.md`, `docs/world/IMMORTALITY_AND_NOETICS_1255.md` and
`docs/campaign/GATEWAY_1255.md` make claims about the game: that only Telepathy and Telekinesis are
selectable for PCs, that astral access is scripted, and that there is no Astral graph. Those claims are
true only while the code says so, and a lore page is exactly where a discipline creeps back in.

These tests are the seam: change the policy and the documentation has to be changed deliberately.

`unittest`, not pytest: the CI job runs `python -m unittest discover` and does not install pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.rules import psi_access
from src.world.graphs import WorldGraphs
from src.world.scenes import (
    POSTPONED_SCENE_TYPES,
    PostponedScene,
    SceneFrame,
)

DOCS = ROOT / "docs"


def page(*parts: str) -> str:
    return DOCS.joinpath(*parts).read_text(encoding="utf-8")


class TestTheDocumentsExist(unittest.TestCase):
    def test_the_three_1255_pages_are_present(self) -> None:
        for parts in (
            ("research", "HIA_DOSSIER_1255.md"),
            ("world", "IMMORTALITY_AND_NOETICS_1255.md"),
            ("campaign", "GATEWAY_1255.md"),
        ):
            self.assertTrue(DOCS.joinpath(*parts).is_file(), parts)


class TestAstralIsStillNotPlayable(unittest.TestCase):
    def test_the_graph_model_has_exactly_four_families(self) -> None:
        families = {name for name in WorldGraphs.__dataclass_fields__ if name != "format"}
        self.assertEqual(families, {"physical", "cyber", "social", "story"})
        self.assertFalse(hasattr(WorldGraphs, "astral"))

    def test_astral_scenes_are_playable_but_not_navigable(self) -> None:
        """#1255 forbids an Astral *graph*; #1261 allows a non-navigable astral *scene*."""
        self.assertEqual(POSTPONED_SCENE_TYPES, ())
        frame = SceneFrame("scene.projection", "Projection", "Astral")
        self.assertEqual(frame.scene_type, "Astral")
        self.assertFalse(hasattr(WorldGraphs, "astral"))

    def test_the_gateway_page_admits_it_is_unbuilt_and_names_this_test(self) -> None:
        text = page("campaign", "GATEWAY_1255.md")
        self.assertIn("**not built.**", text)
        self.assertIn("test_lore_policy_1255.py", text)


class TestPcDisciplinesAreStillTwo(unittest.TestCase):
    def test_only_telepathy_and_telekinesis_are_selectable(self) -> None:
        self.assertEqual(set(psi_access.PC_DISCIPLINES), {"Telekinesis", "Telepathy"})

    def test_projection_is_scripted_only_and_never_a_pc_option(self) -> None:
        self.assertIn("Astral Projection", psi_access.SCRIPTED_ONLY)
        self.assertNotIn("Astral Projection", psi_access.PC_DISCIPLINES)
        self.assertNotIn("Astral Projection", psi_access.NPC_ONLY_DISCIPLINES)

    def test_the_lore_states_the_same_two_disciplines(self) -> None:
        for parts in (
            ("world", "IMMORTALITY_AND_NOETICS_1255.md"),
            ("campaign", "GATEWAY_1255.md"),
        ):
            text = page(*parts)
            self.assertIn("Telepathy", text, parts)
            self.assertIn("Telekinesis", text, parts)


class TestTheDossierKeepsItsLabels(unittest.TestCase):
    def test_every_claim_can_be_told_apart(self) -> None:
        text = page("research", "HIA_DOSSIER_1255.md")
        for label in ("(A) REAL", "(B) THEORY", "(C) NOÖPUNK"):
            self.assertIn(label, text)

    def test_the_contested_paper_is_not_sold_as_settled_science(self) -> None:
        text = page("research", "HIA_DOSSIER_1255.md")
        self.assertIn("pro-Orch OR", text)   # the issue's own citation, labelled for what it is
        self.assertIn("contested", text)     # and the countervailing review beside it
        self.assertIn("PMC13168204", text)

    def test_no_upload_is_claimed_as_established(self) -> None:
        text = page("research", "HIA_DOSSIER_1255.md").replace("**", "")
        self.assertIn("no demonstrated upload", text.lower())


if __name__ == "__main__":
    unittest.main()
