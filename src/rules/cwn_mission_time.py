"""Cities Without Number: scenes, rounds and mission time.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``), ``rules-of-the-game/scenes-rounds-mission-time/``.

## The three clocks, as the SRD states them

* **round** — about six seconds, the unit of combat.
* **scene** — one fight, chase or other tense activity. The SRD says a scene "usually doesn't take
  more than ten or fifteen minutes", and that during mission time a scene is spent when ten minutes
  pass or when a fight ends, whichever comes first. This module uses the ten-minute bound, which is
  the one a clock can be run on; a caller that ends a scene early calls :meth:`MissionClock.end_scene`.
* **mission time** — minutes counted from minute zero, one per standard action. It is the clock that
  drives patrol discovery and escalating security response, so it belongs to the world state, not to
  a character.

## Why this is a module and not three constants

Per-scene abilities need one authority for "has the scene refreshed". If each ability counts for
itself, two of them will disagree about the same fight, and the disagreement is invisible until a
player notices a power that worked at minute 9 and not at minute 11. One clock, one answer — the
same reason the Godot kernel keeps one (``godot/core/cwn_mission_time.gd``).

## What this module does not do

It does not know about patrols, alarms or quests; it reports elapsed time, and the caller decides
what that means. It does not model movement, and it does not decide when a fight ends.
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: SRD: a combat round is about six seconds.
ROUND_SECONDS = 6

#: SRD: a scene is spent after ten minutes of mission time (the lower bound of "ten or fifteen").
SCENE_MINUTES = 10

#: SRD: one standard action is one minute of mission time.
STANDARD_ACTION_MINUTES = 1


class MissionTimeError(ValueError):
    """The clock was asked to run backwards, or to start somewhere impossible."""


@dataclass(frozen=True, slots=True)
class Tick:
    """What one advance did: where the clock is now, and what crossed on the way."""

    minute: int
    scene: int
    scenes_elapsed: int

    @property
    def scene_refreshed(self) -> bool:
        return self.scenes_elapsed > 0


@dataclass
class MissionClock:
    """Minutes from minute zero, and how many scenes that is.

    ``minute`` starts at zero and only moves forwards. ``scene`` is derived, never stored twice:
    two fields that must agree are one field and a bug waiting to happen.
    """

    minute: int = 0
    scenes: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.minute < 0:
            raise MissionTimeError("mission time does not run backwards")
        self.scenes = self.minute // SCENE_MINUTES

    def advance(self, minutes: int = STANDARD_ACTION_MINUTES) -> Tick:
        """Move the clock forward; report whether that crossed a scene boundary.

        A jump longer than a scene reports how many scenes it crossed, so a caller can expire a
        per-scene ability the right number of times instead of once.
        """
        if minutes < 0:
            raise MissionTimeError("mission time does not run backwards")
        before = self.scenes
        self.minute += minutes
        self.scenes = self.minute // SCENE_MINUTES
        return Tick(minute=self.minute, scene=self.scenes, scenes_elapsed=self.scenes - before)

    def spend_action(self, minutes: int = STANDARD_ACTION_MINUTES) -> Tick:
        """A standard action, one minute by the SRD. Named so callers read as the rules do."""
        return self.advance(minutes)

    def end_scene(self) -> Tick:
        """End the current scene early — a fight that finished inside the ten minutes.

        The SRD lets a fight end a scene; this reports the refresh without moving the mission
        clock, because the minutes were already spent by the actions inside it.
        """
        before = self.scenes
        self.scenes = self.minute // SCENE_MINUTES + 1
        return Tick(minute=self.minute, scene=self.scenes, scenes_elapsed=self.scenes - before)

    @property
    def minutes_into_scene(self) -> int:
        """How far into the current ten-minute window the clock stands.

        Measured from the window, not from the scene index: :meth:`end_scene` can make the index
        run ahead of the window, and the minutes are the fact the rules spend.
        """
        return self.minute % SCENE_MINUTES
