"""Issue #229 — the narrative layer.

The issue asks for five things; this pins each, and leans hardest on the two *measured*
safety rules, because both are exactly the kind of promise prose cannot keep:

* an aspect grants **one ladder step, once per roll** (the prototype measured four stacked
  aspects reaching 100% -- auto-success -- without the cap);
* an aspect **never produces a rating** (the "tag-only character" failure AC3 names).

Cross-links: #200 (epic), #233 (the prototype canonised here), #219/#220 (the realms this
sits on top of), #226 (investigation, untouched).
"""
from __future__ import annotations

import inspect
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "19_NARRATIVE_LAYER.md"

from src.rules import narrative_layer as nl
from src.rules import physical_combat as pc
from src.rules import social as soc


def flat(path: Path) -> str:
    """Whitespace-collapsed: the chapter hard-wraps, so phrases span line breaks."""
    return " ".join(path.read_text(encoding="utf-8").split())


def an_aspect(**kw):
    base = {
        "statement": "Owes D a favour",
        "scope": "B",
        "duration": "until the favour is repaid",
        "effect_class": nl.EffectClass.CONSEQUENCE,
        "cancellation": "repaying the favour",
    }
    base.update(kw)
    return nl.Aspect(**base)


class BoundTests(unittest.TestCase):
    """AC1/AC3 — ONE step, once per roll. The cap is load-bearing, not tidiness."""

    def test_the_step_is_one_and_cannot_be_parameterised(self) -> None:
        self.assertEqual(nl.invoke_step(), 1)
        self.assertEqual(nl.invoke_step(99), 1, "a caller cannot buy a bigger step")
        self.assertEqual(nl.invoke_step(bonus=5), 1)

    def test_the_step_function_has_no_increasable_parameter(self) -> None:
        """Structural: an edit that honoured a 'bonus' argument would change this signature.

        The function accepts and ignores `*args`/`**kwargs` on purpose (so a caller cannot
        pass a bigger invocation and be honoured). What it must never gain is a *named*
        parameter -- a named parameter is one an implementation could actually read.
        """
        named = [
            name for name, param in inspect.signature(nl.invoke_step).parameters.items()
            if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
        ]
        self.assertEqual(named, [], "invoke_step must take no honourable parameter")

    def test_one_invocation_per_roll(self) -> None:
        self.assertTrue(nl.can_invoke(0))
        self.assertFalse(nl.can_invoke(1))
        with self.assertRaises(nl.NarrativeError):
            nl.assert_can_invoke(1)

    def test_the_cap_constant_is_one(self) -> None:
        self.assertEqual(nl.MAX_INVOCATIONS_PER_ROLL, 1)

    def test_a_negative_count_is_refused(self) -> None:
        with self.assertRaises(nl.NarrativeError):
            nl.can_invoke(-1)

    def test_the_chapter_records_the_measured_justification(self) -> None:
        """The rules must be traceable to the measurement, not to taste."""
        text = flat(CHAPTER)
        self.assertIn("Invocations are capped at one per roll", text)
        self.assertIn("four stacked aspects reach exactly", text)
        self.assertIn("100%", text)

    def test_the_bound_is_arithmetic_neutral(self) -> None:
        """A ladder STEP, so the pending scale migration cannot invalidate it."""
        self.assertIn("one step on the core ladder", flat(CHAPTER))
        self.assertEqual(nl.INVOKE_STEPS, 1)


class NoRatingTests(unittest.TestCase):
    """AC3 — an aspect is never a rating; 'tag-only characters' is the named failure."""

    def test_no_effect_class_may_produce_a_rating(self) -> None:
        for effect_class in nl.EffectClass:
            with self.subTest(effect_class=effect_class):
                self.assertFalse(nl.effect_class_may_produce_a_rating(effect_class))

    def test_there_is_no_rating_member_on_the_effect_class(self) -> None:
        self.assertNotIn("RATING", {m.name for m in nl.EffectClass})

    def test_the_aspect_carries_no_numeric_field(self) -> None:
        fields = set(an_aspect().__dataclass_fields__)
        for forbidden in ("rating", "score", "value", "bonus", "stat"):
            with self.subTest(field=forbidden):
                self.assertNotIn(forbidden, fields)

    def test_there_is_no_api_that_converts_an_aspect_to_a_rating(self) -> None:
        for forbidden in ("aspect_rating", "rating_from_aspect", "stat_from_aspect", "aspect_stat"):
            with self.subTest(name=forbidden):
                self.assertFalse(hasattr(nl, forbidden))

    def test_an_unknown_effect_class_is_refused(self) -> None:
        with self.assertRaises(nl.NarrativeError):
            nl.effect_class_may_produce_a_rating("rating")


class AspectAnatomyTests(unittest.TestCase):
    """AC1 — permissions, modifiers, duration, cancellation: every part required."""

    def test_all_five_parts_are_required(self) -> None:
        for name in ("statement", "scope", "duration", "cancellation"):
            with self.subTest(part=name), self.assertRaises(nl.NarrativeError):
                an_aspect(**{name: "   "})

    def test_the_three_effect_classes_exist(self) -> None:
        self.assertEqual({c.value for c in nl.EffectClass},
                         {"permission", "modifier", "consequence"})

    def test_an_invalid_effect_class_is_refused(self) -> None:
        with self.assertRaises(nl.NarrativeError):
            an_aspect(effect_class="rating")

    def test_the_chapter_tabulates_the_anatomy(self) -> None:
        text = flat(CHAPTER)
        for part in ("**Statement**", "**Scope**", "**Duration / use condition**",
                     "**Effect class**", "**Cancellation**"):
            with self.subTest(part=part):
                self.assertIn(part, text)


class PoolTests(unittest.TestCase):
    """AC2 — narrative resources with a real cost, which cannot buy a bigger modifier."""

    def test_the_pool_is_bounded(self) -> None:
        self.assertEqual((nl.POOL_MIN, nl.POOL_MAX), (0, 3))
        with self.assertRaises(nl.NarrativeError):
            nl.ResourcePool(current=4)

    def test_earning_caps_at_the_bound(self) -> None:
        pool = nl.ResourcePool(current=3)
        pool.earn()
        self.assertEqual(pool.current, nl.POOL_MAX)

    def test_overspending_is_refused(self) -> None:
        pool = nl.ResourcePool(current=1)
        pool.spend()
        with self.assertRaises(nl.NarrativeError):
            pool.spend()

    def test_invoking_returns_one_step_regardless_of_the_spend(self) -> None:
        pool = nl.ResourcePool(current=3)
        self.assertEqual(pool.invoke(0), 1)

    def test_cannot_invoke_twice_in_the_same_roll(self) -> None:
        pool = nl.ResourcePool(current=3)
        pool.invoke(0)
        with self.assertRaises(nl.NarrativeError):
            pool.invoke(1)

    def test_the_chapter_names_compelling_as_the_only_mid_scene_source(self) -> None:
        self.assertIn("the only way to gain one mid-scene", flat(CHAPTER))


class GMoveTests(unittest.TestCase):
    """AC2 — GM moves and partial success, read off the band the core already produced."""

    def test_a_failure_escalates(self) -> None:
        self.assertEqual(nl.gm_move(band="glancing", success=False), "escalate")

    def test_moves_are_read_from_the_band(self) -> None:
        self.assertEqual(nl.gm_move(band="brutal", success=True), "reward")
        self.assertEqual(nl.gm_move(band="solid", success=True), "cost")
        self.assertEqual(nl.gm_move(band="glancing", success=True), "complication")

    def test_an_unknown_band_is_refused(self) -> None:
        with self.assertRaises(nl.NarrativeError):
            nl.gm_move(band="nope", success=True)

    def test_moves_carry_no_numbers(self) -> None:
        """A move describes the fiction; it must not smuggle a modifier."""
        for band, move in nl.BAND_TO_MOVE.items():
            with self.subTest(band=band):
                self.assertNotRegex(nl.GM_MOVES[move], r"\d")

    def test_partial_success_is_a_band_not_a_second_roll(self) -> None:
        self.assertIn("not a second roll", flat(CHAPTER))


class PrecedenceTests(unittest.TestCase):
    """AC3 — deterministic precedence; the LLM proposes, the engine decides."""

    def test_an_llm_may_not_propose_a_modifier(self) -> None:
        result = nl.validate_proposal(nl.LLMProposal(narration="...", proposed_modifier=3))
        self.assertFalse(result.accepted)
        self.assertIn("may not propose a numeric modifier", result.reason)

    def test_narration_only_is_accepted(self) -> None:
        self.assertTrue(nl.validate_proposal(nl.LLMProposal(narration="...")).accepted)

    def test_a_well_formed_aspect_proposal_is_accepted(self) -> None:
        result = nl.validate_proposal(
            nl.LLMProposal(narration="...", proposed_aspect=an_aspect()))
        self.assertTrue(result.accepted)
        self.assertIsNotNone(result.aspect)

    def test_a_malformed_aspect_proposal_is_rejected(self) -> None:
        bad = an_aspect()
        object.__setattr__(bad, "scope", "  ")
        result = nl.validate_proposal(nl.LLMProposal(narration="...", proposed_aspect=bad))
        self.assertFalse(result.accepted)
        self.assertIn("malformed", result.reason)

    def test_the_chapter_states_the_precedence_order(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("The core check resolves", text)
        self.assertIn("Roll first. An aspect changes what a roll *means*", text)
        self.assertIn("the engine validates or **rejects**", text)


class ParityTests(unittest.TestCase):
    """AC4 — GNS parity is structural: every style resolves on ONE core."""

    def test_all_styles_share_one_core(self) -> None:
        self.assertTrue(nl.styles_share_one_core())

    def test_every_style_maps_to_the_same_core(self) -> None:
        self.assertEqual({nl.core_for_style(s) for s in nl.PLAY_STYLES}, {"core_check"})

    def test_an_unknown_style_is_refused(self) -> None:
        with self.assertRaises(nl.NarrativeError):
            nl.core_for_style("dramatist")

    def test_the_realms_really_do_share_the_arithmetic(self) -> None:
        """Parity is only real if the realm modules actually share the band function."""
        self.assertIs(soc.band_for_margin, pc.band_for_margin)

    def test_the_chapter_covers_all_three_play_readings(self) -> None:
        text = flat(CHAPTER)
        for style in ("Narrativist", "Simulationist", "Gamist"):
            with self.subTest(style=style):
                self.assertIn(style, text)


class AgencyTests(unittest.TestCase):
    """AC2/AC3 — a compel presents a complication; it never removes agency."""

    def test_the_chapter_protects_agency(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("A compel is never a punishment and never a loss of control", text)
        self.assertIn("cannot dictate a choice", text)
        self.assertIn("the player decides what the character does", text)


class HygieneTests(unittest.TestCase):
    """AC5 — provisional labels, independent wording, resolvable links."""

    def test_provisional_numbers_are_labelled(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("PROVISIONAL pending author calibration", text)
        self.assertGreaterEqual(text.count("PROVISIONAL"), 4)

    def test_no_proprietary_system_is_named(self) -> None:
        text = flat(CHAPTER)
        for name in ("Fate", "Cyberpunk", "Shadowrun", "Eclipse Phase", "GURPS", "CY_BORG",
                     "Powered by the Apocalypse", "PbtA"):
            with self.subTest(system=name):
                self.assertNotIn(name, text)

    def test_no_second_dice_system(self) -> None:
        text = flat(CHAPTER)
        for other in ("2d6", "1d100", "d20", "3d6"):
            with self.subTest(term=other):
                self.assertNotIn(other, text)

    def test_no_numeric_stress_track(self) -> None:
        """A stress track would contradict RULEBOOK.md 51's fiction-first ladder."""
        text = flat(CHAPTER)
        self.assertIn("No numeric stress track", text)
        self.assertIn("does not advance by arithmetic", text)

    def test_the_resource_name_is_left_to_the_author(self) -> None:
        self.assertIn("No name for the resource pool", flat(CHAPTER))

    def test_the_chapter_says_what_it_does_not_do(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("What this chapter deliberately does not do", text)
        for owner in ("#219", "#220", "#226"):
            with self.subTest(owner=owner):
                self.assertIn(owner, text)

    def test_the_module_declares_itself_non_canonical(self) -> None:
        self.assertFalse(nl.IS_CANONICAL)

    def test_the_document_keeps_no_dangling_relative_link(self) -> None:
        body = CHAPTER.read_text(encoding="utf-8")
        for target in re.findall(r"\]\((?!https?:)([^)#]+\.md)\)", body):
            with self.subTest(target=target):
                self.assertTrue((CHAPTER.parent / target).resolve().is_file(),
                                f"{target} does not resolve")


if __name__ == "__main__":
    unittest.main()
