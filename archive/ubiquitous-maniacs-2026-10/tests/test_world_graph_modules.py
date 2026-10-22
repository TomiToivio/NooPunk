from io import BytesIO

import networkx as nx
import pytest

from src.cyber import build_cyber_graph
from src.cyber import graph_to_dict as cyber_to_dict
from src.cyber import graph_to_dot as cyber_to_dot
from src.cyber import graph_to_gexf_bytes as cyber_to_gexf
from src.noetic import build_noetic_graph
from src.noetic import graph_to_dict as noetic_to_dict
from src.noetic import graph_to_dot as noetic_to_dot
from src.noetic import graph_to_gexf_bytes as noetic_to_gexf
from src.physical import build_physical_graph
from src.physical import graph_to_dict as physical_to_dict
from src.physical import graph_to_dot as physical_to_dot
from src.physical import graph_to_gexf_bytes as physical_to_gexf


@pytest.mark.parametrize(
    ("builder", "domain", "to_dict", "to_dot", "to_gexf"),
    [
        (build_cyber_graph, "cyber", cyber_to_dict, cyber_to_dot, cyber_to_gexf),
        (build_noetic_graph, "noetic", noetic_to_dict, noetic_to_dot, noetic_to_gexf),
        (build_physical_graph, "physical", physical_to_dict, physical_to_dot, physical_to_gexf),
    ],
)
def test_empty_domain_graph_has_streamlit_and_gephi_formats(
    builder, domain, to_dict, to_dot, to_gexf
) -> None:
    graph = builder()

    assert isinstance(graph, nx.Graph)
    assert graph.graph["domain"] == domain
    assert graph.number_of_nodes() == 0
    assert graph.number_of_edges() == 0
    assert to_dict(graph) == {"domain": domain, "nodes": [], "edges": []}
    assert to_dot(graph).startswith(f'graph "{domain}"')

    exported = nx.read_gexf(BytesIO(to_gexf(graph)))
    assert exported.number_of_nodes() == 0
    assert exported.number_of_edges() == 0
