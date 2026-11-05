"""One actor, one sheet, many views (#1196 §6).

The graphs key everything by string: `PhysicalGraph.occupants`, `CyberGraph.avatars`,
`SocialGraph.nodes`, the text game's `ActorState.actor_id` and the character sheet. Until now the
identity between them was *conventional* — the same string was reused everywhere and nothing checked
it. That is the failure the paper procedure's seventh check names: an actor can be one person on the
sheet, another on the social graph and a third body in a room, and every module stays green.

This module makes the mapping explicit and checks it. It resolves **identity only**:

* CWN remains the action authority. There is no roll, modifier or resolution path here, and adding one
  would be a second rules engine.
* A view handle (``"physical:act.rookie"``, ``"social:npc.wendt"``) may differ from the canonical
  ``actor_id``; it may not differ *per view inconsistently*, and it may not belong to two actors.
* An **avatar is not a person** (#1178). An avatar handle resolves to the operator's canonical actor,
  and an avatar id that is also a registered actor is refused.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "VIEWS",
    "ActorIdentityError",
    "ActorRegistry",
    "CanonicalActor",
    "Handle",
]

#: Where an actor can appear. `sheet` is the character record itself; the rest are graph views.
VIEWS: tuple[str, ...] = ("physical", "cyber", "social", "story", "sheet")


class ActorIdentityError(ValueError):
    """An actor would be two people, or a handle would belong to two actors."""


@dataclass(frozen=True)
class Handle:
    view: str
    handle: str

    def __post_init__(self) -> None:
        if self.view not in VIEWS:
            raise ActorIdentityError(f"unknown view {self.view!r}; expected {VIEWS}")
        if not self.handle.strip():
            raise ActorIdentityError("a handle must be non-empty")

    @property
    def key(self) -> tuple[str, str]:
        return (self.view, self.handle)


@dataclass(frozen=True)
class CanonicalActor:
    """The one record: a canonical id, a label, and every other name it answers to."""

    actor_id: str
    label: str
    handles: tuple[Handle, ...] = ()

    def __post_init__(self) -> None:
        if not self.actor_id.strip():
            raise ActorIdentityError("a canonical actor needs an id")
        if not self.label.strip():
            raise ActorIdentityError(f"{self.actor_id!r} needs a label")
        keys = [handle.key for handle in self.handles]
        if len(set(keys)) != len(keys):
            raise ActorIdentityError(f"{self.actor_id!r} lists the same view handle twice")

    def in_view(self, view: str) -> str:
        for handle in self.handles:
            if handle.view == view:
                return handle.handle
        return self.actor_id


@dataclass
class ActorRegistry:
    """Canonical actors plus the reverse index from (view, handle) back to one actor."""

    actors: dict[str, CanonicalActor] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._index: dict[tuple[str, str], str] = {}
        for actor_id, actor in self.actors.items():
            if actor_id != actor.actor_id:
                raise ActorIdentityError(f"key {actor_id!r} does not match id {actor.actor_id!r}")
            self._index_actor(actor)

    # -- registration ---------------------------------------------------- #
    def register(self, actor: CanonicalActor) -> CanonicalActor:
        if actor.actor_id in self.actors:
            raise ActorIdentityError(f"actor {actor.actor_id!r} is already registered")
        # validate against a copy first: a rejected actor must not poison the index
        index = dict(self._index)
        for handle in actor.handles:
            if handle.key in index:
                raise ActorIdentityError(
                    f"{handle.view}:{handle.handle} already belongs to {index[handle.key]!r}"
                )
            if handle.handle in {other.actor_id for other in self.actors.values()}:
                raise ActorIdentityError(
                    f"{handle.handle!r} is another actor's canonical id; a handle cannot be a person"
                )
            index[handle.key] = actor.actor_id
        self.actors[actor.actor_id] = actor
        self._index = index
        return actor

    # -- resolution ------------------------------------------------------ #
    def canonical(self, view: str, handle: str) -> str:
        """Which actor is this handle in this view? Raises rather than guessing."""
        try:
            return self._index[(view, handle)]
        except KeyError:
            raise ActorIdentityError(
                f"{view}:{handle} is not mapped to any canonical actor; "
                "register the mapping instead of assuming the id matches"
            ) from None

    def actor(self, actor_id: str) -> CanonicalActor:
        try:
            return self.actors[actor_id]
        except KeyError:
            raise ActorIdentityError(f"unknown canonical actor {actor_id!r}") from None

    def handles(self, actor_id: str) -> tuple[Handle, ...]:
        return self.actor(actor_id).handles

    # -- the two checks that matter -------------------------------------- #
    def check_graphs(self, graphs: Any) -> list[str]:
        """Every occupant and avatar in the graphs must resolve to one canonical actor."""
        problems: list[str] = []
        for actor_id in sorted(graphs.physical.occupants):
            try:
                self.canonical("physical", actor_id)
            except ActorIdentityError as error:
                problems.append(str(error))
        for actor_id in sorted(graphs.cyber.avatars):
            try:
                self.canonical("cyber", actor_id)
            except ActorIdentityError as error:
                problems.append(str(error))
        return problems

    def check_avatar_operators(self, operators: Mapping[str, str]) -> list[str]:
        """An avatar is a session, not a person: it must name an operator who is an actor."""
        problems: list[str] = []
        for avatar_id, operator_id in operators.items():
            if avatar_id in self.actors:
                problems.append(
                    f"{avatar_id!r} is a registered actor and cannot also be an avatar; "
                    "an avatar is a session, not a person (#1178)"
                )
            if operator_id not in self.actors:
                problems.append(f"avatar {avatar_id!r} names unknown operator {operator_id!r}")
        return problems

    def one_sheet(self, *, sheets: Mapping[str, str]) -> list[str]:
        """The seventh check: an actor's sheet reference must be its own, and unique."""
        problems: list[str] = []
        seen: dict[str, str] = {}
        for actor_id, sheet_id in sheets.items():
            if actor_id not in self.actors:
                problems.append(f"sheet holder {actor_id!r} is not a canonical actor")
                continue
            if sheet_id in seen:
                problems.append(
                    f"{actor_id!r} and {seen[sheet_id]!r} share one sheet {sheet_id!r}; "
                    "one actor, one sheet"
                )
            seen[sheet_id] = actor_id
        return problems

    # -- serialization --------------------------------------------------- #
    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "noopunk.actor_registry",
            "version": 1,
            "actors": [
                {
                    "actor_id": actor_id,
                    "label": self.actors[actor_id].label,
                    "handles": [
                        {"view": handle.view, "handle": handle.handle}
                        for handle in self.actors[actor_id].handles
                    ],
                }
                for actor_id in sorted(self.actors)
            ],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> ActorRegistry:
        registry = cls()
        for raw in payload.get("actors", ()):
            registry.register(
                CanonicalActor(
                    actor_id=str(raw["actor_id"]),
                    label=str(raw["label"]),
                    handles=tuple(
                        Handle(str(item["view"]), str(item["handle"]))
                        for item in raw.get("handles", ())
                    ),
                )
            )
        return registry

    # -- internals ------------------------------------------------------- #
    def _index_actor(self, actor: CanonicalActor) -> None:
        for handle in actor.handles:
            if handle.key in self._index:
                raise ActorIdentityError(
                    f"{handle.view}:{handle.handle} already belongs to {self._index[handle.key]!r}"
                )
            self._index[handle.key] = actor.actor_id
