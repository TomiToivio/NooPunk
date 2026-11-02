"""LaclauGPT-style social model for the MUD: DA, DNA and SNA kept apart (#1042).

This is a NoöPunk overlay on the locked CWN core: it adds a persistent social world and never
touches a dice roll, an attribute or a rule. The engine is deterministic — same events in, same
state out — and it can be fed by scripted content today and by an LLM later without changing shape.

Three layers, deliberately not one score:

* **DA — discourse.** Each actor carries values, identities, demands, signifiers, antagonisms and
  goals, plus recorded uncertainty. A profile is an interpretation, not a stat.
* **DNA — actor–concept positions.** A position is a claim about where an actor stands on a concept,
  carrying the event that produced it and the kind of source behind it. Contradictory positions are
  kept side by side; nothing is averaged into a friend/enemy axis.
* **SNA — relationships.** Typed ties (communication, affiliation, obligation), each with the event
  that established it. Trust, access and reputation are separate game quantities and are not
  derived from the graph.

Provenance is load-bearing. Every claim is `evidence`, `fiction` or `gameplay`, and a fiction event
never overwrites an evidence-backed stance; the conflict is reported instead.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable

SCHEMA_VERSION = 1

#: What kind of thing produced a claim. An LLM rumour and an observed statement are not the same.
SOURCES = ("evidence", "fiction", "gameplay")

#: Position values are a scale, not a verdict. ``None`` means "no claim", which is not neutral.
POSITION_MIN, POSITION_MAX = -2, 2


class SocialModelError(ValueError):
    """A malformed event or an operation the model refuses."""


@dataclass
class Actor:
    id: str
    kind: str = "person"  # person | organisation
    name: str = ""
    aliases: list[str] = field(default_factory=list)


@dataclass
class Affiliation:
    actor: str
    organisation: str
    role: str = ""
    event_id: str = ""


@dataclass
class Event:
    id: str
    at: str
    kind: str  # statement | contact | membership | observation
    actor: str
    source: str = "evidence"
    concept: str = ""
    polarity: int | None = None
    other: str = ""
    tie: str = ""
    role: str = ""
    text: str = ""
    #: Who may know this event produced a tie. Empty means "not gated" (see :meth:`dossier`).
    other_known_by: list[str] = field(default_factory=list)


@dataclass
class DiscourseProfile:
    actor: str
    values: list[str] = field(default_factory=list)
    identities: list[str] = field(default_factory=list)
    demands: list[str] = field(default_factory=list)
    signifiers: list[str] = field(default_factory=list)
    antagonisms: list[str] = field(default_factory=list)
    goals: list[str] = field(default_factory=list)
    uncertainty: dict[str, str] = field(default_factory=dict)


@dataclass
class Position:
    actor: str
    concept: str
    polarity: int | None
    event_id: str
    source: str


@dataclass
class Tie:
    a: str
    b: str
    kind: str  # communication | affiliation | obligation
    event_id: str
    source: str
    known_by: list[str] = field(default_factory=list)


class SocialWorld:
    """Persistent social state. All mutation goes through :meth:`ingest`."""

    def __init__(self) -> None:
        self.actors: dict[str, Actor] = {}
        self.affiliations: list[Affiliation] = []
        self.events: list[Event] = []
        self.profiles: dict[str, DiscourseProfile] = {}
        self.positions: list[Position] = []
        self.ties: list[Tie] = []

    # ---- identity ------------------------------------------------------------------------

    def add_actor(self, actor: Actor) -> Actor:
        existing = self.actors.get(actor.id)
        if existing is not None:
            # Reconcile rather than duplicate: the same person can arrive under two ids.
            for alias in [existing.name, *existing.aliases]:
                if alias and alias not in actor.aliases and alias != actor.name:
                    actor.aliases.append(alias)
            self.actors[actor.id] = actor
            return actor
        self.actors[actor.id] = actor
        return actor

    def resolve(self, name: str) -> str:
        """Find an actor id by id, name or alias. Case-insensitive; raises when ambiguous or absent."""
        wanted = name.strip().casefold()
        hits = [
            actor.id
            for actor in self.actors.values()
            if wanted == actor.id.casefold()
            or wanted == actor.name.casefold()
            or any(wanted == alias.casefold() for alias in actor.aliases)
        ]
        if not hits:
            raise SocialModelError(f"no actor matches {name!r}")
        if len(hits) > 1:
            raise SocialModelError(f"{name!r} matches several actors: {sorted(hits)}")
        return hits[0]

    # ---- ingestion -----------------------------------------------------------------------

    def ingest(self, event: Event) -> None:
        """Apply one event deterministically. Unknown kinds are refused, not ignored."""
        if event.source not in SOURCES:
            raise SocialModelError(f"unknown source {event.source!r}; expected one of {SOURCES}")
        if event.id in {e.id for e in self.events}:
            return  # idempotent: re-ingesting the same event changes nothing

        if event.actor and event.actor not in self.actors:
            raise SocialModelError(f"event {event.id} names an unknown actor {event.actor!r}")

        if event.kind == "statement":
            if event.polarity is not None and not POSITION_MIN <= event.polarity <= POSITION_MAX:
                raise SocialModelError(f"polarity {event.polarity} is outside {POSITION_MIN}..{POSITION_MAX}")
            if not event.concept:
                raise SocialModelError("a statement needs a concept")
            self.positions.append(
                Position(event.actor, event.concept, event.polarity, event.id, event.source)
            )
        elif event.kind == "contact":
            if event.other not in self.actors:
                raise SocialModelError(f"event {event.id} names an unknown contact {event.other!r}")
            self.ties.append(
                Tie(event.actor, event.other, event.tie or "communication", event.id,
                    event.source, list(event.other_known_by))
            )
        elif event.kind == "affiliation":
            if event.concept not in self.actors:
                raise SocialModelError(f"event {event.id} names an unknown organisation")
            self.affiliations.append(
                Affiliation(event.actor, event.concept, event.role, event.id)
            )
        elif event.kind == "observation":
            pass  # a note with no mechanical consequence; kept in the log for provenance
        else:
            raise SocialModelError(f"unknown event kind {event.kind!r}")

        self.events.append(event)

    # ---- reading -------------------------------------------------------------------------

    def stance(self, actor: str, concept: str) -> dict[str, Any]:
        """Every claim about where ``actor`` stands on ``concept``, and whether they disagree.

        Never averages. ``value`` is only set when all evidence/gameplay claims agree; ``None``
        means "no single value", and ``unknown`` distinguishes "no claim at all".
        """
        rows = [p for p in self.positions if p.actor == actor and p.concept == concept]
        if not rows:
            return {"actor": actor, "concept": concept, "value": None, "unknown": True,
                    "conflicts": [], "sources": []}
        values = {p.polarity for p in rows if p.polarity is not None}
        conflicts = []
        for i, left in enumerate(rows):
            for right in rows[i + 1:]:
                if left.polarity is None or right.polarity is None:
                    continue
                if left.polarity * right.polarity < 0 or (
                    left.polarity != right.polarity and left.source != right.source
                ):
                    conflicts.append({
                        "left": {"event": left.event_id, "polarity": left.polarity, "source": left.source},
                        "right": {"event": right.event_id, "polarity": right.polarity, "source": right.source},
                    })
        return {
            "actor": actor,
            "concept": concept,
            "value": values.pop() if len(values) == 1 else None,
            "unknown": False,
            "conflicts": conflicts,
            "sources": sorted({p.source for p in rows}),
        }

    def dossier(self, actor: str, *, viewer: str | None = None) -> dict[str, Any]:
        """What one viewer may know about an actor. Fog of war is a first-class parameter."""
        row = self.actors.get(actor)
        if row is None:
            raise SocialModelError(f"unknown actor {actor!r}")
        profile = self.profiles.get(actor) or DiscourseProfile(actor)
        concepts = sorted({p.concept for p in self.positions if p.actor == actor})
        ties = [
            {"with": t.b if t.a == actor else t.a, "kind": t.kind, "event": t.event_id,
             "source": t.source}
            for t in self.ties
            if actor in (t.a, t.b) and (viewer is None or viewer in t.known_by or not t.known_by)
        ]
        memberships = [
            {"organisation": m.organisation, "role": m.role}
            for m in self.affiliations
            if m.actor == actor
        ]
        return {
            "actor": actor,
            "name": row.name,
            "kind": row.kind,
            "aliases": list(row.aliases),
            "profile": asdict(profile),
            "stances": {c: self.stance(actor, c) for c in concepts},
            "ties": ties,
            "memberships": memberships,
        }

    def network(self, actor: str, *, depth: int = 1) -> dict[str, Any]:
        """The observed graph around an actor, by typed ties. No affinity, no ranking."""
        seen = {actor}
        frontier = {actor}
        edges: list[dict[str, Any]] = []
        for _ in range(max(depth, 0)):
            nxt: set[str] = set()
            for tie in self.ties:
                if tie.a in frontier or tie.b in frontier:
                    edges.append({"a": tie.a, "b": tie.b, "kind": tie.kind, "source": tie.source})
                    for node in (tie.a, tie.b):
                        if node not in seen:
                            seen.add(node)
                            nxt.add(node)
            frontier = nxt
        return {"root": actor, "nodes": sorted(seen), "edges": edges}

    # ---- persistence ---------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "actors": [asdict(a) for a in self.actors.values()],
            "affiliations": [asdict(m) for m in self.affiliations],
            "events": [asdict(e) for e in self.events],
            "profiles": {k: asdict(v) for k, v in self.profiles.items()},
            "positions": [asdict(p) for p in self.positions],
            "ties": [asdict(t) for t in self.ties],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SocialWorld":
        version = data.get("schema_version")
        if version != SCHEMA_VERSION:
            raise SocialModelError(f"unsupported social world schema {version!r}")
        world = cls()
        for raw in data.get("actors", []):
            world.actors[raw["id"]] = Actor(**raw)
        world.affiliations = [Affiliation(**raw) for raw in data.get("affiliations", data.get("memberships", []))]
        world.profiles = {k: DiscourseProfile(**v) for k, v in data.get("profiles", {}).items()}
        world.positions = [Position(**raw) for raw in data.get("positions", [])]
        world.ties = [Tie(**raw) for raw in data.get("ties", [])]
        world.events = [Event(**raw) for raw in data.get("events", [])]
        return world

    @classmethod
    def load(cls, path: str) -> "SocialWorld":
        with open(path, encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle))

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")


def ingest_all(world: SocialWorld, events: Iterable[Event]) -> SocialWorld:
    for event in events:
        world.ingest(event)
    return world

def render_dossier(world: "SocialWorld", name: str, *, viewer: str | None = "recruit") -> str:
    """Render one actor's dossier as plain text. Pure, so a test can read what a player would."""
    try:
        actor_id = world.resolve(name)
        dossier = world.dossier(actor_id, viewer=viewer)
    except SocialModelError as exc:
        return f"{exc}. Use 'dossier' for the list."

    profile = dossier["profile"]
    lines = [f"{dossier['name']} ({dossier['kind']})"]
    if profile["values"]:
        lines.append("  values: " + ", ".join(profile["values"]))
    if profile["demands"]:
        lines.append("  demands: " + "; ".join(profile["demands"]))
    if profile["signifiers"]:
        lines.append("  signifiers: " + ", ".join(profile["signifiers"]))
    if profile["goals"]:
        lines.append("  goals: " + ", ".join(profile["goals"]))
    for concept, note in (profile["uncertainty"] or {}).items():
        lines.append(f"  uncertain on {concept}: {note}")

    if dossier["stances"]:
        lines.append("  positions:")
        for concept, stance in dossier["stances"].items():
            if stance["unknown"]:
                lines.append(f"    {concept}: ? (no recorded position)")
            elif stance["conflicts"]:
                lines.append(f"    {concept}: CONFLICT ({len(stance['conflicts'])} claim pair(s))")
            else:
                lines.append(f"    {concept}: {stance['value']:+d} [{', '.join(stance['sources'])}]")
    else:
        lines.append("  positions: none recorded")

    if dossier["ties"]:
        lines.append("  known ties:")
        for tie in dossier["ties"]:
            lines.append(f"    {tie['with']} ({tie['kind']}, {tie['source']})")
    else:
        lines.append("  known ties: none you have been told about")

    return "\n".join(lines)


def render_actor_list(world: "SocialWorld") -> str:
    rows = sorted(world.actors.values(), key=lambda a: (a.kind, a.name))
    lines = ["On record:"]
    for actor in rows:
        known = len([p for p in world.positions if p.actor == actor.id])
        lines.append(f"  {actor.name} ({actor.kind}, {known} recorded position(s))")
    return "\n".join(lines)

