"""JSON save/load for the local text prototype.

The save includes the deterministic event envelopes as well as the room/object state,
so a local game can resume without requiring a live LLM.
"""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3

from simulation.events import Event
from simulation.sqlite_store import append as append_events

from .engine import GameEngine
from .model import World


def save_game(engine: GameEngine, path: str | Path) -> None:
    payload = {
        "simulation_id": engine.simulation_id,
        "turn": engine.turn,
        "world": engine.world.to_dict(),
        "events": [event.to_dict() for event in engine.events],
    }
    Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def load_game(
    path: str | Path,
    *,
    connection: sqlite3.Connection | None = None,
    controllers: dict | None = None,
    gm_controller=None,
) -> GameEngine:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    events = [Event.from_dict(item) for item in payload.get("events", [])]
    engine = GameEngine(
        world=World.from_dict(payload["world"]),
        simulation_id=str(payload["simulation_id"]),
        turn=int(payload.get("turn", 0)),
        connection=connection,
        controllers=dict(controllers or {}),
        gm_controller=gm_controller,
        events=events,
    )
    if connection is not None and events:
        append_events(connection, *events)
    return engine


__all__ = ["load_game", "save_game"]
