"""Map specification reader and validator for the Ukweli local scenario (issue #325, deliverable 3).

Issue #325 asks for a *"concise annotated city/islands diagram and data-driven location/network schema,
respecting 6-8 playable nodes"*. `docs/world/UKWELI_MAP_SPECIFICATION.md` is the diagram and schema;
this module is what stops the two drifting apart.

What this module is
-------------------

A stdlib-only reader and validator for the location and route data in ``data/ukweli_local.json``. It
enforces the rules the specification states:

* **6-8 playable nodes** -- under six cannot carry four factions, over eight breaks the small-table
  promise.
* **Well-formed routes** -- both endpoints exist, no self-loops, no duplicates.
* **Connected** -- every node reachable from every other.
* **Islands are reachable** -- an island with no route is scenery, not a location.

What this module is not
-----------------------

Not a map renderer and not a movement system. It proposes **no scale and no distance**; reachability is
the only spatial property it knows, because that is the one the strategy layer actually needs.
``data/ukweli_local.json``'s declared ``pressure`` field is checked for shape only -- this module does
not invent, weight or extend it.

It also encodes one deliberate absence. The specification records that the **restricted ecological
island is not a playable node**: the budget is already full at eight, a prohibited island is somewhere a
leader does not move pieces on turn one, and the existing shock deck is how the anomalous margin reaches
play. :meth:`MapSpec.restricted_node_ids` therefore returns whatever is declared, and the contracts
assert the *rule* (no playable node is marked restricted) rather than a guessed geography.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import json

__all__ = [
    "DATA_FORMAT_PREFIX",
    "DATA_PATH",
    "NODE_MIN",
    "NODE_MAX",
    "MapSpecError",
    "Location",
    "MapSpec",
    "map_spec_from_dict",
    "load_map_spec",
]

#: The scenario document type this module reads.
DATA_FORMAT_PREFIX = "noopunk.strategy.local"

DATA_PATH = Path(__file__).with_name("data") / "ukweli_local.json"

#: The playable node budget #325 states.
NODE_MIN = 6
NODE_MAX = 8

#: Field-name fragments that would mean a scale this specification has no authority to propose.
_SCALE_TOKENS = ("score", "rating", "points", "distance", "weight", "cost")


class MapSpecError(ValueError):
    """Raised when a document cannot be read as a local scenario map."""


@dataclass(frozen=True)
class Location:
    """One playable node. Fields mirror the scenario data exactly."""

    id: str
    label: str = ""
    tags: tuple[str, ...] = ()
    island: bool = False
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "tags": list(self.tags),
                "island": self.island, **self.detail}


@dataclass
class MapSpec:
    """The read map: the nodes, the declared routes and the rules they must satisfy."""

    format: str = ""
    year: Any = None
    locations: tuple[Location, ...] = ()
    routes: tuple[tuple[str, str], ...] = ()
    raw: dict[str, Any] = field(default_factory=dict)

    # -- lookups -----------------------------------------------------------------
    def location(self, node_id: str) -> Location | None:
        return next((l for l in self.locations if l.id == node_id), None)

    @property
    def node_ids(self) -> tuple[str, ...]:
        return tuple(l.id for l in self.locations)

    @property
    def island_ids(self) -> tuple[str, ...]:
        return tuple(l.id for l in self.locations if l.island)

    @property
    def restricted_node_ids(self) -> tuple[str, ...]:
        """Playable nodes declared restricted. By design this is empty -- see the module docstring."""
        return tuple(l.id for l in self.locations if "restricted" in l.tags
                     or l.detail.get("restricted") is True)

    def neighbours(self, node_id: str) -> tuple[str, ...]:
        out: list[str] = []
        for a, b in self.routes:
            if a == node_id:
                out.append(b)
            elif b == node_id:
                out.append(a)
        return tuple(out)

    def reachable_from(self, start: str) -> tuple[str, ...]:
        """Breadth-first reachability. Deliberately the only spatial property this module knows."""
        seen: list[str] = [start]
        queue: list[str] = [start]
        while queue:
            for nxt in self.neighbours(queue.pop(0)):
                if nxt not in seen:
                    seen.append(nxt)
                    queue.append(nxt)
        return tuple(seen)

    def to_dict(self) -> dict[str, Any]:
        data = dict(self.raw)
        data["locations"] = [l.to_dict() for l in self.locations]
        data["routes"] = [list(r) for r in self.routes]
        return data

    # -- validation --------------------------------------------------------------
    def problems(self) -> tuple[str, ...]:
        """Specification defects. Reports; never raises."""
        issues: list[str] = []

        # 1. the node budget
        count = len(self.locations)
        if not NODE_MIN <= count <= NODE_MAX:
            issues.append(f"{count} playable nodes declared, budget is {NODE_MIN}-{NODE_MAX}")
        if count < 2:
            issues.append("fewer than two nodes declared")

        # 2. node identity and shape
        seen: set[str] = set()
        for loc in self.locations:
            if loc.id != loc.id.lower():
                issues.append(f"{loc.id!r} is not lowercase")
            if loc.id in seen:
                issues.append(f"duplicate node id {loc.id!r}")
            seen.add(loc.id)
            if not loc.tags:
                issues.append(f"{loc.id}: node declares no tags")
            for key in loc.detail:
                if any(tok in key.lower() for tok in _SCALE_TOKENS):
                    issues.append(f"{loc.id}: scale-shaped field {key!r}")

        # 3. route shape
        seen_routes: set[frozenset[str]] = set()
        for a, b in self.routes:
            if a == b:
                issues.append(f"self-loop on {a!r}")
            if a not in seen:
                issues.append(f"route endpoint {a!r} is not a declared node")
            if b not in seen:
                issues.append(f"route endpoint {b!r} is not a declared node")
            pair = frozenset((a, b))
            if pair in seen_routes:
                issues.append(f"duplicate route {sorted(pair)}")
            seen_routes.add(pair)

        # 4. connectivity -- every node reachable from every other
        if self.locations:
            reachable = set(self.reachable_from(self.locations[0].id))
            unreachable = sorted(set(seen) - reachable)
            if unreachable:
                issues.append(f"unreachable nodes: {unreachable}")

        # 5. every island must be reachable by a route
        for island_id in self.island_ids:
            if not self.neighbours(island_id):
                issues.append(f"island {island_id!r} has no route")

        # 6. the deliberate absence is stated, not assumed
        if self.restricted_node_ids:
            issues.append(
                f"playable node(s) declared restricted: {sorted(self.restricted_node_ids)} -- the "
                "specification keeps the restricted island out of the playable budget (see section 3)"
            )

        return tuple(issues)


def map_spec_from_dict(data: dict[str, Any]) -> MapSpec:
    """Build a :class:`MapSpec` from an already-parsed scenario document."""
    if not isinstance(data, dict):
        raise MapSpecError("scenario document must be an object")
    locations: list[Location] = []
    for record in data.get("locations", []) or []:
        if not isinstance(record, dict):
            continue
        known = {"id", "label", "tags", "island"}
        locations.append(
            Location(
                id=str(record.get("id", "")),
                label=str(record.get("label", "")),
                tags=tuple(str(t) for t in record.get("tags", []) or []),
                island=bool(record.get("island", False)),
                detail={k: v for k, v in record.items() if k not in known},
            )
        )
    routes: list[tuple[str, str]] = []
    for pair in data.get("routes", []) or []:
        if isinstance(pair, (list, tuple)) and len(pair) == 2:
            routes.append((str(pair[0]), str(pair[1])))
    return MapSpec(
        format=str(data.get("format", "")),
        year=data.get("year"),
        locations=tuple(locations),
        routes=tuple(routes),
        raw=data,
    )


def load_map_spec(path: Path | str | None = None) -> MapSpec:
    """Read and validate the packaged local scenario map, refusing a foreign document type."""
    target = Path(path) if path is not None else DATA_PATH
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:  # pragma: no cover - packaging error
        raise MapSpecError(f"scenario data not found at {target}") from exc
    except json.JSONDecodeError as exc:
        raise MapSpecError(f"scenario data is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise MapSpecError(f"{target} must contain a JSON object, got {type(data).__name__}")

    declared = str(data.get("format", ""))
    if not declared.startswith(DATA_FORMAT_PREFIX):
        raise MapSpecError(f"{target} declares format {declared!r}, expected {DATA_FORMAT_PREFIX!r}...")
    return map_spec_from_dict(data)
