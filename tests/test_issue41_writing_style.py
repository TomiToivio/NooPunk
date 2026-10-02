# -*- coding: utf-8 -*-
"""Regression tests for issue #41: writing style, academic worldbuilding, statistical rules.

These are STRUCTURE guards, in the style of ``test_issue34_theory_grounding.py`` and
``test_issue32_rules_reset.py``. They assert that every convention the issue required
to be *written down* is actually written down, and that the issue's guardrails hold.

They deliberately do NOT constrain mechanics. Issue #41 asks the statistical core
to be **investigated and documented**, not adopted, and ``AGENTS.md`` §1/§4 make
inventing or revising rules out of scope. So a test here may never require a
formula, a parameter, or a chosen model — only that the options, their costs and
their status are recorded.

What is protected here:

* the style guide exists and covers each register and convention the issue lists;
* the epistemic-status system distinguishes evidence from speculation from fiction,
  and treats the in-world-unknown level as a real outcome rather than a gap;
* PKD is documented as a high-level tonal influence **with** a no-pastiche rule;
* the citation and bibliography conventions are defined, including the three
  markers;
* the statistical section is present, is marked as an **investigation**, and
  explicitly does not make itself canonical;
* the tabletop/simulation relationship is described in terms of the **existing**
  canonical engine, and forbids the simulation from inventing a rule;
* a worked example resolves one event in both modes;
* system-level modelling is considered alongside individual checks;
* the "do not write a textbook" design constraint is present;
* the document defers the issue's "consider later" extras rather than silently
  building or silently dropping them.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import itertools
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STYLE_DOC = "docs/WRITING_STYLE_AND_MODELING.md"
RULEBOOK = "RULEBOOK.md"
REGISTRY = "docs/THEORETICAL_SOURCES.md"
DESIGN_PRINCIPLES = "docs/DESIGN_PRINCIPLES.md"
AGENTS = "AGENTS.md"

#: The six epistemic statuses the issue requires, by their distinguishing word.
EPISTEMIC_LEVELS = ("established", "contested", "speculative", "fringe", "extrapolation", "unknown")

#: The three citation markers.
MARKERS = ("REAL:", "MODEL:", "NOÖPUNK:")

#: The four writing registers the issue names.
REGISTERS = ("expository", "setting", "fiction", "sidebar")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalised(relative: str) -> str:
    """Lowercased, whitespace-collapsed, markdown emphasis stripped.

    Structural markers are stripped because a phrase wrapped across a blockquote or
    carrying emphasis would otherwise miss a plain substring assertion. The
    comparison and range characters are NOT stripped: ``>=``, ``-3..+3`` and the
    ladder numbers are canon text and removing them produces false failures.
    """
    text = re.sub(r"[>*_`]", " ", read(relative))
    return " ".join(text.split()).lower()


def flat(relative: str) -> str:
    return normalised(relative)


def section(heading: str, *, relative: str = STYLE_DOC) -> str:
    """Return the normalised body of one ``##`` section, heading excluded.

    Section-scoped assertions matter: a phrase that also appears elsewhere in the
    document must not be able to satisfy a test for a section that was deleted.
    Sabotage-testing found exactly that hole.
    """
    text = read(relative)
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        return ""
    rest = text[match.end():]
    nxt = re.search(r"^##\s+", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(re.sub(r"[>*_`]", " ", body).split()).lower()


class StyleGuideExistsTests(unittest.TestCase):
    """The issue's first deliverable, and its proposed file name."""

    def test_the_style_guide_exists(self) -> None:
        self.assertTrue((ROOT / STYLE_DOC).exists(), f"{STYLE_DOC} is missing")

    def test_covers_every_register(self) -> None:
        text = flat(STYLE_DOC)
        for register in REGISTERS:
            with self.subTest(register=register):
                self.assertIn(register, text)

    def test_defines_the_worldbuilding_workflow(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("theory", text)
        self.assertIn("playable situation", text)

    def test_states_the_do_not_write_a_textbook_constraint(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("textbook", text)


class AcademicWorldbuildingTests(unittest.TestCase):
    """Setting claims must be traceable rather than arbitrary."""

    def test_requires_a_real_source_or_tradition(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("real theory", text)

    def test_requires_the_five_part_treatment(self) -> None:
        """source / citation / interpretation / extension-or-disagreement / consequence."""
        text = flat(STYLE_DOC)
        for part in ("source", "citation", "noöpunk reading", "extension or disagreement",
                     "mechanical consequence"):
            with self.subTest(part=part):
                self.assertIn(part, text)

    def test_states_traceability_as_the_goal(self) -> None:
        self.assertIn("traceable", flat(STYLE_DOC))

    def test_points_at_the_existing_registry_rather_than_forking_it(self) -> None:
        """The per-rule grounding lives in THEORETICAL_SOURCES.md; the style guide
        must reference it, not become a second registry."""
        self.assertIn(REGISTRY, read(STYLE_DOC))

    def test_references_design_principles_without_restating_them(self) -> None:
        """The doc lives in docs/, so its sibling link is relative, not `docs/...`."""
        text = read(STYLE_DOC)
        self.assertIn("DESIGN_PRINCIPLES.md", text)


class EpistemicStatusTests(unittest.TestCase):
    """The issue's six-layer uncertainty hierarchy."""

    def test_the_epistemic_status_section_exists(self) -> None:
        body = section("4. Epistemic status of a claim")
        self.assertTrue(body, "the epistemic-status section is missing")
        self.assertIn("six levels", body)

    def test_all_six_levels_are_defined_in_that_section(self) -> None:
        body = section("4. Epistemic status of a claim")
        for level in EPISTEMIC_LEVELS:
            with self.subTest(level=level):
                self.assertIn(level, body)

    def test_distinguishes_fact_from_speculation_from_fiction(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("established", text)
        self.assertIn("fictional extrapolation", text)

    def test_in_world_unknown_is_a_defined_level_not_only_discussed(self) -> None:
        """The level must remain in the table, not merely be mentioned in prose."""
        body = section("4. Epistemic status of a claim")
        self.assertIn("in-world unknown", body)
        self.assertIn("refuses to establish", body)

    def test_in_world_unknown_is_a_real_outcome_not_a_gap(self) -> None:
        body = section("4. Epistemic status of a claim")
        self.assertIn("refusal is the canon", body)

    def test_fringe_is_not_treated_as_established(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("without strengthening the present-day evidence", text)

    def test_speculative_themes_are_named(self) -> None:
        text = flat(STYLE_DOC)
        for theme in ("consciousness", "psi", "nhi", "quantum"):
            with self.subTest(theme=theme):
                self.assertIn(theme, text)


class FictionStyleTests(unittest.TestCase):
    """PKD as tonal reference, with the no-pastiche rule."""

    def test_names_philip_k_dick_as_tonal_reference(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("philip k. dick", text)

    def test_forbids_direct_style_imitation(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("pastiche", text)
        self.assertIn("do not imitate", text)

    def test_records_the_high_level_qualities(self) -> None:
        text = flat(STYLE_DOC)
        for quality in ("unstable reality", "identity instability", "dark humour",
                        "god's-eye view"):
            with self.subTest(quality=quality):
                self.assertIn(quality, text)

    def test_fiction_is_not_allowed_to_resolve_open_questions(self) -> None:
        """The project's central ambiguity must not be spent by a single scene."""
        text = flat(STYLE_DOC)
        self.assertIn("must not resolve", text)

    def test_states_the_sourcebook_characters_asymmetry(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("characters usually do not know", text)


class CitationConventionTests(unittest.TestCase):
    """Citation and bibliography conventions."""

    def test_defines_all_three_markers(self) -> None:
        text = read(STYLE_DOC)
        for marker in MARKERS:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_defines_where_citations_go(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("references section", text)

    def test_a_citation_must_not_make_a_contested_claim_look_settled(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("contested", text)
        self.assertIn("settled", text)

    def test_each_marker_is_defined_in_the_marker_section(self) -> None:
        # section() lowercases its body, so compare case-insensitively
        body = section("5. Citation conventions")
        for marker in MARKERS:
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), body)

    def test_each_marker_is_demonstrated_outside_the_definition(self) -> None:
        """Each marker must appear in the citation section AND in the examples.

        Counting occurrences document-wide was too weak: a marker could survive in
        one section while vanishing from the other, and the guard still passed.
        Anchoring each marker to two named sections is what makes removal fail.
        """
        citation = section("5. Citation conventions")
        examples = section("13. Examples")
        self.assertTrue(examples, "the examples section is missing")
        for marker in MARKERS:
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), citation,
                              f"{marker} is not defined in the citation section")
                self.assertIn(marker.lower(), examples,
                              f"{marker} is defined but never demonstrated in the examples")


class StatisticalRulesTests(unittest.TestCase):
    """The issue asks for an INVESTIGATION. It must be present, and must not canonize."""

    def test_the_statistical_section_exists(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("latent", text)
        self.assertIn("logistic", text)

    def test_the_section_is_marked_as_an_investigation_not_canon(self) -> None:
        body = section("6. Statistical and probabilistic rules — an investigation")
        self.assertTrue(body, "the statistical section is missing")
        self.assertIn("investigation, not canon", body)

    def test_the_statistical_section_does_not_claim_canon(self) -> None:
        """The section may not assert itself canonical anywhere in its body."""
        body = section("6. Statistical and probabilistic rules — an investigation")
        for claim in ("this section is canon", "the canonical model is",
                      "noöpunk uses the logistic model as canon"):
            with self.subTest(claim=claim):
                self.assertNotIn(claim, body)

    def test_it_does_not_select_a_model(self) -> None:
        """A documentation task may not choose the mechanics."""
        text = flat(STYLE_DOC)
        self.assertNotIn("the canonical model is", text)
        self.assertNotIn("noöpunk uses the logistic model", text)

    def test_it_records_the_cost_of_each_option(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("cost", text)

    def test_it_uses_the_existing_canonical_engine_as_the_baseline(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("2d6", text)
        self.assertIn("difficulty", text)

    def test_it_flags_that_uniform_commensurability_is_a_metaphysical_claim(self) -> None:
        """Fitting one formula across all four domains would assert the psychic
        domain is mechanically commensurable with the others."""
        text = flat(STYLE_DOC)
        self.assertIn("commensurab", text)

    def test_it_points_at_the_authoritative_rulebook_section(self) -> None:
        text = read(STYLE_DOC)
        self.assertIn(RULEBOOK, text)
        self.assertIn("§4", text)


class WorkedExampleTests(unittest.TestCase):
    """The issue requires one event resolved in tabletop and simulation modes."""

    def test_both_modes_are_shown_as_actual_worked_subsections(self) -> None:
        body = section("10. Worked example: one event, two modes")
        self.assertTrue(body, "the worked-example section is missing")
        self.assertIn("10.1 tabletop mode", body)
        self.assertIn("10.2 simulation mode", body)
        # and the simulation half must carry the numbers, not just a heading
        self.assertIn("p(success)", body)
        self.assertIn("0.8333", body)

    def test_the_example_uses_the_canonical_check(self) -> None:
        """The example must not invent a mechanic to demonstrate the architecture."""
        text = flat(STYLE_DOC)
        self.assertIn("2d6", text)
        self.assertIn("skill", text)
        self.assertIn("attribute", text)


class SimulationRelationshipTests(unittest.TestCase):
    """One conceptual model across human play and machine simulation."""

    def test_states_the_same_model_spans_both(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("same model", text)

    def test_forbids_the_simulation_inventing_a_probability(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("must", text)
        self.assertIn("invent a probability", text)

    def test_forbids_approximation_becoming_canon(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("approximation", text)

    def test_considers_system_level_modelling(self) -> None:
        """The issue requires modelling above the individual character level."""
        text = flat(STYLE_DOC)
        self.assertIn("network", text)


class ModelDescriptionTests(unittest.TestCase):
    """Conventions for describing a model."""

    def test_requires_stating_assumptions(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("assumes", text)

    def test_requires_stating_what_a_model_does_not_predict(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("does not predict", text)


class DocumentationHygieneTests(unittest.TestCase):
    """The guide must not quietly become a mechanism, and must not break the guards."""

    def test_the_design_principles_document_is_not_modified_by_this_change(self) -> None:
        """AGENTS.md and DESIGN_PRINCIPLES.md are author-owned."""
        text = read(DESIGN_PRINCIPLES)
        self.assertIn("single canonical explanation", text)

    def test_the_guide_does_not_restate_the_three_balances(self) -> None:
        """DESIGN_PRINCIPLES.md must stay the one place that explains them."""
        text = flat(STYLE_DOC)
        self.assertNotIn("gamism / narrativism / simulationism balance", text)

    def test_the_issue_s_later_extras_are_deferred_explicitly(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("follow-up", text)
        for deferred in ("bibtex", "csl"):
            with self.subTest(deferred=deferred):
                self.assertIn(deferred, text)

    def test_the_rulebook_is_still_intentionally_incomplete(self) -> None:
        text = flat(STYLE_DOC)
        self.assertIn("intentionally incomplete", text)


class WorkedMathIsCorrectTests(unittest.TestCase):
    """The document prints probabilities. They must be right.

    A conventions document that misstates its own arithmetic would be worse than
    one that omits it, and this is cheap to check.
    """

    @staticmethod
    def _two_d6() -> Counter:
        return Counter(a + b for a, b in itertools.product(range(1, 7), repeat=2))

    def test_the_stated_success_probability_in_the_worked_example(self) -> None:
        c = self._two_d6()
        # modifier +3 against difficulty 8 means 2d6 >= 5
        p = sum(v for k, v in c.items() if k >= 5) / 36
        self.assertAlmostEqual(p, 0.8333, places=3)
        self.assertIn("30/36", read(STYLE_DOC))

    def test_the_stated_ladder_probabilities(self) -> None:
        c = self._two_d6()

        def p(mod: int, difficulty: int) -> float:
            return sum(v for k, v in c.items() if k >= difficulty - mod) / 36

        self.assertAlmostEqual(p(0, 6), 0.722, places=3)
        self.assertAlmostEqual(p(0, 8), 0.417, places=3)
        self.assertAlmostEqual(p(0, 10), 0.167, places=3)
        self.assertAlmostEqual(p(0, 12), 1 / 36, places=3)

    def test_the_stated_distribution_facts(self) -> None:
        c = self._two_d6()
        self.assertEqual(c[2], 1)
        self.assertEqual(c[12], 1)
        self.assertEqual(c[7], 6)
        self.assertEqual(sum(c.values()), 36)

    def test_the_top_of_the_ladder_needs_a_positive_modifier(self) -> None:
        """Difficulty 14 at +0 is unreachable; the doc states this."""
        c = self._two_d6()
        max_total_at_zero = max(c)
        self.assertLess(max_total_at_zero, 14)
        self.assertIn("probability zero", flat(STYLE_DOC))

    def test_the_stated_mean_and_variance(self) -> None:
        c = self._two_d6()
        mu = sum(k * v for k, v in c.items()) / 36
        var = sum((k - mu) ** 2 * v for k, v in c.items()) / 36
        self.assertAlmostEqual(mu, 7.0, places=6)
        self.assertAlmostEqual(var, 5.833, places=3)


if __name__ == "__main__":
    unittest.main()
