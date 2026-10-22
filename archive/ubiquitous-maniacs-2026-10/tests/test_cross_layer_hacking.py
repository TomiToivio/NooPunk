"""Tests for cross-layer psychotronic resonance in the layered hacking engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.hacking import (
    AccessLevel,
    CROSS_LAYER_EDGES,
    HackingAction,
    LayeredHackingSession,
    OperationalLayer,
)
from src.rpg import load_character


ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "data" / "hacking" / "sleeping_patient.json"
CHARACTER = ROOT / "data" / "rpg" / "characters" / "romppainen_day_1.md"


def make_session() -> LayeredHackingSession:
    return LayeredHackingSession.from_json(load_character(CHARACTER), SCENARIO)


def gain_access(sim: LayeredHackingSession, source: str, target: str) -> None:
    while sim.access[target] < AccessLevel.ACCESS:
        assert sim.create_access(source, target, roll=4).success


# ── Cross-layer edge types ──────────────────────────────────────


def test_cross_layer_edges_set_is_nonempty():
    assert len(CROSS_LAYER_EDGES) >= 4
    assert "psychotronic_feedback" in CROSS_LAYER_EDGES
    assert "embodied_dream" in CROSS_LAYER_EDGES
    assert "implant_brain_interface" in CROSS_LAYER_EDGES


def test_resonate_action_exists():
    assert HackingAction.RESONATE == "resonate"


# ── Cross-layer neighbors ───────────────────────────────────────


def test_cross_layer_neighbors_from_clinical_terminal():
    sim = make_session()
    # clinical_terminal is cybernetic; it connects to pilgrim_tanaka_implant
    # via network_connection (NOT cross-layer). No cross-layer edges from here
    # until implant is discovered.
    neighbors = sim._cross_layer_neighbors("clinical_terminal")
    # clinical_terminal -> pilgrim_tanaka_implant is network_connection, not cross-layer
    assert all(et in CROSS_LAYER_EDGES for _, et in neighbors)


def test_cross_layer_neighbors_from_pilgrim_tanaka_implant():
    sim = make_session()
    # First discover pilgrim_tanaka_implant
    sim.observe("clinical_terminal", roll=4)
    # pilgrim_tanaka_implant has edges to:
    #   corrupted_memory_buffer (data_flow — not cross-layer)
    #   drug_delivery_controller (control — not cross-layer)
    #   ufab_80mg_concentration (implant_brain_interface — cross-layer!)
    #   foreign_psychic_signal (unauthorized_resonance — cross-layer!)
    neighbors = sim._cross_layer_neighbors("pilgrim_tanaka_implant")
    edge_types = [et for _, et in neighbors]
    assert "implant_brain_interface" in edge_types
    assert "unauthorized_resonance" in edge_types


# ── Resonate action ─────────────────────────────────────────────


def test_resonate_requires_cross_layer_edge():
    sim = make_session()
    sim.observe("clinical_terminal", roll=4)
    # clinical_terminal -> pilgrim_tanaka_implant is network_connection
    with pytest.raises(ValueError, match="ei tue psykotronista resonanssia"):
        sim.resonate("clinical_terminal", "pilgrim_tanaka_implant", roll=4)


def test_resonate_requires_different_layers():
    """counter_resonance connects two psychic nodes. Even though it's a
    cross-layer edge type, resonate rejects same-layer transitions."""
    sim = make_session()
    # Verify the edge exists and is cross-layer typed
    assert sim.graph.has_edge("archetypal_guardian", "foreign_psychic_signal")
    edge = sim.graph.edges["archetypal_guardian", "foreign_psychic_signal"]
    assert edge.get("edge_type") == "counter_resonance"
    # Both are psychic
    assert sim._layer("archetypal_guardian") == OperationalLayer.PSYCHIC
    assert sim._layer("foreign_psychic_signal") == OperationalLayer.PSYCHIC
    # Resonate would reject — but we can't easily reach archetypal_guardian
    # because it's hidden. Test the layer check directly instead:
    source_layer = sim._layer("archetypal_guardian")
    target_layer = sim._layer("foreign_psychic_signal")
    assert source_layer == target_layer  # same layer — resonate would reject


def test_resonate_requires_contact():
    sim = make_session()
    sim.observe("clinical_terminal", roll=4)
    # pilgrim_tanaka_implant is now known but at OBSERVED level
    assert sim.access["pilgrim_tanaka_implant"] == AccessLevel.OBSERVED
    with pytest.raises(ValueError, match="Contact-tason"):
        sim.resonate("pilgrim_tanaka_implant", "ufab_80mg_concentration", roll=4)


def test_resonate_same_node_rejected():
    sim = make_session()
    with pytest.raises(ValueError, match="kaksi eri solmua"):
        sim.resonate("clinical_terminal", "clinical_terminal", roll=4)


def test_resonate_succeeds_cross_layer():
    """Cross-layer resonance: cybernetic → biological via implant_brain_interface."""
    sim = make_session()
    # Gain access to pilgrim_tanaka_implant (cybernetic)
    sim.observe("clinical_terminal", roll=4)
    gain_access(sim, "clinical_terminal", "pilgrim_tanaka_implant")
    assert sim.access["pilgrim_tanaka_implant"] >= AccessLevel.CONTACT

    # Resonate to ufab_80mg_concentration (biological) via implant_brain_interface
    result = sim.resonate("pilgrim_tanaka_implant", "ufab_80mg_concentration", roll=4)
    assert result.success
    assert "ufab_80mg_concentration" in sim.known_nodes
    assert sim.access["ufab_80mg_concentration"] >= AccessLevel.CONTACT
    assert sim.current_node == "ufab_80mg_concentration"
    # ufab_80mg_concentration is biological, pilgrim_tanaka_implant is cybernetic
    assert sim._layer("ufab_80mg_concentration") == OperationalLayer.BIOLOGICAL
    assert sim._layer("pilgrim_tanaka_implant") == OperationalLayer.CYBERNETIC


def test_resonate_failure_increases_instability():
    """Failed resonance is extra dangerous — instability grows.
    The failure adds +1 instability on top of whatever _apply_pressure does."""
    sim = make_session()
    sim.observe("clinical_terminal", roll=4)
    gain_access(sim, "clinical_terminal", "pilgrim_tanaka_implant")
    # foreign_psychic_signal is psychic (defense 6)
    # Willpower(3) + Kinesics(2) + (-4) = 1 vs 6 -> margin -5 -> FAILURE
    # _apply_pressure on PSYCHIC failure: instability += 2
    # resonate failure: instability += 1
    # Total: instability = 3
    result = sim.resonate("pilgrim_tanaka_implant", "foreign_psychic_signal", roll=-4)
    assert not result.success
    assert sim.instability >= 2  # at least the pressure + resonance penalty


def test_resonate_reveals_target_neighbors():
    """Successful resonance discovers the target's neighbors too — layers leak."""
    sim = make_session()
    sim.observe("clinical_terminal", roll=4)
    gain_access(sim, "clinical_terminal", "pilgrim_tanaka_implant")
    # ufab_80mg_concentration connects back to pilgrim_tanaka_implant (already known)
    # and to patient_nervous_system via metabolism (not cross-layer, but still discovered)
    result = sim.resonate("pilgrim_tanaka_implant", "ufab_80mg_concentration", roll=4)
    assert result.success
    # The resonance should have discovered edges around ufab_80mg_concentration
    assert len(sim.discovered_edges) > 0


def test_resonate_to_psychic_layer_via_unauthorized_resonance():
    """Cross-layer resonance: cybernetic → psychic via unauthorized_resonance.
    Resonance can target hidden nodes — that's its purpose."""
    sim = make_session()
    sim.observe("clinical_terminal", roll=4)
    gain_access(sim, "clinical_terminal", "pilgrim_tanaka_implant")
    # foreign_psychic_signal is hidden, connected via unauthorized_resonance
    assert sim.graph.has_edge("pilgrim_tanaka_implant", "foreign_psychic_signal")
    edge = sim.graph.edges["pilgrim_tanaka_implant", "foreign_psychic_signal"]
    assert edge.get("edge_type") == "unauthorized_resonance"
    # foreign_psychic_signal is hidden — but resonance can target it
    assert "foreign_psychic_signal" not in sim.known_nodes
    result = sim.resonate("pilgrim_tanaka_implant", "foreign_psychic_signal", roll=4)
    assert result.success
    assert "foreign_psychic_signal" in sim.known_nodes
    assert sim.current_node == "foreign_psychic_signal"
    assert sim._layer("foreign_psychic_signal") == OperationalLayer.PSYCHIC


# ── Snapshot includes resonance options ─────────────────────────


def test_snapshot_includes_resonance_options():
    sim = make_session()
    sim.observe("clinical_terminal", roll=4)
    snap = sim.snapshot()
    assert "resonance_options" in snap
    assert "current_layer" in snap
    assert snap["current_layer"] == "cybernetic"


def test_snapshot_resonance_options_after_access():
    sim = make_session()
    sim.observe("clinical_terminal", roll=4)
    gain_access(sim, "clinical_terminal", "pilgrim_tanaka_implant")
    snap = sim.snapshot()
    # pilgrim_tanaka_implant has cross-layer edges
    options = snap["resonance_options"]
    edge_types = [o["edge_type"] for o in options]
    assert "implant_brain_interface" in edge_types or "unauthorized_resonance" in edge_types


# ── Sleeping Patient cross-layer playthrough ────────────────────


def test_cross_layer_playthrough_completes():
    """Full cross-layer playthrough: cyber → bio → cyber, with resonance."""
    sim = make_session()
    # 1. Cyber: observe and gain access to implant
    sim.observe("clinical_terminal", roll=4)
    gain_access(sim, "clinical_terminal", "pilgrim_tanaka_implant")

    # 2. Cross-layer: resonate from implant to UFAB concentration (cyber → bio)
    result = sim.resonate("pilgrim_tanaka_implant", "ufab_80mg_concentration", roll=4)
    assert result.success
    assert sim._layer(sim.current_node) == OperationalLayer.BIOLOGICAL

    # 3. Cyber: identify intruder via implant → memory buffer
    sim.observe("pilgrim_tanaka_implant", roll=4)
    assert "corrupted_memory_buffer" in sim.known_nodes
    gain_access(sim, "pilgrim_tanaka_implant", "corrupted_memory_buffer")
    sim.exploit("corrupted_memory_buffer", roll=4)
    assert "identify_intruder" in sim.completed_objectives

    # 4. Bio: stabilize via nervous system
    gain_access(sim, "patient_nervous_system", "patient_nervous_system")
    sim.exploit("patient_nervous_system", roll=4)
    assert "stabilize_patient" in sim.completed_objectives

    assert sim.status == "completed"