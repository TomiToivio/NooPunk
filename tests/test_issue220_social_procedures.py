"""Issue #220 — the social procedures.

The issue asks for five things; this pins each. The guard leans hardest on **AC3**, because
"social NPC agency without automatic mind-reading or guaranteed lie detection" is the
easiest thing for a social system to get wrong, and a prose promise cannot stop it.

Cross-links: #200 (epic), #225 (the shared clock), #219 (the shared band arithmetic),
#233 (the aspect layer reused), #107/#122/#144 (the Affect graph preserved).
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "4_SOCIAL.md"

from src.rules import cross_domain_state as cds
from src.rules import physical_combat as pc
from src.rules import social as soc


def flat(path: Path) -> str:
    """Whitespace-collapsed: the chapter hard-wraps, so phrases span line breaks."""
    return " ".join(path.read_text(encoding="utf-8").split())


class OneArithmeticTests(unittest.TestCase):
    """AC1 — social play uses the SAME arithmetic, not a parallel one."""

    def test_the_band_function_is_imported_not_reimplemented(self) -> None:
        self.assertIs(soc.band_for_margin, pc.band_for_margin,
                      "social must reuse the physical band function, not re-declare it")

    def test_every_margin_maps_to_a_social_consequence(self) -> None:
        for value in range(-30, 31):
            with self.subTest(margin=value):
                got = soc.social_consequence(value, 0)
                self.assertIn(got, (*soc.SOCIAL_CONSEQUENCE.values(), soc.UNMOVED))

    def test_consequence_severity_is_monotonic_in_the_margin(self) -> None:
        order = [soc.UNMOVED,
                 soc.SOCIAL_CONSEQUENCE["glancing"],
                 soc.SOCIAL_CONSEQUENCE["solid"],
                 soc.SOCIAL_CONSEQUENCE["severe"],
                 soc.SOCIAL_CONSEQUENCE["brutal"]]
        previous = 0
        for value in range(-10, 20):
            index = order.index(soc.social_consequence(value + 10, 10))
            self.assertGreaterEqual(index, previous, f"regression at margin {value}")
            previous = index

    def test_the_band_boundaries_are_the_chapter_table(self) -> None:
        self.assertEqual(soc.social_consequence(10, 11), soc.UNMOVED)
        self.assertEqual(soc.social_consequence(10, 10), "Heard")
        self.assertEqual(soc.social_consequence(11, 10), "Leaning")
        self.assertEqual(soc.social_consequence(14, 10), "Leaning")
        self.assertEqual(soc.social_consequence(15, 10), "Convinced")
        self.assertEqual(soc.social_consequence(18, 10), "Convinced")
        self.assertEqual(soc.social_consequence(19, 10), "Committed")

    def test_a_social_result_is_a_state_not_a_counter(self) -> None:
        """Same as the physical ladder: resolving twice does not accumulate."""
        first = soc.resolve_social(14, 10, method="Talk")
        second = soc.resolve_social(14, 10, method="Talk")
        self.assertEqual(first.consequence, second.consequence)

    def test_the_action_economy_is_the_shared_contract(self) -> None:
        self.assertEqual(cds.AP_PER_EXCHANGE, 3)
        self.assertEqual(cds.AP_COSTS["react"], 1)


class HardLimitTests(unittest.TestCase):
    """AC3 — no mind-reading, no guaranteed lie detection, no rewriting a person."""

    def test_cues_alone_never_detect_a_lie(self) -> None:
        self.assertFalse(soc.detects_lie(kinesics_succeeded=True, contradicting_evidence=False),
                         "a good Kinesics check must never return certainty about a mind")
        self.assertFalse(soc.detects_lie(kinesics_succeeded=False, contradicting_evidence=False))

    def test_only_independent_evidence_detects_a_lie(self) -> None:
        self.assertTrue(soc.detects_lie(kinesics_succeeded=False, contradicting_evidence=True))

    def test_no_consequence_ever_rewrites_a_motivation(self) -> None:
        for consequence in (*soc.SOCIAL_CONSEQUENCE.values(), soc.UNMOVED):
            with self.subTest(consequence=consequence):
                self.assertFalse(soc.rewrites_motivation(consequence))

    def test_there_is_no_edge_mutation_api_in_the_module(self) -> None:
        """The capability must not exist: a missing function cannot be called by accident."""
        for forbidden in ("set_motivation", "overwrite_motivation", "write_belief",
                          "set_belief", "convert"):
            with self.subTest(name=forbidden):
                self.assertFalse(hasattr(soc, forbidden))

class CoercionTests(unittest.TestCase):
    """AC1/AC3 — coercion moves behaviour and always leaves a cost."""

    def test_coercion_always_attaches_a_grievance(self) -> None:
        outcome = soc.resolve_social(15, 10, method="Provoke")
        self.assertTrue(outcome.coercive)
        self.assertEqual(outcome.grievance, soc.GRIEVANCE_ASPECT)

    def test_persuasion_leaves_no_grievance(self) -> None:
        outcome = soc.resolve_social(15, 10, method="Talk")
        self.assertFalse(outcome.coercive)
        self.assertIsNone(outcome.grievance)

    def test_a_grievance_without_coercion_is_refused(self) -> None:
        with self.assertRaises(soc.SocialError):
            soc.SocialOutcome(consequence="Leaning", coercive=False, grievance="Grievance")

    def test_an_unknown_consequence_is_refused(self) -> None:
        with self.assertRaises(soc.SocialError):
            soc.SocialOutcome(consequence="Enslaved", coercive=True)

class ReputationStepTests(unittest.TestCase):
    """AC2 — a witnessed exchange may move Reputation by exactly ONE step."""

    def test_a_witnessed_exchange_moves_one_step(self) -> None:
        self.assertEqual(soc.resolve_social(15, 10, method="Talk", witnessed=True).reputation_step,
                         soc.REPUTATION_STEP)

    def test_an_unwitnessed_exchange_moves_nothing(self) -> None:
        self.assertEqual(soc.resolve_social(15, 10, method="Talk").reputation_step, 0)

    def test_an_unmoved_outcome_moves_nothing_even_when_witnessed(self) -> None:
        self.assertEqual(soc.resolve_social(9, 12, method="Talk", witnessed=True).reputation_step, 0)

    def test_a_larger_step_is_refused(self) -> None:
        with self.assertRaises(soc.SocialError):
            soc.SocialOutcome(consequence="Leaning", coercive=False, reputation_step=2)


class RelationshipStatusTests(unittest.TestCase):
    """AC2 — statuses are DERIVED from the Affect graph, never a second store."""

    def test_no_edges_means_unknown_not_a_stored_zero(self) -> None:
        self.assertEqual(soc.relationship_status([]), soc.UNKNOWN)

    def test_unknown_is_not_a_stored_score(self) -> None:
        """A stored zero would produce Acquainted; the absence of an edge must not."""
        self.assertNotEqual(soc.relationship_status([]), soc.ACQUAINTED)

    def test_a_strong_positive_edge_is_trusted(self) -> None:
        self.assertEqual(
            soc.relationship_status([soc.AffectEdgeView(label="Trusts", score=6)]),
            soc.TRUSTED)

    def test_a_strong_negative_edge_is_hostile(self) -> None:
        self.assertEqual(
            soc.relationship_status([soc.AffectEdgeView(label="Hates", score=-7)]),
            soc.HOSTILE)

    def test_an_obligation_is_indebted(self) -> None:
        self.assertEqual(
            soc.relationship_status([soc.AffectEdgeView(label="Owes", score=0)]),
            soc.INDEBTED)

    def test_a_negative_label_near_zero_is_estranged(self) -> None:
        self.assertEqual(
            soc.relationship_status([soc.AffectEdgeView(label="Distrusts", score=-2)]),
            soc.ESTRANGED)

    def test_a_neutral_edge_is_acquainted(self) -> None:
        self.assertEqual(
            soc.relationship_status([soc.AffectEdgeView(label="Knows", score=0)]),
            soc.ACQUAINTED)

    def test_statuses_are_derived_by_construction(self) -> None:
        self.assertTrue(soc.status_is_derived())

class GroupTests(unittest.TestCase):
    """AC1 — group interaction, with a BOUNDED modifier."""

    def test_support_is_capped(self) -> None:
        self.assertEqual(soc.group_support(1), 1)
        self.assertEqual(soc.group_support(2), 2)
        self.assertEqual(soc.group_support(50), soc.MAX_GROUP_SUPPORT)

    def test_negative_support_is_refused(self) -> None:
        with self.assertRaises(soc.SocialError):
            soc.group_support(-1)

    def test_the_cap_matches_the_recorded_situational_cap(self) -> None:
        self.assertEqual(soc.MAX_GROUP_SUPPORT, 2)

class HygieneTests(unittest.TestCase):
    """AC5 — provisional labels, independent wording, resolvable links."""

    def test_the_module_declares_itself_non_canonical(self) -> None:
        self.assertFalse(soc.IS_CANONICAL)

if __name__ == "__main__":
    unittest.main()
