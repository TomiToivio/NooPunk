"""Authoritative world state for the MUD (#946).

Everything the game considers true lives here, and it changes only through `apply()`, which validates an
event before touching anything. That is the whole defence against LLM narration, Mesa simulations and
over-eager command handlers: they can all *propose*, and only a known event type with a valid payload becomes
state.

Persistence is a JSON snapshot plus an append-only event log, so "persists across a restart" is a file
round-trip that a test can check rather than a claim.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.rules.cwn_mission_time import STANDARD_ACTION_MINUTES, MissionClock

SCHEMA_VERSION = 1

#: Event types the state understands. Adding one is a deliberate schema change with its own validation.
EVENT_TYPES = {
    "join", "move", "say", "take", "drop", "spend", "gain", "damage", "heal",
    "faction_join", "faction_leave", "reputation", "flag", "sim_reconcile", "advance_time",
}


class RejectedEvent(ValueError):
    """An event that the state refuses. The message is the reason, and the state is unchanged."""


@dataclass
class WorldState:
    """Rooms, characters, items and factions — the minimum a survival sandbox needs to be real."""

    rooms: dict[str, dict[str, Any]] = field(default_factory=dict)
    characters: dict[str, dict[str, Any]] = field(default_factory=dict)
    items: dict[str, dict[str, Any]] = field(default_factory=dict)
    factions: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: Mission time (#950, SRD ``rules-of-the-game/scenes-rounds-mission-time``): minutes from
    #: minute zero. Stored as minutes only — the scene index is derived by the shared kernel, so
    #: two fields that must agree cannot drift apart in a save file.
    time: dict[str, Any] = field(default_factory=dict)
    #: Applied event ids, so a reconnect or a replay cannot apply the same event twice.
    applied: list[str] = field(default_factory=list)
    #: Append-only history: what was proposed, what was accepted, what changed.
    log: list[dict[str, Any]] = field(default_factory=list)

    # ---- construction ---------------------------------------------------------------------------

    @classmethod
    def helsinki_opening(cls) -> "WorldState":
        """A small starting state: one street, one safehouse, one UNSA faction."""
        state = cls()
        state.rooms["street"] = {"name": "Helsinginkatu", "exits": {"east": "safehouse"},
                                 "description": "Tram rails, a shuttered kiosk, rain that will not commit."}
        state.rooms["safehouse"] = {"name": "UNSA safehouse", "exits": {"west": "street"},
                                    "description": "A basement room with a table, a radio and two chairs."}
        state.factions["unsa"] = {"name": "UNSA", "members": [], "reputation": {},
                                  "resources": {"rations": 6, "medkits": 1}}
        return state

    # ---- queries --------------------------------------------------------------------------------

    def snapshot(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "rooms": self.rooms, "characters": self.characters, "items": self.items,
            "factions": self.factions, "time": self.time, "applied": self.applied,
            "log": self.log,
        }

    def room_of(self, character: str) -> str | None:
        return self.characters.get(character, {}).get("room")

    def inventory(self, character: str) -> dict[str, int]:
        return dict(self.characters.get(character, {}).get("inventory", {}))

    def has_applied(self, event_id: str) -> bool:
        return event_id in self.applied

    def clock(self) -> MissionClock:
        """The mission clock as the shared kernel sees it. Absent `time` means minute zero."""
        return MissionClock(minute=int(self.time.get("minute", 0)))

    @property
    def scene(self) -> int:
        return self.clock().scenes

    # ---- the only way state changes --------------------------------------------------------------

    def apply(self, event: dict[str, Any]) -> dict[str, Any]:
        """Validate and apply one event. Returns a record of what changed."""
        event_id = str(event.get("id", "")).strip()
        kind = str(event.get("type", "")).strip()
        if not event_id:
            raise RejectedEvent("event has no id")
        if kind not in EVENT_TYPES:
            raise RejectedEvent(f"unknown event type: {kind}")
        if event_id in self.applied:
            # Idempotency is not politeness: a reconnecting session replays its queue.
            return {"id": event_id, "type": kind, "duplicate": True, "changes": {}}

        handler = getattr(self, f"_apply_{kind}", None)
        if handler is None:  # pragma: no cover - EVENT_TYPES and handlers must stay in step
            raise RejectedEvent(f"no handler for {kind}")
        changes = handler(event)

        self.applied.append(event_id)
        record = {"id": event_id, "type": kind, "actor": event.get("actor", ""),
                  "duplicate": False, "changes": changes}
        self.log.append(record)
        return record

    # ---- handlers -------------------------------------------------------------------------------

    def _require_character(self, name: str) -> dict[str, Any]:
        if name not in self.characters:
            raise RejectedEvent(f"unknown character: {name}")
        return self.characters[name]

    def _apply_join(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        if not name:
            raise RejectedEvent("join needs a character name")
        if name in self.characters:
            raise RejectedEvent(f"character already exists: {name}")
        room = str(event.get("room", "street"))
        if room not in self.rooms:
            raise RejectedEvent(f"unknown room: {room}")
        self.characters[name] = {"room": room, "inventory": {}, "hp": 6, "faction": None}
        return {"character": name, "room": room}

    def _apply_move(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        character = self._require_character(name)
        direction = str(event.get("direction", ""))
        exits = self.rooms[character["room"]]["exits"]
        if direction not in exits:
            raise RejectedEvent(f"no exit {direction!r} from {character['room']}")
        destination = exits[direction]
        character["room"] = destination
        return {"character": name, "room": destination}

    def _apply_say(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        character = self._require_character(name)
        if not str(event.get("text", "")).strip():
            raise RejectedEvent("say needs text")
        return {"character": name, "room": character["room"]}

    def _apply_take(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        character = self._require_character(name)
        item = str(event.get("item", ""))
        if not item:
            raise RejectedEvent("take needs an item")
        inventory = character.setdefault("inventory", {})
        inventory[item] = int(inventory.get(item, 0)) + 1
        return {"character": name, "item": item, "count": inventory[item]}

    def _apply_drop(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        character = self._require_character(name)
        item = str(event.get("item", ""))
        inventory = character.setdefault("inventory", {})
        if int(inventory.get(item, 0)) <= 0:
            raise RejectedEvent(f"{name} has no {item}")
        inventory[item] = int(inventory[item]) - 1
        if inventory[item] == 0:
            del inventory[item]
        return {"character": name, "item": item, "count": inventory.get(item, 0)}

    def _apply_spend(self, event: dict[str, Any]) -> dict[str, Any]:
        faction = str(event.get("faction", ""))
        resource = str(event.get("resource", ""))
        amount = int(event.get("amount", 0))
        if faction not in self.factions:
            raise RejectedEvent(f"unknown faction: {faction}")
        if amount <= 0:
            raise RejectedEvent("spend needs a positive amount")
        held = int(self.factions[faction]["resources"].get(resource, 0))
        if held < amount:
            raise RejectedEvent(f"{faction} has {held} {resource}, cannot spend {amount}")
        self.factions[faction]["resources"][resource] = held - amount
        return {"faction": faction, "resource": resource, "remaining": held - amount}

    def _apply_gain(self, event: dict[str, Any]) -> dict[str, Any]:
        faction = str(event.get("faction", ""))
        resource = str(event.get("resource", ""))
        amount = int(event.get("amount", 0))
        if faction not in self.factions:
            raise RejectedEvent(f"unknown faction: {faction}")
        if amount <= 0:
            raise RejectedEvent("gain needs a positive amount")
        resources = self.factions[faction]["resources"]
        resources[resource] = int(resources.get(resource, 0)) + amount
        return {"faction": faction, "resource": resource, "total": resources[resource]}

    def _apply_damage(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        character = self._require_character(name)
        amount = int(event.get("amount", 0))
        if amount <= 0:
            raise RejectedEvent("damage needs a positive amount")
        character["hp"] = max(0, int(character.get("hp", 0)) - amount)
        return {"character": name, "hp": character["hp"]}

    def _apply_heal(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        character = self._require_character(name)
        amount = int(event.get("amount", 0))
        if amount <= 0:
            raise RejectedEvent("heal needs a positive amount")
        character["hp"] = int(character.get("hp", 0)) + amount
        return {"character": name, "hp": character["hp"]}

    def _apply_faction_join(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        faction = str(event.get("faction", ""))
        character = self._require_character(name)
        if faction not in self.factions:
            raise RejectedEvent(f"unknown faction: {faction}")
        members = self.factions[faction]["members"]
        if name not in members:
            members.append(name)
        character["faction"] = faction
        return {"character": name, "faction": faction}

    def _apply_faction_leave(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        character = self._require_character(name)
        faction = character.get("faction")
        if faction and name in self.factions[faction]["members"]:
            self.factions[faction]["members"].remove(name)
        character["faction"] = None
        return {"character": name, "faction": None}

    def _apply_reputation(self, event: dict[str, Any]) -> dict[str, Any]:
        faction = str(event.get("faction", ""))
        name = str(event.get("character", ""))
        delta = int(event.get("delta", 0))
        if faction not in self.factions:
            raise RejectedEvent(f"unknown faction: {faction}")
        table = self.factions[faction]["reputation"]
        table[name] = max(-5, min(5, int(table.get(name, 0)) + delta))
        return {"faction": faction, "character": name, "reputation": table[name]}

    def _apply_flag(self, event: dict[str, Any]) -> dict[str, Any]:
        name = str(event.get("character", ""))
        character = self._require_character(name)
        key = str(event.get("key", ""))
        if not key:
            raise RejectedEvent("flag needs a key")
        character.setdefault("flags", {})[key] = event.get("value", True)
        return {"character": name, "key": key}

    def _apply_advance_time(self, event: dict[str, Any]) -> dict[str, Any]:
        """Move mission time. One standard action (one minute) unless the event says otherwise.

        Time is the one thing every scene, quest timer and patrol check reads, so it lives in the
        authoritative state and moves only through an event — never as a side effect of narration.
        """
        minutes = int(event.get("minutes", STANDARD_ACTION_MINUTES))
        if minutes <= 0:
            raise RejectedEvent("advance_time needs a positive number of minutes")
        clock = self.clock()
        tick = clock.advance(minutes)
        self.time["minute"] = tick.minute
        return {"minute": tick.minute, "scene": tick.scene,
                "scenes_elapsed": tick.scenes_elapsed}

    def _apply_sim_reconcile(self, event: dict[str, Any]) -> dict[str, Any]:
        """A simulation's summary becomes state only through a clamped, explicit delta."""
        faction = str(event.get("faction", ""))
        resource = str(event.get("resource", ""))
        delta = int(event.get("delta", 0))
        if faction not in self.factions:
            raise RejectedEvent(f"unknown faction: {faction}")
        if not -3 <= delta <= 3:
            raise RejectedEvent("a simulation delta is capped at +/-3 per reconcile")
        resources = self.factions[faction]["resources"]
        resources[resource] = max(0, int(resources.get(resource, 0)) + delta)
        return {"faction": faction, "resource": resource, "total": resources[resource],
                "delta": delta}

    # ---- persistence ----------------------------------------------------------------------------

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.snapshot(), indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "WorldState":
        data = json.loads(path.read_text(encoding="utf-8"))
        if int(data.get("schema_version", 0)) != SCHEMA_VERSION:
            raise RejectedEvent(f"unsupported world schema: {data.get('schema_version')}")
        return cls(rooms=data.get("rooms", {}), characters=data.get("characters", {}),
                   items=data.get("items", {}), factions=data.get("factions", {}),
                   time=dict(data.get("time", {})),
                   applied=list(data.get("applied", [])), log=list(data.get("log", [])))
