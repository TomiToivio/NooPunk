"""Read-only adapter for LaclauGPT AI26 canonical research records (#1286).

The adapter consumes a JSON-compatible canonical record, validates its identity
and analysis section, and extracts only what the simulator can honestly use:
claims/signifiers, explicit equivalence/difference articulations, review status
and uncertainty. It **does not** write back to the analysis record, infer a
relation from co-occurrence, or treat an AI26 interpretation as observed
behavior.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from itertools import pairwise
from typing import Any

from .model import Articulation, Claim, Material, Provenance

__all__ = ["AI26Adapter", "AI26Export", "AdapterError"]

#: Fields whose items can be represented as claims. Strings become a label-only
#: claim; mappings must provide a label under ``label`` or ``text``.
CLAIM_FIELDS = (
    "signifiers",
    "nodal_points",
    "formations",
    "discourses",
    "imaginaries",
    "us",
    "them",
    "frontier",
    "themes",
)

#: Explicit relation fields only. ``relations`` may mix relation types; only the
#: two discourse-theoretical relations the simulator understands are used.
ARTICULATION_FIELDS = ("equivalence_chains", "difference_chains")


class AdapterError(ValueError):
    """The export cannot be represented without inventing or losing evidence."""


def _text(value: Any, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise AdapterError(f"{field_name} must be non-empty")
    return text


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")
    if cleaned:
        return cleaned[:48]
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]


@dataclass(frozen=True)
class AI26Export:
    """A validated, read-only projection of one AI26 canonical record."""

    source_url: str
    schema_version: str
    claims: tuple[Claim, ...] = ()
    articulations: tuple[Articulation, ...] = ()
    review_status: str = "PROVISIONAL"
    review_flags: tuple[str, ...] = ()
    uncertainty: tuple[Mapping[str, Any], ...] = ()
    abstentions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_url": self.source_url,
            "schema_version": self.schema_version,
            "claims": [claim.to_dict() for claim in self.claims],
            "articulations": [
                articulation.to_dict() for articulation in self.articulations
            ],
            "review_status": self.review_status,
            "review_flags": list(self.review_flags),
            "uncertainty": [dict(item) for item in self.uncertainty],
            "abstentions": list(self.abstentions),
            "warnings": list(self.warnings),
        }


@dataclass
class AI26Adapter:
    """Convert and validate AI26 canonical analysis without mutating it."""

    export: AI26Export

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> AI26Adapter:
        source_url = _text(payload.get("source_url"), "source_url")
        schema_version = _text(payload.get("schema_version"), "schema_version")
        analysis = payload.get("analysis")
        if not isinstance(analysis, Mapping):
            raise AdapterError(
                "analysis must be an object; a collection-only record is not a simulation input"
            )
        review = (
            payload.get("review") if isinstance(payload.get("review"), Mapping) else {}
        )
        review_status = str(
            review.get("status") or analysis.get("status") or "PROVISIONAL"
        )
        flags = tuple(
            str(flag) for flag in review.get("flags", ()) if str(flag).strip()
        )

        claims: list[Claim] = []
        warnings: list[str] = []
        for field_name in CLAIM_FIELDS:
            rows = analysis.get(field_name)
            if rows is None:
                continue
            if isinstance(rows, str):
                rows = [rows]
            if not isinstance(rows, list):
                warnings.append(f"{field_name} is not a list; ignored")
                continue
            for index, raw in enumerate(rows):
                try:
                    label, kind, uncertainty = _claim_row(raw, field_name)
                except AdapterError as exc:
                    warnings.append(f"{field_name}[{index}] ignored: {exc}")
                    continue
                claim_id = f"{_slug(field_name)}:{_slug(label)}"
                # Duplicate labels in one category are one claim, not a new fact.
                if any(claim.id == claim_id for claim in claims):
                    continue
                claims.append(
                    Claim(
                        id=claim_id,
                        label=label,
                        kind=kind,
                        provenance=Provenance(
                            Material.INFERRED,
                            f"{source_url}#analysis.{field_name}[{index}]",
                            method="laclaugpt-ai26-canonical-export",
                            uncertainty=uncertainty,
                            review_status=review_status,
                        ),
                        uncertainty=uncertainty,
                    )
                )

        by_label = {claim.label: claim for claim in claims}
        articulations: list[Articulation] = []
        for field_name in ARTICULATION_FIELDS:
            rows = analysis.get(field_name)
            if not isinstance(rows, list):
                continue
            relation = (
                "equivalence" if field_name.startswith("equivalence") else "difference"
            )
            for index, raw in enumerate(rows):
                if not isinstance(raw, Mapping):
                    warnings.append(f"{field_name}[{index}] ignored: not an object")
                    continue
                refs = raw.get("member_refs") or raw.get("members") or ()
                labels = [str(item) for item in refs if str(item).strip()]
                for left_label, right_label in pairwise(labels):
                    left = by_label.get(left_label)
                    right = by_label.get(right_label)
                    if left is None or right is None or left.id == right.id:
                        warnings.append(
                            f"{field_name}[{index}] ignored: unknown or identical endpoints"
                        )
                        continue
                    art_id = f"{relation}:{left.id}->{right.id}"
                    if any(item.id == art_id for item in articulations):
                        continue
                    articulations.append(
                        Articulation(
                            id=art_id,
                            left=left.id,
                            right=right.id,
                            relation=relation,
                            provenance=Provenance(
                                Material.INFERRED,
                                f"{source_url}#analysis.{field_name}[{index}]",
                                method="laclaugpt-ai26-canonical-export",
                                uncertainty=0.0,
                                review_status=review_status,
                            ),
                        )
                    )

        uncertainty = tuple(
            dict(item)
            for item in analysis.get("uncertainty", ())
            if isinstance(item, Mapping)
        )
        abstentions = tuple(
            str(item) for item in analysis.get("abstentions", ()) if str(item).strip()
        )
        return cls(
            AI26Export(
                source_url=source_url,
                schema_version=schema_version,
                claims=tuple(claims),
                articulations=tuple(articulations),
                review_status=review_status,
                review_flags=flags,
                uncertainty=uncertainty,
                abstentions=abstentions,
                warnings=tuple(warnings),
            )
        )

    @classmethod
    def from_json(cls, path: str) -> AI26Adapter:
        import json
        from pathlib import Path

        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def apply_to(self, simulation: Any) -> None:
        """Add the export's claims and articulations to a simulation, without actors."""
        known = set(simulation.claims)
        for claim in self.export.claims:
            if claim.id not in known:
                simulation.add_claim(claim)
                known.add(claim.id)
        for articulation in self.export.articulations:
            if articulation.id not in simulation.articulations:
                simulation.add_articulation(articulation)

    def claim_ids(self) -> tuple[str, ...]:
        return tuple(claim.id for claim in self.export.claims)


def _claim_row(raw: Any, field_name: str) -> tuple[str, str, float]:
    if isinstance(raw, str):
        label = _text(raw, field_name)
        return (
            label,
            "signifier" if field_name == "signifiers" else field_name.rstrip("s"),
            0.0,
        )
    if not isinstance(raw, Mapping):
        raise AdapterError("claim must be a string or object")
    label = _text(raw.get("label") or raw.get("text") or raw.get("name"), "claim label")
    kind = str(
        raw.get("kind")
        or ("signifier" if field_name == "signifiers" else field_name.rstrip("s"))
    )
    uncertainty = raw.get("uncertainty", raw.get("confidence", 0.0))
    try:
        uncertainty = float(uncertainty)
    except (TypeError, ValueError) as exc:
        raise AdapterError("claim confidence is not numeric") from exc
    if not 0.0 <= uncertainty <= 1.0:
        raise AdapterError("claim confidence must be between 0 and 1")
    return label, kind, uncertainty
