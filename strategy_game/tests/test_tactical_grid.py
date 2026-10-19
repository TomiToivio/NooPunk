"""Executable contracts for the tactical grid and its pathfinding (issue #515's spike).

Code-only, per ``AGENTS.md``: nothing here asserts prose. It exercises the tile format and the
pathfinder — walls, doors, shut doors, unreachable pockets, out-of-bounds targets, determinism — and
the 20x20 fixture that the mission schema packages.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap
    sys.path.insert(0, str(ROOT))

from strategy_game.tactical.grid import (
    LEGEND,
    TILE_GLYPHS,
    Cell,
    Grid,
    GridError,
    TileKind,
)
from strategy_game.tactical.mission import load_mission


def _grid(*rows: str, closed: tuple[Cell, ...] = ()) -> Grid:
    return Grid.from_rows(list(rows), closed_doors=[cell.to_pair() for cell in closed])


class TileFormatTests(unittest.TestCase):
    def test_legend_and_glyphs_are_one_mapping(self):
        self.assertEqual(LEGEND, {".": TileKind.FLOOR, "#": TileKind.WALL, "+": TileKind.DOOR})
        for kind, glyph in TILE_GLYPHS.items():
            self.assertIs(LEGEND[glyph], kind)

    def test_ascii_rows_round_trip(self):
        grid = _grid("####", "#..#", "#+.#", "####")
        again = Grid.from_rows(grid.ascii_rows())
        self.assertEqual(again, grid)

    def test_ascii_rows_round_trip_keeps_closed_doors(self):
        grid = _grid("#####", "#.+.#", "#####", closed=(Cell(1, 2),))
        self.assertEqual(Grid.from_rows(grid.ascii_rows(), closed_doors=[[1, 2]]), grid)

    def test_unknown_glyph_is_refused_by_position(self):
        with self.assertRaises(GridError) as raised:
            Grid.from_rows(["###", "#x#", "###"])
        self.assertIn("'x'", str(raised.exception))
        self.assertIn("row 1 column 1", str(raised.exception))

    def test_rows_of_differing_width_are_refused(self):
        with self.assertRaises(GridError):
            Grid.from_rows(["###", "##"])

    def test_a_declared_width_must_agree_with_the_rows(self):
        with self.assertRaises(GridError) as raised:
            Grid.from_rows(["###", "###"], width=4)
        self.assertIn("width", str(raised.exception))

    def test_a_closed_door_must_be_a_door(self):
        with self.assertRaises(GridError) as raised:
            Grid.from_rows(["###", "#.#", "###"], closed_doors=[[1, 1]])
        self.assertIn("not a door", str(raised.exception))

    def test_a_closed_door_outside_the_grid_is_refused(self):
        with self.assertRaises(GridError):
            Grid.from_rows(["###", "#+#", "###"], closed_doors=[[9, 9]])

    def test_unknown_tile_kind_in_a_legend_is_refused(self):
        with self.assertRaises(GridError) as raised:
            Grid.from_rows(["#"], legend={"#": "lava"})
        self.assertIn("lava", str(raised.exception))


class NeighbourTests(unittest.TestCase):
    def test_neighbours_are_orthogonal_and_in_a_fixed_order(self):
        self.assertEqual(
            Cell(2, 2).neighbours(),
            (Cell(1, 2), Cell(2, 3), Cell(3, 2), Cell(2, 1)),
        )

    def test_only_passable_neighbours_are_returned(self):
        grid = _grid("###", "#+#", "###")
        self.assertEqual(grid.neighbours(Cell(1, 1)), ())
        self.assertTrue(grid.is_passable(Cell(1, 1)))
        self.assertEqual(grid.neighbours(Cell(0, 0)), ())


class PathfindingTests(unittest.TestCase):
    # A wall straight between start and goal, with a way round underneath.
    AROUND = ("#####", "#.#.#", "#.#.#", "#...#", "#####")

    def test_path_goes_around_a_wall(self):
        grid = _grid(*self.AROUND)
        result = grid.path(Cell(1, 1), Cell(1, 3))
        self.assertTrue(result.ok, result.reason)
        self.assertEqual(len(result.steps), 6)
        self.assertEqual(result.steps[-1], Cell(1, 3))
        self.assertNotIn(Cell(1, 2), result.steps)
        for cell in result.steps:
            self.assertTrue(grid.is_passable(cell))

    def test_path_passes_through_a_door(self):
        grid = _grid("#######", "#..#..#", "#..+..#", "#..#..#", "#######")
        result = grid.path(Cell(1, 1), Cell(1, 5))
        self.assertTrue(result.ok, result.reason)
        self.assertIn(Cell(2, 3), result.steps)
        self.assertEqual(len(result.steps), 6)

    def test_a_closed_door_blocks_the_route_and_says_why(self):
        grid = _grid("#######", "#..#..#", "#..+..#", "#..#..#", "#######", closed=(Cell(2, 3),))
        result = grid.path(Cell(1, 1), Cell(1, 5))
        self.assertFalse(result.ok)
        self.assertIn("no route", result.reason)
        self.assertIn("closed doors", result.reason)

    def test_a_closed_door_as_the_destination_is_named(self):
        grid = _grid("#######", "#..#..#", "#..+..#", "#..#..#", "#######", closed=(Cell(2, 3),))
        result = grid.path(Cell(1, 1), Cell(2, 3))
        self.assertFalse(result.ok)
        self.assertIn("the door at (2,3) is closed", result.reason)

    def test_an_unreachable_pocket_is_refused_with_a_legible_reason(self):
        # The centre cell (3,3) is walled in on all four sides.
        grid = _grid(
            "#######",
            "#.....#",
            "#.###.#",
            "#.#.#.#",
            "#.###.#",
            "#.....#",
            "#######",
        )
        self.assertTrue(grid.is_passable(Cell(3, 3)))
        result = grid.path(Cell(1, 1), Cell(3, 3))
        self.assertFalse(result.ok)
        self.assertIn("no route from (1,1) to (3,3)", result.reason)
        self.assertIn("block every path", result.reason)

    def test_a_wall_as_the_destination_is_named(self):
        grid = _grid(*self.AROUND)
        result = grid.path(Cell(1, 1), Cell(1, 2))
        self.assertFalse(result.ok)
        self.assertEqual(result.reason, "cannot route to (1,2): a wall blocks (1,2)")

    def test_a_target_outside_the_grid_is_named(self):
        grid = _grid(*self.AROUND)
        result = grid.path(Cell(1, 1), Cell(99, 0))
        self.assertFalse(result.ok)
        self.assertIn("outside the 5x5 grid", result.reason)

    def test_a_start_outside_the_grid_is_named(self):
        grid = _grid(*self.AROUND)
        result = grid.path(Cell(-1, 0), Cell(1, 1))
        self.assertFalse(result.ok)
        self.assertIn("cannot start a route", result.reason)

    def test_a_request_to_stay_put_succeeds_with_no_steps(self):
        grid = _grid(*self.AROUND)
        result = grid.path(Cell(1, 1), Cell(1, 1))
        self.assertTrue(result.ok)
        self.assertEqual(result.steps, ())

    def test_the_same_request_always_returns_the_same_path(self):
        grid = _grid(*self.AROUND)
        first = grid.path(Cell(1, 1), Cell(3, 3))
        second = grid.path(Cell(1, 1), Cell(3, 3))
        self.assertEqual(first, second)

    def test_the_path_is_a_shortest_path(self):
        grid = _grid(*self.AROUND)
        for goal in (Cell(1, 3), Cell(3, 3), Cell(3, 1)):
            result = grid.path(Cell(1, 1), goal)
            self.assertTrue(result.ok, result.reason)
            # Independent breadth-first distance, counted here rather than trusted.
            distance = {Cell(1, 1): 0}
            queue = [Cell(1, 1)]
            while queue:
                current = queue.pop(0)
                for neighbour in grid.neighbours(current):
                    if neighbour not in distance:
                        distance[neighbour] = distance[current] + 1
                        queue.append(neighbour)
            self.assertEqual(len(result.steps), distance[goal])


class FixtureGridTests(unittest.TestCase):
    def test_the_packaged_mission_is_a_20_by_20_grid(self):
        grid = load_mission().grid
        self.assertEqual((grid.width, grid.height), (20, 20))
        self.assertEqual(len(grid.ascii_rows()), 20)
        self.assertTrue(all(len(row) == 20 for row in grid.ascii_rows()))

    def test_the_fixture_is_enclosed_by_walls(self):
        grid = load_mission().grid
        for col in range(grid.width):
            self.assertIs(grid.tile(Cell(0, col)), TileKind.WALL)
            self.assertIs(grid.tile(Cell(grid.height - 1, col)), TileKind.WALL)
        for row in range(grid.height):
            self.assertIs(grid.tile(Cell(row, 0)), TileKind.WALL)
            self.assertIs(grid.tile(Cell(row, grid.width - 1)), TileKind.WALL)

    def test_the_fixture_has_doors_and_the_annex_is_only_reachable_through_one(self):
        grid = load_mission().grid
        doors = [cell for cell in grid.passable_cells() if grid.tile(cell) is TileKind.DOOR]
        self.assertTrue(doors, "the fixture declares no doors")
        path = grid.path(Cell(17, 10), Cell(5, 12))
        self.assertTrue(path.ok, path.reason)
        self.assertTrue(
            any(grid.tile(cell) is TileKind.DOOR for cell in path.steps),
            "the route into the annex passes through no door",
        )

    def test_the_fixture_grid_round_trips_through_its_json_form(self):
        grid = load_mission().grid
        self.assertEqual(Grid.from_dict(grid.to_dict()), grid)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
