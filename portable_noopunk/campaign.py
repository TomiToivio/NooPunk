"""Engine-neutral application surface over the canonical case session (#1053, #1054).

This module used to be its own narrative prototype: invented locations (`unsa_hq`, `hospital`,
`library`), invented clues (`anomalous_clock`, `witness_statement`) and a "sidequest" that appears
nowhere in the game's own case material. That was a second game with a second idea of what a case is,
and it invented canon the author had not specified — the failure AGENTS.md §1 and §§1–2 of
docs/DESIGN_PRINCIPLES.md forbid.

It is now a **façade**: every command is translated into a call on
:class:`console.session.CaseSession`, which in turn calls `rules.investigation`. One case
(`data/scenarios/lakkahaltia/case_graph.json`), one discovery rule, one dice stream, one save format.
Frontends (`console.py`, `interfaces/*`) keep the `Game`/`Action`/`Outcome` vocabulary, so nothing that
presents the game had to change its own logic.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from console.session import STATE_VERSION as SESSION_STATE_VERSION
from console.session import CaseSession, SessionError, discover
from rules.investigation import Investigator, load_case_graph

STATE_VERSION = SESSION_STATE_VERSION

#: Where the real case lives, relative to a checkout. Override with NOOPUNK_CASE when installed.
DEFAULT_CASE = "data/scenarios/lakkahaltia/case_graph.json"

#: A starting sheet that can reach every scene. Rank 0 is trained in the Without Number baseline, so
#: this sheet holds the competencies the case demands rather than flattering numbers.
DEFAULT_SHEET: dict[str, int] = {"Notice": 1, "Talk": 1, "Administer": 1, "Survive": 0,
                                 "Heal": 0, "Know": 0, "Connect": 0}

EVENT_BY_KIND = {"travel": ("location_changed",), "discover": ("clue_found",),
                 "examine": ("clue_found",), "attach": ("evidence_recorded",),
                 "risk": ("check_rolled",), "conclude": ("case_completed",),
                 "theory": ("theory_stated",)}


def case_path(explicit: str | Path | None = None) -> Path:
    """Find the case graph: explicit path, NOOPUNK_CASE, or the checkout this file sits in."""
    for candidate in (explicit, os.environ.get("NOOPUNK_CASE")):
        if candidate:
            path = Path(candidate).expanduser()
            if not path.is_file():
                raise FileNotFoundError(f"case graph not found: {path}")
            return path
    for root in Path(__file__).resolve().parents:
        candidate = root / DEFAULT_CASE
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"cannot find {DEFAULT_CASE}; pass a path or set NOOPUNK_CASE")


@dataclass(frozen=True)
class Action:
    name: str


@dataclass(frozen=True)
class Outcome:
    message: str
    events: tuple[str, ...] = ()


@dataclass
class GameState:
    """What a frontend may read. A copy, never the session's own objects."""

    version: int = STATE_VERSION
    case_id: str = ""
    location: str = ""
    clues: list[str] = field(default_factory=list)
    theory: str = ""
    visited: list[str] = field(default_factory=list)
    finished: bool = False

    @classmethod
    def from_session(cls, session: CaseSession) -> GameState:
        return cls(version=STATE_VERSION, case_id=session.graph.case.id,
                   location=session.scene_id, clues=list(session.discovered),
                   theory=session.theory_id, visited=list(session.visited),
                   finished=session.concluded)


class Game:
    """One case, played through the canonical session; commands as strings for any frontend."""

    def __init__(self, state: GameState | None = None, *, seed: int = 7,
                 graph: Any | None = None, sheet: dict[str, int] | None = None) -> None:
        self._graph = graph or load_case_graph(case_path())
        self._seed = seed
        if state is None:
            self._session = CaseSession.start(
                self._graph,
                Investigator(name="Investigator", ratings=dict(sheet or DEFAULT_SHEET)),
                seed=seed)
        else:
            if state.version != STATE_VERSION:
                raise ValueError(f"unsupported campaign save version {state.version!r}")
            self._session = self._session_from_state(state)

    # -- construction helpers ------------------------------------------------ #

    def _session_from_state(self, state: GameState) -> CaseSession:
        data = {
            "state_version": STATE_VERSION,
            "case_id": state.case_id,
            "investigator": {"name": "Investigator", "ratings": dict(DEFAULT_SHEET)},
            "scene": state.location,
            "seed": self._seed,
            "visited": list(state.visited or [state.location]),
            "discovered": {clue_id: self._scene_of(clue_id) for clue_id in state.clues},
            "evidence": {},
            "theory": state.theory,
            "turns": 1,
            "concluded": state.finished,
            "conclusion": {},
            "events": [],
            "rng_state": [],
        }
        try:
            return CaseSession.from_dict(self._graph, data)
        except SessionError as exc:
            raise ValueError(str(exc)) from exc

    def _scene_of(self, clue_id: str) -> str:
        for scene in self._graph.case.scenes:
            if any(clue.id == clue_id for clue in scene.clues):
                return scene.id
        raise ValueError(f"unknown clue {clue_id!r}")

    # -- the frontend contract ----------------------------------------------- #

    @property
    def state(self) -> GameState:
        return GameState.from_session(self._session)

    @property
    def session(self) -> CaseSession:
        """The canonical session, for a frontend that wants the full transcript."""
        return self._session

    def available_actions(self) -> tuple[str, ...]:
        if self._session.concluded:
            return ("status",)
        actions: list[str] = ["look", "status"]
        actions += [f"go:{scene_id}" for scene_id in self._session.exits()]
        actions += [f"take:{clue_id}" for clue_id in self._session.open_clues()]
        actions += [f"theory:{hypothesis.id}" for hypothesis in self._graph.hypotheses]
        if self._session.theory_id:
            actions += [f"support:{clue_id}" for clue_id in self._session.discovered]
            actions += [f"contradict:{clue_id}" for clue_id in self._session.discovered]
        actions.append("risk:8")
        actions += [f"conclude:{hypothesis.id}" for hypothesis in self._graph.hypotheses]
        return tuple(dict.fromkeys(actions))

    def apply(self, action: Action) -> Outcome:
        name = action.name.strip().lower()
        if name not in self.available_actions():
            return Outcome("That action is not available here.")
        before = len(self._session.events)
        try:
            message = self._dispatch(name)
        except (SessionError, ValueError) as exc:
            return Outcome(str(exc))
        kinds = tuple(dict.fromkeys(
            kind for event in self._session.events[before:]
            for kind in EVENT_BY_KIND.get(event["kind"], ())))
        return Outcome(message, kinds)

    def _dispatch(self, name: str) -> str:
        session = self._session
        verb, _, argument = name.partition(":")
        if name == "look":
            result = session.look()
            granted = result["granted"]
            return ("You look around; nothing new." if not granted
                    else f"Evidence recorded: {', '.join(granted)}.")
        if name == "status":
            return (f"Scene {session.scene().title} ({session.scene_id}) · "
                    f"clues {len(session.discovered)} · theory {session.theory_id or 'none'} · "
                    f"case {'closed' if session.concluded else 'open'}")
        if verb == "go":
            result = session.travel(argument)
            return f"You arrive at {result['title']} ({argument})."
        if verb == "take":
            clue = session.take(argument)
            return f"Evidence recorded: {clue.fact}"
        if verb == "theory":
            session.choose_theory(argument)
            return f"Working theory: {argument}"
        if verb in ("support", "contradict"):
            if not session.theory_id:
                return "State a theory first."
            stance = "supports" if verb == "support" else "contradicts"
            session.attach(session.theory_id, argument, stance)
            return f"{argument} {stance} {session.theory_id}"
        if verb == "risk":
            result = session.risk(int(argument))
            bonus = f" + {result['rank']}" if result["rank"] else ""
            return (f"2d6 {result['dice'][0]}+{result['dice'][1]}{bonus} = {result['total']} vs "
                    f"{result['difficulty']} -> {'success' if result['success'] else 'failure'}")
        if verb == "conclude":
            result = session.conclude(argument)
            return (f"Recorded: {result['hypothesis']} ({result['family']}) · "
                    f"supports {result['supports']} · contradicts {result['contradicts']}. "
                    "The console does not decide the truth of the theory.")
        raise SessionError(f"unknown command {name!r}")

    # -- persistence --------------------------------------------------------- #

    def to_json(self) -> str:
        # Order of `discovered` is discovery order and is part of what a frontend shows, so no
        # sort_keys: sorting would silently reorder a player's evidence after a save/load.
        return json.dumps(self._session.to_dict())

    @classmethod
    def from_json(cls, serialized: str, *, graph: Any | None = None, seed: int = 7) -> Game:
        try:
            data = json.loads(serialized)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid campaign state: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError("invalid campaign state")
        if data.get("state_version") != STATE_VERSION:
            raise ValueError(f"unsupported campaign save version {data.get('state_version')!r}")
        resolved = graph or load_case_graph(case_path())
        try:
            session = CaseSession.from_dict(resolved, data)
        except SessionError as exc:
            raise ValueError(str(exc)) from exc
        game = cls(GameState.from_session(session), graph=resolved, seed=seed)
        game._session = session
        return game


def snapshot(game: Game) -> dict[str, Any]:
    """Presentation copy of the state, so a UI never holds the domain object."""
    return asdict(game.state)


__all__ = ["Action", "Game", "GameState", "Outcome", "case_path", "discover", "snapshot"]
