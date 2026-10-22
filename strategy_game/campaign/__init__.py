"""The shared world-state increment for issue #502's Phase 1 roadmap.

Issue #502 ("Development roadmap: RPG first, then X-COM-scale strategy, then Terra
Invicta-scale grand strategy") asks for one world model behind three views: the
investigative RPG, the later X-COM scale organizational strategy, and the later grand
strategy. This package is the **first increment only**: data schemas, a versioned
save round trip, and the thinnest tested wiring from a resolved mission onto faction
world state (Phase 1 acceptance criteria 1, 4 and 5, minus all UI and play content).

Reuse, not a competing engine (roadmap rule 6)
---------------------------------------------

Every type here adapts an existing module instead of restating its concept. The map is
also in ``tests/test_issue502_campaign_state.py`` as executable assertions:

============  ==========================================================
Campaign      adapts :class:`strategy_game.core.Leader` and ``core.Faction``
              (same field vocabulary, ``isinstance`` identity) — the
              scaffold's data-only containers
Leader/Agent  the :class:`strategy_game.rpg.fate.Character` sheet (issue
              #482's two-layer model, six individual + strategic skills),
              referenced by id through ``core.Faction``'s existing
              ``leader_id``/``asset_ids`` vocabulary
Case          the author's own ``data/rules/unsa_case_template.json``
              worksheet vocabulary
tie           :class:`strategy_game.relationships.RelationshipEdge`
              (issue #346) reused verbatim; no faction-to-tie scheme here
outcome       the **approved** :class:`strategy_game.rpg.fate.Outcome`
              ladder; ``apply_mission_outcome`` refuses a result the
              engine does not emit
============  ==========================================================

What is deliberately absent (Phase 2/3 scope, ``NO_PHASE2``): no mission board, and no political /
hegemony / institution simulation. The **strategic project clock** of issue #506 Phase 1 now exists on
the same model — ``projects``, ``tech_nodes``, ``capabilities`` and ``capacities`` on
:class:`Campaign`, advanced by ``strategy_game.projects`` and read as research by
``strategy_game.research`` — and #506 **Phase 2** now builds the organisation around it in
``strategy_game.operations``: concurrent projects on one capacity pool, personnel assignment, bounded
capacity investments, bottleneck remedies, opposition sabotage and the mission↔research loop (two new
books, ``capacity_investments`` and ``sabotages``). Rival-faction *simulation* (a rival's own ledger,
turn and plan) is still absent, as is Phase 3 entirely.
``Campaign.state_report`` exposes nothing beyond
the scaffold's declared-data discipline: no quantity, threshold, cadence or win
condition is created here, and the numbers carried are exactly the author-approved
Fate sheet ratings and the fate-point, treasury and asset **inventories** Phase 1
names. ``save_campaign``/``load_campaign`` mirror the scaffold's ``schema_version``
JSON round-trip and grows additively when later phases extend it.
"""
from __future__ import annotations

from .case import Case, CASE_TEMPLATE_FIELDS
from .case import resolve_case as resolve_case
from .missions import MissionError, MissionOutcome, apply_mission_outcome
from .state import (
    AGENT_CAPACITY,
    Agent,
    Campaign,
    CampaignFaction,
    CampaignError,
    Leader,
    SCHEMA_VERSION,
    save_campaign,
    load_campaign,
)

__all__: list[str] = [
    "SCHEMA_VERSION",
    "AGENT_CAPACITY",
    "CampaignError",
    "Agent",
    "Campaign",
    "CampaignFaction",
    "Leader",
    "Case",
    "CASE_TEMPLATE_FIELDS",
    "MissionError",
    "MissionOutcome",
    "apply_mission_outcome",
    "save_campaign",
    "load_campaign",
]