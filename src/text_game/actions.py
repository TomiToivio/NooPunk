"""Structured actions behind both commands and free-text intent."""

from __future__ import annotations

from dataclasses import dataclass
import shlex


@dataclass(frozen=True, slots=True)
class Action:
    actor_id: str
    verb: str
    args: tuple[str, ...] = ()
    raw: str = ""
    source: str = "system"


@dataclass(frozen=True, slots=True)
class ActionResult:
    text: str
    completed: bool = False


_DIRECTION_ALIASES = {
    "n": "north", "s": "south", "e": "east", "w": "west",
    "north": "north", "south": "south", "east": "east", "west": "west",
}


def parse_command(actor_id: str, command: str, *, source: str = "system") -> Action:
    raw = command.strip()
    if not raw:
        raise ValueError("Command must not be empty.")
    parts = shlex.split(raw)
    head = parts[0].casefold()

    if head in _DIRECTION_ALIASES:
        return Action(actor_id, "go", (_DIRECTION_ALIASES[head],), raw, source)

    aliases = {"i": "inventory", "inv": "inventory", "l": "look"}
    verb = aliases.get(head, head)
    return Action(actor_id, verb, tuple(parts[1:]), raw, source)


__all__ = ["Action", "ActionResult", "parse_command"]
