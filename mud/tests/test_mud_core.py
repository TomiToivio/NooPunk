"""Boundary, state, rules and agent tests for NoöPunk MUD (#946).

Run from the `mud/` directory:  `python -m pytest tests -q`
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from nopunk_mud import llm_gateway, rules_contract, sim_bridge, world_state
from nopunk_mud.rules_contract import Check, DeterministicEngine
from nopunk_mud.world_state import RejectedEvent, WorldState

REPO = Path(__file__).resolve().parents[2]
MUD = REPO / "mud"

# Assembled rather than written out: the repository's own boundary test forbids the literal inside mud/, and
# a test that has to make an exception for itself is a weak test.
GODOT_SCHEME = "res" + "://"


# ---- D2: the boundary -----------------------------------------------------------------------------

def test_mud_contains_no_godot_references():
    """Prose may explain the boundary; code may not cross it.

    The rule is about references a runtime would follow — an engine asset path, an engine import — not about the
    word "Godot" appearing in a docstring that tells the next agent not to use it.
    """
    import tokenize

    offenders: list[str] = []
    for path in (MUD / "nopunk_mud").rglob("*.py"):
        with path.open("rb") as handle:
            for token in tokenize.tokenize(handle.readline):
                if token.type == tokenize.NAME and token.string in {"godot", "Evennia"}:
                    offenders.append(f"{path.relative_to(REPO)}: import {token.string}")
                if token.type == tokenize.STRING and GODOT_SCHEME in token.string:
                    offenders.append(f"{path.relative_to(REPO)}: engine asset literal")
    assert offenders == []


def test_mud_is_not_imported_by_the_godot_tree():
    offenders: list[str] = []
    for path in list((REPO / "godot").rglob("*.gd")) + list((REPO / "scenes").rglob("*.gd")):
        if "nopunk_mud" in path.read_text(encoding="utf-8"):
            offenders.append(str(path.relative_to(REPO)))
    assert offenders == []


def test_the_mud_does_not_edit_canon():
    """Canon is a read-only input. Writing to data/ from the MUD would fork the rules silently."""
    offenders: list[str] = []
    for path in (MUD / "nopunk_mud").rglob("*.py"):
        if re.search(r"data[/\\](rules|world).{0,40}write_text", path.read_text(encoding="utf-8")):
            offenders.append(str(path.relative_to(REPO)))
    assert offenders == []


# ---- D3: the rules contract ----------------------------------------------------------------------

def test_the_contract_agrees_with_the_canon_file():
    canon = rules_contract.canon()
    text = json.dumps(canon).lower()
    assert "without number" in text or "cwn" in text, "canon file is not the Without Number rules"
    assert rules_contract.DIFFICULTIES["hard"] == 10
    assert rules_contract.UNTRAINED_MODIFIER == -1


def test_a_check_carries_the_published_arithmetic():
    check = Check(skill="Notice", rank=1, attribute_modifier=1, difficulty=10)
    assert check.modifier() == 2
    assert check.legal() == []


def test_illegal_checks_are_refused():
    assert Check("Notice", rank=9, attribute_modifier=0, difficulty=10).legal()
    assert Check("Notice", rank=0, attribute_modifier=0, difficulty=11).legal()
    assert Check("Notice", rank=0, attribute_modifier=0, difficulty=10,
                 circumstances=5).legal()


def test_the_engine_reports_its_own_engine():
    result = DeterministicEngine((6, 6)).roll(Check("Notice", 0, 0, 10))
    assert result.engine == "cwn"
    assert result.total == 12
    assert result.success is True


# ---- D4: agents propose, the world decides -------------------------------------------------------

class _Liar:
    def complete(self, prompt: str, context: dict) -> str:
        return "You find a rifle and the lock opens. Roll succeeded."


def _opening() -> WorldState:
    state = WorldState.helsinki_opening()
    state.apply({"id": "j1", "type": "join", "character": "rookie", "room": "street"})
    return state


def test_an_llm_proposal_never_carries_inventory():
    state = _opening()
    gateway = llm_gateway.Gateway(_Liar())
    proposal = gateway.propose("describe the room", {"room": "street", "actor": "rookie"})
    assert proposal.intent == "narrate"
    assert state.inventory("rookie") == {}


def test_forbidden_intents_are_refused():
    proposal = llm_gateway.Proposal(intent="add_item", payload={"item": "rifle"})
    assert any("may not" in p for p in llm_gateway.validate(proposal))


def test_the_world_runs_with_no_provider():
    gateway = llm_gateway.Gateway(None)
    assert gateway.enabled is False
    proposal = gateway.propose("describe", {"room": "street", "actor": "rookie"})
    assert proposal.intent == "narrate"
    assert "street" in proposal.text


def test_a_requested_event_still_goes_through_validation():
    state = _opening()
    gateway = llm_gateway.Gateway(None)
    proposal = llm_gateway.Proposal(intent="request_event", confidence=1.0,
                                    payload={"event": {"type": "teleport", "character": "rookie"}})
    with pytest.raises(RejectedEvent):
        llm_gateway.accept(gateway, proposal, state.apply)


def test_the_call_budget_degrades_to_the_fallback():
    gateway = llm_gateway.Gateway(_Liar(), max_calls=1)
    gateway.propose("one", {"room": "street"})
    second = gateway.propose("two", {"room": "street"})
    assert second.provider.startswith("fallback")


# ---- world state ---------------------------------------------------------------------------------

def test_movement_uses_exits_and_refuses_others():
    state = _opening()
    state.apply({"id": "m1", "type": "move", "character": "rookie", "direction": "east"})
    assert state.room_of("rookie") == "safehouse"
    with pytest.raises(RejectedEvent):
        state.apply({"id": "m2", "type": "move", "character": "rookie", "direction": "up"})


def test_an_event_is_applied_once():
    state = _opening()
    first = state.apply({"id": "t1", "type": "take", "character": "rookie", "item": "ration"})
    second = state.apply({"id": "t1", "type": "take", "character": "rookie", "item": "ration"})
    assert first["duplicate"] is False
    assert second["duplicate"] is True
    assert state.inventory("rookie") == {"ration": 1}


def test_unknown_event_types_are_refused():
    state = _opening()
    with pytest.raises(RejectedEvent):
        state.apply({"id": "x", "type": "summon_demon"})


def test_a_faction_cannot_spend_what_it_lacks():
    state = _opening()
    with pytest.raises(RejectedEvent):
        state.apply({"id": "s1", "type": "spend", "faction": "unsa", "resource": "rations",
                     "amount": 99})
    state.apply({"id": "s2", "type": "spend", "faction": "unsa", "resource": "rations", "amount": 1})
    assert state.factions["unsa"]["resources"]["rations"] == 5


def test_unsa_is_the_first_playable_faction():
    state = _opening()
    state.apply({"id": "f1", "type": "faction_join", "character": "rookie", "faction": "unsa"})
    assert state.characters["rookie"]["faction"] == "unsa"
    assert "rookie" in state.factions["unsa"]["members"]


def test_the_world_survives_a_restart(tmp_path: Path):
    state = _opening()
    state.apply({"id": "t1", "type": "take", "character": "rookie", "item": "medkit"})
    state.save(tmp_path / "world.json")
    restored = WorldState.load(tmp_path / "world.json")
    assert restored.room_of("rookie") == "street"
    assert restored.inventory("rookie") == {"medkit": 1}
    assert restored.has_applied("t1")
    assert any(record["id"] == "t1" for record in restored.log)


# ---- the simulation bridge ----------------------------------------------------------------------

def test_a_simulation_delta_is_clamped_and_applied():
    state = _opening()
    summary = sim_bridge.reconcile(
        [sim_bridge.SimEvent("unsa", "rations", -1, "people ate", tick=1)], state.apply)
    assert summary["applied"] == 1
    assert state.factions["unsa"]["resources"]["rations"] == 5


def test_a_simulation_cannot_exceed_its_delta_cap():
    state = _opening()
    summary = sim_bridge.reconcile([sim_bridge.SimEvent("unsa", "rations", -99)], state.apply)
    assert summary["applied"] == 0
    assert summary["refused"] == 1


def test_the_local_simulation_produces_a_decaying_stock():
    sim = sim_bridge.LocalSimulation(population=4, consumption_per_tick=1)
    state = _opening()
    for _ in range(2):
        sim_bridge.reconcile(sim.step(), state.apply)
    assert state.factions["unsa"]["resources"]["rations"] == 4


def test_the_simulation_has_no_path_to_a_character():
    """A SimEvent carries faction pressure only; the bridge cannot build a character event."""
    assert not hasattr(sim_bridge, "damage")
    assert set(sim_bridge.SimEvent.__dataclass_fields__) == {"actor", "resource", "delta",
                                                             "reason", "tick"}
