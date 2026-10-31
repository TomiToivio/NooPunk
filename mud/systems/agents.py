"""Concordia-style LLM interface with strict, inspectable action boundaries.

An LLM may propose actions or narrate observations. Only server-side
validated handlers may perform changes. No external provider is required.
"""
from dataclasses import dataclass

ALLOWED_NPC_ACTIONS = frozenset({"say", "wait", "move"})

@dataclass(frozen=True)
class Intent:
    actor_id: str
    action: str
    target: str = ""
    text: str = ""

def validate_npc_intent(intent: Intent, npc_ids: set[str], reachable_rooms: set[str]) -> bool:
    if intent.actor_id not in npc_ids or intent.action not in ALLOWED_NPC_ACTIONS:
        return False
    if intent.action == "move" and intent.target not in reachable_rooms:
        return False
    if len(intent.text) > 400 or len(intent.target) > 120:
        return False
    return True

class OfflineGM:
    """Safe narrative fallback, no decisions or rolls disguised as prose."""
    def narrate(self, location: str, public_events: list[str]) -> str:
        details = "; ".join(public_events[-3:]) if public_events else "The city is unusually quiet."
        return f"{location}: {details}"
