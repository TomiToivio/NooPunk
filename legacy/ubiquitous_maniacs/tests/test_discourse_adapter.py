"""Tests for the discourse-graph adapter: social graph → Castells/Laclau models."""

from __future__ import annotations

from src.game.social_graph import MultiDimensionalSocialGraph
from src.political.discourse_adapter import social_to_combined, CHARACTER_ROLE_MAP


def make_graph() -> MultiDimensionalSocialGraph:
    g = MultiDimensionalSocialGraph(seed=42)
    g.add_character("romppainen", "Emil Romppainen", "patient", ["survive"], "disoriented")
    g.add_character("ingrid_falk", "Ingrid Falk", "patient", ["heal"], "grieving")
    g.add_character("elin_dahl", "Dr. Elin Dahl", "staff", ["filter"], "professional")
    g.add_character("yuki_tanaka", "Dr. Yuki Tanaka", "staff", ["protect"], "watchful")
    g.add_character("soren_pilgrim", "Dr. Søren Pilgrim", "staff", ["experiment"], "intense")
    g.add_character("ufab_ragnarok", "UFAB Ragnarök", "ai", ["facilitate"], "omniscient")
    return g


# ── Basic structure tests ──────────────────────────────────────


def test_adapter_returns_combined_extraction():
    g = make_graph()
    result = social_to_combined(g)
    assert result is not None
    assert hasattr(result, "social")
    assert hasattr(result, "castells")
    assert hasattr(result, "laclau")


def test_all_characters_become_nodes():
    g = make_graph()
    result = social_to_combined(g)
    assert len(result.castells.nodes) == 6
    assert len(result.laclau.nodes) == 6
    ids = {n.id for n in result.castells.nodes}
    assert "romppainen" in ids
    assert "ufab_ragnarok" in ids
    assert "ingrid_falk" in ids


def test_ragnarok_is_programming_power():
    g = make_graph()
    result = social_to_combined(g)
    ragnarok = [n for n in result.castells.nodes if n.id == "ufab_ragnarok"][0]
    assert ragnarok.label == "ProgrammingPower"


def test_pilgrim_is_switching_power():
    g = make_graph()
    result = social_to_combined(g)
    pilgrim = [n for n in result.castells.nodes if n.id == "soren_pilgrim"][0]
    assert pilgrim.label == "SwitchingPower"


def test_tanaka_is_counterpower():
    g = make_graph()
    result = social_to_combined(g)
    tanaka = [n for n in result.castells.nodes if n.id == "yuki_tanaka"][0]
    assert tanaka.label == "Counterpower"


def test_dahl_is_hub():
    g = make_graph()
    result = social_to_combined(g)
    dahl = [n for n in result.castells.nodes if n.id == "elin_dahl"][0]
    assert dahl.label == "Hub"


def test_patients_are_nodes():
    g = make_graph()
    result = social_to_combined(g)
    romppainen = [n for n in result.castells.nodes if n.id == "romppainen"][0]
    ingrid = [n for n in result.castells.nodes if n.id == "ingrid_falk"][0]
    assert romppainen.label == "Node"
    assert ingrid.label == "Node"


# ── Edge mapping tests ─────────────────────────────────────────


def test_authority_creates_programs_edge():
    g = make_graph()
    g.set_relationship("ufab_ragnarok", "romppainen", {"authority": 3})
    result = social_to_combined(g)
    programs_edges = [e for e in result.castells.edges if e.relation == "programs"]
    assert len(programs_edges) >= 1
    assert programs_edges[0].source == "ufab_ragnarok"
    assert programs_edges[0].target == "romppainen"


def test_negative_trust_creates_opposes_edge():
    g = make_graph()
    g.set_relationship("romppainen", "soren_pilgrim", {"trust": -3})
    result = social_to_combined(g)
    opposes = [e for e in result.castells.edges if e.relation == "opposes"]
    assert len(opposes) >= 1


def test_suspicion_creates_excludes_edge():
    g = make_graph()
    g.set_relationship("ufab_ragnarok", "romppainen", {"suspicion": 3})
    result = social_to_combined(g)
    excludes = [e for e in result.castells.edges if e.relation == "excludes"]
    assert len(excludes) >= 1


def test_positive_trust_creates_connects_edge():
    g = make_graph()
    g.set_relationship("yuki_tanaka", "elin_dahl", {"trust": 3})
    result = social_to_combined(g)
    connects = [e for e in result.castells.edges if e.relation == "connects"]
    assert len(connects) >= 1


# ── Laclau layer tests ─────────────────────────────────────────


def test_ragnarok_is_nodal_point():
    g = make_graph()
    result = social_to_combined(g)
    ragnarok = [n for n in result.laclau.nodes if n.id == "ufab_ragnarok"][0]
    assert ragnarok.label == "NodalPoint"
    assert ragnarok.is_empty_signifier is True


def test_authority_creates_hegemonizes_edge():
    g = make_graph()
    g.set_relationship("ufab_ragnarok", "romppainen", {"authority": 3})
    result = social_to_combined(g)
    hegemonizes = [e for e in result.laclau.edges if e.relation == "HEGEMONIZES"]
    assert len(hegemonizes) >= 1
    assert hegemonizes[0].logic == "hegemony"


def test_negative_trust_creates_enemy_edge():
    g = make_graph()
    g.set_relationship("romppainen", "soren_pilgrim", {"trust": -3})
    result = social_to_combined(g)
    enemies = [e for e in result.laclau.edges if e.relation == "CONSTRUCTS_AS_ENEMY"]
    assert len(enemies) >= 1
    assert enemies[0].logic == "antagonism"


def test_suspicion_creates_contested_edge():
    g = make_graph()
    g.set_relationship("ufab_ragnarok", "romppainen", {"suspicion": 3})
    result = social_to_combined(g)
    contested = [e for e in result.laclau.edges if e.relation == "CONTESTED_BY"]
    assert len(contested) >= 1
    assert contested[0].logic == "contestation"


def test_positive_trust_creates_articulated_edge():
    g = make_graph()
    g.set_relationship("yuki_tanaka", "elin_dahl", {"trust": 3})
    result = social_to_combined(g)
    articulated = [e for e in result.laclau.edges if e.relation == "ARTICULATED_WITH"]
    assert len(articulated) >= 1
    assert articulated[0].logic == "equivalence"


# ── Social layer tests ─────────────────────────────────────────


def test_social_nodes_created():
    g = make_graph()
    result = social_to_combined(g)
    assert len(result.social.nodes) == 6


def test_social_positive_trust_edge():
    g = make_graph()
    g.set_relationship("yuki_tanaka", "elin_dahl", {"trust": 3})
    result = social_to_combined(g)
    positive = [e for e in result.social.edges
                if e.relation == "has_positive_sentiment_towards"]
    assert len(positive) >= 1


def test_social_negative_trust_edge():
    g = make_graph()
    g.set_relationship("romppainen", "soren_pilgrim", {"trust": -3})
    result = social_to_combined(g)
    negative = [e for e in result.social.edges
                if e.relation == "has_negative_sentiment_towards"]
    assert len(negative) >= 1


# ── Hidden edge tests ──────────────────────────────────────────


def test_hidden_edges_respect_observer():
    g = make_graph()
    g.set_relationship("ufab_ragnarok", "romppainen", {"suspicion": 3}, hidden=True)
    result = social_to_combined(g, observer="romppainen")
    # Hidden edge should NOT appear
    edges_to_rompp = [e for e in result.castells.edges if e.target == "romppainen"]
    assert all(e.source != "ufab_ragnarok" for e in edges_to_rompp)


def test_no_edges_when_all_zero():
    g = make_graph()
    # No relationships set — all dims are 0
    result = social_to_combined(g)
    assert len(result.castells.edges) == 0
    assert len(result.laclau.edges) == 0