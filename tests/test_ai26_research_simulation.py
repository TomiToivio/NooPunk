"""Synthetic AI26 simulator regression tests; no RPG or empirical data."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from simulation.ai26_research import (  # noqa: E402
    ResearchActor, demo_roster, main, simulate, verify_replay,
)
from simulation.events import Event  # noqa: E402
from simulation.world_state import reduce_events  # noqa: E402


def test_seeded_runs_are_byte_identical():
    roster = demo_roster(50)
    first = simulate(roster, turns=40, seed=11)
    second = simulate(reversed(roster), turns=40, seed=11)
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert verify_replay(first)
    assert first["summary"]["communication_events"] == 40


def test_different_seed_changes_communications():
    roster = demo_roster(20)
    first = simulate(roster, turns=20, seed=1)
    second = simulate(roster, turns=20, seed=2)
    assert first["graphs"]["communication_edges"] != second["graphs"]["communication_edges"]


def test_graph_integrity_and_replay_with_independent_organizations():
    result = simulate(demo_roster(5), seed=7, turns=8)
    graph = result["graphs"]
    ids = {node["actor_id"] for node in graph["nodes"]}
    assert {"synthetic:organization-a", "synthetic:organization-b"} <= ids
    assert all(edge["source"] in ids and edge["target"] in ids
               for edge in graph["social_edges"] + graph["communication_edges"])
    assert len(graph["social_edges"]) == 5
    assert all(edge["turn"] >= 0 for edge in graph["communication_edges"])
    assert all(edge["source"] != edge["target"] for edge in graph["communication_edges"])
    assert verify_replay(result)
    events = [Event.from_dict(item) for item in result["events"]]
    assert reduce_events(events).event_count == len(result["events"])


def test_isolates_and_empty_rosters_have_no_fake_messages():
    zero = simulate((), seed=7, turns=5)
    single = simulate((ResearchActor("synthetic:a", "individual"),), turns=5)
    assert zero["summary"]["events"] == 0
    assert single["summary"]["events"] == 0
    assert single["summary"]["isolated_actors"] == ["synthetic:a"]
    assert verify_replay(zero)


@pytest.mark.parametrize("bad_roster", [
    (ResearchActor("synthetic:a", "individual"), ResearchActor("synthetic:a", "individual")),
    (ResearchActor("synthetic:a", "individual", "synthetic:missing"),),
])
def test_rejects_duplicate_or_dangling_actor_references(bad_roster):
    with pytest.raises(ValueError):
        simulate(bad_roster)


def test_rejects_non_synthetic_actor_ids_and_invalid_membership():
    with pytest.raises(ValueError):
        ResearchActor("real-person", "individual")
    with pytest.raises(ValueError):
        ResearchActor("synthetic:org", "organization", "synthetic:other")
    with pytest.raises(ValueError):
        simulate(demo_roster(2), turns=-1)


def test_export_replay_and_provenance(tmp_path):
    path = tmp_path / "synthetic.json"
    assert main(["--population", "4", "--turns", "6", "--seed", "15", "--output", str(path)]) == 0
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema"] == "ai26-synthetic-experiment-v1"
    assert payload["provenance"] == "simulated"
    assert payload["scientific_status"] == "hypothetical_null_model_not_empirical_finding"
    assert verify_replay(payload)
    payload["events"][-1]["content"] = "tampered"
    assert not verify_replay(payload)


def test_no_game_or_llm_runtime_imports():
    import inspect
    import simulation.ai26_research as research
    source = inspect.getsource(research)
    for forbidden in ("import rules", "import mud", "import godot", "import ollama",
                      "import strategy_game", "import concordia"):
        assert forbidden not in source
