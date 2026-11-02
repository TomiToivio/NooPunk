"""Optional event-sourced DA/DNA/SNA world ledger (#1042).

No CWN rule modifications. Observations, narrative inferences and game events are
separate; discourse agreement never implies friendship or institutional access.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

POLARITIES = ("support", "oppose", "uncertain")
PROVENANCE = ("observed", "fictional", "gameplay")
VISIBILITY = ("public", "private", "secret")

@dataclass(frozen=True)
class Position:
    actor_id: str
    concept_id: str
    polarity: str
    event_id: str
    source: str
    at: str
    provenance: str = "gameplay"
    visibility: str = "public"

    def __post_init__(self):
        if not all((self.actor_id, self.concept_id, self.event_id, self.source, self.at)):
            raise ValueError("DNA positions require source, event, actor, concept and timestamp")
        if self.polarity not in POLARITIES or self.provenance not in PROVENANCE:
            raise ValueError("invalid polarity or provenance")
        if self.visibility not in VISIBILITY:
            raise ValueError("invalid visibility")

@dataclass
class DiscourseLedger:
    profiles: dict[str, dict] = field(default_factory=dict)
    positions: list[Position] = field(default_factory=list)
    communications: list[dict] = field(default_factory=list)
    affiliations: list[dict] = field(default_factory=list)
    relations: dict[str, dict] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)

    def profile(self, actor: str, *, identities=(), values=(), demands=(),
                signifiers=(), antagonisms=(), goals=None, uncertainty=None):
        if not actor:
            raise ValueError("actor required")
        self.profiles[actor] = dict(identities=list(identities), values=list(values),
            demands=list(demands), signifiers=list(signifiers),
            antagonisms=list(antagonisms), goals=dict(goals or {}),
            uncertainty=dict(uncertainty or {}))

    def statement(self, item: Position):
        if any(p.event_id == item.event_id and p.actor_id == item.actor_id
               and p.concept_id == item.concept_id for p in self.positions):
            raise ValueError("duplicate actor/concept/event")
        self.positions.append(item)

    def communication(self, sender: str, recipient: str, event_id: str, at: str,
                      *, provenance: str = "gameplay"):
        if not all((sender, recipient, event_id, at)) or provenance not in PROVENANCE:
            raise ValueError("invalid communication")
        self.communications.append(dict(sender=sender, recipient=recipient,
                                        event_id=event_id, at=at, provenance=provenance))

    def affiliation(self, actor: str, organization: str, event_id: str,
                    *, role: str = "", at: str):
        if not all((actor, organization, event_id, at)):
            raise ValueError("invalid affiliation")
        self.affiliations.append(dict(actor=actor, organization=organization,
                                      role=role, event_id=event_id, at=at))

    def relation(self, actor: str, other: str, *, trust: int, access: int,
                 reputation: int, event_id: str, authorized: bool = False):
        if not authorized or not event_id:
            raise PermissionError("relationships change only through an authorized game event")
        for value in (trust, access, reputation):
            if type(value) is not int or not -4 <= value <= 4:
                raise ValueError("relationship values must be integers -4..4")
        self.relations[f"{actor}|{other}"] = dict(trust=trust, access=access,
                reputation=reputation, event_id=event_id)

    def alignment(self, first: str, second: str, *, known_events: set[str] | None = None):
        """Only explicit latest certain positions; never infer social ties."""
        def current(actor):
            found = {}
            for p in self.positions:
                if p.actor_id == actor and p.polarity != "uncertain" and (
                        known_events is None or p.event_id in known_events
                ) and p.visibility == "public":
                    found[p.concept_id] = p.polarity
            return found
        a, b = current(first), current(second)
        shared = a.keys() & b.keys()
        return dict(agreement=sorted(c for c in shared if a[c] == b[c]),
                    conflict=sorted(c for c in shared if a[c] != b[c]))

    def snapshot(self):
        return dict(version=1, profiles=self.profiles,
                    positions=[asdict(x) for x in self.positions],
                    communications=self.communications, affiliations=self.affiliations,
                    relations=self.relations, events=self.events)

    @classmethod
    def from_snapshot(cls, data):
        if data.get("version") != 1:
            raise ValueError("unsupported DA/DNA/SNA snapshot")
        obj = cls(profiles=dict(data["profiles"]),
                  positions=[Position(**p) for p in data["positions"]],
                  communications=list(data["communications"]),
                  affiliations=list(data["affiliations"]),
                  relations=dict(data["relations"]), events=list(data["events"]))
        return obj
