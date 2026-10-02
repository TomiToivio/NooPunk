"""Tests for the unified tag engine prototype (issue #51).

The issue's central constraint is **"Attributes are tags too"**, so the tests are
organized around proving that rather than around proving tags work at all:

* an attribute tag is an ordinary ``Tag`` with ``category="attribute"``;
* it sits *inside* the same stack as skill/gear/condition tags;
* there is no second resolution path for attributes;
* a non-attribute tag and an attribute tag with the same rating behave identically.

The absent-layer cases are tested as refusals, because the issue is explicit that an
absent layer is not a low score.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import resolve_check
from tags import (
    STACK_CAP_DEFAULT,
    Category,
    Entity,
    Outcome,
    Source,
    System,
    SystemPresence,
    Tag,
    TagError,
    attribute_tag,
    build_stack,
    resolve_action,
    sample_entities,
)
from tags.model import CANONICALITY_NOTE, PROTOTYPE_ATTRIBUTE_SYSTEMS


class TagModelTests(unittest.TestCase):
    def test_attribute_tags_are_ordinary_tags(self) -> None:
        """The issue's headline rule, asserted structurally."""
        tag = attribute_tag("REF", 2)
        self.assertIsInstance(tag, Tag)
        self.assertIs(tag.category, Category.ATTRIBUTE)
        self.assertTrue(tag.is_attribute)
        # Identical machinery: the same fields a skill tag has.
        for field in ("name", "rating", "category", "system", "scope", "source"):
            self.assertTrue(hasattr(tag, field), field)

    def test_attribute_tag_must_name_one_of_the_four_systems(self) -> None:
        for name, system in PROTOTYPE_ATTRIBUTE_SYSTEMS.items():
            with self.subTest(attribute=name):
                self.assertIs(attribute_tag(name, 1).system, system)

    def test_four_systems_are_canonical_from_the_rulebook(self) -> None:
        """RULEBOOK §5 makes the division canonical, so it is pinned here."""
        self.assertEqual(
            {system.value for system in System},
            {"physical", "social", "psychic", "cybernetic"},
        )

    def test_prototype_vocabulary_is_marked_non_canonical(self) -> None:
        """RULEBOOK §5 leaves the statistics unfinalised, so this must not be canon."""
        self.assertIn("non-canonical", CANONICALITY_NOTE)
        source = (ROOT / "src" / "tags" / "model.py").read_text(encoding="utf-8")
        self.assertIn("NOT CANON", source)
        # The prototype vocabulary must not have been written into the shared canon.
        canon = (ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8")
        for name in ("SOC", "WIL", "NET"):
            with self.subTest(attribute=name):
                self.assertNotIn(f'"{name}"', canon)

    def test_human_attribute_range_is_minus_three_to_plus_three(self) -> None:
        self.assertEqual(attribute_tag("FIT", 3).rating, 3)
        self.assertEqual(attribute_tag("FIT", -3).rating, -3)
        # Beyond +3 is explicitly available for transhuman capability.
        self.assertEqual(attribute_tag("CYB", 7).rating, 7)

    def test_zero_rating_non_attribute_tag_is_refused(self) -> None:
        """A zero tag is bookkeeping with no effect; omit it instead."""
        with self.assertRaises(TagError):
            Tag("Nothing", 0, Category.SKILL, System.PHYSICAL, ("combat",))

    def test_attribute_tag_without_system_is_refused(self) -> None:
        with self.assertRaises(TagError):
            Tag("REF", 2, Category.ATTRIBUTE, None, ("physical",))

    def test_unknown_attribute_name_is_refused(self) -> None:
        with self.assertRaises(TagError):
            attribute_tag("LUCK", 2)

    def test_tag_round_trips_through_serialisation(self) -> None:
        original = Tag("Mesh intrusion", 2, Category.SKILL, System.CYBERNETIC,
                       ("network_access", "security"), Source.CHARACTER, "fixture")
        restored = Tag.from_dict(original.as_dict())
        self.assertEqual(restored, original)

    def test_entity_round_trips_including_presence(self) -> None:
        entity = sample_entities()["fixture:utility-ai"]
        restored = Entity(
            entity_id=entity.entity_id,
            name=entity.name,
            tags=tuple(Tag.from_dict(t.as_dict()) for t in entity.tags),
            presence=SystemPresence.from_dict(entity.presence.as_dict()),
            flags=entity.flags,
        )
        self.assertEqual(restored.presence.absent(), (System.PHYSICAL, System.PSYCHIC))
        self.assertEqual(restored.attributes(), entity.attributes())


class StackingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = sample_entities()["fixture:runner"]

    def test_attribute_contributes_inside_the_same_stack(self) -> None:
        """The issue's worked example: REF + skill + cyberware + condition."""
        stack = build_stack(
            self.runner, action="shoot", facets=("ranged", "combat"),
            system=System.PHYSICAL, attribute="REF",
        )
        counted = {tag.name: tag.rating for tag in stack.counted}
        self.assertEqual(counted.get("REF"), 2)
        self.assertEqual(counted.get("Pistol"), 2)
        self.assertEqual(counted.get("Smartlink"), 1)
        self.assertEqual(stack.total, 5)

    def test_the_nominated_attribute_is_the_one_that_counts(self) -> None:
        """RULEBOOK §4: the GM selects the attribute that fits the action."""
        ref = build_stack(self.runner, action="shoot", facets=("ranged",),
                          system=System.PHYSICAL, attribute="REF")
        fit = build_stack(self.runner, action="shoot", facets=("ranged",),
                          system=System.PHYSICAL, attribute="FIT")
        self.assertIn("REF", [t.name for t in ref.counted])
        self.assertNotIn("REF", [t.name for t in fit.counted])
        self.assertIn("FIT", [t.name for t in fit.counted])

    def test_irrelevant_tags_are_excluded_and_the_reason_is_recorded(self) -> None:
        stack = build_stack(self.runner, action="shoot", facets=("ranged", "combat"),
                            system=System.PHYSICAL, attribute="REF")
        excluded = {item.tag.name: item.reason for item in stack.excluded}
        self.assertIn("Parkour", excluded)
        self.assertIn("scope does not intersect", excluded["Parkour"])
        # Transparency: everything not counted is accounted for.
        self.assertEqual(
            len(stack.counted) + len(stack.excluded), len(self.runner.tags)
        )

    def test_synonymous_tags_do_not_stack(self) -> None:
        """The issue's anti-abuse rule: one cause per category."""
        entity = Entity(
            entity_id="fixture:synonym",
            tags=(
                attribute_tag("REF", 1),
                Tag("Pistol", 2, Category.SKILL, System.PHYSICAL, ("ranged",)),
                Tag("Handguns", 2, Category.SKILL, System.PHYSICAL, ("ranged",)),
            ),
        )
        stack = build_stack(entity, action="shoot", facets=("ranged",),
                            system=System.PHYSICAL, attribute="REF")
        skills = [t for t in stack.counted if t.category is Category.SKILL]
        self.assertEqual(len(skills), 1, "two skills must not both pay out")
        self.assertTrue(any("already contributes" in item.reason for item in stack.excluded))

    def test_duplicate_name_collapses_to_the_strongest(self) -> None:
        entity = Entity(
            entity_id="fixture:dupe",
            tags=(
                Tag("Neural interface", 1, Category.CYBERWARE, System.CYBERNETIC, ("interface",)),
                Tag("Neural interface", 3, Category.CYBERWARE, System.CYBERNETIC, ("interface",)),
            ),
        )
        stack = build_stack(entity, action="jack in", facets=("interface",),
                            system=System.CYBERNETIC)
        self.assertEqual([t.rating for t in stack.counted], [3])
        self.assertTrue(any("duplicate name" in item.reason for item in stack.excluded))

    def test_stack_cap_is_enforced_and_is_a_prototype_parameter(self) -> None:
        """The cap applies after the one-cause-per-category rule, so the fixture needs
        distinct categories -- ten skill tags would already collapse to one."""
        categories = (
            Category.SKILL, Category.SPECIALIZATION, Category.GEAR, Category.CYBERWARE,
            Category.BIOMOD, Category.CONDITION, Category.ADVANTAGE, Category.BACKGROUND,
            Category.PROFESSION, Category.REPUTATION,
        )
        entity = Entity(
            entity_id="fixture:many",
            tags=tuple(
                Tag(f"Tag {index}", 1, category, System.PHYSICAL, ("combat",))
                for index, category in enumerate(categories)
            ),
        )
        capped = build_stack(entity, action="fight", facets=("combat",),
                             system=System.PHYSICAL, cap=3)
        self.assertEqual(len(capped.counted), 3)
        self.assertTrue(any("stack cap" in item.reason for item in capped.excluded))
        # The cap is injectable, because the issue leaves it open.
        uncapped = build_stack(entity, action="fight", facets=("combat",),
                               system=System.PHYSICAL, cap=len(categories))
        self.assertEqual(len(uncapped.counted), len(categories))
        # ...and the default cap is a prototype value, not canon.
        self.assertEqual(STACK_CAP_DEFAULT, 6)

    def test_negative_tags_subtract(self) -> None:
        entity = Entity(
            entity_id="fixture:hurt",
            tags=(
                attribute_tag("FIT", 2),
                Tag("Broken arm", -2, Category.INJURY, System.PHYSICAL, ("force",)),
            ),
        )
        stack = build_stack(entity, action="lift", facets=("force",),
                            system=System.PHYSICAL, attribute="FIT")
        self.assertEqual(stack.total, 0)

    def test_no_facets_yields_an_empty_stack(self) -> None:
        stack = build_stack(self.runner, action="vague", facets=(), system=System.PHYSICAL)
        self.assertEqual(stack.counted, ())
        self.assertEqual(stack.total, 0)


class ResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.entities = sample_entities()

    def test_one_resolver_serves_all_five_domains(self) -> None:
        """Issue item 6: the same resolver on combat, social, hacking, investigation, psionics."""
        cases = (
            ("fixture:runner", "shoot", ("ranged", "combat"), System.PHYSICAL, "REF"),
            ("fixture:negotiator", "sway", ("persuasion", "negotiation"), System.SOCIAL, "CHA"),
            ("fixture:cyborg", "intrude", ("network_access", "hacking"), System.CYBERNETIC, "NET"),
            ("fixture:researcher", "investigate", ("investigation", "analysis"), System.PSYCHIC, "INT"),
            ("fixture:psion", "read", ("mind", "detection"), System.PSYCHIC, "PSY"),
        )
        for entity_id, action, facets, system, attribute in cases:
            with self.subTest(domain=action):
                result = resolve_action(
                    self.entities[entity_id], action=action, facets=facets,
                    system=system, attribute=attribute, difficulty=10, dice_total=7,
                )
                self.assertIs(result.outcome, Outcome.RESOLVED)
                self.assertIsNotNone(result.check)

    def test_resolution_matches_the_shared_rules_layer(self) -> None:
        """The prototype must not fork the 2d6 engine (RULEBOOK §4)."""
        result = resolve_action(
            self.entities["fixture:runner"], action="shoot", facets=("ranged", "combat"),
            system=System.PHYSICAL, attribute="REF", difficulty=10, dice_total=7,
        )
        expected = resolve_check(attribute_modifier=result.stack.total, target=10, dice_total=7)
        self.assertEqual(result.check.total, expected.total)
        self.assertEqual(result.check.success, expected.success)

    def test_difficulty_is_required_not_defaulted(self) -> None:
        """Assigning difficulty is a tabletop decision; the prototype must not guess."""
        result = resolve_action(
            self.entities["fixture:runner"], action="shoot", facets=("ranged",),
            system=System.PHYSICAL, attribute="REF", difficulty=None, dice_total=7,
        )
        self.assertIsNot(result.outcome, Outcome.RESOLVED)
        self.assertIn("difficulty", result.reason)
        self.assertIsNone(result.check)

    def test_no_facets_is_unresolved_rather_than_guessed(self) -> None:
        result = resolve_action(
            self.entities["fixture:runner"], action="vague", facets=(),
            system=System.PHYSICAL, difficulty=10, dice_total=7,
        )
        self.assertIs(result.outcome, Outcome.UNRESOLVED_NO_FACETS)

    def test_the_mechanical_result_is_flagged_as_fixed_for_the_narrative_layer(self) -> None:
        result = resolve_action(
            self.entities["fixture:runner"], action="shoot", facets=("ranged",),
            system=System.PHYSICAL, attribute="REF", difficulty=10, dice_total=7,
        )
        self.assertIn("may not change this number", result.narrative_hint)

    def test_result_is_serialisable_for_simulation_state(self) -> None:
        result = resolve_action(
            self.entities["fixture:cyborg"], action="intrude", facets=("network_access",),
            system=System.CYBERNETIC, attribute="NET", difficulty=10, dice_total=7,
        )
        payload = result.as_dict()
        self.assertEqual(payload["outcome"], "RESOLVED")
        self.assertIn("stack", payload)
        self.assertIn("check", payload)


class AbsentLayerTests(unittest.TestCase):
    """Issue item 15. An absent layer is not a low attribute."""

    def setUp(self) -> None:
        self.entities = sample_entities()

    def test_non_conscious_ai_has_no_psychic_system(self) -> None:
        entity = self.entities["fixture:utility-ai"]
        self.assertFalse(entity.presence.has(System.PSYCHIC))
        result = resolve_action(entity, action="empathise", facets=("mind",),
                                system=System.PSYCHIC, difficulty=10, dice_total=7)
        self.assertIs(result.outcome, Outcome.UNRESOLVED_ABSENT_SYSTEM)
        self.assertIsNone(result.check, "an absent layer must not be rolled at a penalty")

    def test_noetic_entity_has_no_physical_system(self) -> None:
        result = resolve_action(
            self.entities["fixture:noetic"], action="punch", facets=("combat",),
            system=System.PHYSICAL, difficulty=10, dice_total=7,
        )
        self.assertIs(result.outcome, Outcome.UNRESOLVED_ABSENT_SYSTEM)

    def test_vr_agent_has_no_direct_physical_presence(self) -> None:
        result = resolve_action(
            self.entities["fixture:vr-agent"], action="lift", facets=("force",),
            system=System.PHYSICAL, difficulty=10, dice_total=7,
        )
        self.assertIs(result.outcome, Outcome.UNRESOLVED_ABSENT_SYSTEM)

    def test_absent_layer_differs_from_a_low_score(self) -> None:
        """The distinction the issue draws, asserted directly."""
        absent = resolve_action(
            self.entities["fixture:noetic"], action="punch", facets=("combat",),
            system=System.PHYSICAL, difficulty=6, dice_total=12,
        )
        # Even with a perfect roll and the easiest difficulty, presence is required.
        self.assertIs(absent.outcome, Outcome.UNRESOLVED_ABSENT_SYSTEM)
        self.assertIsNone(absent.success)

    def test_an_entity_can_still_act_in_the_systems_it_has(self) -> None:
        entity = self.entities["fixture:vr-agent"]
        social = resolve_action(entity, action="persuade", facets=("social",),
                                system=System.SOCIAL, attribute="CHA", difficulty=8, dice_total=7)
        cyber = resolve_action(entity, action="manipulate", facets=("network_access",),
                               system=System.CYBERNETIC, attribute="CYB", difficulty=10, dice_total=7)
        self.assertIs(social.outcome, Outcome.RESOLVED)
        self.assertIs(cyber.outcome, Outcome.RESOLVED)


class SampleEntityTests(unittest.TestCase):
    def test_sample_set_covers_ordinary_and_absent_layer_cases(self) -> None:
        entities = sample_entities()
        ordinary = [e for e in entities.values() if not e.presence.absent()]
        absent = [e for e in entities.values() if e.presence.absent()]
        self.assertGreaterEqual(len(ordinary), 3, "issue asks for 3-5 sample characters")
        self.assertGreaterEqual(len(absent), 3, "issue item 15 asks for absent-layer cases")

    def test_all_sample_ids_are_non_canonical_fixtures(self) -> None:
        """Prototype material must not be mistakable for canon (AGENTS.md §1)."""
        for entity_id in sample_entities():
            with self.subTest(entity=entity_id):
                self.assertTrue(entity_id.startswith("fixture:"), entity_id)

    def test_attribute_tags_read_out_of_the_tag_list(self) -> None:
        runner = sample_entities()["fixture:runner"]
        attributes = runner.attributes()
        self.assertEqual(attributes["REF"], 2)
        self.assertEqual(attributes["CHA"], -1)
        # They are tags, so they are in the same collection as everything else.
        self.assertEqual(len(runner.attribute_tags()) + len(runner.non_attribute_tags()),
                         len(runner.tags))

    def test_narrative_flags_are_not_dice_modifiers(self) -> None:
        """The issue: flags tell the GM what matters, they are not skill bonuses."""
        negotiator = sample_entities()["fixture:negotiator"]
        self.assertTrue(negotiator.flags)
        for flag in negotiator.flags:
            with self.subTest(flag=flag):
                self.assertIsNone(negotiator.tag(flag))

    def test_cross_system_tags_can_contribute_to_one_action(self) -> None:
        """Physical -> Cybernetic: a physical action helped by a cybernetic tag."""
        runner = sample_entities()["fixture:runner"]
        stack = build_stack(runner, action="aim", facets=("ranged", "aim"),
                            system=System.PHYSICAL, attribute="REF")
        categories = {tag.category for tag in stack.counted}
        self.assertIn(Category.SKILL, categories)
        self.assertIn(Category.CYBERWARE, categories, "a cybernetic tag applies to a physical action")


class CrossLayerTests(unittest.TestCase):
    """Issue item 14: one event propagates through all four layers, distinct but entangled."""

    def test_one_event_yields_a_distinct_outcome_per_layer_from_one_engine(self) -> None:
        entity = sample_entities()["fixture:negotiator"]
        layers = (
            (System.PHYSICAL, ("combat", "force"), "FIT", "absorb the wound"),
            (System.PSYCHIC, ("resolve", "fear"), "WIL", "hold nerve"),
            (System.SOCIAL, ("negotiation",), "CHA", "keep respect"),
            (System.CYBERNETIC, ("interface",), "CYB", "check telemetry"),
        )
        results = {}
        for system, facets, attribute, action in layers:
            with self.subTest(layer=system.value):
                result = resolve_action(
                    entity, action=action, facets=facets, system=system,
                    attribute=attribute, difficulty=10, dice_total=7,
                )
                self.assertIs(result.outcome, Outcome.RESOLVED)
                results[system] = result
        # Distinct but entangled: different stacks, same entity, one engine.
        self.assertEqual(len({r.stack.total for r in results.values()}), len(layers))
        self.assertNotEqual(results[System.PHYSICAL].success, results[System.SOCIAL].success)

    def test_an_absent_layer_propagates_as_absence_not_as_a_result(self) -> None:
        entity = sample_entities()["fixture:utility-ai"]
        result = resolve_action(entity, action="feel fear", facets=("fear",),
                                system=System.PSYCHIC, difficulty=10, dice_total=7)
        self.assertIs(result.outcome, Outcome.UNRESOLVED_ABSENT_SYSTEM)
        self.assertIsNone(result.success, "there is no psychic outcome to report")


if __name__ == "__main__":
    unittest.main()
