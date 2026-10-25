"""Deterministic tests for issue #594's non-overlapping original systems."""
import unittest

from src.rules.noopunk_crisis_contact import Crisis, Contact


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


if __name__ == "__main__":
    unittest.main()
