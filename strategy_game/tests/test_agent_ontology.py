"""Executable contracts for the agent/card ontology (issue #303).

Code-only, per `AGENTS.md` and issue #271. These exercise the **ontology and its validator** -- the
agent/context split, the shared card interface, the no-numbers discipline and the no-third-spelling
rule -- not the tone guide's prose.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_agent_ontology.py"
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game import agents as ag  # noqa: E402
from strategy_game.agents import (  # noqa: E402
    AGENT_KIND_IDS,
    CONTEXT_IDS,
    ONTOLOGY_FORMAT,
    AgentOntology,
    OntologyError,
    load_agent_ontology,
    ontology_from_dict,
)


class ShippedOntologyTests(unittest.TestCase):
    """The packaged ontology is readable and self-consistent."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.onto = load_agent_ontology()

    def test_loads_and_declares_its_format(self) -> None:
        self.assertEqual(self.onto.format, ONTOLOGY_FORMAT)

    def test_problems_is_clean(self) -> None:
        self.assertEqual(self.onto.problems(), ())

    def test_marks_itself_a_proposal(self) -> None:
        self.assertIn("PROPOSAL", self.onto.status)

    def test_a_foreign_document_is_refused(self) -> None:
        raw = json.loads(ag.DATA_PATH.read_text(encoding="utf-8"))
        raw["format"] = "noopunk.strategy_game.something_else"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "onto.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(OntologyError):
                load_agent_ontology(path)

    def test_round_trip_preserves_validity(self) -> None:
        self.assertEqual(ontology_from_dict(self.onto.to_dict()).problems(), ())


class SplitTests(unittest.TestCase):
    """The load-bearing rule: function systems are contexts, never agents."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.onto = load_agent_ontology()

    def test_the_four_named_agent_kinds_are_declared(self) -> None:
        self.assertEqual(set(self.onto.kind_ids), set(AGENT_KIND_IDS))

    def test_the_three_interpretive_contexts_are_declared(self) -> None:
        self.assertEqual(set(self.onto.context_ids), set(CONTEXT_IDS))

    def test_the_two_sets_are_disjoint(self) -> None:
        self.assertEqual(set(self.onto.kind_ids) & set(self.onto.context_ids), set())

    def test_no_context_is_an_agent(self) -> None:
        for ctx in self.onto.contexts:
            self.assertFalse(ctx.is_agent, ctx.id)

    def test_every_kind_is_an_agent(self) -> None:
        for kind in self.onto.kinds:
            self.assertTrue(kind.is_agent, kind.id)

    def test_function_systems_are_never_listed_as_an_agent_kind(self) -> None:
        for ctx_id in CONTEXT_IDS:
            self.assertNotIn(ctx_id, self.onto.kind_ids)

    def test_every_context_says_why_it_is_not_an_agent(self) -> None:
        for ctx in self.onto.contexts:
            self.assertTrue(ctx.why_not_an_agent, ctx.id)
            self.assertTrue(ctx.how_it_acts, ctx.id)

    def test_the_rule_is_stated_in_terminology(self) -> None:
        self.assertIn("how does this read", self.onto.terminology.get("rule", ""))
        self.assertIn("what do you do now", self.onto.terminology.get("rule", ""))


class CardInterfaceTests(unittest.TestCase):
    """One shared card shape, and explicitly not one shared algorithm."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.onto = load_agent_ontology()

    def test_required_fields_are_kind_identity_provenance(self) -> None:
        self.assertEqual(set(self.onto.required_fields), {"kind", "identity", "provenance"})

    def test_optional_fields_cover_relationships_associations_and_tags(self) -> None:
        for field_name in ("relationships", "location_associations", "system_associations", "scenario_tags"):
            self.assertIn(field_name, self.onto.optional_fields)

    def test_sharing_a_shape_is_not_sharing_behaviour(self) -> None:
        behaviour = self.onto.common_card_interface.get("behaviour", "")
        self.assertIn("not sharing an algorithm", behaviour)

    def test_no_default_llm_requirement(self) -> None:
        self.assertIn("a default LLM requirement", " ".join(self.onto.common_card_interface.get("not_included", [])))

    def test_every_kind_states_aggregation_and_a_double_counting_guard(self) -> None:
        for kind in self.onto.kinds:
            self.assertTrue(kind.aggregation_rule, kind.id)
            self.assertTrue(kind.double_counting_guard, kind.id)

    def test_overlap_rules_are_declared(self) -> None:
        rules = self.onto.overlap_and_aggregation.get("rules", [])
        self.assertTrue(rules)
        self.assertTrue(any("cross-cutting" in r for r in rules))
        self.assertTrue(any("attributed once" in r for r in rules))


class NoNumbersTests(unittest.TestCase):
    """No scale is approved by this record, so no number may appear."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.onto = load_agent_ontology()

    def test_no_numeric_value_in_any_kind_or_context(self) -> None:
        for card in list(self.onto.kinds) + list(self.onto.contexts):
            self.assertFalse(ag._has_number(card.detail), card.id)

    def test_no_scale_shaped_field_name(self) -> None:
        for card in list(self.onto.kinds) + list(self.onto.contexts):
            for key in card.detail:
                self.assertFalse(
                    any(tok in key.lower() for tok in ag._SCALE_TOKENS), f"{card.id}:{key}"
                )

    def test_capacity_legitimacy_influence_and_coercion_stay_axes_not_scales(self) -> None:
        blob = json.dumps(self.onto.to_dict())
        self.assertIn("conceptually separable axes", blob)


class VocabularyDisciplineTests(unittest.TestCase):
    """No third spelling, and the politics.py / political.py fork stays open."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.onto = load_agent_ontology()

    def test_no_banned_synonym_for_the_unclassified_role(self) -> None:
        blob = json.dumps(self.onto.raw).lower()
        for banned in ag._BANNED_SPELLINGS:
            self.assertNotIn(f'"{banned}"', blob)

    def test_the_rule_cites_the_v1_record(self) -> None:
        note = self.onto.vocabulary_discipline.get("no_third_spelling", "")
        self.assertIn("V1_DISCOURSE_AND_NETWORK.md", note)
        self.assertIn("unspecified", note)

    def test_the_fork_is_declared_unresolved(self) -> None:
        note = self.onto.vocabulary_discipline.get("unresolved_fork", "")
        self.assertIn("political.py", note)
        self.assertIn("routed to the author", note)

    def test_author_choices_are_left_open(self) -> None:
        self.assertGreaterEqual(len(self.onto.pending_author_choices), 4)
        blob = " ".join(self.onto.pending_author_choices).lower()
        self.assertIn("node or becomes an edge", blob)


class ValidatorTests(unittest.TestCase):
    """The validator reports rather than raises."""

    def setUp(self) -> None:
        self.onto = load_agent_ontology()

    def _mutated(self, mutate) -> AgentOntology:
        raw = json.loads(ag.DATA_PATH.read_text(encoding="utf-8"))
        mutate(raw)
        return ontology_from_dict(raw)

    def test_a_function_system_declared_as_an_agent_is_reported(self) -> None:
        def mutate(raw):
            raw["agent_kinds"].append({"id": "function_systems", "is_agent": True,
                                       "represents": "x", "aggregation_rule": "y",
                                       "double_counting_guard": "z"})
        bad = self._mutated(mutate)
        self.assertTrue(any("both agent and context" in p for p in bad.problems()))

    def test_a_context_marked_as_an_agent_is_reported(self) -> None:
        def mutate(raw):
            raw["interpretive_contexts"][0]["is_agent"] = True
        bad = self._mutated(mutate)
        self.assertTrue(any("is marked is_agent" in p for p in bad.problems()))

    def test_a_numeric_value_is_reported(self) -> None:
        def mutate(raw):
            raw["agent_kinds"][0]["capacity"] = 3
        bad = self._mutated(mutate)
        self.assertTrue(any("numeric value" in p for p in bad.problems()))

    def test_a_scale_shaped_field_is_reported(self) -> None:
        def mutate(raw):
            raw["agent_kinds"][0]["legitimacy_score"] = "high"
        bad = self._mutated(mutate)
        self.assertTrue(any("scale-shaped" in p for p in bad.problems()))

    def test_a_missing_agent_kind_is_reported(self) -> None:
        def mutate(raw):
            raw["agent_kinds"].pop()
        bad = self._mutated(mutate)
        self.assertTrue(any("missing agent kinds" in p for p in bad.problems()))

    def test_a_banned_synonym_is_reported(self) -> None:
        def mutate(raw):
            raw["vocabulary_discipline"]["example_role"] = "unrecorded"
        bad = self._mutated(mutate)
        self.assertTrue(any("banned synonym" in p for p in bad.problems()))

    def test_discussing_the_ban_is_not_itself_a_violation(self) -> None:
        # The shipped record names both banned spellings in order to ban them; only *using* one as a
        # value is a defect.
        self.assertEqual(self.onto.problems(), ())
        blob = json.dumps(self.onto.raw).lower()
        self.assertTrue(any(b in blob for b in ag._BANNED_SPELLINGS))

    def test_a_kind_without_an_aggregation_rule_is_reported(self) -> None:
        def mutate(raw):
            raw["agent_kinds"][0].pop("aggregation_rule")
        bad = self._mutated(mutate)
        self.assertTrue(any("aggregation_rule" in p for p in bad.problems()))


class ScopeDirectiveTests(unittest.TestCase):
    """Design-only, offline, and no engine smuggled in."""

    def test_the_module_does_not_import_laclaugpt(self) -> None:
        source = Path(ag.__file__).read_text(encoding="utf-8")
        self.assertNotIn("laclaugpt", source.lower())

    def test_the_module_needs_no_optional_dependency(self) -> None:
        source = Path(ag.__file__).read_text(encoding="utf-8")
        for banned in ("pandas", "numpy", "networkx", "requests", "openai"):
            self.assertNotIn(f"import {banned}", source)

    def test_the_module_defines_no_resolution_or_behaviour(self) -> None:
        source = Path(ag.__file__).read_text(encoding="utf-8").lower()
        for banned in ("def resolve", "def step", "def tick", "def act("):
            self.assertNotIn(banned, source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
