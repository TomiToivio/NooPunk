"""Controllers for scripted, dumb and optional LLM actors.

Controllers only propose structured actions or language. They never resolve rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .actions import Action, parse_command
from .model import ActorState, World


@dataclass(slots=True)
class PatrolController:
    """Tiny deterministic Mesa-style policy for background NPCs."""

    route: Mapping[str, str]

    def choose_action(self, actor: ActorState, world: World, context: str = "") -> Action | None:
        direction = self.route.get(actor.room_id)
        if not direction:
            return None
        return Action(actor.actor_id, "go", (direction,), source="system")


@dataclass(slots=True)
class ConcordiaTextController:
    """Adapter around a Concordia-compatible language model.

    The model is expected to expose sample_text(prompt=...). Tests use a fake model;
    production may use the existing Ollama-backed Concordia adapter.
    """

    model: Any

    def _sample(self, prompt: str) -> str:
        method = getattr(self.model, "sample_text", None)
        if method is None:
            raise TypeError("LLM model must expose sample_text().")
        try:
            value = method(prompt=prompt)
        except TypeError:
            value = method(prompt)
        return str(value).strip()

    def reply(self, *, actor: ActorState, message: str, context: str) -> str:
        prompt = (
            "You are an NPC in the NoöPunk runtime. Use only supplied fixture/world "
            "context. Do not invent rules, rolls, numeric outcomes or canon.\n"
            f"Actor: {actor.label}\nContext: {context}\nHuman says: {message}\n"
            "Reply briefly in character."
        )
        return self._sample(prompt)

    def narrate(self, *, context: str) -> str:
        prompt = (
            "You are the NoöPunk Game Master narrator. Describe only the supplied "
            "resolved state/result. Do not invent rules, rolls, modifiers, canon or "
            "new facts. Keep it brief.\nContext: " + context
        )
        return self._sample(prompt)

    def choose_action(self, *, actor: ActorState, world: World, context: str) -> Action:
        prompt = (
            "Choose exactly one valid text command for this actor. Do not narrate. "
            "Allowed verbs: look, go <direction>, inventory, take <item-id>, "
            "drop <item-id>, talk <actor-id> <message>, say <message>.\n"
            f"Actor: {actor.actor_id}\nRoom: {actor.room_id}\nContext: {context}"
        )
        raw = self._sample(prompt).splitlines()[0].strip()
        return parse_command(actor.actor_id, raw, source="concordia")


def build_ollama_controller_from_env() -> ConcordiaTextController:
    """Build the repository's existing Concordia/Ollama provider on demand."""

    from concordia_runtime.config import ConcordiaRuntimeConfig
    from concordia_runtime.providers import OllamaProvider

    model = OllamaProvider(ConcordiaRuntimeConfig.from_env()).build()
    return ConcordiaTextController(model)


__all__ = [
    "ConcordiaTextController",
    "PatrolController",
    "build_ollama_controller_from_env",
]
