"""LLM agents propose; the world decides (#946).

The gateway exists to make one thing impossible: a language model changing the world by describing it. An
agent returns a **proposal** — a structured intent — and never receives a handle to `WorldState`. A narrator
that says "you find a rifle" produces text, not inventory.

With no provider configured, `deterministic_fallback()` answers instead, so a deployment without an API key is
still a playable game and not a broken one.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol, runtime_checkable

#: The only intents an agent may propose. Anything else is refused before it can reach the state.
ALLOWED_INTENTS = {
    "narrate",          # prose for the room; carries no mechanical effect
    "suggest_action",   # "you could ask the clerk about the second badge"
    "request_check",    # asks the host to resolve a CWN check; the host decides, not the model
    "request_event",    # proposes an event the world may apply, subject to normal validation
}

#: Intents that can never be produced by an agent, whatever it says.
FORBIDDEN_INTENTS = {"set_hp", "add_item", "grant_success", "teleport", "spawn"}


class RefusedProposal(ValueError):
    """The proposal was malformed or asked for something an agent may not do."""


@dataclass(frozen=True)
class Proposal:
    intent: str
    text: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    provider: str = "none"


@runtime_checkable
class Provider(Protocol):
    """A language model, behind a wall."""

    def complete(self, prompt: str, context: dict[str, Any]) -> str:  # pragma: no cover - protocol
        ...


def validate(proposal: Proposal) -> list[str]:
    """Problems with a proposal. Empty means it may be handed to the world layer as a *proposal*."""
    problems: list[str] = []
    if proposal.intent in FORBIDDEN_INTENTS:
        problems.append(f"agents may not {proposal.intent}")
    elif proposal.intent not in ALLOWED_INTENTS:
        problems.append(f"unknown intent: {proposal.intent}")
    if proposal.intent == "narrate" and not proposal.text.strip():
        problems.append("a narration proposal needs text")
    if proposal.intent == "request_event":
        event = proposal.payload.get("event") or {}
        if not isinstance(event, dict) or not event.get("type"):
            problems.append("a requested event needs a type")
    if not 0.0 <= proposal.confidence <= 1.0:
        problems.append("confidence must be 0..1")
    return problems


class Gateway:
    """Wraps a provider, enforces the proposal contract, and degrades to rules without one."""

    def __init__(self, provider: Provider | None = None, *,
                 max_calls: int = 100, prompt_budget: int = 4000) -> None:
        self.provider = provider
        self.max_calls = max_calls
        self.prompt_budget = prompt_budget
        self.calls = 0
        self.refusals: list[str] = []

    @property
    def enabled(self) -> bool:
        return self.provider is not None

    def propose(self, prompt: str, context: dict[str, Any]) -> Proposal:
        """Ask the provider for a proposal. Never returns anything but a validated Proposal."""
        if not self.enabled:
            return self.deterministic_fallback(context)
        if self.calls >= self.max_calls:
            self.refusals.append("call budget exhausted")
            return self.deterministic_fallback(context, reason="budget")
        self.calls += 1
        bounded = {key: value for key, value in context.items() if key in
                   ("room", "actor", "nearby", "recent_events", "faction")}
        raw = self.provider.complete(prompt[: self.prompt_budget], bounded)
        proposal = Proposal(intent="narrate", text=str(raw), confidence=0.6,
                            provider=type(self.provider).__name__)
        problems = validate(proposal)
        if problems:
            self.refusals.append("; ".join(problems))
            return self.deterministic_fallback(context, reason="invalid")
        return proposal

    def deterministic_fallback(self, context: dict[str, Any], reason: str = "disabled") -> Proposal:
        """A description with no invention: it reports the room the state already holds."""
        room = str(context.get("room", "somewhere"))
        actor = str(context.get("actor", "you"))
        return Proposal(intent="narrate",
                        text=f"{actor} is in {room}. Nothing here changes because nobody described it.",
                        confidence=1.0, provider=f"fallback:{reason}")


def accept(gateway: Gateway, proposal: Proposal,
           apply_event: Callable[[dict[str, Any]], dict[str, Any]]) -> dict[str, Any] | None:
    """Route an accepted proposal. Only `request_event` can reach the world, and only as a normal event."""
    problems = validate(proposal)
    if problems:
        raise RefusedProposal("; ".join(problems))
    if proposal.intent != "request_event":
        return None
    event = dict(proposal.payload["event"])
    event.setdefault("id", f"llm-{gateway.calls}-{event.get('type')}")
    event.setdefault("source", proposal.provider)
    return apply_event(event)
