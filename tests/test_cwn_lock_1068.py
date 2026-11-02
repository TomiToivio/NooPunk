"""Regression checks for the structural CWN lock (#1068)."""
import unittest
from tools.check_cwn_lock_1068 import audit


class CWNLockTests(unittest.TestCase):
    def test_required_core_and_tabletop_evidence_exists(self):
        self.assertEqual(audit(), [])


if __name__ == "__main__":
    unittest.main()
