"""The tactical mission layer: renderer-independent map, mission data and session (issue #515).

Issue #515 asks for a minimal top-down tactical map serving both squad combat and investigation
quests, and its first milestone is a **technical spike**: choose renderer, grid/tile format and
mission-data schema. This package is the half of that spike that can be built before the author picks
a renderer, because it is the half no renderer owns:

* :mod:`strategy_game.tactical.grid` — the tile grid, its ASCII interchange format and pathfinding;
* :mod:`strategy_game.tactical.mission` — the mission-data schema and its validating loader;
* :mod:`strategy_game.tactical.session` — four agent seats, click-to-move, interactions, objectives,
  and the mission outcome written into the campaign's persistent state;
* :mod:`strategy_game.tactical.demo` — a headless, deterministic fixture mission.

The boundary this package keeps
-------------------------------

**No rendering library, no engine, no third-party dependency.** The package imports the standard
library and ``strategy_game``'s own approved rules kernel, and nothing else; a test asserts both the
import graph and that no mission document can carry a sprite, tile id or pixel coordinate. A Godot
scene, a Pygame window, a Tiled map or a terminal view are all *views over the same data* — choosing
one cannot make the mission layer wrong, and choosing none cannot make it incomplete.

It also adds **no rule**. Stats, skills, checks, stress, consequences and the mission outcome are
:mod:`strategy_game.rpg`'s and :mod:`strategy_game.campaign`'s; ``strategy_game/RULEBOOK.md`` keeps
its *no rules approved* status, and the renderer decision the spike informs is queued as row D29 of
``docs/design/AUTHOR_DECISION_QUEUE.md`` rather than made here.

    python -m strategy_game.tactical            # the headless demo as reading text
    python -m strategy_game.tactical --json     # the same run as JSON
"""
from __future__ import annotations

from . import demo as demo
from . import grid as grid
from . import mission as mission
from . import session as session
from .grid import (
    LEGEND,
    TILE_GLYPHS,
    Cell,
    Grid,
    GridError,
    PathResult,
    TileKind,
)
from .mission import (
    MISSION_FORMAT,
    MISSION_SCHEMA_VERSION,
    Interaction,
    InteractionKind,
    MissionError,
    MissionSpec,
    Objective,
    load_mission,
    mission_from_dict,
)
from .session import (
    DEFAULT_SEED,
    InteractionResult,
    MissionSession,
    MoveResult,
    ObjectiveStatus,
)

__all__ = [
    "DEFAULT_SEED",
    "LEGEND",
    "MISSION_FORMAT",
    "MISSION_SCHEMA_VERSION",
    "TILE_GLYPHS",
    "Cell",
    "Grid",
    "GridError",
    "Interaction",
    "InteractionKind",
    "InteractionResult",
    "MissionError",
    "MissionSession",
    "MissionSpec",
    "MoveResult",
    "Objective",
    "ObjectiveStatus",
    "PathResult",
    "TileKind",
    "demo",
    "grid",
    "load_mission",
    "mission",
    "mission_from_dict",
    "session",
]
