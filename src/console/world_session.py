"""The world graphs as a navigator (#1196 §6).

The graphs were a library: the console never read them, so a player could not walk the Physical graph
or see which scene the Story graph offers next. This adapter is the smallest thing that makes them
playable without inventing a second game loop.

Three constraints, straight from §6:

* **one canonical actor record** — an actor ID maps to exactly one sheet, and a sheet belongs to one
  actor; two names for one person is how state forks
* **explicit actor-ID mapping** — nothing is inferred from a name
* **CWN remains the action authority** — this adapter moves actors and lists scenes; it never rolls,
  spends Effort, or changes a sheet
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

try:
    from src.world.items import Kit
except ModuleNotFoundError:  # pragma: no cover
    from world.items import Kit

try:  # see src/world/scenes.py for why both import roots are supported
    from src.world.graphs import GraphError, WorldGraphs
except ModuleNotFoundError:  # pragma: no cover
    from world.graphs import GraphError, WorldGraphs  # type: ignore[no-redef]


class WorldSessionError(RuntimeError):
    """The session was asked for a fact it cannot supply without guessing."""


@dataclass
class WorldSession:
    """A navigable view over ``WorldGraphs`` for one table."""

    graphs: WorldGraphs
    sheets: dict[str, str] = field(default_factory=dict)
    flags: set[str] = field(default_factory=set)
    completed_goals: set[str] = field(default_factory=set)
    scene_id: str = ""
    kit: Kit | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "WorldSession":
        return cls(graphs=WorldGraphs.from_dict(payload))

    # -- identity ----------------------------------------------------------------------------
    def register(self, actor: str, sheet: str) -> str:
        """Bind an actor ID to a sheet, explicitly and once.

        Refuses a second sheet for the same actor and a second actor for the same sheet. The console
        and Evennia both read actors by ID; letting two IDs point at one sheet is how a character
        ends up in two places at once and nobody notices until the third session.
        """
        actor = self._text(actor, "actor")
        sheet = self._text(sheet, "sheet")
        existing = self.sheets.get(actor)
        if existing is not None and existing != sheet:
            raise WorldSessionError(
                f"actor {actor!r} is already bound to sheet {existing!r}; one actor, one sheet"
            )
        for other_actor, other_sheet in self.sheets.items():
            if other_sheet == sheet and other_actor != actor:
                raise WorldSessionError(
                    f"sheet {sheet!r} is already bound to actor {other_actor!r}; "
                    "two actor IDs for one sheet fork the state"
                )
        self.sheets[actor] = sheet
        return sheet

    def sheet_for(self, actor: str) -> str:
        try:
            return self.sheets[actor]
        except KeyError:
            raise WorldSessionError(
                f"actor {actor!r} has no sheet mapping; register it explicitly"
            ) from None

    def identity(self, actor: str) -> dict[str, Any]:
        """The same actor seen through every view — the seventh check of the paper procedure."""
        self.sheet_for(actor)
        try:
            avatar = self.graphs.cyber.at(actor)
        except GraphError:
            # Not being jacked in is a normal state, not an error: the actor simply has no avatar.
            avatar = None
        return {
            "actor": actor,
            "sheet": self.sheets[actor],
            "physical": self.graphs.physical.at(actor),
            "cyber": avatar,
            "social": actor in self.graphs.social.nodes,
        }

    # -- movement ----------------------------------------------------------------------------
    def where(self, actor: str) -> str | None:
        return self.graphs.physical.at(actor)

    def look(self, actor: str) -> dict[str, Any]:
        place = self.where(actor)
        if place is None:
            raise WorldSessionError(f"actor {actor!r} is not on the physical graph")
        node = self.graphs.physical.nodes[place]
        return {
            "place": place,
            "label": getattr(node, "label", place),
            "occupants": self.graphs.physical.occupants_at(place),
            "devices": self.graphs.cyber.devices_at(place),
            "exits": self.graphs.physical.adjacent(place),
        }

    def move(self, actor: str, destination: str) -> dict[str, Any]:
        """Move along the physical graph, refusing an impossible route instead of narrating it."""
        self.sheet_for(actor)
        try:
            if not self.graphs.physical.can_move(actor, destination):
                raise WorldSessionError(
                    f"no passable route from {self.where(actor)!r} to {destination!r}"
                )
            place = self.graphs.physical.move(actor, destination)
        except GraphError as exc:
            raise WorldSessionError(str(exc)) from exc
        return {"place": place, "label": getattr(self.graphs.physical.nodes[place], "label", place)}

    # -- story -------------------------------------------------------------------------------
    def scenes_available(self) -> tuple[str, ...]:
        """Which story scenes this table may enter next, given the flags and finished goals."""
        if not self.scene_id:
            return tuple(
                node.id for node in self.graphs.story.nodes.values()
                if getattr(node, "kind", "") == "series"
            )
        return self.graphs.story.available(
            self.scene_id, flags=self.flags, completed=self.completed_goals
        )

    def enter_scene(self, scene_id: str) -> str:
        if scene_id not in self.graphs.story.nodes:
            raise WorldSessionError(f"no story node {scene_id!r}")
        if self.scene_id and not self.graphs.story.can_enter(
            scene_id, flags=self.flags, completed=self.completed_goals
        ):
            raise WorldSessionError(f"scene {scene_id!r} is not enterable from here")
        self.scene_id = scene_id
        return scene_id

    def complete_goal(self, goal_id: str) -> None:
        self.completed_goals.add(self._text(goal_id, "goal"))

    # -- portable save for the graph/session adapter -----------------------------------------
    def to_snapshot(self) -> dict[str, Any]:
        """Persist the *same* world/session, not a second campaign state machine."""
        return {
            "session_format": "noopunk.world.session",
            "version": 1,
            "graphs": self.graphs.to_dict(),
            "sheets": dict(self.sheets),
            "flags": sorted(self.flags),
            "completed_goals": sorted(self.completed_goals),
            "scene_id": self.scene_id,
            **({"kit": self.kit.to_dict()} if self.kit is not None else {}),
        }

    @classmethod
    def from_snapshot(cls, payload: Mapping[str, Any]) -> "WorldSession":
        """Restore graph positions and first-day flags, rejecting forked actor sheets."""
        if payload.get("session_format") != "noopunk.world.session" or payload.get("version") != 1:
            raise WorldSessionError("unsupported world-session snapshot format or version")
        try:
            instance = cls(graphs=WorldGraphs.from_dict(payload["graphs"]))
            for actor, sheet in payload["sheets"].items():
                instance.register(actor, sheet)
            for field_name in ("flags", "completed_goals"):
                values = payload[field_name]
                if not isinstance(values, list) or any(
                    not isinstance(value, str) or not value.strip() for value in values
                ):
                    raise WorldSessionError(f"invalid {field_name} in snapshot")
                setattr(instance, field_name, set(values))
            scene_id = payload["scene_id"]
            if not isinstance(scene_id, str) or (
                scene_id and scene_id not in instance.graphs.story.nodes
            ):
                raise WorldSessionError("unknown scene in world-session snapshot")
            instance.scene_id = scene_id
            if "kit" in payload:
                instance.kit = Kit.from_dict(payload["kit"])
                if instance.kit.actor not in instance.sheets:
                    raise WorldSessionError("kit actor has no canonical session sheet")
            return instance
        except (KeyError, TypeError, ValueError, GraphError) as exc:
            raise WorldSessionError(f"invalid world-session snapshot: {exc}") from exc

    # -- helpers -----------------------------------------------------------------------------
    @staticmethod
    def _text(value: str, label: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise WorldSessionError(f"{label} must be a nonempty string")
        return value.strip()
