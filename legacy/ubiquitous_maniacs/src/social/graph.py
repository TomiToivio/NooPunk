from __future__ import annotations

from io import BytesIO

import networkx as nx

from .ontology import validate_person_record, validate_relationship_record


def build_social_graph(
    people_records: list[dict[str, object]],
    relationship_records: list[dict[str, object]],
) -> nx.Graph:
    graph = nx.Graph()
    graph.graph["domain"] = "social"

    for person in people_records:
        validate_person_record(person)
        person_id = str(person["id"])
        if person_id in graph:
            raise ValueError(f"Henkilötunnus esiintyy kahdesti: {person_id}")
        graph.add_node(
            person_id,
            id=person_id,
            name=str(person["name"]),
            role=str(person["role"]),
        )

    people_by_id = {person_id: attributes for person_id, attributes in graph.nodes(data=True)}

    for relationship in relationship_records:
        validate_relationship_record(relationship, people_by_id)
        source = str(relationship["source"])
        target = str(relationship["target"])
        if graph.has_edge(source, target):
            raise ValueError(f"Suhde esiintyy kahdesti: {source} – {target}")
        graph.add_edge(
            source,
            target,
            relationship=int(relationship["relationship"]),
        )

    return graph


def list_people(graph: nx.Graph) -> list[dict[str, object]]:
    return sorted(
        ({"id": person_id, **attributes} for person_id, attributes in graph.nodes(data=True)),
        key=lambda item: (str(item["role"]), str(item["name"])),
    )


def list_relationships(graph: nx.Graph) -> list[dict[str, object]]:
    return sorted(
        (
            {
                "source": source,
                "target": target,
                "relationship": attributes["relationship"],
            }
            for source, target, attributes in graph.edges(data=True)
        ),
        key=lambda item: (str(item["source"]), str(item["target"])),
    )


def get_person_relationships(graph: nx.Graph, person_id: str) -> list[dict[str, object]]:
    if person_id not in graph:
        raise KeyError(f"Tuntematon henkilö: {person_id}")

    relationships: list[dict[str, object]] = []
    for neighbor_id, attributes in graph[person_id].items():
        relationships.append(
            {
                "person_id": person_id,
                "other_id": neighbor_id,
                "other_name": graph.nodes[neighbor_id]["name"],
                "relationship": attributes["relationship"],
            }
        )
    return sorted(relationships, key=lambda item: str(item["other_name"]))


def graph_to_dict(graph: nx.Graph) -> dict[str, list[dict[str, object]]]:
    return {
        "people": list_people(graph),
        "relationships": list_relationships(graph),
    }


def graph_to_dot(graph: nx.Graph) -> str:
    """Return a Graphviz DOT representation for the Streamlit overview."""

    def quoted(value: object) -> str:
        escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    lines = [
        "graph laboratory_social_graph {",
        '  graph [overlap=false, splines=true, bgcolor="transparent"];',
        '  node [shape=ellipse, style="filled", fontname="Arial"];',
        '  edge [fontname="Arial", color="#64748b"];',
    ]

    for person_id, attributes in sorted(graph.nodes(data=True)):
        role = attributes["role"]
        if role == "patient":
            fill_color = "#bfdbfe"
        elif role == "ai":
            fill_color = "#fde68a"
        else:
            fill_color = "#bbf7d0"
        lines.append(
            f"  {quoted(person_id)} "
            f"[label={quoted(attributes['name'])}, fillcolor={quoted(fill_color)}];"
        )

    for source, target, attributes in sorted(graph.edges(data=True)):
        lines.append(
            f"  {quoted(source)} -- {quoted(target)} "
            f"[label={quoted(attributes['relationship'])}];"
        )

    lines.append("}")
    return "\n".join(lines)


def graph_to_gexf_bytes(graph: nx.Graph) -> bytes:
    """Return a Gephi-editable GEXF export without changing the graph."""
    export_graph = graph.copy()
    for _, attributes in export_graph.nodes(data=True):
        attributes["label"] = str(attributes["name"])

    buffer = BytesIO()
    nx.write_gexf(export_graph, buffer, encoding="utf-8", prettyprint=True)
    return buffer.getvalue()
