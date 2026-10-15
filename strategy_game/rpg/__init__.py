"""Fate Core-based, setting-independent NoöPunk RPG layer (issue #389).

The layer's mechanics are the author-approved ones for the **RPG layer only**: Fate Core's four
actions over 4dF, character aspects and typed TAGs, skills, stunts, Fate points, stress and
consequences, a natural (never viral, never installed) PSI capability, and an optional, rare cortical
stack. Faction strategy and political simulation are **not approved** and are not implemented here;
:mod:`strategy_game.rpg.boundary` fills the reserved ``strategy_game.ports.LeaderRPG`` seam for them
without inventing any of their mechanics.

This package declares its **own** ``__all__``. It does not widen :data:`strategy_game.__all__` and it
does not change the key set of ``python -m strategy_game``; both are frozen by
``strategy_game/tests/test_runtime_contracts.py``.

    python -m strategy_game.rpg            # the worked scene as JSON
    python -m strategy_game.rpg --text    # the same report as reading text
"""
from . import ports
from . import roster as roster
from . import skills as skills
from .fate import (
    Action,
    Character,
    Consequence,
    Outcome,
    Resolution,
    ResourceError,
    demo_investigation,
    demo_netrunning,
    demo_netrunning_foothold,
    resolve,
    roll_fate,
    skill_check,
)
from .roster import (
    AGENT_SEAT_COUNT,
    Seat,
    SeatKind,
    TurnLedger,
    default_seats,
)
from .skills import (
    INDIVIDUAL_SKILLS,
    ActionContext,
    SkillLayerError,
    capabilities_of,
    check,
    require_capability,
)
from .run import (
    DEFAULT_SEED,
    ENGINE_DOES_NOT_DECIDE,
    FATE_NOTATION,
    SCENE_REPORT_VERSION,
    render_report,
    scene_report,
)

__all__ = [
    # the four actions and the dice
    "Action",
    "FATE_NOTATION",
    "Outcome",
    "roll_fate",
    # the character sheet
    "Character",
    "Consequence",
    "ResourceError",
    # resolution
    "Resolution",
    "resolve",
    "skill_check",
    # the two skill layers and the context that selects one (issue #482)
    "ActionContext",
    "INDIVIDUAL_SKILLS",
    "SkillLayerError",
    "capabilities_of",
    "check",
    "require_capability",
    "skills",
    # the five seats and the one-action-per-character turn (issue #482)
    "AGENT_SEAT_COUNT",
    "Seat",
    "SeatKind",
    "TurnLedger",
    "default_seats",
    "roster",
    # the worked scene and the netrunning examples
    "demo_investigation",
    "demo_netrunning",
    "demo_netrunning_foothold",
    # the runnable report
    "DEFAULT_SEED",
    "ENGINE_DOES_NOT_DECIDE",
    "SCENE_REPORT_VERSION",
    "render_report",
    "scene_report",
    # the reserved adapter seam to the unapproved strategy and political layers
    "ports",
]
