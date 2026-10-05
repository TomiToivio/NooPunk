"""Tests for the mandatory resolver seam (#40 Phase C), on the issue #111 core.

``docs/SIMULATION_ARCHITECTURE_SPEC.md`` §7.4 is binding:

> No LLM output may enter the event log except through the deterministic resolver.
> Where a canonical rule exists, the resolver must reach the rule through the shared
> rules layer — not through a re-implementation inside Concordia. Where no rule
> exists, the resolver must return an *explicit unresolved outcome*, not an
> improvised one.

Issue #111 replaced the resolution kernel with ``STAT + Skill + 1d10 >= DV`` (both
ratings 1..10) and retired the 2d6 engine, the ``SkillAccess`` gate and the
``attempted`` / ``unskilled_modifier`` fields. This module is ported to that kernel:
the seam's *guarantees* are unchanged — no bypass, explicit gaps, one event per
committed resolution — while the assertions about retired fields are gone rather than
asserting mechanics the rulebook no longer contains.
"""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concordia_runtime import (
    Capability,
    Decision,
    ProposedAction,
    Resolution,
    ResolverSeam,
    resolve_proposal,
)
from rules import AttributeSet, resolve_check
from simulation.engine import Simulation


#: 1..10 STAT ratings (issue #111). Deliberately non-canonical names.
ATTRIBUTES = AttributeSet(
    {"FIT": 4, "REF": 6, "INT": 5, "CHA": 7, "CYB": 8, "PSY": 5}
)

#: A deliberately minimal, clearly non-canonical action registry. Defining which
#: actions exist is a tabletop decision (AGENTS.md §4), so the tests supply their
#: own rather than reading canon that does not exist yet.
RULES = {
    "persuade": {"difficulty": 15},
    "climb": {"difficulty": 17},
    "lift": {"difficulty": 15},
}


def capability(**kwargs) -> Capability:
    return Capability(**{"attribute_id": "CHA", **kwargs})


class ResolverSeamTests(unittest.TestCase):
    def setUp(self) -> None:
        self.simulation = Simulation(simulation_id="sim:test")
        self.seam = ResolverSeam(self.simulation)

    # -- resolved path ----------------------------------------------------- #

    def test_resolved_action_uses_the_shared_rules_layer(self) -> None:
        """The seam must not re-implement resolution; the numbers must match it."""
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="persuade the council", action_type="persuade"),
            attributes=ATTRIBUTES,
            capability=capability(skill_level=6),
            rules=RULES,
            dice_total=4,
        )
        expected = resolve_check(
            stat=ATTRIBUTES["CHA"], skill=6, target=15, die=4
        )
        self.assertIs(resolution.decision, Decision.RESOLVED)
        self.assertEqual(resolution.outcome.total, expected.total)
        self.assertEqual(resolution.outcome.success, expected.success)
        self.assertEqual(resolution.outcome.die, expected.die)

    def test_resolved_action_records_canonical_numbers_in_the_event(self) -> None:
        resolution, event = self.seam.resolve_and_commit(
            ProposedAction(actor="fixture:a", intent="persuade the council", action_type="persuade"),
            attributes=ATTRIBUTES,
            capability=capability(skill_level=6),
            rules=RULES,
            dice_total=4,
        )
        # The event states the canonical 1d10 formula and the DV it faced.
        self.assertIn("1d10", event.content)
        self.assertIn("DV 15", event.content)
        self.assertIn("success", event.content)
        # The natural-language intent survives beside the numbers.
        self.assertIn("persuade the council", event.content)

    def test_committed_event_is_concordia_sourced_and_synthetic(self) -> None:
        _, event = self.seam.resolve_and_commit(
            ProposedAction(actor="fixture:a", intent="climb it", action_type="climb"),
            attributes=ATTRIBUTES,
            capability=capability(attribute_id="REF", skill_level=6),
            rules=RULES,
            dice_total=9,
        )
        self.assertEqual(event.source, "concordia")
        self.assertTrue(event.synthetic)

    def test_the_llm_cannot_supply_dice(self) -> None:
        """`dice_total` is for deterministic callers; a proposal cannot carry one."""
        proposal = ProposedAction(
            actor="fixture:a", intent="climb it", action_type="climb",
            check={"difficulty": 17, "dice_total": 18},
        )
        # Even with an attempt to smuggle a dice value into `check`, the seam rolls
        # or takes the injection from the *caller*, not from the proposal.
        resolution = resolve_proposal(
            proposal, attributes=ATTRIBUTES,
            capability=capability(attribute_id="REF", skill_level=6), rules=RULES,
        )
        self.assertIsNotNone(resolution.outcome.die)
        self.assertNotEqual(resolution.outcome.die, 18)

    # -- unresolved path: the whole point --------------------------------- #

    def test_action_without_a_canonical_rule_is_unresolved(self) -> None:
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="declare martial law",
                           action_type="declare_martial_law"),
            attributes=ATTRIBUTES, capability=capability(), rules=RULES,
        )
        self.assertIs(resolution.decision, Decision.UNRESOLVED)
        self.assertEqual(resolution.reason, "no_canonical_rule_for_action")
        self.assertIsNone(resolution.outcome)
        self.assertNotIn("success", resolution.event_content())

    def test_missing_difficulty_is_unresolved_not_invented(self) -> None:
        """The tabletop rulebook has not assigned a difficulty: that is a gap, not a guess."""
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="do the undefined thing", action_type="vague"),
            attributes=ATTRIBUTES, capability=capability(), rules={"vague": {}},
        )
        self.assertIs(resolution.decision, Decision.UNRESOLVED)
        self.assertEqual(resolution.reason, "no_difficulty_specified")

    def test_missing_capability_is_unresolved(self) -> None:
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="persuade", action_type="persuade"),
            rules=RULES,
        )
        self.assertIs(resolution.decision, Decision.UNRESOLVED)
        self.assertEqual(resolution.reason, "no_capability_specified")

    def test_unknown_attribute_is_unresolved(self) -> None:
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="persuade", action_type="persuade"),
            attributes=ATTRIBUTES, capability=capability(attribute_id="LUCK"), rules=RULES,
        )
        self.assertIs(resolution.decision, Decision.UNRESOLVED)
        self.assertEqual(resolution.reason, "no_stat_specified")

    def test_empty_intent_is_unresolved(self) -> None:
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="   ", action_type="persuade"),
            attributes=ATTRIBUTES, capability=capability(), rules=RULES,
        )
        self.assertIs(resolution.decision, Decision.UNRESOLVED)
        self.assertEqual(resolution.reason, "empty_action")

    def test_action_without_the_skill_is_unresolved_not_a_failure(self) -> None:
        """Issue #111 defines no unskilled procedure, so a skill-less attempt is a gap.

        It must be reported as such rather than resolved at an invented penalty.
        """
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="suture the wound", action_type="climb"),
            attributes=ATTRIBUTES,
            capability=capability(attribute_id="REF", has_skill=False),
            rules=RULES,
        )
        self.assertIs(resolution.decision, Decision.UNRESOLVED)
        self.assertEqual(resolution.reason, "skill_not_available")
        self.assertIsNone(resolution.outcome)

    def test_unresolved_actions_appear_in_the_review_queue(self) -> None:
        self.seam.resolve_and_commit(
            ProposedAction(actor="a", intent="persuade", action_type="persuade"),
            attributes=ATTRIBUTES, capability=capability(skill_level=6), rules=RULES, dice_total=5,
        )
        self.seam.resolve_and_commit(
            ProposedAction(actor="b", intent="declare war", action_type="declare_war"),
            attributes=ATTRIBUTES, capability=capability(), rules=RULES,
        )
        queue = self.seam.unresolved()
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0].proposal.intent, "declare war")

    def test_summary_reports_reasons_not_just_counts(self) -> None:
        self.seam.resolve_and_commit(
            ProposedAction(actor="a", intent="declare war", action_type="declare_war"),
            attributes=ATTRIBUTES, capability=capability(), rules=RULES,
        )
        self.seam.resolve_and_commit(
            ProposedAction(actor="b", intent="suture", action_type="climb"),
            attributes=ATTRIBUTES,
            capability=capability(attribute_id="REF", has_skill=False),
            rules=RULES,
        )
        summary = self.seam.summary()
        self.assertEqual(summary["decisions"]["UNRESOLVED"], 2)
        self.assertIn("no_canonical_rule_for_action", summary["unresolved_reasons"])
        self.assertIn("skill_not_available", summary["unresolved_reasons"])

    # -- the bypass must be impossible ------------------------------------ #

    def test_commit_refuses_a_raw_proposal(self) -> None:
        proposal = ProposedAction(actor="fixture:a", intent="persuade", action_type="persuade")
        with self.assertRaises(TypeError):
            self.seam.commit(proposal)  # type: ignore[arg-type]

    def test_commit_refuses_a_raw_string(self) -> None:
        """A model's utterance must never reach the log by being passed through."""
        with self.assertRaises(TypeError):
            self.seam.commit("Alice persuades the council successfully")  # type: ignore[arg-type]

    def test_commit_refuses_a_hand_built_event(self) -> None:
        event = self.simulation.emit(actor="fixture:a", action_type="free_form",
                                     content="the LLM says this succeeded")
        with self.assertRaises(TypeError):
            self.seam.commit(event)  # type: ignore[arg-type]

    def test_nothing_reaches_the_log_without_a_resolution(self) -> None:
        with self.assertRaises(TypeError):
            self.seam.commit("unresolved text")  # type: ignore[arg-type]
        self.assertEqual(self.simulation.events, [])

    def test_seam_requires_a_simulation(self) -> None:
        with self.assertRaises(ValueError):
            ResolverSeam(None)

    # -- log integrity ----------------------------------------------------- #

    def test_one_event_per_committed_resolution(self) -> None:
        for index in range(3):
            self.seam.resolve_and_commit(
                ProposedAction(actor=f"fixture:a{index}", intent="persuade the council",
                               action_type="persuade"),
                attributes=ATTRIBUTES, capability=capability(skill_level=6), rules=RULES,
                dice_total=5,
            )
        self.assertEqual(len(self.simulation.events), 3)
        self.assertEqual(len(self.seam.resolutions), 3)

    def test_resolution_is_serialisable_for_audit(self) -> None:
        resolution, _ = self.seam.resolve_and_commit(
            ProposedAction(actor="fixture:a", intent="persuade the council", action_type="persuade"),
            attributes=ATTRIBUTES, capability=capability(skill_level=6), rules=RULES, dice_total=5,
        )
        payload = resolution.as_dict()
        self.assertEqual(payload["decision"], "RESOLVED")
        self.assertEqual(payload["outcome"]["skill"], 6)
        self.assertEqual(payload["outcome"]["die"], 5)

    def test_rule_provenance_is_recorded(self) -> None:
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="lift it", action_type="lift"),
            attributes=ATTRIBUTES, capability=capability(attribute_id="FIT", skill_level=5),
            rules=RULES, dice_total=6,
        )
        self.assertEqual(resolution.rule, "lift")
        # 1..10 STAT + 1..10 Skill + 1d10, no retired modifier stack.
        self.assertEqual(resolution.outcome.total, 4 + 5 + 6)

    def test_event_content_marks_unresolved_visibly(self) -> None:
        resolution, event = self.seam.resolve_and_commit(
            ProposedAction(actor="fixture:a", intent="declare war", action_type="declare_war"),
            attributes=ATTRIBUTES, capability=capability(), rules=RULES,
        )
        self.assertFalse(resolution.resolved)
        self.assertIn("unresolved", event.content)
        self.assertIn("no_canonical_rule_for_action", event.content)

    def test_playable_without_any_rule_registry(self) -> None:
        """An empty registry must degrade to explicit gaps, never crash or invent."""
        resolution = resolve_proposal(
            ProposedAction(actor="fixture:a", intent="anything at all", action_type="anything"),
            attributes=ATTRIBUTES, capability=capability(), rules={},
        )
        self.assertIs(resolution.decision, Decision.UNRESOLVED)
        self.assertEqual(resolution.reason, "no_canonical_rule_for_action")

    def test_resolution_must_be_the_type_the_seam_accepts(self) -> None:
        """Guard the guard: a Resolution built by hand is committable, others are not."""
        legitimate = Resolution(Decision.UNRESOLVED, ProposedAction(actor="a", intent="x"),
                                reason="no_canonical_rule_for_action")
        event = self.seam.commit(legitimate)
        self.assertEqual(event.actor, "a")


if __name__ == "__main__":
    unittest.main()
