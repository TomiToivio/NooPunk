"""#1156: two non-canon documents, and the guard that keeps them non-canon.

The failure mode here is not a broken script — it is a proposal quietly becoming setting because
nobody noticed the banner was missing, or a research note being cited as evidence that the setting
is true. These tests pin the separation, not the prose.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research" / "UFO_DISCLOSURE_BACKGROUND_RESEARCH.md"
PROPOSAL = ROOT / "docs" / "proposals" / "UFO_DISCLOSURE_NHI_CRISIS_SCENARIO_DRAFT.md"
REGISTER = ROOT / "docs" / "DOCUMENT_REGISTER.md"
CANON_CRISIS = ROOT / "docs" / "world" / "NHI_CRISIS_921.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(path: Path) -> str:
    raw = re.sub(r"(?m)^\s*>\s?", "", text(path))
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", raw))


def test_the_two_deliverables_exist_and_are_separate() -> None:
    assert RESEARCH.is_file() and PROPOSAL.is_file()
    assert RESEARCH.parent.name == "research"
    assert PROPOSAL.parent.name == "proposals"


def test_the_proposal_wears_its_banner_and_the_research_its_label() -> None:
    proposal = flat(PROPOSAL).upper()
    assert "PROPOSAL / NOT CANON" in proposal
    assert "NOTHING IN THIS FILE IS APPROVED SETTING MATERIAL" in proposal
    research = flat(RESEARCH)
    assert "NOT canon and not approved" in research
    assert "REAL-DOCUMENTED" in research and "IN-WORLD CANON" in research


def test_the_research_dossier_carries_the_quote_matrix_and_its_provenance() -> None:
    body = flat(RESEARCH)
    assert "fetched 2026-11-05" in body
    for ref in ("6.25", "7.12", "8.2", "8.6", "8.9", "12.9", "38.7", "51.2", "52.10",
                "53.17", "70.19", "84.8"):
        assert f"[{ref}]" in text(RESEARCH), f"Law of One passage missing from matrix: {ref}"


def test_the_four_claimants_stay_attributed_and_unproven() -> None:
    body = flat(RESEARCH)
    for name in ("David Grusch", "Jake Barber", "Eric Davis", "Luis Elizondo"):
        assert name in body, f"claimant missing: {name}"
    assert "REAL-CLAIM" in body
    assert "Do not fabricate quotes" in body


def test_at_least_eight_hypotheses_are_compared() -> None:
    body = flat(RESEARCH)
    for hypothesis in ("Extraterrestrial", "Interdimensional", "Extratemporal",
                       "Cryptoterrestrial", "Plasma / space-animal",
                       "Thanatological", "Psychosocial", "Demonic", "Secret human technology"):
        assert hypothesis in body, f"hypothesis missing: {hypothesis}"


def test_the_finnish_documentary_layer_is_cited_not_invented() -> None:
    body = flat(RESEARCH)
    assert "R-5-8-47" in body
    assert "10 February 1947" in body
    assert "M. Niamala" in body
    assert "1946" in body
    # The 1946 recovery is fiction and must say so.
    assert "invented" in body.lower()


def test_the_proposal_covers_helsinki_and_missions_beyond_it() -> None:
    body = flat(PROPOSAL)
    assert "Helsinki 2045" in body
    assert "Tähtitorninmäki" in body and "Vuosaari" in body and "Santahamina" in body
    assert "Onkalo" in body and "Porkkala" in body and "Virolahti" in body
    assert body.count("| H") >= 10  # metropolitan mission sites
    assert body.count("| F") >= 12  # rest-of-Finland sites


def test_the_proposal_declares_a_change_impact_map_and_no_mechanics() -> None:
    body = flat(PROPOSAL)
    assert "Change-impact map" in body
    assert "No mechanical change" in body or "Not touched under any outcome" in body
    assert "no new mechanics" in body.lower() or "No new mechanics" in body


def test_the_proposal_keeps_the_open_mysteries_open() -> None:
    body = flat(PROPOSAL)
    assert "MJ-12" in body and "ПРОГРАММА" in body
    assert "stay open" in body
    assert "Mandela Effect is a witness, not a puzzle" in body


def test_canonical_crisis_history_was_not_edited_by_this_issue() -> None:
    body = text(CANON_CRISIS)
    assert "PROPOSAL" not in body
    assert "Helsinki 2045" not in body


def test_the_register_marks_both_documents_non_canon() -> None:
    body = text(REGISTER)
    row = [line for line in body.splitlines() if "UFO_DISCLOSURE_BACKGROUND_RESEARCH.md" in line]
    assert row, "register row missing"
    assert "non-canon" in row[0]
    assert "proposals/UFO_DISCLOSURE_NHI_CRISIS_SCENARIO_DRAFT.md" in row[0]
