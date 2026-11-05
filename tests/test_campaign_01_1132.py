"""Guards for the first campaign outline (#1132).

Design documents rot differently from code: links break silently, drafts get quoted as canon, and a second
outline appears next to the first one. These tests are cheap and they fail loudly.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md"
INDEX = ROOT / "docs/campaign/README.md"


def test_the_outline_exists_and_is_marked_draft():
    text = DOC.read_text(encoding="utf-8")
    assert "**Status: DRAFT" in text[:600], "the outline must announce that it is a draft"


def test_act_three_is_still_a_proposal():
    """The author has not decided Act III. If this test fails, someone decided it in code."""
    text = DOC.read_text(encoding="utf-8")
    act3 = text.split("### ACT III")[1].split("### ACT IV")[0]
    assert "PROPOSAL, PENDING AUTHOR DECISION" in act3.upper() or "PROPOSAL" in act3, (
        "Act III must stay labelled as a proposal until the author rules on it")


def test_the_fixed_points_are_stated_as_fixed():
    text = DOC.read_text(encoding="utf-8")
    lowered = text.lower()
    assert "service-to-others" in lowered and "fixed" in lowered
    assert "no sts route" in lowered or "no joinable sts" in lowered, (
        "the campaign must state that there is no StS route")


def test_cwn_stays_the_immutable_core():
    text = DOC.read_text(encoding="utf-8")
    assert "CWN is the immutable core".lower() in text.lower()


def test_every_relative_link_in_the_outline_resolves():
    text = DOC.read_text(encoding="utf-8")
    links = re.findall(r"\]\((\.{0,2}/?[^)#]+\.md)\)", text)
    assert links, "the outline should link to the repository it depends on"
    broken = [l for l in links if not (DOC.parent / l).resolve().exists()]
    assert not broken, f"broken links: {broken}"


def test_there_is_exactly_one_campaign_outline():
    """One *outline*. Companion worksheets (the dream writing sheet, #1152) are not competing outlines."""
    companions = {"README.md", "DREAMS.md"}
    outlines = [p for p in (ROOT / "docs/campaign").glob("*.md") if p.name not in companions]
    assert len(outlines) == 1, f"more than one campaign outline: {[p.name for p in outlines]}"
    assert outlines[0].name == "CAMPAIGN_01_EUROPOL_ROOKIE.md"
    assert "CAMPAIGN_01_EUROPOL_ROOKIE.md" in INDEX.read_text(encoding="utf-8")


def test_the_outline_is_discoverable_from_the_root_readme():
    assert "CAMPAIGN_01_EUROPOL_ROOKIE.md" in (ROOT / "README.md").read_text(encoding="utf-8")


def test_the_law_of_one_game_is_not_merged_into_the_campaign():
    """#1124 requires the standalone game to stay separate; a campaign reference is not a merge."""
    text = DOC.read_text(encoding="utf-8")
    assert "separate game" in text.lower()
    assert not (ROOT / "law_of_one").exists(), "the standalone game must not be moved into the rules namespace"
