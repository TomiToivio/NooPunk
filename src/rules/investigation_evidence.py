"""NoöPunk #226: deterministic evidence and custody records, not automated proof.

Case data can be read at the tabletop or serialized by a computer RPG.
LLM GM/NPC outputs may propose witness testimony, but not rewrite ledger history.
All rules text/code here is independently authored for NoöPunk.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal

Provenance = Literal["physical", "digital", "testimony", "psi_lead", "other"]
Kind = Literal["collect", "transfer", "analyze", "question", "seal"]


@dataclass(frozen=True)
class Evidence:
    id: str
    label: str
    provenance: Provenance
    found_at: str
    collector: str
    session_id: str

    def __post_init__(self) -> None:
        for key in ("id", "label", "found_at", "collector", "session_id"):
            if not getattr(self, key).strip():
                raise ValueError(f"{key} cannot be blank")
        if self.provenance not in ("physical", "digital", "testimony", "psi_lead", "other"):
            raise ValueError("invalid evidence provenance")


@dataclass(frozen=True)
class CustodyEvent:
    ordinal: int
    evidence_id: str
    actor: str
    kind: Kind
    note: str
    recipient: str | None = None


@dataclass
class EvidenceLedger:
    items: dict[str, Evidence] = field(default_factory=dict)
    events: list[CustodyEvent] = field(default_factory=list)
    custodians: dict[str, str] = field(default_factory=dict)

    def collect(self, evidence: Evidence) -> CustodyEvent:
        if evidence.id in self.items:
            raise ValueError("duplicate evidence ID")
        self.items[evidence.id] = evidence
        self.custodians[evidence.id] = evidence.collector
        return self._record(evidence.id, evidence.collector, "collect", "Initial collection")

    def event(self, evidence_id: str, actor: str, kind: Kind, note: str,
              recipient: str | None = None) -> CustodyEvent:
        if evidence_id not in self.items:
            raise KeyError(evidence_id)
        if not actor.strip() or not note.strip():
            raise ValueError("actor and note required")
        if kind not in ("transfer", "analyze", "question", "seal"):
            raise ValueError("invalid event kind")
        if kind == "transfer":
            if self.custodians[evidence_id] != actor:
                raise PermissionError("Only current custodian may transfer evidence")
            if not recipient or not recipient.strip():
                raise ValueError("transfer requires recipient")
            record = self._record(evidence_id, actor, kind, note, recipient)
            self.custodians[evidence_id] = recipient
            return record
        if kind in ("analyze", "seal") and self.custodians[evidence_id] != actor:
            raise PermissionError("Only custodian may analyze or seal evidence")
        return self._record(evidence_id, actor, kind, note)

    def _record(self, evidence_id: str, actor: str, kind: Kind, note: str,
                recipient: str | None = None) -> CustodyEvent:
        record = CustodyEvent(len(self.events) + 1, evidence_id, actor, kind, note, recipient)
        self.events.append(record)
        return record

    def history(self, evidence_id: str) -> tuple[CustodyEvent, ...]:
        if evidence_id not in self.items:
            raise KeyError(evidence_id)
        return tuple(x for x in self.events if x.evidence_id == evidence_id)

    def export(self) -> dict:
        """Stable JSON-friendly snapshot; append-only events (no inference)."""
        return {
            "items": [asdict(self.items[k]) for k in sorted(self.items)],
            "events": [asdict(e) for e in self.events],
            "custodians": dict(sorted(self.custodians.items())),
        }

    def lead_only(self, evidence_id: str) -> bool:
        """PSI impressions are leads, never automatic admissible proof."""
        return self.items[evidence_id].provenance == "psi_lead"
