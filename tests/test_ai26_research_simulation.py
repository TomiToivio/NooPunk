"""Synthetic AI26 simulator regression tests; no RPG or empirical data.

Plain `unittest`, because the repository's CI runs `unittest discover` without pytest installed — the import of pytest
here was what reddened the root suite, not a behaviour change.
"""
from __future__ import annotations

import inspect
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simulation import ai26_research as research  # noqa: E402
from simulation.ai26_research import (  # noqa: E402
    ResearchActor, demo_roster, main, simulate, verify_replay,
)
from simulation.events import Event  # noqa: E402
from simulation.provenance import Origin, Provenance  # noqa: E402
from simulation.world_state import reduce_events  # noqa: E402


class DeterminismTests(unittest.TestCase):
    def test_seeded_runs_are_byte_identical(self):
        roster = demo_roster(50)
        first = simulate(roster, turns=40, seed=11)
        second = simulate(reversed(roster), turns=40, seed=11)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertTrue(verify_replay(first))
        self.assertEqual(first["summary"]["communication_events"], 40)

    def test_different_seed_changes_communications(self):
        roster = demo_roster(20)
        first = simulate(roster, turns=20, seed=1)
        second = simulate(roster, turns=20, seed=2)
        self.assertNotEqual(first["graphs"]["communication_edges"], second["graphs"]["communication_edges"])


class GraphTests(unittest.TestCase):
    def test_graph_integrity_and_replay_with_independent_organizations(self):
        result = simulate(demo_roster(5), seed=7, turns=8)
        graph = result["graphs"]
        ids = {node["actor_id"] for node in graph["nodes"]}
        self.assertTrue({"synthetic:organization-a", "synthetic:organization-b"} <= ids)
        self.assertTrue(all(edge["source"] in ids and edge["target"] in ids
                            for edge in graph["social_edges"] + graph["communication_edges"]))
        self.assertEqual(len(graph["social_edges"]), 5)
        self.assertTrue(all(edge["turn"] >= 0 for edge in graph["communication_edges"]))
        self.assertTrue(all(edge["source"] != edge["target"] for edge in graph["communication_edges"]))
        self.assertTrue(verify_replay(result))
        events = [Event.from_dict(item) for item in result["events"]]
        self.assertEqual(reduce_events(events).event_count, len(result["events"]))

    def test_isolates_and_empty_rosters_have_no_fake_messages(self):
        zero = simulate((), seed=7, turns=5)
        single = simulate((ResearchActor("synthetic:a", "individual"),), turns=5)
        self.assertEqual(zero["summary"]["events"], 0)
        self.assertEqual(single["summary"]["events"], 0)
        self.assertEqual(single["summary"]["isolated_actors"], ["synthetic:a"])
        self.assertTrue(verify_replay(zero))


class RefusalTests(unittest.TestCase):
    def test_rejects_duplicate_actor_references(self):
        duplicate = (ResearchActor("synthetic:a", "individual"), ResearchActor("synthetic:a", "individual"))
        with self.assertRaises(ValueError):
            simulate(duplicate)

    def test_rejects_dangling_actor_references(self):
        dangling = (ResearchActor("synthetic:a", "individual", "synthetic:missing"),)
        with self.assertRaises(ValueError):
            simulate(dangling)

    def test_rejects_non_synthetic_actor_ids_and_invalid_membership(self):
        with self.assertRaises(ValueError):
            ResearchActor("real-person", "individual")
        with self.assertRaises(ValueError):
            ResearchActor("synthetic:org", "organization", "synthetic:other")
        with self.assertRaises(ValueError):
            simulate(demo_roster(2), turns=-1)


class ExportTests(unittest.TestCase):
    def test_export_replay_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.json"
            self.assertEqual(main(["--population", "4", "--turns", "6", "--seed", "15",
                                   "--output", str(path)]), 0)
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], "ai26-synthetic-experiment-v2")
        # Provenance is a record now, not a string: the run is simulated, and it says why (#1286).
        self.assertEqual(payload["provenance"]["origin"], "simulated")
        self.assertEqual(payload["provenance"]["method"], "random-encounter-null-v1")
        self.assertTrue(payload["provenance"]["uncertainty"])
        self.assertEqual(payload["scientific_status"], "hypothetical_null_model_not_empirical_finding")
        self.assertTrue(verify_replay(payload))
        payload["events"][-1]["content"] = "tampered"
        self.assertFalse(verify_replay(payload))

    def test_no_game_or_llm_runtime_imports(self):
        source = inspect.getsource(research)
        for forbidden in ("import rules", "import mud", "import godot", "import ollama",
                          "import strategy_game", "import concordia"):
            self.assertNotIn(forbidden, source)


class ProvenanceTests(unittest.TestCase):
    def test_actor_origins_are_distinguishable_and_survive_export(self):
        """The four origins exist as a type, and an export says which one each actor is."""
        roster = demo_roster(6)
        payload = simulate(roster, turns=3, seed=5)
        # `demo_roster(n)` yields n individuals *plus* the organizations they affiliate to.
        self.assertEqual(payload["origins"]["synthesized"], len(roster))
        self.assertEqual(payload["origins"]["observed"], 0, "a synthetic roster is never observed material")
        self.assertTrue(all(actor["origin"] == "synthesized" for actor in payload["configuration"]["actors"]))

    def test_an_actor_may_be_inferred_but_never_observed(self):
        inferred = ResearchActor("synthetic:inferred-one", "individual", origin=Origin.INFERRED)
        payload = simulate((inferred, ResearchActor("synthetic:two", "individual")), turns=2, seed=1)
        self.assertEqual(payload["origins"]["inferred"], 1)
        with self.assertRaises(ValueError):
            ResearchActor("synthetic:corpus-record", "individual", origin=Origin.OBSERVED)

    def test_provenance_round_trips_through_json(self):
        for origin in Origin:
            record = Provenance(origin, source="s", method="m", uncertainty="high", review_status="provisional")
            restored = Provenance.from_dict(json.loads(json.dumps(record.to_dict())))
            self.assertEqual(restored, record)
        with self.assertRaises(ValueError):
            Provenance.from_dict({"source": "nowhere"})


if __name__ == "__main__":
    unittest.main()
