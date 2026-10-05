from __future__ import annotations
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simulation.affect import AffectEdge, AffectGraph, inherit_faction_affects

def edge(source,target,affect,score,domain):
    return AffectEdge(source=source,source_type="faction" if domain.startswith("faction_") else "character",
                      target=target,target_type="concept",affect=affect,
                      affect_score=score,domain=domain)

def test_validation():
    with pytest.raises(ValueError): edge("a","b","Supports",101,"motivation")
    with pytest.raises(ValueError): edge("a","b","Supports",10,"sentiment")

def test_unknown_differs_from_explicit_neutral():
    graph=AffectGraph()
    assert graph.between("a","b")==[]
    assert graph.effective_score("a","b","Knows")==0
    graph.add(edge("a","b","Knows",0,"contact"))
    assert len(graph.between("a","b",domain="contact"))==1

def test_multiple_labels_and_directionality():
    graph=AffectGraph()
    graph.add(edge("pc","AGI","Supports",30,"motivation"))
    graph.add(edge("pc","AGI","Fears",-45,"motivation"))
    graph.add(edge("AGI","pc","Distrusts",-20,"reputation"))
    assert {x.affect for x in graph.between("pc","AGI")}=={"Supports","Fears"}
    assert [x.affect for x in graph.between("AGI","pc")]==["Distrusts"]

def test_inheritance_preserves_ambivalence_and_means_matching_labels():
    inherited=inherit_faction_affects(character_id="pc",faction_edges=[
        edge("a","AGI","Supports",70,"faction_us"),
        edge("b","AGI","Supports",50,"faction_us"),
        edge("b","AGI","Fears",-60,"faction_frontier")])
    by={x.affect:x for x in inherited}
    assert by["Supports"].affect_score==60
    assert by["Fears"].affect_score==-60
    assert by["Supports"].metadata["inherited_from"]==["a","b"]

def test_personal_override():
    personal=AffectEdge(source="pc",source_type="character",target="AGI",target_type="concept",
                        affect="Supports",affect_score=85,domain="motivation",
                        metadata={"origin":"personal"})
    inherited=inherit_faction_affects(character_id="pc",
        faction_edges=[edge("a","AGI","Supports",70,"faction_us"),
                       edge("b","AGI","Fears",-60,"faction_frontier")],
        personal_edges=[personal])
    by={x.affect:x for x in inherited}
    assert by["Supports"].affect_score==85
    assert by["Fears"].affect_score==-60

def test_round_trip():
    graph=AffectGraph([edge("pc","friend","Trusts",55,"contact")])
    assert AffectGraph.from_dict(graph.to_dict()).edges==graph.edges
