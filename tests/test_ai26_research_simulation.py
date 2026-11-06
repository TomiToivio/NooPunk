"""Synthetic AI26 simulator regression tests; no RPG and no empirical data (#1286).

**Converted from pytest to `unittest`**, for two reasons that made the original suite invisible:

* CI runs `python -m unittest discover`, which collects `unittest.TestCase` classes only. Module-level
  `def test_*()` functions are imported and then ignored, so this file previously contributed **zero
  tests** while looking like eight.
* `pytest` is not in `requirements.txt`, so importing it made discovery of this module fail in CI even
  though it passes on a workstation where pytest happens to be installed.

Every assertion is preserved. The parametrised duplicate/dangling case became a `subTest` loop so a
failure still names which roster broke it.
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

from simulation import ai26_research as research
from simulation.ai26_research import (
    ResearchActor,
    demo_roster,
    main,
    simulate,
    verify_replay,
)
from simulation.events import Event
from simulation.world_state import reduce_events


class SeededReplayTest(unittest.TestCase):
    def test_seeded_runs_are_byte_identical(self) -> None:
        roster = demo_roster(50)
        first = simulate(roster, turns=40, seed=11)
        second = simulate(reversed(roster), turns=40, seed=11)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertTrue(verify_replay(first))
        self.assertEqual(first["summary"]["communication_events"], 40)

    def test_different_seed_changes_communications(self) -> None:
        roster = demo_roster(20)
        first = simulate(roster, turns=20, seed=1)
        second = simulate(roster, turns=20, seed=2)
        self.assertNotEqual(
            first["graphs"]["communication_edges"],
            second["graphs"]["communication_edges"],
        )


class GraphIntegrityTest(unittest.TestCase):
    def test_graph_integrity_and_replay_with_independent_organizations(self) -> None:
        result = simulate(demo_roster(5), seed=7, turns=8)
        graph = result["graphs"]
        ids = {node["actor_id"] for node in graph["nodes"]}
        self.assertTrue({"synthetic:organization-a", "synthetic:organization-b"} <= ids)
        for edge in graph["social_edges"] + graph["communication_edges"]:
            self.assertIn(edge["source"], ids)
            self.assertIn(edge["target"], ids)
        self.assertEqual(len(graph["social_edges"]), 5)
        self.assertTrue(all(edge["turn"] >= 0 for edge in graph["communication_edges"]))
        self.assertTrue(all(edge["source"] != edge["target"] for edge in graph["communication_edges"]))
        self.assertTrue(verify_replay(result))
        events = [Event.from_dict(item) for item in result["events"]]
        self.assertEqual(reduce_events(events).event_count, len(result["events"]))

    def test_isolates_and_empty_rosters_have_no_fake_messages(self) -> None:
        zero = simulate((), seed=7, turns=5)
        single = simulate((ResearchActor("synthetic:a", "individual"),), turns=5)
        self.assertEqual(zero["summary"]["events"], 0)
        self.assertEqual(single["summary"]["events"], 0)
        self.assertEqual(single["summary"]["isolated_actors"], ["synthetic:a"])
        self.assertTrue(verify_replay(zero))


class RejectionTest(unittest.TestCase):
    def test_rejects_duplicate_or_dangling_actor_references(self) -> None:
        cases = {
            "duplicate": (
                ResearchActor("synthetic:a", "individual"),
                ResearchActor("synthetic:a", "individual"),
            ),
            "dangling": (ResearchActor("synthetic:a", "individual", "synthetic:missing"),),
        }
        for name, roster in cases.items():
            with self.subTest(case=name), self.assertRaises(ValueError):
                simulate(roster)

    def test_rejects_non_synthetic_actor_ids_and_invalid_membership(self) -> None:
        with self.assertRaises(ValueError):
            ResearchActor("real-person", "individual")
        with self.assertRaises(ValueError):
            ResearchActor("synthetic:org", "organization", "synthetic:other")
        with self.assertRaises(ValueError):
            simulate(demo_roster(2), turns=-1)


class ExportTest(unittest.TestCase):
    def test_export_replay_and_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.json"
            code = main(
                ["--population", "4", "--turns", "6", "--seed", "15", "--output", str(path)]
            )
            self.assertEqual(code, 0)
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(payload["schema"], "ai26-synthetic-experiment-v1")
        self.assertEqual(payload["provenance"], "simulated")
        self.assertEqual(payload["scientific_status"], "hypothetical_null_model_not_empirical_finding")
        self.assertTrue(verify_replay(payload))
        payload["events"][-1]["content"] = "tampered"
        self.assertFalse(verify_replay(payload), "a tampered stream must not verify")


class ScopeTest(unittest.TestCase):
    def test_no_game_or_llm_runtime_imports(self) -> None:
        source = inspect.getsource(research)
        for forbidden in (
            "import rules",
            "import mud",
            "import godot",
            "import ollama",
            "import strategy_game",
            "import concordia",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
