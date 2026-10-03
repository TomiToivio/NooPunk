"""Engine-neutral room/object/actor state for the issue #51 text prototype.

All bundled content uses the fixture: prefix and is non-canonical test/demo data.
The model defines storage shape only. It does not define combat, social, hacking,
psionic, equipment, advancement, or setting rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


FIXTURE_PREFIX = "fixture:"


@dataclass(slots=True)
class Item:
    item_id: str
    label: str
    description: str = ""
    takeable: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "label": self.label,
            "description": self.description,
            "takeable": self.takeable,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Item":
        return cls(
            item_id=str(data["item_id"]),
            label=str(data["label"]),
            description=str(data.get("description", "")),
            takeable=bool(data.get("takeable", True)),
        )


@dataclass(slots=True)
class Room:
    room_id: str
    label: str
    description: str
    exits: dict[str, str] = field(default_factory=dict)
    items: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "room_id": self.room_id,
            "label": self.label,
            "description": self.description,
            "exits": dict(self.exits),
            "items": list(self.items),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Room":
        return cls(
            room_id=str(data["room_id"]),
            label=str(data["label"]),
            description=str(data["description"]),
            exits={str(k): str(v) for k, v in dict(data.get("exits", {})).items()},
            items=[str(x) for x in data.get("items", [])],
        )


@dataclass(slots=True)
class ActorState:
    actor_id: str
    label: str
    room_id: str
    controller: str = "scripted"
    inventory: list[str] = field(default_factory=list)
    dialogue: dict[str, str] = field(default_factory=dict)
    #: Optional EP2-derived mechanics (#60 milestone items 4-11). ``None`` means the
    #: actor participates exactly as before, so fixture/scripted actors without a
    #: sheet are unaffected. Stored as a plain dict so this module keeps defining
    #: storage shape only and stays free of rules imports.
    sheet: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "actor_id": self.actor_id,
            "label": self.label,
            "room_id": self.room_id,
            "controller": self.controller,
            "inventory": list(self.inventory),
            "dialogue": dict(self.dialogue),
            "sheet": dict(self.sheet) if self.sheet is not None else None,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ActorState":
        sheet = data.get("sheet")
        return cls(
            actor_id=str(data["actor_id"]),
            label=str(data["label"]),
            room_id=str(data["room_id"]),
            controller=str(data.get("controller", "scripted")),
            inventory=[str(x) for x in data.get("inventory", [])],
            dialogue={str(k): str(v) for k, v in dict(data.get("dialogue", {})).items()},
            sheet=dict(sheet) if sheet else None,
        )


@dataclass(slots=True)
class AdventureState:
    adventure_id: str
    objective_item_id: str = ""
    completed_by: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_id": self.adventure_id,
            "objective_item_id": self.objective_item_id,
            "completed_by": self.completed_by,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AdventureState":
        return cls(
            adventure_id=str(data["adventure_id"]),
            objective_item_id=str(data.get("objective_item_id", "")),
            completed_by=str(data.get("completed_by", "")),
        )


@dataclass(slots=True)
class World:
    rooms: dict[str, Room]
    items: dict[str, Item]
    actors: dict[str, ActorState]
    adventure: AdventureState

    def validate(self) -> None:
        for room in self.rooms.values():
            for destination in room.exits.values():
                if destination not in self.rooms:
                    raise ValueError(f"Room {room.room_id!r} exits to unknown room {destination!r}.")
            for item_id in room.items:
                if item_id not in self.items:
                    raise ValueError(f"Room {room.room_id!r} contains unknown item {item_id!r}.")
        for actor in self.actors.values():
            if actor.room_id not in self.rooms:
                raise ValueError(f"Actor {actor.actor_id!r} is in unknown room {actor.room_id!r}.")
            for item_id in actor.inventory:
                if item_id not in self.items:
                    raise ValueError(f"Actor {actor.actor_id!r} holds unknown item {item_id!r}.")

    def actors_in(self, room_id: str) -> list[ActorState]:
        return [a for a in self.actors.values() if a.room_id == room_id]

    def to_dict(self) -> dict[str, Any]:
        return {
            "rooms": {k: v.to_dict() for k, v in self.rooms.items()},
            "items": {k: v.to_dict() for k, v in self.items.items()},
            "actors": {k: v.to_dict() for k, v in self.actors.items()},
            "adventure": self.adventure.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "World":
        world = cls(
            rooms={k: Room.from_dict(v) for k, v in dict(data["rooms"]).items()},
            items={k: Item.from_dict(v) for k, v in dict(data["items"]).items()},
            actors={k: ActorState.from_dict(v) for k, v in dict(data["actors"]).items()},
            adventure=AdventureState.from_dict(data["adventure"]),
        )
        world.validate()
        return world


def fixture_world(*, with_sheets: bool = True) -> World:
    """Small non-canonical adventure fixture with two routes to one objective.

    ``with_sheets`` attaches the non-canonical fixture character sheets (#60
    milestone items 4-11) to the actors. Passing ``False`` yields the original
    sheet-free world, which is what the earlier #51 tests exercise.
    """

    hub = FIXTURE_PREFIX + "hub"
    side = FIXTURE_PREFIX + "side"
    goal = FIXTURE_PREFIX + "goal"
    token = FIXTURE_PREFIX + "token"

    world = World(
        rooms={
            hub: Room(
                hub,
                "Fixture Hub",
                "A neutral test room for the local text prototype.",
                exits={"north": goal, "east": side},
            ),
            side: Room(
                side,
                "Fixture Side Room",
                "A second neutral test room containing an optional conversational actor.",
                exits={"west": hub, "north": goal},
            ),
            goal: Room(
                goal,
                "Fixture Goal Room",
                "A neutral destination room. Taking the fixture token completes the demo.",
                exits={"south": hub, "west": side},
                items=[token],
            ),
        },
        items={
            token: Item(
                token,
                "fixture token",
                "A non-canonical object used only to prove inventory, persistence and completion.",
            ),
        },
        actors={
            FIXTURE_PREFIX + "human": ActorState(
                FIXTURE_PREFIX + "human", "Human player", hub, controller="human"
            ),
            FIXTURE_PREFIX + "greeter": ActorState(
                FIXTURE_PREFIX + "greeter",
                "Scripted greeter",
                hub,
                controller="scripted",
                dialogue={
                    "default": "This is fixture dialogue. The goal can be reached by more than one route."
                },
            ),
            FIXTURE_PREFIX + "wanderer": ActorState(
                FIXTURE_PREFIX + "wanderer", "Dumb wanderer", hub, controller="dumb"
            ),
            FIXTURE_PREFIX + "llm-contact": ActorState(
                FIXTURE_PREFIX + "llm-contact", "LLM contact", side, controller="llm"
            ),
            FIXTURE_PREFIX + "llm-player": ActorState(
                FIXTURE_PREFIX + "llm-player", "LLM player", side, controller="llm_player"
            ),
        },
        adventure=AdventureState(FIXTURE_PREFIX + "adventure", objective_item_id=token),
    )
    if with_sheets:
        # Imported lazily so this module keeps defining storage shape only and the
        # #51 tests that use a sheet-free world do not pull in the rules kernel.
        from .sheet import fixture_sheets

        sheets = fixture_sheets()
        for actor_id, actor in world.actors.items():
            sheet = sheets.get(actor_id)
            if sheet is not None:
                actor.sheet = sheet.to_dict()
    world.validate()
    return world
