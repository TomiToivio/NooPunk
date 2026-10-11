"""Run the empty strategy game view-model demonstration."""
import json

from .core import WorldState
from .view import board_view

print(json.dumps(board_view(WorldState()), ensure_ascii=False, indent=2))
