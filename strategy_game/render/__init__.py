"""The board as text: a view, not a rule.

Issue #347 asks for "a renderer / interface shell" because nothing currently draws the board, and
its plan records that this **choice of tooling is a decision record, not a rule** — so the spike can
build one working view without touching Gate A (check procedure), B (political transitions), C
(strategic actions) or D (joining the table to the world state).

This subpackage draws *declared* content only. It reads :func:`strategy_game.view.board_view`
(the pinned display projection) and returns strings, so it infers no borders, travel, control or
ownership — the constraint :class:`strategy_game.ports.MapProvider` states in its own docstring.
"""
from __future__ import annotations

from .text import (
    RENDER_SCHEMA_VERSION,
    TextMapProvider,
    board_lines,
    render_board_text,
    render_roster_text,
    state_from_local_slice,
)

__all__ = [
    "RENDER_SCHEMA_VERSION",
    "TextMapProvider",
    "board_lines",
    "render_board_text",
    "render_roster_text",
    "state_from_local_slice",
]
