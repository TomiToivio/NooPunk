"""Rule-free demonstration of the tabletop primitives: ``python -m strategy_game.tabletop``.

Prints one small table as JSON — a board with a headquarters node, an institution node and one
abstract faraway contact node, one dice pool rolled with a fixed seed, and one card drawn. Everything
in it is **an illustration of the machinery, not canon**: the labels are examples, the die is arbitrary,
and no roll is compared to anything. Nothing here decides a rule.

This is the substrate the approved rule layers will sit on, shown working end to end: seeded roll with
a per-die breakdown, reproducible draw with a log, layered graph, versioned snapshot.
"""
from __future__ import annotations

import json
from typing import Any

from .board import Board, BoardEdge, BoardNode, EdgeKind, Layout
from .cards import Card, CardRole, CardType
from .decks import Deck, DuplicatePolicy
from .dice import parse_notation, roll
from .serialization import TableState


def demo() -> tuple[TableState, dict[str, Any]]:
    """A minimal, illustrative table. Not a scenario and not canon."""
    board = Board(identifier="demo")
    board.add_node(BoardNode("hq", "Faction headquarters (illustrative)", "location", "physical"))
    board.add_node(BoardNode("ministry", "National ministry (illustrative)", "institution", "social"))
    board.add_node(BoardNode("contact", "Abstract faraway contact (illustrative)", "location", "cyber"))
    board.add_edge(BoardEdge("e1", "hq", "ministry", EdgeKind.COOPERATION, "social"))
    board.add_edge(BoardEdge("e2", "hq", "contact", EdgeKind.COMMUNICATION, "cyber"))

    layout = Layout()
    layout.set("hq", 0.0, 0.0)
    layout.set("ministry", 1.0, 0.5)
    layout.set("contact", 8.0, -3.0)

    deck = Deck(identifier="demo-events", name="Illustrative deck",
                duplicate_policy=DuplicatePolicy.DEDUPE_BY_ID)
    deck.add(Card("card-1", CardType.PLACE, "A place card (illustrative)",
                  role=CardRole.PERSISTENT_RECORD, tags=("example",)))
    deck.add(Card("card-2", CardType.EVENT, "An event card (illustrative)",
                  role=CardRole.PLAYABLE_MOVE, tags=("example",),
                  effects=({"kind": "unspecified", "note": "no approved effect"},)))

    state = TableState(board=board, decks={deck.identifier: deck})
    state.rolls.record(roll(parse_notation("2d6+1"), seed=1, label="illustrative check"))
    deck.shuffle(seed=2)
    deck.draw(1, seed=3)

    payload = state.to_dict()
    # The layout is cosmetic and deliberately outside the state, so it is shown beside it rather than
    # in it -- the board must reload identically whether or not a layout is cached.
    payload["layout"] = layout.to_dict()
    return state, payload


if __name__ == "__main__":
    _state, _payload = demo()
    print(json.dumps(_payload, ensure_ascii=False, indent=2))
