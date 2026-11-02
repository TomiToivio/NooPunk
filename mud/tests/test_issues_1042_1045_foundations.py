"""Deterministic optional-mod tests, no Evennia service needed."""
import json
import pytest
from nopunk_mud.discourse_network import DiscourseLedger, Position
from nopunk_mud.crisis_regions import Region, RegionalWorld

def test_agreement_is_not_trust_or_friendship():
    ledger = DiscourseLedger()
    ledger.statement(Position("agent", "aid", "support", "e1", "case", "2045-01-01"))
    ledger.statement(Position("cultist", "aid", "support", "e2", "case", "2045-01-02"))
    assert ledger.alignment("agent", "cultist")["agreement"] == ["aid"]
    assert ledger.relations == {}
    with pytest.raises(PermissionError):
        ledger.relation("agent", "cultist", trust=4, access=4, reputation=4, event_id="e3")

def test_positions_are_separate_from_communications():
    ledger = DiscourseLedger()
    ledger.communication("agent", "scientist", "call1", "2045-01-01")
    assert not ledger.positions
    ledger.statement(Position("agent", "policy", "uncertain", "e2", "case", "2045-01-01"))
    assert ledger.alignment("agent", "scientist") == {"agreement": [], "conflict": []}
    restored = DiscourseLedger.from_snapshot(json.loads(json.dumps(ledger.snapshot())))
    assert restored.snapshot() == ledger.snapshot()

def test_disclosure_does_not_force_global_ruin():
    world = RegionalWorld()
    world.add_region(Region("helsinki"))
    world.add_region(Region("breach_zone", "after_the_fall"))
    assert world.ontological_disclosure is True
    assert world.regions["helsinki"].local_overlays == ()
    assert "scarcity" in world.regions["breach_zone"].local_overlays
    world.regions["breach_zone"].transition("recovering", event_id="aid1", reason="relief")
    assert world.regions["breach_zone"].local_overlays == ()
    assert RegionalWorld.from_snapshot(json.loads(json.dumps(world.snapshot()))).snapshot() == world.snapshot()

def test_bad_transition_does_not_mutate_region():
    region = Region("district")
    with pytest.raises(ValueError):
        region.transition("after_the_fall", event_id="a", reason="x", changes={"supplies": 10})
    assert region.state == "functioning"
    assert not region.history
