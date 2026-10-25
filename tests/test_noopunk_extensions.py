"""Offline, deterministic checks for additive NoöPunk extensions (#572)."""
import unittest

from src.rules.noopunk_extensions import (
    Node, UbiquitousNetwork, HumanPsi, Crisis, Contact, seeded_scene,
)


class UbiquitousNetworkTests(unittest.TestCase):
    def test_relay_and_permission_are_separate(self):
        net = UbiquitousNetwork()
        for node in (Node("operator"), Node("implant"),
                     Node("clinic", protected=True, owner="clinic_admin")):
            net.add(node)
        net.connect("operator", "implant")
        net.connect("implant", "clinic")
        self.assertEqual(net.route("operator", "clinic"), ("operator", "implant", "clinic"))
        self.assertEqual(net.assess("operator", "clinic", "unauthorized"), "contested")
        self.assertEqual(net.assess("operator", "clinic", "clinic_admin"), "permitted")

    def test_disconnected_target_never_yields_to_lucky_dice(self):
        net = UbiquitousNetwork()
        net.add(Node("user"))
        net.add(Node("offline", online=False, protected=True))
        self.assertIsNone(net.route("user", "offline"))
        self.assertEqual(net.assess("user", "offline", "user"), "blocked")
        self.assertEqual(net.assess("user", "offline", "user", physical_presence=True), "contested")

    def test_cycle_has_deterministic_shortest_path(self):
        net = UbiquitousNetwork()
        for key in ("a", "b", "c", "d"):
            net.add(Node(key))
        for a, b in (("a", "c"), ("c", "d"), ("a", "b"), ("b", "d")):
            net.connect(a, b)
        self.assertEqual(net.route("a", "d"), ("a", "b", "d"))


class HumanPsiTests(unittest.TestCase):
    def test_any_human_can_train_and_sustain_psi(self):
        human = HumanPsi()
        self.assertFalse(human.activate("telepathy"))
        self.assertEqual(human.learn("telepathy"), 1)
        self.assertTrue(human.activate("telepathy", ongoing_id="shared-impression"))
        self.assertTrue(human.activate("telepathy"))
        self.assertEqual(human.available, 0)
        self.assertFalse(human.activate("telepathy"))
        clone = HumanPsi.restore(human.snapshot())
        self.assertEqual(clone.snapshot(), human.snapshot())
        clone.rest()
        self.assertEqual(clone.available, 1)
        clone.release("shared-impression")
        self.assertEqual(clone.available, 2)

    def test_invalid_training_is_rejected(self):
        with self.assertRaises(ValueError):
            HumanPsi(training={"made_up": 3})


class OriginalSubsystemTests(unittest.TestCase):
    def test_crisis_is_local_and_optional(self):
        crisis = Crisis()
        crisis.event(supply_loss=2, solidarity=-1)
        self.assertEqual((crisis.scarcity, crisis.trust), (2, 2))
        self.assertEqual(Crisis().scarcity, 0)

    def test_contact_preserves_autonomy_as_separate_dimension(self):
        contact = Contact()
        contact.negotiate(exchange=2, pressure=1)
        self.assertEqual((contact.reciprocity, contact.autonomy), (2, 2))

    def test_seeded_demo_replays(self):
        self.assertEqual(seeded_scene(19, 2, 8), seeded_scene(19, 2, 8))


if __name__ == "__main__":
    unittest.main()
