"""LaclauGPT as a NooPunk mod on CWN characters (#1042) — the character-level layer, no LLM required.

Three different questions wear the same word "politics" in a game, and this module keeps them apart on purpose:

* **DA (discourse analysis)** — what an actor *said*: a statement about a signifier, with a stance, a demand
  and a source. Speech is not belief and not truth.
* **DNA (discourse network analysis)** — where actors *stand* relative to concepts: chains of equivalence and
  antagonistic frontiers. Position is not friendship.
* **SNA (social network analysis)** — who actually *knows* whom: ties, trust, debts. Relationship is not
  agreement.

The rule the whole design rests on: none of these may be collapsed into one friend/enemy score. An actor can
share every signifier with you and still be your enemy, and the data model has to be able to say so without a
special case. `Relationship` therefore has no ideological field, and `Statement` has no relationship field.

Deterministic by construction: authored statements in, graph arithmetic out. No model call, no sampling, no
hidden state. Two runs over the same fixtures produce the same numbers, which is what makes a faction's
politics arguable rather than oracular.

CWN is untouched. Nothing here resolves a check, changes an attribute or grants a bonus.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Iterable, Sequence

STANCES = ("support", "oppose", "neutral")
VISIBILITY = ("public", "private", "secret")
ACTOR_KINDS = ("faction", "person", "outlet", "collective")

#: What a claim rests on. An assertion is not evidence and must never be counted as one.
EVIDENCE_KINDS = ("document", "testimony", "observation", "rumour", "assertion")


class IdeologyError(ValueError):
    """A rule was about to be broken: unknown stance, collapsed categories, duplicate ids."""


@dataclass(frozen=True)
class Concept:
    """A signifier. Its meaning is contested by design; the gloss is a label, not a definition."""
    id: str
    gloss: str = ""

    def __post_init__(self):
        if not self.id:
            raise IdeologyError("a concept needs an id")


@dataclass(frozen=True)
class Actor:
    id: str
    kind: str = "faction"
    scope: str = ""          # network this actor speaks within (UNSA, SuomiNet, MarsNet Hype, ...)

    def __post_init__(self):
        if self.kind not in ACTOR_KINDS:
            raise IdeologyError(f"unknown actor kind {self.kind!r}")


@dataclass(frozen=True)
class Statement:
    """One articulation. What was said, about what, on whose authority, at which confidence."""
    actor: str
    concept: str
    stance: str
    demand: str = ""
    source: str = ""
    evidence: str = "assertion"
    confidence: float = 0.5
    visibility: str = "public"
    date: str = ""

    def __post_init__(self):
        if self.stance not in STANCES:
            raise IdeologyError(f"unknown stance {self.stance!r}")
        if self.evidence not in EVIDENCE_KINDS:
            raise IdeologyError(f"unknown evidence kind {self.evidence!r}")
        if not 0.0 <= self.confidence <= 1.0:
            raise IdeologyError("confidence is 0..1")
        if self.visibility not in VISIBILITY:
            raise IdeologyError(f"unknown visibility {self.visibility!r}")

    @property
    def is_evidence_backed(self) -> bool:
        """A rumour is still a claim. Only these kinds may be cited as support in a projection."""
        return self.evidence in ("document", "testimony", "observation")


@dataclass(frozen=True)
class Relationship:
    """SNA. Deliberately has no stance, no concept and no ideology field."""
    a: str
    b: str
    trust: int = 0            # -4..+4, same scale as reputation but a different question
    debt: str = ""            # free text: who owes whom, and what
    visibility: str = "public"

    def __post_init__(self):
        if self.a == self.b:
            raise IdeologyError("a relationship needs two different actors")
        if not -4 <= self.trust <= 4:
            raise IdeologyError("trust is -4..+4")
        if self.visibility not in VISIBILITY:
            raise IdeologyError(f"unknown visibility {self.visibility!r}")


@dataclass
class Discourse:
    """One persistent social/ideological world state."""
    concepts: dict[str, Concept] = field(default_factory=dict)
    actors: dict[str, Actor] = field(default_factory=dict)
    statements: list[Statement] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)

    # ---- authoring -------------------------------------------------------
    def add_concept(self, concept: Concept) -> None:
        if concept.id in self.concepts:
            raise IdeologyError(f"concept {concept.id!r} already exists")
        self.concepts[concept.id] = concept

    def add_actor(self, actor: Actor) -> None:
        if actor.id in self.actors:
            raise IdeologyError(f"actor {actor.id!r} already exists")
        self.actors[actor.id] = actor

    def articulate(self, statement: Statement) -> None:
        if statement.actor not in self.actors:
            raise IdeologyError(f"unknown actor {statement.actor!r}")
        if statement.concept not in self.concepts:
            raise IdeologyError(f"unknown concept {statement.concept!r}")
        self.statements.append(statement)

    def relate(self, relationship: Relationship) -> None:
        for who in (relationship.a, relationship.b):
            if who not in self.actors:
                raise IdeologyError(f"unknown actor {who!r}")
        self.relationships.append(relationship)

    # ---- DNA projections (deterministic) ---------------------------------
    def visible(self, viewer_scope: str, *, shares_secret: bool = False) -> list[Statement]:
        """What a viewer may read.

        Three levels, and the difference between the last two is the point:
        ``public``  — everyone.
        ``private`` — the speaker's own network knows it was said; outsiders do not.
        ``secret``  — need-to-know. Even the speaker's own network does not see it without ``shares_secret``,
                      which is the flag for "someone told you".
        """
        out = []
        for s in self.statements:
            if s.visibility == "public":
                out.append(s)
            elif s.visibility == "private":
                if self.actors[s.actor].scope == viewer_scope:
                    out.append(s)
            elif shares_secret and self.actors[s.actor].scope == viewer_scope:
                out.append(s)
        return out

    def positions(self, *, evidence_only: bool = False) -> dict[str, dict[str, int]]:
        """actor -> concept -> net stance. Weighted by confidence, never by relationship."""
        table: dict[str, dict[str, int]] = {}
        for s in self.statements:
            if evidence_only and not s.is_evidence_backed:
                continue
            weight = 1 if s.stance == "support" else -1 if s.stance == "oppose" else 0
            if weight == 0:
                continue
            row = table.setdefault(s.actor, {})
            row[s.concept] = row.get(s.concept, 0) + weight
        return {actor: dict(sorted(row.items())) for actor, row in sorted(table.items())}

    def contested_concepts(self) -> dict[str, dict[str, list[str]]]:
        """Signifiers claimed by both sides — the most useful object in the system, and the plot engine."""
        out: dict[str, dict[str, list[str]]] = {}
        for concept in sorted(self.concepts):
            supporters, opponents = [], []
            for actor, row in self.positions().items():
                net = row.get(concept, 0)
                if net > 0:
                    supporters.append(actor)
                elif net < 0:
                    opponents.append(actor)
            if supporters and opponents:
                out[concept] = {"support": supporters, "oppose": opponents}
        return out

    def overlap(self, a: str, b: str) -> int:
        """How many signifiers two actors read the same way. Agreement, nothing more."""
        pa, pb = self.positions().get(a, {}), self.positions().get(b, {})
        return sum(1 for c in set(pa) & set(pb) if pa[c] == pb[c] and pa[c] != 0)

    def antagonists_are_not_enemies(self, a: str, b: str) -> dict[str, object]:
        """The separation, made checkable: ideological overlap and personal trust are independent."""
        trust = None
        for r in self.relationships:
            if {r.a, r.b} == {a, b}:
                trust = r.trust
                break
        return {"overlap": self.overlap(a, b), "trust": trust}

    # ---- persistence ------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "concepts": {k: asdict(v) for k, v in sorted(self.concepts.items())},
            "actors": {k: asdict(v) for k, v in sorted(self.actors.items())},
            "statements": [asdict(s) for s in self.statements],
            "relationships": [asdict(r) for r in self.relationships],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Discourse":
        d = cls(
            concepts={k: Concept(**v) for k, v in (data.get("concepts") or {}).items()},
            actors={k: Actor(**v) for k, v in (data.get("actors") or {}).items()},
            statements=[Statement(**s) for s in data.get("statements", [])],
            relationships=[Relationship(**r) for r in data.get("relationships", [])],
        )
        return d
