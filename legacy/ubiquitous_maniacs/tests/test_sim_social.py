from __future__ import annotations

from pathlib import Path

import pytest

from src.sim.social import SocialSimulation, ACTIONS, REL_MIN, REL_MAX
from src.social import load_people_records, load_relationship_records

ROOT = Path(__file__).resolve().parents[1]
PEOPLE_CSV = ROOT / "data/lab_people.csv"
RELS_CSV = ROOT / "data/lab_relationships.csv"


def make_sim() -> SocialSimulation:
    people = load_people_records(PEOPLE_CSV)
    rels = load_relationship_records(RELS_CSV)
    return SocialSimulation.from_lab_data(people, rels)


# ── Social simulation ────────────────────────────────────────────


def test_social_sim_loads_from_lab_data() -> None:
    sim = make_sim()
    state = sim.state()
    assert len(state["characters"]) == 6
    assert len(state["relationships"]) == 3
    assert "small_talk" in state["available_actions"]


def test_relationships_scaled_to_100_range() -> None:
    sim = make_sim()
    # Pilgrim-Tanaka was -2 in CSV, should be -40 scaled
    rel = sim.get_relationship("soren_pilgrim", "yuki_tanaka")
    assert rel == -40


def test_interaction_modifies_relationship() -> None:
    sim = make_sim()
    before = sim.get_relationship("sven_olof_romppainen", "ingrid_falk")
    sim.interact("sven_olof_romppainen", "ingrid_falk", "deep_convo")
    after = sim.get_relationship("sven_olof_romppainen", "ingrid_falk")
    assert after == before + 5  # deep_convo delta is +5


def test_relationship_clamps_at_max() -> None:
    sim = make_sim()
    for _ in range(50):
        sim.interact("ingrid_falk", "elin_dahl", "share_secret")
    rel = sim.get_relationship("ingrid_falk", "elin_dahl")
    assert rel == REL_MAX


def test_negative_action_decreases_relationship() -> None:
    sim = make_sim()
    before = sim.get_relationship("soren_pilgrim", "elin_dahl")
    sim.interact("soren_pilgrim", "elin_dahl", "insult")
    after = sim.get_relationship("soren_pilgrim", "elin_dahl")
    assert after == before - 10


def test_step_generates_ambient_events() -> None:
    sim = make_sim()
    events = sim.step()
    assert len(events) >= 1  # at least one ambient interaction


def test_history_records_events() -> None:
    sim = make_sim()
    sim.interact("sven_olof_romppainen", "ingrid_falk", "flirt")
    hist = sim.history()
    assert len(hist) == 1
    assert hist[0]["action"] == "flirt"
    assert hist[0]["delta"] == 4


def test_gossip_spread_affects_third_party() -> None:
    sim = make_sim()
    # Betray has spread=3. Use Pilgrim as target — he has neighbors (Tanaka, Dahl)
    sim.interact("sven_olof_romppainen", "soren_pilgrim", "betray")
    # Check that spread events were logged
    hist = sim.history()
    spread_events = [e for e in hist if e["type"] == "spread"]
    assert len(spread_events) >= 1


def test_self_interaction_rejected() -> None:
    sim = make_sim()
    with pytest.raises(ValueError, match="self"):
        sim.interact("ingrid_falk", "ingrid_falk", "small_talk")


def test_unknown_action_rejected() -> None:
    sim = make_sim()
    with pytest.raises(KeyError, match="Unknown action"):
        sim.interact("ingrid_falk", "elin_dahl", "dance")


def test_state_is_inspectable() -> None:
    sim = make_sim()
    state = sim.state()
    assert "tick" in state
    assert "characters" in state
    assert "relationships" in state
    assert "available_actions" in state


def test_social_sim_save_round_trip_preserves_events_and_relationships() -> None:
    sim = make_sim()
    sim.interact("sven_olof_romppainen", "ingrid_falk", "flirt")

    restored = SocialSimulation.from_dict(sim.to_dict())

    assert restored.state() == sim.state()
    assert restored.history() == sim.history()
