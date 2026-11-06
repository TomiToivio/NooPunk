"""A standalone computational social-science simulator kernel (#1286).

NoöPunk's RPG is frozen this phase, so nothing here imports it: no `rules`, no `world`, no `console`, no `simulation`,
no engine, no CWN. The simulator runs from Python with synthetic fixtures, fixed seeds and a step clock, and it is
inspectable: every event names the rule that produced it and the inputs it consumed.

The scientific boundary the kernel enforces:

* **four kinds of material stay apart** — `observed`, `inferred`, `synthesized`, `simulated` — and every record carries
  one, so an export cannot quietly mix a corpus fact with a synthetic disposition;
* **no fabricated evidence** — an event must cite a rule from the registry, and a rule must exist for its name;
* **no agent-level LLM** — the kernel calls no provider and has no network code;
* **no predictive claim** — a run explores the consequences of stated assumptions.

Work package 1 of #1286. The contracts it consumes are described in `docs/simulator/BOUNDARY_AND_CONTRACTS_1286.md`.
"""
from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Sequence

__all__ = [
    "Actor",
    "ActorKind",
    "CommunicationEdge",
    "Event",
    "EventKind",
    "KernelError",
    "Origin",
    "Provenance",
    "Simulation",
    "SocialEdge",
    "broadcast",
    "noop",
]

KERNEL_VERSION = 1


class KernelError(ValueError):
    """A population, edge or rule the kernel refuses rather than guessing at."""


class Origin(str, Enum):
    """Where a value came from. The four are never merged into one another (#1286 §the four kinds of material)."""

    OBSERVED = "observed"        # taken from AI26 output exactly
    INFERRED = "inferred"        # analysis or researcher judgement over observed material
    SYNTHESIZED = "synthesized"  # invented for a scenario
    SIMULATED = "simulated"      # produced by the simulator's rules


@dataclass(frozen=True, slots=True)
class Provenance:
    """Who says this, how, and how sure they are. Survives every round trip."""

    origin: Origin
    source: str = ""
    method: str = ""
    uncertainty: str = ""
    review_status: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "origin": self.origin.value,
            "source": self.source,
            "method": self.method,
            "uncertainty": self.uncertainty,
            "review_status": self.review_status,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "Provenance":
        try:
            origin = Origin(str(payload["origin"]))
        except (KeyError, ValueError) as exc:
            raise KernelError(f"unreadable provenance origin in {payload!r}") from exc
        return cls(
            origin=origin,
            source=str(payload.get("source") or ""),
            method=str(payload.get("method") or ""),
            uncertainty=str(payload.get("uncertainty") or ""),
            review_status=str(payload.get("review_status") or ""),
        )


class ActorKind(str, Enum):
    """Individuals and organizations are different actor types, never folded together (#1286)."""

    INDIVIDUAL = "individual"
    ORGANIZATION = "organization"


@dataclass(frozen=True, slots=True)
class Actor:
    """A synthetic social actor.

    ``affiliation`` links an individual to an organization *by id*; the kernel refuses a dangling affiliation. The
    attributes are simulation variables, and explicitly **not** NoöPunk RPG tags.
    """

    id: str
    kind: ActorKind = ActorKind.INDIVIDUAL
    affiliation: str = ""
    role: str = ""
    resources: float = 0.0
    attributes: tuple[tuple[str, float], ...] = ()
    provenance: Provenance = field(default_factory=lambda: Provenance(Origin.SYNTHESIZED))

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise KernelError("an actor needs an id")
        if self.resources < 0:
            raise KernelError(f"actor {self.id!r} cannot hold negative resources")

    def attribute(self, name: str, default: float = 0.0) -> float:
        return dict(self.attributes).get(name, default)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "kind": self.kind.value,
            "affiliation": self.affiliation,
            "role": self.role,
            "resources": self.resources,
            "attributes": dict(sorted(self.attributes)),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "Actor":
        return cls(
            id=str(payload["id"]),
            kind=ActorKind(str(payload.get("kind") or ActorKind.INDIVIDUAL.value)),
            affiliation=str(payload.get("affiliation") or ""),
            role=str(payload.get("role") or ""),
            resources=float(payload.get("resources") or 0.0),
            attributes=tuple(sorted((str(k), float(v)) for k, v in dict(payload.get("attributes") or {}).items())),
            provenance=Provenance.from_dict(dict(payload.get("provenance") or {"origin": Origin.SYNTHESIZED.value})),
        )


@dataclass(frozen=True, slots=True)
class SocialEdge:
    """A typed, time-indexed tie between two actors (#1286 relational layer)."""

    source: str
    target: str
    relation: str
    since_step: int = 0
    provenance: Provenance = field(default_factory=lambda: Provenance(Origin.SYNTHESIZED))

    def __post_init__(self) -> None:
        if not self.relation.strip():
            raise KernelError("a social edge needs a relation name")
        if self.since_step < 0:
            raise KernelError("a tie cannot start before step 0")

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source, "target": self.target, "relation": self.relation,
            "since_step": self.since_step, "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "SocialEdge":
        return cls(
            source=str(payload["source"]), target=str(payload["target"]),
            relation=str(payload["relation"]), since_step=int(payload.get("since_step") or 0),
            provenance=Provenance.from_dict(dict(payload.get("provenance") or {"origin": Origin.SYNTHESIZED.value})),
        )


@dataclass(frozen=True, slots=True)
class CommunicationEdge:
    """One communication event as an edge: who spoke to whom, when, on what channel."""

    source: str
    target: str
    at_step: int
    channel: str = "social_tie"
    provenance: Provenance = field(default_factory=lambda: Provenance(Origin.SIMULATED))

    def __post_init__(self) -> None:
        if self.at_step < 0:
            raise KernelError("a communication cannot happen before step 0")
        if not self.channel.strip():
            raise KernelError("a communication needs a channel")

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source, "target": self.target, "at_step": self.at_step,
            "channel": self.channel, "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "CommunicationEdge":
        return cls(
            source=str(payload["source"]), target=str(payload["target"]),
            at_step=int(payload["at_step"]), channel=str(payload.get("channel") or "social_tie"),
            provenance=Provenance.from_dict(dict(payload.get("provenance") or {"origin": Origin.SIMULATED.value})),
        )


class EventKind(str, Enum):
    """The event vocabulary #1286 names. Open by construction: a new kind is a new member, never a free string."""

    COMMUNICATE = "communicate"
    RESPOND = "respond"
    AFFILIATE = "affiliate"
    DISAFFILIATE = "disaffiliate"
    SUPPORT = "support"
    CONTEST = "contest"
    LINK_DEMANDS = "link_demands"
    SEPARATE_DEMANDS = "separate_demands"
    RESOURCE_CHANGE = "resource_change"
    ATTENTION_CHANGE = "attention_change"


@dataclass(frozen=True, slots=True)
class Event:
    """One thing that happened, with the rule that caused it and the inputs it read.

    ``event_id`` is derived from the event's own content plus its sequence number, so two runs with the same seed and
    inputs produce byte-identical streams, and a duplicated event is detectable without a central counter.
    """

    step: int
    sequence: int
    kind: EventKind
    actor: str
    target: str = ""
    rule: str = ""
    inputs: tuple[str, ...] = ()
    payload: tuple[tuple[str, str], ...] = ()
    provenance: Provenance = field(default_factory=lambda: Provenance(Origin.SIMULATED))

    def __post_init__(self) -> None:
        if self.step < 0 or self.sequence < 0:
            raise KernelError("an event needs a non-negative step and sequence")
        if not self.actor.strip():
            raise KernelError("an event needs an actor")
        if not self.rule.strip():
            raise KernelError("an event must cite the rule that produced it")
        if self.provenance.origin is not Origin.SIMULATED:
            raise KernelError("simulator events are 'simulated'; observed material enters as records, not events")

    @property
    def event_id(self) -> str:
        blob = json.dumps(
            {
                "step": self.step, "sequence": self.sequence, "kind": self.kind.value, "actor": self.actor,
                "target": self.target, "rule": self.rule, "inputs": list(self.inputs),
                "payload": dict(self.payload),
            },
            sort_keys=True, ensure_ascii=False,
        )
        return "evt-" + hashlib.sha256(blob.encode("utf-8")).hexdigest()[:24]

    def to_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id, "step": self.step, "sequence": self.sequence,
            "kind": self.kind.value, "actor": self.actor, "target": self.target, "rule": self.rule,
            "inputs": list(self.inputs), "payload": dict(self.payload),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "Event":
        return cls(
            step=int(payload["step"]), sequence=int(payload["sequence"]), kind=EventKind(str(payload["kind"])),
            actor=str(payload["actor"]), target=str(payload.get("target") or ""), rule=str(payload["rule"]),
            inputs=tuple(str(i) for i in payload.get("inputs") or ()),
            payload=tuple(sorted((str(k), str(v)) for k, v in dict(payload.get("payload") or {}).items())),
            provenance=Provenance.from_dict(dict(payload.get("provenance") or {"origin": Origin.SIMULATED.value})),
        )


# --------------------------------------------------------------------------- #
# Rules: documented assumptions, one function each
# --------------------------------------------------------------------------- #

def noop(_state: "Simulation", _rng: random.Random, _step: int) -> tuple[tuple[str, str], ...]:
    """The do-nothing rule. Present so a run can be shown to be genuinely empty rather than merely quiet."""
    return ()


def broadcast(state: "Simulation", rng: random.Random, step: int) -> tuple[tuple[str, str], ...]:
    """One speaker per step, chosen from actors that have at least one social tie.

    **Assumption, stated plainly:** a simulated population talks along its existing ties, at a rate of one message per
    step, with the speaker chosen uniformly among actors that have a tie. That is a modelling choice for the kernel to
    have *a* transition, not a claim that discourse works this way. A scenario that wants different behaviour supplies
    its own rule and documents it.

    Returns ``(speaker, listener)`` pairs; the kernel turns each into a :class:`CommunicationEdge` and an
    :class:`Event`.
    """
    connected = sorted(
        actor.id for actor in state.actors.values()
        if any(edge.source == actor.id for edge in state.social)
    )
    if not connected:
        return ()
    speaker = connected[rng.randrange(len(connected))]
    neighbours = sorted(edge.target for edge in state.social if edge.source == speaker)
    if not neighbours:
        return ()
    listener = neighbours[rng.randrange(len(neighbours))]
    return ((speaker, listener),)


#: The rule registry. A name outside it is refused, so a run cannot cite a rule that does not exist.
RULES = {"noop": noop, "broadcast": broadcast}


def resolve_rule(name: str):
    """The rule function for ``name``; refuses an unknown name instead of inventing behaviour."""
    try:
        return RULES[name]
    except KeyError as exc:
        raise KernelError(f"no rule named {name!r}; known rules: {sorted(RULES)}") from exc


# --------------------------------------------------------------------------- #
# The simulation
# --------------------------------------------------------------------------- #

@dataclass
class Simulation:
    """A synthetic population, its ties, and the events a rule produces over it."""

    actors: dict[str, Actor] = field(default_factory=dict)
    social: list[SocialEdge] = field(default_factory=list)
    communication: list[CommunicationEdge] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    step: int = 0
    seed: int = 0
    rules_used: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        for actor_id, actor in self.actors.items():
            if actor_id != actor.id:
                raise KernelError(f"actor registered as {actor_id!r} but carries id {actor.id!r}")
            if actor.affiliation and actor.affiliation not in self.actors:
                raise KernelError(f"{actor.id!r} is affiliated to unknown actor {actor.affiliation!r}")
            if actor.affiliation and self.actors[actor.affiliation].kind is not ActorKind.ORGANIZATION:
                raise KernelError(f"{actor.id!r} is affiliated to {actor.affiliation!r}, which is not an organization")
        for edge in self.social:
            for endpoint in (edge.source, edge.target):
                if endpoint not in self.actors:
                    raise KernelError(f"social edge {edge.source!r}→{edge.target!r} names unknown actor {endpoint!r}")

    # -- population --------------------------------------------------------------------------- #
    def add_actor(self, actor: Actor) -> Actor:
        if actor.id in self.actors:
            raise KernelError(f"duplicate actor id {actor.id!r}")
        self.actors[actor.id] = actor
        self.__post_init__()
        return actor

    def add_social_edge(self, edge: SocialEdge) -> SocialEdge:
        self.social.append(edge)
        self.__post_init__()
        return edge

    def neighbours(self, actor_id: str) -> tuple[str, ...]:
        """Outgoing ties of one actor, sorted so a caller cannot depend on insertion order."""
        return tuple(sorted(edge.target for edge in self.social if edge.source == actor_id))

    def isolated(self) -> tuple[str, ...]:
        """Actors with no ties at all, in or out. They are legitimate; the kernel does not delete them."""
        involved = {endpoint for edge in self.social for endpoint in (edge.source, edge.target)}
        return tuple(sorted(actor_id for actor_id in self.actors if actor_id not in involved))

    # -- running ------------------------------------------------------------------------------ #
    def run(self, steps: int, *, rule: str = "broadcast") -> tuple[Event, ...]:
        """Advance ``steps`` steps under one named rule; returns the events produced in this call.

        Determinism: each step's generator is seeded from ``(seed, step, rule)``, so a continuous run and a resumed one
        produce identical streams, and no generator state needs to be saved.
        """
        if steps < 0:
            raise KernelError("steps cannot be negative")
        function = resolve_rule(rule)
        if rule not in self.rules_used:
            self.rules_used.append(rule)
        produced: list[Event] = []
        for _ in range(steps):
            self.step += 1
            # Seeded per step, not per call: a run of ten and two runs of five must produce the same stream, which is
            # what makes a resumed save equal to an uninterrupted one. `Random` accepts str/bytes/int, not a tuple.
            rng = random.Random(f"{self.seed}:{self.step}:{rule}")
            for speaker, listener in function(self, rng, self.step):
                if speaker not in self.actors or listener not in self.actors:
                    raise KernelError(f"rule {rule!r} produced an unknown actor pair {speaker!r}→{listener!r}")
                self.communication.append(CommunicationEdge(
                    source=speaker, target=listener, at_step=self.step, channel="social_tie",
                ))
                event = Event(
                    step=self.step, sequence=len(self.events), kind=EventKind.COMMUNICATE,
                    actor=speaker, target=listener, rule=rule, inputs=(f"tie:{speaker}->{listener}",),
                    payload=(("channel", "social_tie"),),
                )
                self.events.append(event)
                produced.append(event)
        return tuple(produced)

    # -- reproducibility ---------------------------------------------------------------------- #
    def digest(self) -> str:
        """A stable hash of the event stream: the acceptance test's 'output hash'."""
        blob = json.dumps([event.to_dict() for event in self.events], sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def snapshot(self) -> dict[str, object]:
        """Everything needed to resume or reproduce the run, in one JSON-safe document."""
        return {
            "kernel_version": KERNEL_VERSION,
            "step": self.step,
            "seed": self.seed,
            "rules_used": list(self.rules_used),
            "actors": [self.actors[key].to_dict() for key in sorted(self.actors)],
            "social": [edge.to_dict() for edge in self.social],
            "communication": [edge.to_dict() for edge in self.communication],
            "events": [event.to_dict() for event in self.events],
            "digest": self.digest(),
        }

    @classmethod
    def from_snapshot(cls, payload: Mapping[str, object]) -> "Simulation":
        """Rebuild a run from its snapshot. A version or digest mismatch is refused, not repaired."""
        if int(payload.get("kernel_version") or 0) != KERNEL_VERSION:
            raise KernelError(f"unsupported kernel version {payload.get('kernel_version')!r}")
        simulation = cls(seed=int(payload.get("seed") or 0))
        for raw in payload.get("actors") or ():
            actor = Actor.from_dict(raw)
            simulation.actors[actor.id] = actor
        simulation.social = [SocialEdge.from_dict(raw) for raw in payload.get("social") or ()]
        simulation.communication = [CommunicationEdge.from_dict(raw) for raw in payload.get("communication") or ()]
        simulation.events = [Event.from_dict(raw) for raw in payload.get("events") or ()]
        simulation.step = int(payload.get("step") or 0)
        simulation.rules_used = [str(name) for name in payload.get("rules_used") or ()]
        simulation.__post_init__()
        if "digest" in payload and simulation.digest() != payload["digest"]:
            raise KernelError("snapshot digest does not match its event stream")
        return simulation


def build(actors: Iterable[Actor], edges: Iterable[SocialEdge] = (), *, seed: int = 0) -> Simulation:
    """Convenience constructor: validate a population and its ties in one call."""
    simulation = Simulation(seed=seed)
    for actor in actors:
        simulation.actors[actor.id] = actor
    simulation.social = list(edges)
    simulation.__post_init__()
    return simulation
