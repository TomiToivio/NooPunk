"""Executable contracts for the tactical mission map (issue #515, technical-spike milestone 1).

Code-only, per `AGENTS.md` and issue #271: these exercise the **schema, its validator and the
pathfinder**, never lore or rulebook prose. They are the evidence that the spike's "grid/tile format
and mission-data schema" deliverable is real rather than a paragraph claiming it is.

The map deliberately models no rule. A test asserts that by parsing the module and scanning its
identifiers, because the prohibition may be stated in prose but must not appear as code.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_mission_map.py"
"""

from __future__ import annotations

import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game import mission_map as mm  # noqa: E402
from strategy_game.mission_map import (  # noqa: E402
    AGENT_COUNT,
    MISSION_MAP_FORMAT,
    MISSION_MAP_VERSION,
    MissionMapError,
    load_mission_map,
    mission_map_from_dict,
)

DATA = ROOT / "strategy_game" / "data" / "mission_map_municipal_archive.json"

#: Tile vocabulary used by the small purpose-built maps below: wall, floor, door, exit.
CODES = {
    "#": {"name": "wall", "walkable": False},
    ".": {"name": "floor", "walkable": True},
    "+": {"name": "door", "walkable": "when_open"},
    "X": {"name": "exit", "walkable": True},
}


def _map(rows, *, doors=(), agents=None, extra=None):
    """Build a minimal well-formed map around the given rows."""
    height = len(rows)
    width = len(rows[0])
    if agents is None:
        agents = [
            {"agent_ref": f"agent.{i}", "cell": [1 + i, height - 2]} for i in range(AGENT_COUNT)
        ]
    payload = {
        "format": MISSION_MAP_FORMAT,
        "version": MISSION_MAP_VERSION,
        "grid": {"width": width, "height": height},
        "tile_codes": dict(CODES),
        "rows": list(rows),
        "doors": [{"cell": list(c), "state": s} for c, s in doors],
        "agents": agents,
        "leader_ref": "agent.leader",
        "interactables": [],
        "objectives": [],
        "overlays": [],
    }
    payload.update(extra or {})
    return mission_map_from_dict(payload)


class ReferenceMapContracts(unittest.TestCase):
    """The shipped instance must be internally consistent and completable."""

    def test_reference_map_has_no_defects(self):
        self.assertEqual(load_mission_map().problems(), ())

    def test_grid_is_the_requested_prototype_size(self):
        m = load_mission_map()
        self.assertEqual((m.width, m.height), (20, 20))
        self.assertEqual(len(m.rows), 20)
        for row in m.rows:
            self.assertEqual(len(row), 20)

    def test_four_agents_deploy_and_the_leader_does_not(self):
        m = load_mission_map()
        self.assertEqual(len(m.agents), AGENT_COUNT)
        refs = [a["agent_ref"] for a in m.agents]
        self.assertEqual(len(set(refs)), AGENT_COUNT)
        self.assertNotIn(m.leader_ref, refs, "the leader must not occupy a fifth squad slot")
        for agent in m.agents:
            self.assertTrue(m.walkable(tuple(agent["cell"])))

    def test_every_objective_is_reachable_from_a_deployed_agent(self):
        m = load_mission_map()
        reachable = set()
        for agent in m.agents:
            reachable |= set(m.reachable_from(tuple(agent["cell"])))
        for objective in m.objectives:
            if objective.kind == "exit":
                self.assertIn(objective.cell, reachable, objective.id)
                continue
            item = m.interactable(objective.interactable_ref)
            if item is None:
                self.fail(f"{objective.id} references a missing interactable")
            approaches = m.approach_cells(item.id)
            self.assertTrue(approaches, f"{item.id} has no approach cell")
            self.assertTrue(
                any(cell in reachable for cell in approaches),
                f"{objective.id} cannot be reached",
            )

    def test_the_whole_reference_map_is_connected(self):
        m = load_mission_map()
        start = tuple(m.agents[0]["cell"])
        self.assertEqual(len(m.reachable_from(start)), len(m.walkable_cells()))


class GeometryContracts(unittest.TestCase):
    def test_a_path_crosses_only_walkable_cells_without_diagonals(self):
        m = load_mission_map()
        start, goal = (2, 18), (4, 4)
        route = m.path(start, goal)
        self.assertTrue(route, "the reference map should connect the entrance to the west wing")
        self.assertEqual(route[0], start)
        self.assertEqual(route[-1], goal)
        for cell in route:
            self.assertTrue(m.walkable(cell), f"{cell} is not walkable")
        for first, second in zip(route, route[1:]):
            dx = abs(first[0] - second[0])
            dy = abs(first[1] - second[1])
            self.assertEqual(dx + dy, 1, f"{first}->{second} is not one orthogonal step")

    def test_paths_are_deterministic(self):
        m = load_mission_map()
        self.assertEqual(m.path((2, 18), (7, 15)), m.path((2, 18), (7, 15)))

    def test_an_unreachable_target_reports_no_path_rather_than_inventing_one(self):
        # a sealed room: no door at all, so nothing can enter it
        rows = [
            "######",
            "#....#",
            "#.##.#",
            "#.##.#",
            "#....#",
            "######",
        ]
        m = _map(rows)
        self.assertTrue(m.walkable((1, 1)))
        self.assertEqual(m.path((1, 1), (2, 2)), ())
        self.assertNotIn((2, 2), m.reachable_from((1, 1)))

    def test_out_of_bounds_is_never_walkable_or_routable(self):
        m = load_mission_map()
        for cell in ((-1, 5), (5, -1), (20, 5), (5, 20)):
            self.assertFalse(m.walkable(cell))
            self.assertEqual(m.path((2, 18), cell), ())


class DoorContracts(unittest.TestCase):
    ROWS = [
        "#######",
        "#..#..#",
        "#..+..#",
        "#..#..#",
        "#######",
    ]

    def test_a_closed_door_blocks_and_an_open_door_passes(self):
        closed = _map(self.ROWS, doors=[([3, 2], "closed")])
        self.assertFalse(closed.walkable((3, 2)))
        self.assertEqual(closed.path((1, 1), (5, 1)), ())

        opened = _map(self.ROWS, doors=[([3, 2], "open")])
        self.assertTrue(opened.walkable((3, 2)))
        self.assertTrue(opened.path((1, 1), (5, 1)))

    def test_a_door_cell_without_a_record_is_reported(self):
        m = _map(self.ROWS, doors=())
        self.assertTrue(any("no door record" in p for p in m.problems()))

    def test_a_door_record_off_the_door_cell_is_reported(self):
        m = _map(self.ROWS, doors=[([1, 1], "open")])
        self.assertTrue(any("not on a door cell" in p for p in m.problems()))


class VocabularyContracts(unittest.TestCase):
    def test_an_undeclared_tile_character_is_a_defect(self):
        m = _map(["#####", "#.Q.#", "#####"])
        self.assertTrue(any("undeclared tile" in p for p in m.problems()))

    def test_an_unsealed_boundary_is_a_defect(self):
        m = _map(["#####", "#...#", "##.##"])
        self.assertTrue(any("boundary cell" in p for p in m.problems()))

    def test_a_short_row_is_a_defect(self):
        m = _map(["#####", "#...#", "####"])
        self.assertTrue(any("cells wide" in p for p in m.problems()))

    def test_wrong_format_and_version_are_refused_outright(self):
        raw = json.loads(DATA.read_text(encoding="utf-8"))
        for field_name, value in (("format", "noopunk.something.else"), ("version", 99)):
            broken = dict(raw)
            broken[field_name] = value
            with self.assertRaises(MissionMapError):
                mission_map_from_dict(broken)

    def test_valid_json_that_is_not_a_map_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "map.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(MissionMapError):
                load_mission_map(path)
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(MissionMapError):
                load_mission_map(path)


class AgentContracts(unittest.TestCase):
    ROWS = ["######", "#....#", "#....#", "######"]

    def test_the_leader_as_a_fifth_member_is_a_defect(self):
        agents = [{"agent_ref": f"agent.{i}", "cell": [1 + i, 1]} for i in range(3)]
        agents.append({"agent_ref": "agent.leader", "cell": [4, 1]})
        m = _map(self.ROWS, agents=agents)
        self.assertTrue(any("leader is deployed" in p for p in m.problems()))

    def test_wrong_squad_size_and_stacked_agents_are_defects(self):
        two = [{"agent_ref": "agent.a", "cell": [1, 1]}, {"agent_ref": "agent.b", "cell": [2, 1]}]
        self.assertTrue(any("deployed agents" in p for p in _map(self.ROWS, agents=two).problems()))

        stacked = [{"agent_ref": f"agent.{i}", "cell": [1, 1]} for i in range(AGENT_COUNT)]
        self.assertTrue(any("share a cell" in p for p in _map(self.ROWS, agents=stacked).problems()))

    def test_an_agent_on_a_wall_is_a_defect(self):
        agents = [{"agent_ref": f"agent.{i}", "cell": [1, 1]} for i in range(AGENT_COUNT)]
        agents[0]["cell"] = [0, 0]
        m = _map(self.ROWS, agents=agents)
        self.assertTrue(any("non-walkable cell" in p for p in m.problems()))


class InteractableContracts(unittest.TestCase):
    ROWS = ["#######", "#.....#", "#.....#", "#######"]

    def test_an_interactable_must_sit_on_its_own_kind_of_tile(self):
        extra = {
            "interactables": [{"id": "person.x", "kind": "person", "cell": [2, 1]}],
        }
        m = _map(self.ROWS, extra=extra)
        self.assertTrue(any("sits on tile" in p for p in m.problems()))

    def test_an_objective_naming_a_missing_interactable_is_a_defect(self):
        extra = {
            "interactables": [],
            "objectives": [{"id": "objective.x", "kind": "evidence", "interactable_ref": "nope"}],
        }
        m = _map(self.ROWS, extra=extra)
        self.assertTrue(any("unknown interactable" in p for p in m.problems()))


class OverlayContracts(unittest.TestCase):
    def test_overlays_are_display_only_and_never_make_a_wall_walkable(self):
        rows = ["######", "#....#", "#.##.#", "#....#", "######"]
        extra = {
            "overlays": [
                {"cell": [2, 2], "layer": "astral"},
                {"cell": [2, 2], "layer": "cyber"},
            ]
        }
        m = _map(rows, extra=extra)
        self.assertFalse(m.walkable((2, 2)), "an overlay must not create a passage")
        self.assertEqual(m.problems(), ())

    def test_an_unknown_overlay_layer_is_a_defect(self):
        extra = {"overlays": [{"cell": [2, 1], "layer": "dreamtime"}]}
        m = _map(["#######", "#.....#", "#.....#", "#######"], extra=extra)
        self.assertTrue(any("unknown layer" in p for p in m.problems()))


class NoRulesContracts(unittest.TestCase):
    """The map describes place. A rule that drifts into the data is a defect, not a feature."""

    def test_map_data_declares_no_mechanic_keys(self):
        raw = json.loads(DATA.read_text(encoding="utf-8"))

        def keys(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    yield str(key).lower()
                    yield from keys(value)
            elif isinstance(node, list):
                for value in node:
                    yield from keys(value)

        forbidden = set(mm._FORBIDDEN_KEYS)
        self.assertEqual(sorted(forbidden & set(keys(raw))), [])

    def test_the_module_contains_no_rule_identifiers(self):
        tree = ast.parse((ROOT / "strategy_game" / "mission_map.py").read_text(encoding="utf-8"))
        names = {
            node.id.lower() if isinstance(node, ast.Name) else node.attr.lower()
            for node in ast.walk(tree)
            if isinstance(node, (ast.Name, ast.Attribute))
        }
        names |= {
            node.name.lower()
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        }
        banned = ("damage", "hit_point", "initiative", "action_point", "difficulty", "morale", "modifier")
        offenders = sorted(n for n in names if any(token in n for token in banned))
        self.assertEqual(offenders, [], "the pathfinder must not grow rule logic")

    def test_a_map_carrying_a_damage_key_is_reported(self):
        extra = {"interactables": [{"id": "terminal.x", "kind": "terminal", "cell": [2, 1]}]}
        raw_extra = {"damage": 3}
        m = _map(["#####", "#.T.#", "#####"], extra={**extra, **raw_extra})
        self.assertTrue(any("mechanic key" in p for p in m.problems()))


if __name__ == "__main__":
    unittest.main()
