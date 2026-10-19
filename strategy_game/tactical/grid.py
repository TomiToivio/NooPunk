"""A renderer-independent tile grid and its pathfinding (issue #515, first milestone).

Issue #515 asks for a *"minimalist, top-down 8-bit retro pixel-art tactical map"* that serves both
turn-based squad combat and investigation quests, and it asks for the spike to settle **"grid/tile
format and mission-data schema"** before any renderer is chosen. This module is the grid half of that
answer, and it is deliberately the smallest thing that a tactical UI needs:

* a rectangular grid of **floor / wall / door** cells, declared as ASCII rows so a human can edit it
  and any renderer can convert it to its own tile layer;
* **four-neighbour pathfinding** that returns a path or a legible refusal, with a fixed neighbour
  order so the same grid always yields the same path;
* nothing else. No sprite, no pixel, no camera, no draw order, no animation, no visibility cone, no
  movement cost, no turn structure.

Why this is not a rule
----------------------

A grid states what is *spatially true*: which cells exist, which are passable, which are doors. It
resolves nothing and rates nothing. Movement **cost** is a rules question and is not answered here:
:meth:`Grid.path` counts steps only because a shortest path is the only sensible click-to-move answer,
and it prices a step at nothing. ``strategy_game/RULEBOOK.md`` keeps its *no rules approved* status.

Why doors are a tile kind and not an object
-------------------------------------------

#515 names "walls, doors" as the prototype's obstacle vocabulary, so a door is a cell that a route may
pass through. Whether a *closed* door blocks (and what opening one costs) is not decided by this
spike, so :attr:`Grid.closed_doors` is **declared state**, not a mechanic: a grid may be declared with
doors shut, pathfinding respects them, and no operation in this package opens one. A later milestone
that makes doors interactive needs an author ruling on its action cost.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum

__all__ = [
    "LEGEND",
    "TILE_GLYPHS",
    "Cell",
    "Grid",
    "GridError",
    "PathResult",
    "TileKind",
]

#: The one glyph per tile kind. This is the interchange format: a mission's rows are these
#: characters, one per cell, so a Tiled tileset or a Godot TileSet is a mapping from glyph to
#: tile, not a second description of the map. Filled below, once ``TileKind`` exists.
LEGEND: dict[str, TileKind] = {}


class GridError(ValueError):
    """A grid document or operation the tile format does not allow."""


class TileKind(str, Enum):
    """What occupies one cell. Three kinds are all #515's prototype needs."""

    FLOOR = "floor"
    WALL = "wall"
    DOOR = "door"


TILE_GLYPHS: dict[TileKind, str] = {
    TileKind.FLOOR: ".",
    TileKind.WALL: "#",
    TileKind.DOOR: "+",
}
LEGEND.update({glyph: kind for kind, glyph in TILE_GLYPHS.items()})


def _int_pair(value: object, what: str) -> tuple[int, int]:
    if isinstance(value, (list, tuple)) and len(value) == 2:
        row, col = value
        if isinstance(row, int) and isinstance(col, int) and not isinstance(row, bool):
            return row, col
    raise GridError(f"{what} must be a [row, col] pair of integers, got {value!r}")


@dataclass(frozen=True, order=True)
class Cell:
    """One grid cell, addressed ``(row, col)`` from the top-left corner.

    Out-of-bounds coordinates are constructible on purpose: a caller that asks for ``(40, 3)`` on a
    20x20 grid deserves a refusal that names the cell, not an exception from the coordinate type.
    ``order=True`` gives a deterministic sort for stable reports and tie-breaks.
    """

    row: int
    col: int

    @classmethod
    def from_pair(cls, value: object, *, what: str = "a cell") -> Cell:
        row, col = _int_pair(value, what)
        return cls(row, col)

    def to_pair(self) -> list[int]:
        return [self.row, self.col]

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def neighbours(self) -> tuple[Cell, ...]:
        """The four orthogonal neighbours, in a fixed order: north, east, south, west."""
        return (
            Cell(self.row - 1, self.col),
            Cell(self.row, self.col + 1),
            Cell(self.row + 1, self.col),
            Cell(self.row, self.col - 1),
        )


@dataclass(frozen=True)
class PathResult:
    """The answer to one path request: a path, or a refusal with a reason a player can read.

    ``steps`` excludes the start cell and includes the destination, so ``steps[-1]`` is where the
    character ends up and ``len(steps)`` is the distance. A successful empty path means the request
    was a no-op (start equals destination); callers decide whether that is worth an action.
    """

    ok: bool
    steps: tuple[Cell, ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class Grid:
    """A rectangular tile grid: the map, as data, with no renderer attached to it.

    ``tiles`` is row-major — ``tiles[row][col]`` — and is what :meth:`from_rows` builds from the
    ASCII form the mission-data schema carries.
    """

    width: int
    height: int
    tiles: tuple[tuple[TileKind, ...], ...]
    #: Doors declared shut. Pathfinding treats them as walls; nothing in this package opens one.
    closed_doors: frozenset[Cell] = frozenset()

    def __post_init__(self) -> None:
        if self.width < 1 or self.height < 1:
            raise GridError(f"a grid needs positive width and height, got {self.width}x{self.height}")
        if len(self.tiles) != self.height:
            raise GridError(f"grid declares height {self.height} but {len(self.tiles)} rows")
        for index, row in enumerate(self.tiles):
            if len(row) != self.width:
                raise GridError(
                    f"grid row {index} has {len(row)} cells, expected width {self.width}"
                )
            for cell_kind in row:
                if not isinstance(cell_kind, TileKind):
                    raise GridError(f"grid row {index} carries {cell_kind!r}, not a TileKind")
        for cell in self.closed_doors:
            if not isinstance(cell, Cell):
                raise GridError("closed doors are Cell records")
            if not self.in_bounds(cell):
                raise GridError(f"closed door {cell} is outside the {self.width}x{self.height} grid")
            if self.tile(cell) is not TileKind.DOOR:
                raise GridError(f"closed door {cell} is not a door cell")

    # -- reading ---------------------------------------------------------------

    def in_bounds(self, cell: Cell) -> bool:
        return 0 <= cell.row < self.height and 0 <= cell.col < self.width

    def tile(self, cell: Cell) -> TileKind | None:
        """The tile at ``cell``, or ``None`` outside the grid."""
        if not self.in_bounds(cell):
            return None
        return self.tiles[cell.row][cell.col]

    def is_passable(self, cell: Cell) -> bool:
        """Whether a route may enter ``cell``: floor, or a door that is not declared shut."""
        kind = self.tile(cell)
        if kind is TileKind.FLOOR:
            return True
        if kind is TileKind.DOOR:
            return cell not in self.closed_doors
        return False

    def refusal(self, cell: Cell) -> str:
        """Why a route may not enter ``cell`` — empty text when it may.

        The wording is the refusal a click-to-move request shows the player, so it names the cell
        and the obstruction rather than a code.
        """
        kind = self.tile(cell)
        if kind is None:
            return f"{cell} is outside the {self.width}x{self.height} grid"
        if kind is TileKind.WALL:
            return f"a wall blocks {cell}"
        if kind is TileKind.DOOR and cell in self.closed_doors:
            return f"the door at {cell} is closed"
        return ""

    def passable_cells(self) -> tuple[Cell, ...]:
        return tuple(
            Cell(row, col)
            for row in range(self.height)
            for col in range(self.width)
            if self.is_passable(Cell(row, col))
        )

    def neighbours(self, cell: Cell) -> tuple[Cell, ...]:
        """The passable orthogonal neighbours of ``cell``, in :meth:`Cell.neighbours` order."""
        return tuple(n for n in cell.neighbours() if self.is_passable(n))

    # -- pathfinding -----------------------------------------------------------

    def path(self, start: Cell, goal: Cell) -> PathResult:
        """The shortest four-neighbour route from ``start`` to ``goal``, or a refusal.

        Breadth-first search, so the result is a shortest path in steps; the neighbour order is fixed,
        so equal-length routes always resolve the same way and a replay needs no tie-break rule. The
        search is exhaustive over passable cells and does **not** know about other characters:
        occupancy is a mission-session concern, not a property of the map.
        """
        start_refusal = self.refusal(start)
        if start_refusal:
            return PathResult(False, (), f"cannot start a route at {start}: {start_refusal}")
        goal_refusal = self.refusal(goal)
        if goal_refusal:
            return PathResult(False, (), f"cannot route to {goal}: {goal_refusal}")
        if start == goal:
            return PathResult(True, ())

        parents: dict[Cell, Cell | None] = {start: None}
        queue: deque[Cell] = deque([start])
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for neighbour in self.neighbours(current):
                if neighbour not in parents:
                    parents[neighbour] = current
                    queue.append(neighbour)

        if goal not in parents:
            return PathResult(
                False,
                (),
                f"no route from {start} to {goal}: walls and closed doors block every path "
                f"within the {self.width}x{self.height} grid",
            )

        steps: list[Cell] = []
        cursor: Cell | None = goal
        while cursor is not None and cursor != start:
            steps.append(cursor)
            cursor = parents[cursor]
        steps.reverse()
        return PathResult(True, tuple(steps))

    # -- interchange -----------------------------------------------------------

    def ascii_rows(self) -> tuple[str, ...]:
        """The grid as the mission-data schema declares it: one glyph per cell, one string per row."""
        return tuple("".join(TILE_GLYPHS[kind] for kind in row) for row in self.tiles)

    def to_dict(self) -> dict[str, object]:
        """The JSON form of the grid section of a mission document."""
        payload: dict[str, object] = {
            "width": self.width,
            "height": self.height,
            "legend": {glyph: kind.value for glyph, kind in LEGEND.items()},
            "rows": list(self.ascii_rows()),
        }
        if self.closed_doors:
            payload["closed_doors"] = [cell.to_pair() for cell in sorted(self.closed_doors)]
        return payload

    @classmethod
    def from_rows(
        cls,
        rows: object,
        *,
        legend: object = None,
        closed_doors: object = None,
        width: object = None,
        height: object = None,
    ) -> Grid:
        """Build a grid from ASCII rows, refusing anything the legend cannot read.

        ``width`` and ``height`` are optional and, when supplied, must agree with the rows — a
        declared size that disagrees with the drawing is a defect, never a resize.
        """
        if not isinstance(rows, (list, tuple)) or not rows:
            raise GridError("a grid needs a non-empty list of rows")
        glyphs: dict[str, TileKind] = dict(LEGEND)
        if legend is not None:
            if not isinstance(legend, dict):
                raise GridError("a legend must be an object of glyph -> tile kind")
            for glyph, name in legend.items():
                try:
                    glyphs[str(glyph)] = TileKind(str(getattr(name, "value", name)))
                except ValueError as exc:
                    raise GridError(
                        f"legend glyph {glyph!r} names {name!r}, which is not one of "
                        f"{[kind.value for kind in TileKind]}"
                    ) from exc
        parsed: list[tuple[TileKind, ...]] = []
        for index, row in enumerate(rows):
            if not isinstance(row, str):
                raise GridError(f"grid row {index} is {type(row).__name__}, expected a string")
            if not row:
                raise GridError(f"grid row {index} is empty")
            line: list[TileKind] = []
            for col, glyph in enumerate(row):
                if glyph not in glyphs:
                    raise GridError(
                        f"grid row {index} column {col} carries {glyph!r}, which the legend does "
                        f"not define ({', '.join(sorted(glyphs))})"
                    )
                line.append(glyphs[glyph])
            parsed.append(tuple(line))
        row_widths = {len(row) for row in parsed}
        if len(row_widths) != 1:
            raise GridError(f"grid rows have differing widths: {sorted(row_widths)}")
        actual_width = row_widths.pop()
        actual_height = len(parsed)
        for label, declared, actual in (
            ("width", width, actual_width),
            ("height", height, actual_height),
        ):
            if declared is None:
                continue
            if not isinstance(declared, int) or isinstance(declared, bool) or declared < 1:
                raise GridError(f"grid declares {label} {declared!r}, which is not a positive integer")
            if declared != actual:
                raise GridError(f"grid declares {label} {declared} but its rows give {actual}")
        if closed_doors is not None and not isinstance(closed_doors, (list, tuple)):
            raise GridError("closed_doors must be a list of [row, col] pairs")
        doors: set[Cell] = set()
        for pair in closed_doors or ():
            doors.add(Cell.from_pair(pair, what="a closed door"))
        return cls(
            width=actual_width,
            height=actual_height,
            tiles=tuple(parsed),
            closed_doors=frozenset(doors),
        )

    @classmethod
    def from_dict(cls, payload: object) -> Grid:
        if not isinstance(payload, dict):
            raise GridError(f"a grid must be an object, got {type(payload).__name__}")
        return cls.from_rows(
            payload.get("rows"),
            legend=payload.get("legend"),
            closed_doors=payload.get("closed_doors"),
            width=payload.get("width"),
            height=payload.get("height"),
        )
