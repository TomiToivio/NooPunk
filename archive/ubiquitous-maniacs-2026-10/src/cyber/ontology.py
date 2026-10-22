from __future__ import annotations


CYBER_NODE_TYPES = (
    {
        "type": "host",
        "description": "Tavallinen verkkoon kytketty päätelaite, kuten PC, puhelin tai IoT-laite.",
    },
    {
        "type": "server",
        "description": "Palveluja tarjoava tietokone.",
    },
    {
        "type": "router",
        "description": "Verkkojen välinen reitityslaite.",
    },
    {
        "type": "switch",
        "description": "Saman lähiverkon laitteita yhdistävä verkkolaite.",
    },
    {
        "type": "access_point",
        "description": "Langattoman verkon tukiasema.",
    },
    {
        "type": "firewall",
        "description": "Liikennettä suodattava verkkolaite tai kontrollipiste.",
    },
    {
        "type": "gateway",
        "description": "Eri verkkoja tai protokollia yhdistävä solmu.",
    },
)

CYBER_EDGE_TYPES = (
    {
        "type": "wired_link",
        "description": "Fyysinen langallinen verkkoyhteys.",
    },
    {
        "type": "wireless_link",
        "description": "Fyysinen langaton verkkoyhteys.",
    },
    {
        "type": "logical_link",
        "description": "Looginen yhteys fyysisen verkon päällä, kuten VPN tai tunneli.",
    },
)


def list_node_types() -> list[dict[str, str]]:
    return [dict(node_type) for node_type in CYBER_NODE_TYPES]


def list_edge_types() -> list[dict[str, str]]:
    return [dict(edge_type) for edge_type in CYBER_EDGE_TYPES]


def cyber_ontology_to_dict() -> dict[str, list[dict[str, str]]]:
    return {
        "node_types": list_node_types(),
        "edge_types": list_edge_types(),
    }
