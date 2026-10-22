from __future__ import annotations

import pytest

from src.sim.hacking import HackingSimulation, NODE_TYPES, EDGE_TYPES


def make_hack() -> HackingSimulation:
    hack = HackingSimulation()
    hack.build_default_target()
    return hack


# ── Hacking simulation ──────────────────────────────────────────


def test_default_target_has_nodes_and_edges() -> None:
    hack = make_hack()
    state = hack.state()
    assert len(state["nodes"]) >= 15
    assert len(state["edges"]) >= 15


def test_inspect_returns_node_details() -> None:
    hack = make_hack()
    info = hack.inspect("true_self")
    assert info["type"] == "identity"
    assert info["state"] == "suppressed"
    assert len(info["neighbors"]) >= 1


def test_trace_finds_path() -> None:
    hack = make_hack()
    path = hack.trace("self_image", "cg_jung")
    assert len(path) >= 2
    assert path[0] == "self_image"
    assert path[-1] == "cg_jung"


def test_strengthen_increases_edge() -> None:
    hack = make_hack()
    hack.strengthen("self_image", "cover_identity", 15)
    edge = hack.graph.edges["self_image", "cover_identity"]
    assert edge["strength"] >= 70


def test_weaken_decreases_edge() -> None:
    hack = make_hack()
    hack.weaken("self_image", "cover_identity", 10)
    edge = hack.graph.edges["self_image", "cover_identity"]
    assert edge["strength"] <= 55


def test_weaken_to_zero_breaks_edge() -> None:
    hack = make_hack()
    hack.weaken("self_image", "cover_identity", 100)
    assert not hack.graph.has_edge("self_image", "cover_identity")


def testinject_lowers_stability() -> None:
    hack = make_hack()
    before = hack.graph.nodes["memory_elsa"]["stability"]
    hack.inject("memory_elsa", "fear_pattern")
    after = hack.graph.nodes["memory_elsa"]["stability"]
    assert after < before
    assert "fear_pattern" in hack.graph.nodes["memory_elsa"]["patterns"]


def test_suppress_clears_patterns() -> None:
    hack = make_hack()
    hack.inject("memory_childhood", "false_memory")
    assert len(hack.graph.nodes["memory_childhood"]["patterns"]) == 1
    hack.suppress("memory_childhood")
    assert len(hack.graph.nodes["memory_childhood"]["patterns"]) == 0


def test_resonate_strengthens_and_destabilizes() -> None:
    hack = make_hack()
    s_before = hack.graph.nodes["self_image"]["stability"]
    t_before = hack.graph.nodes["cover_identity"]["stability"]
    hack.resonate("self_image", "cover_identity")
    s_after = hack.graph.nodes["self_image"]["stability"]
    t_after = hack.graph.nodes["cover_identity"]["stability"]
    edge = hack.graph.edges["self_image", "cover_identity"]
    assert edge["strength"] > 60  # strengthened
    assert s_after < s_before  # destabilized
    assert t_after < t_before


def test_entangle_synchronizes_stability() -> None:
    hack = make_hack()
    hack.entangle("memory_fall", "memory_elsa")
    s = hack.graph.nodes["memory_fall"]["stability"]
    t = hack.graph.nodes["memory_elsa"]["stability"]
    assert s == t  # synchronized


def test_isolate_removes_all_edges() -> None:
    hack = make_hack()
    removed = hack.isolate("implant_cortical")
    assert len(removed) >= 1
    assert hack.graph.degree("implant_cortical") == 0


def test_collapse_suppressed_may_reveal() -> None:
    hack = make_hack()
    result = hack.collapse("true_self")
    assert result["outcome"] in ("revealed", "failed_collapse")
    assert "before" in result
    assert "after" in result


def test_collapse_destabilized_stabilizes_or_destroys() -> None:
    hack = make_hack()
    # First destabilize a node
    hack.inject("memory_childhood", "disruptor")
    hack.inject("memory_childhood", "disruptor2")
    data = hack.graph.nodes["memory_childhood"]
    if data["stability"] < 25:
        data["state"] = "destabilized"
    result = hack.collapse("memory_childhood")
    assert result["outcome"] in ("stabilized", "collapsed", "no_effect")


def test_history_records_all_actions() -> None:
    hack = make_hack()
    hack.inspect("true_self")
    hack.strengthen("self_image", "cover_identity")
    hack.inject("memory_elsa", "fear")
    hist = hack.history()
    assert len(hist) == 3
    assert hist[0]["action"] == "inspect"
    assert hist[1]["action"] == "strengthen"
    assert hist[2]["action"] == "inject"


def test_state_is_inspectable() -> None:
    hack = make_hack()
    state = hack.state()
    assert "tick" in state
    assert "nodes" in state
    assert "edges" in state
    assert "node_types" in state
    assert "edge_types" in state


def test_unknown_node_rejected() -> None:
    hack = make_hack()
    with pytest.raises(KeyError, match="Unknown node"):
        hack.inspect("nonexistent")