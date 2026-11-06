"""Read-only AI26 adapter: LaclauGPT canonical analysis → simulator input (#1286, work package 2).

The simulator may not invent its empirical input, and it may not launder an interpretation into an
observation. This module is the one door a canonical LaclauGPT AI26 record comes through, and it does
four things and nothing else:

* **validates** the published canonical contract — `schema_version` 1.2.0, a source identity, resolvable
  provenance, resolvable evidence tied to that same source, and a review state that is not a rejection;
* **projects** the discourse objects the analysis coded into :class:`ImportedClaim` and the *explicit*
  articulations into :class:`ImportedArticulation`, keeping the canonical ids so a reader can go back to
  the record;
* **labels material**: an evidence span is ``observed`` text, an analysis object or relation is
  ``inferred``, and neither becomes ``simulated`` until a rule in the kernel produces something;
* **refuses** rather than coerces — an unsupported schema version, a dangling evidence id, an
  unresolved relation endpoint, a duplicate object id, a rejected review, or an analysis that is still
  collection-only is an error, not a warning.

What it deliberately does **not** do:

* no writing back to the analysis record, and no mutation of the input at all;
* no relation inferred from co-occurrence, similarity, frequency or clustering. Only relations and
  equivalence/difference chains that the analysis stated explicitly are imported. THEORY.md says
  frequency and semantic similarity establish nothing on their own, so a co-occurrence table cannot
  become an articulation here;
* **no actors**. An analysis label may denote a real person; instantiating one as a simulated agent is
  forbidden by #1286 §the scientific boundary, and choosing synthetic stand-ins is a scenario decision
  (work package 4), so this adapter emits discourse material only;
* no import of the analysis engine. The canonical record is validated structurally against the
  documented contract; a caller who has ``laclaugpt_data_analysis`` installed may validate the record
  with its own models before handing it over.

Run it:

    python -m social_sim.ai26 --canonical record.json            # the imported bundle as JSON
    python -m social_sim.ai26 --canonical record.json --summary  # counts, for a human
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .kernel import KernelError, Origin, Provenance

__all__ = [
    "ADAPTER_VERSION",
    "ARTICULATION_FAMILIES",
    "CLAIM_FAMILIES",
    "SCHEMA_VERSION",
    "AI26Import",
    "AdapterError",
    "ImportedArticulation",
    "ImportedClaim",
    "ImportedEvidence",
    "read_canonical_record",
]

#: The only canonical schema this adapter reads. Anything else is refused by name, never guessed at.
SCHEMA_VERSION = "1.2.0"

ADAPTER_VERSION = 1

#: `AnalysisSection` fields that hold `DiscourseObject` rows. Each is a family of claims.
CLAIM_FAMILIES = (
    "signifiers",
    "nodal_points",
    "formations",
    "discourses",
    "imaginaries",
    "us",
    "them",
    "frontier",
    "themes",
    "floating_signifiers",
    "empty_signifier_candidates",
    "affects",
    "sentiments",
    "stances",
)

#: Fields holding **explicit** relations. `equivalence_chains` / `difference_chains` carry
#: `member_refs`; the rest carry `source_ref` / `target_ref`.
ARTICULATION_FAMILIES = ("relations", "equivalence_chains", "difference_chains", "antagonisms")

#: A record in one of these states is not simulation input. The status is otherwise carried, not
#: enforced: #1286 leaves "may an unreviewed statement enter a scenario" to the researcher.
REJECTING_REVIEW_STATES = frozenset({"REJECTED", "SUPERSEDED"})

#: Present in a rich AI26 record and deliberately not imported here. `actor_entity_relations`
#: names entities, not discourse objects, and turning an entity into an actor is the scenario's job.
NOT_IMPORTED = ("entities", "entity_mentions", "actor_entity_relations", "formula_of_populism")


class AdapterError(KernelError):
    """The record cannot be represented without inventing, coercing or losing evidence."""


# --------------------------------------------------------------------------- #
# Imported material
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class ImportedEvidence:
    """One span of the observed text that the analysis cited. `observed`: it is taken as it stands."""

    evidence_id: str
    kind: str
    source_url: str
    provenance_id: str
    quote: str = ""
    ref: str = ""
    start_offset: int | None = None
    end_offset: int | None = None
    provenance: Provenance = field(
        default_factory=lambda: Provenance(Origin.OBSERVED, method="canonical_evidence")
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "kind": self.kind,
            "source_url": self.source_url,
            "provenance_id": self.provenance_id,
            "quote": self.quote,
            "ref": self.ref,
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> ImportedEvidence:
        return cls(
            evidence_id=str(payload["evidence_id"]),
            kind=str(payload.get("kind") or ""),
            source_url=str(payload.get("source_url") or ""),
            provenance_id=str(payload.get("provenance_id") or ""),
            quote=str(payload.get("quote") or ""),
            ref=str(payload.get("ref") or ""),
            start_offset=_optional_int(payload.get("start_offset")),
            end_offset=_optional_int(payload.get("end_offset")),
            provenance=Provenance.from_dict(dict(payload.get("provenance") or {})),
        )


@dataclass(frozen=True, slots=True)
class ImportedClaim:
    """One coded discourse object. `inferred`: it is the analysis' reading of observed text."""

    claim_id: str
    native_id: str
    family: str
    label: str
    kind: str
    evidence_ids: tuple[str, ...] = ()
    provenance: Provenance = field(
        default_factory=lambda: Provenance(Origin.INFERRED, method="canonical_analysis")
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "native_id": self.native_id,
            "family": self.family,
            "label": self.label,
            "kind": self.kind,
            "evidence_ids": list(self.evidence_ids),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> ImportedClaim:
        return cls(
            claim_id=str(payload["claim_id"]),
            native_id=str(payload.get("native_id") or ""),
            family=str(payload.get("family") or ""),
            label=str(payload.get("label") or ""),
            kind=str(payload.get("kind") or ""),
            evidence_ids=tuple(str(item) for item in payload.get("evidence_ids") or ()),
            provenance=Provenance.from_dict(dict(payload.get("provenance") or {})),
        )


@dataclass(frozen=True, slots=True)
class ImportedArticulation:
    """An articulation the analysis stated explicitly. `inferred`, never an equivalence claim."""

    articulation_id: str
    native_id: str
    family: str
    kind: str
    members: tuple[str, ...]
    evidence_ids: tuple[str, ...] = ()
    provenance: Provenance = field(
        default_factory=lambda: Provenance(Origin.INFERRED, method="canonical_relation")
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "articulation_id": self.articulation_id,
            "native_id": self.native_id,
            "family": self.family,
            "kind": self.kind,
            "members": list(self.members),
            "evidence_ids": list(self.evidence_ids),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> ImportedArticulation:
        return cls(
            articulation_id=str(payload["articulation_id"]),
            native_id=str(payload.get("native_id") or ""),
            family=str(payload.get("family") or ""),
            kind=str(payload.get("kind") or ""),
            members=tuple(str(item) for item in payload.get("members") or ()),
            evidence_ids=tuple(str(item) for item in payload.get("evidence_ids") or ()),
            provenance=Provenance.from_dict(dict(payload.get("provenance") or {})),
        )


@dataclass(frozen=True, slots=True)
class AI26Import:
    """A validated, read-only projection of one canonical record: the simulator's empirical input."""

    source_url: str
    schema_version: str
    input_sha256: str
    analysis_status: str
    review_status: str
    claims: tuple[ImportedClaim, ...] = ()
    articulations: tuple[ImportedArticulation, ...] = ()
    evidence: tuple[ImportedEvidence, ...] = ()
    uncertainty: tuple[str, ...] = ()
    abstentions: tuple[str, ...] = ()
    reviewer: str = ""
    reviewed_at: str = ""
    review_flags: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    adapter_version: int = ADAPTER_VERSION

    @property
    def record_id(self) -> str:
        """A stable id for the imported record: the content hash, not a counter."""
        return f"ai26:{self.input_sha256[:16]}"

    def claim_ids(self) -> tuple[str, ...]:
        return tuple(claim.claim_id for claim in self.claims)

    def digest(self) -> str:
        """A stable hash of the projection, so two imports of one record are comparable."""
        blob = json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_version": self.adapter_version,
            "record_id": self.record_id,
            "source_url": self.source_url,
            "schema_version": self.schema_version,
            "input_sha256": self.input_sha256,
            "analysis_status": self.analysis_status,
            "review": {
                "status": self.review_status,
                "reviewer": self.reviewer,
                "reviewed_at": self.reviewed_at,
                "flags": list(self.review_flags),
            },
            "claims": [claim.to_dict() for claim in self.claims],
            "articulations": [articulation.to_dict() for articulation in self.articulations],
            "evidence": [span.to_dict() for span in self.evidence],
            "uncertainty": list(self.uncertainty),
            "abstentions": list(self.abstentions),
            "warnings": list(self.warnings),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> AI26Import:
        """Rebuild a projection from its export. Provenance, uncertainty and review survive."""
        review = _mapping(payload.get("review"))
        return cls(
            source_url=str(payload.get("source_url") or ""),
            schema_version=str(payload.get("schema_version") or ""),
            input_sha256=str(payload.get("input_sha256") or ""),
            analysis_status=str(payload.get("analysis_status") or ""),
            review_status=str(review.get("status") or ""),
            claims=tuple(ImportedClaim.from_dict(raw) for raw in payload.get("claims") or ()),
            articulations=tuple(
                ImportedArticulation.from_dict(raw) for raw in payload.get("articulations") or ()
            ),
            evidence=tuple(ImportedEvidence.from_dict(raw) for raw in payload.get("evidence") or ()),
            uncertainty=tuple(str(item) for item in payload.get("uncertainty") or ()),
            abstentions=tuple(str(item) for item in payload.get("abstentions") or ()),
            reviewer=str(review.get("reviewer") or ""),
            reviewed_at=str(review.get("reviewed_at") or ""),
            review_flags=tuple(str(item) for item in review.get("flags") or ()),
            warnings=tuple(str(item) for item in payload.get("warnings") or ()),
            adapter_version=int(payload.get("adapter_version") or ADAPTER_VERSION),
        )

    def summary(self) -> str:
        return (
            f"{self.record_id} {self.source_url}\n"
            f"  analysis {self.analysis_status}; review {self.review_status}"
            f"{f' by {self.reviewer} at {self.reviewed_at}' if self.reviewer else ''}\n"
            f"  {len(self.claims)} claims, {len(self.articulations)} explicit articulations, "
            f"{len(self.evidence)} evidence spans\n"
            f"  uncertainty {len(self.uncertainty)}; abstentions {len(self.abstentions)}; "
            f"warnings {len(self.warnings)}\n"
            f"  digest {self.digest()}"
        )


# --------------------------------------------------------------------------- #
# Small readers with explicit failure
# --------------------------------------------------------------------------- #

def _mapping(value: object) -> Mapping[str, Any]:
    """A mapping or nothing: a missing or wrong-shaped section is an empty one, never a guess."""
    return value if isinstance(value, Mapping) else {}


def _optional_int(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(str(value))
    except ValueError as exc:
        raise AdapterError(f"expected an integer offset, got {value!r}") from exc


def _text(payload: Mapping[str, Any], key: str, where: str) -> str:
    value = payload.get(key)
    text = str(value).strip() if value is not None else ""
    if not text:
        raise AdapterError(f"{where}: {key} must be non-empty")
    return text


def _rows(analysis: Mapping[str, Any], family: str) -> list[Mapping[str, Any]]:
    """The rows of one analysis family, refusing a shape the contract does not allow."""
    raw = analysis.get(family)
    if raw is None:
        return []
    if isinstance(raw, (Mapping, str)):
        raise AdapterError(
            f"analysis.{family} must be a list of objects, got {type(raw).__name__}"
        )
    if not isinstance(raw, Sequence):
        raise AdapterError(f"analysis.{family} must be a list, got {type(raw).__name__}")
    rows: list[Mapping[str, Any]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise AdapterError(f"analysis.{family}[{index}] must be an object")
        rows.append(item)
    return rows


def _index(rows: Sequence[Mapping[str, Any]], key: str, where: str) -> dict[str, Mapping[str, Any]]:
    """Index rows by a required id, refusing a duplicate rather than letting one win."""
    indexed: dict[str, Mapping[str, Any]] = {}
    for position, row in enumerate(rows):
        identifier = _text(row, key, f"{where}[{position}]")
        if identifier in indexed:
            raise AdapterError(f"{where}: ambiguous {key} {identifier!r}")
        indexed[identifier] = row
    return indexed


def _provenance_table(record: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """Every imported value must resolve its provenance, including an identifier and a timestamp."""
    rows = record.get("provenance") or []
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        raise AdapterError("provenance must be a list")
    table: dict[str, Mapping[str, Any]] = {}
    for position, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise AdapterError(f"provenance[{position}] must be an object")
        identifier = _text(row, "provenance_id", f"provenance[{position}]")
        _text(row, "created_at", f"provenance[{identifier}]")
        if identifier in table:
            raise AdapterError(f"provenance: ambiguous provenance_id {identifier!r}")
        table[identifier] = row
    return table


def _provenance(
    origin: Origin,
    *,
    row: Mapping[str, Any],
    table: Mapping[str, Mapping[str, Any]],
    source_url: str,
    uncertainty: str,
    review_status: str,
    where: str,
) -> Provenance:
    identifier = str(row.get("provenance_id") or "").strip()
    if not identifier:
        raise AdapterError(f"{where}: no provenance_id, so the interpretation cannot be traced")
    if identifier not in table:
        raise AdapterError(f"{where}: unresolved provenance_id {identifier!r}")
    entry = table[identifier]
    method = str(entry.get("method") or "").strip() or "unspecified_method"
    model = str(entry.get("model") or "").strip()
    version = str(entry.get("model_version") or "").strip()
    if model:
        method = f"{method} [{model}{f' {version}' if version else ''}]"
    return Provenance(
        origin,
        source=source_url,
        method=method,
        uncertainty=uncertainty,
        review_status=review_status,
    )


def _review_status(row: Mapping[str, Any], default: str, where: str) -> str:
    status = str(row.get("review_status") or default or "").strip()
    if status.upper() in REJECTING_REVIEW_STATES:
        raise AdapterError(f"{where}: review_status {status!r} is a rejection, not simulation input")
    return status


def _evidence_ids(row: Mapping[str, Any], where: str) -> tuple[str, ...]:
    raw = row.get("evidence_ids")
    if not raw:
        raise AdapterError(f"{where}: no evidence, so the claim is unsupported")
    if isinstance(raw, (str, bytes)) or not isinstance(raw, Sequence):
        raise AdapterError(f"{where}: evidence_ids must be a list")
    identifiers = tuple(str(item).strip() for item in raw)
    if not all(identifiers):
        raise AdapterError(f"{where}: empty evidence id")
    return identifiers


def _resolve_evidence(
    identifiers: Sequence[str],
    evidence: Mapping[str, Mapping[str, Any]],
    where: str,
) -> None:
    for identifier in identifiers:
        if identifier not in evidence:
            raise AdapterError(f"{where}: unresolved evidence id {identifier!r}")


# --------------------------------------------------------------------------- #
# The adapter
# --------------------------------------------------------------------------- #

def read_canonical_record(source: Mapping[str, Any] | str | Path) -> AI26Import:
    """Validate one canonical AI26 record and project it into simulator input.

    ``source`` is a parsed record, a filesystem path or a JSON string of one. The input is never
    mutated. Anything this function cannot carry with its provenance and evidence intact raises
    :class:`AdapterError` — a partial or coerced import would be worse than none.
    """
    raw_bytes, record = _load(source)

    schema_version = str(record.get("schema_version") or "").strip()
    if schema_version != SCHEMA_VERSION:
        raise AdapterError(
            f"unsupported canonical schema_version {schema_version or '<missing>'!r}; "
            f"this adapter reads exactly {SCHEMA_VERSION}"
        )

    source_url = str(record.get("source_url") or "").strip()
    if not source_url:
        raise AdapterError("source_url is the canonical source identity and may not be empty")

    provenance_table = _provenance_table(record)

    review = _mapping(record.get("review"))
    review_status = str(review.get("status") or "").strip() or "PROVISIONAL"
    if review_status.upper() in REJECTING_REVIEW_STATES:
        raise AdapterError(
            f"review.status {review_status!r}: a rejected or superseded record is not simulation input"
        )
    reviewer = str(review.get("reviewer") or "").strip()
    reviewed_at = str(review.get("reviewed_at") or "").strip()
    review_flags = tuple(str(flag) for flag in review.get("flags") or () if str(flag).strip())

    analysis = record.get("analysis")
    if not isinstance(analysis, Mapping):
        raise AdapterError("analysis must be an object; a collection-only record has none")
    analysis_status = str(analysis.get("status") or "collection-only").strip()
    if analysis_status == "collection-only":
        raise AdapterError(
            "analysis.status is 'collection-only'; there is no coded discourse to import"
        )

    uncertainty = tuple(
        str(item).strip() for item in analysis.get("uncertainty") or () if str(item).strip()
    )
    abstentions = tuple(
        str(item).strip() for item in analysis.get("abstentions") or () if str(item).strip()
    )
    default_uncertainty = "; ".join(uncertainty)

    # -- evidence: the only `observed` material in this projection ---------------------------------- #
    evidence_rows = record.get("evidence") or []
    if not isinstance(evidence_rows, Sequence) or isinstance(evidence_rows, (str, bytes)):
        raise AdapterError("evidence must be a list")
    evidence_table = _index(
        [row for row in evidence_rows if isinstance(row, Mapping)], "evidence_id", "evidence"
    )
    warnings: list[str] = []
    evidence: list[ImportedEvidence] = []
    for evidence_id, row in sorted(evidence_table.items()):
        where = f"evidence[{evidence_id}]"
        span_source = str(row.get("source_url") or "").strip()
        if span_source != source_url:
            raise AdapterError(
                f"{where}: source_url {span_source!r} is not this record's source {source_url!r}"
            )
        if not (str(row.get("quote") or "").strip() or str(row.get("ref") or "").strip()):
            raise AdapterError(f"{where}: neither quote nor ref, so there is no evidence")
        evidence.append(
            ImportedEvidence(
                evidence_id=evidence_id,
                kind=str(row.get("kind") or "").strip() or "span",
                source_url=span_source,
                provenance_id=str(row.get("provenance_id") or "").strip(),
                quote=str(row.get("quote") or ""),
                ref=str(row.get("ref") or ""),
                start_offset=_optional_int(row.get("start_offset")),
                end_offset=_optional_int(row.get("end_offset")),
                provenance=_provenance(
                    Origin.OBSERVED,
                    row=row,
                    table=provenance_table,
                    source_url=source_url,
                    uncertainty=default_uncertainty,
                    review_status=review_status,
                    where=where,
                ),
            )
        )

    # -- claims: coded discourse objects, all `inferred` ------------------------------------------- #
    claims: list[ImportedClaim] = []
    seen_claim_ids: set[str] = set()
    for family in CLAIM_FAMILIES:
        for position, row in enumerate(_rows(analysis, family)):
            where = f"analysis.{family}[{position}]"
            object_id = _text(row, "object_id", where)
            claim_id = f"claim:{family}:{object_id}"
            if claim_id in seen_claim_ids:
                raise AdapterError(f"{where}: duplicate object_id {object_id!r} in {family}")
            seen_claim_ids.add(claim_id)
            identifiers = _evidence_ids(row, where)
            _resolve_evidence(identifiers, evidence_table, where)
            item_uncertainty = str(row.get("uncertainty") or "").strip() or default_uncertainty
            claims.append(
                ImportedClaim(
                    claim_id=claim_id,
                    native_id=object_id,
                    family=family,
                    label=_text(row, "label", where),
                    kind=str(row.get("kind") or family).strip() or family,
                    evidence_ids=identifiers,
                    provenance=_provenance(
                        Origin.INFERRED,
                        row=row,
                        table=provenance_table,
                        source_url=source_url,
                        uncertainty=item_uncertainty,
                        review_status=_review_status(row, review_status, where),
                        where=where,
                    ),
                )
            )

    # -- articulations: only what the analysis stated explicitly ----------------------------------- #
    articulations: list[ImportedArticulation] = []
    for family in ARTICULATION_FAMILIES:
        rows = _rows(analysis, family)
        for position, row in enumerate(rows):
            where = f"analysis.{family}[{position}]"
            native_id = _text(row, "relation_id" if "relation_id" in row else "chain_id", where)
            if family.endswith("_chains"):
                members = tuple(
                    str(item).strip() for item in row.get("member_refs") or () if str(item).strip()
                )
                kind = str(row.get("chain_type") or family.replace("_chains", "")).strip()
            else:
                members = tuple(
                    str(row.get(key) or "").strip()
                    for key in ("source_ref", "target_ref")
                )
                kind = _text(row, "relation_type", where)
            if len(members) < 2 or not all(members):
                raise AdapterError(f"{where}: an articulation needs at least two endpoints")
            for member in members:
                if not _member_resolves(member, seen_claim_ids, claims):
                    raise AdapterError(
                        f"{where}: unsupported discourse endpoint {member!r}; import refuses to "
                        "coerce a reference it cannot place"
                    )
            identifiers = _evidence_ids(row, where)
            _resolve_evidence(identifiers, evidence_table, where)
            articulations.append(
                ImportedArticulation(
                    articulation_id=f"art:{family}:{native_id}",
                    native_id=native_id,
                    family=family,
                    kind=kind,
                    members=members,
                    evidence_ids=identifiers,
                    provenance=_provenance(
                        Origin.INFERRED,
                        row=row,
                        table=provenance_table,
                        source_url=source_url,
                        uncertainty=default_uncertainty,
                        review_status=_review_status(row, review_status, where),
                        where=where,
                    ),
                )
            )

    if not claims:
        raise AdapterError(
            "the record codes no discourse object this adapter can place; nothing to import"
        )
    if not articulations:
        warnings.append(
            "no explicit equivalence, difference or relation rows: the import carries claims only. "
            "Co-occurrence is not an articulation, so none is invented."
        )
    for family in NOT_IMPORTED:
        if analysis.get(family):
            warnings.append(
                f"analysis.{family} is not imported: naming an actor is a scenario decision, and no "
                "real person may be instantiated as a simulated agent"
            )
    if abstentions:
        warnings.append(
            f"{len(abstentions)} abstention(s) preserved as abstentions; none was rescaled into a claim"
        )
    if reviewer and reviewed_at:
        warnings.append(f"human review recorded: {review_status} by {reviewer} at {reviewed_at}")
    elif review_status.upper() in {"ACCEPTED", "CANONICAL"}:
        warnings.append(
            f"review.status is {review_status} but no reviewer or reviewed_at is recorded; "
            "the claim of review cannot be checked"
        )

    return AI26Import(
        source_url=source_url,
        schema_version=schema_version,
        input_sha256=hashlib.sha256(raw_bytes).hexdigest(),
        analysis_status=analysis_status,
        review_status=review_status,
        claims=tuple(claims),
        articulations=tuple(articulations),
        evidence=tuple(evidence),
        uncertainty=uncertainty,
        abstentions=abstentions,
        reviewer=reviewer,
        reviewed_at=reviewed_at,
        review_flags=review_flags,
        warnings=tuple(warnings),
    )


def _member_resolves(member: str, claim_ids: set[str], claims: Sequence[ImportedClaim]) -> bool:
    """A relation endpoint resolves when it names an imported claim, by native id or by claim id."""
    if member in claim_ids:
        return True
    return any(claim.native_id == member for claim in claims)


def _load(source: Mapping[str, Any] | str | Path) -> tuple[bytes, Mapping[str, Any]]:
    """Read a record from a parsed mapping, a path or a JSON string. Returns the exact input bytes."""
    if isinstance(source, Mapping):
        blob = json.dumps(source, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return blob, source
    if isinstance(source, Path):
        raw = source.read_bytes()
    else:
        text = str(source)
        candidate = Path(text)
        try:
            is_file = candidate.is_file()
        except OSError:
            is_file = False
        if is_file:
            raw = candidate.read_bytes()
        else:
            raw = text.encode("utf-8")
    try:
        record = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AdapterError(f"not JSON: {exc}") from exc
    if not isinstance(record, Mapping):
        raise AdapterError("a canonical record must be a JSON object")
    return raw, record


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m social_sim.ai26",
        description="Validate one LaclauGPT AI26 canonical record read-only and print the "
                    "simulator's imported discourse bundle.",
    )
    parser.add_argument("--canonical", required=True, help="path to a canonical 1.2.0 JSON record")
    parser.add_argument(
        "--summary", action="store_true", help="print a human-readable summary instead of JSON"
    )
    arguments = parser.parse_args(argv)
    try:
        imported = read_canonical_record(Path(arguments.canonical))
    except AdapterError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    if arguments.summary:
        print(imported.summary())
        return 0
    print(json.dumps(imported.to_dict(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised through the tests as a subprocess
    raise SystemExit(main())
