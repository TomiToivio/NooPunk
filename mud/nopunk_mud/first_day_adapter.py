"""Evennia adapter for Tony German's first-day WorldSession (#1217).

The console and the MUD must render the **same** session, not two parallel openings. This module
wraps the canonical `src.console.first_day` adapter and adds only presentation: it turns typed
Evennia commands into the existing first-day actions and stores the canonical
`WorldSession.to_snapshot()` on the caller.

No rules live here. It never rolls, never changes a sheet, never writes a second map and never
decides what Tony remembers. `CmdFirstDay` in `mud/commands/default_cmdsets.py` is the only
player-facing surface.
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

# Evennia runs with `mud/` as the working directory; the canonical console package lives at the
# repository root. Add the root without copying any module.
ROOT = Path(__file__).resolve().parents[2]
for _path in (ROOT, ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from src.console.first_day import (
    ACTOR,
    KIT,
    FirstDayError,
    available_first_day_actions,
    create_first_day,
    first_day_action,
    kit_of,
)
from src.console.world_session import WorldSession, WorldSessionError

__all__ = ["ACTOR", "FirstDayAdapter", "FirstDayAdapterError"]


class FirstDayAdapterError(ValueError):
    """The typed command cannot be expressed as a first-day action."""


class FirstDayAdapter:
    """One player's canonical first-day session, rendered through Evennia."""

    def __init__(self, session: WorldSession | None = None) -> None:
        self.session = session if session is not None else create_first_day()

    @classmethod
    def from_snapshot(cls, payload: Mapping[str, Any]) -> FirstDayAdapter:
        """Restore a saved morning; invalid snapshots are refused, never silently reset."""
        return cls(WorldSession.from_snapshot(payload))

    def snapshot(self) -> dict[str, Any]:
        return self.session.to_snapshot()

    def available(self) -> tuple[str, ...]:
        return available_first_day_actions(self.session)

    def status(self) -> str:
        actions = self.available()
        if not actions:
            return "First day complete. Tony has reported to Dr. Harri Romppainen at Ratakatu 12."
        return "Available: " + ", ".join(actions)

    def look(self) -> str:
        """The current place and scene, using the canonical graph view."""
        place = self.session.where(ACTOR) or "nowhere"
        scene = self.session.scene_id or "no scene"
        view = self.session.look(ACTOR)
        occupants = ", ".join(view["occupants"]) or "no one else"
        exits = ", ".join(view["exits"]) or "no exit"
        return (
            f"{view['label']} [{place}] | scene: {scene} | "
            f"occupants: {occupants} | exits: {exits}"
        )

    def kit_summary(self) -> str:
        """What the interface can see: issued items and whether they are live."""
        book = kit_of(self.session)
        parts = []
        for item_id in KIT:
            item = book.get(item_id)
            state = (
                "faulty"
                if item.fault
                else ("active" if item.active else "inspected/off")
            )
            parts.append(f"{item_id}:{state}")
        return "Kit | " + " | ".join(parts)

    def act(self, command: str) -> str:
        """Map one typed command to exactly one canonical action."""
        text = (command or "").strip().lower()
        if not text or text in ("status", "actions"):
            return self.status()
        if text in ("look", "here"):
            return self.look()
        if text == "kit":
            return self.kit_summary()
        if text in ("help", "?"):
            return self.help_text()

        # Accept the human form `inspect police_radio` and the canonical `inspect:police_radio`.
        if text.startswith("inspect "):
            text = "inspect:" + text.split(None, 1)[1].strip()
        elif text.startswith("connect "):
            text = "connect:" + text.split(None, 1)[1].strip()
        elif text.startswith("repair "):
            text = "repair:" + text.split(None, 1)[1].strip()

        try:
            return first_day_action(self.session, text)
        except (FirstDayError, WorldSessionError) as exc:
            raise FirstDayAdapterError(str(exc)) from exc

    @staticmethod
    def help_text() -> str:
        return (
            "firstday [wake|uniform|inspect <item>|connect <item>|repair <item>|"
            "dispatch|ride|arrive|report|look|kit|status]"
        )
