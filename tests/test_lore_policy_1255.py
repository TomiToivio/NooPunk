"""Lore must not outrun the rules (#1255).

`docs/research/HIA_DOSSIER_1255.md`, `docs/world/IMMORTALITY_AND_NOETICS_1255.md` and
`docs/campaign/GATEWAY_1255.md` make claims about the game: that only Telepathy and Telekinesis are
selectable for PCs, that astral access is scripted, and that there is no Astral graph. Those claims are
true only while the code says so, and a lore page is exactly where a discipline creeps back in.

These tests are the seam: change the policy and the documentation has to be changed deliberately.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

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


def test_the_three_1255_pages_are_present() -> None:
    for parts in (
        ("research", "HIA_DOSSIER_1255.md"),
        ("world", "IMMORTALITY_AND_NOETICS_1255.md"),
        ("campaign", "GATEWAY_1255.md"),
    ):
        assert DOCS.joinpath(*parts).is_file(), parts


class TestAstralIsStillNotPlayable:
    def test_the_graph_model_has_exactly_four_families(self) -> None:
        families = {name for name in WorldGraphs.__dataclass_fields__ if name != "format"}
        assert families == {"physical", "cyber", "social", "story"}
        assert not hasattr(WorldGraphs, "astral")

    def test_an_astral_scene_type_is_refused_for_the_stated_reason(self) -> None:
        assert POSTPONED_SCENE_TYPES == ("Astral",)
        with pytest.raises(PostponedScene) as caught:
            SceneFrame("scene.projection", "Projection", "Astral")
        assert "postponed by author decision" in str(caught.value)

    def test_the_gateway_page_admits_it_is_unbuilt_and_names_this_test(self) -> None:
        text = page("campaign", "GATEWAY_1255.md")
        assert "**not built.**" in text
        assert "test_lore_policy_1255.py" in text


class TestPcDisciplinesAreStillTwo:
    def test_only_telepathy_and_telekinesis_are_selectable(self) -> None:
        assert set(psi_access.PC_DISCIPLINES) == {"Telekinesis", "Telepathy"}

    def test_projection_is_scripted_only_and_never_a_pc_option(self) -> None:
        assert "Astral Projection" in psi_access.SCRIPTED_ONLY
        assert "Astral Projection" not in psi_access.PC_DISCIPLINES
        assert "Astral Projection" not in psi_access.NPC_ONLY_DISCIPLINES

    def test_the_lore_states_the_same_two_disciplines(self) -> None:
        for parts in (
            ("world", "IMMORTALITY_AND_NOETICS_1255.md"),
            ("campaign", "GATEWAY_1255.md"),
        ):
            text = page(*parts)
            assert "Telepathy" in text
            assert "Telekinesis" in text


class TestTheDossierKeepsItsLabels:
    def test_every_claim_can_be_told_apart(self) -> None:
        text = page("research", "HIA_DOSSIER_1255.md")
        for label in ("(A) REAL", "(B) THEORY", "(C) NOÖPUNK"):
            assert label in text

    def test_the_contested_paper_is_not_sold_as_settled_science(self) -> None:
        text = page("research", "HIA_DOSSIER_1255.md")
        assert "pro-Orch OR" in text            # the issue's own citation, labelled for what it is
        assert "contested" in text               # and the countervailing review beside it
        assert "PMC13168204" in text

    def test_no_upload_is_claimed_as_established(self) -> None:
        text = page("research", "HIA_DOSSIER_1255.md").replace("**", "")
        assert "no demonstrated upload" in text.lower()
