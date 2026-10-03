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

#: Keywords a ``test`` command may carry, so a value can never be read as a skill
#: name by accident.
_TEST_KEYWORDS = ("modifier", "damage", "roll", "vs", "defence", "defense", "defenderroll")


def _is_keyword(token: str) -> bool:
    return token.casefold() in _TEST_KEYWORDS


def _keyword_value(args: tuple[str, ...], keyword: str) -> str:
    """Read ``<keyword> VALUE`` from a command, or "" when absent."""
    lowered = [t.casefold() for t in args]
    if keyword not in lowered:
        return ""
    index = lowered.index(keyword)
    return args[index + 1] if len(args) > index + 1 else ""


def _keyword_int(args: tuple[str, ...], keyword: str, default):
    """Read ``<keyword> N`` from a command, refusing a non-integer value.

    Returning the default when the keyword is absent is deliberate; raising when it is
    present but unparseable is also deliberate, because silently defaulting a
    mistyped modifier would change a mechanical result.
    """
    lowered = [t.casefold() for t in args]
    if keyword not in lowered:
        return default
    index = lowered.index(keyword)
    if len(args) <= index + 1:
        raise ValueError(f"{keyword} requires a numeric value")
    try:
        return int(args[index + 1])
    except ValueError as exc:
        raise ValueError(f"{keyword} requires an integer, got {args[index + 1]!r}") from exc


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
        item_id = self._match_by_id_or_label(
            token, ids, lambda i: self.world.items[i].label, kind="item",
            where="inventory" if inventory else "room",
        )
        return self.world.items[item_id]

    @staticmethod
    def _match_by_id_or_label(token, ids, label_for, *, kind: str, where: str):
        """Match a player-typed token against ids and labels.

        Exact matches win. A second pass accepts the *short* form of a prefixed id,
        because every fixture id carries a prefix (``fixture:token``, label
        ``fixture token``) and requiring the player to type it is needless friction.
        Short forms are a fallback, never an override, and an ambiguous short form is
        refused rather than guessed.
        """
        wanted = token.casefold()
        exact, short = [], []
        for identifier in ids:
            label = label_for(identifier)
            if identifier.casefold() == wanted or label.casefold() == wanted:
                exact.append(identifier)
                continue
            # Accept "...<sep><token>" where sep is the fixture separator, so both
            # `fixture:token` -> `token` and label `fixture token` -> `token` resolve.
            tail = identifier.casefold().rsplit(":", 1)[-1]
            label_tail = label.casefold().rsplit(" ", 1)[-1]
            if wanted in {tail, label_tail}:
                short.append(identifier)
        if exact:
            return exact[0]
        if len(short) == 1:
            return short[0]
        if len(short) > 1:
            raise ValueError(f"Ambiguous {kind} {token!r}: matches {sorted(short)}.")
        raise ValueError(f"No {kind} {token!r} in {where}.")

    def _resolve_actor_here(self, actor: ActorState, token: str) -> ActorState:
        candidates = [
            a.actor_id for a in self.world.actors_in(actor.room_id) if a.actor_id != actor.actor_id
        ]
        actor_id = self._match_by_id_or_label(
            token, candidates, lambda i: self.world.actors[i].label, kind="actor", where="here"
        )
        return self.world.actors[actor_id]

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

        elif verb == "sheet":
            sheet = self._sheet_for(actor)
            if sheet is None:
                text = f"{actor.label} has no character sheet."
            else:
                text = sheet.summary()

        elif verb == "test":
            text = self._resolve_test_verb(actor, args, action)

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

    def _sheet_for(self, actor: ActorState):
        """The actor's character sheet, or ``None`` when it has none (issue #60).

        The sheet lives in actor state as a plain dict; rebuilding the typed object
        each call keeps a single mutable source of truth in the world (and in the
        save file) rather than two copies that can drift.
        """
        if not actor.sheet:
            return None
        from .sheet import CharacterSheet

        return CharacterSheet.from_dict(actor.sheet)

    def _store_sheet(self, actor: ActorState, sheet) -> None:
        actor.sheet = sheet.to_dict()

    def _resolve_test_verb(self, actor: ActorState, args: tuple[str, ...], action: Action) -> str:
        """Resolve a playable test through the EP2 kernel (#60 milestone items 5-11).

        Usage::

            test skill <skill> [modifier N] [roll N]
            test social|mesh <skill> [modifier N] [roll N] [vs <actor>]
            test combat <skill> [modifier N] [roll N] vs <actor> [defence SKILL] [damage N]

        The controller chooses the intent and the target; this method owns the
        mechanics, and the dice come from the kernel or an explicitly injected
        ``roll`` - never from a model (RULEBOOK §7, AGENTS.md §12). Every value is
        keyword-labelled so no positional argument can be mistaken for another.
        """
        sheet = self._sheet_for(actor)
        if sheet is None:
            raise ValueError(f"{actor.label} has no character sheet, so cannot test a skill.")

        if not args:
            raise ValueError("test requires a kind (skill, social, mesh or combat) and a skill name")
        head = args[0].casefold()
        kind = "skill" if head in {"skill", "check"} else head
        if kind not in {"skill", "social", "mesh", "combat"}:
            raise ValueError(
                f"unknown test kind {args[0]!r}; expected skill, social, mesh or combat"
            )

        skill = args[1] if len(args) > 1 and not _is_keyword(args[1]) else ""
        if not skill:
            raise ValueError("test requires a skill name, e.g. 'test skill Perceive'")

        modifier = _keyword_int(args, "modifier", 0)
        damage = _keyword_int(args, "damage", 0)
        roll = _keyword_int(args, "roll", None)
        # Both sides' rolls are injectable so an entire exchange is reproducible from
        # the command line, which is what makes a simulation replayable.
        defender_roll = _keyword_int(args, "defenderroll", None)
        # The defender rolls its own defence, which is often a different skill from
        # the attacker's. Defaulting it to the attacker's skill would silently
        # resolve combat against a skill the defender may not even have.
        defender_skill = _keyword_value(args, "defence") or _keyword_value(args, "defense")

        defender = None
        if "vs" in [t.casefold() for t in args]:
            idx = [t.casefold() for t in args].index("vs")
            token = args[idx + 1] if len(args) > idx + 1 else ""
            if not token:
                raise ValueError("vs requires an actor in this room")
            defender_actor = self._resolve_actor_here(actor, token)
            defender = (defender_actor, self._sheet_for(defender_actor))
            if defender[1] is None:
                raise ValueError(f"{defender_actor.label} has no character sheet.")
        elif kind != "skill":
            raise ValueError(f"a {kind} test needs an opponent: add 'vs <actor>'")

        from .sheet import resolve_sheet_test

        kwargs: dict[str, Any] = {
            "kind": kind,
            "skill": skill,
            "modifier": modifier,
            "roll": roll,
        }
        if defender is not None:
            kwargs["defender_sheet"] = defender[1]
            kwargs["defender_skill"] = defender_skill or skill
            kwargs["defender_roll"] = defender_roll
            kwargs["damage"] = damage

        resolution = resolve_sheet_test(sheet, **kwargs)
        if defender is not None and kind == "combat":
            # The kernel mutated the defender's harm state; persist it back so the
            # damage survives the call and the save file.
            self._store_sheet(defender[0], kwargs["defender_sheet"])

        self._event(
            actor=actor.actor_id,
            action_type="test",
            target=defender[0].actor_id if defender else "",
            content=resolution.as_text(),
            location=actor.room_id,
            source=action.source,
        )
        return resolution.as_text()

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
