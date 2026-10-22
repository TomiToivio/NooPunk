import copy
import json
from pathlib import Path

import pytest

from src.hacking import AccessLevel, LayeredHackingSession, OperationalLayer
from src.rpg import RPGState, load_character


ROOT = Path(__file__).parents[1]
SCENARIO = ROOT / "data" / "hacking" / "sleeping_patient.json"
CHARACTER = ROOT / "data" / "rpg" / "characters" / "romppainen_day_1.md"


def session() -> LayeredHackingSession:
    return LayeredHackingSession.from_json(load_character(CHARACTER), SCENARIO)


def scenario_data() -> dict:
    return json.loads(SCENARIO.read_text(encoding="utf-8"))


def gain_access(sim: LayeredHackingSession, source: str, target: str) -> None:
    while sim.access[target] < AccessLevel.ACCESS:
        assert sim.create_access(source, target, roll=4).success


def technical_identification(sim: LayeredHackingSession) -> None:
    reveal = sim.observe("clinical_terminal", roll=4)
    assert "pilgrim_tanaka_implant" in reveal.revealed_nodes
    gain_access(sim, "clinical_terminal", "pilgrim_tanaka_implant")
    implant = sim.observe("pilgrim_tanaka_implant", roll=4)
    assert "corrupted_memory_buffer" in implant.revealed_nodes
    gain_access(sim, "pilgrim_tanaka_implant", "corrupted_memory_buffer")
    assert sim.exploit("corrupted_memory_buffer", roll=4).success


def biological_stabilization(sim: LayeredHackingSession) -> None:
    gain_access(sim, "patient_nervous_system", "patient_nervous_system")
    assert sim.exploit("patient_nervous_system", roll=4).success


def test_loader_exposes_four_layers_but_keeps_hidden_nodes_secret() -> None:
    sim = session()
    visible_layers = {OperationalLayer(sim.graph.nodes[node]["layer"]) for node in sim.known_nodes}
    assert visible_layers == set(OperationalLayer)
    assert "foreign_psychic_signal" not in sim.known_nodes
    assert sim.access["clinical_terminal"] == AccessLevel.CONTACT


def test_layered_hacking_save_round_trip_preserves_mutable_state() -> None:
    sim = session()
    sim.observe("clinical_terminal", roll=4)
    sim.graph.nodes["clinical_terminal"]["overcome"] = True

    restored = LayeredHackingSession.from_save_dict(sim.actor, sim.to_save_dict())

    assert restored.snapshot() == sim.snapshot()
    assert restored.graph.nodes["clinical_terminal"]["overcome"] is True


def test_loader_rejects_hidden_entry_and_silent_duplicate_records() -> None:
    actor = load_character(CHARACTER)

    hidden_entry = scenario_data()
    hidden_entry["entry_node"] = "foreign_psychic_signal"
    with pytest.raises(ValueError, match="entry node must be visible"):
        LayeredHackingSession.from_dict(actor, hidden_entry)

    duplicate_edge = scenario_data()
    duplicate_edge["edges"].append(copy.deepcopy(duplicate_edge["edges"][0]))
    with pytest.raises(ValueError, match="Duplicate hacking edge"):
        LayeredHackingSession.from_dict(actor, duplicate_edge)

    duplicate_tool = scenario_data()
    duplicate_tool["tools"].append(copy.deepcopy(duplicate_tool["tools"][0]))
    with pytest.raises(ValueError, match="Duplicate hacking tool"):
        LayeredHackingSession.from_dict(actor, duplicate_tool)


def test_observe_discovers_nodes_and_edges() -> None:
    sim = session()
    result = sim.observe("clinical_terminal", roll=4)
    assert result.success
    assert result.revealed_nodes == ("pilgrim_tanaka_implant",)
    assert ("clinical_terminal", "pilgrim_tanaka_implant") in sim.discovered_edges


def test_access_requires_a_real_connection_and_increases_in_steps() -> None:
    sim = session()
    with pytest.raises(ValueError, match="hidden"):
        sim.create_access("clinical_terminal", "corrupted_memory_buffer", roll=4)
    sim.observe("clinical_terminal", roll=4)
    result = sim.create_access("clinical_terminal", "pilgrim_tanaka_implant", roll=4)
    assert result.access_level == AccessLevel.CONTACT
    result = sim.create_access("clinical_terminal", "pilgrim_tanaka_implant", roll=4)
    assert result.access_level == AccessLevel.ACCESS


def test_cross_layer_movement_uses_typed_edge() -> None:
    sim = session()
    sim.observe("tanaka_trust", roll=4)
    assert "patient_consent" in sim.known_nodes
    gain_access(sim, "tanaka_trust", "patient_consent")
    result = sim.create_access("patient_consent", "patient_conscious_self", roll=4)
    assert result.success
    assert sim.graph.edges["patient_consent", "patient_conscious_self"]["edge_type"] == "permission"


def test_success_at_cost_advances_and_adds_detection_pressure() -> None:
    sim = session()
    result = sim.observe("clinical_terminal", roll=-4)
    assert result.success and result.costly_success
    assert result.revealed_nodes
    assert sim.alert == 1 and sim.trace == 1


def test_create_advantage_uses_shared_rpg_action_result() -> None:
    sim = session()
    result = sim.create_advantage("tanaka_trust", "TANAKA VALVOO TOIMENPIDETTÄ", roll=4)
    assert result.success
    assert result.created_aspect in sim.aspects
    assert result.check is not None


def test_tools_and_fate_invokes_modify_shared_check_without_stacking_silently() -> None:
    sim = session()
    sim.actor.resources["fate_points"] = 1
    result = sim.observe(
        "clinical_terminal",
        roll=0,
        tool_id="ufab_diagnostic_deck",
        invoke_aspect="Totuus puskee halkeamista",
    )
    assert result.check.check.situational_modifier == 3
    assert sim.actor.resources["fate_points"] == 0
    with pytest.raises(ValueError, match="does not permit"):
        sim.observe("patient_conscious_self", roll=0, tool_id="ufab_diagnostic_deck")


def test_overcome_uses_layer_specific_rpg_check() -> None:
    sim = session()
    result = sim.overcome(
        "patient_conscious_self",
        roll=4,
        tool_id="tanaka_grounding_protocol",
    )
    assert result.success
    assert sim.graph.nodes["patient_conscious_self"]["overcome"] is True


def test_exploit_requires_access_and_attack_creates_system_stress() -> None:
    sim = session()
    with pytest.raises(ValueError, match="requires Access"):
        sim.exploit("patient_nervous_system", roll=4)
    gain_access(sim, "patient_nervous_system", "patient_nervous_system")
    attack = sim.attack("patient_nervous_system", roll=4)
    assert attack.success
    assert sim.system_stress == attack.check.shifts


def test_costly_attack_still_inflicts_one_system_stress() -> None:
    sim = session()
    gain_access(sim, "patient_nervous_system", "patient_nervous_system")
    attack = sim.attack("patient_nervous_system", roll=-4)
    assert attack.success and attack.costly_success
    assert attack.check is not None and attack.check.shifts == 0
    assert sim.system_stress == 1


def test_hybrid_route_completes_scenario_and_builds_rpg_transfer() -> None:
    sim = session()
    technical_identification(sim)
    assert sim.status == "active"
    biological_stabilization(sim)
    assert sim.status == "completed"
    assert sim.completed_objectives == {"identify_intruder", "stabilize_patient"}
    assert "intruder_has_multiple_provenances" in sim.transfer.information
    assert sim.transfer.flags["sleeping_patient_resolved"] is True


def test_psychic_route_can_identify_intruder() -> None:
    sim = session()
    gain_access(sim, "patient_conscious_self", "patient_conscious_self")
    sim.observe("patient_conscious_self", roll=4)
    gain_access(sim, "patient_conscious_self", "dream_city")
    sim.observe("dream_city", roll=4)
    gain_access(sim, "dream_city", "archetypal_guardian")
    sim.observe("archetypal_guardian", roll=4)
    gain_access(sim, "archetypal_guardian", "foreign_psychic_signal")
    result = sim.exploit("foreign_psychic_signal", roll=4)
    assert result.success
    assert "identify_intruder" in sim.completed_objectives
    assert "foreign_signal_afterimage" in sim.transfer.conditions


def test_failure_reaches_safe_detected_terminal_and_retreat_is_safe() -> None:
    sim = session()
    attempts = 0
    while sim.status == "active" and attempts < 10:
        sim.observe("clinical_terminal", roll=-4)
        attempts += 1
    assert sim.status in {"detected", "feedback_failure"}
    snapshot = sim.snapshot()
    assert snapshot["status"] == sim.status

    escaped = session()
    escaped.trace = 4
    assert escaped.retreat().success
    assert escaped.status == "retreated"
    assert "europol_trace_pending" in escaped.transfer.conditions


def test_results_persist_to_normal_rpg_state() -> None:
    sim = session()
    technical_identification(sim)
    biological_stabilization(sim)
    actor = sim.actor
    state = RPGState(current_scene="after_hack", current_character=actor.id)
    sim.transfer.relationships["yuki_tanaka"] = 3

    sim.transfer.apply(state, actor)

    assert state.campaign_flags["sleeping_patient_resolved"] is True
    assert "intruder_has_multiple_provenances" in state.known_information
    assert state.relationships["yuki_tanaka"] == 3
    assert any(effect.domain == "cyber" for effect in state.graph_effects)


def test_terminal_state_rejects_further_mutation_and_exploit_is_single_use() -> None:
    sim = session()
    technical_identification(sim)
    with pytest.raises(ValueError, match="already been exploited"):
        sim.exploit("corrupted_memory_buffer", roll=4)
    biological_stabilization(sim)
    with pytest.raises(ValueError, match="session has ended"):
        sim.observe("clinical_terminal", roll=4)
