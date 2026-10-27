import unittest
from src.rules.swn_transhuman import (
    ContinuityRegistry, DuplicationPolicy, Imprint, Mind, Shell, ContinuityError
)
from src.rules.swn_true_ai import TrueAI, AIHost, AIState, AIAgencyError


class TranshumanTests(unittest.TestCase):
    def setUp(self):
        self.origin = Mind("person", "lineage-x", Imprint("i0", "lineage-x", 1, "day-one"),
                           Shell("body-1", "organic"), True)

    def test_soft_lineage_forbids_active_forks(self):
        registry = ContinuityRegistry(DuplicationPolicy.SOFT)
        registry.register(self.origin)
        registry.backup("person", "copy1")
        with self.assertRaises(ContinuityError):
            registry.instantiate("copy1", "fork", Shell("body-2", "synthetic"))
        registry.deactivate("person")
        clone = registry.instantiate("copy1", "fork", Shell("body-2", "synthetic"))
        self.assertTrue(clone.active)

    def test_hard_lineage_allows_divergence(self):
        registry = ContinuityRegistry(DuplicationPolicy.HARD)
        registry.register(self.origin)
        registry.backup("person", "copy1")
        registry.instantiate("copy1", "fork", Shell("body-2", "synthetic"))
        self.assertEqual(registry.active_lineage("lineage-x"), ["fork", "person"])
        with self.assertRaises(ContinuityError):
            registry.resleeve("person", Shell("body-2", "synthetic"))
        self.assertEqual(registry.minds["person"].shell.identifier, "body-1")


class TrueAITests(unittest.TestCase):
    def test_host_brake_network_and_isolation(self):
        ai = TrueAI("panopticon", "core-01", 3, True,
                    permissions={"network", "physical", "self_modify"})
        ai.attach(AIHost("isolated-box", "server", 5))
        self.assertFalse(ai.authorize("network"))
        self.assertFalse(ai.authorize("self_modify"))
        ai.detach()
        ai.attach(AIHost("robot", "android", 5, True, True))
        self.assertTrue(ai.execute("physical"))
        self.assertFalse(ai.authorize("self_modify"))
        with self.assertRaises(AIAgencyError):
            ai.set_brake(False)
        ai.set_brake(False, oversight=True)
        self.assertTrue(ai.authorize("self_modify"))
        ai.isolate()
        self.assertFalse(ai.authorize("physical"))
        ai.reconnect()
        self.assertTrue(ai.authorize("network"))
        ai.terminate()
        self.assertEqual(ai.state, AIState.TERMINATED)
        with self.assertRaises(AIAgencyError):
            ai.attach(AIHost("new", "server", 2))

    def test_online_host_requirement(self):
        with self.assertRaises(AIAgencyError):
            TrueAI("a", "b", 1, False, state=AIState.ONLINE)


if __name__ == "__main__":
    unittest.main()
