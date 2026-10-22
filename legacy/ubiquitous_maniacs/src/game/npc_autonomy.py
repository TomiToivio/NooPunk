"""Deterministic NPC social turns for the integrated Noöpunk game state.

This is deliberately a small rules layer, not an LLM agent. NPCs act from
their current mood, goals and directed relationships. Every action becomes a
normal relationship change plus an NPC-owned memory, so it is inspectable and
survives the existing save format.
"""

from __future__ import annotations

from dataclasses import dataclass

from .social_graph import MultiDimensionalSocialGraph, NPCMemory


@dataclass(frozen=True)
class NPCAutonomyAction:
    actor: str
    target: str
    dimension: str
    delta: int
    goal: str
    mood: str
    summary: str


_MOOD_POLICY: dict[str, tuple[str, int]] = {
    "alarmed": ("trust", 1),
    "calm": ("trust", 1),
    "grieving": ("trust", 1),
    "intense": ("authority", 1),
    "omniscient": ("suspicion", 1),
    "professional": ("authority", 1),
    "watchful": ("suspicion", 1),
}


def _target_score(
    social: MultiDimensionalSocialGraph,
    actor: str,
    target: str,
    dimension: str,
) -> tuple[int, int, int, str]:
    rel = social.get_relationship(actor, target)
    values = rel.to_dict()
    if dimension == "trust":
        # Support familiar people first, especially where trust still has room
        # to grow. This makes Kallio seek Romppainen without hard-coding names.
        return (rel.familiarity, 100 - rel.trust, rel.fear, target)
    if dimension == "suspicion":
        return (rel.suspicion, rel.familiarity, rel.authority, target)
    if dimension == "authority":
        return (rel.authority, rel.familiarity, rel.suspicion, target)
    return (values.get(dimension, 0), rel.familiarity, 0, target)


def plan_npc_action(
    social: MultiDimensionalSocialGraph,
    actor: str,
) -> NPCAutonomyAction | None:
    """Plan one auditable action from an NPC's current graph state."""
    if actor not in social.graph:
        raise KeyError(f"Unknown character: {actor}")

    node = social.graph.nodes[actor]
    mood = str(node.get("mood", "neutral"))
    policy = _MOOD_POLICY.get(mood)
    if policy is None:
        return None
    dimension, delta = policy

    targets = [target for target in social.graph.successors(actor) if target != actor]
    if not targets:
        return None
    target = max(targets, key=lambda item: _target_score(social, actor, item, dimension))

    goals = [str(goal).strip() for goal in node.get("goals", []) if str(goal).strip()]
    goal = goals[0] if goals else "Reagoi verkoston muutokseen"
    actor_name = str(node.get("name", actor))
    target_name = str(social.graph.nodes[target].get("name", target))
    verbs = {
        "trust": "hakeutuu yhteistyöhön",
        "suspicion": "tarkkailee",
        "authority": "käyttää institutionaalista painetta",
    }
    summary = f"{actor_name} {verbs[dimension]}: {target_name}. Tavoite: {goal}"
    return NPCAutonomyAction(actor, target, dimension, delta, goal, mood, summary)


def run_npc_turn(
    social: MultiDimensionalSocialGraph,
    *,
    player_id: str = "romppainen",
    scene_id: str = "social_turn",
    max_actions: int = 2,
) -> list[NPCAutonomyAction]:
    """Run a deterministic ambient NPC turn and persist its consequences.

    Actor order rotates with the social turn counter so the same NPCs do not
    monopolize every tick. No action is invented for neutral/unknown moods.
    """
    limit = max(0, int(max_actions))
    if limit == 0:
        return []

    actors = sorted(node for node in social.graph.nodes if node != player_id)
    if not actors:
        return []
    offset = social.turn % len(actors)
    actors = actors[offset:] + actors[:offset]

    social.advance_turn()
    actions: list[NPCAutonomyAction] = []
    for actor in actors:
        action = plan_npc_action(social, actor)
        if action is None:
            continue
        social.change_relationship(
            action.actor,
            action.target,
            action.dimension,
            action.delta,
            reason=f"NPC autonomy: {action.goal}",
        )
        social.remember(action.actor, NPCMemory(
            turn=social.turn,
            scene=scene_id,
            interaction=f"npc_turn:{social.turn}:{len(actions)}",
            actor=action.actor,
            summary=action.summary,
            valence=action.delta if action.dimension == "trust" else 0,
            tags=("npc_autonomy", action.dimension, action.mood),
        ))
        actions.append(action)
        if len(actions) >= limit:
            break
    return actions
