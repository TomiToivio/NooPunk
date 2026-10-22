"""Tests for the Helsinki campaign frame (LaclauGPT → Noöpunk integration, Track 4).

Verifies that the ported Helsinki 2026 campaign data is structurally valid under
B's loaders: characters load via ``load_character``, the four phase scenarios
load via ``scenario_from_dict`` (which validates typed events and the tarot
resolver), and the NHI factions carry the ``contested`` canon flag. No live
Ollama, no network, no heavy models.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.rpg import load_character, load_factions, load_scenario

ROOT = Path(__file__).resolve().parents[1]
HELSINKI = ROOT / "data/rpg/campaigns/helsinki"
CHARACTERS = sorted((HELSINKI / "characters").glob("*.md"))
SCENARIOS = sorted((HELSINKI / "scenarios").glob("*.json"))
NHI_FACTIONS = ROOT / "data/rpg/factions/nhi_factions.json"


# ── Sanity: the campaign data files exist ─────────────────────────────────


def test_campaign_files_exist() -> None:
    assert CHARACTERS, "expected Helsinki character markdown files"
    assert SCENARIOS, "expected Helsinki scenario json files"
    assert NHI_FACTIONS.exists()


# ── Characters ────────────────────────────────────────────────────────────


EXPECTED_CHARACTERS = {
    "katri_virtanen", "reijo_koskinen", "reikka_lindqvist",
    "mikko_halonen", "markus_hakkinen", "the_assembly",
}


def test_all_helsinki_characters_load() -> None:
    loaded = {load_character(path).id for path in CHARACTERS}
    assert loaded == EXPECTED_CHARACTERS


def test_reikka_is_psi_sensitive_first() -> None:
    reikka = load_character(HELSINKI / "characters/reikka_lindqvist.md")
    assert "psi_sensitive" in reikka.tags
    assert reikka.psyche.get("psi_rating") == 1


def test_the_assembly_is_contested_non_personified() -> None:
    assembly = load_character(HELSINKI / "characters/the_assembly.md")
    assert "contested_source" in assembly.tags
    assert "non_personified" in assembly.tags
    assert assembly.psyche.get("canon") == "contested"


# ── Scenarios ─────────────────────────────────────────────────────────────


EXPECTED_SCENARIOS = {
    "phase1_mundane", "phase2_anomalous",
    "phase3_membrane", "phase4_noosphere",
}


def test_all_helsinki_scenarios_load() -> None:
    loaded = {load_scenario(path).id for path in SCENARIOS}
    assert loaded == EXPECTED_SCENARIOS


def test_each_scenario_has_entry_and_terminals() -> None:
    for path in SCENARIOS:
        scenario = load_scenario(path)
        assert scenario.entry_scene in scenario.scenes
        assert scenario.terminal_scenes, f"{scenario.id} has no terminal scenes"
        unknown = scenario.terminal_scenes - set(scenario.scenes)
        assert not unknown, f"{scenario.id} has unknown terminals: {unknown}"


def test_scenarios_declare_addressable_locations() -> None:
    """At least some scenarios declare locations (Track 4 Location entity use)."""
    declared = [load_scenario(p) for p in SCENARIOS]
    with_locations = [s for s in declared if s.locations]
    assert with_locations, "no scenario declares locations"


def test_phase3_and_phase4_use_tarot_resolver() -> None:
    """The mechanical Tarot transition (Track 1) is exercised in phases 3 & 4."""
    tarot_scenarios = {"phase3_membrane", "phase4_noosphere"}
    for path in SCENARIOS:
        scenario = load_scenario(path)
        if scenario.id not in tarot_scenarios:
            continue
        tarot_interactions = [
            interaction
            for scene in scenario.scenes.values()
            for interaction in scene.interactions.values()
            if interaction.resolver == "tarot"
        ]
        assert tarot_interactions, f"{scenario.id} should have at least one tarot interaction"


def test_phase1_and_phase2_use_default_resolver() -> None:
    """Phases 1 & 2 stay on the default 4dF resolver (the rules change in phase 3)."""
    default_scenarios = {"phase1_mundane", "phase2_anomalous"}
    for path in SCENARIOS:
        scenario = load_scenario(path)
        if scenario.id not in default_scenarios:
            continue
        resolvers = {
            interaction.resolver
            for scene in scenario.scenes.values()
            for interaction in scene.interactions.values()
        }
        assert resolvers == {"4df"}, f"{scenario.id} should use only the default resolver, got {resolvers}"


def test_scenarios_use_typed_events() -> None:
    """Scenario events use the typed payloads validated by scenario_from_dict."""
    event_types: set[str] = set()
    for path in SCENARIOS:
        scenario = load_scenario(path)
        for scene in scenario.scenes.values():
            for interaction in scene.interactions.values():
                outcomes = list(interaction.outcomes.values())
                if interaction.automatic_outcome is not None:
                    outcomes.append(interaction.automatic_outcome)
                for outcome in outcomes:
                    for event in outcome.events:
                        event_types.add(event["type"])
    assert "npc_memory" in event_types
    assert "relationship_change_requested" in event_types


# ── NHI factions (contested canon) ────────────────────────────────────────


def test_nhi_factions_load_with_contested_canon() -> None:
    factions = load_factions(NHI_FACTIONS)
    assert {f.id for f in factions} == {"the_watchers", "the_architects"}
    for faction in factions:
        assert faction.canon == "contested", f"{faction.id} should be contested canon"
        assert "contested" in faction.description.lower()


def test_nhi_factions_have_goals_and_projects() -> None:
    factions = load_factions(NHI_FACTIONS)
    for faction in factions:
        assert faction.goals, f"{faction.id} should have goals"
        assert faction.projects, f"{faction.id} should have projects"
        assert faction.relationships, f"{faction.id} should have relationships"


def test_watchers_and_architects_disagree() -> None:
    """The two NHI factions are in fundamental disagreement (relationship < 0)."""
    factions = {f.id: f for f in load_factions(NHI_FACTIONS)}
    assert factions["the_watchers"].relationships.get("the_architects", 0) < 0
    assert factions["the_architects"].relationships.get("the_watchers", 0) < 0