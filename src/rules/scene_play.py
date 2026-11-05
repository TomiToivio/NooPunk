"""Thin, CWN-first scene affordances for the four-graph world.

This is not a second resolver or game loop. It validates a Story scene and
describes which existing subsystem owns each player action. Frontends may
display these verbs, while CWN and the existing investigation/goal/social
modules remain the authorities for outcomes. Astral is explicitly deferred.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.world.graphs import GraphError, StoryNode

SceneKind = Literal["Social", "Investigation", "Exploration", "Action", "Cyber"]

# Descriptions are interface verbs, not substitute skill or dice rules.
# Collection and analysis are investigation modes, not new scene types.
AFFORDANCES: dict[str, dict[str, str]] = {
    "Social": {
        "talk": "cwn_social",
        "persuade": "cwn_social",
        "ask": "investigation",
        "present_evidence": "investigation",
    },
    "Investigation": {
        "search": "investigation",
        "interview": "investigation",
        "collect": "investigation",
        "osint": "investigation",
        "panopticon": "investigation",
        "informant": "investigation",
        "analyze": "investigation",
        "link_clues": "investigation",
    },
    "Exploration": {
        "observe": "investigation",
        "move": "physical_graph",
        "interact": "cwn",
    },
    "Action": {
        "arrest": "cwn",
        "pursue": "cwn",
        "restrain": "cwn",
        "negotiate": "cwn_social",
        "fight": "cwn_combat",
    },
    "Cyber": {
        "scan": "cwn_hacking",
        "connect": "cwn_hacking",
        "hack": "cwn_hacking",
        "operate_device": "cwn_hacking",
    },
}

@dataclass(frozen=True)
class SceneAffordance:
    scene_id: str
    scene_type: str
    verb: str
    authority: str


def available_actions(scene: StoryNode) -> tuple[SceneAffordance, ...]:
    """Return allowed verbs without revealing hidden world facts or performing rolls."""
    if scene.kind != "scene":
        raise GraphError("actions belong to a Story scene")
    if any(kind.strip().lower() == "astral" for kind in scene.scene_types):
        raise GraphError("Astral scenes are postponed; scripted dreams use authored narrative")
    if not scene.scene_types:
        raise GraphError("a playable scene needs a scene type")
    result: list[SceneAffordance] = []
    seen: set[str] = set()
    canonical = {kind.lower(): kind for kind in AFFORDANCES}
    for raw_kind in scene.scene_types:
        # StoryNode validation is case-insensitive; normalize at the interface boundary.
        kind = canonical.get(raw_kind.strip().lower(), raw_kind)
        # Refuse unsupported extensions, even if they have a valid Story vocabulary.
        if kind not in AFFORDANCES:
            raise GraphError(f"scene type is not playable now: {kind}")
        for verb, authority in AFFORDANCES[kind].items():
            if verb not in seen:
                result.append(SceneAffordance(scene.id, kind, verb, authority))
                seen.add(verb)
    return tuple(result)


def route_action(scene: StoryNode, verb: str) -> SceneAffordance:
    """Locate the authoritative subsystem. Never infer that an action succeeds."""
    for action in available_actions(scene):
        if action.verb == verb:
            return action
    raise GraphError(f"{verb!r} is not available in {scene.id!r}")
