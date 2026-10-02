"""The canonical event envelope for the NoöPunk simulation.

Issue #40 Phase B. This module owns the *shape* of an event and the rules that
make the event log trustworthy. It defines no rules, mechanics, factions, or
simulation semantics: it stores what happened and who acted, nothing derived.

The two schema rules from ``docs/SIMULATION_ARCHITECTURE_SPEC.md`` §3 are enforced
here rather than left to callers:

1. **Ordering is ``turn``, never ``timestamp``.** A timestamp is recorded for the
   record, but it is not an ordering key: timestamps collide, drift, and are not
   reproducible, so a reducer that ordered by them would not replay identically.
2. **``source`` and ``synthetic`` are set by the emitting boundary, not the
   actor.** An LLM agent must not be able to emit an event claiming to be
   tabletop-sourced or non-synthetic, so those fields are supplied by the runtime
   seam that builds the event, never parsed from model output.

``event_id`` is derived deterministically from the event's own content plus its
occurrence index within that (simulation, turn,...) tuple. That makes replay
idempotent and de-duplication possible without a central counter, which is what
#40 asks for.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping

#: Which view emitted an event. Closed on purpose: an unknown source is a bug in
#: the emitting boundary, not new vocabulary.
EVENT_SOURCES = ("tabletop", "concordia", "godot", "system")

#: Visibility of a communication. Only ``public`` communications are available to
#: the LaclauGPT discourse layer (#40 §4); ``private`` is visible to the
#: simulation but is not a public communication.
VISIBILITIES = ("public", "private")


class EventValidationError(ValueError):
    """An event violates the envelope contract."""


def _text(raw: Any) -> str:
    if raw is None:
        return ""
    text = str(raw).strip()
    return "" if text.lower() in {"nan", "none", "<na>"} else text


def _require_text(value: Any, field_name: str) -> str:
    text = _text(value)
    if not text:
        raise EventValidationError(f"event field {field_name!r} must be non-empty")
    return text


@dataclass(frozen=True, slots=True)
class Event:
    """One immutable event in a simulation run.

    Every field the architecture depends on is explicit. Nothing here is derived
    from an LLM: ``actor`` names the entity that acted, ``content`` is the
    substance as text, and the provenance fields are set by the boundary.
    """

    simulation_id: str
    turn: int
    actor: str
    action_type: str
    source: str
    synthetic: bool
    event_id: str = ""
    timestamp: str = ""
    target: str = ""
    content: str = ""
    location: str = ""
    visibility: str = "public"
    #: Deterministic de-duplication ordinal; set by :meth:`create`, not by callers.
    occurrence: int = 0

    def __post_init__(self) -> None:
        _require_text(self.simulation_id, "simulation_id")
        _require_text(self.actor, "actor")
        _require_text(self.action_type, "action_type")
        if not isinstance(self.turn, int) or isinstance(self.turn, bool):
            raise EventValidationError("event field 'turn' must be an int")
        if self.turn < 0:
            raise EventValidationError("event field 'turn' must be >= 0")
        if self.source not in EVENT_SOURCES:
            raise EventValidationError(
                f"unknown event source {self.source!r}; expected one of {list(EVENT_SOURCES)}"
            )
        if not isinstance(self.synthetic, bool):
            raise EventValidationError(
                "event field 'synthetic' must be an explicit bool set by the emitting "
                "boundary, never inferred or defaulted"
            )
        if self.visibility not in VISIBILITIES:
            raise EventValidationError(
                f"unknown visibility {self.visibility!r}; expected one of {list(VISIBILITIES)}"
            )
        if self.event_id and not self.event_id.startswith("event:"):
            raise EventValidationError("event_id must use the 'event:' prefix")

    # -- construction ------------------------------------------------------ #

    @classmethod
    def create(
        cls,
        *,
        simulation_id: str,
        turn: int,
        actor: str,
        action_type: str,
        source: str,
        synthetic: bool,
        timestamp: str = "",
        target: str = "",
        content: str = "",
        location: str = "",
        visibility: str = "public",
        occurrence: int = 0,
    ) -> "Event":
        """Build an event, deriving ``event_id`` from its own content.

        The id is a pure function of the event contents and the occurrence index,
        so the same event built twice yields the same id (idempotent replay) while
        two genuinely distinct-but-identical acts in one turn stay distinct.
        """
        event_id = "event:" + _hash(
            simulation_id,
            str(turn),
            actor,
            action_type,
            source,
            target,
            content,
            location,
            visibility,
            str(occurrence),
        )
        return cls(
            simulation_id=simulation_id,
            turn=turn,
            actor=actor,
            action_type=action_type,
            source=source,
            synthetic=synthetic,
            event_id=event_id,
            timestamp=timestamp,
            target=target,
            content=content,
            location=location,
            visibility=visibility,
            occurrence=occurrence,
        )

    # -- serialization ----------------------------------------------------- #

    def to_dict(self) -> dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "event_id": self.event_id,
            "turn": self.turn,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "action_type": self.action_type,
            "target": self.target,
            "content": self.content,
            "location": self.location,
            "visibility": self.visibility,
            "source": self.source,
            "synthetic": self.synthetic,
            "occurrence": self.occurrence,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Event":
        """Rebuild an event from storage/JSON.

        ``synthetic`` is coerced to a real bool here because SQLite has no boolean
        type and returns 0/1. The constructor still requires an explicit bool: the
        coercion exists for *reading back* a stored event, never for constructing
        a new one, so the "boundary states synthetic explicitly" rule is intact.
        """
        missing = [
            name
            for name in ("simulation_id", "turn", "actor", "action_type", "source", "synthetic")
            if name not in payload
        ]
        if missing:
            raise EventValidationError(f"event payload missing required field(s): {missing}")
        return cls(
            simulation_id=payload["simulation_id"],
            turn=payload["turn"],
            actor=payload["actor"],
            action_type=payload["action_type"],
            source=payload["source"],
            synthetic=_as_bool(payload["synthetic"], "synthetic"),
            event_id=_text(payload.get("event_id")),
            timestamp=_text(payload.get("timestamp")),
            target=_text(payload.get("target")),
            content=_text(payload.get("content")),
            location=_text(payload.get("location")),
            visibility=_text(payload.get("visibility")) or "public",
            occurrence=int(payload.get("occurrence") or 0),
        )

    def is_public_communication(self) -> bool:
        """Whether the LaclauGPT layer may consume this (#40 §4)."""
        return self.visibility == "public"


def _as_bool(raw: Any, field_name: str) -> bool:
    """Strict bool for storage round-trips: accepts bool or 0/1, nothing else."""
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, int) and raw in (0, 1):
        return bool(raw)
    raise EventValidationError(
        f"event field {field_name!r} must be a bool (or 0/1 from storage), got {raw!r}"
    )


def _hash(*parts: str) -> str:
    payload = "\x1f".join(str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def order_key(event: Event) -> tuple[int, int]:
    """The canonical ordering key: ``(turn, occurrence)``, never a timestamp."""
    return (event.turn, event.occurrence)


def next_occurrence(events: list[Event], *, simulation_id: str, turn: int) -> int:
    """Occurrence index for a new event, so identical acts in one turn stay distinct."""
    return sum(
        1
        for event in events
        if event.simulation_id == simulation_id and event.turn == turn
    )


#: Fields a caller must never be able to set from model output.
BOUNDARY_OWNED_FIELDS = ("source", "synthetic", "event_id", "occurrence")
