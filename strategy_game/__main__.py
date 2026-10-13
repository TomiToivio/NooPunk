"""Run the empty strategy game view-model demonstration."""
from __future__ import annotations

import json

from .core import WorldState
from .view import board_view


def main() -> None:
    """Print a portable, rule-free empty-world board representation."""
    print(json.dumps(board_view(WorldState()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
