"""Psionics: Effort, commitment lifecycle, torching and the training gate.

The subsystem's shape is adopted (``rulebook/WITHOUT_NUMBER_BASELINE.md`` §2); its numbers and its
technique catalogue are provisional NoöPunk content.

This suite also carries the assertions of the model it supersedes (#648's ``swn_psionics.Psychic``):
named commitment keys, unique-key protection, the ACTIVE/SCENE/DAY lifecycle, snapshot/restore,
scene and rest recovery, and rejection of malformed restores. Superseding a module is not a licence
to drop its coverage.
"""
from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rules import psionics as psi
from rules import wn_core as wn

CATALOGUE = psi.load_catalogue()
Duration = psi.Duration


def practitioner(**skills: int) -> psi.Practitioner:
    return psi.Practitioner(
        attributes={"STR": 10, "DEX": 12, "CON": 10, "INT": 14, "WIS": 14, "CHA": 9},
        skills=dict(skills),
    )


class CatalogueTests(unittest.TestCase):
    def test_the_six_disciplines_are_the_adopted_ones(self) -> None:
        self.assertEqual(CATALOGUE.disciplines, psi.PSI_DISCIPLINES)
        self.assertEqual(len(psi.PSI_DISCIPLINES), 6)

    def test_every_discipline_has_exactly_one_core_technique(self) -> None:
        cores = {core.discipline for core in CATALOGUE.cores.values()}
        self.assertEqual(cores, set(psi.PSI_DISCIPLINES))
        for core in CATALOGUE.cores.values():
            self.assertEqual(core.min_skill, 0)
            self.assertTrue(core.core)

    def test_every_technique_is_legal_and_playable(self) -> None:
        self.assertGreaterEqual(len(CATALOGUE.techniques), 18)
        for technique in CATALOGUE.techniques.values():
            with self.subTest(technique=technique.id):
                self.assertIn(technique.discipline, psi.PSI_DISCIPLINES)
                self.assertGreaterEqual(technique.min_skill, 1)  # level 0 is the core's job
                self.assertLessEqual(technique.min_skill, wn.MAX_SKILL_LEVEL)
                self.assertIn(technique.effort, ("none", "commit_scene", "commit_day"))
                self.assertIn(technique.duration, psi.EFFORT_DURATIONS)
                self.assertTrue(technique.effect.strip())

    def test_a_missing_technique_is_an_error_not_an_empty_power(self) -> None:
        with self.assertRaises(psi.PsiError):
            CATALOGUE.get("no_such_technique")


class EffortCapacityTests(unittest.TestCase):
    def test_maximum_effort_is_one_plus_the_better_modifier_plus_the_best_skill(self) -> None:
        self.assertEqual(psi.max_effort({"WIS": 14, "CON": 10}, {"Telepathy": 1}), 3)
        self.assertEqual(psi.max_effort({"WIS": 9, "CON": 18}, {"Telepathy": 1, "Precognition": 0}), 4)
        self.assertEqual(psi.max_effort({"WIS": 14, "CON": 10}, {}), 2)
        self.assertEqual(psi.max_effort({"WIS": 5, "CON": 4}, {}), 0)

    def test_an_untrained_discipline_does_not_reduce_the_pool(self) -> None:
        self.assertEqual(psi.max_effort({"WIS": 10, "CON": 10}, {"Telepathy": wn.UNTRAINED}), 1)


class CommitmentLifecycleTests(unittest.TestCase):
    """#648's lifecycle, carried over: named keys and no early refunds."""

    def test_three_commitment_types_coexist_and_scene_day_do_not_refund(self) -> None:
        pool = psi.EffortPool(maximum=3)
        pool.commit("contact", Duration.ACTIVE)
        pool.commit("insight", Duration.SCENE)
        pool.commit("vision", Duration.DAY)
        self.assertEqual(pool.available, 0)
        with self.assertRaises(psi.PsiError):
            pool.release("vision")
        with self.assertRaises(psi.PsiError):
            pool.commit("extra", Duration.SCENE)
        self.assertTrue(pool.release("contact"))
        self.assertEqual(pool.available, 1)
        pool.end_scene()
        self.assertEqual(pool.available, 2)          # the day commitment survives the scene
        self.assertEqual(pool.committed_day, 1)
        pool.rest()
        self.assertEqual(pool.available, pool.maximum)

    def test_keys_are_unique_and_nonempty(self) -> None:
        pool = psi.EffortPool(maximum=3)
        pool.commit("contact", Duration.SCENE)
        with self.assertRaises(psi.PsiError):
            pool.commit("contact", Duration.SCENE)
        with self.assertRaises(psi.PsiError):
            pool.commit("", Duration.SCENE)

    def test_an_unknown_duration_is_refused(self) -> None:
        with self.assertRaises(psi.PsiError):
            psi.EffortPool(maximum=3).commit("x", "hour")

    def test_releasing_an_unknown_key_is_false_not_an_error(self) -> None:
        self.assertFalse(psi.EffortPool(maximum=3).release("never-committed"))

    def test_torched_effort_is_extra_capacity_for_the_scene(self) -> None:
        pool = psi.EffortPool(maximum=1)
        pool.commit("held", Duration.SCENE)
        self.assertEqual(pool.available, 0)
        pool.torched += 1
        self.assertEqual(pool.available, 1)
        pool.end_scene()
        self.assertEqual(pool.torched, 0)


class SnapshotTests(unittest.TestCase):
    """#648's persistence, carried over: a save must not silently reset the pool."""

    def test_a_snapshot_round_trips(self) -> None:
        pool = psi.EffortPool(maximum=3)
        pool.commit("oracle", Duration.DAY)
        pool.commit("thread", Duration.SCENE)
        restored = psi.EffortPool.from_snapshot(pool.snapshot())
        self.assertEqual(restored.snapshot(), pool.snapshot())
        self.assertEqual(restored.available, pool.available)
        restored.end_scene()
        self.assertEqual(restored.available, 2)   # the scene point returns, the day reserve stays
        self.assertEqual(restored.committed_day, 1)
        restored.rest()
        self.assertEqual(restored.available, restored.maximum)

    def test_a_malformed_snapshot_is_an_error(self) -> None:
        with self.assertRaises(psi.PsiError):
            psi.EffortPool.from_snapshot({"reservations": {"bad": {"amount": 1, "duration": "hour"}}})
        with self.assertRaises(psi.PsiError):
            psi.EffortPool.from_snapshot({"maximum": 1,
                                          "reservations": {"over": {"amount": 99, "duration": "day"}}})

    def test_bad_scores_and_foreign_disciplines_are_refused(self) -> None:
        with self.assertRaises(psi.PsiError):
            psi.Practitioner(attributes={"WIS": 2, "CON": 10}, skills={"Telepathy": 0})
        with self.assertRaises(psi.PsiError):
            psi.Practitioner(attributes={"WIS": 10, "CON": 10}, skills={"Foretelling": 1})


class TorchingTests(unittest.TestCase):
    def test_torching_grants_effort_above_the_maximum(self) -> None:
        character = practitioner()
        character.pool.maximum = 1
        character.pool.commit("held", Duration.SCENE)
        self.assertEqual(character.pool.available, 0)
        character.torch(die=6)
        self.assertEqual(character.pool.available, 1)

    def test_the_d6_table_charges_an_attribute(self) -> None:
        character = practitioner()
        self.assertEqual(character.torch(die=1).attribute_lost, "WIS")
        self.assertEqual(character.attributes["WIS"], 13)
        self.assertEqual(character.torch(die=3).attribute_lost, "CON")
        self.assertEqual(character.attributes["CON"], 9)
        harmless = character.torch(die=6)
        self.assertTrue(harmless.harmless)
        self.assertFalse(harmless.feral)

    def test_a_psychic_pushed_below_wisdom_three_is_feral(self) -> None:
        character = psi.Practitioner(
            attributes={"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 4, "CHA": 10},
            skills={"Telepathy": 0},
        )
        self.assertFalse(character.torch(die=1).feral)
        self.assertTrue(character.torch(die=1).feral)


class TrainingGateTests(unittest.TestCase):
    def test_a_core_technique_needs_only_training_at_level_zero(self) -> None:
        character = practitioner(Telepathy=0)
        self.assertTrue(character.may_use(CATALOGUE.get("surface_read")))
        character.use("surface_read")
        self.assertEqual(character.pool.committed, 0)

    def test_an_untaught_technique_is_refused_as_a_permission_failure(self) -> None:
        character = practitioner(Telepathy=0)
        self.assertFalse(character.may_use(CATALOGUE.get("thread")))
        with self.assertRaises(psi.PsiError) as caught:
            character.use("thread")
        self.assertIn("never trained", str(caught.exception))
        self.assertEqual(character.pool.committed, 0)

    def test_learning_enforces_the_minimum_skill_level(self) -> None:
        character = practitioner(Telepathy=0)
        with self.assertRaises(psi.PsiError):
            character.learn(CATALOGUE.get("thread"))
        character.skills = dict(character.skills, Telepathy=1)
        character.learn(CATALOGUE.get("thread"))
        self.assertIn("thread", character.known)

    def test_a_core_technique_is_never_learned(self) -> None:
        with self.assertRaises(psi.PsiError):
            practitioner(Telepathy=1).learn(CATALOGUE.get("surface_read"))

    def test_using_a_power_commits_the_duration_its_record_names(self) -> None:
        character = practitioner(Telepathy=2)
        character.use("thread")
        self.assertEqual(character.pool.committed_scene, 1)
        self.assertIn("thread", character.pool.reservations)
        character.use("command")
        self.assertEqual(character.pool.committed_day, 1)

    def test_the_same_power_can_be_held_twice_under_distinct_keys(self) -> None:
        character = practitioner(Telepathy=2)
        character.pool.maximum = 5
        character.use("thread")
        character.use("thread")
        self.assertEqual(sorted(character.pool.reservations), ["thread", "thread#2"])

    def test_a_technique_with_a_check_resolves_on_the_one_kernel(self) -> None:
        character = practitioner(Precognition=1)
        check = character.check(CATALOGUE.get("hunch"), dice=(4, 4))
        self.assertIsInstance(check, wn.Check)
        self.assertEqual(check.skill_level, 1)
        self.assertEqual(check.total, 8 + 1 + 1)  # 2d6 8 + INT 14 = +1 + Precognition 1

    def test_a_technique_without_a_check_refuses_to_roll_one(self) -> None:
        with self.assertRaises(psi.PsiError):
            practitioner(Teleportation=1).check(CATALOGUE.get("blink"))


if __name__ == "__main__":
    unittest.main()
