"""Regression tests for quarantine reachability in the provisional hacking subsystem."""
import unittest

from src.rules.ubiquitous_network import (
    AccessClass, ConnectivityClass, Era, IntrusionSession, NetworkError, reach,
)


class QuarantineReachTests(unittest.TestCase):
    def test_quarantine_never_reaches_isolated_targets(self):
        for era in Era:
            with self.subTest(era=era):
                allowed, reason = reach(ConnectivityClass.ISOLATED, AccessClass.QUARANTINE, era)
                self.assertFalse(allowed, reason)
                with self.assertRaises(NetworkError):
                    IntrusionSession(
                        target=ConnectivityClass.ISOLATED,
                        access=AccessClass.QUARANTINE,
                        era=era,
                    )

    def test_local_access_still_reaches_isolated_targets(self):
        for era in Era:
            with self.subTest(era=era):
                allowed, reason = reach(ConnectivityClass.ISOLATED, AccessClass.LOCAL, era)
                self.assertTrue(allowed, reason)

    def test_quarantine_bridge_remains_possible_for_connected_targets(self):
        for era in Era:
            with self.subTest(era=era):
                allowed, reason = reach(ConnectivityClass.PUBLIC_GATEWAY, AccessClass.QUARANTINE, era)
                self.assertTrue(allowed, reason)
                session = IntrusionSession(
                    target=ConnectivityClass.PUBLIC_GATEWAY,
                    access=AccessClass.QUARANTINE,
                    era=era,
                )
                self.assertTrue(session.breach)


if __name__ == "__main__":
    unittest.main()
