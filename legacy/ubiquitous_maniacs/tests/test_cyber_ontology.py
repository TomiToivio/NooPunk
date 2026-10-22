from src.cyber import cyber_ontology_to_dict, list_edge_types, list_node_types


def test_cyber_node_types_are_listed() -> None:
    node_types = list_node_types()
    assert [node_type["type"] for node_type in node_types] == [
        "host",
        "server",
        "router",
        "switch",
        "access_point",
        "firewall",
        "gateway",
    ]


def test_cyber_edge_types_are_listed() -> None:
    edge_types = list_edge_types()
    assert [edge_type["type"] for edge_type in edge_types] == [
        "wired_link",
        "wireless_link",
        "logical_link",
    ]


def test_cyber_ontology_can_be_serialized_to_dict() -> None:
    ontology = cyber_ontology_to_dict()
    assert set(ontology) == {"node_types", "edge_types"}
    assert len(ontology["node_types"]) == 7
    assert len(ontology["edge_types"]) == 3
