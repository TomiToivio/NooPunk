"""Acceptance tests for the standalone LaclauGPT social-science simulator (#1286)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.social_science import (
    Actor,
    AdapterError,
    AI26Adapter,
    Claim,
    Material,
    SimulationConfig,
    SocialScienceSimulation,
    build_synthetic_scenario,
    export_run,
    simulation_metrics,
    write_run,
)
from src.social_science.demo import main as demo_main
from src.social_science.engine import DEFAULT_RULES


def fixture_payload() -> dict:
    return {
        "schema_version": "1.2.0",
        "source_url": "fixture://ai26/synthetic-record-001",
        "analysis": {
            "status": "complete",
            "signifiers": ["shared future", "control"],
            "nodal_points": [{"label": "control", "confidence": 0.7}],
            "formations": [{"label": "synthetic formation", "confidence": 0.6}],
            "equivalence_chains": [{"member_refs": ["shared future", "control"]}],
            "difference_chains": [
                {"member_refs": ["shared future", "synthetic formation"]}
            ],
            "uncertainty": [
                {
                    "target_id": "shared future",
                    "kind": "model_confidence",
                    "value": 0.64,
                }
            ],
            "abstentions": ["no actor attribution"],
        },
        "review": {"status": "PROVISIONAL", "flags": ["synthetic-fixture"]},
    }


class DeterminismTests(unittest.TestCase):
    def test_same_seed_same_events_and_digest(self):
        first = build_synthetic_scenario(seed=11, turns=4)
        second = build_synthetic_scenario(seed=11, turns=4)
        first.run()
        second.run()
        self.assertEqual(
            [event.to_dict() for event in first.log.events],
            [event.to_dict() for event in second.log.events],
        )
        self.assertEqual(first.digest(), second.digest())

    def test_different_seed_changes_the_run(self):
        first = build_synthetic_scenario(seed=11, turns=4)
        second = build_synthetic_scenario(seed=12, turns=4)
        first.run()
        second.run()
        self.assertNotEqual(first.digest(), second.digest())

    def test_snapshot_restores_and_continues_identically(self):
        original = build_synthetic_scenario(seed=5, turns=6)
        original.run(2)
        restored = SocialScienceSimulation.from_snapshot(original.to_snapshot())
        self.assertEqual(original.digest(), restored.digest())
        original_events = [event.to_dict() for event in original.run(2)]
        restored_events = [event.to_dict() for event in restored.run(2)]
        self.assertEqual(original_events, restored_events)

    def test_event_ids_are_unique_and_time_is_monotonic(self):
        sim = build_synthetic_scenario(seed=3, turns=5)
        sim.run()
        ids = [event.event_id for event in sim.log.events]
        self.assertEqual(len(ids), len(set(ids)))
        times = [event.time for event in sim.log.events]
        self.assertEqual(times, sorted(times))


class StructureTests(unittest.TestCase):
    def test_edges_reference_known_actors_and_claims(self):
        sim = build_synthetic_scenario()
        for edge in sim.social_edges:
            self.assertIn(edge.source, sim.actors)
            self.assertIn(edge.target, sim.actors)
        for articulation in sim.articulations.values():
            self.assertIn(articulation.left, sim.claims)
            self.assertIn(articulation.right, sim.claims)

    def test_organizations_and_members_are_distinct(self):
        sim = build_synthetic_scenario()
        kinds = {actor.id: actor.kind for actor in sim.actors.values()}
        self.assertEqual(kinds["org.tenant"], "organization")
        self.assertEqual(kinds["actor.a"], "individual")
        self.assertNotEqual(kinds["org.tenant"], kinds["actor.a"])

    def test_isolated_actor_abstains_instead_of_inventing_contact(self):
        sim = SocialScienceSimulation(config=SimulationConfig(seed=1, turns=1))
        sim.add_claim(Claim("c1", "a demand"))
        sim.add_actor(Actor("a", "A"))
        sim.add_actor(Actor("b", "B"))
        sim.run()
        self.assertTrue(all(event.kind == "abstain" for event in sim.log.events))
        self.assertIn("no outgoing social tie", sim.log.events[0].payload["reason"])

    def test_empty_claims_abstain_without_crashing(self):
        sim = SocialScienceSimulation(config=SimulationConfig(seed=1, turns=1))
        sim.add_actor(Actor("a", "A"))
        sim.run()
        self.assertEqual(sim.log.events[0].kind, "abstain")
        self.assertIn("no claims", sim.log.events[0].payload["reason"])

    def test_explicit_rules_are_exported(self):
        self.assertIn("communication", DEFAULT_RULES)
        self.assertIn("influence", DEFAULT_RULES)
        self.assertIn("coalition", DEFAULT_RULES)


class AdapterTests(unittest.TestCase):
    def test_canonical_export_becomes_inferred_claims_and_articulations(self):
        adapter = AI26Adapter.from_dict(fixture_payload())
        self.assertEqual(
            adapter.export.source_url, "fixture://ai26/synthetic-record-001"
        )
        self.assertGreaterEqual(len(adapter.export.claims), 4)
        labels = {claim.label for claim in adapter.export.claims}
        self.assertIn("shared future", labels)
        self.assertIn("control", labels)
        self.assertTrue(
            all(
                claim.provenance.material is Material.INFERRED
                for claim in adapter.export.claims
            )
        )
        self.assertTrue(
            any(art.relation == "equivalence" for art in adapter.export.articulations)
        )
        self.assertTrue(
            any(art.relation == "difference" for art in adapter.export.articulations)
        )
        self.assertEqual(adapter.export.review_flags, ("synthetic-fixture",))
        self.assertEqual(adapter.export.abstentions, ("no actor attribution",))

    def test_adapter_rejects_collection_only_records(self):
        payload = fixture_payload()
        payload.pop("analysis")
        with self.assertRaises(AdapterError):
            AI26Adapter.from_dict(payload)

    def test_adapter_rejects_missing_source_identity(self):
        payload = fixture_payload()
        payload["source_url"] = "  "
        with self.assertRaises(AdapterError):
            AI26Adapter.from_dict(payload)

    def test_adapter_does_not_invent_cooccurrence_relations(self):
        payload = fixture_payload()
        payload["analysis"]["signifiers"] = ["shared future", "control"]
        payload["analysis"].pop("equivalence_chains")
        payload["analysis"].pop("difference_chains")
        adapter = AI26Adapter.from_dict(payload)
        self.assertEqual(adapter.export.articulations, ())

    def test_adapter_apply_is_read_only_and_idempotent(self):
        adapter = AI26Adapter.from_dict(fixture_payload())
        sim = build_synthetic_scenario()
        adapter.apply_to(sim)
        count = len(sim.claims)
        adapter.apply_to(sim)
        self.assertEqual(len(sim.claims), count)


class ExportTests(unittest.TestCase):
    def test_export_labels_observed_inferred_synthesized_simulated(self):
        sim = build_synthetic_scenario(seed=2, turns=3)
        sim.run()
        document = export_run(sim)
        self.assertEqual(document["format"], "noopunk.social_science.run")
        self.assertTrue(document["metrics"]["synthetic"])
        materials = {claim["provenance"]["material"] for claim in document["claims"]}
        self.assertIn("synthesized", materials)
        self.assertTrue(all(event["synthetic"] is True for event in document["events"]))
        self.assertIn(
            "not an empirical finding",
            document["manifest"]["provenance_note"].replace(
                "no value here is an", "not an"
            ),
        )

    def test_write_run_round_trip_json(self):
        sim = build_synthetic_scenario(seed=4, turns=2)
        sim.run()
        with tempfile.TemporaryDirectory() as directory:
            path = write_run(Path(directory) / "run.json", sim)
            loaded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["manifest"]["seed"], 4)
        self.assertEqual(loaded["events"], sim.log.to_dicts())

    def test_cli_runs_without_rpg_or_llm(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run.json"
            code = demo_main(["--seed", "7", "--turns", "2", "--out", str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())

    def test_baseline_benchmark_runs_without_rpg_or_llm(self):
        from src.social_science.benchmark import benchmark

        result = benchmark(actors=20, turns=2)
        self.assertGreater(result["events"], 0)
        self.assertGreater(result["seconds"], 0.0)
        self.assertTrue(result["synthetic"])

    def test_simulator_package_does_not_import_rpg_modules(self):
        import ast

        package = Path(__file__).resolve().parents[1] / "src" / "social_science"
        forbidden = {"rules", "mud", "godot", "evennia", "cwn", "world", "console"}
        for path in package.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module or ""]
                for name in names:
                    self.assertFalse(
                        any(part in forbidden for part in name.split(".")),
                        f"{path.name} imports RPG module {name}",
                    )

    def test_document_records_boundary_and_no_rpg_diff(self):
        doc = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "simulation"
            / "SOCIAL_SCIENCE_SIMULATOR_1286.md"
        )
        text = doc.read_text(encoding="utf-8").lower()
        for term in (
            "observed",
            "inferred",
            "synthesized",
            "simulated",
            "no rpg",
            "ai26",
        ):
            self.assertIn(term, text)

    def test_metrics_are_exploratory_not_predictive(self):
        sim = build_synthetic_scenario(seed=7, turns=2)
        sim.run()
        metrics = simulation_metrics(sim)
        self.assertIn("exploratory", metrics["provenance_note"])
        self.assertIn("social", metrics["graphs"])
        self.assertIn("communication", metrics["graphs"])


if __name__ == "__main__":
    unittest.main()
