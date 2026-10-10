# -*- coding: utf-8 -*-
"""Issue #222 — the cyberspace subsystem, in the chapter the issue names.

The issue asks for five things and this pins each one, in the shape the repo's guard
discipline demands: a POSITIVE claim, clause-scoped, never a bare noun that a
negation could satisfy. "There is no universal brain-hack" is asserted as the denial
it is; "wetware is reachable only through a real neural path" is asserted as the
precondition it is.

The chapter previously deferred deep hacking in two places. Those deferrals are gone
and replaced by a pointer, so the chapter cannot both define the subsystem and say it
is undefined.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "5_CYBERNETIC.md"
RULEBOOK = ROOT / "RULEBOOK.md"


def flat(path: Path) -> str:
    """Whitespace-collapsed: the chapter hard-wraps, so phrases span line breaks."""
    return " ".join(path.read_text(encoding="utf-8").split())


class FourModes(unittest.TestCase):
    """AC1 — four DISTINCT modes, not one hack action with adjectives."""

    MODES = (
        "Global WWW / telepresence",
        "Embodied local AR + WLAN",
        "Node/edge graph hacking",
        "Immersive VR",
    )

    def test_every_mode_is_named(self) -> None:
        text = flat(CHAPTER)
        for mode in self.MODES:
            with self.subTest(mode=mode):
                self.assertIn(mode, text)

    def test_the_modes_are_tabulated_as_distinct(self) -> None:
        text = flat(CHAPTER)
        anchor = text.index("| Mode | Precondition | Reach | Latency | Authority |")
        table = text[anchor : anchor + 1400]
        for mode in self.MODES:
            with self.subTest(mode=mode):
                self.assertIn(mode, table, "a mode is missing from the mode table")

    def test_a_mode_is_chosen_by_place_not_by_skill(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("chosen by **where the character is and what path they use**", text)

    def test_the_immersive_mode_states_the_body_cost(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("trades the body for the network", text)
        self.assertIn("cannot be controlled by the projected consciousness", text)


class GraphHacking(unittest.TestCase):
    """AC2 — nodes/edges, privilege, ICE, defenders, detection, containment."""

    def test_the_node_card_carries_every_required_field(self) -> None:
        text = flat(CHAPTER)
        for field in ("`id`", "`zone`", "`hardening`", "`privilege`", "`ice`",
                      "`defenders`", "`edges`", "`containment`"):
            with self.subTest(field=field):
                self.assertIn(field, text)

    def test_the_card_is_the_same_object_in_both_media(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("renders the same card one-to-one", text)
        self.assertIn("no hidden state, no separate computer rules", text)

    def test_privilege_is_earned_one_tier_at_a_time(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("earned per node, one tier at a time", text)
        for tier in ("T0 Observe", "T1 Operate", "T2 Escalate", "T3 Control", "T4 Own"):
            with self.subTest(tier=tier):
                self.assertIn(tier, text)

    def test_each_ice_behaviour_is_defined(self) -> None:
        text = flat(CHAPTER)
        for behaviour in ("Sentry", "Barrier", "Hunter", "Warden"):
            with self.subTest(ice=behaviour):
                self.assertIn(f"**{behaviour}**", text)

    def test_the_defenders_are_actors_capped_by_permission(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Defenders are actors, not statistics", text)
        self.assertIn("capped by its permissions", text)

    def test_trace_is_the_detection_clock_and_containment_fires_from_the_card(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Trace is the detection clock", text)
        self.assertIn("the node's `containment` fires", text)

    def test_the_procedure_has_all_five_steps(self) -> None:
        text = flat(CHAPTER)
        for step in ("**Map**", "**Approach**", "**Escalate**", "**Act**", "**Cover**"):
            with self.subTest(step=step):
                self.assertIn(step, text)


class DamageLadder(unittest.TestCase):
    """AC3 — software -> hardware -> CONDITIONAL wetware, and the non-BCI path."""

    def test_the_three_layers_exist_in_order(self) -> None:
        text = flat(CHAPTER)
        software = text.index("**Software** — session-level")
        hardware = text.index("**Hardware** — device-level")
        wetware = text.index("**Wetware** — reachable")
        self.assertLess(software, hardware, "software must precede hardware")
        self.assertLess(hardware, wetware, "hardware must precede wetware")

    def test_wetware_requires_a_real_neural_path(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("only through an actual vulnerable connected neural path", text)
        self.assertIn("unreachable, whatever the attacker rolls", text)

    def test_universal_brain_hacking_is_denied(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Device compromise is not brain compromise", text)
        self.assertIn("There is no universal brain-hack", text)

    def test_emergency_disconnect_exists_and_costs_something(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Emergency disconnect is always available and always costs something", text)

    def test_a_non_bci_character_is_fully_playable(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Cybersecurity without a BCI is fully playable", text)
        self.assertIn("wetware risk is zero", text)

    def test_the_neurotechnical_gateway_is_the_precondition(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Neurotechnical gateways", text)
        self.assertIn("invasive BCI on an unhardened gateway is the *precondition*", text)


class WorkedExampleAndHygiene(unittest.TestCase):
    """AC4 + AC5 — one intrusion on the shared clock; DRAFT labels; no contradictions."""

    def test_a_worked_example_runs_on_the_shared_clock(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("Worked example: one intrusion on the shared clock", text)
        self.assertIn("3 actions per exchange", text)
        self.assertIn("one shared clock", text)

    def test_provisional_numbers_are_labelled_draft(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("DRAFT pending calibration", text)
        self.assertGreaterEqual(text.count("DRAFT"), 4, "provisional numbers must be labelled")

    def test_the_old_deferrals_no_longer_contradict_the_section(self) -> None:
        text = flat(CHAPTER)
        self.assertNotIn("deferred deep-hacking subsystem", text)
        self.assertNotIn("Deep hacking remains a separate deferred subsystem", text)
        self.assertIn("cyberspace surface itself is specified below", text)

    def test_the_chapter_still_preserves_the_non_invasive_path(self) -> None:
        """The new section must not have displaced the existing guarantee."""
        text = flat(CHAPTER)
        self.assertIn("A character who rejects invasive augmentation remains fully playable", text)

    def test_the_rulebook_mesh_section_is_untouched_and_cross_linked(self) -> None:
        """No new top-level section: the split map and the ledger numbering stay valid."""
        rulebook = flat(RULEBOOK)
        self.assertIn("## 15. Mesh, hacking, cyberspace, and the Noösphere", rulebook)
        self.assertIn("## 16. Psionics and Noösphere interaction", rulebook)

    def test_no_proprietary_system_is_named_in_the_new_section(self) -> None:
        text = flat(CHAPTER)
        for name in ("Cyberpunk", "Shadowrun", "Eclipse Phase", "GURPS", "CY_BORG"):
            with self.subTest(system=name):
                self.assertNotIn(name, text)

    def test_the_document_keeps_no_dangling_relative_link(self) -> None:
        body = CHAPTER.read_text(encoding="utf-8")
        for target in re.findall(r"\]\((?!https?:)([^)#]+\.md)\)", body):
            with self.subTest(target=target):
                self.assertTrue((CHAPTER.parent / target).resolve().is_file(),
                                f"{target} does not resolve")


if __name__ == "__main__":
    unittest.main()
