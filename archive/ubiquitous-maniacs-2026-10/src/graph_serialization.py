from __future__ import annotations

from io import BytesIO

import networkx as nx


def empty_domain_graph(domain: str) -> nx.Graph:
    """Create an empty, undirected graph for one world domain."""
    graph = nx.Graph()
    graph.graph["domain"] = domain
    return graph


def graph_to_dict(graph: nx.Graph) -> dict[str, object]:
    """Return a simple Streamlit-friendly representation."""
    return {
        "domain": graph.graph.get("domain", "unknown"),
        "nodes": [
            {"id": node_id, **attributes}
            for node_id, attributes in sorted(graph.nodes(data=True), key=lambda item: str(item[0]))
        ],
        "edges": [
            {"source": source, "target": target, **attributes}
            for source, target, attributes in sorted(
                graph.edges(data=True), key=lambda item: (str(item[0]), str(item[1]))
            )
        ],
    }


def graph_to_dot(graph: nx.Graph) -> str:
    """Return Graphviz DOT suitable for Streamlit."""

    def quoted(value: object) -> str:
        escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    domain = str(graph.graph.get("domain", "world"))
    lines = [
        f"graph {quoted(domain)} {{",
        '  graph [overlap=false, splines=true, bgcolor="transparent"];',
        '  node [shape=ellipse, style="filled", fillcolor="#e2e8f0", fontname="Arial"];',
        '  edge [fontname="Arial", color="#64748b"];',
    ]
    for node_id, attributes in sorted(graph.nodes(data=True), key=lambda item: str(item[0])):
        label = attributes.get("name", attributes.get("label", node_id))
        lines.append(f"  {quoted(node_id)} [label={quoted(label)}];")
    for source, target, attributes in sorted(
        graph.edges(data=True), key=lambda item: (str(item[0]), str(item[1]))
    ):
        label = attributes.get("relationship", attributes.get("type", ""))
        label_attribute = f" [label={quoted(label)}]" if label != "" else ""
        lines.append(f"  {quoted(source)} -- {quoted(target)}{label_attribute};")
    lines.append("}")
    return "\n".join(lines)


def graph_to_gexf_bytes(graph: nx.Graph) -> bytes:
    """Return a Gephi-editable GEXF export."""
    export_graph = graph.copy()
    for node_id, attributes in export_graph.nodes(data=True):
        attributes["label"] = str(attributes.get("name", attributes.get("label", node_id)))

    buffer = BytesIO()
    nx.write_gexf(export_graph, buffer, encoding="utf-8", prettyprint=True)
    return buffer.getvalue()
