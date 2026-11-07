"""A standalone social-science simulator (#1286). No RPG dependency, by design."""

from .kernel import (
    Actor, ActorKind, CommunicationEdge, Event, EventKind, KernelError, Origin, Provenance,
    RULES, Simulation, SocialEdge, build, resolve_rule,
)

__all__ = [
    "Actor", "ActorKind", "CommunicationEdge", "Event", "EventKind", "KernelError", "Origin", "Provenance",
    "RULES", "Simulation", "SocialEdge", "build", "resolve_rule",
]
