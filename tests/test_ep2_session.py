"""Reproducible action/state/memory integration tests for #60."""
import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from concordia_runtime.ep2_session import EP2Session
from eclipse_phase_homebrew import EP2Character, EP2PoolState, PoolKind

class EP2SessionTests(unittest.TestCase):
    def setup_session(self, path):
        session = EP2Session(path, seed=23)
        session.add_character("player", EP2Character("fixture", skills={"Infosec": 60}),
                              EP2PoolState(maximum={PoolKind.INSIGHT: 2}))
        session.offer_action("player", "mesh_test", {"skill": "Infosec", "pool_kind": "insight", "pool_spend": "add_20"})
        return session

    def test_reload_preserves_pool_memory_and_rng(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "world.sqlite"
            session = self.setup_session(path)
            observations = []
            class Agent:
                def observe(self, text): observations.append(text)
            first = session.resolve("player", "mesh_test", observers=(Agent(),))
            session.close()
            resumed = EP2Session(path, seed=999)
            self.assertEqual(resumed.memories(), [first])
            self.assertEqual(resumed.state["characters"]["player"]["current"]["insight"], 1)
            second = resumed.resolve("player", "mesh_test")
            baseline = self.setup_session(":memory:")
            self.assertEqual(first, baseline.resolve("player", "mesh_test"))
            self.assertEqual(second, baseline.resolve("player", "mesh_test"))
            self.assertEqual(len(observations), 1)
            resumed.close()
            baseline.close()

    def test_rejected_action_has_no_effect(self):
        session = self.setup_session(":memory:")
        with self.assertRaises(ValueError): session.resolve("player", "invented_outcome")
        self.assertEqual(session.memories(), [])
        self.assertEqual(session.state["characters"]["player"]["current"][PoolKind.INSIGHT], 2)
        session.resolve("player", "mesh_test")
        session.resolve("player", "mesh_test")
        with self.assertRaises(ValueError): session.resolve("player", "mesh_test")
        self.assertEqual(len(session.memories()), 2)
        session.close()
