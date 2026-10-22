"""Data-only, rule-free foundation for the separate NoöPunk strategy game."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any

from .politics import Demand, Formation, Frontier, Signifier
from .provenance import Provenance


@dataclass
class Leader:
    identifier: str
    name: str
    attributes: dict[str, Any] = field(default_factory=dict)
    personality_tags: list[str] = field(default_factory=list)


@dataclass
class Faction:
    identifier: str
    name: str
    leader_id: str | None = None
    asset_ids: list[str] = field(default_factory=list)


@dataclass
class Asset:
    identifier: str
    label: str
    location_id: str | None = None
    owner_faction_id: str | None = None


@dataclass
class Location:
    """One place on the board.

    The two optional numbers are **board position on the fictional map** — a grid reference
    for the tabletop, not a geographic coordinate of a real place. They are named ``grid_row``
    and ``grid_column`` rather than ``latitude``/``longitude`` for exactly that reason: the
    names CodeQL's sensitive-data heuristic treats as personal location data would make a
    fictional board coordinate look like a person's whereabouts in every security scan
    (issue #186), which is both a false positive and a real drain on the scanner's signal.
    """
    identifier: str
    label: str
    grid_row: float | None = None
    grid_column: float | None = None


@dataclass
class NetworkEdge:
    source: str
    target: str
    layer: str = ""


@dataclass
class Event:
    identifier: str
    description: str
    #: Where this record came from, kept separate from ``description`` so source-supported material
    #: is never conflated with authored, generated or simulated discourse (issue #282). Defaults to
    #: an ``UNKNOWN`` origin: a missing provenance stays visibly unknown rather than reading as fact.
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        # Accept a legacy bare string (or a raw dict) so existing constructor calls keep working;
        # it becomes an UNKNOWN-origin Provenance rather than being rejected or upgraded.
        if not isinstance(self.provenance, Provenance):
            self.provenance = Provenance.from_dict(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "description": self.description,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Event":
        return cls(
            identifier=data["identifier"],
            description=data["description"],
            provenance=Provenance.from_dict(data.get("provenance")),
        )


@dataclass
class WorldState:
    schema_version: str = "scaffold-1"
    leaders: list[Leader] = field(default_factory=list)
    factions: list[Faction] = field(default_factory=list)
    assets: list[Asset] = field(default_factory=list)
    locations: list[Location] = field(default_factory=list)
    edges: list[NetworkEdge] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    #: Layer II (issue #282). Declared political records, empty by default. Political *relations*
    #: are ordinary :class:`NetworkEdge` entries in ``edges`` carrying a
    #: :class:`strategy_game.politics.RelationLayer` label -- there is deliberately no second
    #: edge collection, so the whole political field stays one multiplex graph.
    demands: list[Demand] = field(default_factory=list)
    signifiers: list[Signifier] = field(default_factory=list)
    formations: list[Formation] = field(default_factory=list)
    frontiers: list[Frontier] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Plain-JSON representation. Nested records are serialized explicitly."""
        data = asdict(self)
        # ``asdict`` would leave a Provenance enum member inside the payload; emit the scalars.
        data["events"] = [event.to_dict() for event in self.events]
        data["demands"] = [item.to_dict() for item in self.demands]
        data["signifiers"] = [item.to_dict() for item in self.signifiers]
        data["formations"] = [item.to_dict() for item in self.formations]
        data["frontiers"] = [item.to_dict() for item in self.frontiers]
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> WorldState:
        data = json.loads(text)
        # ``.get`` so a snapshot written before a section existed still loads, and so a legacy
        # bare-string ``Event.provenance`` is read rather than rejected.
        return cls(
            schema_version=data.get("schema_version", "scaffold-1"),
            leaders=[Leader(**item) for item in data.get("leaders", [])],
            factions=[Faction(**item) for item in data.get("factions", [])],
            assets=[Asset(**item) for item in data.get("assets", [])],
            locations=[Location(**item) for item in data.get("locations", [])],
            edges=[NetworkEdge(**item) for item in data.get("edges", [])],
            events=[Event.from_dict(item) for item in data.get("events", [])],
            demands=[Demand.from_dict(item) for item in data.get("demands", [])],
            signifiers=[Signifier.from_dict(item) for item in data.get("signifiers", [])],
            formations=[Formation.from_dict(item) for item in data.get("formations", [])],
            frontiers=[Frontier.from_dict(item) for item in data.get("frontiers", [])],
        )
