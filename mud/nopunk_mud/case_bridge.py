"""Headless case interface for the MUD — the same engine the terminal plays (#1217).

#1217 requires *"one canonical actor ID and sheet across CLI/Evennia/GUI"* and that the first approved
investigation works *"consistently via selected interfaces"*. The MUD previously had no path to the
Lakkahaltia case at all: `solo_campaign.py` is a 62-line dataclass and `case_consciousness.py` is a
different, smaller case. Only the terminal could play it.

This module is the adapter, not a second game. It:

* loads the **same** `data/scenarios/lakkahaltia/case_graph.json`;
* drives the **same** `console.session.CaseSession` and the **same** `console.play.run_command`, so
  the command semantics, the clue invariants and the CWN rolls are identical by construction;
* binds the actor to a sheet through `world.actor_registry`, so a character cannot acquire a second
  sheet by entering through a second interface.

Nothing here resolves a rule. If a command needs a rule, it goes to the session.
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
for _candidate in (ROOT, ROOT / "src"):
    if str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))

from console.play import run_command
from console.session import (
    CaseSession,
    SessionError,
    load_session,
    save_session,
)
from rules.investigation import Investigator, load_case_graph

try:  # the repository import path, used by the root test suite
    from src.world.actor_registry import (
        ActorIdentityError,
        ActorRegistry,
        CanonicalActor,
        Handle,
    )
except ModuleNotFoundError:  # pragma: no cover - when only `src` is on the path
    from world.actor_registry import (
        ActorIdentityError,
        ActorRegistry,
        CanonicalActor,
        Handle,
    )

__all__ = ["DEFAULT_CASE", "CaseBridge", "CaseBridgeError"]

DEFAULT_CASE = "data/scenarios/lakkahaltia/case_graph.json"

#: The same competent-but-short sheet the terminal's walkthrough uses, so both interfaces reach the
#: whole case. A narrower sheet is allowed; it simply finds less.
DEFAULT_RATINGS: Mapping[str, int] = {
    "Notice": 1,
    "Talk": 1,
    "Administer": 1,
    "Survive": 0,
    "Heal": 0,
    "Know": 0,
    "Connect": 0,
}


class CaseBridgeError(RuntimeError):
    """The bridge was asked to do something the session or the registry refuses."""


def _bind_identity(registry: ActorRegistry, actor_id: str, sheet_id: str) -> None:
    """Make one actor own one sheet, or prove it already does.

    ``register`` refuses a second registration outright — including a renewal of the same actor — so
    an existing actor is *verified* rather than re-registered. A sheet that already belongs to another
    actor is refused by the registry itself, which is the whole point of routing identity through it.
    """
    try:
        existing = registry.actor(actor_id)
    except ActorIdentityError:
        registry.register(
            CanonicalActor(
                actor_id=actor_id,
                label=actor_id,
                handles=(Handle("sheet", sheet_id), Handle("physical", actor_id)),
            )
        )
        return
    owned = {handle.view: handle.handle for handle in existing.handles}
    if owned.get("sheet") != sheet_id:
        raise CaseBridgeError(
            f"actor {actor_id!r} already has sheet {owned.get('sheet')!r}; "
            f"{sheet_id!r} would be a second sheet for one character"
        )


@dataclass
class CaseBridge:
    """One actor, one sheet, one case session."""

    session: CaseSession
    actor_id: str
    sheet_id: str
    registry: ActorRegistry = field(repr=False, default_factory=ActorRegistry)

    # -- construction ---------------------------------------------------------------------------
    @classmethod
    def open(
        cls,
        *,
        actor_id: str,
        sheet_id: str,
        registry: ActorRegistry | None = None,
        case_path: str = DEFAULT_CASE,
        name: str = "",
        seed: int = 0,
        ratings: Mapping[str, int] | None = None,
    ) -> CaseBridge:
        """Start a case for one actor.

        The registry is the authority on identity: opening a second bridge for the same actor with a
        different sheet is refused here rather than discovered later as two divergent saves.
        """
        registry = registry if registry is not None else ActorRegistry()
        try:
            _bind_identity(registry, actor_id, sheet_id)
        except ActorIdentityError as error:  # sheet already belongs to another actor
            raise CaseBridgeError(str(error)) from None

        graph = load_case_graph(case_path)
        investigator = Investigator(name=name or actor_id, ratings=dict(ratings or DEFAULT_RATINGS))
        return cls(
            session=CaseSession.start(graph, investigator, seed=seed),
            actor_id=actor_id,
            sheet_id=sheet_id,
            registry=registry,
        )

    @classmethod
    def resume(
        cls,
        path: str | Path,
        *,
        actor_id: str,
        sheet_id: str,
        registry: ActorRegistry | None = None,
        case_path: str = DEFAULT_CASE,
    ) -> CaseBridge:
        """Load a save written by either interface."""
        registry = registry if registry is not None else ActorRegistry()
        try:
            _bind_identity(registry, actor_id, sheet_id)
        except ActorIdentityError as error:
            raise CaseBridgeError(str(error)) from None
        graph = load_case_graph(case_path)
        try:
            session = load_session(graph, path)
        except SessionError as error:
            raise CaseBridgeError(str(error)) from None
        return cls(session=session, actor_id=actor_id, sheet_id=sheet_id, registry=registry)

    # -- play -----------------------------------------------------------------------------------
    def command(self, line: str) -> tuple[bool, str]:
        """Run one command through the terminal's own dispatcher.

        Returns ``(keep_playing, output)`` exactly as the console does, so a MUD command can print
        the text it gets without knowing what any command means.
        """
        return run_command(self.session, line)

    def play(self, lines) -> list[str]:
        """Run a script of commands; stops at `quit` or the case ending."""
        output: list[str] = []
        for line in lines:
            keep_going, text = self.command(line)
            output.append(text)
            if not keep_going:
                break
        return output

    # -- state ----------------------------------------------------------------------------------
    def snapshot(self) -> dict[str, Any]:
        session_state = self.session.to_dict()
        session_state["interface"] = {"actor_id": self.actor_id, "sheet_id": self.sheet_id}
        return session_state

    def save(self, path: str | Path) -> Path:
        return save_session(self.session, path)

    def view(self) -> dict[str, Any]:
        """What an interface needs to render: scene, clues, exits, theory."""
        scene = self.session.scene()
        return {
            "scene": scene.id,
            "title": scene.title,
            "clues": list(self.session.open_clues()),
            "exits": list(self.session.exits()),
            "theory": self.session.theory() or "",
            "actor_id": self.actor_id,
            "sheet_id": self.sheet_id,
        }
