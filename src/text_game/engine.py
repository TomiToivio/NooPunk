"""Deterministic local text-game loop for issue #51.

Every human, scripted, dumb or LLM-controlled actor submits the same Action object.
The engine mutates room/object/actor state and appends canonical Event envelopes.
LLMs may propose actions or language but never resolve mechanics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import sqlite3
from typing import Any, Mapping

from simulation.events import Event, next_occurrence
from simulation.sqlite_store import append as append_events
from simulation.engine import new_simulation_id

from .actions import Action, ActionResult
from .model import ActorState, Item, World


@dataclass(slots=True)
class GameEngine:
    world: World
    simulation_id: str = field(default_factory=lambda: new_simulation_id("text"))
    turn: int = 0
    connection: sqlite3.Connection | None = None
    controllers: dict[str, Any] = field(default_factory=dict)
    gm_controller: Any | None = None
    events: list[Event] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.world.validate()

    def _event(
        self,
        *,
        actor: str,
        action_type: str,
        target: str = "",
        content: str = "",
        location: str = "",
        source: str = "system",
        visibility: str = "public",
    ) -> Event:
        event = Event.create(
            simulation_id=self.simulation_id,
            turn=self.turn,
            actor=actor,
            action_type=action_type,
            target=target,
            content=content,
            location=location,
            visibility=visibility,
            source=source if source in {"system", "concordia", "tabletop", "godot"} else "system",
            synthetic=True,
            occurrence=next_occurrence(self.events, simulation_id=self.simulation_id, turn=self.turn),
        )
        self.events.append(event)
        if self.connection is not None:
            append_events(self.connection, event)
        return event

    def _actor(self, actor_id: str) -> ActorState:
        try:
            return self.world.actors[actor_id]
        except KeyError as exc:
            raise ValueError(f"Unknown actor {actor_id!r}.") from exc

    def _resolve_item(self, actor: ActorState, token: str, *, inventory: bool) -> Item:
        ids = actor.inventory if inventory else self.world.rooms[actor.room_id].items
        wanted = token.casefold()
        for item_id in ids:
            item = self.world.items[item_id]
            if item_id.casefold() == wanted or item.label.casefold() == wanted:
                return item
        where = "inventory" if inventory else "room"
        raise ValueError(f"No item {token!r} in {where}.")

    def _resolve_actor_here(self, actor: ActorState, token: str) -> ActorState:
        wanted = token.casefold()
        for candidate in self.world.actors_in(actor.room_id):
            if candidate.actor_id == actor.actor_id:
                continue
            if candidate.actor_id.casefold() == wanted or candidate.label.casefold() == wanted:
                return candidate
        raise ValueError(f"No actor {token!r} here.")

    def describe_room(self, actor_id: str) -> str:
        actor = self._actor(actor_id)
        room = self.world.rooms[actor.room_id]
        items = [self.world.items[i].label for i in room.items]
        others = [a.label for a in self.world.actors_in(room.room_id) if a.actor_id != actor_id]
        lines = [room.label, room.description]
        lines.append("Exits: " + (", ".join(sorted(room.exits)) or "none"))
        lines.append("Items: " + (", ".join(items) or "none"))
        lines.append("Actors: " + (", ".join(others) or "none"))
        return "\n".join(lines)

    def context_for(self, actor_id: str) -> str:
        actor = self._actor(actor_id)
        return self.describe_room(actor_id) + "\nInventory: " + ", ".join(actor.inventory)

    def execute(self, action: Action) -> ActionResult:
        actor = self._actor(action.actor_id)
        verb = action.verb.casefold()
        args = action.args
        text = ""

        if verb == "look":
            text = self.describe_room(actor.actor_id)
            self._event(actor=actor.actor_id, action_type="observe", location=actor.room_id, source=action.source)

        elif verb == "inventory":
            labels = [self.world.items[i].label for i in actor.inventory]
            text = "Inventory: " + (", ".join(labels) or "empty")

        elif verb == "go":
            if not args:
                raise ValueError("go requires a direction")
            direction = args[0].casefold()
            room = self.world.rooms[actor.room_id]
            if direction not in room.exits:
                raise ValueError(f"No exit {direction!r} from this room.")
            actor.room_id = room.exits[direction]
            text = self.describe_room(actor.actor_id)
            self._event(actor=actor.actor_id, action_type="move", content=direction, location=actor.room_id, source=action.source)

        elif verb == "take":
            if not args:
                raise ValueError("take requires an item")
            item = self._resolve_item(actor, " ".join(args), inventory=False)
            if not item.takeable:
                raise ValueError(f"{item.label} is not takeable.")
            self.world.rooms[actor.room_id].items.remove(item.item_id)
            actor.inventory.append(item.item_id)
            text = f"Taken: {item.label}"
            self._event(actor=actor.actor_id, action_type="take", target=item.item_id, location=actor.room_id, source=action.source)

        elif verb == "drop":
            if not args:
                raise ValueError("drop requires an item")
            item = self._resolve_item(actor, " ".join(args), inventory=True)
            actor.inventory.remove(item.item_id)
            self.world.rooms[actor.room_id].items.append(item.item_id)
            text = f"Dropped: {item.label}"
            self._event(actor=actor.actor_id, action_type="drop", target=item.item_id, location=actor.room_id, source=action.source)

        elif verb == "talk":
            if not args:
                raise ValueError("talk requires an actor")
            target = self._resolve_actor_here(actor, args[0])
            message = " ".join(args[1:]).strip() or "Hello."
            self._event(
                actor=actor.actor_id,
                action_type="communicate",
                target=target.actor_id,
                content=message,
                location=actor.room_id,
                source=action.source,
            )
            controller = self.controllers.get(target.actor_id)
            if target.controller in {"llm", "llm_player"} and controller is not None:
                reply = controller.reply(actor=target, message=message, context=self.context_for(target.actor_id))
                reply_source = "concordia"
            elif target.controller == "scripted":
                reply = target.dialogue.get(message.casefold(), target.dialogue.get("default", "..."))
                reply_source = "system"
            else:
                reply = "..."
                reply_source = "system"
            self._event(
                actor=target.actor_id,
                action_type="communicate",
                target=actor.actor_id,
                content=reply,
                location=target.room_id,
                source=reply_source,
            )
            text = f"{target.label}: {reply}"

        elif verb == "say":
            message = " ".join(args).strip()
            if not message:
                raise ValueError("say requires text")
            self._event(actor=actor.actor_id, action_type="communicate", content=message, location=actor.room_id, source=action.source)
            text = f'You say: "{message}"'

        elif verb == "use":
            if not args:
                raise ValueError("use requires an item")
            item = self._resolve_item(actor, args[0], inventory=True)
            target = args[1] if len(args) > 1 else ""
            self._event(actor=actor.actor_id, action_type="use", target=target or item.item_id, content=item.item_id, location=actor.room_id, source=action.source)
            text = f"Used {item.label}. No generic item effect is defined."

        elif verb == "stats":
            text = "Final attribute names are not locked. Character mechanics use the shared tag/rules layer."

        else:
            raise ValueError(f"Unknown command verb {action.verb!r}.")

        objective = self.world.adventure.objective_item_id
        if objective and objective in actor.inventory and not self.world.adventure.completed_by:
            self.world.adventure.completed_by = actor.actor_id
            self._event(actor=actor.actor_id, action_type="complete", target=self.world.adventure.adventure_id, source="system")
            text += "\nFixture adventure complete."

        completed = bool(self.world.adventure.completed_by)
        self.turn += 1
        return ActionResult(text=text, completed=completed)

    def run_background_once(self) -> list[tuple[str, ActionResult]]:
        results: list[tuple[str, ActionResult]] = []
        for actor_id in sorted(self.controllers):
            actor = self.world.actors.get(actor_id)
            controller = self.controllers[actor_id]
            if actor is None or actor.controller not in {"dumb", "llm_player"}:
                continue
            try:
                action = controller.choose_action(
                    actor=actor,
                    world=self.world,
                    context=self.context_for(actor.actor_id),
                )
            except TypeError:
                action = controller.choose_action(actor, self.world)
            if action is None:
                continue
            results.append((actor_id, self.execute(action)))
        return results

    def gm_narration(self, result: ActionResult) -> str:
        if self.gm_controller is None:
            return ""
        narrate = getattr(self.gm_controller, "narrate", None)
        if narrate is None:
            return ""
        return str(narrate(context=result.text)).strip()


__all__ = ["GameEngine"]
