"""Issue #51 prototype tests: the unified tag system, on the issue #111 core.

#51's "First implementation target" items 1-6 are code, so they are tested as
behaviour rather than guarded as prose:

1. one unified tag data structure, ``category="attribute"`` included;
2. the ordinary-human attribute-tag range -- now the 1..10 STAT scale (issue #111);
3. applicability and stacking;
4. **one** generic resolver -- and critically, it is the *existing canonical* one;
5. sample characters;
6. the same resolver on combat, social, hacking, investigation and psionics.

The property worth protecting above all: **tags feed the canonical d10 engine, they
do not fork a second one**. A test asserts that composition calls `rules.resolve_check`
and that no dice are rolled inside the tag module.

Issue #111 replaced the retired -3..+3 attribute band / 0..4 skill levels and the 2d6
kernel with ``STAT + Skill + 1d10 >= DV`` (both ratings 1..10). It also retired the
kernel's ``attempted`` / ``unskilled_modifier`` fields and left an *unskilled*
procedure undefined. The assertions below are ported to that kernel: they assert the
current canonical behaviour instead of retired fields, rather than inventing an
unskilled rule.

Fixture characters only; no setting material is created or asserted.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import (  # noqa: E402
    FOUR_SYSTEMS,
    HUMAN_ATTRIBUTE_MAX,
    HUMAN_ATTRIBUTE_MIN,
    PROTOTYPE_ATTRIBUTE_SYSTEMS,
    PROTOTYPE_MAX_CONTRIBUTING_TAGS,
    RESOLVED,
    UNRESOLVED_ABSENT_SYSTEM,
    AbsentSystemResult,
    CheckResult,
    SystemPresence,
    Tag,
    TagError,
    TranshumanTag,
    build_stack,
    compose_check,
    resolve_check,
    resolve_tag_check,
)
from rules.tag_fixtures import SAMPLE_CHARACTERS, TRANSHUMAN_SAMPLE  # noqa: E402


def _attr(name: str, rating: int) -> Tag:
    return Tag(name=name, rating=rating, system=PROTOTYPE_ATTRIBUTE_SYSTEMS[name],
               category="attribute")


def _skill(name: str, rating: int, system: str, scope: tuple[str, ...], category: str = "skill") -> Tag:
    return Tag(name=name, rating=rating, system=system, category=category, scope=scope)


class OneTagTypeTests(unittest.TestCase):
    """#51 principle 1 and 2: attributes are tags, and there is one tag engine."""

    def test_an_attribute_is_a_tag_with_the_attribute_category(self) -> None:
        tag = _attr("FIT", 6)
        self.assertIsInstance(tag, Tag)
        self.assertTrue(tag.is_attribute)
        self.assertEqual(tag.category, "attribute")

    def test_other_categories_are_the_same_type(self) -> None:
        """Gear, condition and reputation tags are Tags too, not separate systems."""
        for category in ("skill", "gear", "condition", "reputation", "cyberware"):
            with self.subTest(category=category):
                tag = _skill("X", 5, "physical", ("y",), category=category)
                self.assertIsInstance(tag, Tag)
                self.assertFalse(tag.is_attribute)

    def test_systems_are_the_four_canonical_groups(self) -> None:
        for system in ("physical", "social", "psychic", "cybernetic"):
            with self.subTest(system=system):
                self.assertEqual(_skill("X", 5, system, ("y",)).system, system)

    def test_unknown_system_is_rejected(self) -> None:
        with self.assertRaises(TagError):
            _skill("X", 5, "spiritual", ("y",))

    def test_empty_name_is_rejected(self) -> None:
        with self.assertRaises(TagError):
            _skill("", 5, "physical", ("y",))


class AttributeRangeTests(unittest.TestCase):
    """#51 principle 3: ordinary-human attribute tags run 1..10 (issue #111)."""

    def test_the_whole_human_range_is_accepted(self) -> None:
        for rating in range(HUMAN_ATTRIBUTE_MIN, HUMAN_ATTRIBUTE_MAX + 1):
            with self.subTest(rating=rating):
                self.assertEqual(_attr("FIT", rating).rating, rating)

    def test_beyond_the_human_range_requires_the_transhuman_type(self) -> None:
        """The ceiling must stay verifiable, not quietly widened."""
        with self.assertRaises(TagError):
            _attr("CYB", 11)
        self.assertEqual(TranshumanTag("CYB", 11, "cybernetic", category="attribute").rating, 11)

    def test_transhuman_tag_must_actually_exceed_the_human_range(self) -> None:
        with self.assertRaises(TagError):
            TranshumanTag("CYB", 8, "cybernetic", category="attribute")

    def test_the_ceiling_is_the_top_of_the_ordinary_human_scale(self) -> None:
        """The 1..10 band is pinned by both ends, and 0 is *not* a valid rating."""
        self.assertEqual(_attr("INT", HUMAN_ATTRIBUTE_MIN).rating, 1)
        self.assertEqual(_attr("INT", HUMAN_ATTRIBUTE_MAX).rating, 10)
        with self.assertRaises(TagError):
            _attr("INT", 0)


class ApplicabilityTests(unittest.TestCase):
    """#51 principle 6 (defined enough for code) and 7 (fiction still matters)."""

    def test_attribute_tags_are_always_applicable(self) -> None:
        """#51: attributes are 'always present; broad rather than situational'."""
        tag = _attr("REF", 7)
        for scopes in ((), ("combat",), ("negotiation",)):
            with self.subTest(scopes=scopes):
                self.assertTrue(tag.applies_to(scopes))

    def test_a_scope_tag_applies_only_to_its_scopes(self) -> None:
        pistol = _skill("Pistol", 7, "physical", ("combat", "firearms"))
        self.assertTrue(pistol.applies_to(("combat",)))
        self.assertFalse(pistol.applies_to(("negotiation",)))

    def test_an_unscoped_situational_tag_never_applies(self) -> None:
        """Otherwise an unscoped tag would help everything, which #51 forbids."""
        tag = _skill("Vague", 7, "physical", ())
        self.assertFalse(tag.applies_to(("combat",)))

    def test_applicability_is_case_insensitive(self) -> None:
        tag = _skill("Pistol", 7, "physical", ("Combat",))
        self.assertTrue(tag.applies_to(("COMBAT",)))


class StackingTests(unittest.TestCase):
    """#51: distinct relevant tags stack, with explicit anti-abuse rules."""

    def test_distinct_relevant_tags_stack(self) -> None:
        stack = build_stack(
            [_attr("REF", 7), _skill("Pistol", 8, "physical", ("combat",)),
             _skill("Smartlink", 6, "cybernetic", ("combat",), category="gear")],
            action_scopes=("combat",),
        )
        # Every contributed tag is summed in the audit total (attribute + situational).
        self.assertEqual(stack.total, 7 + 8 + 6)

    def test_duplicate_tags_do_not_stack(self) -> None:
        """Same name + system is one cause, whatever its source (#51)."""
        stack = build_stack(
            [_skill("Pistol", 7, "physical", ("combat",), category="skill"),
             _skill("Pistol", 7, "physical", ("combat",), category="gear")],
            action_scopes=("combat",),
        )
        pistols = [t for t in stack.contributed if t.name == "Pistol"]
        self.assertEqual(len(pistols), 1, "the same cause must not be counted twice")
        self.assertTrue(any("duplicate" in reason for _, reason in stack.rejected))

    def test_the_stronger_duplicate_survives(self) -> None:
        stack = build_stack(
            [_skill("Pistol", 6, "physical", ("combat",), category="skill"),
             _skill("Pistol", 9, "physical", ("combat",), category="gear")],
            action_scopes=("combat",),
        )
        pistols = [t for t in stack.contributed if t.name == "Pistol"]
        self.assertEqual(pistols[0].rating, 9)

    def test_irrelevant_tags_are_rejected_with_a_reason(self) -> None:
        stack = build_stack(
            [_attr("REF", 7), _skill("Pistol", 7, "physical", ("combat",))],
            action_scopes=("negotiation",),
        )
        self.assertEqual(len(stack.contributed), 1)
        self.assertTrue(any("not relevant" in reason for _, reason in stack.rejected))

    def test_contributing_tags_are_capped(self) -> None:
        """#51 lists a maximum as an open question; the mechanism must exist."""
        many = [_skill(f"S{i}", 7, "physical", ("combat",)) for i in range(10)]
        stack = build_stack([_attr("REF", 7), *many], action_scopes=("combat",))
        situational = [t for t in stack.contributed if not t.is_attribute]
        self.assertEqual(len(situational), PROTOTYPE_MAX_CONTRIBUTING_TAGS)
        self.assertTrue(stack.capped, "dropped tags must be reported, not hidden")

    def test_the_cap_is_deterministic_regardless_of_input_order(self) -> None:
        a = _skill("Alpha", 6, "physical", ("combat",))
        b = _skill("Beta", 9, "physical", ("combat",))
        c = _skill("Gamma", 5, "physical", ("combat",))
        first = build_stack([a, b, c], action_scopes=("combat",), max_contributing=2)
        second = build_stack([c, b, a], action_scopes=("combat",), max_contributing=2)
        self.assertEqual(
            [t.name for t in first.contributed], [t.name for t in second.contributed]
        )

    def test_attribute_tags_are_never_capped(self) -> None:
        """Dropping an attribute would silently change the STAT."""
        tag = _skill("Filler", 6, "physical", ("combat",))
        stack = build_stack(
            [_attr("FIT", 5), _attr("REF", 7), _attr("INT", 6), _attr("CHA", 4),
             _attr("CYB", 6), _attr("PSY", 5), tag],
            action_scopes=("combat",), max_contributing=0,
        )
        self.assertEqual(len([t for t in stack.contributed if t.is_attribute]), 6)

    def test_stack_explanation_is_human_readable(self) -> None:
        stack = build_stack([_attr("REF", 7), _skill("Pistol", 8, "physical", ("combat",))],
                            action_scopes=("combat",))
        joined = "\n".join(stack.explain())
        self.assertIn("REF", joined)
        self.assertIn("Pistol", joined)


class CanonicalEngineCompositionTests(unittest.TestCase):
    """The load-bearing property: tags feed the canonical engine, not a second one."""

    def test_composition_produces_canonical_check_arguments(self) -> None:
        composed = compose_check(
            [_attr("REF", 7), _skill("Pistol", 8, "physical", ("combat",)),
             _skill("Smartlink", 6, "cybernetic", ("combat",), category="gear")],
            attribute="REF", skill="Pistol", action_scopes=("combat",),
        )
        self.assertEqual(composed.attribute_modifier, 7)
        self.assertEqual(composed.skill_level, 8)
        self.assertEqual(composed.extra_modifiers, (6,))

    def test_the_tag_module_does_not_roll_its_own_dice(self) -> None:
        """#51 principle 9: the deterministic core resolves; one engine, one mechanic."""
        source = (ROOT / "src" / "rules" / "tags.py").read_text(encoding="utf-8")
        for dice in ("randint", "random", "roll_2d6(", "roll_3d6("):
            with self.subTest(dice=dice):
                self.assertNotIn(
                    dice, source,
                    "the tag module must delegate dice to the canonical resolver",
                )

    def test_resolution_equals_the_canonical_resolve_check(self) -> None:
        """Given the same inputs, the tag path and the direct path agree exactly."""
        tags = [_attr("REF", 7), _skill("Pistol", 8, "physical", ("combat",)),
                _skill("Smartlink", 6, "cybernetic", ("combat",), category="gear")]
        result, composed = resolve_tag_check(
            tags, attribute="REF", skill="Pistol", difficulty=15,
            action_scopes=("combat",), dice_total=8,
        )
        direct = resolve_check(
            stat=composed.attribute_modifier,
            target=15,
            skill=composed.skill_level,
            die=8,
        )
        self.assertEqual(result, direct)

    def test_a_missing_attribute_tag_is_an_error_not_a_silent_zero(self) -> None:
        """A silent 0 would hide a malformed character."""
        with self.assertRaises(TagError):
            compose_check([_skill("Pistol", 7, "physical", ("combat",))],
                          attribute="REF", skill="Pistol", action_scopes=("combat",))

    def test_skill_rating_is_the_canonical_skill_directly(self) -> None:
        """A trained Skill is 1..10, the same scale as a tag, so there is no clamp.

        The retired prototype clamped a tag's magnitude to 0..4; issue #111 makes the
        skill tag's rating the canonical Skill rating outright.
        """
        tags = [_attr("CYB", 6), _skill("Mesh intrusion", 9, "cybernetic", ("hacking",))]
        composed = compose_check(tags, attribute="CYB", skill="Mesh intrusion",
                                 action_scopes=("hacking",))
        self.assertEqual(composed.skill_level, 9)
        self.assertEqual(composed.skill, 9)

    def test_an_unskilled_attempt_is_refused_not_silently_resolved(self) -> None:
        """Issue #111 defines no unskilled procedure.

        The retired kernel rolled an unskilled attempt at a -1 penalty and reported
        ``attempted`` / ``unskilled_modifier`` on the result. Neither field exists on
        the #111 ``CheckResult``, and such an attempt must be refused explicitly rather
        than resolved at an invented rating.
        """
        # A caller that declares it has no trained Skill for the action is refused.
        with self.assertRaises(TagError):
            resolve_tag_check(
                [_attr("REF", 7)], attribute="REF", difficulty=10, action_scopes=(),
                unskilled=True, dice_total=7,
            )
        # Naming a skill that no contributing tag supplies is likewise refused.
        with self.assertRaises(TagError):
            resolve_tag_check(
                [_attr("REF", 7)], attribute="REF", difficulty=10, skill="Pistol",
                action_scopes=("combat",), dice_total=7,
            )
        # And the canonical result itself carries no retired unskilled surface.
        result, _ = resolve_tag_check(
            [_attr("REF", 7), _skill("Pistol", 7, "physical", ("combat",))],
            attribute="REF", difficulty=10, skill="Pistol", action_scopes=("combat",),
            dice_total=7,
        )
        self.assertFalse(hasattr(result, "attempted"))
        self.assertFalse(hasattr(result, "unskilled_modifier"))


class SampleCharacterTests(unittest.TestCase):
    """#51 item 5, and item 6: the same resolver across five domains."""

    def test_between_three_and_five_examples_exist(self) -> None:
        self.assertGreaterEqual(len(SAMPLE_CHARACTERS), 3)
        self.assertLessEqual(len(SAMPLE_CHARACTERS), 5)

    def test_every_character_has_all_six_prototype_attributes(self) -> None:
        for name, tags in SAMPLE_CHARACTERS.items():
            with self.subTest(character=name):
                attributes = {t.name for t in tags if t.is_attribute}
                self.assertEqual(attributes, set(PROTOTYPE_ATTRIBUTE_SYSTEMS))

    def test_characters_are_marked_as_fixtures(self) -> None:
        """Nothing here may be mistaken for author-specified setting material."""
        for name in SAMPLE_CHARACTERS:
            with self.subTest(character=name):
                self.assertTrue(name.startswith("fixture:"))
        for tags in SAMPLE_CHARACTERS.values():
            for tag in tags:
                self.assertEqual(tag.source, "fixture", tag.name)

    def test_characters_span_the_four_systems(self) -> None:
        systems = {t.system for tags in SAMPLE_CHARACTERS.values() for t in tags}
        self.assertEqual(systems, {"physical", "social", "psychic", "cybernetic"})

    def test_transhuman_sample_exceeds_the_human_ceiling(self) -> None:
        cyber = [t for t in TRANSHUMAN_SAMPLE if t.is_attribute and t.name == "CYB"]
        self.assertEqual(len(cyber), 1)
        self.assertGreater(cyber[0].rating, HUMAN_ATTRIBUTE_MAX)

    # -- item 6: the same resolver on five domains -------------------------- #

    def test_combat_check_resolves(self) -> None:
        result, _ = resolve_tag_check(
            SAMPLE_CHARACTERS["fixture:street-fixer"], attribute="REF", difficulty=10,
            skill="Pistol", action_scopes=("combat", "firearms"), dice_total=7,
        )
        self.assertTrue(result.success)

    def test_social_check_resolves(self) -> None:
        result, composed = resolve_tag_check(
            SAMPLE_CHARACTERS["fixture:investigative-journalist"], attribute="CHA",
            difficulty=8, skill="Investigative journalist",
            action_scopes=("investigation", "interviews"), dice_total=6,
        )
        self.assertTrue(result.success)
        self.assertEqual(composed.attribute_modifier, 6)

    def test_hacking_check_resolves(self) -> None:
        result, _ = resolve_tag_check(
            SAMPLE_CHARACTERS["fixture:mesh-intruder"], attribute="CYB", difficulty=12,
            skill="Mesh intrusion", action_scopes=("hacking", "network_access"), dice_total=9,
        )
        self.assertTrue(result.success)

    def test_investigation_check_resolves(self) -> None:
        result, _ = resolve_tag_check(
            SAMPLE_CHARACTERS["fixture:investigative-journalist"], attribute="INT",
            difficulty=10, skill="Pattern recognition", action_scopes=("investigation",),
            dice_total=8,
        )
        self.assertTrue(result.success)

    def test_psionics_check_resolves(self) -> None:
        result, _ = resolve_tag_check(
            SAMPLE_CHARACTERS["fixture:noosphere-sensitive"], attribute="PSY", difficulty=10,
            skill="Telepathy", action_scopes=("psionics",), dice_total=7,
        )
        self.assertTrue(result.success)

    def test_a_condition_tag_is_recorded_but_not_folded_into_the_total(self) -> None:
        """A negative tag must appear in the audit, not silently vanish.

        Issue #111 §10.3 leaves the situational-modifier procedure undefined, so the
        condition tag is recorded in the stack and in ``extra_modifiers`` but does not
        change the canonical total: the tag prototype must not invent a modifier rule
        the core rules declined to state.
        """
        result, composed = resolve_tag_check(
            SAMPLE_CHARACTERS["fixture:mesh-intruder"], attribute="CYB", difficulty=14,
            skill="Mesh intrusion", action_scopes=("security",), dice_total=9,
        )
        names = {tag.name for tag in composed.stack.contributed}
        self.assertIn("Compromised firmware", names)
        # It is carried as an audit modifier...
        self.assertEqual(composed.extra_modifiers, (3,))
        # ...but the canonical total is STAT + Skill + 1d10 only.
        self.assertEqual(result.total, 9 + 9 + 9)

    def test_the_same_resolver_serves_every_domain(self) -> None:
        """#51 principle 8: one mechanic across genres."""
        source = (ROOT / "src" / "rules" / "tags.py").read_text(encoding="utf-8")
        self.assertIn("resolve_check", source)
        for distinct_engine in ("def resolve_combat", "def resolve_hacking", "def resolve_social"):
            with self.subTest(engine=distinct_engine):
                self.assertNotIn(distinct_engine, source)

    def test_resolution_is_deterministic_for_a_fixed_seed(self) -> None:
        class FixedRng:
            def randint(self, a: int, b: int) -> int:
                return 3

        first, _ = resolve_tag_check(
            SAMPLE_CHARACTERS["fixture:street-fixer"], attribute="REF", difficulty=10,
            skill="Pistol", action_scopes=("combat",), rng=FixedRng(),
        )
        second, _ = resolve_tag_check(
            SAMPLE_CHARACTERS["fixture:street-fixer"], attribute="REF", difficulty=10,
            skill="Pistol", action_scopes=("combat",), rng=FixedRng(),
        )
        self.assertEqual(first, second)
        self.assertIsInstance(first, CheckResult)


class AntiInventionTests(unittest.TestCase):
    """#51 lists many mechanics as open questions; the prototype must not settle them."""

    def test_the_module_states_it_is_a_prototype(self) -> None:
        source = (ROOT / "src" / "rules" / "tags.py").read_text(encoding="utf-8")
        self.assertIn("This module defines no canon", source)

    def test_the_attribute_vocabulary_is_marked_non_canonical(self) -> None:
        source = (ROOT / "src" / "rules" / "tags.py").read_text(encoding="utf-8")
        self.assertIn("Prototype vocabulary — not canon", source)


class AbsentSystemTests(unittest.TestCase):
    """RULEBOOK §5.2: a system can be absent, and absence is not a low score.

    The reconciliation made this canonical in prose. These tests are the mechanism
    behind that sentence: without them the rulebook required something no code did.
    """

    def test_presence_defaults_to_all_four_systems(self) -> None:
        presence = SystemPresence()
        for system in FOUR_SYSTEMS:
            with self.subTest(system=system):
                self.assertTrue(presence.has(system))
        self.assertEqual(presence.absent(), ())

    def test_absent_systems_helper_names_the_rulebook_cases(self) -> None:
        # A non-conscious AI: no meaningful Psychic participation.
        self.assertEqual(SystemPresence.absent_systems("psychic").absent(), ("psychic",))
        # A disembodied/noetic entity: no meaningful Physical participation.
        self.assertEqual(SystemPresence.absent_systems("physical").absent(), ("physical",))
        # An AI operating only in VR: Social and Cybernetic without local Physical.
        vr = SystemPresence.absent_systems("physical")
        self.assertTrue(vr.has("social"))
        self.assertTrue(vr.has("cybernetic"))
        self.assertFalse(vr.has("physical"))

    def test_presence_round_trips_through_a_dict(self) -> None:
        presence = SystemPresence.absent_systems("psychic", "physical")
        self.assertEqual(SystemPresence.from_dict(presence.as_dict()), presence)

    def test_unknown_system_in_presence_is_rejected(self) -> None:
        with self.assertRaises(TagError):
            SystemPresence({"magical": True})
        with self.assertRaises(TagError):
            SystemPresence().has("magical")

    def test_absent_system_refuses_instead_of_rolling_at_a_penalty(self) -> None:
        """Rolling at a penalty would assert a capability the entity does not have."""
        ai = SystemPresence.absent_systems("psychic")
        result, composed = resolve_tag_check(
            [_attr("PSY", 5)],
            attribute="PSY", difficulty=10, presence=ai, dice_total=7,
        )
        self.assertIsInstance(result, AbsentSystemResult)
        self.assertEqual(composed.outcome, UNRESOLVED_ABSENT_SYSTEM)
        self.assertFalse(composed.resolved)
        self.assertEqual(composed.absent_system, "psychic")

    def test_a_perfect_roll_cannot_override_absence(self) -> None:
        """Presence is a precondition, not a modifier."""
        noetic = SystemPresence.absent_systems("physical")
        result, composed = resolve_tag_check(
            [_attr("FIT", 1)],
            attribute="FIT", difficulty=6, presence=noetic, dice_total=12,
        )
        self.assertIsInstance(result, AbsentSystemResult)
        self.assertFalse(composed.resolved)
        self.assertFalse(hasattr(result, "success"),
                         "there is no success to read; nothing was rolled")

    def test_a_present_but_very_low_attribute_still_rolls(self) -> None:
        """The distinction §5.2 draws, asserted directly: 1 rolls, absence does not."""
        frail = SystemPresence()
        low = [_attr("FIT", 1), _skill("Climb", 1, "physical", ("movement",))]
        result, composed = resolve_tag_check(
            low, attribute="FIT", difficulty=8, skill="Climb",
            action_scopes=("movement",), presence=frail, dice_total=7,
        )
        self.assertEqual(composed.outcome, RESOLVED)
        self.assertTrue(hasattr(result, "total"))
        self.assertEqual(composed.stat, HUMAN_ATTRIBUTE_MIN,
                         "the lowest ordinary-human STAT is still a real rating, not absence")
        # ...whereas the same action for an entity with no Physical participation
        # does not resolve at all.
        absent, composed_absent = resolve_tag_check(
            low, attribute="FIT", difficulty=8, skill="Climb",
            action_scopes=("movement",),
            presence=SystemPresence.absent_systems("physical"), dice_total=7,
        )
        self.assertIsInstance(absent, AbsentSystemResult)
        self.assertEqual(composed_absent.outcome, UNRESOLVED_ABSENT_SYSTEM)

    def test_an_entity_can_still_act_in_the_systems_it_has(self) -> None:
        ai = SystemPresence.absent_systems("psychic")
        result, composed = resolve_tag_check(
            [_attr("CYB", 8), _skill("Mesh intrusion", 6, "cybernetic", ("hacking",))],
            attribute="CYB", difficulty=10, skill="Mesh intrusion",
            action_scopes=("hacking",), presence=ai, dice_total=7,
        )
        self.assertEqual(composed.outcome, RESOLVED)
        self.assertTrue(hasattr(result, "success"))

    def test_the_action_system_can_be_named_explicitly(self) -> None:
        """Useful when the attribute lives in one system but the action is in another."""
        ai = SystemPresence.absent_systems("psychic")
        result, composed = resolve_tag_check(
            [_attr("CYB", 8)],
            attribute="CYB", difficulty=10, presence=ai, system="psychic", dice_total=7,
        )
        self.assertIsInstance(result, AbsentSystemResult)
        self.assertEqual(composed.absent_system, "psychic")

    def test_presence_is_optional_so_existing_callers_are_unaffected(self) -> None:
        result, composed = resolve_tag_check(
            [_attr("REF", 7), _skill("Pistol", 7, "physical", ("combat",))],
            attribute="REF", difficulty=10, skill="Pistol",
            action_scopes=("combat",), dice_total=7,
        )
        self.assertEqual(composed.outcome, RESOLVED)
        self.assertTrue(hasattr(result, "success"))


if __name__ == "__main__":
    unittest.main()
