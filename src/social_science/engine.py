"""Deterministic social-science simulation kernel (#1286).

The kernel contains **no LLM roleplay and no RPG mechanics**. It applies a small,
documented set of behavioral assumptions to synthetic actors and explicit claims:
communication, influence, affiliation/coalition formation, contestation and a
simple institutional response. Every transition is seeded, logged with the rule
that produced it, and exported with its provenance.

The rules are deliberately modest. They are a research instrument, not a claim
that Laclau and Mouffe's concepts are causal variables or that a simulation
predicts real politics.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from .events import EventLog, SimEvent
from .model import (
    Actor,
    Articulation,
    Claim,
    CommunicationEdge,
    Material,
    Provenance,
    SimulationConfig,
    SocialEdge,
)

__all__ = ["DEFAULT_RULES", "SimulationError", "SocialScienceSimulation"]

#: Human-readable statement of the MVP assumptions. The code below implements
#: exactly these; a change here is a modelling change and must be reported.
DEFAULT_RULES: Mapping[str, str] = {
    "communication": "An active actor with at least one outgoing social tie may communicate one claim per turn with probability communication_probability; otherwise it abstains.",
    "influence": "A receiver moves its disposition toward a claim by influence_rate times the sender's stance sign; dispositions are bounded to [-1, 1].",
    "attention": "A receiver's attention rises by 0.10 after a communication and decays by attention_decay each turn, bounded to [0, 1].",
    "coalition": "When a receiver's disposition toward a claim crosses coalition_threshold, a simulated 'coalition' social edge is recorded once.",
    "contest": "When sender and receiver have opposite-sign dispositions beyond the coalition threshold, the receiver records a contest event.",
    "institution": "An organization whose attention is at least institutional_threshold records one institutional_response per turn; this is an attention heuristic, not a decision procedure.",
    "abstention": "No target, a failed communication draw, or the abstention draw produces an abstain event rather than a fabricated message.",
}


class SimulationError(ValueError):
    """The run is malformed or an input cannot be represented honestly."""


def _clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


@dataclass
class SocialScienceSimulation:
    """One synthetic run over actors, claims and social ties."""

    config: SimulationConfig = field(default_factory=SimulationConfig)
    actors: dict[str, Actor] = field(default_factory=dict)
    claims: dict[str, Claim] = field(default_factory=dict)
    articulations: dict[str, Articulation] = field(default_factory=dict)
    social_edges: list[SocialEdge] = field(default_factory=list)
    communication_edges: list[CommunicationEdge] = field(default_factory=list)
    log: EventLog = field(default_factory=EventLog)
    turn: int = 0
    _rng: random.Random = field(init=False, repr=False)
    _institutional_this_turn: set[str] = field(
        default_factory=set, init=False, repr=False
    )

    def __post_init__(self) -> None:
        self._rng = random.Random(self.config.seed)
        for actor in self.actors.values():
            self._require_actor(actor.id)
        for edge in self.social_edges:
            self._require_actor(edge.source)
            self._require_actor(edge.target)
        for claim in self.claims.values():
            if not claim.id.strip():
                raise SimulationError("claim id must be non-empty")
        for articulation in self.articulations.values():
            if (
                articulation.left not in self.claims
                or articulation.right not in self.claims
            ):
                raise SimulationError("articulation endpoints must be known claims")

    # -- construction -------------------------------------------------------------------------- #
    def add_actor(self, actor: Actor) -> Actor:
        if actor.id in self.actors:
            raise SimulationError(f"duplicate actor id {actor.id!r}")
        self.actors[actor.id] = actor
        return actor

    def add_claim(self, claim: Claim) -> Claim:
        if claim.id in self.claims:
            raise SimulationError(f"duplicate claim id {claim.id!r}")
        self.claims[claim.id] = claim
        return claim

    def add_articulation(self, articulation: Articulation) -> Articulation:
        self._require_claim(articulation.left)
        self._require_claim(articulation.right)
        if articulation.id in self.articulations:
            raise SimulationError(f"duplicate articulation id {articulation.id!r}")
        self.articulations[articulation.id] = articulation
        return articulation

    def add_social_edge(self, edge: SocialEdge) -> SocialEdge:
        self._require_actor(edge.source)
        self._require_actor(edge.target)
        key = (edge.source, edge.target, edge.relation, edge.time)
        if any(
            (e.source, e.target, e.relation, e.time) == key for e in self.social_edges
        ):
            raise SimulationError("duplicate social edge")
        self.social_edges.append(edge)
        return edge

    # -- simulation ---------------------------------------------------------------------------- #
    def step(self) -> list[SimEvent]:
        """Advance one turn under :data:`DEFAULT_RULES`."""
        self._decay_attention()
        self._institutional_this_turn.clear()
        emitted: list[SimEvent] = []
        if not self.claims:
            for actor in self._sorted_actors():
                emitted.append(
                    self._emit(
                        "abstain",
                        actor.id,
                        "",
                        {"reason": "no claims in scenario"},
                        "abstention",
                    )
                )
            self.turn += 1
            return emitted
        organizations = [a for a in self._sorted_actors() if a.kind == "organization"]
        for actor in self._sorted_actors():
            if not actor.active:
                continue
            targets = sorted(
                {edge.target for edge in self.social_edges if edge.source == actor.id}
            )
            if not targets:
                emitted.append(
                    self._emit(
                        "abstain",
                        actor.id,
                        "",
                        {"reason": "no outgoing social tie"},
                        "abstention",
                    )
                )
                continue
            if self._rng.random() < self.config.abstention_probability:
                emitted.append(
                    self._emit(
                        "abstain",
                        actor.id,
                        "",
                        {"reason": "abstention draw"},
                        "abstention",
                    )
                )
                continue
            if self._rng.random() > self.config.communication_probability:
                emitted.append(
                    self._emit(
                        "abstain",
                        actor.id,
                        "",
                        {"reason": "communication draw failed"},
                        "communication",
                    )
                )
                continue
            target_id = self._rng.choice(targets)
            claim = self._rng.choice(self._sorted_claims())
            target = self.actors[target_id]
            stance = float(actor.disposition.get(claim.id, 0.0))
            emitted.append(
                self._emit(
                    "communicate",
                    actor.id,
                    target_id,
                    {
                        "claim": claim.id,
                        "stance": round(stance, 4),
                        "channel": "public",
                    },
                    "communication",
                )
            )
            self.communication_edges.append(
                CommunicationEdge(
                    source=actor.id,
                    target=target_id,
                    time=self.turn,
                    channel="public",
                    provenance=Provenance(
                        Material.SIMULATED,
                        f"sim:{self.config.seed}",
                        "behavioral-rule:communication",
                    ),
                )
            )
            emitted.extend(
                self._influence(source=actor, target=target, claim=claim, stance=stance)
            )
            emitted.extend(self._maybe_institutional(organizations, claim))
        self.turn += 1
        return emitted

    def run(self, turns: int | None = None) -> list[SimEvent]:
        total = self.config.turns if turns is None else turns
        if total < 1:
            raise SimulationError("turns must be at least 1")
        emitted: list[SimEvent] = []
        for _ in range(total):
            emitted.extend(self.step())
        return emitted

    # -- behavior ------------------------------------------------------------------------------ #
    def _influence(
        self, *, source: Actor, target: Actor, claim: Claim, stance: float
    ) -> list[SimEvent]:
        emitted: list[SimEvent] = []
        delta = self.config.influence_rate * (1.0 if stance >= 0 else -1.0)
        before = float(target.disposition.get(claim.id, 0.0))
        after = _clamp(before + delta)
        target.disposition[claim.id] = after
        emitted.append(
            self._emit(
                "respond",
                target.id,
                source.id,
                {"claim": claim.id, "from": round(before, 4), "to": round(after, 4)},
                "influence",
            )
        )
        target.attention = _clamp(target.attention + 0.10, 0.0, 1.0)
        emitted.append(
            self._emit(
                "attention_change",
                target.id,
                "",
                {
                    "value": round(target.attention, 4),
                    "reason": "received communication",
                },
                "attention",
            )
        )
        if after >= self.config.coalition_threshold and not self._has_relation(
            target.id, claim.id, "coalition"
        ):
            self.add_social_edge(
                SocialEdge(
                    source=target.id,
                    target=source.id,
                    relation="coalition",
                    time=self.turn,
                    provenance=Provenance(
                        Material.SIMULATED,
                        f"sim:{self.config.seed}",
                        "behavioral-rule:coalition",
                    ),
                )
            )
            emitted.append(
                self._emit(
                    "affiliate",
                    target.id,
                    source.id,
                    {"claim": claim.id, "disposition": round(after, 4)},
                    "coalition",
                )
            )
        if before * after < 0 and abs(before) >= self.config.coalition_threshold:
            emitted.append(
                self._emit(
                    "contest",
                    target.id,
                    source.id,
                    {
                        "claim": claim.id,
                        "from": round(before, 4),
                        "to": round(after, 4),
                    },
                    "contest",
                )
            )
        return emitted

    def _maybe_institutional(
        self, organizations: Iterable[Actor], claim: Claim
    ) -> list[SimEvent]:
        emitted: list[SimEvent] = []
        for organization in organizations:
            if organization.id in self._institutional_this_turn:
                continue
            if organization.attention >= self.config.institutional_threshold:
                self._institutional_this_turn.add(organization.id)
                emitted.append(
                    self._emit(
                        "institutional_response",
                        organization.id,
                        "",
                        {
                            "claim": claim.id,
                            "attention": round(organization.attention, 4),
                        },
                        "institution",
                    )
                )
        return emitted

    def _decay_attention(self) -> None:
        for actor in self.actors.values():
            actor.attention = _clamp(
                actor.attention * (1.0 - self.config.attention_decay), 0.0, 1.0
            )

    def _has_relation(self, source: str, claim: str, relation: str) -> bool:
        # Coalition edges are actor-to-actor; the claim is captured in the payload of
        # the affiliate event, so this guard is deliberately about the *pair* only.
        return any(
            e.source == source and e.relation == relation for e in self.social_edges
        )

    # -- event helpers ------------------------------------------------------------------------- #
    def _emit(
        self, kind: str, actor: str, target: str, payload: Mapping[str, Any], rule: str
    ) -> SimEvent:
        index = len(self.log) + 1
        event = SimEvent(
            event_id=f"evt:{self.turn:04d}:{index:05d}",
            time=self.turn,
            kind=kind,
            actor=actor,
            target=target,
            payload=dict(payload),
            rule=rule,
            provenance=Provenance(
                Material.SIMULATED, f"sim:{self.config.seed}", f"behavioral-rule:{rule}"
            ),
        )
        self.log.append(event)
        return event

    # -- validation ---------------------------------------------------------------------------- #
    def _sorted_actors(self) -> list[Actor]:
        return [self.actors[key] for key in sorted(self.actors)]

    def _sorted_claims(self) -> list[Claim]:
        return [self.claims[key] for key in sorted(self.claims)]

    def _require_actor(self, actor_id: str) -> None:
        if actor_id not in self.actors:
            raise SimulationError(f"unknown actor {actor_id!r}")

    def _require_claim(self, claim_id: str) -> None:
        if claim_id not in self.claims:
            raise SimulationError(f"unknown claim {claim_id!r}")

    # -- persistence --------------------------------------------------------------------------- #
    def to_snapshot(self) -> dict[str, Any]:
        return {
            "format": "noopunk.social_science.simulation",
            "version": 1,
            "config": self.config.to_dict(),
            "turn": self.turn,
            "actors": [actor.to_dict() for actor in self._sorted_actors()],
            "claims": [claim.to_dict() for claim in self._sorted_claims()],
            "articulations": [
                a.to_dict()
                for a in sorted(self.articulations.values(), key=lambda a: a.id)
            ],
            "social_edges": [edge.to_dict() for edge in self.social_edges],
            "communication_edges": [
                edge.to_dict() for edge in self.communication_edges
            ],
            "events": self.log.to_dicts(),
            "rng_state": list(self._rng.getstate()),
        }

    @classmethod
    def from_snapshot(cls, payload: Mapping[str, Any]) -> SocialScienceSimulation:
        if (
            payload.get("format") != "noopunk.social_science.simulation"
            or payload.get("version") != 1
        ):
            raise SimulationError("unsupported simulation snapshot format or version")
        config = SimulationConfig(**dict(payload["config"]))
        simulation = cls(config=config)
        for raw in payload["actors"]:
            simulation.add_actor(Actor.from_dict(raw))
        for raw in payload["claims"]:
            simulation.add_claim(Claim.from_dict(raw))
        for raw in payload["articulations"]:
            simulation.add_articulation(Articulation.from_dict(raw))
        for raw in payload["social_edges"]:
            simulation.social_edges.append(
                SocialEdge(
                    source=str(raw["source"]),
                    target=str(raw["target"]),
                    relation=str(raw["relation"]),
                    time=int(raw["time"]),
                    provenance=Provenance.from_dict(raw["provenance"]),
                    uncertainty=float(raw.get("uncertainty", 0.0)),
                )
            )
        for raw in payload["communication_edges"]:
            simulation.communication_edges.append(
                CommunicationEdge(
                    source=str(raw["source"]),
                    target=str(raw["target"]),
                    time=int(raw["time"]),
                    channel=str(raw.get("channel", "public")),
                    provenance=Provenance.from_dict(raw["provenance"]),
                    uncertainty=float(raw.get("uncertainty", 0.0)),
                )
            )
        simulation.log = EventLog.from_dicts(payload["events"])
        simulation.turn = int(payload["turn"])

        def _tupleize(value: Any) -> Any:
            if isinstance(value, list):
                return tuple(_tupleize(item) for item in value)
            return value

        state = _tupleize(payload.get("rng_state", ()))
        if state:
            simulation._rng.setstate(state)  # type: ignore[arg-type]
        return simulation

    def digest(self) -> str:
        """Stable hash of the snapshot, excluding the RNG state (which is seed-derived)."""
        snapshot = self.to_snapshot()
        snapshot.pop("rng_state", None)
        canonical = json.dumps(
            snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
