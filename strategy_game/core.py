"""Data-only, rule-free foundation for the separate NoöPunk strategy game."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from typing import Any


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
    identifier: str
    label: str
    latitude: float | None = None
    longitude: float | None = None


@dataclass
class NetworkEdge:
    source: str
    target: str
    layer: str = ""


@dataclass
class Event:
    identifier: str
    description: str
    provenance: str = ""


@dataclass
class WorldState:
    schema_version: str = "scaffold-1"
    leaders: list[Leader] = field(default_factory=list)
    factions: list[Faction] = field(default_factory=list)
    assets: list[Asset] = field(default_factory=list)
    locations: list[Location] = field(default_factory=list)
    edges: list[NetworkEdge] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "WorldState":
        data = json.loads(text)
        return cls(
            schema_version=data["schema_version"],
            leaders=[Leader(**item) for item in data["leaders"]],
            factions=[Faction(**item) for item in data["factions"]],
            assets=[Asset(**item) for item in data["assets"]],
            locations=[Location(**item) for item in data["locations"]],
            edges=[NetworkEdge(**item) for item in data["edges"]],
            events=[Event(**item) for item in data["events"]],
        )
