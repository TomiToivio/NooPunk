"""The character-level DA/DNA/SNA layer (#1042).

The tests that matter here are the separations. Anyone can store a statement; the design only holds if the
model refuses, structurally, to let ideology become friendship or evidence become truth.
"""
from __future__ import annotations

import json

import pytest

from mud.nopunk_mud.ideology import (Actor, Concept, Discourse, IdeologyError, Relationship, Statement)


def _world() -> Discourse:
    d = Discourse()
    for cid in ("humanity", "security", "consciousness"):
        d.add_concept(Concept(cid, cid.title()))
    for aid, kind in (("unsa", "faction"), ("sipuli", "faction"), ("romppainen", "person")):
        d.add_actor(Actor(aid, kind, scope="UNSA" if aid == "unsa" else "SipuliVerkko"))
    return d


def test_a_statement_needs_a_known_actor_and_concept():
    d = _world()
    with pytest.raises(IdeologyError):
        d.articulate(Statement("ghost", "humanity", "support"))
    with pytest.raises(IdeologyError):
        d.articulate(Statement("unsa", "unheard-of", "support"))


def test_unknown_stances_and_evidence_kinds_are_refused():
    with pytest.raises(IdeologyError):
        Statement("unsa", "humanity", "vibes")
    with pytest.raises(IdeologyError):
        Statement("unsa", "humanity", "support", evidence="vibes")


def test_only_documents_testimony_and_observation_count_as_evidence():
    assert Statement("a", "c", "support", evidence="document").is_evidence_backed
    assert Statement("a", "c", "support", evidence="testimony").is_evidence_backed
    assert Statement("a", "c", "support", evidence="observation").is_evidence_backed
    assert not Statement("a", "c", "support", evidence="rumour").is_evidence_backed
    assert not Statement("a", "c", "support", evidence="assertion").is_evidence_backed


def test_positions_are_net_stance_per_actor_and_concept():
    d = _world()
    d.articulate(Statement("unsa", "security", "support"))
    d.articulate(Statement("unsa", "security", "support"))
    d.articulate(Statement("sipuli", "security", "oppose"))
    pos = d.positions()
    assert pos["unsa"]["security"] == 2
    assert pos["sipuli"]["security"] == -1


def test_a_contested_signifier_is_one_claimed_from_both_sides():
    d = _world()
    d.articulate(Statement("unsa", "security", "support"))
    d.articulate(Statement("sipuli", "security", "oppose"))
    d.articulate(Statement("unsa", "humanity", "support"))
    contested = d.contested_concepts()
    assert "security" in contested
    assert contested["security"] == {"support": ["unsa"], "oppose": ["sipuli"]}
    assert "humanity" not in contested, "one-sided agreement is not a contest"


def test_agreement_and_trust_are_independent():
    """The whole design in one assertion: shared signifiers, mutual contempt."""
    d = _world()
    for c in ("humanity", "consciousness"):
        d.articulate(Statement("unsa", c, "support"))
        d.articulate(Statement("sipuli", c, "support"))
    d.relate(Relationship("unsa", "sipuli", trust=-4, debt="a seized shipment"))
    verdict = d.antagonists_are_not_enemies("unsa", "sipuli")
    assert verdict["overlap"] == 2, "they agree about two signifiers"
    assert verdict["trust"] == -4, "and trust each other not at all"


def test_a_relationship_has_no_ideological_field():
    fields = set(Relationship.__dataclass_fields__)
    assert "stance" not in fields and "concept" not in fields and "ideology" not in fields
    st = set(Statement.__dataclass_fields__)
    assert "trust" not in st and "debt" not in st


def test_secret_is_need_to_know_not_merely_private():
    """`private` is known inside the speaker's network; `secret` needs the shares_secret flag even there."""
    d = _world()
    d.articulate(Statement("unsa", "security", "support", visibility="private"))
    d.articulate(Statement("unsa", "humanity", "support", visibility="secret"))
    visible = d.visible("UNSA")
    assert [s.concept for s in visible] == ["security"], "the private one, not the secret one"
    assert len(d.visible("UNSA", shares_secret=True)) == 2
    assert d.visible("SipuliVerkko") == [], "outsiders see neither"


def test_projections_are_deterministic_and_ordered():
    d = _world()
    for actor, concept in (("unsa", "security"), ("sipuli", "humanity"), ("unsa", "humanity")):
        d.articulate(Statement(actor, concept, "support"))
    once = json.dumps(d.positions(), sort_keys=True)
    twice = json.dumps(_world().positions(), sort_keys=True)
    assert once != twice  # empty world versus populated: the projection tracks the data, not the clock
    assert json.dumps(d.positions(), sort_keys=True) == once
    assert list(d.positions()) == sorted(d.positions())


def test_the_whole_world_round_trips_through_json():
    d = _world()
    d.articulate(Statement("unsa", "security", "support", demand="a public inquiry"))
    d.relate(Relationship("unsa", "romppainen", trust=2))
    again = Discourse.from_dict(json.loads(json.dumps(d.to_dict())))
    assert again.to_dict() == d.to_dict()
