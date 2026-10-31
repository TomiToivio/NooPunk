"""#897 item 4: a NoöPunk mod may not change a CWN outcome.

The lock (`docs/rules/RULES_BASIS_LOCK.md`) says mods read resolved CWN state and add narrative state.
That is only true if something fails when a mod does otherwise, and these tests are that something:

* a well-behaved mod leaves the mechanical outcome *identical* — the parity guard;
* a mod that declares ``changes_core_mechanics`` is refused before it runs;
* a "narrative" effect may not shadow a baseline key (``total``, ``dv``, ``success``) — the quiet way a
  mod would rewrite a resolution;
* the outcome handed to a mod is read-only, so mutation raises instead of happening;
* two mods cannot collide with each other's narrative state;
* the shipped registry (`data/mods/registry.json`) lists only overlays.

Executable code only (#271): every assertion below calls the adapter.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.rules.mod_boundary import (
    BaselineViolation,
    Mod,
    ModEffect,
    apply_mods,
    validate_registry,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "mods" / "registry.json"

#: A resolved CWN skill check, as the baseline hands it to an overlay.
OUTCOME = {"stat": 3, "skill": 2, "roll": 7, "total": 12, "dv": 13, "success": False}


def narrative(state: dict) -> Mod:
    return Mod(name="noosphere_psyche", resolve=lambda outcome, current: ModEffect(state))


class ParityTests(unittest.TestCase):
    def test_a_mod_leaves_the_cwn_outcome_identical(self):
        before = dict(OUTCOME)
        outcome, mods = apply_mods(OUTCOME, [narrative({"exposure": 2})])
        self.assertEqual(outcome, before, "the resolved CWN outcome must not move")
        self.assertEqual(OUTCOME, before, "the caller's outcome must not be mutated")
        self.assertEqual(mods["noosphere_psyche"], {"exposure": 2})

    def test_no_mods_is_the_baseline(self):
        outcome, mods = apply_mods(OUTCOME, [])
        self.assertEqual(outcome, OUTCOME)
        self.assertEqual(mods, {})

    def test_a_mod_sees_the_resolved_state_it_is_given(self):
        seen: dict = {}

        def spy(resolved, current):
            seen.update(resolved)
            seen["narrative"] = dict(current)
            return ModEffect({"read": True})

        apply_mods(OUTCOME, [Mod("spy", spy)], state={"reputation": {"UNSA": 1}})
        self.assertEqual(seen["total"], OUTCOME["total"])
        self.assertEqual(seen["narrative"], {"reputation": {"UNSA": 1}})


class BaselineGuards(unittest.TestCase):
    def test_a_mod_that_declares_a_rules_change_is_refused_before_it_runs(self):
        ran: list[bool] = []
        mod = Mod("rewrite_the_ladder", lambda o, c: ran.append(True),
                  changes_core_mechanics=True)
        with self.assertRaises(BaselineViolation):
            apply_mods(OUTCOME, [mod])
        self.assertEqual(ran, [], "a refused mod must not run at all")

    def test_a_narrative_effect_may_not_shadow_a_baseline_key(self):
        for key in ("total", "dv", "success"):
            with self.subTest(key=key):
                with self.assertRaises(BaselineViolation):
                    apply_mods(OUTCOME, [Mod("shadow", lambda o, c: {key: 99})])

    def test_the_outcome_handed_to_a_mod_is_read_only(self):
        def mutate(resolved, current):
            resolved["total"] = 99  # type: ignore[index]
            return ModEffect({})

        with self.assertRaises(TypeError):
            apply_mods(OUTCOME, [Mod("mutator", mutate)])

    def test_a_mod_without_a_name_is_rejected(self):
        with self.assertRaises(ValueError):
            Mod("   ", lambda o, c: ModEffect({}))


class CompositionTests(unittest.TestCase):
    def test_two_mods_namespace_their_own_state(self):
        mods = [
            Mod("ideology_factions", lambda o, c: {"stance": "solidary"}),
            Mod("relationships_reputation", lambda o, c: {"stance": "obligated"}),
        ]
        _, narrative_state = apply_mods(OUTCOME, mods)
        self.assertEqual(narrative_state["ideology_factions"], {"stance": "solidary"})
        self.assertEqual(narrative_state["relationships_reputation"], {"stance": "obligated"})

    def test_mods_see_each_other_in_order(self):
        order: list[str] = []

        def first(outcome, current):
            order.append(f"first:{sorted(current)}")
            return {"marked": True}

        def second(outcome, current):
            order.append(f"second:{sorted(current)}")
            return {}

        apply_mods(OUTCOME, [Mod("a", first), Mod("b", second)])
        self.assertEqual(order, ["first:[]", "second:['a']"])


class RegistryTests(unittest.TestCase):
    def test_the_shipped_registry_lists_overlays_only(self):
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
        names = validate_registry(payload["mods"])
        self.assertEqual(len(names), len(set(names)))
        self.assertIn("noosphere_psyche", names)
        self.assertFalse(payload["baseline"]["may_be_changed_by_a_mod"])

    def test_a_registry_entry_claiming_the_baseline_is_refused(self):
        with self.assertRaises(BaselineViolation):
            validate_registry([{"name": "new_core", "changes_core_mechanics": True}])

    def test_duplicate_mod_names_are_refused(self):
        with self.assertRaises(BaselineViolation):
            validate_registry([{"name": "same"}, {"name": "same"}])


if __name__ == "__main__":
    unittest.main()
