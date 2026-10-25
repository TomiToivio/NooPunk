"""Offline contract tests for #572's opt-in NoöPunk extension kernel."""
import unittest

from src.rules.noopunk_extensions import Link, NaturalPsi, reach


class NetworkTests(unittest.TestCase):
    def test_heterogeneous_ubiquitous_route(self):
        links = (Link("agent", "drone", "radio"), Link("drone", "terminal", "mesh"),
                 Link("terminal", "archive", "wired"))
        self.assertEqual(reach(links, "agent", "archive").channel_path,
                         ("radio", "mesh", "wired"))
        self.assertFalse(reach(links, "agent", "archive",
                               channels=frozenset({"wired"})).reachable)

    def test_airgap_social_link_and_offline_route(self):
        self.assertFalse(reach((Link("agent", "friend", "radio"),),
                               "agent", "isolated").reachable)
        with self.assertRaises(ValueError):
            Link("agent", "archive", "social_tie")
        self.assertFalse(reach((Link("agent", "archive", "bci", authorized=False),),
                               "agent", "archive", require_authorization=True).reachable)

    def test_psi_channels_are_not_network_routes_by_default(self):
        """#572: PSI resolves where the network does not -- a psychic hop is not a login."""
        links = (Link("operator", "archive", "psychic"),)
        self.assertFalse(reach(links, "operator", "archive").reachable)
        self.assertTrue(reach(links, "operator", "archive", allow_psi_channels=True).reachable)
        self.assertFalse(reach((Link("operator", "archive", "psychotronic"),),
                               "operator", "archive").reachable)

    def test_disciplines_are_the_six_canonical_psi_skills(self):
        from src.rules import noopunk_extensions as ext
        self.assertEqual(set(ext.DISCIPLINES),
                         {"esp", "telepathy", "psychokinesis", "precognition",
                          "psychic_defence", "noospace"})

    def test_failed_link_does_not_become_access(self):
        self.assertFalse(reach((Link("agent", "target", "mesh", operational=False),),
                               "agent", "target").reachable)


class PsiTests(unittest.TestCase):
    def test_natural_psi_is_learned_not_class_bound(self):
        psi = NaturalPsi(capacity=2)
        self.assertEqual(psi.learn("telepathy"), 0)
        psi.commit("ongoing-contact", "telepathy")
        self.assertEqual(psi.available, 1)
        copy = NaturalPsi.from_dict(psi.to_dict())
        self.assertEqual(copy.to_dict(), psi.to_dict())
        copy.release("ongoing-contact")
        self.assertEqual(copy.available, 2)

    def test_effort_limit_and_training_gates(self):
        psi = NaturalPsi(capacity=1)
        with self.assertRaises(ValueError):
            psi.commit("untrained", "telepathy")
        psi.learn("esp")
        psi.commit("vision", "esp")
        with self.assertRaises(ValueError):
            psi.commit("second", "esp")
        psi.rest()
        self.assertEqual(psi.available, 1)
        with self.assertRaises(ValueError):
            NaturalPsi(aptitude=False).learn("esp")


if __name__ == "__main__":
    unittest.main()
