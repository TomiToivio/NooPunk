"""Read reviewed, evidence-linked relations between canonical discourse objects."""
import hashlib
import json
from pathlib import Path

OBJECT_GROUPS = (
    "signifiers", "themes", "formations", "discourses", "imaginaries", "us", "them",
    "frontier", "nodal_points", "floating_signifiers", "empty_signifier_candidates",
)
APPROVED = {"ACCEPTED", "CANONICAL"}


def indexed(rows, field):
    result = {}
    for row in rows:
        key = getattr(row, field)
        if not key.strip() or key in result:
            raise ValueError(f"Missing or ambiguous {field}: {key!r}")
        result[key] = row
    return result


def read_relations(path):
    from laclaugpt_data_analysis.canonical import CanonicalRecord

    data = Path(path).read_bytes()
    raw = json.loads(data)
    if raw.get("schema_version") != "1.2.0":
        raise ValueError("Expected an explicit canonical 1.2.0 export")
    for item in raw.get("provenance", []):
        if not item.get("provenance_id") or not item.get("created_at"):
            raise ValueError("Supply original provenance identifiers and timestamps")
    record = CanonicalRecord.model_validate(raw)
    review = record.review
    if review.status not in APPROVED or not (review.reviewer or "").strip() or not review.reviewed_at:
        raise ValueError("A dated human approval is required")
    analysis = record.analysis
    if analysis.abstentions or not analysis.relations:
        raise ValueError("Record abstains or lacks explicit relations")
    objects = indexed((obj for group in OBJECT_GROUPS for obj in getattr(analysis, group)), "object_id")
    evidence = indexed(record.evidence, "evidence_id")
    provenance = indexed(record.provenance, "provenance_id")
    relations = indexed(analysis.relations, "relation_id")
    for relation in relations.values():
        if not relation.relation_type.strip():
            raise ValueError("Missing relation type")
        for endpoint in (relation.source_ref, relation.target_ref):
            if endpoint not in objects:
                raise ValueError(f"Unsupported discourse endpoint: {endpoint}")
        for item in (relation, objects[relation.source_ref], objects[relation.target_ref]):
            if item.review_status not in APPROVED or item.provenance_id not in provenance or not item.evidence_ids:
                raise ValueError("Interpretation lacks approval, provenance or evidence")
            for key in item.evidence_ids:
                span = evidence.get(key)
                if (span is None or span.source_url != record.source_url
                        or span.provenance_id not in provenance or not (span.quote or span.ref)):
                    raise ValueError(f"Unresolved source evidence: {key}")
    return {
        "origin": "inferred", "source_url": record.source_url,
        "input_sha256": hashlib.sha256(data).hexdigest(),
        "review": review.model_dump(mode="json"), "uncertainty": analysis.uncertainty,
        "relations": [r.model_dump() for r in relations.values()],
        "objects": {k: o.model_dump() for k, o in objects.items()},
        "evidence": {k: e.model_dump() for k, e in evidence.items()},
        "provenance": {k: p.model_dump(mode="json") for k, p in provenance.items()},
    }
