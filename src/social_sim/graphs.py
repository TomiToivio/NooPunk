"""The Simulator's three graph views, validated together (#1309).

The Simulator has **three** graph layers, and they are not three RPG graph families:

* **Social** — the base: people, organizations, factions and institutions as actors, with typed ties. A tie is
  **reciprocal** when both ends agree about the relationship; a **directed** tie is one actor's opinion of another, which
  the target may not share. Tomi's `Paper/SOCIAL_GRAPH.md` fixes the value range (−4 hatred … +4 alliance), and that is
  the one scale used here.
* **Ideology** — a *projection* over the same actor ids: actor–concept–position statements, so affiliation, agreement and
  conflict can be read off coded positions. It is an explicit Simulator view, **not** a fifth world-graph family
  (`docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md` still lists four, and this module does not claim a fifth).
* **Physical** — the Helsinki city graph: locations as nodes, routes as edges, with Tomi's three node kinds (passive,
  active, graph). Coordinates are optional and never invented; a location that enters another graph names it.

Two rules shape everything below:

* **Co-occurrence is not a tie.** A social edge is authored or observed, never inferred because two actors mention the
  same concept. The ideology projection may say two actors *position themselves* similarly; it may not create a
  friendship, a membership or a conflict of interests.
* **One id per actor.** The same actor id is used by the social node, the ideology statements and any location reference,
  so a cross-layer question ("who is in this room, and what do they claim?") is a join, not a mapping exercise.

Paper drafts use underscore ids (`person_mars_eldrich`, `location_europol_field_office`); the shared RPG contract uses
dotted ids (`social.…`, `loc.…`). Both are accepted, the mapping is explicit in :func:`shared_id`, and neither is
silently rewritten — the choice of final convention is Tomi's.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

try:  # the kernel is the canonical simulator: its provenance contract is reused, not re-implemented
    from src.social_sim.kernel import KernelError, Origin, Provenance
except ModuleNotFoundError:  # pragma: no cover - installed with src/ on PYTHONPATH
    from .kernel import KernelError, Origin, Provenance  # type: ignore[no-redef]

__all__ = [
    "Concept",
    "GraphError",
    "IdeologyGraph",
    "Place",
    "Route",
    "SocialGraph",
    "SocialNode",
    "SocialTie",
    "Stance",
    "World",
    "load_world",
    "shared_id",
    "TIE_MIN",
    "TIE_MAX",
    "PLACE_KINDS",
    "POSITIONS",
]

#: Tomi's relationship scale, from `Paper/SOCIAL_GRAPH.md`: −4 hatred … +4 friendship, love or alliance.
TIE_MIN, TIE_MAX = -4, 4

#: The three city-graph node kinds from `Paper/PHYSICAL_GRAPH.md`.
PLACE_KINDS = ("passive", "active", "graph")

#: Positions an actor can take on a concept. `unknown` is not a weak stance; it is the absence of a coded one.
POSITIONS = ("support", "oppose", "neutral", "mixed", "unknown")


class GraphError(ValueError):
    """A graph that contradicts its own contract, rather than merely being sparse."""


# --------------------------------------------------------------------------- #
# Identifiers
# --------------------------------------------------------------------------- #

def shared_id(identifier: str, *, kind: str = "auto") -> str:
    """Map a Paper-style underscore id to the shared contract's dotted form, or leave a dotted id alone.

    This is a **mapping helper, not a migration**: nothing rewrites a fixture, and both conventions load. The final
    convention is an open decision recorded in `Rulebook/GRAPHS_1309.md`.
    """
    text = identifier.strip()
    if not text:
        raise GraphError("an identifier may not be empty")
    if "." in text:
        return text
    prefix = {
        "person": "social.",
        "organization": "social.",
        "faction": "social.",
        "institution": "social.",
        "location": "loc.",
        "auto": "",
    }.get(kind, "")
    if not prefix:
        raise GraphError(f"cannot map {text!r} without knowing whether it is an actor or a location")
    return prefix + text


# --------------------------------------------------------------------------- #
# Social
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class SocialNode:
    """An actor with identity and agency: a person, an organization, a faction, an institution."""

    id: str
    name: str
    kind: str = "person"          # person | organization | faction | institution
    tags: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=lambda: Provenance(Origin.SYNTHESIZED))

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.name.strip():
            raise GraphError("a social node needs an id and a name")
        if self.kind not in ("person", "organization", "faction", "institution"):
            raise GraphError(f"unknown actor kind {self.kind!r}")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "kind": self.kind, "tags": list(self.tags),
                "provenance": self.provenance.to_dict()}


@dataclass(frozen=True, slots=True)
class SocialTie:
    """A typed tie. ``reciprocal`` means both ends agree about the relationship; otherwise it is one opinion."""

    source: str
    target: str
    value: int
    kind: str = "opinion"
    reciprocal: bool = False
    tags: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=lambda: Provenance(Origin.SYNTHESIZED))

    def __post_init__(self) -> None:
        if self.source == self.target:
            raise GraphError("a tie joins two different actors")
        if not (TIE_MIN <= self.value <= TIE_MAX):
            raise GraphError(f"a tie value is {TIE_MIN}..{TIE_MAX}, got {self.value}")
        if not self.kind.strip():
            raise GraphError("a tie needs a kind")

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source, "target": self.target, "value": self.value, "kind": self.kind,
                "reciprocal": self.reciprocal, "tags": list(self.tags), "provenance": self.provenance.to_dict()}


@dataclass
class SocialGraph:
    """The base graph: actors and their ties, with the mutual/one-sided distinction enforced."""

    nodes: dict[str, SocialNode] = field(default_factory=dict)
    ties: list[SocialTie] = field(default_factory=list)

    def __post_init__(self) -> None:
        for key, node in self.nodes.items():
            if key != node.id:
                raise GraphError(f"node registered as {key!r} but carries id {node.id!r}")
        for tie in self.ties:
            for endpoint in (tie.source, tie.target):
                if endpoint not in self.nodes:
                    raise GraphError(f"tie {tie.source}→{tie.target} names unknown actor {endpoint!r}")
            mirror = self._mirror(tie)
            if tie.reciprocal and mirror is None:
                raise GraphError(f"{tie.source}→{tie.target} claims to be mutual but has no mirror tie")
            if not tie.reciprocal and mirror is not None:
                raise GraphError(f"{tie.source}→{tie.target} has a mirror; mark both as reciprocal")

    def _mirror(self, tie: SocialTie) -> SocialTie | None:
        for other in self.ties:
            if other is tie:
                continue
            if other.source == tie.target and other.target == tie.source and other.value == tie.value:
                return other
        return None

    # -- reading ------------------------------------------------------------------------------- #
    def degree(self, actor: str) -> int:
        """How many distinct actors this one has a tie with, in either direction."""
        neighbours = {t.target for t in self.ties if t.source == actor} | {t.source for t in self.ties if t.target == actor}
        return len(neighbours)

    def mutual(self) -> tuple[SocialTie, ...]:
        """Ties both ends agree about, each reported once."""
        seen: set[tuple[str, str]] = set()
        out: list[SocialTie] = []
        for tie in self.ties:
            key: tuple[str, str] = (min(tie.source, tie.target), max(tie.source, tie.target))
            if tie.reciprocal and key not in seen:
                seen.add(key)
                out.append(tie)
        return tuple(out)

    def one_sided(self) -> tuple[SocialTie, ...]:
        """Ties that are one actor's opinion — the target may not know, or may disagree."""
        return tuple(t for t in self.ties if not t.reciprocal)

    def to_dict(self) -> dict[str, Any]:
        return {"format": "noopunk.simulator.social", "version": 1,
                "nodes": [self.nodes[k].to_dict() for k in sorted(self.nodes)],
                "ties": [t.to_dict() for t in self.ties]}


# --------------------------------------------------------------------------- #
# Ideology — a projection over the same actors
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class Concept:
    id: str
    label: str
    kind: str = "signifier"       # signifier | demand | claim | frame | frontier

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.label.strip():
            raise GraphError("a concept needs an id and a label")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "kind": self.kind}


@dataclass(frozen=True, slots=True)
class Stance:
    """One coded actor–concept–position statement, with the evidence it rests on."""

    actor: str
    concept: str
    position: str
    statement_id: str
    evidence_id: str = ""
    review_status: str = "provisional"
    provenance: Provenance = field(default_factory=lambda: Provenance(Origin.INFERRED))

    def __post_init__(self) -> None:
        if self.position not in POSITIONS:
            raise GraphError(f"a position is one of {POSITIONS}, got {self.position!r}")
        if not self.statement_id.strip():
            raise GraphError("a stance must name the statement it was coded from")

    def to_dict(self) -> dict[str, Any]:
        return {"actor": self.actor, "concept": self.concept, "position": self.position,
                "statement_id": self.statement_id, "evidence_id": self.evidence_id,
                "review_status": self.review_status, "provenance": self.provenance.to_dict()}


@dataclass
class IdeologyGraph:
    """Coded positions over the social graph's actors. It never invents a social tie."""

    concepts: dict[str, Concept] = field(default_factory=dict)
    stances: list[Stance] = field(default_factory=list)
    actor_ids: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        for stance in self.stances:
            if self.actor_ids and stance.actor not in self.actor_ids:
                raise GraphError(f"stance names {stance.actor!r}, which is not an actor in the Social Graph")
            if stance.concept not in self.concepts:
                raise GraphError(f"stance names unknown concept {stance.concept!r}")

    def table(self) -> dict[str, dict[str, str]]:
        """``actor → concept → position``; a later statement for the same pair replaces the earlier one."""
        out: dict[str, dict[str, str]] = {}
        for stance in self.stances:
            out.setdefault(stance.actor, {})[stance.concept] = stance.position
        return out

    def agreement(self, left: str, right: str) -> float:
        """Share of *shared, coded* concepts on which two actors take the same position.

        Coded only: `unknown` is the absence of a position, not a moderate one, so it never counts as agreement. A pair
        with no shared coded concept has no measurable agreement, and the function refuses rather than returning 0.
        """
        table = self.table()
        shared = [c for c in table.get(left, {}) if c in table.get(right, {})]
        coded = [c for c in shared if table[left][c] != "unknown" and table[right][c] != "unknown"]
        if not coded:
            raise GraphError(f"{left} and {right} share no coded concept; agreement is undefined")
        same = sum(1 for c in coded if table[left][c] == table[right][c])
        return same / len(coded)

    def conflicts(self, *, threshold: int = 2) -> tuple[tuple[str, str], ...]:
        """Actor pairs who oppose each other on at least ``threshold`` coded concepts."""
        table = self.table()
        pairs: dict[tuple[str, str], int] = {}
        actors = sorted(table)
        for i, left in enumerate(actors):
            for right in actors[i + 1:]:
                opposed = 0
                for concept, position in table[left].items():
                    other = table[right].get(concept)
                    if other and position != "unknown" and other != "unknown":
                        if {position, other} == {"support", "oppose"}:
                            opposed += 1
                if opposed >= threshold:
                    pairs[(left, right)] = opposed
        return tuple(pair for pair in sorted(pairs))

    def to_dict(self) -> dict[str, Any]:
        return {"format": "noopunk.simulator.ideology", "version": 1,
                "concepts": [self.concepts[k].to_dict() for k in sorted(self.concepts)],
                "stances": [s.to_dict() for s in self.stances]}


# --------------------------------------------------------------------------- #
# Physical — the Helsinki city graph
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class Place:
    """A location node. Coordinates are optional and never invented; ``graph`` nodes name the graph they open."""

    id: str
    name: str
    kind: str = "active"
    address: str = ""
    coordinates: tuple[float, float] | None = None
    graph_ref: str = ""
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.name.strip():
            raise GraphError("a place needs an id and a name")
        if self.kind not in PLACE_KINDS:
            raise GraphError(f"a place kind is one of {PLACE_KINDS}, got {self.kind!r}")
        if self.kind == "graph" and not self.graph_ref.strip():
            raise GraphError(f"{self.id!r} enters another graph but names none")
        if self.coordinates is not None and len(self.coordinates) != 2:
            raise GraphError(f"{self.id!r} coordinates are a (lat, lon) pair")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "kind": self.kind, "address": self.address,
                "coordinates": list(self.coordinates) if self.coordinates else None,
                "graph_ref": self.graph_ref, "tags": list(self.tags)}


@dataclass(frozen=True, slots=True)
class Route:
    """A travel edge between two places."""

    source: str
    target: str
    kind: str = "street"          # street | metro | tram | door | path
    directed: bool = False
    traversable: bool = True

    def __post_init__(self) -> None:
        if self.source == self.target:
            raise GraphError("a route joins two different places")
        if not self.kind.strip():
            raise GraphError("a route needs a kind")

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source, "target": self.target, "kind": self.kind,
                "directed": self.directed, "traversable": self.traversable}


@dataclass
class PhysicalGraph:
    places: dict[str, Place] = field(default_factory=dict)
    routes: list[Route] = field(default_factory=list)

    def __post_init__(self) -> None:
        for route in self.routes:
            for endpoint in (route.source, route.target):
                if endpoint not in self.places:
                    raise GraphError(f"route {route.source}→{route.target} names unknown place {endpoint!r}")
        if not self.routes:
            raise GraphError("a city graph with no routes cannot be travelled")

    def reachable_from(self, place: str) -> tuple[str, ...]:
        reachable = {place}
        changed = True
        while changed:
            changed = False
            for route in self.routes:
                if not route.traversable:
                    continue
                if route.source in reachable and route.target not in reachable:
                    reachable.add(route.target)
                    changed = True
                if not route.directed and route.target in reachable and route.source not in reachable:
                    reachable.add(route.source)
                    changed = True
        return tuple(sorted(reachable))

    def to_dict(self) -> dict[str, Any]:
        return {"format": "noopunk.simulator.physical", "version": 1,
                "places": [self.places[k].to_dict() for k in sorted(self.places)],
                "routes": [r.to_dict() for r in self.routes]}


# --------------------------------------------------------------------------- #
# The world: three views, one set of ids
# --------------------------------------------------------------------------- #

@dataclass
class World:
    social: SocialGraph
    ideology: IdeologyGraph
    physical: PhysicalGraph

    def cross_reference(self) -> dict[str, int]:
        """Check the joins that make the three views one world; returns counts for the demo and the tests."""
        actors = set(self.social.nodes)
        missing_actors = sorted({s.actor for s in self.ideology.stances} - actors)
        if missing_actors:
            raise GraphError(f"ideology names actors absent from the Social Graph: {missing_actors}")
        graph_nodes = {p.graph_ref for p in self.physical.places.values() if p.graph_ref}
        missing_graphs = sorted(graph_nodes - {p.id for p in self.physical.places.values()})
        return {
            "actors": len(actors),
            "concepts": len(self.ideology.concepts),
            "stances": len(self.ideology.stances),
            "places": len(self.physical.places),
            "routes": len(self.physical.routes),
            "external_graph_refs": len(missing_graphs),
        }

    def to_dict(self) -> dict[str, Any]:
        return {"format": "noopunk.simulator.world", "version": 1,
                "social": self.social.to_dict(), "ideology": self.ideology.to_dict(),
                "physical": self.physical.to_dict()}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "World":
        if payload.get("format") != "noopunk.simulator.world":
            raise GraphError(f"not a world document: {payload.get('format')!r}")
        social_raw = payload["social"]
        social = SocialGraph(
            nodes={n["id"]: SocialNode(id=n["id"], name=n["name"], kind=n.get("kind", "person"),
                                       tags=tuple(n.get("tags") or ()),
                                       provenance=Provenance.from_dict(n.get("provenance") or {"origin": "synthesized"}))
                   for n in social_raw["nodes"]},
            ties=[SocialTie(source=t["source"], target=t["target"], value=int(t["value"]),
                            kind=t.get("kind", "opinion"), reciprocal=bool(t.get("reciprocal")),
                            tags=tuple(t.get("tags") or ()),
                            provenance=Provenance.from_dict(t.get("provenance") or {"origin": "synthesized"}))
                  for t in social_raw["ties"]],
        )
        ideology_raw = payload["ideology"]
        concepts = {c["id"]: Concept(id=c["id"], label=c["label"], kind=c.get("kind", "signifier"))
                    for c in ideology_raw["concepts"]}
        ideology = IdeologyGraph(
            concepts=concepts,
            stances=[Stance(actor=s["actor"], concept=s["concept"], position=s["position"],
                            statement_id=s["statement_id"], evidence_id=s.get("evidence_id", ""),
                            review_status=s.get("review_status", "provisional"),
                            provenance=Provenance.from_dict(s.get("provenance") or {"origin": "inferred"}))
                     for s in ideology_raw["stances"]],
            actor_ids=frozenset(social.nodes),
        )
        physical_raw = payload["physical"]
        places = {p["id"]: Place(id=p["id"], name=p["name"], kind=p.get("kind", "active"),
                                 address=p.get("address", ""),
                                 coordinates=tuple(p["coordinates"]) if p.get("coordinates") else None,
                                 graph_ref=p.get("graph_ref", ""), tags=tuple(p.get("tags") or ()))
                  for p in physical_raw["places"]}
        physical = PhysicalGraph(
            places=places,
            routes=[Route(source=r["source"], target=r["target"], kind=r.get("kind", "street"),
                          directed=bool(r.get("directed")), traversable=bool(r.get("traversable", True)))
                    for r in physical_raw["routes"]],
        )
        return cls(social=social, ideology=ideology, physical=physical)


def load_world(directory: Path | str) -> World:
    """Load the three fixtures from a directory and validate the joins between them."""
    base = Path(directory)
    social_raw = json.loads((base / "social_graph_1309.json").read_text(encoding="utf-8"))
    ideology_raw = json.loads((base / "ideology_graph_1309.json").read_text(encoding="utf-8"))
    physical_raw = json.loads((base / "physical_graph_1309.json").read_text(encoding="utf-8"))
    world = World.from_dict({"format": "noopunk.simulator.world", "version": 1,
                             "social": social_raw, "ideology": ideology_raw, "physical": physical_raw})
    world.cross_reference()
    return world
