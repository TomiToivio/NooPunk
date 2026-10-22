from io import BytesIO
from pathlib import Path

import networkx as nx
import pytest

from src.social import (
    build_social_graph,
    get_person_relationships,
    graph_to_dict,
    graph_to_dot,
    graph_to_gexf_bytes,
    list_people,
    list_relationships,
    load_people_records,
    load_relationship_records,
)


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _build_sample_graph() -> nx.Graph:
    people = load_people_records(DATA_DIR / "lab_people.csv")
    relationships = load_relationship_records(DATA_DIR / "lab_relationships.csv")
    return build_social_graph(people, relationships)


def test_graph_is_undirected_graph() -> None:
    graph = _build_sample_graph()
    assert isinstance(graph, nx.Graph)
    assert graph.graph["domain"] == "social"


def test_graph_contains_six_people() -> None:
    graph = _build_sample_graph()
    assert graph.number_of_nodes() == 6


def test_people_can_be_listed() -> None:
    graph = _build_sample_graph()
    people = list_people(graph)
    assert len(people) == 6
    assert {person["role"] for person in people} == {"patient", "staff", "ai"}


def test_relationships_can_be_listed() -> None:
    graph = _build_sample_graph()
    relationships = list_relationships(graph)
    assert relationships
    assert all("relationship" in relationship for relationship in relationships)


def test_single_person_relationships_can_be_inspected() -> None:
    graph = _build_sample_graph()
    relationships = get_person_relationships(graph, "soren_pilgrim")
    assert relationships
    assert all(relationship["person_id"] == "soren_pilgrim" for relationship in relationships)


def test_graph_can_be_converted_to_dictionary() -> None:
    graph = _build_sample_graph()
    graph_state = graph_to_dict(graph)
    assert set(graph_state) == {"people", "relationships"}
    assert len(graph_state["people"]) == 6


def test_graph_can_be_rendered_as_dot() -> None:
    graph = _build_sample_graph()
    dot = graph_to_dot(graph)
    assert dot.startswith("graph laboratory_social_graph")
    assert "Ingrid Falk" in dot
    assert "--" in dot


def test_graph_can_be_exported_to_gephi_gexf() -> None:
    graph = _build_sample_graph()
    gexf_data = graph_to_gexf_bytes(graph)
    exported_graph = nx.read_gexf(BytesIO(gexf_data))

    assert exported_graph.number_of_nodes() == 6
    assert exported_graph.number_of_edges() == graph.number_of_edges()
    assert exported_graph.nodes["ingrid_falk"]["label"] == "Ingrid Falk"
    assert "relationship" in exported_graph["soren_pilgrim"]["yuki_tanaka"]


def test_duplicate_person_id_is_rejected() -> None:
    people = [
        {"id": "same", "name": "First", "role": "patient"},
        {"id": "same", "name": "Second", "role": "staff"},
    ]
    with pytest.raises(ValueError, match="Henkilötunnus esiintyy kahdesti"):
        build_social_graph(people, [])


def test_duplicate_undirected_relationship_is_rejected() -> None:
    people = [
        {"id": "a", "name": "A", "role": "patient"},
        {"id": "b", "name": "B", "role": "staff"},
    ]
    relationships = [
        {"source": "a", "target": "b", "relationship": 1},
        {"source": "b", "target": "a", "relationship": 2},
    ]
    with pytest.raises(ValueError, match="Suhde esiintyy kahdesti"):
        build_social_graph(people, relationships)