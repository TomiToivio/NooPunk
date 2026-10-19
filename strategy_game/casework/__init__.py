"""Casework: one complete, playable investigation on the approved RPG kernel (#502, Phase 1).

This package is the **narrative/investigation vertical slice** the author directed to come first: a
short, complete, replayable case for the faction-leader PC and four agents, composed from the engine
that already exists rather than replacing it.

============================  ==============================================================
:mod:`.spec`                  the case declaration — scenes, actions, checks, clues, findings,
                              resolutions. No rule, no dice, no new skill.
:mod:`.session`               the playable session — five seats through
                              :class:`strategy_game.rpg.roster.TurnLedger`, checks through
                              :func:`strategy_game.rpg.skills.check`, hits through
                              :func:`strategy_game.rpg.scene.apply_hit`, cyber reachability through
                              :mod:`strategy_game.cyber`, and one write to the campaign through
                              :func:`strategy_game.campaign.missions.apply_mission_outcome`.
:mod:`.kallio`                *The Second Shadow*, the packaged case: 2045, Helsinki Field Office,
                              a Reptilian raid, and a second figure the camera did not record.
:mod:`.demo`                  the headless play-through and its text report.
============================  ==============================================================

The case is **fail-forward**: a clue never depends on one successful check, a tie and a failure cost
different prices rather than stopping the story, and a party that misses a fragment can still assemble
a partial conclusion and close the case on a weaker record. It has three endings — on the record, in
the loading bay, or referred upstairs — and the third is always available.

    python -m strategy_game.casework                 # play the packaged case headless
    python -m strategy_game.casework --route confront --approach force
    python -m strategy_game.casework --json          # the same run as one JSON record

Nothing here is canon. The frame is the canonical 2045 / Helsinki Field Office / UNSA setting; the
incident, its people and its outcome are scenario fiction, and the four agents' sheets are
placeholder playtest ratings.
"""
from __future__ import annotations

from . import demo as demo
from . import kallio as kallio
from . import session as session
from . import spec as spec
from .kallio import CASE, CASE_ID, build_campaign, build_session
from .session import (
    SESSION_SCHEMA_VERSION,
    ActionResult,
    CaseSession,
    CaseworkError,
    FindingResult,
    ResolutionResult,
    load_session,
)
from .spec import (
    CASE_FORMAT,
    CASE_SCHEMA_VERSION,
    DIFFICULTY_BANDS,
    ActionSpec,
    CaseFile,
    CaseSpecError,
    CheckSpec,
    ClueSpec,
    Cost,
    CyberGate,
    FindingSpec,
    PsiGate,
    ResolutionSpec,
    SceneSpec,
    band_difficulty,
)

__all__ = [
    "CASE",
    "CASE_FORMAT",
    "CASE_ID",
    "CASE_SCHEMA_VERSION",
    "DIFFICULTY_BANDS",
    "SESSION_SCHEMA_VERSION",
    "ActionResult",
    "ActionSpec",
    "CaseFile",
    "CaseSession",
    "CaseSpecError",
    "CaseworkError",
    "CheckSpec",
    "ClueSpec",
    "Cost",
    "CyberGate",
    "FindingResult",
    "FindingSpec",
    "PsiGate",
    "ResolutionResult",
    "ResolutionSpec",
    "SceneSpec",
    "band_difficulty",
    "build_campaign",
    "build_session",
    "demo",
    "kallio",
    "load_session",
    "session",
    "spec",
]
