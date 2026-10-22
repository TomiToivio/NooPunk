from __future__ import annotations

import pytest

from src.rpg import ProjectionLayer, ProjectionSession, ProjectionStatus


def test_projection_loop_returns_with_ambiguous_provenance() -> None:
    session = ProjectionSession()
    session.enter(preparation=10, anchor_support=20)
    session.observe("impossible_corridor", {ProjectionLayer.VIRTUAL: 10, ProjectionLayer.NOETIC: 10})
    session.traverse(2)
    session.resonate("ingrid_falk", intensity=2)
    session.manifest("komisario_kallio")
    session.return_to_body(assistance=5)

    state = session.inspect_state()
    assert state["status"] == ProjectionStatus.RETURNED.value
    assert state["trace"] > 0
    assert "returned_with_ambiguous_provenance" in state["known_information"]
    assert sum(state["hypotheses"].values()) == 100
    assert state["hypotheses"]["virtual"] == state["hypotheses"]["noetic"]


def test_projection_can_lose_its_anchor_without_declaring_a_layer_true() -> None:
    session = ProjectionSession()
    session.enter(anchor_support=-60)
    session.traverse(10)

    state = session.inspect_state()
    assert state["status"] == ProjectionStatus.LOST.value
    assert "projection_integrity_lost" in state["known_information"]
    assert len([value for value in state["hypotheses"].values() if value > 0]) == 4


def test_projection_actions_require_an_active_projection() -> None:
    session = ProjectionSession()
    with pytest.raises(ValueError, match="active projection"):
        session.observe("premature")
