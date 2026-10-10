"""Issue #225 — the cross-domain state machine and the shared action economy.

The issue asks for five things; this pins each. Two halves, because the contract has
two halves: the **chapter** states the rules a table reads, and the **module** executes
the invariants that prose cannot enforce.

House discipline: every content assertion is a POSITIVE, clause-scoped claim, never a
bare noun a negation could satisfy. "No realm reaches another without a declared
gateway" is asserted as the denial-plus-condition it is.

Cross-links: #200 (epic), #217 (resolution semantics), #222 (cyberspace procedure).
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "18_CROSS_DOMAIN_STATE.md"

from src.rules import cross_domain_state as cds


def flat(path: Path) -> str:
    """Whitespace-collapsed: the chapter hard-wraps, so phrases span line breaks."""
    return " ".join(path.read_text(encoding="utf-8").split())












class ExecutableInvariantTests(unittest.TestCase):
    """The module executes the contract; these are the invariants prose cannot enforce."""

    def test_the_module_declares_itself_non_canonical(self) -> None:
        """PROVISIONAL must not quietly become shipped."""
        self.assertFalse(cds.IS_CANONICAL)

    def test_only_embodied_controls_the_body(self) -> None:
        self.assertTrue(cds.controls_body(cds.EMBODIED))
        for state in cds.PROJECTED_STATES:
            with self.subTest(state=state):
                self.assertFalse(cds.controls_body(state))

    def test_a_projected_character_cannot_take_a_physical_action(self) -> None:
        for state in cds.PROJECTED_STATES:
            with self.subTest(state=state):
                self.assertFalse(cds.can_act_in(state, cds.PHYSICAL))
                with self.assertRaises(cds.CrossDomainError):
                    cds.assert_can_act_in(state, cds.PHYSICAL)

    def test_no_direct_edge_between_two_projected_states(self) -> None:
        for source in cds.PROJECTED_STATES:
            for target in cds.PROJECTED_STATES:
                if source == target:
                    continue
                with self.subTest(source=source, target=target):
                    self.assertFalse(cds.legal_transition(source, target))
                    with self.assertRaises(cds.CrossDomainError):
                        cds.assert_transition(source, target)

    def test_every_projected_state_returns_to_embodied(self) -> None:
        for state in cds.PROJECTED_STATES:
            with self.subTest(state=state):
                self.assertTrue(cds.legal_transition(state, cds.EMBODIED))

    def test_single_locus_refuses_two_states(self) -> None:
        self.assertEqual(cds.single_locus((cds.EMBODIED,)), cds.EMBODIED)
        with self.assertRaises(cds.CrossDomainError):
            cds.single_locus((cds.EMBODIED, cds.CYBER_IMMERSED))

    def test_unknown_state_is_refused(self) -> None:
        with self.assertRaises(cds.CrossDomainError):
            cds.controls_body("lucid")

    def test_crossing_without_a_gateway_is_impossible(self) -> None:
        self.assertFalse(cds.can_cross(cds.CYBERNETIC, cds.PSYCHIC, has_gateway=False))
        self.assertTrue(cds.can_cross(cds.CYBERNETIC, cds.PSYCHIC, has_gateway=True))

    def test_no_general_noospace_cyberspace_gateway(self) -> None:
        """The impossibility must be *recorded*, not merely a fall-through of the lookup.

        Without the explicit membership assertion, deleting an entry from
        `NO_GATEWAY_EXISTS` is behaviour-preserving (the sparse-map fall-through also
        returns False), so the documented impossibility could rot away unnoticed.
        """
        self.assertIn((cds.NOOSPACE, cds.CYBERNETIC), cds.NO_GATEWAY_EXISTS)
        self.assertIn((cds.CYBERNETIC, cds.NOOSPACE), cds.NO_GATEWAY_EXISTS)
        for source, target in ((cds.NOOSPACE, cds.CYBERNETIC), (cds.CYBERNETIC, cds.NOOSPACE)):
            with self.subTest(source=source, target=target):
                self.assertIsNone(cds.gateway_for(source, target))
                self.assertFalse(cds.can_cross(source, target, has_gateway=True))

    def test_same_realm_crossing_needs_nothing(self) -> None:
        for realm in cds.REALMS:
            with self.subTest(realm=realm):
                self.assertTrue(cds.can_cross(realm, realm, has_gateway=False))

    def test_the_ap_budget_is_three_and_cannot_be_overspent(self) -> None:
        economy = cds.ActionEconomy()
        self.assertEqual(cds.AP_PER_EXCHANGE, 3)
        economy.spend("act")
        economy.spend("move")
        economy.spend("cover")
        with self.assertRaises(cds.CrossDomainError):
            economy.spend("act")





if __name__ == "__main__":
    unittest.main()
