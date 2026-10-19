"""Mission-map reader, validator and pathfinder for the optional tactical layer (issue #515).

Issue #515's first milestone is a *technical spike*: choose a renderer, a grid/tile format and a
mission-data schema. This module is the grid/tile format and the schema's executable half. It reads
``data/mission_map_municipal_archive.json`` and answers exactly one spatial question -- **is there a
walkable route between two cells, and which cells does it cross** -- because that is the one spatial
property the optional tactical layer needs before any rules exist.

What this module is
-------------------

A stdlib-only reader and validator for a tile-grid mission map, plus breadth-first pathfinding over
traversable cells. It enforces the shape the proposal claims:

* **A rectangular grid of declared size** -- every row has the declared width.
* **A sealed boundary** -- the perimeter is wall, so no path can leave the map.
* **A closed tile vocabulary** -- every character in the grid is declared in ``tile_codes``.
* **Doors are state, not scenery** -- a door cell is traversable only when its record says open, and
  every door cell has exactly one record.
* **Four deployed agents, and no leader** -- #515's "four-character squad" with the leader remaining
  the faction leader rather than silently occupying a fifth slot.
* **Every objective is approachable** -- each objective resolves to an interactable (or the exit) with
  at least one walkable neighbouring cell reachable from a deployed agent. A map that cannot be
  finished is a defect, not a difficulty setting.

What this module is not
-----------------------

Not a movement system, not a combat map and not a rules engine. ``path()`` reports which cells a route
crosses; it does **not** say what the route costs, how long it takes, whether the agent is permitted to
take it, or what happens on arrival. There is deliberately no damage, hit point, initiative, action
point, cover, line-of-sight, difficulty modifier or turn structure anywhere in this module -- the
issue's own non-goals and the repository's gates keep those for author-approved rules (#516).

A network fact is not a floor plan: whether a terminal can reach anything is decided by
``strategy_game/cyber.py`` in the current era (#344), never by this grid.

Overlays are display-only. The Physical / Cyber / Astral markers #515 asks for can be drawn on any
cell, but they never change walkability -- the ``overlays`` records are not consulted by ``walkable()``
at all, which is the cheapest way to keep that promise true.
"""

from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = [
    "AGENT_COUNT",
    "DATA_FORMAT",
    "DATA_PATH",
    "MISSION_MAP_FORMAT",
    "MISSION_MAP_VERSION",
    "Cell",
    "Door",
    "Interactable",
    "MissionMap",
    "MissionMapError",
    "Objective",
    "TileCode",
    "load_mission_map",
    "mission_map_from_dict",
]

MISSION_MAP_FORMAT = "noopunk.strategy_game.mission_map"
MISSION_MAP_VERSION = 1
DATA_FORMAT = MISSION_MAP_FORMAT

DATA_PATH = Path(__file__).with_name("data") / "mission_map_municipal_archive.json"

#: #515 asks for a four-character squad; the leader stays upstairs as faction leader.
AGENT_COUNT = 4

Cell = tuple[int, int]

INTERACTABLE_KINDS = ("person", "terminal", "evidence")
OBJECTIVE_KINDS = ("evidence", "conversation", "exit")
OVERLAY_LAYERS = ("physical", "cyber", "astral")
DOOR_STATES = ("open", "closed")

#: Keys that would smuggle an unapproved mechanic into map data. The map describes place, not rules.
_FORBIDDEN_KEYS = (
    "damage",
    "hit_points",
    "hp",
    "initiative",
    "action_points",
    "difficulty",
    "modifier",
    "morale",
    "cover",
    "line_of_sight",
    "turn_order",
)


class MissionMapError(ValueError):
    """Raised when a mission map cannot be read at all (bad JSON, wrong format, wrong version)."""


@dataclass(frozen=True)
class TileCode:
    """One entry of the closed tile vocabulary."""

    char: str
    name: str
    walkable: bool | str

    def traversable(self, door_open: bool) -> bool:
        """Whether a cell of this tile type can be entered, given the door state if relevant."""
        if self.walkable == "when_open":
            return door_open
        return bool(self.walkable)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "walkable": self.walkable}


@dataclass(frozen=True)
class Door:
    cell: Cell
    state: str
    note: str = ""

    @property
    def is_open(self) -> bool:
        return self.state == "open"

    def to_dict(self) -> dict[str, Any]:
        return {"cell": list(self.cell), "state": self.state, "note": self.note}


@dataclass(frozen=True)
class Interactable:
    id: str
    kind: str
    cell: Cell
    label: str = ""
    network_ref: str = ""
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        out = {"id": self.id, "kind": self.kind, "cell": list(self.cell)}
        if self.label:
            out["label"] = self.label
        if self.network_ref:
            out["network_ref"] = self.network_ref
        if self.note:
            out["note"] = self.note
        return out


@dataclass(frozen=True)
class Objective:
    id: str
    kind: str
    interactable_ref: str = ""
    cell: Cell | None = None
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"id": self.id, "kind": self.kind}
        if self.interactable_ref:
            out["interactable_ref"] = self.interactable_ref
        if self.cell is not None:
            out["cell"] = list(self.cell)
        if self.note:
            out["note"] = self.note
        return out


@dataclass
class MissionMap:
    """A validated-by-report tile map. ``problems()`` lists defects; it never raises."""

    map_id: str
    width: int
    height: int
    rows: tuple[str, ...]
    tile_codes: dict[str, TileCode]
    doors: tuple[Door, ...] = ()
    agents: tuple[dict[str, Any], ...] = ()
    leader_ref: str = ""
    interactables: tuple[Interactable, ...] = ()
    objectives: tuple[Objective, ...] = ()
    overlays: tuple[dict[str, Any], ...] = ()
    status: str = ""
    sources: tuple[str, ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)
    #: keys found in the data as received that name an unapproved mechanic
    declared_mechanic_keys: tuple[str, ...] = ()

    # -- geometry ---------------------------------------------------------------------------

    def in_bounds(self, cell: Cell) -> bool:
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def tile_char(self, cell: Cell) -> str:
        x, y = cell
        return self.rows[y][x]

    def tile(self, cell: Cell) -> TileCode | None:
        return self.tile_codes.get(self.tile_char(cell))

    def _door_at(self, cell: Cell) -> Door | None:
        for door in self.doors:
            if door.cell == cell:
                return door
        return None

    def walkable(self, cell: Cell) -> bool:
        """Whether an agent may occupy this cell. Overlays are never consulted here."""
        if not self.in_bounds(cell):
            return False
        code = self.tile(cell)
        if code is None:
            return False
        door = self._door_at(cell)
        return code.traversable(bool(door and door.is_open))

    def walkable_cells(self) -> tuple[Cell, ...]:
        return tuple(
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.walkable((x, y))
        )

    # -- interaction ------------------------------------------------------------------------

    def interactable(self, ref: str) -> Interactable | None:
        for item in self.interactables:
            if item.id == ref:
                return item
        return None

    def approach_cells(self, ref: str) -> tuple[Cell, ...]:
        """Walkable cells from which an interactable can be used (empty if none exist)."""
        item = self.interactable(ref)
        if item is None:
            return ()
        return tuple(
            cell for cell in self._neighbours(item.cell) if self.walkable(cell)
        )

    # -- pathfinding ------------------------------------------------------------------------

    def _neighbours(self, cell: Cell) -> tuple[Cell, ...]:
        """Four-neighbour order: west, east, north, south. Fixed, so paths are reproducible."""
        x, y = cell
        return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))

    def path(self, start: Cell, goal: Cell) -> tuple[Cell, ...]:
        """Shortest walkable route, inclusive of both ends; ``()`` if there is no route.

        Reports cells only. Cost, timing, permission and consequences belong to adjudication.
        """
        if not self.walkable(start) or not self.walkable(goal):
            return ()
        if start == goal:
            return (start,)
        parents: dict[Cell, Cell | None] = {start: None}
        queue: deque[Cell] = deque([start])
        while queue:
            cell = queue.popleft()
            for nxt in self._neighbours(cell):
                if nxt in parents or not self.walkable(nxt):
                    continue
                parents[nxt] = cell
                if nxt == goal:
                    route: list[Cell] = [nxt]
                    step: Cell | None = cell
                    while step is not None:
                        route.append(step)
                        step = parents[step]
                    route.reverse()
                    return tuple(route)
                queue.append(nxt)
        return ()

    def reachable_from(self, start: Cell) -> frozenset[Cell]:
        """Every cell reachable from ``start`` including itself."""
        if not self.walkable(start):
            return frozenset()
        seen: set[Cell] = {start}
        queue: deque[Cell] = deque([start])
        while queue:
            cell = queue.popleft()
            for nxt in self._neighbours(cell):
                if nxt in seen or not self.walkable(nxt):
                    continue
                seen.add(nxt)
                queue.append(nxt)
        return frozenset(seen)

    # -- validation -------------------------------------------------------------------------

    def problems(self) -> tuple[str, ...]:
        """Map defects. Reports; never raises."""
        issues: list[str] = []

        # 1. the grid itself
        if self.width <= 0 or self.height <= 0:
            issues.append(f"grid size {self.width}x{self.height} is not positive")
        if len(self.rows) != self.height:
            issues.append(f"{len(self.rows)} rows declared, height says {self.height}")
        for index, row in enumerate(self.rows):
            if len(row) != self.width:
                issues.append(f"row {index} is {len(row)} cells wide, width says {self.width}")
        if issues:
            return tuple(issues)

        # 2. closed tile vocabulary
        for y, row in enumerate(self.rows):
            for x, char in enumerate(row):
                if char not in self.tile_codes:
                    issues.append(f"cell ({x},{y}) uses undeclared tile {char!r}")

        # 3. sealed boundary: no route may leave the map
        perimeter = [(x, 0) for x in range(self.width)]
        perimeter += [(x, self.height - 1) for x in range(self.width)]
        perimeter += [(0, y) for y in range(self.height)]
        perimeter += [(self.width - 1, y) for y in range(self.height)]
        for cell in dict.fromkeys(perimeter):
            code = self.tile(cell)
            if code is not None and code.name != "wall":
                issues.append(f"boundary cell {cell} is {code.name}, not wall")

        # 4. doors are state, not scenery
        door_cells = {
            (x, y)
            for y, row in enumerate(self.rows)
            for x, char in enumerate(row)
            if char in self.tile_codes and self.tile_codes[char].walkable == "when_open"
        }
        recorded: set[Cell] = set()
        for door in self.doors:
            if not self.in_bounds(door.cell):
                issues.append(f"door record at {door.cell} is outside the grid")
                continue
            if self.tile(door.cell) is None or self.tile_codes[self.tile_char(door.cell)].walkable != "when_open":
                issues.append(f"door record at {door.cell} is not on a door cell")
            if door.state not in DOOR_STATES:
                issues.append(f"door at {door.cell} has state {door.state!r}")
            if door.cell in recorded:
                issues.append(f"two door records for {door.cell}")
            recorded.add(door.cell)
        for cell in sorted(door_cells - recorded):
            issues.append(f"door cell {cell} has no door record, so its state is undefined")

        # 5. four agents, no leader, distinct walkable cells
        if len(self.agents) != AGENT_COUNT:
            issues.append(f"{len(self.agents)} deployed agents, the squad is {AGENT_COUNT}")
        refs = [str(a.get("agent_ref", "")) for a in self.agents]
        if len(set(refs)) != len(refs):
            issues.append("duplicate agent_ref among deployed agents")
        if self.leader_ref and self.leader_ref in refs:
            issues.append("the leader is deployed as a fifth squad member")
        cells: list[Cell] = []
        for agent in self.agents:
            raw = agent.get("cell")
            if isinstance(raw, (list, tuple)) and len(raw) == 2:
                cells.append((int(raw[0]), int(raw[1])))
            else:
                cells.append((0, 0))
                issues.append(f"agent {agent.get('agent_ref')!r} has no two-integer cell")
        if len(set(cells)) != len(cells):
            issues.append("two agents share a cell")
        for ref, cell in zip(refs, cells):
            if not ref:
                issues.append("an agent has an empty agent_ref")
            if not self.in_bounds(cell):
                issues.append(f"agent {ref!r} is not on a cell of the grid")
            elif not self.walkable(cell):
                issues.append(f"agent {ref!r} stands on a non-walkable cell {cell}")

        # 6. interactables: kind must match the tile, and reachable from somewhere
        ids = [item.id for item in self.interactables]
        if len(set(ids)) != len(ids):
            issues.append("duplicate interactable id")
        expected_tile = {"person": "P", "terminal": "T", "evidence": "E"}
        for item in self.interactables:
            if item.kind not in INTERACTABLE_KINDS:
                issues.append(f"interactable {item.id!r} has kind {item.kind!r}")
            if not self.in_bounds(item.cell):
                issues.append(f"interactable {item.id!r} is outside the grid")
                continue
            if self.tile_char(item.cell) != expected_tile.get(item.kind, "?"):
                issues.append(
                    f"interactable {item.id!r} of kind {item.kind!r} sits on tile "
                    f"{self.tile_char(item.cell)!r}"
                )
            if not self.approach_cells(item.id):
                issues.append(f"interactable {item.id!r} cannot be approached from any walkable cell")

        # 7. objectives resolve, and the mission is completable
        reach: set[Cell] = set()
        for cell in cells:
            if self.in_bounds(cell) and self.walkable(cell):
                reach |= set(self.reachable_from(cell))
        for objective in self.objectives:
            if objective.kind not in OBJECTIVE_KINDS:
                issues.append(f"objective {objective.id!r} has kind {objective.kind!r}")
            if objective.kind == "exit":
                if objective.cell is None or not self.in_bounds(objective.cell):
                    issues.append(f"exit objective {objective.id!r} has no cell on the grid")
                elif objective.cell not in reach:
                    issues.append(f"exit objective {objective.id!r} cannot be reached")
                continue
            if not objective.interactable_ref:
                issues.append(f"objective {objective.id!r} names no interactable")
                continue
            item = self.interactable(objective.interactable_ref)
            if item is None:
                issues.append(
                    f"objective {objective.id!r} references unknown interactable "
                    f"{objective.interactable_ref!r}"
                )
                continue
            if not any(cell in reach for cell in self.approach_cells(item.id)):
                issues.append(f"objective {objective.id!r} cannot be reached by any deployed agent")

        # 8. overlays are display-only
        for overlay in self.overlays:
            if overlay.get("layer") not in OVERLAY_LAYERS:
                issues.append(f"overlay has unknown layer {overlay.get('layer')!r}")
            cell = tuple(overlay.get("cell") or ())
            if len(cell) != 2 or not self.in_bounds(cell):
                issues.append(f"overlay at {overlay.get('cell')!r} is outside the grid")

        # 9. no mechanic smuggled in as data
        issues.extend(self._forbidden_keys())

        return tuple(issues)

    def _forbidden_keys(self) -> list[str]:
        return [
            f"map data declares a mechanic key {key!r}"
            for key in self.declared_mechanic_keys
        ]

    # -- serialisation ----------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": MISSION_MAP_FORMAT,
            "version": MISSION_MAP_VERSION,
            "status": self.status,
            "sources": list(self.sources),
            "provenance": dict(self.provenance),
            "grid": {"width": self.width, "height": self.height},
            "tile_codes": {char: code.to_dict() for char, code in self.tile_codes.items()},
            "rows": list(self.rows),
            "doors": [door.to_dict() for door in self.doors],
            "agents": [dict(agent) for agent in self.agents],
            "leader_ref": self.leader_ref,
            "interactables": [item.to_dict() for item in self.interactables],
            "objectives": [objective.to_dict() for objective in self.objectives],
            "overlays": [dict(overlay) for overlay in self.overlays],
        }


# -- constructors ---------------------------------------------------------------------------


def _mechanic_keys(node: Any) -> tuple[str, ...]:
    """Every key in the received payload that names an unapproved mechanic."""
    found: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                text = str(key)
                if text.lower() in _FORBIDDEN_KEYS:
                    found.add(text)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(node)
    return tuple(sorted(found))


def _cell(value: Any) -> Cell:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise MissionMapError(f"expected a two-integer cell, got {value!r}")
    try:
        return (int(value[0]), int(value[1]))
    except (TypeError, ValueError) as exc:
        raise MissionMapError(f"expected a two-integer cell, got {value!r}") from exc


def mission_map_from_dict(data: dict[str, Any]) -> MissionMap:
    """Build a map from its dict form. Shape errors raise; content defects are reported."""
    if not isinstance(data, dict):
        raise MissionMapError("mission map must be a JSON object")
    if data.get("format") != MISSION_MAP_FORMAT:
        raise MissionMapError(
            f"unexpected format {data.get('format')!r}, expected {MISSION_MAP_FORMAT!r}"
        )
    if data.get("version") != MISSION_MAP_VERSION:
        raise MissionMapError(
            f"unsupported version {data.get('version')!r}, expected {MISSION_MAP_VERSION}"
        )
    grid = data.get("grid") or {}
    try:
        width = int(grid.get("width", 0))
        height = int(grid.get("height", 0))
    except (TypeError, ValueError) as exc:
        raise MissionMapError("grid dimensions must be integers") from exc

    rows_raw = data.get("rows") or []
    if not isinstance(rows_raw, list) or not all(isinstance(r, str) for r in rows_raw):
        raise MissionMapError("rows must be a list of strings")

    codes: dict[str, TileCode] = {}
    for char, spec in (data.get("tile_codes") or {}).items():
        if not isinstance(spec, dict):
            raise MissionMapError(f"tile code {char!r} must be an object")
        codes[str(char)] = TileCode(
            char=str(char),
            name=str(spec.get("name", "")),
            walkable=spec.get("walkable", False),
        )
    if not codes:
        raise MissionMapError("tile_codes is empty")

    return MissionMap(
        map_id=str(data.get("map_id") or data.get("id") or "unnamed"),
        width=width,
        height=height,
        rows=tuple(rows_raw),
        tile_codes=codes,
        doors=tuple(
            Door(cell=_cell(d.get("cell")), state=str(d.get("state", "")), note=str(d.get("note", "")))
            for d in (data.get("doors") or [])
        ),
        agents=tuple(dict(a) for a in (data.get("agents") or [])),
        leader_ref=str(data.get("leader_ref", "")),
        interactables=tuple(
            Interactable(
                id=str(i.get("id", "")),
                kind=str(i.get("kind", "")),
                cell=_cell(i.get("cell")),
                label=str(i.get("label", "")),
                network_ref=str(i.get("network_ref", "")),
                note=str(i.get("note", "")),
            )
            for i in (data.get("interactables") or [])
        ),
        objectives=tuple(
            Objective(
                id=str(o.get("id", "")),
                kind=str(o.get("kind", "")),
                interactable_ref=str(o.get("interactable_ref", "")),
                cell=_cell(o["cell"]) if o.get("cell") is not None else None,
                note=str(o.get("note", "")),
            )
            for o in (data.get("objectives") or [])
        ),
        overlays=tuple(dict(o) for o in (data.get("overlays") or [])),
        status=str(data.get("status", "")),
        sources=tuple(str(s) for s in (data.get("sources") or [])),
        provenance=dict(data.get("provenance") or {}),
        declared_mechanic_keys=_mechanic_keys(data),
    )


def load_mission_map(path: Path | str | None = None) -> MissionMap:
    """Read a mission map from disk (default: the municipal-archive reference instance)."""
    target = Path(path) if path is not None else DATA_PATH
    try:
        raw = json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MissionMapError(f"mission map not found: {target}") from exc
    except json.JSONDecodeError as exc:
        raise MissionMapError(f"mission map is not valid JSON: {target}: {exc}") from exc
    return mission_map_from_dict(raw)
