"""Where a value came from (#1286).

The issue's acceptance criterion is that schemas "distinguish observed, inferred, synthesized and simulated material;
provenance and uncertainty survive round trips". A single ``"provenance": "simulated"`` string on an export cannot do
that once empirical and synthetic records sit in one document, so the distinction is a small typed record here and every
producer carries one.

Nothing in this module interprets anything: it records an origin and the evidence for it, and it refuses an origin it
does not know rather than defaulting.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

__all__ = ["Origin", "Provenance", "ProvenanceError"]


class ProvenanceError(ValueError):
    """An origin a record may not claim, or a provenance document that cannot be read."""


class Origin(str, Enum):
    """The four kinds of material, kept apart end to end."""

    OBSERVED = "observed"        # taken from AI26 output exactly
    INFERRED = "inferred"        # analysis or researcher judgement over observed material
    SYNTHESIZED = "synthesized"  # invented for a scenario
    SIMULATED = "simulated"      # produced by a rule during a run


@dataclass(frozen=True, slots=True)
class Provenance:
    """An origin plus the source, method and uncertainty that justify it.

    ``review_status`` carries the AI26 review vocabulary when the record came from analysis
    (``provisional``, ``reviewed``, ``validated``, ``rejected``, ``needs_review``); for a synthetic record it is empty,
    because no reviewer has seen it yet and saying otherwise would be a claim.
    """

    origin: Origin
    source: str = ""
    method: str = ""
    uncertainty: str = ""
    review_status: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.origin, Origin):
            raise ProvenanceError(f"origin must be an Origin, got {self.origin!r}")

    def to_dict(self) -> dict[str, str]:
        return {
            "origin": self.origin.value,
            "source": self.source,
            "method": self.method,
            "uncertainty": self.uncertainty,
            "review_status": self.review_status,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Provenance":
        try:
            origin = Origin(str(payload["origin"]))
        except (KeyError, ValueError) as exc:
            raise ProvenanceError(f"unreadable provenance origin in {payload!r}") from exc
        return cls(
            origin=origin,
            source=str(payload.get("source") or ""),
            method=str(payload.get("method") or ""),
            uncertainty=str(payload.get("uncertainty") or ""),
            review_status=str(payload.get("review_status") or ""),
        )
