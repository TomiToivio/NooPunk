"""LaclauGPT as a CWN character-level mod: DA, DNA and SNA kept as three separate layers (#1042).

The mod adds a social/ideological world model beside the locked CWN rules; it never changes them.
Its whole point is that three things the table usually collapses into one "friend/enemy" score stay
distinct:

* **DA — discourse analysis.** One actor's ideology: identities, values, demands, signifiers,
  antagonisms and goals (personal, institutional, ideological), versioned and dated. A faction's
  discourse is not the average of its members, so profiles belong to actors, not to groups.
* **DNA — discourse network analysis.** Explicit, dated ``Stance`` statements: actor → concept, with
  a polarity of support / oppose / uncertain. Disagreement is not hostility, and agreement is not
  trust: nothing here writes a tie.
* **SNA — social network analysis.** ``Tie`` records what was *observed* (talked to, met, is a member
  of). Trust, access and reputation are ``GameRelation`` game state, set by play, never derived from
  a tie or a stance.

Every row carries its provenance, because the issue requires evidence, fiction and game outcome to
stay distinguishable: a transcript-backed statement, an LLM-authored line and a consequence the engine
resolved are three different kinds of fact. Derived questions ("do these two agree?") return ``None``
rather than a number when the evidence does not exist — no evidence is not neutrality.

Deterministic by construction: no randomness, no LLM calls, explicit ids and dates, and a snapshot that
round-trips through JSON for Evennia persistence.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum

#: Bumped whenever the snapshot shape changes; the loader refuses unknown versions.
SCHEMA_VERSION = 1


class SocialModelError(ValueError):
    pass


class Provenance(str, Enum):
    """Where a fact came from. The distinction is the issue's core requirement, not decoration."""

    EVIDENCE = "evidence"      # a captured statement, document, or observed interaction
    FICTION = "fiction"        # written or LLM-authored text; interpretation, not measurement
    OUTCOME = "outcome"        # the rules resolved something (a check, a faction action)


class Polarity(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    UNCERTAIN = "uncertain"


class GoalKind(str, Enum):
    PERSONAL = "personal"
    INSTITUTIONAL = "institutional"
    IDEOLOGICAL = "ideological"


class TieKind(str, Enum):
    COMMUNICATION = "communication"
    AFFILIATION = "affiliation"
    PERSONAL = "personal"


def _require_id(value: str, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SocialModelError(f"{what} needs a stable id")
    return value.strip()


def _require_day(value: str) -> str:
    """Dates are ISO ``YYYY-MM-DD`` strings: sortable, timezone-free and readable in game logs."""
    if not isinstance(value, str) or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise SocialModelError("dates are ISO YYYY-MM-DD")
    return value


@dataclass(frozen=True)
class Concept:
    """A signifier an actor can take a stance on. ``chain`` groups equivalents (Laclau)."""

    identifier: str
    label: str
    chain: str = ""

    def __post_init__(self) -> None:
        _require_id(self.identifier, "concept")
        if not self.label.strip():
            raise SocialModelError("concept needs a label")


@dataclass(frozen=True)
class Stance:
    """One DNA statement. ``minimum_rank``-style gating belongs to the caller, not here."""

    actor: str
    concept: str
    polarity: Polarity
    on: str
    provenance: Provenance
    event: str = ""
    note: str = ""

    def __post_init__(self) -> None:
        _require_id(self.actor, "stance actor")
        _require_id(self.concept, "stance concept")
        _require_day(self.on)
        if not isinstance(self.polarity, Polarity):
            raise SocialModelError("polarity must be support, oppose or uncertain")


@dataclass(frozen=True)
class Tie:
    """What was observed, not what it means. Trust lives in :class:`GameRelation`."""

    source: str
    target: str
    kind: TieKind
    since: str
    provenance: Provenance
    directed: bool = True

    def __post_init__(self) -> None:
        _require_id(self.source, "tie source")
        _require_id(self.target, "tie target")
        _require_day(self.since)
        if self.source == self.target:
            raise SocialModelError("a tie needs two different actors")
        if not isinstance(self.kind, TieKind):
            raise SocialModelError("unknown tie kind")

    def connects(self, a: str, b: str) -> bool:
        return (self.source, self.target) == (a, b) or (
            not self.directed and (self.source, self.target) == (b, a))


@dataclass
class DiscourseProfile:
    """The DA layer for one actor, versioned. Empty lists are a real answer: nothing recorded yet."""

    actor: str
    version: int = 1
    identities: list[str] = field(default_factory=list)
    values: list[str] = field(default_factory=list)
    demands: list[str] = field(default_factory=list)
    signifiers: list[str] = field(default_factory=list)
    antagonisms: list[str] = field(default_factory=list)
    goals: dict[GoalKind, list[str]] = field(default_factory=dict)
    on: str = "1970-01-01"
    provenance: Provenance = Provenance.FICTION

    def __post_init__(self) -> None:
        _require_id(self.actor, "profile actor")
        _require_day(self.on)

    def goal(self, kind: GoalKind) -> tuple[str, ...]:
        return tuple(self.goals.get(kind, ()))

    def revise(self, on: str, *, identities: list[str] | None = None,
               values: list[str] | None = None, demands: list[str] | None = None,
               signifiers: list[str] | None = None, antagonisms: list[str] | None = None,
               goals: dict[GoalKind, list[str]] | None = None,
               provenance: Provenance | None = None) -> DiscourseProfile:
        """Return the next version; profiles are append-only so an ideological shift stays traceable."""
        return DiscourseProfile(
            actor=self.actor,
            version=self.version + 1,
            identities=list(identities if identities is not None else self.identities),
            values=list(values if values is not None else self.values),
            demands=list(demands if demands is not None else self.demands),
            signifiers=list(signifiers if signifiers is not None else self.signifiers),
            antagonisms=list(antagonisms if antagonisms is not None else self.antagonisms),
            goals=dict(goals if goals is not None else self.goals),
            on=_require_day(on),
            provenance=Provenance(provenance if provenance is not None else self.provenance),
        )


@dataclass
class GameRelation:
    """Trust, access and reputation are game state: play sets them, nothing infers them."""

    trust: int = 0
    access: int = 0
    reputation: int = 0

    def adjust(self, **deltas: int) -> None:
        for key, delta in deltas.items():
            if key not in ("trust", "access", "reputation"):
                raise SocialModelError(f"unknown relation axis {key!r}")
            if type(delta) is not int:
                raise SocialModelError("relation changes are whole numbers")
            setattr(self, key, getattr(self, key) + delta)


@dataclass(frozen=True)
class Compatibility:
    """DNA-only overlap. ``score`` is ``None`` when the two actors share no stated concept."""

    shared: int
    agree: int
    disagree: int
    uncertain: int
    score: float | None

    @property
    def has_evidence(self) -> bool:
        return self.score is not None


class SocialWorld:
    """The persistent world state behind DA, DNA and SNA — one object, three separate layers."""

    def __init__(self) -> None:
        self.actors: dict[str, dict] = {}
        self.concepts: dict[str, Concept] = {}
        self.profiles: dict[str, DiscourseProfile] = {}
        self.stances: list[Stance] = []
        self.ties: list[Tie] = []
        self.relations: dict[tuple[str, str], GameRelation] = {}
        self.events: list[dict] = []
        self._event_seq = 0

    # -- registration -----------------------------------------------------------------
    def add_actor(self, identifier: str, *, name: str = "", faction: str = "",
                  provenance: Provenance = Provenance.FICTION, on: str = "1970-01-01") -> dict:
        identifier = _require_id(identifier, "actor")
        if identifier in self.actors:
            raise SocialModelError(f"actor {identifier!r} already exists")
        _require_day(on)
        record = {"id": identifier, "name": name or identifier, "faction": faction,
                  "provenance": Provenance(provenance).value, "since": on}
        self.actors[identifier] = record
        self._log("actor.added", identifier, on, Provenance(provenance))
        return record

    def add_concept(self, concept: Concept) -> Concept:
        if concept.identifier in self.concepts:
            raise SocialModelError(f"concept {concept.identifier!r} already exists")
        self.concepts[concept.identifier] = concept
        return concept

    def set_profile(self, profile: DiscourseProfile) -> DiscourseProfile:
        if profile.actor not in self.actors:
            raise SocialModelError("profile actor is not registered")
        current = self.profiles.get(profile.actor)
        if current is not None and profile.version != current.version + 1:
            raise SocialModelError("a profile revision must be the next version")
        if current is not None and profile.on < current.on:
            raise SocialModelError("a profile revision cannot predate the version it replaces")
        self.profiles[profile.actor] = profile
        self._log("profile.set", profile.actor, profile.on, profile.provenance, version=profile.version)
        return profile

    # -- DNA --------------------------------------------------------------------------
    def record_stance(self, stance: Stance) -> Stance:
        if stance.actor not in self.actors:
            raise SocialModelError("stance actor is not registered")
        if stance.concept not in self.concepts:
            raise SocialModelError("stance concept is not registered")
        # Superseding is by date: the latest statement about a concept wins, older ones stay readable.
        self.stances.append(stance)
        self._log("stance.recorded", stance.actor, stance.on, stance.provenance,
                  concept=stance.concept, polarity=stance.polarity.value)
        return stance

    def stance(self, actor: str, concept: str, on_or_before: str | None = None) -> Stance | None:
        """The actor's latest statement, optionally as of a date — this is how shifts stay honest."""
        found = [s for s in self.stances if s.actor == actor and s.concept == concept
                 and (on_or_before is None or s.on <= on_or_before)]
        return max(found, key=lambda s: (s.on, self.stances.index(s))) if found else None

    def compatibility(self, a: str, b: str, on: str | None = None) -> Compatibility:
        """Agreement over stated concepts. Deliberately silent about friendship (see docstring)."""
        shared = agree = disagree = uncertain = 0
        for concept_id in sorted(self.concepts):
            left, right = self.stance(a, concept_id, on), self.stance(b, concept_id, on)
            if left is None or right is None:
                continue
            shared += 1
            if Polarity.UNCERTAIN in (left.polarity, right.polarity):
                uncertain += 1
            elif left.polarity == right.polarity:
                agree += 1
            else:
                disagree += 1
        decided = agree + disagree
        score = round((agree - disagree) / decided, 3) if decided else None
        return Compatibility(shared=shared, agree=agree, disagree=disagree,
                              uncertain=uncertain, score=score)

    # -- SNA --------------------------------------------------------------------------
    def record_tie(self, tie: Tie) -> Tie:
        for actor in (tie.source, tie.target):
            if actor not in self.actors:
                raise SocialModelError(f"tie actor {actor!r} is not registered")
        self.ties.append(tie)
        self._log("tie.recorded", tie.source, tie.since, tie.provenance,
                  target=tie.target, tie_kind=tie.kind.value)
        return tie

    def ties_of(self, actor: str, kind: TieKind | None = None) -> tuple[Tie, ...]:
        return tuple(t for t in self.ties if (t.source == actor or (not t.directed and t.target == actor))
                     and (kind is None or t.kind == kind))

    def relation(self, a: str, b: str, *, create: bool = False) -> GameRelation | None:
        key = (a, b)
        if key not in self.relations:
            if not create:
                return None
            self.relations[key] = GameRelation()
        return self.relations[key]

    def adjust_relation(self, a: str, b: str, **deltas: int) -> GameRelation:
        relation = self.relation(a, b, create=True)
        assert relation is not None
        relation.adjust(**deltas)
        self._log("relation.adjusted", a, self._today(), Provenance.OUTCOME, target=b, **deltas)
        return relation

    # -- what an NPC decides with ------------------------------------------------------
    def decision_context(self, actor: str, concept: str | None = None) -> dict:
        """The inputs an NPC's reaction is allowed to use, each labelled by its layer.

        The caller (dialogue, investigation, faction turn) decides the outcome; this only assembles
        evidence. Keep ideology and relationships apart downstream or the mod has no reason to exist.
        """
        if actor not in self.actors:
            raise SocialModelError("unknown actor")
        profile = self.profiles.get(actor)
        context: dict = {
            "actor": self.actors[actor]["name"],
            "faction": self.actors[actor]["faction"],
            "ideology": None,
            "stance": None,
            "ties": [t.target if t.source == actor else t.source for t in self.ties_of(actor)],
            "relations": {},
        }
        if profile is not None:
            context["ideology"] = {
                "identities": list(profile.identities),
                "values": list(profile.values),
                "demands": list(profile.demands),
                "signifiers": list(profile.signifiers),
                "antagonisms": list(profile.antagonisms),
                "goals": {kind.value: list(values) for kind, values in profile.goals.items()},
            }
        if concept is not None:
            stance = self.stance(actor, concept)
            context["stance"] = None if stance is None else {
                "concept": stance.concept, "polarity": stance.polarity.value,
                "on": stance.on, "provenance": stance.provenance.value,
            }
        for (left, right), relation in self.relations.items():
            if actor in (left, right):
                other = right if left == actor else left
                context["relations"][other] = {"trust": relation.trust,
                                               "access": relation.access,
                                               "reputation": relation.reputation}
        return context

    # -- persistence -------------------------------------------------------------------
    def snapshot(self) -> dict:
        return {
            "schema": SCHEMA_VERSION,
            "actors": self.actors,
            "concepts": {k: vars(v) for k, v in self.concepts.items()},
            "profiles": [
                {**vars(p), "provenance": p.provenance.value,
                 "goals": {k.value: list(v) for k, v in p.goals.items()}}
                for p in self.profiles.values()
            ],
            "stances": [{**vars(s), "polarity": s.polarity.value, "provenance": s.provenance.value}
                        for s in self.stances],
            "ties": [{**vars(t), "kind": t.kind.value, "provenance": t.provenance.value}
                     for t in self.ties],
            "relations": [{"a": a, "b": b, **vars(r)} for (a, b), r in self.relations.items()],
            "events": self.events,
        }

    def to_json(self) -> str:
        return json.dumps(self.snapshot(), indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> SocialWorld:
        return cls.from_snapshot(json.loads(text))

    @classmethod
    def from_snapshot(cls, state: dict) -> SocialWorld:
        if state.get("schema") != SCHEMA_VERSION:
            raise SocialModelError(f"unsupported schema version {state.get('schema')!r}")
        world = cls()
        world.actors = dict(state["actors"])
        world.concepts = {k: Concept(**v) for k, v in state["concepts"].items()}
        for raw in state["profiles"]:
            data = dict(raw)
            data["goals"] = {GoalKind(k): list(v) for k, v in data["goals"].items()}
            data["provenance"] = Provenance(data["provenance"])
            world.profiles[data["actor"]] = DiscourseProfile(**data)
        world.stances = [Stance(**{**raw, "polarity": Polarity(raw["polarity"]),
                                   "provenance": Provenance(raw["provenance"])})
                         for raw in state["stances"]]
        world.ties = [Tie(**{**raw, "kind": TieKind(raw["kind"]),
                             "provenance": Provenance(raw["provenance"])})
                      for raw in state["ties"]]
        world.relations = {(raw["a"], raw["b"]): GameRelation(trust=raw["trust"],
                                                              access=raw["access"],
                                                              reputation=raw["reputation"])
                           for raw in state["relations"]}
        world.events = list(state["events"])
        world._event_seq = len(world.events)
        return world

    # -- internals --------------------------------------------------------------------
    def _log(self, event: str, subject: str, on: str, provenance: Provenance, **detail) -> None:
        self._event_seq += 1
        self.events.append({"seq": self._event_seq, "kind": event, "subject": subject,
                            "on": on, "provenance": Provenance(provenance).value, **detail})

    def _today(self) -> str:
        return self.events[-1]["on"] if self.events else "1970-01-01"
