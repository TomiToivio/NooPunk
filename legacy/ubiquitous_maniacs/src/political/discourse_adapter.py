"""Discourse-graph adapter: Noöpunkin social graph → Castells/Laclau Pydantic-mallit.

Tämä moduuli yhdistää Noöpunkin 6-dimensionaalisen sosiaalisen verkon
(`MultiDimensionalSocialGraph`) LaclauGPT:n Pydantic-pohjaisiin Castells
ja Laclau -graafimalleihin (`discourse_graph.py`).

Mapping-logiikka:

  Noöpunkin hahmot → Castells-solmut:
    Ragnarök  → ProgrammingPower (ohjelmoija, asettaa säännöt)
    Pilgrim   → SwitchingPower    (kytkijä, hallitsee liityntäpisteitä)
    Dahl      → Hub               (portinvartija, gatekeeper)
    Tanaka    → Counterpower      (vastavoima, etiikan vartija)
    Romppainen → Node             (potilas, verkoston reunalla)
    Ingrid    → Node              (potilas, verkoston reunalla)

  Noöpunkin suhdedimensiot → Castells/Laclau-relaatiot:
    authority > 2  → programs / dominates
    authority < -2 → resists
    trust < -2     → opposes / CONSTRUCTS_AS_ENEMY
    trust > 2      → connects / ARTICULATED_WITH
    suspicion > 2  → excludes / CONTESTED_BY
    fear > 2       → resists / DISLOCATED_BY
    familiarity > 2 → ARTICULATED_WITH / UNIFIED_BY
"""

from __future__ import annotations

from typing import Any

from src.game.social_graph import MultiDimensionalSocialGraph, RELATIONSHIP_DIMENSIONS
from src.political.discourse_graph import (
    CastellsNode,
    CastellsEdge,
    CastellsGraphExtraction,
    LaclauNode,
    LaclauEdge,
    LaclauGraphExtraction,
    SocialNode,
    SocialEdge,
    SocialGraphExtraction,
    CombinedGraphExtraction,
)

# ── Hahmojen roolimappaus Castells-ontologiaan ──────────────────────

CHARACTER_ROLE_MAP: dict[str, str] = {
    "ufab_ragnarok": "ProgrammingPower",
    "soren_pilgrim": "SwitchingPower",
    "elin_dahl": "Hub",
    "yuki_tanaka": "Counterpower",
    "romppainen": "Node",
    "ingrid_falk": "Node",
    "irungu_wakini": "Node",
}


def _to_castells_node(char_id: str, char_data: dict[str, Any]) -> CastellsNode:
    """Muunna Noöpunkin hahmo Castells-solmuksi."""
    label = CHARACTER_ROLE_MAP.get(char_id, "Node")
    name = char_data.get("name", char_id)
    role = char_data.get("role", "")
    mood = char_data.get("mood", "")
    desc = f"{role}, mieliala={mood}" if role else name
    return CastellsNode(
        id=char_id,
        label=label,  # type: ignore[arg-type]
        name=name,
        description=desc,
    )


def _to_castells_edge(
    source: str, target: str, dims: dict[str, int]
) -> CastellsEdge | None:
    """Muunna Noöpunkin suhdedimensiot Castells-kaareksi.

    Palauttaa None jos suhde ei tuota mielekästä Castells-relaatiota.
    """
    trust = dims.get("trust", 0)
    authority = dims.get("authority", 0)
    suspicion = dims.get("suspicion", 0)
    fear = dims.get("fear", 0)
    familiarity = dims.get("familiarity", 0)

    # Priorisoi vahvimmat relaatiot
    if authority > 2:
        return CastellsEdge(
            source=source, target=target, relation="programs",  # type: ignore[arg-type]
            weight=min(1.0, authority / 5.0),
            description=f"authority={authority}",
        )
    if authority < -2:
        return CastellsEdge(
            source=source, target=target, relation="resists",  # type: ignore[arg-type]
            weight=min(1.0, abs(authority) / 5.0),
            description=f"authority={authority}",
        )
    if trust < -2:
        return CastellsEdge(
            source=source, target=target, relation="opposes",  # type: ignore[arg-type]
            weight=min(1.0, abs(trust) / 5.0),
            description=f"trust={trust}",
        )
    if suspicion > 2:
        return CastellsEdge(
            source=source, target=target, relation="excludes",  # type: ignore[arg-type]
            weight=min(1.0, suspicion / 5.0),
            description=f"suspicion={suspicion}",
        )
    if fear > 2:
        return CastellsEdge(
            source=source, target=target, relation="resists",  # type: ignore[arg-type]
            weight=min(1.0, fear / 5.0),
            description=f"fear={fear}",
        )
    if trust > 2:
        return CastellsEdge(
            source=source, target=target, relation="connects",  # type: ignore[arg-type]
            weight=min(1.0, trust / 5.0),
            description=f"trust={trust}",
        )
    if familiarity > 2:
        return CastellsEdge(
            source=source, target=target, relation="connects",  # type: ignore[arg-type]
            weight=min(1.0, familiarity / 5.0),
            description=f"familiarity={familiarity}",
        )
    return None


def _to_laclau_node(char_id: str, char_data: dict[str, Any]) -> LaclauNode:
    """Muunna Noöpunkin hahmo Laclau-solmuksi."""
    label = CHARACTER_ROLE_MAP.get(char_id, "Node")
    # Kuvaa Castells-roolit Laclau-käsitteiksi
    laclau_label = {
        "ProgrammingPower": "NodalPoint",
        "SwitchingPower": "NodalPoint",
        "Hub": "Signifier",
        "Counterpower": "Antagonism",
        "Node": "Demand",
    }.get(label, "Signifier")

    is_empty = label == "ProgrammingPower"  # Ragnarök = tyhjä merkitsijä?

    return LaclauNode(
        id=char_id,
        label=laclau_label,  # type: ignore[arg-type]
        name=char_data.get("name", char_id),
        description=f"{char_data.get('role', '')}, mieliala={char_data.get('mood', '')}",
        is_empty_signifier=is_empty if is_empty else None,
    )


def _to_laclau_edge(
    source: str, target: str, dims: dict[str, int]
) -> LaclauEdge | None:
    """Muunna Noöpunkin suhdedimensiot Laclau-kaareksi."""
    trust = dims.get("trust", 0)
    suspicion = dims.get("suspicion", 0)
    authority = dims.get("authority", 0)
    familiarity = dims.get("familiarity", 0)

    if authority > 2:
        return LaclauEdge(
            source=source, target=target, relation="HEGEMONIZES",  # type: ignore[arg-type]
            logic="hegemony",
            weight=min(1.0, authority / 5.0),
        )
    if trust < -2:
        return LaclauEdge(
            source=source, target=target, relation="CONSTRUCTS_AS_ENEMY",  # type: ignore[arg-type]
            logic="antagonism",
            weight=min(1.0, abs(trust) / 5.0),
        )
    if suspicion > 2:
        return LaclauEdge(
            source=source, target=target, relation="CONTESTED_BY",  # type: ignore[arg-type]
            logic="contestation",
            weight=min(1.0, suspicion / 5.0),
        )
    if trust > 2 or familiarity > 2:
        return LaclauEdge(
            source=source, target=target, relation="ARTICULATED_WITH",  # type: ignore[arg-type]
            logic="equivalence",
            weight=min(1.0, max(trust, familiarity) / 5.0),
        )
    return None


def social_to_combined(
    graph: MultiDimensionalSocialGraph,
    observer: str | None = None,
) -> CombinedGraphExtraction:
    """Muunna Noöpunkin social graph CombinedGraphExtraction-malliksi.

    Args:
        graph: Noöpunkin MultiDimensionalSocialGraph
        observer: jos annettu, piilota hidden-suhteet tältä hahmolta

    Returns:
        CombinedGraphExtraction (Social + Castells + Laclau)
    """
    # ── Solmut ──────────────────────────────────────────────
    social_nodes: list[SocialNode] = []
    castells_nodes: list[CastellsNode] = []
    laclau_nodes: list[LaclauNode] = []

    for char in graph.known_characters(observer):
        cid = char["id"]
        # Social node
        social_nodes.append(SocialNode(
            id=cid,
            label="CONCEPT",  # type: ignore[arg-type]
            name=char["name"],
            description=f"role={char.get('role','')}, mood={char.get('mood','')}",
        ))
        # Castells node
        castells_nodes.append(_to_castells_node(cid, char))
        # Laclau node
        laclau_nodes.append(_to_laclau_node(cid, char))

    # ── Kaaret ──────────────────────────────────────────────
    social_edges: list[SocialEdge] = []
    castells_edges: list[CastellsEdge] = []
    laclau_edges: list[LaclauEdge] = []

    for rel in graph.visible_relationships(observer):
        src = rel["source"]
        tgt = rel["target"]
        dims = {d: rel.get(d, 0) for d in RELATIONSHIP_DIMENSIONS}

        # Social edge — aina, jos jokin dimensio ≠ 0
        nonzero = {k: v for k, v in dims.items() if v != 0}
        if nonzero:
            # Määritä relaatio
            if dims.get("trust", 0) > 0:
                relation = "has_positive_sentiment_towards"
            elif dims.get("trust", 0) < 0:
                relation = "has_negative_sentiment_towards"
            elif dims.get("suspicion", 0) > 0:
                relation = "opposes"
            else:
                relation = "mentions"
            social_edges.append(SocialEdge(
                source=src, target=tgt, relation=relation,  # type: ignore[arg-type]
                weight=min(1.0, max(abs(v) for v in nonzero.values()) / 5.0) if nonzero else 0.5,
            ))

        # Castells edge — vain jos mielekäs
        c_edge = _to_castells_edge(src, tgt, dims)
        if c_edge:
            castells_edges.append(c_edge)

        # Laclau edge — vain jos mielekäs
        l_edge = _to_laclau_edge(src, tgt, dims)
        if l_edge:
            laclau_edges.append(l_edge)

    return CombinedGraphExtraction(
        social=SocialGraphExtraction(nodes=social_nodes, edges=social_edges),
        castells=CastellsGraphExtraction(nodes=castells_nodes, edges=castells_edges),
        laclau=LaclauGraphExtraction(nodes=laclau_nodes, edges=laclau_edges),
    )