"""Synthetic AI26 simulator regression tests; no RPG or empirical data."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

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
    assert payload["schema"] == "ai26-synthetic-experiment-v2"
    # Provenance is a record now, not a string: the run is simulated, and it says why (#1286 acceptance conditions).
    assert payload["provenance"]["origin"] == "simulated"
    assert payload["provenance"]["method"] == "random-encounter-null-v1"
    assert payload["provenance"]["uncertainty"]
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

def test_actor_origins_are_distinguishable_and_survive_export():
    """The four origins exist as a type, and an export says which one each actor is."""
    roster = demo_roster(6)
    payload = simulate(roster, turns=3, seed=5)
    # `demo_roster(n)` yields n individuals *plus* the organizations they affiliate to; count what it gave us.
    assert payload["origins"]["synthesized"] == len(roster)
    assert payload["origins"]["observed"] == 0, "a synthetic roster is never observed material"
    assert all(actor["origin"] == "synthesized" for actor in payload["configuration"]["actors"])


def test_an_actor_may_be_inferred_but_never_observed():
    from simulation.provenance import Origin

    inferred = ResearchActor("synthetic:inferred-one", "individual", origin=Origin.INFERRED)
    payload = simulate((inferred, ResearchActor("synthetic:two", "individual")), turns=2, seed=1)
    assert payload["origins"]["inferred"] == 1

    with pytest.raises(ValueError):
        ResearchActor("synthetic:corpus-record", "individual", origin=Origin.OBSERVED)


def test_provenance_round_trips_through_json():
    from simulation.provenance import Origin, Provenance

    for origin in Origin:
        record = Provenance(origin, source="s", method="m", uncertainty="high", review_status="provisional")
        restored = Provenance.from_dict(json.loads(json.dumps(record.to_dict())))
        assert restored == record

    with pytest.raises(ValueError):
        Provenance.from_dict({"source": "nowhere"})
