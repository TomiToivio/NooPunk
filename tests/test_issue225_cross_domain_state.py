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

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "18_CROSS_DOMAIN_STATE.md"

from src.rules import cross_domain_state as cds


def flat(path: Path) -> str:
    """Whitespace-collapsed: the chapter hard-wraps, so phrases span line breaks."""
    return " ".join(path.read_text(encoding="utf-8").split())


class StateMachineTests(unittest.TestCase):
    """AC1 — ONE state machine covering embodied, immersed, projected and involuntary."""

    STATES = ("Embodied", "Cyber-immersed", "Astral-projected", "Involuntary dream / NDE")

    def test_the_four_states_are_named(self) -> None:
        text = flat(CHAPTER)
        for state in self.STATES:
            with self.subTest(state=state):
                self.assertIn(f"**{state}**", text)

    def test_the_states_are_tabulated_as_one_machine(self) -> None:
        text = flat(CHAPTER)
        anchor = text.index("| State | Where the consciousness acts | Body |")
        table = text[anchor : anchor + 1400]
        for state in self.STATES:
            with self.subTest(state=state):
                self.assertIn(f"**{state}**", table, "a state is missing from the state table")

    def test_the_single_locus_rule_is_stated(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("One consciousness-instance has exactly one locus of control", text)

    def test_state_not_skill_decides_reach(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("State, not skill, decides reach", text)
        self.assertIn("cannot leave the embodied state by rolling well", text)

    def test_projection_is_distinguished_from_interface(self) -> None:
        """Modes 1-3 and local PSI are NOT states — the distinction is the whole point."""
        text = flat(CHAPTER)
        self.assertIn("Cyberspace modes 1\u20133", text)
        self.assertIn("Embodied local PSI", text)
        self.assertIn("is an *interface*, not a locus", text)

    def test_a_non_embodied_body_cannot_act(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("A non-embodied body cannot act", text)


class ActionEconomyTests(unittest.TestCase):
    """AC2 — shared AP/initiative, reactions, agent action economy."""

    def test_the_budget_and_one_clock_are_stated(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("3 action points (AP) per actor per exchange", text)
        self.assertIn("There is no separate hacking turn, PSI turn or astral turn", text)

    def test_ap_costs_are_tabulated(self) -> None:
        text = flat(CHAPTER)
        for action in ("**Act**", "**Move**", "**Prepare**", "**Cover**", "**React**", "**Exit**"):
            with self.subTest(action=action):
                self.assertIn(action, text)

    def test_held_ap_does_not_carry_over(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Unspent AP does **not** carry over between exchanges", text)

    def test_a_reaction_is_never_free(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("A reaction is therefore never free", text)
        self.assertIn("borrowed from the next", text)

    def test_agents_spend_from_the_same_clock_and_are_permission_capped(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Agents are actors", text)
        self.assertIn("capped by its permissions", text)

    def test_initiative_is_a_single_shared_contract(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("descending REF", text)
        self.assertIn("it may not fork it: every realm uses this one order", text)


class BodyExposureTests(unittest.TestCase):
    """AC2 — physical-body exposure, crossing realms, interruptions."""

    def test_the_body_is_exposed(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("The body is present, locatable and vulnerable", text)
        self.assertIn("It cannot be actively controlled by the projected consciousness", text)

    def test_harm_to_the_body_forces_a_return_test(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("forced-return test", text)
        self.assertIn("Harm to the body is a forced-return trigger", text)

    def test_no_realm_reaches_another_without_a_gateway(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("No realm reaches another without a declared gateway", text)
        self.assertIn("A gateway is a **precondition**, not a modifier", text)

    def test_device_compromise_is_not_brain_compromise_is_generalised(self) -> None:
        """#222's cybernetic case is asserted here as the cyber case of the general rule."""
        text = flat(CHAPTER)
        self.assertIn("Device compromise is not brain compromise", text)
        self.assertIn("the cybernetic case of this one general rule", text)

    def test_return_is_possible_but_never_free(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Returning is **always possible and never free**", text)


class CyberPsiTests(unittest.TestCase):
    """AC3 — the rare PSI-in-cyberspace power: prerequisites and counterplay, not general."""

    def test_the_power_is_named_and_scoped(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Noetic coupling", text)
        self.assertIn("**not a general ability**", text)

    def test_the_prerequisites_are_all_required(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Prerequisites \u2014 all of them, every time", text)
        for prereq in ("Awakened PSI", "actual vulnerable neural gateway",
                       "psychotronic coupling or attunement", "declared action"):
            with self.subTest(prereq=prereq):
                self.assertIn(prereq, text)

    def test_counterplay_is_specific(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Counterplay \u2014 specific and available", text)
        self.assertIn("Remove the gateway", text)
        self.assertIn("Psychic Defence", text)

    def test_it_is_not_a_psionic_hacking_license(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("does not replace **Infosec**", text)
        self.assertIn("cannot exceed the gateway it runs through", text)


class WorkedExampleTests(unittest.TestCase):
    """AC4 — simultaneous Physical/Social/Cyber/Psychic scenario on one clock."""

    def test_the_example_spans_four_realms_on_one_clock(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Worked example: one exchange, four realms", text)
        self.assertIn("All four spend from one clock, 3 AP each", text)
        for realm in ("Cyberspace", "Social", "Physical", "No\u00f6space"):
            with self.subTest(realm=realm):
                self.assertIn(realm, text)

    def test_the_example_shows_the_gateway_denial(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("No gateway, no crossing", text)
        self.assertIn("no general No\u00f6space\u2192cyberspace gateway exists", text)


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

    def test_a_reaction_is_never_free(self) -> None:
        economy = cds.ActionEconomy()
        economy.react()
        self.assertEqual(economy.debt, 1, "an unheld reaction must incur debt")
        economy.reset_for_exchange()
        self.assertEqual(economy.spent, 1, "the debt must be paid in the next exchange")


class HygieneTests(unittest.TestCase):
    """AC5 — cross-links, provisional labels, and the structural boundaries."""

    def test_provisional_numbers_are_labelled(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("PROVISIONAL pending author calibration", text)
        self.assertGreaterEqual(text.count("PROVISIONAL"), 6, "provisional numbers must be labelled")

    def test_the_three_named_chapters_cross_link_the_contract(self) -> None:
        for rel in ("rulebook/2_ATTRIBUTES.md", "rulebook/5_CYBERNETIC.md", "rulebook/6_PSYCHIC.md"):
            with self.subTest(chapter=rel):
                self.assertIn("18_CROSS_DOMAIN_STATE.md",
                              (ROOT / rel).read_text(encoding="utf-8"))

    def test_the_chapter_states_what_it_does_not_do(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("What this section deliberately does not do", text)
        for owner in ("#219", "#221/#228", "#223", "#224"):
            with self.subTest(owner=owner):
                self.assertIn(owner, text)

    def test_no_proprietary_system_is_named(self) -> None:
        text = flat(CHAPTER)
        for name in ("Cyberpunk", "Shadowrun", "Eclipse Phase", "GURPS", "CY_BORG", "Fudge", "Fate"):
            with self.subTest(system=name):
                self.assertNotIn(name, text)

    def test_the_document_keeps_no_dangling_relative_link(self) -> None:
        body = CHAPTER.read_text(encoding="utf-8")
        for target in re.findall(r"\]\((?!https?:)([^)#]+\.md)\)", body):
            with self.subTest(target=target):
                self.assertTrue((CHAPTER.parent / target).resolve().is_file(),
                                f"{target} does not resolve")

    def test_no_new_skill_or_attribute_is_invented(self) -> None:
        """The contract spends AP and uses existing Skills; it adds no vocabulary."""
        text = flat(CHAPTER)
        self.assertIn("No new Skills, STATs or derived statistics", text)


if __name__ == "__main__":
    unittest.main()
