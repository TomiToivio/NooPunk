"""Standalone narrative RPG module for Noöpunk."""

from .engine import RPGSession
from .actions import ActionResult, ActionType, resolve_action
from .astral import ProjectionLayer, ProjectionResult, ProjectionSession, ProjectionStatus
from .conflict import Conflict, Conflictant
from .cyber import intrude
from .effects import apply_graph_effect
from .factions import Faction, FactionProject, analyze_faction, analyze_faction_v3, load_factions
from .npcs import create_npc
from .loaders import character_from_dict, load_character, load_scenario, scenario_from_dict
from .models import (
    CANONICAL_ATTRIBUTES,
    Character,
    CheckResult,
    Choice,
    DialogueNode,
    Interaction,
    InteractionResult,
    GraphEffect,
    Outcome,
    RPGEvent,
    RPGState,
    ResultTier,
    Scenario,
    Scene,
    SkillCheck,
)
from .psi import (
    CrossLayerEffect,
    PsiActionContext,
    PsiActionResult,
    PsiMode,
    PsiPressure,
    RealityShift,
    belief_bonus,
    consensus_modifier,
    load_psi_tables,
    ontological_shock,
    psi_rating_for,
    reality_shift,
    resolve_psi_action,
    use_psi,
)
from .psychosurgery import PsychosurgerySession
from .tarot import Card, Deck, DrawnCard, draw, load_deck, resolve_action_tarot, resolve_check_tarot, value_to_roll
from .persistence import load_session, save_session, session_from_dict, session_to_dict
from .integration import apply_social_graph_effect
from .social import Relationship
from .traits import Aspect, Condition, Consequence, Skill, Stunt, advance_skill
from .rules import (
    TRANSHUMANITY_FATE_SKILLS,
    resolve_check,
    tier_for_margin,
    validate_skill_check,
    validate_transhumanity_fate_skill_profile,
)

__all__ = [
    "CANONICAL_ATTRIBUTES", "Character", "CheckResult", "Choice", "DialogueNode",
    "Interaction", "InteractionResult", "Outcome", "RPGEvent", "RPGSession", "RPGState",
    "ResultTier", "Scenario", "Scene", "SkillCheck", "character_from_dict", "load_character",
    "load_scenario", "resolve_check", "scenario_from_dict", "tier_for_margin",
    "validate_skill_check",
    "TRANSHUMANITY_FATE_SKILLS", "validate_transhumanity_fate_skill_profile",
    "ProjectionLayer", "ProjectionResult", "ProjectionSession", "ProjectionStatus",
    "ActionResult", "ActionType", "Aspect", "Condition", "Conflict", "Conflictant",
    "Consequence", "Faction", "FactionProject", "GraphEffect", "PsychosurgerySession",
    "analyze_faction", "analyze_faction_v3", "load_factions",
    "PsiMode", "Relationship", "Skill", "Stunt", "apply_graph_effect", "intrude", "resolve_action",
    "use_psi",
    "advance_skill", "create_npc",
    "CrossLayerEffect", "PsiActionContext", "PsiActionResult", "PsiPressure",
    "RealityShift", "belief_bonus", "consensus_modifier", "load_psi_tables",
    "ontological_shock", "psi_rating_for", "reality_shift",
    "resolve_psi_action",
    "load_session", "save_session", "session_from_dict", "session_to_dict",
    "apply_social_graph_effect",
    "Card", "Deck", "DrawnCard", "draw", "load_deck", "resolve_action_tarot",
    "resolve_check_tarot", "value_to_roll",
]

