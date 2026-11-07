"""Synthetic AI26 simulator regression tests; no RPG or empirical data.

Rewritten as a `unittest.TestCase` suite (#1286 follow-up): the file was merged with bare
`pytest`-style functions and `import pytest`, which `unittest discover` cannot collect and CI cannot
install — `requirements.txt` has no pytest, so the module failed at import in CI while passing on a
developer machine. The assertions are unchanged; only the harness is, so the guards actually run.

Run:
    python -m unittest discover -s tests -p "test_ai26_research_simulation.py"
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

from simulation.ai26_research import (
    ResearchActor,
    demo_roster,
    main,
    simulate,
    verify_replay,
)
from simulation.events import Event
from simulation.world_state import reduce_events


class ReplayTests(unittest.TestCase):
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
        self.assertNotEqual(
            first["graphs"]["communication_edges"], second["graphs"]["communication_edges"]
        )


class GraphIntegrityTests(unittest.TestCase):
    def test_graph_integrity_and_replay_with_independent_organizations(self):
        result = simulate(demo_roster(5), seed=7, turns=8)
        graph = result["graphs"]
        ids = {node["actor_id"] for node in graph["nodes"]}
        self.assertLessEqual({"synthetic:organization-a", "synthetic:organization-b"}, ids)
        for edge in graph["social_edges"] + graph["communication_edges"]:
            self.assertIn(edge["source"], ids)
            self.assertIn(edge["target"], ids)
        self.assertEqual(len(graph["social_edges"]), 5)
        for edge in graph["communication_edges"]:
            self.assertGreaterEqual(edge["turn"], 0)
            self.assertNotEqual(edge["source"], edge["target"])
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


class RosterRefusalTests(unittest.TestCase):
    def test_rejects_duplicate_actor_references(self):
        with self.assertRaises(ValueError):
            simulate((ResearchActor("synthetic:a", "individual"),
                      ResearchActor("synthetic:a", "individual")))

    def test_rejects_a_dangling_organization_reference(self):
        with self.assertRaises(ValueError):
            simulate((ResearchActor("synthetic:a", "individual", "synthetic:missing"),))

    def test_rejects_non_synthetic_actor_ids_and_invalid_membership(self):
        with self.assertRaises(ValueError):
            ResearchActor("real-person", "individual")
        with self.assertRaises(ValueError):
            ResearchActor("synthetic:org", "organization", "synthetic:other")
        with self.assertRaises(ValueError):
            simulate(demo_roster(2), turns=-1)


class ExportTests(unittest.TestCase):
    def test_export_replay_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            self.assertEqual(
                main(["--population", "4", "--turns", "6", "--seed", "15",
                      "--output", str(path)]),
                0,
            )
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], "ai26-synthetic-experiment-v1")
        self.assertEqual(payload["provenance"], "simulated")
        self.assertEqual(payload["scientific_status"],
                         "hypothetical_null_model_not_empirical_finding")
        self.assertTrue(verify_replay(payload))
        payload["events"][-1]["content"] = "tampered"
        self.assertFalse(verify_replay(payload))


class BoundaryTests(unittest.TestCase):
    def test_no_game_or_llm_runtime_imports(self):
        import simulation.ai26_research as research

        source = inspect.getsource(research)
        for forbidden in ("import rules", "import mud", "import godot", "import ollama",
                          "import strategy_game", "import concordia"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
