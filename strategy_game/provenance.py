"""Provenance records: keep source-supported material distinct from authored, generated or simulated.

Issue #282 asks that evidence and provenance be stored **separately from simulated or generated
discourse**, and that empirical extraction/interpretation be distinguished from hypothetical
simulation transitions. `strategy_game/docs/INTEGRATION_BOUNDARIES.md` adds the rule this module
takes most seriously:

    "absence of provenance must remain visibly unknown, not be silently upgraded into evidence"

So the default kind is :attr:`ProvenanceKind.UNKNOWN`, never ``EVIDENCE``. This module is a data
container and nothing else — no rules, no confidence model, no thresholds, no transitions.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ProvenanceKind(Enum):
    """Where a stored record came from. A category, not a quality or reliability judgement."""

    #: Not recorded. Deliberately the default: unknown stays visible rather than being read as fact.
    UNKNOWN = "unknown"
    #: Observed / source-supported extraction or interpretation (the empirical side).
    EVIDENCE = "evidence"
    #: A fictional authored event.
    AUTHORED = "authored"
    #: Machine- or template-generated text.
    GENERATED = "generated"
    #: A hypothetical simulation result or transition — modelled, not observed.
    SIMULATED = "simulated"


#: The declared value set, so callers can validate without constructing an enum member.
PROVENANCE_KINDS: tuple[str, ...] = tuple(kind.value for kind in ProvenanceKind)

#: Kinds that are *not* evidence, for callers that must never treat them as observations.
NON_EVIDENCE_KINDS: tuple[ProvenanceKind, ...] = tuple(
    kind for kind in ProvenanceKind if kind is not ProvenanceKind.EVIDENCE
)


@dataclass
class Provenance:
    """A stored record's origin. Serializes to plain JSON scalars; the scaffold interprets nothing."""

    kind: ProvenanceKind = ProvenanceKind.UNKNOWN
    #: Free-text origin (document, session, adapter). Never interpreted by the scaffold.
    source: str = ""
    #: Free-text note for the author. Never interpreted by the scaffold.
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind.value, "source": self.source, "note": self.note}

    @classmethod
    def from_dict(cls, data: Any) -> "Provenance":
        """Rebuild from :meth:`to_dict` output, or from a legacy bare string.

        ``Event.provenance`` used to be a plain ``str``. A string payload is read as the ``source``
        and the kind stays :attr:`ProvenanceKind.UNKNOWN` — a legacy string is an unclassified
        origin, so promoting it to ``EVIDENCE`` would be exactly the silent upgrade the boundary
        note forbids.
        """
        if data is None:
            return cls()
        if isinstance(data, Provenance):
            return data
        if isinstance(data, str):
            return cls(source=data)
        kind = str(data.get("kind", ProvenanceKind.UNKNOWN.value))
        return cls(
            kind=ProvenanceKind(kind) if kind in PROVENANCE_KINDS else ProvenanceKind.UNKNOWN,
            source=str(data.get("source", "")),
            note=str(data.get("note", "")),
        )

    def is_kind(self, kind: ProvenanceKind) -> bool:
        return self.kind is kind

    @property
    def is_evidence(self) -> bool:
        """True only when the record is explicitly classified as evidence."""
        return self.kind is ProvenanceKind.EVIDENCE

    @property
    def is_unknown(self) -> bool:
        return self.kind is ProvenanceKind.UNKNOWN
