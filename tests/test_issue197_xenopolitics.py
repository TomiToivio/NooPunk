# -*- coding: utf-8 -*-
"""Guard for the #197 §4 xenopolitics update — Earth as a strategic crisis.

#197 added a fourth section that is unusually easy to lose, because none of it is
mechanical: the status quo as a *strategic crisis* rather than a war; Orion already
embedded; the Pleiadian human colony and the staged contact strategy; the Grey/Mantid vs
Reptilian strategic blocs; the religious schism; the escalation horizon; and the
source/inspiration boundary.

The #187 guard covers the older chapter. This one covers what #197 added, and — like it —
asserts **structure and invariants only**, never incidental wording.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"
CHAPTER = ROOT / "rulebook" / "15_XENOPOLITICS.md"
MARKER = "# Extended canon and reference material"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(text: str) -> str:
    return " ".join(text.split())


class ChapterSectionsTests(unittest.TestCase):
    """The sections #197 §4 added must exist at their chapter numbers."""

    EXPECTED = (
        "### 187.3.1 A strategic crisis, not a war",
        "### 187.4.2 No membership, and no alliance",
        "### 187.4.3 Pleiadian humans, and staged contact",
        "### 187.5.3 Preserve and assimilate, not annihilate",
        "### 187.5.4 Two strategic blocs: Grey/Mantid and Reptilian",
        "### 187.5.5 A genuine rift, or a performance?",
        "### 187.5.6 Materialism, cults and elite networks",
        "### 187.6.2 The religious schism",
        "### 187.6.3 Other NHI are secondary",
        "### 187.8.1 The escalation horizon",
        "### 187.9.1 UNSA's position in the crisis",
    )

    def test_the_new_sections_exist(self) -> None:
        ch = read(CHAPTER)
        for heading in self.EXPECTED:
            with self.subTest(heading=heading):
                self.assertIn(heading, ch)

    def test_the_chapter_credits_both_issues(self) -> None:
        self.assertIn("issues #187 and #197", read(CHAPTER))

    def test_the_ledger_summary_mirrors_the_chapter(self) -> None:
        """§53 is the pointer most readers hit first; it must not lag the chapter."""
        _, appendix = read(RULEBOOK).split(MARKER, 1)
        self.assertRegex(appendix, r"(?m)^### 53\.4 A strategic crisis, not a war$")
        self.assertRegex(appendix, r"(?m)^### 53\.5 The blocs, the colony and the staging$")
        self.assertRegex(appendix, r"(?m)^### 53\.6 What this section does not define$")


class StrategicFrameTests(unittest.TestCase):
    """The frame: a crisis, not a war — and Orion is already here."""

    def setUp(self) -> None:
        self.ch = flat(read(CHAPTER))

    def test_it_is_a_crisis_not_an_all_out_war(self) -> None:
        self.assertIn("strategic crisis of the *Three-Body Problem* kind", self.ch)
        # the negation is emphasised in the chapter, so match the phrase, not its bolding
        self.assertRegex(self.ch, r"not\*{0,2} an all-out alien war")

    def test_orion_is_already_embedded(self) -> None:
        self.assertRegex(self.ch, r"already on\s+Earth and embedded within human institutions")

    def test_the_sophon_comparison_stays_a_shorthand(self) -> None:
        """The comparison must never harden into a claim about Orion's actual technology."""
        self.assertIn("thematic shorthand for asymmetric surveillance, infiltration, anxiety and",
                      self.ch)
        self.assertRegex(self.ch, r"not\*{0,2} a claim that Orion uses literal sophons")

    def test_panic_and_false_accusation_are_political_forces(self) -> None:
        self.assertIn("false accusation", self.ch)
        self.assertIn("opportunistic human abuse", self.ch)

    def test_case_level_uncertainty_survives_the_fixed_global_truths(self) -> None:
        self.assertIn("what any particular case actually is remains a question of evidence",
                      self.ch)


class ConfederacyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ch = flat(read(CHAPTER))

    def test_there_is_no_membership_and_no_alliance(self) -> None:
        self.assertIn("There is no full Earth membership and no alliance", self.ch)
        self.assertIn("incompatible with human self-determination and sovereignty", self.ch)

    def test_confederacy_doubts_readiness(self) -> None:
        self.assertRegex(self.ch, r"doubt that most Earth humans are\s+\*{0,2}ready\*{0,2}")

    def test_aid_does_not_depend_on_membership(self) -> None:
        self.assertIn("Assistance does not depend on membership", self.ch)
        self.assertRegex(self.ch, r"help defend,\s+protect and rebuild Earth even without formal membership")

    def test_the_pleiadian_colony_anchors_the_staging(self) -> None:
        self.assertIn("The Pleiadian human colony", self.ch)
        self.assertIn("largest Confederacy group initially", self.ch)
        # staged: humans -> other humanoids -> the visibly strange
        self.assertIn("Pleiadian humans first", self.ch)
        self.assertIn("other humanoid species", self.ch)
        self.assertIn("most visibly strange or nonhuman species", self.ch)
        self.assertIn("who counts as \"human\"", self.ch)


class OrionBlocTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ch = flat(read(CHAPTER))

    def test_orion_preserves_and_assimilates_rather_than_annihilates(self) -> None:
        self.assertIn("Preserve and assimilate, not annihilate", self.ch)
        self.assertIn("assimilation and control, not indiscriminate extermination", self.ch)
        self.assertIn("how much damage is", self.ch)

    def test_the_two_blocs_are_named_with_their_doctrines(self) -> None:
        self.assertIn("Grey/Mantid bloc", self.ch)
        self.assertIn("Reptilian bloc", self.ch)
        # infiltration-and-deals vs coercive conquest
        self.assertIn("covert social infiltration", self.ch)
        self.assertIn("enjoys battle", self.ch)
        self.assertIn("expendable proxy troops", self.ch)
        self.assertIn("being feared matters more to it than being liked", self.ch)

    def test_the_reptilian_damage_tolerance_is_stated(self) -> None:
        self.assertRegex(self.ch, r"half\s+of Earth's biosphere and noösphere")

    def test_the_coercive_idiom_carries_an_explicit_frame(self) -> None:
        """The in-world threat idiom must never read as a claim about a real people."""
        self.assertIn("in-world characterisation of a coercive threat idiom", self.ch)
        self.assertIn("not a statement about any real people", self.ch)

    def test_the_rift_stays_unresolved(self) -> None:
        self.assertIn("A genuine rift, or a performance?", self.ch)
        self.assertIn("a coordinated good-cop/bad-cop performance", self.ch)
        self.assertIn("unresolved intelligence question", self.ch)

    def test_orion_is_materialist_and_cults_are_instrumentalised(self) -> None:
        self.assertIn("materialist in rhetoric and governing ideology", self.ch)
        self.assertIn("human cults devoted to Orion", self.ch)
        self.assertIn("elite capture", self.ch)


class EscalationHorizonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ch = flat(read(CHAPTER))

    def test_a_future_invasion_is_expected(self) -> None:
        self.assertIn("Reptilian invasion fleet", self.ch)
        self.assertIn("The fleet is anticipated, not arrived", self.ch)

    def test_invasion_is_not_the_default_campaign_state(self) -> None:
        """The single most load-bearing sentence of the escalation section."""
        self.assertIn("does not make open invasion the default campaign state", self.ch)

    def test_the_expectation_does_work_in_several_directions(self) -> None:
        for driver in ("military preparation", "opportunistic alliance", "xenophobia",
                       "pre-emptive violence"):
            with self.subTest(driver=driver):
                self.assertIn(driver, self.ch)


class HumanReactionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ch = flat(read(CHAPTER))

    def test_the_religious_schism_is_recorded(self) -> None:
        self.assertIn("The religious schism", self.ch)
        self.assertIn("reinterpret or absorb", self.ch)
        self.assertIn("intensely xenophobic fundamentalism", self.ch)
        self.assertIn("Do not treat any religion as reacting as one body", self.ch)

    def test_the_schism_is_not_only_religious(self) -> None:
        """Secular and xenophobic opposition must not be folded into the religious story."""
        self.assertIn("not all opposition is religious at all", self.ch)
        self.assertIn("human-supremacist politics", self.ch)

    def test_law_of_one_stays_an_in_world_movement(self) -> None:
        self.assertIn("\"Law of One cult\" is an in-world religious and social movement",
                      self.ch)

    def test_other_nhi_stay_peripheral(self) -> None:
        self.assertIn("Other NHI are secondary", self.ch)
        self.assertIn("Earth–Confederacy–Orion conflict", self.ch)
        self.assertIn("case-level encounters", self.ch)


class InspirationBoundaryTests(unittest.TestCase):
    """Real-world sources must stay distinguishable from setting fact."""

    def setUp(self) -> None:
        self.ch = flat(read(CHAPTER))

    def test_the_reference_works_are_labelled_as_fiction_sources(self) -> None:
        self.assertIn("narrative comparison", self.ch)
        self.assertIn("fictional-setting inspiration", self.ch)

    def test_neither_is_evidence_of_real_extraterrestrial_activity(self) -> None:
        self.assertIn("Neither is a documented account of", self.ch)
        self.assertIn("sources for fiction, never as\nfindings".replace("\n", " "), self.ch)


class OpenQuestionsTests(unittest.TestCase):
    """New canon must not silently close what the issue left open."""

    def setUp(self) -> None:
        self.ch = flat(read(CHAPTER))

    def test_the_two_added_questions_are_declared_open(self) -> None:
        self.assertIn("no settlement of the two questions this chapter adds", self.ch)

    def test_the_chapter_still_defines_no_mechanics(self) -> None:
        """#197 §4 is lore; it must not have smuggled in a subsystem."""
        raw = read(CHAPTER)
        for token in ("2d6", "1d10", "d100", "hit points", "reputation points",
                      "damage:", "cost:", "price:"):
            with self.subTest(token=token):
                self.assertNotIn(token, raw.lower())

    def test_no_concrete_year_was_introduced(self) -> None:
        years = [y for y in re.findall(r"\b(?:19|20)\d{2}\b", read(CHAPTER)) if y != "20XX"]
        self.assertEqual(years, [], f"#197 additions assign concrete years: {years}")


if __name__ == "__main__":
    unittest.main()
