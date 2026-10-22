from pathlib import Path

from src.social.simulation import SocialSimulation

DATA = Path(__file__).parents[1] / "data" / "social_simulation" / "demo.json"


def test_multi_relationship_event_and_history_are_persistent():
    sim = SocialSimulation.from_json(DATA)
    before = sim.relationship("tanaka", "pilgrim")
    result = sim.apply_event("ethics_dispute")
    assert len(result.changes) == 3
    assert sim.relationship("tanaka", "pilgrim") < before
    assert sim.graph.nodes["pilgrim"]["mood"] == "irritated"
    assert sim.snapshot()["history"][0]["event_id"] == "ethics_dispute"


def test_missing_edges_are_created_and_values_are_clamped():
    data = {"characters": [{"id": "a"}, {"id": "b"}],
            "events": [{"id": "impact", "effects": [{"source": "a", "target": "b", "delta": 150}]}]}
    sim = SocialSimulation.from_dict(data)
    sim.apply_event("impact")
    assert sim.relationship("a", "b") == 100


def test_seeded_automatic_turn_is_reproducible():
    first = SocialSimulation.from_json(DATA, seed=9).auto_step().event_id
    second = SocialSimulation.from_json(DATA, seed=9).auto_step().event_id
    assert first == second

