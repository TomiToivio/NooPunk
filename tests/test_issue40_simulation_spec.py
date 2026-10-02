"""Structure guards for the issue #40 Phase A simulation specification.

These are STRUCTURE guards in the style of ``test_issue32_rules_reset.py`` and
``test_issue34_theory_grounding.py``. They assert that the specification the issue
asked for actually exists, that it carries the interfaces and boundaries the issue
requires, and — most importantly — that it did not do the thing NoöPunk forbids:
invent rules, mechanics, factions, or simulation semantics to look complete.

They deliberately do NOT constrain how the simulator will be implemented. Issue #40
is explicit that Phase A is "specification only", so a test here may never require
a mechanic, a numeric value, or a canonical entity list.

What is protected here:

* the spec exists and is reachable from the README;
* Phase A items 1-3 are answered (state model, event format, synthetic separation);
* the event envelope carries every field the architecture depends on, and ordering
  is stated as ``turn`` rather than ``timestamp``;
* the Concordia API review is recorded, including the finding that its built-in
  world-state/clock components are LLM-generated and therefore cannot be canonical;
* the mandatory resolver seam ("no LLM output enters the event log except through
  the deterministic resolver") is stated;
* the DEFER register exists and names an owner for every deferred decision;
* the theory division of labour is recorded without collapsing the theories;
* the specification states that it defines no rules/mechanics and marks the
  proposed vocabulary as unconfirmed — i.e. the anti-invention constraint holds.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPEC = "docs/SIMULATION_ARCHITECTURE_SPEC.md"
README = "README.md"

#: Fields the architecture depends on, with the reason recorded in the spec.
REQUIRED_EVENT_FIELDS = (
    "simulation_id",
    "event_id",
    "turn",
    "timestamp",
    "actor",
    "action_type",
    "target",
    "content",
    "location",
    "visibility",
    "source",
    "synthetic",
)

#: The pinned Concordia revision the API review was performed against.
PINNED_CONCORDIA_REVISION = "405584db8e09e001da6deb147a6389f7a7f44e28"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalised(relative: str) -> str:
    """Lowercased, whitespace-collapsed text, robust to markdown emphasis.

    Emphasis characters are **removed** rather than replaced with a space: the
    spec writes field names in backticks (`turn`, `WorldState`), and substituting a
    space turns `` `turn`, `` into ``turn ,`` and splits slashed pairs such as
    ``WorldState`/`GenerativeClock`` into three words, which would make a phrase
    assertion fail on correct text.
    """
    text = read(relative)
    text = re.sub(r"[*`_]", "", text)
    text = re.sub(r"[>|]", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return " ".join(text.split()).lower()


class SpecExistsTests(unittest.TestCase):
    def test_specification_document_exists(self) -> None:
        self.assertTrue((ROOT / SPEC).exists(), f"{SPEC} is missing")

    def test_readme_makes_the_specification_discoverable(self) -> None:
        self.assertIn(
            "SIMULATION_ARCHITECTURE_SPEC.md",
            read(README),
            "the simulation specification must be reachable from the README",
        )

    def test_spec_links_the_canonical_design_principles(self) -> None:
        self.assertIn("DESIGN_PRINCIPLES.md", read(SPEC))

    def test_spec_is_labelled_phase_a_specification_only(self) -> None:
        text = normalised(SPEC)
        self.assertIn("phase a specification", text)
        self.assertIn("documentation only", text)


class AntiInventionTests(unittest.TestCase):
    """The guards that matter most: the spec must not invent canon."""

    def test_spec_states_it_defines_no_rules_or_mechanics(self) -> None:
        text = normalised(SPEC)
        self.assertIn("defines no rules", text)
        self.assertIn("mechanics", text)

    def test_candidate_vocabulary_is_marked_unconfirmed(self) -> None:
        """Issue text is a proposal, not an author decision.

        The natural agent failure is to reproduce the issue's entity list as if it
        were canon. The spec must keep it labelled as unconfirmed.
        """
        text = normalised(SPEC)
        self.assertIn("unconfirmed", text)
        self.assertIn("candidate vocabulary", text)

    def test_spec_does_not_declare_the_proposed_kinds_canonical(self) -> None:
        """A 'canonical entity kinds' enumeration would be the invention itself."""
        text = normalised(SPEC)
        for forbidden in (
            "canonical entity kinds are",
            "the canonical entity list is",
            "the following entity kinds are canonical",
            "canonical relation types are",
        ):
            with self.subTest(phrase=forbidden):
                self.assertNotIn(forbidden, text)

    def test_spec_defers_rather_than_choosing_macro_mechanics(self) -> None:
        """Naming a sheet field with a value/scale would define a social mechanic."""
        text = normalised(SPEC)
        self.assertIn("tabletop macro mechanics", text)
        # the requirement must be recorded...
        self.assertIn("playable without a computer", text)
        # ...while the field set stays explicitly undecided.
        self.assertRegex(text, r"no field is defined")

    def test_spec_did_not_cite_the_withdrawn_chassis_policy(self) -> None:
        """The spec must describe main's actual governance, not a superseded one.

        Invariant 9 was the Cities Without Number chassis when this issue was filed;
        it is now "Original NoöPunk rules only", and the CWN review policy is gone
        from ``AGENTS.md``. Citing the withdrawn verdict language (KEEP/MODIFY/
        REPLACE/OMIT/DEFER) would describe a policy the repository no longer has.
        """
        text = normalised(SPEC)
        for withdrawn in (
            "cities without number",
            "cwn chassis",
            "keep/modify/replace/omit",
            "open mechanical chassis",
        ):
            with self.subTest(phrase=withdrawn):
                self.assertNotIn(
                    withdrawn, text, f"the spec cites the withdrawn chassis policy: {withdrawn}"
                )

    def test_spec_matches_the_current_original_rules_policy(self) -> None:
        text = normalised(SPEC)
        self.assertIn("left unresolved rather than", text)

    def test_spec_does_not_supply_numeric_simulation_values(self) -> None:
        """No invented scales, ranges, or thresholds for social quantities.

        The six canonical attributes and the 2d6 ladder are tabletop canon and may
        be *referenced*; what must not appear is a new numeric mechanic invented
        here (e.g. a legitimacy or cohesion scale).
        """
        body = read(SPEC)
        for quantity in ("legitimacy", "cohesion", "reach", "institutional power"):
            with self.subTest(quantity=quantity):
                # may be named as a candidate, but never assigned a value/range
                pattern = rf"{quantity}[^\n]{{0,40}}\b(1d|d\d|\d+\s*[-–]\s*\d+|scale of)\b"
                self.assertIsNone(
                    re.search(pattern, body, re.I),
                    f"{quantity} appears to have been given a numeric definition",
                )


class PhaseAItemTests(unittest.TestCase):
    """Phase A items 1-3 must be genuinely answered, not mentioned."""

    def test_items_1_to_3_are_indexed_to_their_sections(self) -> None:
        text = normalised(SPEC)
        self.assertIn("phase a items are answered", text)
        for anchor in ("canonical-state-model", "event-format", "simulation-vs-empirical-separation"):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, read(SPEC))

    def test_state_model_requires_provenance_and_open_vocabularies(self) -> None:
        text = normalised(SPEC)
        self.assertIn("open vocabularies", text)
        self.assertIn("provenance", text)

    def test_state_model_forbids_storing_unspecified_quantities(self) -> None:
        """Storing an unspecified derived number is inventing a mechanic."""
        text = normalised(SPEC)
        self.assertIn("no mechanics", text)
        self.assertRegex(text, r"storing an unspecified number is inventing a mechanic")

    def test_every_required_event_field_is_present(self) -> None:
        body = read(SPEC)
        for field in REQUIRED_EVENT_FIELDS:
            with self.subTest(field=field):
                self.assertIn(f"`{field}`", body, f"event field {field} is not specified")

    def test_ordering_is_turn_and_not_timestamp(self) -> None:
        text = normalised(SPEC)
        self.assertIn("ordering is turn, never timestamp", text)

    def test_provenance_fields_are_set_by_the_boundary_not_the_actor(self) -> None:
        """An agent must not be able to self-report as non-synthetic."""
        text = normalised(SPEC)
        self.assertIn("set by the emitting boundary, not by the actor", text)

    def test_events_are_immutable(self) -> None:
        text = normalised(SPEC)
        self.assertIn("immutable once logged", text)

    def test_synthetic_separation_is_structural_not_a_convention(self) -> None:
        text = normalised(SPEC)
        self.assertIn("impossible to confuse", text)
        self.assertIn("inherits the marker transitively", text)


class EventSourcingTests(unittest.TestCase):
    def test_state_is_defined_as_a_reduction_of_the_log(self) -> None:
        text = normalised(SPEC)
        self.assertIn("state is a function of the event log", text)

    def test_reducers_are_required_to_be_deterministic(self) -> None:
        text = normalised(SPEC)
        self.assertIn("reducers are deterministic", text)

    def test_branching_is_a_log_operation(self) -> None:
        text = normalised(SPEC)
        self.assertIn("branching is a log operation", text)


class ConcordiaReviewTests(unittest.TestCase):
    """Phase A item 8: the API review must be real and its finding recorded."""

    def test_review_names_the_pinned_revision(self) -> None:
        self.assertIn(PINNED_CONCORDIA_REVISION, read(SPEC))

    def test_finding_records_that_world_state_is_llm_generated(self) -> None:
        text = normalised(SPEC)
        self.assertIn("llm-generated", text)
        self.assertIn("worldstate", text)
        self.assertIn("generativeclock", text)

    def test_finding_states_concordia_components_are_not_the_canonical_store(self) -> None:
        text = normalised(SPEC)
        self.assertIn("not", text)
        self.assertRegex(text, r"`?worldstate`?/`?generativeclock`? components are not the canonical store")

    def test_mandatory_resolver_seam_is_stated(self) -> None:
        text = normalised(SPEC)
        self.assertIn(
            "no llm output may enter the event log except through the deterministic resolver",
            text,
        )

    def test_resolver_must_return_an_unresolved_outcome_not_an_improvisation(self) -> None:
        text = normalised(SPEC)
        self.assertIn("explicit unresolved outcome", text)

    def test_the_resolve_seam_is_identified_in_concordias_api(self) -> None:
        body = read(SPEC)
        self.assertIn("OutputType.RESOLVE", body)
        self.assertIn("post_act", body)


class TheoryDivisionTests(unittest.TestCase):
    #: The theories the issue requires to stay distinct.
    THEORIES = (
        "deleuze",
        "luhmann",
        "laclau",
        "castells",
        "leifeld",
        "sna",
        "pcm",
    )

    def test_every_theory_has_a_recorded_role(self) -> None:
        text = normalised(SPEC)
        for theory in self.THEORIES:
            with self.subTest(theory=theory):
                self.assertIn(theory, text)

    def test_theories_are_not_collapsed(self) -> None:
        text = normalised(SPEC)
        self.assertIn("collapse", text)
        self.assertIn("proposal for the author to confirm", text)

    def test_assemblage_is_not_redefined_as_a_network_community(self) -> None:
        text = normalised(SPEC)
        self.assertIn("not the same thing as a network community", text)


class DeferRegisterTests(unittest.TestCase):
    def test_defer_register_exists(self) -> None:
        self.assertIn("DEFER register", read(SPEC))

    def test_register_carries_a_meaningful_number_of_deferred_decisions(self) -> None:
        ids = set(re.findall(r"DEFER-\d+", read(SPEC)))
        self.assertGreaterEqual(
            len(ids), 10, f"expected >=10 deferred decisions, found {sorted(ids)}"
        )

    def test_every_defer_entry_names_an_owner(self) -> None:
        """A 'deferred' with no owner is just an abandoned question."""
        section = re.search(
            r"(?ms)^## 11\. DEFER register.*?(?=^## 12\.)", read(SPEC)
        )
        self.assertIsNotNone(section, "could not locate the DEFER register section")
        assert section is not None
        rows = [
            line
            for line in section.group(0).splitlines()
            if line.strip().startswith("| DEFER-")
        ]
        self.assertGreaterEqual(len(rows), 10, "DEFER register rows are missing")
        for row in rows:
            with self.subTest(row=row[:40]):
                self.assertIn("author", row.lower(), f"no owner on: {row[:80]}")

    def test_tabletop_macro_policy_is_deferred(self) -> None:
        text = normalised(SPEC)
        self.assertIn("defer-9", text)
        self.assertIn("social mechanics are in", text)

    def test_spec_records_that_phase_b_is_implemented(self) -> None:
        """The spec must not still claim Phase B is unbuilt once it exists.

        A specification that drifts from the code is how a reader ends up
        implementing something that already exists — the duplicate-work failure the
        repository's own workflow warns about.
        """
        text = normalised(SPEC)
        self.assertIn("implemented", text)
        self.assertIn("src/simulation/", text)
        # normalised() strips underscores (they are markdown emphasis here), so
        # compare against the normalised filenames rather than the literal ones.
        for module in ("events.py", "sqlite_store.py", "world_state.py", "engine.py"):
            with self.subTest(module=module):
                self.assertIn(module.replace("_", ""), text)

    def test_phase_b_status_is_not_overstated(self) -> None:
        """It must say what Phase B does NOT contain, not just that it landed."""
        text = normalised(SPEC)
        self.assertIn("no graph module yet", text)

    def test_phase_dependencies_are_stated(self) -> None:
        text = normalised(SPEC)
        for dependency in ("phase b", "phase c", "phase e"):
            with self.subTest(phase=dependency):
                self.assertIn(dependency, text)


if __name__ == "__main__":
    unittest.main()
