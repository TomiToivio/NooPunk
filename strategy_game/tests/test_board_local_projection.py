"""Code contracts for the first non-empty board (issue #347, work item 3).

Executable-code tests only, per ``AGENTS.md`` and issue #271. They exercise the projection from the
local slice onto the layered board, the declared binding, the cosmetic layout and the two exclusions
that matter: **no number reaches the board**, and **no endpoint is invented**.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import copy
import dataclasses
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap, mirrors the sibling test modules
    sys.path.insert(0, str(ROOT))

from strategy_game.tabletop import (  # noqa: E402
    BOARD_BINDING_DATA,
    BOARD_BINDING_FORMAT,
    Board,
    BoardBindingError,
    BoardEdge,
    BoardNode,
    BoardPiece,
    EdgeKind,
    Layout,
    board_from_local_slice,
    layout_from_slice_binding,
    load_board_binding,
    local_slice_board,
)
from strategy_game.tabletop.board import EDGE_KINDS  # noqa: E402
from strategy_game.tabletop.serialization import TableState, load_table, save_table  # noqa: E402

SLICE_DATA = BOARD_BINDING_DATA.parent / "ukweli_local.json"


def _slice() -> dict:
    return json.loads(SLICE_DATA.read_text(encoding="utf-8"))


def _binding() -> dict:
    return load_board_binding()


def _board() -> Board:
    return board_from_local_slice(_slice(), _binding())


def _numbers(value: object) -> list[object]:
    """Every bool-free number anywhere in a payload."""
    found: list[object] = []
    if isinstance(value, bool):
        return found
    if isinstance(value, (int, float)):
        return [value]
    if isinstance(value, dict):
        for item in value.values():
            found.extend(_numbers(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            found.extend(_numbers(item))
    return found


class BindingTests(unittest.TestCase):
    def test_the_binding_declares_its_format(self) -> None:
        self.assertTrue(BOARD_BINDING_DATA.is_file())
        self.assertEqual(_binding()["format"], BOARD_BINDING_FORMAT)

    def test_a_document_of_another_format_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wrong = Path(tmp) / "other.json"
            wrong.write_text(json.dumps({"format": "something.else"}), encoding="utf-8")
            with self.assertRaises(BoardBindingError):
                load_board_binding(wrong)

    def test_a_binding_missing_a_required_section_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            incomplete = Path(tmp) / "partial.json"
            incomplete.write_text(
                json.dumps({"format": BOARD_BINDING_FORMAT, "slice": "ukweli_local.json"}),
                encoding="utf-8",
            )
            with self.assertRaises(BoardBindingError):
                load_board_binding(incomplete)

    def test_the_binding_points_at_the_slice_the_crossover_actually_has(self) -> None:
        binding = _binding()
        self.assertEqual(binding["slice"], "ukweli_local.json")
        self.assertTrue((BOARD_BINDING_DATA.parent / binding["slice"]).is_file())

    def test_the_binding_reserves_what_is_not_projected(self) -> None:
        """The binding says out loud what a reader must not treat the board as carrying."""
        reserved = " ".join(_binding().get("reserved") or []).lower()
        for term in ("piece", "victory", "worldstate"):
            self.assertIn(term, reserved)


class NodeProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.slice = _slice()
        cls.board = _board()

    def test_the_node_set_is_exactly_locations_parties_and_leaders(self) -> None:
        expected = {
            str(item["id"])
            for family in ("locations", "parties", "leaders")
            for item in self.slice.get(family) or []
        }
        self.assertEqual(set(self.board.nodes), expected)
        self.assertEqual(len(self.board.nodes), 8 + 3 + 12)

    def test_identifiers_are_preserved_verbatim(self) -> None:
        self.assertIn("old_harbor", self.board.nodes)
        self.assertIn("outer_island", self.board.nodes)
        for identifier in self.board.nodes:
            self.assertNotIn(" ", identifier)
            self.assertEqual(identifier, identifier.lower())

    def test_labels_come_from_the_source_records(self) -> None:
        self.assertEqual(self.board.nodes["old_harbor"].label, "Old Harbor")
        self.assertEqual(self.board.nodes["cpu"].label, "Communist Party of Ukweli")

    def test_the_bindings_place_the_families_on_the_declared_layers(self) -> None:
        binding = _binding()["node_bindings"]
        for family in ("locations", "parties", "leaders"):
            rules = binding[family]
            for item in self.slice.get(family) or []:
                node = self.board.nodes[str(item["id"])]
                with self.subTest(family=family, node=node.identifier):
                    self.assertEqual(node.kind, rules["kind"])
                    self.assertEqual(node.layer, rules["layer"])

    def test_the_three_families_are_distinguishable_by_kind(self) -> None:
        kinds = {self.board.nodes[id_].kind for id_ in self.board.nodes}
        self.assertEqual(kinds, {"location", "faction", "person"})
        self.assertEqual(len(self.board.nodes_in_layer("physical")), 8)
        self.assertEqual(len(self.board.nodes_in_layer("social")), 15)

    def test_declared_tags_are_carried_and_quantities_are_not(self) -> None:
        self.assertEqual(self.board.nodes["old_harbor"].tags, ("heritage", "trade"))
        self.assertEqual(self.board.nodes["cpu1"].tags, ())

    def test_no_piece_is_invented(self) -> None:
        """The slice declares no token, so a leader is a node and not a marker on a location."""
        self.assertEqual(self.board.pieces, {})

    def test_a_record_without_an_id_is_skipped_rather_than_given_one(self) -> None:
        data = copy.deepcopy(self.slice)
        data["locations"] = data["locations"] + [{"label": "A place with no id"}]
        board = board_from_local_slice(data, _binding())
        self.assertEqual(len(board.nodes), len(self.board.nodes))
        self.assertNotIn("A place with no id", {node.label for node in board.nodes.values()})


class EdgeProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.slice = _slice()
        cls.board = _board()

    def test_routes_become_travel_edges_on_the_physical_layer(self) -> None:
        travel = [edge for edge in self.board.edges.values() if edge.kind is EdgeKind.TRAVEL]
        self.assertEqual(len(travel), len(self.slice["routes"]))
        for edge in travel:
            with self.subTest(edge=edge.identifier):
                self.assertEqual(edge.layer, "physical")

    def test_relationships_become_social_edges(self) -> None:
        social = [edge for edge in self.board.edges.values() if edge.layer == "social"]
        self.assertEqual(len(social), len(self.slice["relationships"]))
        for edge in social:
            with self.subTest(edge=edge.identifier):
                self.assertEqual(edge.kind, EdgeKind.COMMUNICATION)

    def test_every_edge_endpoint_is_a_node_the_projection_created(self) -> None:
        for edge in self.board.edges.values():
            for endpoint in edge.endpoints:
                with self.subTest(edge=edge.identifier, endpoint=endpoint):
                    self.assertIn(endpoint, self.board.nodes)
        self.board.validate()

    def test_edge_identifiers_are_derived_from_their_endpoints(self) -> None:
        """So an id survives a reordering of the source, which is what a persistent reference needs."""
        first = self.slice["routes"][0]
        self.assertIn(f"route-{first[0]}-{first[1]}", self.board.edges)

    def test_the_declared_tags_survive_on_the_relationship_edge(self) -> None:
        """Each relationship's own declared tags are kept on its own edge, verbatim."""
        for item in self.slice["relationships"]:
            edge = self.board.edges[f"relationship-{item['a']}-{item['b']}"]
            for tag in item.get("tags") or []:
                with self.subTest(identifier=edge.identifier, tag=tag):
                    self.assertIn(tag, edge.notes)

    def test_an_edge_whose_endpoint_is_not_projected_is_skipped_not_invented(self) -> None:
        data = copy.deepcopy(self.slice)
        data["routes"] = data["routes"] + [["old_harbor", "a_place_that_does_not_exist"]]
        board = board_from_local_slice(data, _binding())
        self.assertEqual(len(board.edges), len(self.board.edges))
        self.assertNotIn("a_place_that_does_not_exist", board.nodes)

    def test_a_declared_tag_mapping_types_the_relationship(self) -> None:
        """Type a relationship by declaring the mapping; a tag left out keeps the neutral default."""
        binding = copy.deepcopy(_binding())
        binding["edge_bindings"]["relationships"]["kind_from_tags"] = {"rivals": "opposition"}
        board = board_from_local_slice(copy.deepcopy(self.slice), binding)
        typed = board.edges["relationship-cpu1-uip1"]
        untyped = board.edges["relationship-cpu4-ulp4"]
        self.assertEqual(typed.kind, EdgeKind.OPPOSITION)
        self.assertEqual(untyped.kind, EdgeKind.COMMUNICATION)

    def test_an_undeclared_tag_mapping_is_not_guessed(self) -> None:
        binding = copy.deepcopy(_binding())
        binding["edge_bindings"]["relationships"]["kind_from_tags"] = {"rivals": "nemesis"}
        board = board_from_local_slice(_slice(), binding)
        social = [edge for edge in board.edges.values() if edge.layer == "social"]
        for edge in social:
            self.assertEqual(edge.kind, EdgeKind.COMMUNICATION)

    def test_no_route_or_relationship_is_dropped_silently_from_the_shipped_slice(self) -> None:
        self.assertEqual(
            len(self.board.edges), len(self.slice["routes"]) + len(self.slice["relationships"])
        )
        for edge in self.board.edges.values():
            self.assertIn(edge.kind.value, EDGE_KINDS)


class NoNumberTests(unittest.TestCase):
    """The one exclusion the audit is proud of: a prototype's number must not become a rule."""

    def test_no_board_dataclass_field_can_hold_a_quantity(self) -> None:
        for dataclass in (BoardNode, BoardEdge, BoardPiece):
            for item in dataclasses.fields(dataclass):
                with self.subTest(dataclass=dataclass.__name__, field=item.name):
                    self.assertNotIn(item.type, {"int", "float", "complex"})

    def test_the_projected_board_carries_no_number(self) -> None:
        self.assertEqual(_numbers(_board().to_dict()), [])

    def test_the_illustrative_slice_numbers_cannot_reach_the_board(self) -> None:
        """Change every quantity in the source and the board must be byte-identical."""
        data = copy.deepcopy(_slice())
        data["year"] = 9999
        for item in data["locations"]:
            item["pressure"] = 12345
        for item in data["leaders"]:
            item["skill"] = -99
        for item in data["relationships"]:
            item["trust"] = 777
        for item in data["shocks"]:
            item["legitimacy_delta"] = -12345
        self.assertEqual(
            board_from_local_slice(data, _binding()).to_dict(), _board().to_dict()
        )

    def test_the_board_itself_has_no_coordinate_field(self) -> None:
        self.assertNotIn("layout", _board().to_dict())
        self.assertNotIn("positions", _board().to_dict())

    def test_the_projection_does_not_mutate_the_slice(self) -> None:
        data = _slice()
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        board_from_local_slice(data, _binding())
        self.assertEqual(json.dumps(data, ensure_ascii=False, sort_keys=True), before)


class LayoutTests(unittest.TestCase):
    def test_the_committed_layout_covers_every_node_the_projection_creates(self) -> None:
        board, layout = local_slice_board()
        self.assertEqual(set(layout.positions), set(board.nodes))

    def test_layout_positions_are_numbers_beside_the_board_not_on_it(self) -> None:
        board, layout = local_slice_board()
        self.assertTrue(layout.positions)
        for node_id, point in layout.positions.items():
            with self.subTest(node=node_id):
                self.assertIn(node_id, board.nodes)
                self.assertEqual(len(point), 2)

    def test_a_layout_for_a_node_that_no_longer_exists_is_refused(self) -> None:
        binding = _binding()
        binding["layout"]["positions"]["a_node_that_is_gone"] = [0.0, 0.0]
        with self.assertRaises(BoardBindingError):
            layout_from_slice_binding(binding, _board())

    def test_a_layout_entry_may_be_missing_without_breaking_the_projection(self) -> None:
        binding = copy.deepcopy(_binding())
        binding["layout"]["positions"].pop("old_harbor")
        board = board_from_local_slice(_slice(), binding)
        layout = layout_from_slice_binding(binding, board)
        self.assertIsNone(layout.get("old_harbor"))
        self.assertEqual(len(layout.positions), len(board.nodes) - 1)

    def test_recomputing_a_layout_cannot_change_the_graph(self) -> None:
        board, layout = local_slice_board()
        before = json.dumps(board.to_dict(), sort_keys=True)
        other = Layout()
        for node_id in board.nodes:
            other.set(node_id, 0.0, 0.0)
        self.assertTrue(other.positions)
        self.assertEqual(json.dumps(board.to_dict(), sort_keys=True), before)
        self.assertNotEqual(layout.to_dict(), other.to_dict())


class RoundTripTests(unittest.TestCase):
    def test_the_projected_board_survives_save_and_load_unchanged(self) -> None:
        board, layout = local_slice_board()
        state = TableState(board=board)
        with tempfile.TemporaryDirectory() as tmp:
            first = save_table(state, Path(tmp) / "one.json")
            second = save_table(load_table(first), Path(tmp) / "two.json")
            self.assertEqual(first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8"))
            loaded = load_table(first)
        self.assertEqual(loaded.board.to_dict(), board.to_dict())
        loaded.board.validate()
        self.assertNotIn("layout", loaded.to_dict())

    def test_the_snapshot_is_byte_stable_across_two_saves(self) -> None:
        board, _layout = local_slice_board()
        state = TableState(board=board)
        with tempfile.TemporaryDirectory() as tmp:
            one = save_table(state, Path(tmp) / "a.json").read_text(encoding="utf-8")
            two = save_table(state, Path(tmp) / "b.json").read_text(encoding="utf-8")
        self.assertEqual(one, two)


class ModdingFromDataTests(unittest.TestCase):
    """Issue #347: a new node must be addable from data alone, and here it demonstrably is."""

    def test_a_new_place_enters_the_board_by_editing_the_slice_data_only(self) -> None:
        data = copy.deepcopy(_slice())
        data["locations"] = data["locations"] + [
            {"id": "far_contact", "label": "An abstract faraway contact", "tags": ["abstract"]}
        ]
        board = board_from_local_slice(data, _binding())
        self.assertIn("far_contact", board.nodes)
        self.assertEqual(board.nodes["far_contact"].layer, "physical")
        self.assertEqual(board.nodes["far_contact"].kind, "location")
        self.assertEqual(board.nodes["far_contact"].tags, ("abstract",))
        board.validate()

    def test_a_new_route_to_a_new_place_is_projected_when_both_endpoints_exist(self) -> None:
        data = copy.deepcopy(_slice())
        data["locations"] = data["locations"] + [{"id": "far_contact", "label": "A faraway contact"}]
        data["routes"] = data["routes"] + [["port", "far_contact"]]
        board = board_from_local_slice(data, _binding())
        self.assertIn("route-port-far_contact", board.edges)
        self.assertEqual(board.edges["route-port-far_contact"].kind, EdgeKind.TRAVEL)

    def test_the_binding_can_be_pointed_at_another_slice_without_touching_code(self) -> None:
        """The mapping is data, so a second slice is a second document rather than a second module."""
        with tempfile.TemporaryDirectory() as tmp:
            other = Path(tmp) / "other_slice.json"
            other.write_text(
                json.dumps(
                    {
                        "locations": [{"id": "hq_a", "label": "Headquarters"}],
                        "parties": [{"id": "party_a", "name": "A party"}],
                        "leaders": [],
                        "routes": [],
                        "relationships": [],
                    }
                ),
                encoding="utf-8",
            )
            binding = copy.deepcopy(_binding())
            binding["slice"] = "other_slice.json"
            binding["layout"]["positions"] = {"hq_a": [0.0, 0.0]}
            board = board_from_local_slice(
                json.loads(other.read_text(encoding="utf-8")), binding
            )
        self.assertEqual(set(board.nodes), {"hq_a", "party_a"})
        board.validate()


if __name__ == "__main__":
    unittest.main()
