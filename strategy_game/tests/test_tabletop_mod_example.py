"""Issue #347: a mod adds a board node and a card as JSON, not code changes."""
import json
import unittest
from pathlib import Path

from strategy_game.tabletop.board import Board, BoardNode, BoardError
from strategy_game.tabletop.cards import Card, CardType, CardRole

FIXTURE = Path(__file__).resolve().parents[1] / "data" / "mods" / "example_contact.json"


def load_example(path=FIXTURE):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "noopunk.mod_example.v1":
        raise ValueError("unsupported example schema version")
    board = Board(identifier="mod-example")
    for item in data["nodes"]:
        board.add_node(BoardNode.from_dict(item))
    cards = [Card.from_dict(item) for item in data["cards"]]
    if len({card.identifier for card in cards}) != len(cards):
        raise ValueError("duplicate card identifier")
    return board, cards


class DataOnlyModdingTests(unittest.TestCase):
    def test_new_node_and_card_load_from_json_only(self):
        board, cards = load_example()
        self.assertIn("example-foreign-lab", board.nodes)
        self.assertEqual(board.nodes["example-foreign-lab"].layer, "social")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0].card_type, CardType.EVENT)
        self.assertEqual(cards[0].role, CardRole.PERSISTENT_RECORD)
        self.assertFalse(cards[0].effects)
        self.assertEqual(BoardNode.from_dict(board.nodes["example-foreign-lab"].to_dict()).to_dict(), board.nodes["example-foreign-lab"].to_dict())
        self.assertEqual(Card.from_dict(cards[0].to_dict()).to_dict(), cards[0].to_dict())

    def test_mod_content_is_extendible_without_python_edits(self):
        raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
        raw["nodes"].append({"identifier": "another-researcher", "label": "Another researcher", "kind": "person", "layer": "social"})
        raw["cards"].append({"identifier": "new-contact-card", "card_type": "relationship", "title": "A tentative introduction"})
        board = Board(identifier="extended")
        for node in raw["nodes"]:
            board.add_node(BoardNode.from_dict(node))
        cards = [Card.from_dict(record) for record in raw["cards"]]
        self.assertIn("another-researcher", board.nodes)
        self.assertEqual(cards[-1].card_type, CardType.RELATIONSHIP)

    def test_duplicate_nodes_are_rejected(self):
        board = Board(identifier="duplicate-check")
        node = BoardNode(identifier="repeated", label="First")
        board.add_node(node)
        with self.assertRaises(BoardError):
            board.add_node(BoardNode(identifier="repeated", label="Second"))

    def test_duplicate_cards_are_rejected_by_example_loader(self):
        from tempfile import TemporaryDirectory

        raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
        raw["cards"].append(dict(raw["cards"][0]))
        with TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate-cards.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate card identifier"):
                load_example(path)

    def test_unsupported_schema_is_rejected(self):
        from tempfile import TemporaryDirectory

        raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
        raw["schema_version"] = "noopunk.mod_example.v999"
        with TemporaryDirectory() as folder:
            path = Path(folder) / "future-schema.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsupported example schema version"):
                load_example(path)


if __name__ == "__main__":
    unittest.main()
