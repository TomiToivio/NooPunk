from pathlib import Path

from src.hacking import HackingSimulation

DATA = Path(__file__).parents[1] / "data" / "hacking" / "demo_target.json"


def test_core_inspect_trace_and_manipulation_loop():
    sim = HackingSimulation.from_json(DATA, seed=4)
    assert sim.inspect_node("identity_sven").data["node_type"] == "identity"
    assert sim.trace_connection("memory_arrival", "ufab_mesh").success
    before = sim.graph.edges["memory_arrival", "identity_sven"]["strength"]
    sim.adjust_edge("memory_arrival", "identity_sven", 10)
    assert sim.graph.edges["memory_arrival", "identity_sven"]["strength"] == before + 10
    assert sim.focus == 11 and sim.alert == 2


def test_patterns_entanglement_isolation_and_collapse_are_inspectable():
    sim = HackingSimulation.from_json(DATA, seed=1)
    assert sim.inject_pattern("memory_arrival", "echo").success
    assert "echo" in sim.graph.nodes["memory_arrival"]["patterns"]
    assert sim.suppress_pattern("memory_arrival", "echo").success
    assert sim.entangle_nodes("memory_arrival", "cg_jung_agent").success
    assert sim.graph.nodes["memory_arrival"]["state"] == "superposed"
    assert sim.collapse_state("memory_arrival").data["stabilized"] is True
    assert sim.isolate_node("cg_jung_agent").success
    assert all(not sim.graph.edges["cg_jung_agent", n]["active"] for n in sim.graph.neighbors("cg_jung_agent"))


def test_associations_can_be_created_broken_and_low_focus_is_transactional():
    sim = HackingSimulation.from_json(DATA)
    assert sim.create_association("memory_arrival", "cg_jung_agent").success
    assert sim.break_association("memory_arrival", "cg_jung_agent").success
    sim.focus = 0
    before = sim.graph.nodes["memory_arrival"]["stability"]
    assert not sim.inject_pattern("memory_arrival", "should-not-apply").success
    assert sim.graph.nodes["memory_arrival"]["stability"] == before


def test_failed_action_does_not_consume_turn_or_focus():
    sim = HackingSimulation.from_json(DATA)
    result = sim.suppress_pattern("memory_arrival", "absent")
    assert not result.success
    assert (sim.turn, sim.focus, sim.alert) == (0, 12, 0)
