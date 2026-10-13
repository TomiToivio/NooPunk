"""Tabletop primitives for the NoöPunk × LaclauGPT crossover (issue #347).

The tabletop is a **design constraint and rules vocabulary**, not a manufacturing requirement: this
package implements the digital equivalents of dice, cards, decks, a board, pieces and tarot cards
so that a turn can be explained with RPG sheets, board pieces, cards and dice — even though the
digital collection would be absurd to print.

## What this package is NOT

It carries **no rules**. Nothing here decides what a roll *means*, what a card *does*, what an edge
*costs*, whose turn it is, or who wins. That boundary is not stylistic: issue #347 says it is a
"vertical slice implementation specification, not approval to ... invent fixed numerical rules",
and `strategy_game/docs/RULE_SYSTEM_RESEARCH.md` keeps four gates open —

    Gate A: author-approved leader RPG rules.
    Gate B: author-approved political-simulation methodology and simulation assumptions.
    Gate C: author-approved strategy rules.
    Gate D: explicit integration contract and prototype playtest.

— with the standing rule *"Until all relevant gates, no gameplay mechanics are implemented."*

So this package is the **rule-free substrate the gates are about**: the shapes a later, approved
rule layer would manipulate. Concretely, the following are deliberately absent and reserved:

* dice **resolution** — no difficulty, no target number, no success/failure, no advantage or
  opposed check, no modifier cap, and no opinion about which die the game uses;
* card **effects** — prerequisites and effects are carried as opaque structured data that nothing
  in this package interprets;
* tarot **meanings and modifiers** — the card identity is a typed placeholder, and the composition,
  meanings and any mechanical claim need author approval per issue #304;
* **turn order, actions, economy, victory** — not modelled at all;
* integration with :class:`strategy_game.core.WorldState` — joining a new subsystem to the shared
  container *is* the Gate D decision, so :func:`strategy_game.tabletop.bridge.board_from_world`
  takes the world state as an explicit **argument** and returns a projection. The rendering path
  exists; the gate is not performed, and the argument is still there to remove when it is.

The public API of this subpackage is its own; :mod:`strategy_game`'s pinned ``__all__`` and the
pinned key set of ``python -m strategy_game`` are untouched (#282/#347).
"""
from .board import (
    BOARD_LAYERS,
    EDGE_KINDS,
    Board,
    BoardEdge,
    BoardError,
    BoardNode,
    BoardPiece,
    EdgeKind,
    Layout,
)
from .bridge import board_from_world
from .cards import Card, CardError, CardRole, CardType, CardVisibility
from .decks import Deck, DeckError, DrawLogEntry, DuplicatePolicy, Zone
from .dice import DiceNotationError, DicePool, RollLog, RollResult, parse_notation, roll
from .serialization import TABLE_SCHEMA_VERSION, TableState, load_table, save_table
from .tarot import TAROT_USES, TarotCard, TarotDraw, TarotUse, draw_tarot, tarot_deck

__all__ = [
    # dice
    "DiceNotationError",
    "DicePool",
    "RollLog",
    "RollResult",
    "parse_notation",
    "roll",
    # cards
    "Card",
    "CardError",
    "CardRole",
    "CardType",
    "CardVisibility",
    # decks
    "Deck",
    "DeckError",
    "DrawLogEntry",
    "DuplicatePolicy",
    "Zone",
    # board
    "BOARD_LAYERS",
    "EDGE_KINDS",
    "Board",
    "BoardEdge",
    "BoardError",
    "BoardNode",
    "BoardPiece",
    "EdgeKind",
    "Layout",
    # tarot
    "TAROT_USES",
    "TarotCard",
    "TarotDraw",
    "TarotUse",
    "draw_tarot",
    # bridge
    "board_from_world",
    # serialization
    "TABLE_SCHEMA_VERSION",
    "TableState",
    "load_table",
    "save_table",
]
