"""Conditions, not a track (#698; D46–D48). Includes the refusal test D48 demands."""

from __future__ import annotations

import inspect

import pytest

from src.rules.mental_load import (
    Choice,
    Condition,
    ConditionError,
    ExposureLayer,
    ParadigmShock,
    WorldviewState,
    offer_choices,
    resolve_shock,
)


def condition(**overrides: object) -> Condition:
    base: dict[str, object] = {
        "id": "c1",
        "layer": ExposureLayer.PERSISTENT_CONDITION,
        "statement": "the ward breathes when nobody is watching",
        "severity": "AUTHOR-SUPPLIED",
        "constrains": ("Perceive in the hospital",),
        "clears_when": "a WWN project proves what the breathing is",
    }
    base.update(overrides)
    return Condition(**base)  # type: ignore[arg-type]


class TestConditionsAreNotATrack:
    def test_there_is_no_numeric_field_to_deplete(self):
        fields = condition().__dataclass_fields__
        numeric = [name for name, f in fields.items()
                   if f.type in ("int", "float")]
        assert numeric == [], f"a condition must not carry a number to drain: {numeric}"

    def test_severity_is_author_supplied_not_enumerated(self):
        # D46 leaves the severity list open; the module must accept a name and not invent a scale.
        assert condition(severity="whatever the author decides").severity
        with pytest.raises(ConditionError):
            condition(severity="   ")

    def test_a_condition_must_constrain_a_choice(self):
        with pytest.raises(ConditionError):
            condition(constrains=())

    def test_a_condition_must_say_what_clears_it(self):
        with pytest.raises(ConditionError):
            condition(clears_when="")

    def test_a_world_view_is_not_a_condition(self):
        # D47: conflating layers 3 and 4 is exactly what makes sanity rules mushy.
        with pytest.raises(ConditionError):
            condition(layer=ExposureLayer.WORLDVIEW_STATE)


SHOCK = ParadigmShock(
    belief="the ward is a psychiatric hospital",
    evidence="the patients' files are written in the future tense",
    choices=(
        Choice(id="accept", label="accept the reframe",
               cost="the ward is something else, and you knew",
               resulting_state=WorldviewState.REFRAMED),
        Choice(id="hold", label="hold the belief",
               cost="denial: one band against Medicine in this building",
               resulting_state=WorldviewState.FRACTURED),
    ),
)


class TestTheChoiceIsThePlayer:
    def test_two_branches_with_different_costs(self):
        first, second = offer_choices(SHOCK)
        assert first.id != second.id
        assert first.cost != second.cost

    def test_resolving_requires_naming_a_branch(self):
        with pytest.raises(TypeError):
            resolve_shock(SHOCK)  # type: ignore[call-arg]  # deliberately omitted

    def test_an_unknown_branch_is_refused(self):
        with pytest.raises(ConditionError):
            resolve_shock(SHOCK, choice_id="whatever the referee prefers")

    def test_each_branch_produces_its_own_state(self):
        accept = resolve_shock(SHOCK, choice_id="accept")
        hold = resolve_shock(SHOCK, choice_id="hold")
        assert accept.state_after is WorldviewState.REFRAMED
        assert hold.state_after is WorldviewState.FRACTURED
        assert accept.state_after is not hold.state_after

    def test_the_record_carries_both_layers(self):
        record = resolve_shock(SHOCK, choice_id="accept")
        assert record.events[0].startswith("layer 1")
        assert record.events[1].startswith("layer 4")

    def test_a_choice_cannot_leave_the_state_unchanged_by_accident(self):
        # A branch that resolved to 'received' would be a silent no-op; the type forbids it.
        with pytest.raises(ConditionError):
            Choice(id="x", label="l", cost="c", resulting_state=WorldviewState.RECEIVED)


class TestRefusalTestD48:
    """No code path may change a world view as the result of a roll."""

    def test_no_public_function_accepts_randomness(self):
        import src.rules.mental_load as module

        offenders = []
        for name, function in vars(module).items():
            if not inspect.isfunction(function) or name.startswith("_"):
                continue
            params = [p.lower() for p in inspect.signature(function).parameters]
            if {"rng", "random", "die", "dice", "roll", "seed"} & set(params):
                offenders.append(name)
        assert offenders == [], f"these could let a roll decide a conviction: {offenders}"

    def test_the_module_refuses_to_import_a_randomness_api(self):
        import src.rules.mental_load as module

        source = inspect.getsource(module)
        assert "import random" not in source
        assert "from random" not in source
        assert "secrets" not in source
