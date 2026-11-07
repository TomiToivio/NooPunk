"""#1286 work package 2: the read-only AI26 adapter, tested against the issue's conditions.

Three things are adversarial here, because they are the three ways this adapter could quietly do the
wrong thing:

* **coercion** — a record that lacks provenance, evidence, a resolvable endpoint or a real source
  identity must be refused by name, not repaired;
* **invention** — co-occurrence is not an articulation, abstentions are not weak signals, and no
  relation may appear in the import that the analysis did not state;
* **laundering** — evidence is `observed` text, analysis is `inferred`, and neither may drift.

Every fixture is synthetic and built inside this file. No AI26 corpus data, no real person and no RPG
record is read or written.

Run:
    python -m unittest discover -s tests -p "test_social_sim_ai26_1286.py"
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from social_sim.ai26 import (
    AdapterError,
    AI26Import,
    ImportedArticulation,
    ImportedClaim,
    read_canonical_record,
)
from social_sim.kernel import Origin

SOURCE = "https://fixture.invalid/ai26/statement-1"


def canonical() -> dict:
    """A minimal, valid canonical 1.2.0 record: three coded objects, two explicit chains, one relation."""
    return {
        "schema_version": "1.2.0",
        "source_url": SOURCE,
        "provenance": [
            {
                "provenance_id": "prov-1",
                "method": "laclaugpt-data-analysis/analysis",
                "model": "fixture-model",
                "model_version": "0.0.1",
                "pipeline_version": "fixture",
                "created_at": "2026-11-07T00:00:00Z",
                "metadata": {"stage": "analysis"},
            }
        ],
        "evidence": [
            {
                "evidence_id": "ev-1",
                "kind": "quote",
                "source_url": SOURCE,
                "quote": "public control of the model",
                "start_offset": 0,
                "end_offset": 26,
                "provenance_id": "prov-1",
            },
            {
                "evidence_id": "ev-2",
                "kind": "quote",
                "source_url": SOURCE,
                "quote": "a commons, not a market",
                "start_offset": 27,
                "end_offset": 51,
                "provenance_id": "prov-1",
            },
        ],
        "analysis": {
            "status": "analyzed",
            "signifiers": [
                {
                    "object_id": "obj-ai-public",
                    "label": "public AI control",
                    "kind": "signifier",
                    "description": "fixture",
                    "evidence_ids": ["ev-1"],
                    "confidence": 0.6,
                    "uncertainty": "one coded statement",
                    "provenance_id": "prov-1",
                    "review_status": "ACCEPTED",
                },
                {
                    "object_id": "obj-ai-commons",
                    "label": "AI as commons",
                    "kind": "signifier",
                    "evidence_ids": ["ev-2"],
                    "provenance_id": "prov-1",
                    "review_status": "ACCEPTED",
                },
            ],
            "frontier": [
                {
                    "object_id": "obj-market-frontier",
                    "label": "market frontier",
                    "kind": "frontier",
                    "evidence_ids": ["ev-2"],
                    "provenance_id": "prov-1",
                    "review_status": "ACCEPTED",
                }
            ],
            "equivalence_chains": [
                {
                    "chain_id": "chain-1",
                    "chain_type": "equivalence",
                    "member_refs": ["obj-ai-public", "obj-ai-commons"],
                    "evidence_ids": ["ev-2"],
                    "provenance_id": "prov-1",
                    "review_status": "ACCEPTED",
                }
            ],
            "difference_chains": [
                {
                    "chain_id": "chain-2",
                    "chain_type": "difference",
                    "member_refs": ["obj-ai-commons", "obj-market-frontier"],
                    "evidence_ids": ["ev-2"],
                    "provenance_id": "prov-1",
                    "review_status": "ACCEPTED",
                }
            ],
            "relations": [
                {
                    "relation_id": "rel-1",
                    "relation_type": "antagonism",
                    "source_ref": "obj-ai-public",
                    "target_ref": "obj-market-frontier",
                    "evidence_ids": ["ev-1"],
                    "provenance_id": "prov-1",
                    "review_status": "ACCEPTED",
                }
            ],
            "uncertainty": ["the codes are interpretations of one text"],
            "abstentions": ["statement-9: stance abstained"],
        },
        "review": {
            "status": "ACCEPTED",
            "reviewer": "fixture-reviewer",
            "reviewed_at": "2026-11-07T01:00:00Z",
            "flags": ["fixture"],
        },
    }


class ImportTests(unittest.TestCase):
    def test_a_valid_record_imports_claims_and_explicit_articulations(self):
        imported = read_canonical_record(canonical())
        self.assertEqual(imported.source_url, SOURCE)
        self.assertEqual(imported.schema_version, "1.2.0")
        self.assertEqual(len(imported.claims), 3)
        self.assertEqual(
            sorted(claim.claim_id for claim in imported.claims),
            ["claim:frontier:obj-market-frontier", "claim:signifiers:obj-ai-commons",
             "claim:signifiers:obj-ai-public"],
        )
        self.assertEqual(len(imported.articulations), 3)
        self.assertEqual(
            sorted(articulation.kind for articulation in imported.articulations),
            ["antagonism", "difference", "equivalence"],
        )
        self.assertEqual([span.evidence_id for span in imported.evidence], ["ev-1", "ev-2"])

    def test_evidence_is_observed_and_analysis_is_inferred(self):
        imported = read_canonical_record(canonical())
        for span in imported.evidence:
            self.assertIs(span.provenance.origin, Origin.OBSERVED)
        for item in tuple(imported.claims) + tuple(imported.articulations):
            self.assertIs(item.provenance.origin, Origin.INFERRED,
                          f"{item} must not pass an interpretation off as an observation")

    def test_provenance_keeps_the_method_model_and_item_uncertainty(self):
        imported = read_canonical_record(canonical())
        claim = next(item for item in imported.claims if item.native_id == "obj-ai-public")
        self.assertEqual(claim.provenance.source, SOURCE)
        self.assertIn("laclaugpt-data-analysis/analysis", claim.provenance.method)
        self.assertIn("fixture-model", claim.provenance.method)
        self.assertEqual(claim.provenance.uncertainty, "one coded statement")
        self.assertEqual(claim.provenance.review_status, "ACCEPTED")
        commons = next(item for item in imported.claims if item.native_id == "obj-ai-commons")
        self.assertEqual(commons.provenance.uncertainty,
                         "the codes are interpretations of one text",
                         "an object without its own uncertainty inherits the record's, verbatim")

    def test_review_state_is_carried_and_dated(self):
        imported = read_canonical_record(canonical())
        self.assertEqual(imported.review_status, "ACCEPTED")
        self.assertEqual(imported.reviewer, "fixture-reviewer")
        self.assertEqual(imported.reviewed_at, "2026-11-07T01:00:00Z")
        self.assertEqual(imported.review_flags, ("fixture",))

    def test_abstentions_and_uncertainty_are_preserved_not_rescaled(self):
        imported = read_canonical_record(canonical())
        self.assertEqual(imported.abstentions, ("statement-9: stance abstained",))
        self.assertEqual(imported.uncertainty, ("the codes are interpretations of one text",))
        self.assertTrue(any("abstention" in warning for warning in imported.warnings))

    def test_the_export_round_trips_provenance_uncertainty_and_review(self):
        imported = read_canonical_record(canonical())
        exported = json.loads(json.dumps(imported.to_dict()))
        restored = AI26Import.from_dict(exported)
        self.assertEqual(restored.digest(), imported.digest())
        self.assertEqual(restored.claims, imported.claims)
        self.assertEqual(restored.articulations, imported.articulations)
        self.assertEqual(restored.evidence, imported.evidence)
        self.assertEqual(restored.review_status, "ACCEPTED")
        self.assertEqual(restored.abstentions, imported.abstentions)
        for claim in restored.claims:
            self.assertIs(claim.provenance.origin, Origin.INFERRED)

    def test_the_digest_is_stable_for_the_same_record(self):
        first, second = read_canonical_record(canonical()), read_canonical_record(canonical())
        self.assertEqual(first.digest(), second.digest())
        self.assertEqual(first.record_id, second.record_id)
        self.assertEqual(first.claim_ids(), second.claim_ids())

    def test_importing_does_not_mutate_the_input_record(self):
        record = canonical()
        before = copy.deepcopy(record)
        read_canonical_record(record)
        self.assertEqual(record, before, "the adapter is read-only: it may not rewrite the analysis")

    def test_a_path_and_a_mapping_import_the_same_material(self):
        record = canonical()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            raw = path.read_bytes()
            from_path = read_canonical_record(path)
        from_mapping = read_canonical_record(record)
        self.assertEqual(from_path.claims, from_mapping.claims)
        self.assertEqual(from_path.articulations, from_mapping.articulations)
        self.assertEqual(from_path.input_sha256, hashlib.sha256(raw).hexdigest())

    def test_an_accepted_review_without_a_reviewer_is_flagged(self):
        record = canonical()
        record["review"] = {"status": "ACCEPTED"}
        imported = read_canonical_record(record)
        self.assertTrue(any("reviewer" in warning for warning in imported.warnings))


class RefusalTests(unittest.TestCase):
    def assert_refused(self, record, fragment: str):
        with self.assertRaises(AdapterError) as context:
            read_canonical_record(record)
        self.assertIn(fragment, str(context.exception))

    def test_an_unsupported_schema_version_is_refused_by_name(self):
        record = canonical()
        record["schema_version"] = "1.1.0"
        self.assert_refused(record, "1.2.0")

    def test_a_missing_schema_version_is_refused(self):
        record = canonical()
        del record["schema_version"]
        self.assert_refused(record, "1.2.0")

    def test_an_empty_source_identity_is_refused(self):
        record = canonical()
        record["source_url"] = "   "
        self.assert_refused(record, "source_url")

    def test_a_collection_only_record_is_refused(self):
        record = canonical()
        record["analysis"]["status"] = "collection-only"
        self.assert_refused(record, "collection-only")

    def test_a_record_without_an_analysis_section_is_refused(self):
        record = canonical()
        del record["analysis"]
        self.assert_refused(record, "analysis")

    def test_provenance_without_an_identifier_is_refused(self):
        record = canonical()
        record["provenance"][0]["provenance_id"] = ""
        self.assert_refused(record, "provenance_id")

    def test_provenance_without_a_timestamp_is_refused(self):
        record = canonical()
        del record["provenance"][0]["created_at"]
        self.assert_refused(record, "created_at")

    def test_an_unresolved_evidence_id_is_refused(self):
        record = canonical()
        record["analysis"]["signifiers"][0]["evidence_ids"] = ["ev-missing"]
        self.assert_refused(record, "ev-missing")

    def test_evidence_from_another_source_is_refused(self):
        record = canonical()
        record["evidence"][0]["source_url"] = "https://fixture.invalid/elsewhere"
        self.assert_refused(record, "fixture.invalid/elsewhere")

    def test_evidence_without_a_quote_or_a_reference_is_refused(self):
        record = canonical()
        record["evidence"][0]["quote"] = ""
        del record["evidence"][0]["start_offset"]
        self.assert_refused(record, "no evidence")

    def test_a_claim_without_evidence_is_refused(self):
        record = canonical()
        record["analysis"]["signifiers"][0]["evidence_ids"] = []
        self.assert_refused(record, "no evidence")

    def test_a_rejected_record_is_refused(self):
        record = canonical()
        record["review"]["status"] = "REJECTED"
        self.assert_refused(record, "REJECTED")

    def test_a_superseded_record_is_refused(self):
        record = canonical()
        record["review"]["status"] = "SUPERSEDED"
        self.assert_refused(record, "SUPERSEDED")

    def test_a_rejected_object_is_refused(self):
        record = canonical()
        record["analysis"]["signifiers"][1]["review_status"] = "REJECTED"
        self.assert_refused(record, "REJECTED")

    def test_a_duplicate_object_id_is_refused_as_ambiguous(self):
        record = canonical()
        record["analysis"]["signifiers"].append(copy.deepcopy(record["analysis"]["signifiers"][0]))
        self.assert_refused(record, "duplicate object_id")

    def test_a_relation_endpoint_the_adapter_cannot_place_is_refused(self):
        record = canonical()
        record["analysis"]["relations"][0]["target_ref"] = "entity-42"
        self.assert_refused(record, "entity-42")

    def test_a_chain_with_one_member_is_refused(self):
        record = canonical()
        record["analysis"]["equivalence_chains"][0]["member_refs"] = ["obj-ai-public"]
        self.assert_refused(record, "at least two endpoints")

    def test_a_relation_without_evidence_is_refused(self):
        record = canonical()
        record["analysis"]["relations"][0]["evidence_ids"] = []
        self.assert_refused(record, "no evidence")

    def test_an_unresolved_provenance_identifier_is_refused(self):
        record = canonical()
        record["analysis"]["frontier"][0]["provenance_id"] = "prov-missing"
        self.assert_refused(record, "prov-missing")

    def test_an_analysis_that_codes_nothing_is_refused(self):
        record = canonical()
        for family in ("signifiers", "frontier", "relations", "equivalence_chains",
                       "difference_chains"):
            record["analysis"][family] = []
        self.assert_refused(record, "nothing to import")

    def test_a_family_with_a_coerced_shape_is_refused(self):
        record = canonical()
        record["analysis"]["signifiers"] = "public AI control"
        self.assert_refused(record, "must be a list")

    def test_something_that_is_not_json_is_refused(self):
        with self.assertRaises(AdapterError):
            read_canonical_record("not json at all")


class NoInventionTests(unittest.TestCase):
    def test_co_occurrence_alone_produces_no_articulation(self):
        record = canonical()
        for family in ("equivalence_chains", "difference_chains", "relations"):
            record["analysis"][family] = []
        imported = read_canonical_record(record)
        self.assertEqual(imported.articulations, (),
                         "two claims in one record are not an articulation")
        self.assertTrue(any("Co-occurrence" in warning for warning in imported.warnings))

    def test_the_import_names_only_the_relations_the_analysis_stated(self):
        imported = read_canonical_record(canonical())
        self.assertEqual(
            sorted(articulation.native_id for articulation in imported.articulations),
            ["chain-1", "chain-2", "rel-1"],
        )
        for articulation in imported.articulations:
            self.assertTrue(articulation.evidence_ids, articulation.articulation_id)

    def test_actor_naming_is_not_imported_as_an_actor(self):
        record = canonical()
        record["analysis"]["actor_entity_relations"] = [
            {
                "relation_id": "actor-1",
                "relation_type": "speaks_for",
                "source_ref": "entity-42",
                "target_ref": "obj-ai-public",
                "evidence_ids": ["ev-1"],
                "provenance_id": "prov-1",
            }
        ]
        imported = read_canonical_record(record)
        self.assertTrue(any("scenario decision" in warning for warning in imported.warnings))
        self.assertFalse(hasattr(imported, "actors"))


class BoundaryTests(unittest.TestCase):
    def test_the_adapter_imports_no_rpg_module_and_no_provider(self):
        source = (ROOT / "src" / "social_sim" / "ai26.py").read_text(encoding="utf-8")
        for forbidden in ("from src.rules", "import rules", "from rules", "src.world", "from world",
                          "src.console", "src.simulation", "evennia", "godot", "openai",
                          "anthropic", "requests", "urllib.request", "httpx"):
            self.assertNotIn(forbidden, source, forbidden)

    def test_the_adapter_defines_no_actor_type(self):
        import social_sim.ai26 as adapter

        self.assertFalse(hasattr(adapter, "Actor"),
                         "instantiating an actor is a scenario decision, not the adapter's")

    def test_the_projected_material_is_immutable(self):
        imported = read_canonical_record(canonical())
        with self.assertRaises(dataclasses.FrozenInstanceError):
            imported.claims[0].label = "rewritten"  # type: ignore[misc]


class CliTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess:
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "social_sim.ai26", *arguments],
            cwd=ROOT, env=environment, capture_output=True, text=True, check=False,
        )

    def test_the_cli_prints_the_import_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text(json.dumps(canonical()), encoding="utf-8")
            completed = self.run_cli("--canonical", str(path))
            summary = self.run_cli("--canonical", str(path), "--summary")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        bundle = json.loads(completed.stdout)
        self.assertEqual(bundle["source_url"], SOURCE)
        self.assertEqual(len(bundle["claims"]), 3)
        self.assertTrue(bundle["claims"][0]["provenance"]["origin"] == "inferred")
        self.assertEqual(summary.returncode, 0, summary.stderr)
        self.assertIn("claims", summary.stdout)

    def test_the_cli_refuses_a_record_it_cannot_import(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            record = canonical()
            record["schema_version"] = "0.9.0"
            path.write_text(json.dumps(record), encoding="utf-8")
            completed = self.run_cli("--canonical", str(path))
        self.assertEqual(completed.returncode, 2)
        self.assertIn("refused", completed.stderr)


class TypedMaterialTests(unittest.TestCase):
    def test_the_imported_types_are_the_documented_ones(self):
        imported = read_canonical_record(canonical())
        self.assertTrue(all(isinstance(claim, ImportedClaim) for claim in imported.claims))
        self.assertTrue(all(isinstance(item, ImportedArticulation)
                            for item in imported.articulations))


if __name__ == "__main__":
    unittest.main()
