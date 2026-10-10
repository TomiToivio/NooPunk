"""Guard for issue #224: the astral projection / Noöspace procedure.

Issue #224 asks for the projection procedure (access, navigation, encounters, perception,
return), the embodied/full-projection distinction, vulnerability and temporal ambiguity, the
shared AP/state-machine contract, and tests for remote astral interactions and permission
boundaries.

Three things this guard refuses to let drift:

* **Projection is a state, not a Skill roll.** #225 owns the four states; a projection must
  consult that machine rather than grow its own.
* **The body is not reachable from Noöspace.** The permission boundary is the point of the
  procedure: a projected consciousness acts in Noöspace, not in Physical or Social space.
* **Numbers are provisional.** `AGENTS.md` §4 reserves psionic mechanics; #224 asks for a
  procedure, so every value must stay marked PROVISIONAL and nothing may be promoted silently.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from src.rules import core  # noqa: E402
from src.rules import cross_domain_state as cd  # noqa: E402
from src.rules import noospace_projection as npj  # noqa: E402


class ProvisionalStatusTests(unittest.TestCase):
    def test_the_module_is_not_canonical(self) -> None:
        self.assertFalse(npj.IS_CANONICAL)

    def test_the_module_declares_itself_provisional(self) -> None:
        self.assertTrue(npj.PROVISIONAL)


class StateMachineIsConsumedTests(unittest.TestCase):
    """#225 owns the states; projection must consult them, not re-declare them."""

    def test_the_astral_state_is_225s_state(self) -> None:
        self.assertEqual(npj.ASTRAL_PROJECTED, cd.ASTRAL_PROJECTED)

    def test_the_realms_helper_defers_to_225(self) -> None:
        self.assertEqual(npj.astral_realms(), cd.realms_for(cd.ASTRAL_PROJECTED))

    def test_a_projection_acts_in_noospace_only(self) -> None:
        self.assertEqual(npj.astral_realms(), frozenset({cd.NOOSPACE}))

    def test_the_ap_table_is_225s_table(self) -> None:
        for action, cost in cd.AP_COSTS.items():
            self.assertEqual(npj.ap_price(action), cost)

    def test_ap_price_delegates_rather_than_hardcoding(self) -> None:
        original = cd.AP_COSTS["act"]
        try:
            cd.AP_COSTS["act"] = 4
            self.assertEqual(npj.ap_price("act"), 4)
        finally:
            cd.AP_COSTS["act"] = original

    def test_an_unknown_action_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            npj.ap_price("project")


class BodyIsUnreachableTests(unittest.TestCase):
    """The permission boundary the issue asks to test."""

    def test_a_projected_consciousness_cannot_control_its_body(self) -> None:
        self.assertFalse(npj.can_act_through_body(cd.ASTRAL_PROJECTED))
        self.assertFalse(npj.can_act_through_body(cd.CYBER_IMMERSED))
        self.assertFalse(npj.can_act_through_body(cd.INVOLUNTARY_DREAM_NDE))

    def test_an_embodied_character_controls_their_body(self) -> None:
        self.assertTrue(npj.can_act_through_body(cd.EMBODIED))

    def test_remote_action_in_noospace_is_permitted(self) -> None:
        npj.check_remote_action(state=cd.ASTRAL_PROJECTED, realm=cd.NOOSPACE)  # must not raise

    def test_remote_action_in_physical_space_is_blocked(self) -> None:
        with self.assertRaises(cd.CrossDomainError):
            npj.check_remote_action(state=cd.ASTRAL_PROJECTED, realm=cd.PHYSICAL)

    def test_remote_action_in_social_space_is_blocked(self) -> None:
        with self.assertRaises(cd.CrossDomainError):
            npj.check_remote_action(state=cd.ASTRAL_PROJECTED, realm=cd.SOCIAL)

    def test_a_projected_body_is_in_danger_when_deliberately_attacked(self) -> None:
        self.assertTrue(npj.body_in_danger(state=cd.ASTRAL_PROJECTED, deliberately_attacked=True))

    def test_a_body_alone_is_not_in_danger(self) -> None:
        self.assertFalse(npj.body_in_danger(state=cd.ASTRAL_PROJECTED, deliberately_attacked=False))


class AccessRouteTests(unittest.TestCase):
    def test_every_route_maps_to_a_225_state(self) -> None:
        states = {cd.EMBODIED, cd.CYBER_IMMERSED, cd.ASTRAL_PROJECTED, cd.INVOLUNTARY_DREAM_NDE}
        for route in npj.AccessRoute:
            self.assertIn(npj.ROUTE_STATE[route], states)

    def test_the_involuntary_route_is_involuntary(self) -> None:
        self.assertFalse(npj.AccessRoute.INVOLUNTARY.voluntary)

    def test_trained_technique_is_voluntary(self) -> None:
        self.assertTrue(npj.AccessRoute.TRAINED.voluntary)

    def test_the_involuntary_route_does_not_enter_full_projection(self) -> None:
        self.assertNotEqual(npj.ROUTE_STATE[npj.AccessRoute.INVOLUNTARY], cd.ASTRAL_PROJECTED)

    def test_lucid_dreaming_is_not_full_projection(self) -> None:
        self.assertEqual(npj.ROUTE_STATE[npj.AccessRoute.LUCID_DREAM], cd.INVOLUNTARY_DREAM_NDE)


class RegionTests(unittest.TestCase):
    def test_the_five_regions_are_404s(self) -> None:
        self.assertEqual([r.value for r in npj.REGION_ORDER],
                         ["near", "collective-unconscious", "biospheric", "noospheric", "deep"])

    def test_category_reliability_falls_strictly_with_depth(self) -> None:
        values = [npj.CATEGORY_RELIABILITY[r] for r in npj.REGION_ORDER]
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertEqual(len(set(values)), len(values), "reliability must strictly decrease")

    def test_uncertainty_rises_strictly_with_depth(self) -> None:
        values = [npj.UNCERTAINTY_BY_REGION[r] for r in npj.REGION_ORDER]
        self.assertEqual(values, sorted(values))
        self.assertEqual(len(set(values)), len(values), "uncertainty must strictly increase")

    def test_deeper_saturates_at_deep(self) -> None:
        self.assertEqual(npj.deeper(npj.Region.DEEP), npj.Region.DEEP)

    def test_nearer_saturates_at_near(self) -> None:
        self.assertEqual(npj.nearer(npj.Region.NEAR), npj.Region.NEAR)

    def test_deeper_steps_walk_the_order(self) -> None:
        self.assertEqual(npj.deeper(npj.Region.NEAR, 2), npj.Region.BIOSPHERIC)

    def test_negative_steps_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            npj.shift_region(npj.Region.NEAR, npj.Direction.DEEPER, -1)


class ResonanceNavigationTests(unittest.TestCase):
    def test_resonance_is_bounded(self) -> None:
        for score in (0.0, 0.5, 1.0):
            self.assertTrue(0.0 <= npj.resonance_score(familiarity=score) <= 1.0)

    def test_an_unknown_resonance_factor_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            npj.resonance_score(metres_travelled=0.5)

    def test_resonance_rises_with_its_inputs(self) -> None:
        low = npj.resonance_score(familiarity=0.1)
        high = npj.resonance_score(familiarity=0.9)
        self.assertGreater(high, low)

    def test_more_resonance_lowers_the_navigation_dv(self) -> None:
        hard = npj.navigation_dv(region=npj.Region.NEAR, resonance=0.1)
        easy = npj.navigation_dv(region=npj.Region.NEAR, resonance=0.9)
        self.assertLess(easy, hard)

    def test_deeper_regions_are_harder_to_navigate(self) -> None:
        dvs = [npj.navigation_dv(region=r, resonance=0.5) for r in npj.REGION_ORDER]
        self.assertEqual(dvs, sorted(dvs))

    def test_navigation_never_consumes_distance(self) -> None:
        """§40.4.3: near/far are metaphors for resonance, not Euclidean distance."""
        import inspect
        source = inspect.getsource(npj.navigation_dv)
        self.assertNotIn("distance", source)
        self.assertNotIn("metres", source)

    def test_the_navigation_rung_is_a_real_ladder_value(self) -> None:
        for region in npj.REGION_ORDER:
            name = npj.navigation_difficulty(region=region, resonance=0.5)
            self.assertIn(name, core.DIFFICULTIES.values())

    def test_out_of_range_resonance_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            npj.navigation_dv(region=npj.Region.NEAR, resonance=1.5)


class TemporalAmbiguityTests(unittest.TestCase):
    def test_time_ratio_rises_with_depth(self) -> None:
        values = [npj.TIME_RATIO_BY_REGION[r] for r in npj.REGION_ORDER]
        self.assertEqual(values, sorted(values))

    def test_near_noospace_maps_one_to_one(self) -> None:
        self.assertEqual(npj.elapsed_in_spacetime(region=npj.Region.NEAR, subjective_minutes=10),
                         10.0)

    def test_deep_noospace_does_not_map_one_to_one(self) -> None:
        self.assertNotEqual(
            npj.elapsed_in_spacetime(region=npj.Region.DEEP, subjective_minutes=10), 10.0)

    def test_negative_subjective_time_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            npj.elapsed_in_spacetime(region=npj.Region.NEAR, subjective_minutes=-1)


class PerceptionTests(unittest.TestCase):
    def test_uncorroborated_information_is_ambiguous_by_default(self) -> None:
        self.assertEqual(
            npj.perceived_information(region=npj.Region.NEAR, corroborated=False),
            npj.InformationSource.AMBIGUOUS)

    def test_a_same_region_witness_makes_it_shared(self) -> None:
        self.assertEqual(
            npj.perceived_information(region=npj.Region.NEAR, corroborated=True,
                                      same_region_witnesses=1),
            npj.InformationSource.SHARED_NOOSPACE)

    def test_corroboration_without_a_witness_is_still_ambiguous(self) -> None:
        self.assertEqual(
            npj.perceived_information(region=npj.Region.NEAR, corroborated=True,
                                      same_region_witnesses=0),
            npj.InformationSource.AMBIGUOUS)

    def test_confidence_is_bounded(self) -> None:
        for region in npj.REGION_ORDER:
            for source in npj.InformationSource:
                value = npj.confidence_in(region=region, source=source, corroborated=True)
                self.assertTrue(0.0 <= value <= 1.0)

    def test_confidence_falls_with_depth(self) -> None:
        values = [npj.confidence_in(region=r, source=npj.InformationSource.SHARED_NOOSPACE,
                                    corroborated=True) for r in npj.REGION_ORDER]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_an_out_of_range_confidence_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            npj.Perception(content="x", source=npj.InformationSource.AMBIGUOUS, confidence=1.4)


class EncounterTests(unittest.TestCase):
    def test_every_consciouous_agent_class_has_a_skill(self) -> None:
        for kind in npj.EncounterKind:
            self.assertIn(npj.encounter_skill(kind), {"Telepathy", "Perceive", "Psychic Defence"})

    def test_encounter_dv_rises_strictly_with_depth(self) -> None:
        dvs = [npj.encounter_dv(kind=npj.EncounterKind.DREAM_ENTITY, region=r, hostile=False)
               for r in npj.REGION_ORDER]
        self.assertEqual(dvs, sorted(dvs))
        self.assertEqual(len(set(dvs)), len(dvs),
                         "each region must be strictly harder than the one before it")

    def test_a_hostile_encounter_is_harder(self) -> None:
        calm = npj.encounter_dv(kind=npj.EncounterKind.DREAM_ENTITY, region=npj.Region.NEAR,
                                hostile=False)
        hostile = npj.encounter_dv(kind=npj.EncounterKind.DREAM_ENTITY, region=npj.Region.NEAR,
                                   hostile=True)
        self.assertGreater(hostile, calm)

    def test_a_nonhuman_encounter_is_harder_than_a_dream_entity(self) -> None:
        common = npj.encounter_dv(kind=npj.EncounterKind.DREAM_ENTITY, region=npj.Region.NEAR,
                                  hostile=False)
        nonhuman = npj.encounter_dv(kind=npj.EncounterKind.NONHUMAN, region=npj.Region.NEAR,
                                    hostile=False)
        self.assertGreater(nonhuman, common)


class ReturnTests(unittest.TestCase):
    def test_a_projected_character_can_return(self) -> None:
        self.assertTrue(npj.can_return(cd.ASTRAL_PROJECTED))

    def test_an_embodied_character_has_nowhere_to_return_from(self) -> None:
        self.assertFalse(npj.can_return(cd.EMBODIED))

    def test_voluntary_return_costs_the_exit_action(self) -> None:
        self.assertEqual(npj.return_cost(npj.ReturnKind.VOLUNTARY), cd.AP_COSTS["exit"])

    def test_snap_back_and_severance_are_free(self) -> None:
        self.assertEqual(npj.return_cost(npj.ReturnKind.SNAP_BACK), 0)
        self.assertEqual(npj.return_cost(npj.ReturnKind.SEVERANCE), 0)

    def test_voluntary_return_leaves_no_injury(self) -> None:
        self.assertIsNone(npj.return_aftermath(npj.ReturnKind.VOLUNTARY))

    def test_aftermath_uses_51_wound_vocabulary_only(self) -> None:
        ladder = ("Scratched", "Wounded", "Critical", "Down")
        for kind in npj.ReturnKind:
            state = npj.return_aftermath(kind)
            if state is not None:
                self.assertIn(state, ladder)

    def test_severance_is_worse_than_snap_back(self) -> None:
        ladder = ("Scratched", "Wounded", "Critical", "Down")
        snap = ladder.index(npj.return_aftermath(npj.ReturnKind.SNAP_BACK))
        sev = ladder.index(npj.return_aftermath(npj.ReturnKind.SEVERANCE))
        self.assertGreater(sev, snap)


class ProjectionLifecycleTests(unittest.TestCase):
    def test_a_trained_projection_enters_the_astral_state(self) -> None:
        p = npj.Projection("a", npj.AccessRoute.TRAINED)
        self.assertEqual(p.state, cd.ASTRAL_PROJECTED)
        self.assertTrue(p.voluntary)

    def test_an_involuntary_route_enters_the_dream_state(self) -> None:
        p = npj.Projection("a", npj.AccessRoute.INVOLUNTARY)
        self.assertEqual(p.state, cd.INVOLUNTARY_DREAM_NDE)
        self.assertFalse(p.voluntary)

    def test_navigation_changes_the_region(self) -> None:
        p = npj.Projection("a", npj.AccessRoute.TRAINED)
        self.assertEqual(p.navigate(resonance=0.6, direction=npj.Direction.DEEPER),
                         npj.Region.COLLECTIVE)

    def test_navigation_is_refused_while_embodied(self) -> None:
        p = npj.Projection("a", npj.AccessRoute.TRAINED)
        p.state = cd.EMBODIED
        with self.assertRaises(ValueError):
            p.navigate(resonance=0.6, direction=npj.Direction.DEEPER)

    def test_low_resonance_is_not_travel(self) -> None:
        p = npj.Projection("a", npj.AccessRoute.TRAINED)
        with self.assertRaises(ValueError):
            p.navigate(resonance=0.05, direction=npj.Direction.DEEPER)

    def test_returning_restores_the_embodied_state(self) -> None:
        p = npj.Projection("a", npj.AccessRoute.TRAINED)
        self.assertEqual(p.return_to_body(npj.ReturnKind.VOLUNTARY), cd.EMBODIED)

    def test_returning_from_an_embodied_state_is_refused(self) -> None:
        p = npj.Projection("a", npj.AccessRoute.TRAINED)
        p.state = cd.EMBODIED
        with self.assertRaises(ValueError):
            p.return_to_body(npj.ReturnKind.VOLUNTARY)

    def test_return_uses_225s_transition_legality(self) -> None:
        self.assertTrue(cd.legal_transition(cd.ASTRAL_PROJECTED, cd.EMBODIED))
