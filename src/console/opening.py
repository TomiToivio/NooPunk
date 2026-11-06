"""The opening as one flow: build the character, then play his first day (#1217).

Two halves already existed and never met. `rules.europol_lifepath.build_lifepath` validates a complete
set of character choices; `console.first_day` plays the authored first morning. Nothing called the
builder, so the officer who woke in Sörnäinen was **not** the officer anybody had built — the sheet
name was a string and the kit was a list of flags.

This module is the join, and nothing else:

* answers in, ``Lifepath`` out — every legality rule stays in the builder
* the session, the sheet name and the issued kit are bound to that result
* ``save()``/``load()`` round-trip the whole opening, so a half-played first morning resumes

No dice, no prose choices, no new session. CWN remains the action authority; the opening moves the
actor and switches kit on, and that is the whole of its power.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

try:  # same two import roots as `.first_day`; the first one is pytest's rootdir
    from src.rules.cwn_backgrounds import Background
    from src.rules.cwn_edges_foci import Edge
    from src.rules.europol_lifepath import Lifepath, build_lifepath
    from src.rules.scene_tags import PersonalityTag
    from src.world.items import Kit, first_day_kit
except ModuleNotFoundError:  # pragma: no cover - installed with src/ on PYTHONPATH
    from rules.cwn_backgrounds import Background  # type: ignore[no-redef]
    from rules.cwn_edges_foci import Edge  # type: ignore[no-redef]
    from rules.europol_lifepath import Lifepath, build_lifepath  # type: ignore[no-redef]
    from rules.scene_tags import PersonalityTag  # type: ignore[no-redef]
    from world.items import Kit, first_day_kit  # type: ignore[no-redef]

from .first_day import (
    ACTOR,
    KIT as ISSUED_KIT,
    LINKED,
    SHEET,
    available_first_day_actions,
    create_first_day,
    first_day_action,
)
from .world_session import WorldSession

#: The questions the flow asks, in order. A save that lacks one of these is not a partial opening —
#: it is a different character, and is refused rather than filled in with a default.
QUESTIONS: tuple[str, ...] = ("path", "attributes", "edges", "foci", "learning", "personality")

OPENING_FORMAT = "noopunk.opening"
OPENING_VERSION = 1


class OpeningError(ValueError):
    """The opening was built, loaded or advanced with something that is not a complete set of choices."""


@dataclass(frozen=True, slots=True)
class OpeningAnswers:
    """What the player chose. Ids, not objects: a catalogue decides what an id means."""

    path: str
    attributes: Mapping[str, int]
    edges: tuple[str, ...] = ()
    foci: tuple[str, ...] = ()
    learning: tuple[str, ...] = ()
    personality: tuple[PersonalityTag, ...] = ()

    def __post_init__(self) -> None:
        if self.path not in ("grunt", "geek", "freak"):
            raise OpeningError(f"unknown recruitment route {self.path!r}")
        if not self.attributes:
            raise OpeningError("a character needs attributes; the flow has no defaults")
        for name in ("edges", "foci", "learning", "personality"):
            value = getattr(self, name)
            if not isinstance(value, tuple):
                raise OpeningError(f"{name} must be a tuple, got {type(value).__name__}")

    def missing(self) -> tuple[str, ...]:
        """Questions a save did not answer. Used by ``load`` to explain a refused file."""
        return tuple(q for q in QUESTIONS if not hasattr(self, q))


@dataclass
class Opening:
    """A built character, his session and his kit — the three things a save must keep together."""

    lifepath: Lifepath
    session: WorldSession
    kit: Kit = field(default_factory=lambda: Kit(actor=ACTOR))
    events: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.session.sheet_for(ACTOR) != SHEET:
            raise OpeningError(
                "the opening session is not bound to Tony's canonical sheet; "
                "building a second session would fork the character"
            )
        if self.kit.actor != ACTOR:
            raise OpeningError("the kit belongs to Tony; a kit is actor-scoped")

    # -- reading -----------------------------------------------------------------------------
    def character(self) -> dict[str, Any]:
        return self.lifepath.to_dict()

    def actions(self) -> tuple[str, ...]:
        """First-day actions, plus switching on the radio or the phone once inspected.

        The authored flow inspects those two and never links them, because they are what Dispatch
        answers on. But `world.items` counts only *active* devices as coverage, and Dispatch needs
        `dispatch.call` covered — so the opening offers the two connections itself and refuses
        Dispatch until one of them is live. A radio you have looked at is not a radio you can hear.
        """
        base = available_first_day_actions(self.session)
        if "dispatch.call" not in self.kit.coverage():
            base = tuple(a for a in base if a != "dispatch")
        extra: list[str] = []
        for item_id in ("police_radio", "phone"):
            if item_id not in self.kit.items or self.kit.get(item_id).active:
                continue
            if "kit.fault:" + item_id in self.session.flags:
                continue  # a faulty device is repaired through the authored action, not connected
            if "first_day:inspect:" + item_id in self.session.flags:
                extra.append("connect:" + item_id)
        return tuple(base) + tuple(extra)

    def equipment(self) -> dict[str, Any]:
        """Kit state as the interface would show it: what is covered, what is missing."""
        return {
            "coverage": {function: list(sources)
                         for function, sources in self.kit.coverage().items()},
            "missing": list(self.kit.missing()),
            "active": sorted(item_id for item_id, carried in self.kit.items.items()
                             if carried.usable),
        }

    # -- playing -----------------------------------------------------------------------------
    def act(self, action: str) -> str:
        """One first-day action. The narrative flag and the equipment state advance together."""
        available = self.actions()
        if action not in available:
            raise OpeningError(
                f"action {action!r} is unavailable here; available: {', '.join(available) or 'none'}"
            )
        if action == "dispatch" and "dispatch.call" not in self.kit.coverage():
            raise OpeningError(
                "Dispatch cannot be answered yet: no radio and no phone is live"
            )
        if action.startswith("connect:") and action not in available_first_day_actions(self.session):
            # The radio and the phone: the flow inspects them, but Dispatch needs one of them live.
            item = action.split(":", 1)[1]
            carried = self.kit.get(item)
            if not carried.usable:
                raise OpeningError(f"{item!r} cannot be connected: it is stowed or faulty")
            self.kit.activate(item)
            self.session.flags.add("first_day:" + action)
            self.events.append(action)
            return f"Opened the line on {item.replace('_', ' ')}."
        message = first_day_action(self.session, action)
        if action.startswith("connect:"):
            item = action.split(":", 1)[1]
            carried = self.kit.get(item)
            if not carried.usable:
                raise OpeningError(f"{item!r} cannot be connected: it is stowed or faulty")
            self.kit.activate(item)
        self.events.append(action)
        return message

    def run(self, script: Iterable[str]) -> tuple[str, ...]:
        """Play a deterministic script. Used by tests and by the tabletop walkthrough."""
        messages = []
        for action in script:
            if action not in self.actions():
                raise OpeningError(
                    f"action {action!r} is unavailable here; available: {', '.join(self.actions())}"
                )
            messages.append(self.act(action))
        return tuple(messages)

    def script(self) -> tuple[str, ...]:
        """The shortest legal script from waking to reporting: no roll, no optional stop.

        The order is fixed: wake, dress, inspect the whole kit, bring every link up, answer
        Dispatch, ride, arrive, report. Inspecting everything before connecting anything is not an
        optimisation — it is what makes the equipment sequence a legible checklist rather than a
        guessing game about which device Dispatch wants.
        """
        order = ["wake", "uniform"]
        order += ["inspect:" + item for item in ISSUED_KIT]
        # Faults are found by inspecting, so any repair the authored flow offers comes first.
        order += ["repair:" + item for item in ISSUED_KIT]
        order += ["connect:" + item for item in ISSUED_KIT
                  if item in ("police_radio", "phone") or item in LINKED]
        order += ["dispatch", "ride", "arrive", "report"]
        actions: list[str] = []
        for step in order:
            if step in self.actions():
                actions.append(step)
                self.act(step)
        return tuple(actions)

    # -- saving ------------------------------------------------------------------------------
    def save(self) -> dict[str, Any]:
        return {
            "format": OPENING_FORMAT,
            "version": OPENING_VERSION,
            "lifepath": self.lifepath.to_dict(),
            "session": self.session.to_snapshot(),
            "kit": self.kit.to_dict(),
            "events": list(self.events),
        }

    @classmethod
    def load(cls, payload: Mapping[str, Any]) -> "Opening":
        if payload.get("format") != OPENING_FORMAT:
            raise OpeningError("not an opening save")
        if payload.get("version") != OPENING_VERSION:
            raise OpeningError(
                f"opening save version {payload.get('version')!r} is not {OPENING_VERSION}"
            )
        raw = payload["lifepath"]
        lifepath = Lifepath(
            path=raw["path"],
            attributes=dict(raw["attributes"]),
            background=raw["background"],
            edges=tuple(raw["edges"]),
            focus_levels=dict(raw["focus_levels"]),
            skills=dict(raw["skills"]),
            underdog=bool(raw["underdog"]),
            personality=tuple(
                PersonalityTag(**p) if isinstance(p, Mapping) else p
                for p in raw.get("personality", ())
            ),
            provenance=tuple(raw.get("provenance", ())),
        )
        session = WorldSession.from_snapshot(payload["session"])
        kit = Kit.from_dict(payload["kit"])
        opening = cls(lifepath=lifepath, session=session, kit=kit)
        opening.events = list(payload.get("events", ()))
        return opening


def build_opening(
    answers: OpeningAnswers,
    *,
    background: Background,
    edge_catalogue: Mapping[str, Edge],
    focus_catalogue: Mapping[str, object] | None = None,
    level: int = 1,
) -> Opening:
    """Resolve the answers, build the character, and bind the first day to him.

    Every refusal comes from ``build_lifepath`` and names the violation; this function adds only the
    one rule the builder cannot know: an Edge id must exist in the caller's catalogue, because a
    character built from an id nobody can look up is a typo with a sheet.
    """
    edges: list[Edge] = []
    for edge_id in answers.edges:
        try:
            edges.append(edge_catalogue[edge_id])
        except KeyError:
            raise OpeningError(
                f"Edge {edge_id!r} is not in the verified catalogue "
                f"({', '.join(sorted(edge_catalogue)) or 'empty'})"
            ) from None

    lifepath = build_lifepath(
        path=answers.path,
        attributes=answers.attributes,
        background=background,
        edges=tuple(edges),
        foci=answers.foci,
        learning_picks=answers.learning,
        personality=answers.personality,
        edge_catalogue=edge_catalogue,
        focus_catalogue=focus_catalogue,
        level=level,
    )

    session = create_first_day()
    kit = Kit(actor=ACTOR)
    for item in first_day_kit():
        kit.issue(item)
    return Opening(lifepath=lifepath, session=session, kit=kit)
