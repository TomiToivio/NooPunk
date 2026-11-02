"""Optional AWN-inspired settlement, crisis and encounter data (#1083).

Original NoöPunk domain records, not transcriptions of unlicensed AWN tables.
No dice, faction turns, CWN checks, or automatic apocalypse clocks live here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any


class WorldModelError(ValueError):
    """Invalid campaign-world event or cross-scale reference."""


def _date(value: str) -> str:
    try:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError
    except (TypeError, ValueError) as exc:
        raise WorldModelError("dates must use ISO YYYY-MM-DD") from exc
    return value


def _id(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorldModelError(f"{label} needs a nonempty id")
    return value


@dataclass(frozen=True)
class Enclave:
    """A settlement in one region, distinct from an SWN faction asset."""

    id: str
    region_id: str
    name: str
    tags: tuple[str, ...] = ()
    dominance: str = "undecided"
    cohesion: str = "undecided"

    def __post_init__(self) -> None:
        for key in ("id", "region_id", "name"):
            _id(getattr(self, key), key)


@dataclass(frozen=True)
class Site:
    """Scenario author supplies tags and contents; this format grants no loot."""

    id: str
    region_id: str
    enclave_id: str | None = None
    tags: tuple[str, ...] = ()
    features: tuple[str, ...] = ()
    occupants: tuple[str, ...] = ()
    hazards: tuple[str, ...] = ()
    salvage: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _id(self.id, "site")
        _id(self.region_id, "region")


@dataclass(frozen=True)
class Crisis:
    id: str
    region_id: str
    title: str
    pressure: int = 0
    active: bool = True

    def __post_init__(self) -> None:
        _id(self.id, "crisis")
        _id(self.region_id, "region")
        if type(self.pressure) is not int or self.pressure < 0:
            raise WorldModelError("pressure is a nonnegative integer")


@dataclass(frozen=True)
class WorldEvent:
    """An authored consequence, never an automatically generated turn."""

    id: str
    date: str
    kind: str
    target_id: str
    cause: str
    source: str = ""
    pressure_change: int = 0
    outcome: str = ""

    def __post_init__(self) -> None:
        _id(self.id, "event")
        _date(self.date)
        if self.kind not in {"crisis", "enclave", "mission"}:
            raise WorldModelError("kind must be crisis, enclave or mission")
        _id(self.target_id, "target")
        _id(self.cause, "cause")
        if type(self.pressure_change) is not int:
            raise WorldModelError("pressure_change must be an integer")
        if self.kind != "crisis" and self.pressure_change:
            raise WorldModelError("only a crisis event changes pressure")


@dataclass
class WorldLedger:
    """Independent scales linked by IDs and dated evidence, not shared turns.

    Enclave events and CWN missions are evidence. SWN faction rules remain
    authoritative for faction assets and turns. RegionLedger stays authoritative
    for the material-collapse axes.
    """

    region_ids: set[str] = field(default_factory=set)
    enclaves: dict[str, Enclave] = field(default_factory=dict)
    sites: dict[str, Site] = field(default_factory=dict)
    crises: dict[str, Crisis] = field(default_factory=dict)
    faction_assets: dict[str, tuple[str, str]] = field(default_factory=dict)
    events: list[WorldEvent] = field(default_factory=list)

    def add_enclave(self, enclave: Enclave) -> None:
        self._region(enclave.region_id)
        if enclave.id in self.enclaves:
            raise WorldModelError("duplicate enclave")
        self.enclaves[enclave.id] = enclave

    def add_site(self, site: Site) -> None:
        self._region(site.region_id)
        if site.enclave_id is not None:
            enclave = self._enclave(site.enclave_id)
            if enclave.region_id != site.region_id:
                raise WorldModelError("site/enclave region mismatch")
        if site.id in self.sites:
            raise WorldModelError("duplicate site")
        self.sites[site.id] = site

    def add_crisis(self, crisis: Crisis) -> None:
        self._region(crisis.region_id)
        if crisis.id in self.crises:
            raise WorldModelError("duplicate crisis")
        self.crises[crisis.id] = crisis

    def link_faction_asset(self, asset_id: str, faction_id: str, enclave_id: str) -> None:
        """Reference an SWN asset without modifying the SWN asset or its turn."""
        _id(asset_id, "asset")
        _id(faction_id, "faction")
        self._enclave(enclave_id)
        if asset_id in self.faction_assets:
            raise WorldModelError("asset already linked")
        self.faction_assets[asset_id] = (faction_id, enclave_id)

    def record(self, event: WorldEvent) -> Crisis | None:
        if any(e.id == event.id for e in self.events):
            raise WorldModelError("duplicate event")
        if self.events and event.date < self.events[-1].date:
            raise WorldModelError("events must be date-monotonic")
        updated = None
        if event.kind == "crisis":
            if event.target_id not in self.crises:
                raise WorldModelError("unknown crisis")
            old = self.crises[event.target_id]
            if not old.active:
                raise WorldModelError("a resolved crisis cannot change")
            pressure = old.pressure + event.pressure_change
            if pressure < 0:
                raise WorldModelError("pressure cannot drop below zero")
            updated = Crisis(old.id, old.region_id, old.title, pressure,
                             event.outcome != "resolved")
            self.crises[old.id] = updated
        elif event.kind == "enclave":
            self._enclave(event.target_id)
        else:
            # Mission ids originate in CWN campaign state and are evidence only.
            _id(event.target_id, "mission")
            if not event.source:
                raise WorldModelError("mission evidence needs a source")
        self.events.append(event)
        return updated

    def _region(self, region_id: str) -> None:
        if region_id not in self.region_ids:
            raise WorldModelError(f"unknown region {region_id!r}")

    def _enclave(self, enclave_id: str) -> Enclave:
        try:
            return self.enclaves[enclave_id]
        except KeyError as exc:
            raise WorldModelError(f"unknown enclave {enclave_id!r}") from exc

    def to_dict(self) -> dict[str, Any]:
        return {"version": 1, "region_ids": sorted(self.region_ids),
                "enclaves": [asdict(e) for e in self.enclaves.values()],
                "sites": [asdict(s) for s in self.sites.values()],
                "crises": [asdict(c) for c in self.crises.values()],
                "faction_assets": {k: list(v) for k, v in self.faction_assets.items()},
                "events": [asdict(e) for e in self.events]}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorldLedger:
        if data.get("version") != 1:
            raise WorldModelError("unsupported world ledger version")
        ledger = cls(region_ids=set(data["region_ids"]))
        for entry in data["enclaves"]:
            ledger.add_enclave(Enclave(**entry))
        for entry in data["sites"]:
            ledger.add_site(Site(**entry))
        for entry in data["crises"]:
            ledger.add_crisis(Crisis(**entry))
        for asset, (faction, enclave) in data["faction_assets"].items():
            ledger.link_faction_asset(asset, faction, enclave)
        # The crisis records above are already the *final* state. Do not replay
        # their events while loading or pressure is applied twice.
        events = [WorldEvent(**entry) for entry in data["events"]]
        if len({event.id for event in events}) != len(events):
            raise WorldModelError("duplicate persisted events")
        if any(left.date > right.date for left, right in zip(events, events[1:])):
            raise WorldModelError("persisted events are not date-monotonic")
        for event in events:
            if event.kind == "crisis" and event.target_id not in ledger.crises:
                raise WorldModelError("persisted event points to unknown crisis")
            if event.kind == "enclave":
                ledger._enclave(event.target_id)
        ledger.events = events
        return ledger
