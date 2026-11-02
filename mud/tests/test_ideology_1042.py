"""The character-level DA/DNA/SNA layer (#1042).

The tests that matter here are the separations. Anyone can store a statement; the design only holds if the
model refuses, structurally, to let ideology become friendship or evidence become truth.
"""
from __future__ import annotations

import json

import pytest

from mud.nopunk_mud.ideology import (
    Actor, Concept, Discourse, Goal, IdeologyError, ProfileVersion, Relationship, Statement, reaction,
)


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


# --------------------------------------------------------------------------- #
# Phase 1 residue (#1042): goals, append-only profile versions, outcome evidence
# and the one place the three layers meet — a first reaction.
# --------------------------------------------------------------------------- #


def _politicised() -> Discourse:
    """Two actors who agree about everything and cannot stand each other."""
    d = _world()
    for concept in ("humanity", "security", "consciousness"):
        d.articulate(Statement("unsa", concept, "support"))
        d.articulate(Statement("sipuli", concept, "support"))
    d.relate(Relationship("unsa", "sipuli", trust=-4, debt="the van"))
    return d


def test_goals_keep_three_registers_apart():
    d = _politicised()
    d.add_goal(Goal("unsa", "institutional", "survive the audit"))
    d.add_goal(Goal("unsa", "personal", "be proved right about the van"))
    d.add_goal(Goal("unsa", "ideological", "keep the disclosure file public"))
    assert d.goals_of("unsa", "institutional") == ["survive the audit"]
    assert d.goals_of("unsa", "ideological") == ["keep the disclosure file public"]
    assert len(d.goals_of("unsa")) == 3


def test_a_goal_must_belong_to_a_known_actor_and_a_known_register():
    d = _world()
    with pytest.raises(IdeologyError):
        d.add_goal(Goal("ghost", "personal", "haunt the archive"))
    with pytest.raises(IdeologyError):
        Goal("unsa", "budgetary", "cut costs")
    with pytest.raises(IdeologyError):
        Goal("unsa", "personal", "   ")


def test_a_profile_version_is_append_only():
    d = _politicised()
    d.record_profile(ProfileVersion("unsa", "2026-03-01", "public line", ("humanity",)))
    d.record_profile(ProfileVersion("unsa", "2026-09-01", "revised line", ("humanity", "psi")))
    assert d.profile_at("unsa", "2026-05-01").label == "public line"
    assert d.profile_at("unsa", "2026-09-01").label == "revised line"
    assert d.profile_at("unsa", "2026-01-01") is None
    # the history cannot be rewritten: an earlier or conflicting version is refused
    with pytest.raises(IdeologyError):
        d.record_profile(ProfileVersion("unsa", "2026-02-01", "backdated", ()))
    with pytest.raises(IdeologyError):
        d.record_profile(ProfileVersion("unsa", "2026-09-01", "same day, other line", ()))
    # re-recording the identical version is a no-op rather than an error
    d.record_profile(ProfileVersion("unsa", "2026-09-01", "revised line", ("humanity", "psi")))


def test_an_outcome_is_evidence_when_the_rules_resolved_it():
    d = _world()
    d.articulate(Statement("unsa", "security", "support", evidence="outcome", source="check failed"))
    d.articulate(Statement("sipuli", "security", "oppose", evidence="rumour"))
    assert d.statements[0].is_evidence_backed
    assert not d.statements[1].is_evidence_backed
    assert d.positions(evidence_only=True) == {"unsa": {"security": 1}}


def test_agreement_without_a_tie_is_open_not_warm():
    d = _politicised()
    stranger = Discourse()
    for concept in ("humanity", "security", "consciousness"):
        stranger.add_concept(Concept(concept, concept.title()))
    stranger.add_actor(Actor("unsa", "faction", scope="UNSA"))
    stranger.add_actor(Actor("passerby", "person", scope="Street"))
    for concept in ("humanity", "security", "consciousness"):
        stranger.articulate(Statement("unsa", concept, "support"))
        stranger.articulate(Statement("passerby", concept, "support"))
    result = stranger.reaction("unsa", "passerby", concept="security")
    assert result["band"] == "open"
    assert result["unknown"] == ["trust"]
    assert result["means"]["band_is_trust"] is False


def test_shared_signifiers_do_not_override_contempt():
    d = _politicised()
    result = d.reaction("unsa", "sipuli", concept="security")
    assert result["inputs"] == {"overlap": 3, "stance": "support", "trust": -4}
    assert result["band"] == "guarded", "agreement does not outrank contempt"
    assert result["score"] == 1, "the score alone would say 'open'; the tie is what caps it"


def test_disagreeing_with_a_trusted_colleague_is_not_hostility():
    d = _world()
    d.add_concept(Concept("psi", "PSI disclosure"))
    d.articulate(Statement("unsa", "psi", "oppose"))
    d.articulate(Statement("romppainen", "psi", "support"))
    for concept in ("humanity", "security"):
        d.articulate(Statement("unsa", concept, "support"))
        d.articulate(Statement("romppainen", concept, "support"))
    d.relate(Relationship("unsa", "romppainen", trust=2))
    result = d.reaction("unsa", "romppainen", concept="psi")
    assert result["inputs"] == {"overlap": 2, "stance": "oppose", "trust": 2}
    assert result["band"] == "neutral", "-1 for disagreement, +1 overlap, +1 trust: still civil"
    assert result["unknown"] == []
    result_stranger = reaction(overlap=0, stance="oppose", trust=None)
    assert result_stranger["band"] == "cold"
    assert result_stranger["unknown"] == ["trust"]


def test_reaction_refuses_inputs_outside_their_documented_ranges():
    with pytest.raises(IdeologyError):
        reaction(overlap=-1)
    with pytest.raises(IdeologyError):
        reaction(overlap=0, stance="undecided")
    with pytest.raises(IdeologyError):
        reaction(overlap=0, trust=5)


def test_goals_and_profiles_survive_a_json_round_trip():
    d = _politicised()
    d.add_goal(Goal("sipuli", "ideological", "keep the tunnels open", date="2026-08-01"))
    d.record_profile(ProfileVersion("sipuli", "2026-08-01", "hard line", ("humanity",)))
    again = Discourse.from_dict(json.loads(json.dumps(d.to_dict())))
    assert again.to_dict() == d.to_dict()
    assert again.goals_of("sipuli", "ideological") == ["keep the tunnels open"]
