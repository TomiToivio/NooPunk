"""Quick NPC construction for scene-scale supporting characters."""

from __future__ import annotations

from .models import CANONICAL_ATTRIBUTES, Character


def create_npc(
    npc_id: str,
    name: str,
    *,
    focus_attribute: str,
    focus_skill: str,
    competence: int = 2,
    aspects: set[str] | None = None,
) -> Character:
    if focus_attribute not in CANONICAL_ATTRIBUTES:
        raise ValueError(f"Unknown attribute: {focus_attribute}")
    if competence < 0 or competence > 4:
        raise ValueError("NPC competence must be between +0 and +4")
    attributes = {attribute: 0 for attribute in CANONICAL_ATTRIBUTES}
    attributes[focus_attribute] = competence
    return Character(
        id=npc_id,
        name=name,
        attributes=attributes,
        skills={focus_skill: competence},
        aspects=set(aspects or ()),
    )
