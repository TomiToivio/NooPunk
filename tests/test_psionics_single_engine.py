"""One Effort engine, one technique table, one package vocabulary (#1105, P0-A first checkbox).

#1105 opens by requiring `src/rules/swn_psionics.py` and `src/rules/psionics.py` to be "**one** native
implementation with thin interfaces". They were close — `psionics.Psychic` already subclassed the engine —
but three seams had rotted, and each is the kind that only shows up in play:

* the technique table was a hand-written three-id map consulted *before* the twenty-entry catalogue, so a
  catalogue technique the gate accepted could still be unresolvable;
* the duration vocabulary existed twice (a dict here, a dict there) and the module's public words
  (`none`/`scene`/`day`) differed from both;
* `Psychic.from_snapshot` rebuilt the object from four arguments and **silently dropped** the torched
  Effort bonus, the torch round and the Partial Psychic's discipline restriction.

These tests assert the seams cannot come apart again: equality between the two modules, not literals that
could be copied.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import psionics, swn_psionics  # noqa: E402


class OneEngineTests(unittest.TestCase):
    def test_the_gated_type_is_the_engine_with_a_gate(self) -> None:
        """`psionics.Psychic` must add permission checking, not a second Effort implementation."""
        self.assertTrue(issubclass(psionics.Psychic, swn_psionics.Psychic))
        for name in ("capacity", "free", "commit", "release", "end_scene", "rest", "torch", "snapshot"):
            self.assertTrue(hasattr(psionics.Psychic, name), name)

    def test_capacity_is_the_printed_formula(self) -> None:
        """SWN p.30: 1 + best(WIS, CON) modifier + highest discipline rank, minimum 1."""
        psychic = psionics.Psychic(14, 10, {"Telepathy": 2}, {"swn_psychic"})
        expected = max(1, 1 + max(swn_psionics.attribute_modifier(14),
                                  swn_psionics.attribute_modifier(10)) + 2)
        self.assertEqual(psychic.capacity, expected)
        self.assertGreaterEqual(psychic.capacity, 1)

    def test_the_gate_refuses_before_any_effort_moves(self) -> None:
        operator = psionics.Psychic(14, 10, {"Telepathy": 1})
        with self.assertRaises(swn_psionics.PsiRulesError):
            operator.commit("read", "Telepathy")
        self.assertEqual(operator.free, operator.capacity)

    def test_the_package_vocabularies_are_derived_not_redeclared(self) -> None:
        self.assertLessEqual(psionics.PSYCHIC_PACKAGES, swn_psionics.RESTRICTED_PACKAGES
                             | psionics.UNRESTRICTED_PACKAGES)
        self.assertTrue(psionics.authorized({"swn_partial_psychic"}))
        self.assertTrue(psionics.authorized({"swn_psychic"}))
        self.assertFalse(psionics.authorized({"cwn_soldier"}))

    def test_a_partial_psychic_may_master_one_discipline(self) -> None:
        partial = psionics.Psychic(12, 12, {"Telepathy": 1}, {"swn_partial_psychic"},
                                   restricted_discipline="Telepathy")
        self.assertTrue(partial.can_learn("Telepathy"))
        self.assertFalse(partial.can_learn("Biopsionics"))
        with self.assertRaises(swn_psionics.PsiRulesError):
            partial.commit("heal", "Biopsionics")


class OneTechniqueTableTests(unittest.TestCase):
    def test_the_table_is_the_catalogue(self) -> None:
        """A second hand-written table is how the three-id map and the 20-id catalogue disagreed."""
        catalogue = psionics.load_catalogue()
        projected = {key: (str(entry.get("discipline", "")), int(entry.get("min_skill", 0)))
                     for key, entry in catalogue.items()}
        self.assertEqual(psionics.TECHNIQUES, projected)

    def test_an_id_only_the_catalogue_knows_is_resolvable(self) -> None:
        psychic = psionics.Psychic(16, 12, {"Biopsionics": 2}, {"swn_psychic"})
        psychic.use_technique("stabilise", "staunch")
        self.assertEqual(psychic.free, psychic.capacity - 1)

    def test_an_unknown_id_is_refused_with_no_effort_spent(self) -> None:
        psychic = psionics.Psychic(16, 12, {"Telepathy": 0}, {"swn_psychic"})
        with self.assertRaises(swn_psionics.PsiRulesError):
            psychic.use_technique("nope", "source_book_power")
        self.assertEqual(psychic.free, psychic.capacity)

    def test_the_duration_vocabularies_agree(self) -> None:
        """`effort_duration` (public words) and `DURATION_BY_EFFORT` (engine enums) are one mapping."""
        self.assertEqual(set(psionics._PUBLIC_DURATION), set(psionics.DURATION_BY_EFFORT))
        engine_durations = {duration.value for duration in swn_psionics.Duration}
        public_words = set(psionics._PUBLIC_DURATION.values())
        for technique_id, entry in psionics.load_catalogue().items():
            cost = str(entry.get("effort", "none"))
            self.assertIn(cost, psionics.DURATION_BY_EFFORT, technique_id)
            self.assertIn(cost, psionics._PUBLIC_DURATION, technique_id)
            duration = psionics.DURATION_BY_EFFORT[cost]
            self.assertIn(duration.value, engine_durations)
            self.assertEqual(psionics.effort_duration(technique_id), psionics._PUBLIC_DURATION[cost])
        # The three vocabularies: catalogue words, engine enums, and this module's public words.
        self.assertEqual(public_words - {"none"}, engine_durations - {swn_psionics.Duration.ACTIVE.value})

    def test_effort_commitment_follows_the_catalogue_cost(self) -> None:
        psychic = psionics.Psychic(18, 12, {"Telepathy": 2}, {"swn_psychic"}, scene=4)
        psychic.use_technique("thread", "thread")
        self.assertEqual(psychic.free, psychic.capacity - 1)
        psychic.end_scene()               # a scene commitment is released at the end of the scene
        self.assertEqual(psychic.free, psychic.capacity)


class SnapshotFidelityTests(unittest.TestCase):
    def test_a_torched_partial_psychic_round_trips(self) -> None:
        """The bug this pins: the gated type rebuilt from four arguments and lost the torch state."""
        psychic = psionics.Psychic(12, 12, {"Telekinesis": 1}, {"swn_partial_psychic"},
                                   restricted_discipline="Telekinesis", scene=3)
        result = psychic.torch(die=1, round_number=2)      # 1-2 costs Wisdom
        self.assertEqual(result["attribute_lost"], "WIS")
        self.assertGreater(psychic.torch_bonus, 0)

        restored = psionics.Psychic.from_snapshot(psychic.snapshot())
        self.assertEqual(restored.wisdom, psychic.wisdom)
        self.assertEqual(restored.torch_bonus, psychic.torch_bonus)
        self.assertEqual(restored.torched_round, psychic.torched_round)
        self.assertEqual(restored.restricted_discipline, psychic.restricted_discipline)
        self.assertEqual(restored.scene, psychic.scene)
        self.assertEqual(restored.snapshot(), psychic.snapshot())

    def test_torched_effort_does_not_survive_the_scene(self) -> None:
        psychic = psionics.Psychic(12, 12, {"Telekinesis": 1}, {"swn_psychic"})
        before = psychic.capacity
        psychic.torch(die=6, round_number=1)               # 6: no attribute cost
        self.assertGreater(psychic.capacity, before)
        psychic.end_scene()
        self.assertEqual(psychic.capacity, before)

    def test_unauthorized_reservations_still_fail_to_load(self) -> None:
        psychic = psionics.Psychic(14, 10, {"Telepathy": 0}, {"swn_psychic"})
        psychic.use_technique("read", "surface_read")
        state = psychic.snapshot()
        state["permissions"] = []
        with self.assertRaises(swn_psionics.PsiRulesError):
            psionics.Psychic.from_snapshot(state)


class NoCrossEngineLeakTests(unittest.TestCase):
    def test_wwn_effort_is_a_different_pool(self) -> None:
        """WWN High Mage Effort and SWN psychic Effort are separate resources and must stay so."""
        from rules import wwn_high_mage

        self.assertFalse(hasattr(wwn_high_mage.HighMage, "reservations"),
                         "WWN magic Effort must not share the psychic reservation model")
        source = (ROOT / "src/rules/wwn_high_mage.py").read_text(encoding="utf-8")
        for import_line in ("from .swn_psionics", "import swn_psionics", "from src.rules.swn_psionics"):
            self.assertNotIn(import_line, source,
                             "the magic module must not import the psychic engine; the prose may name it")


if __name__ == "__main__":
    unittest.main()
