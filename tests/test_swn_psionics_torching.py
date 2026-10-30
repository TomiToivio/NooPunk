"""SWN psionics: Torching and the restricted/unrestricted package distinction.

Stars Without Number Revised has no verified SRD licence, so these tests exercise the *mechanics*
(Effort arithmetic, the torching table, package restrictions) and never a power name or description.
"""
import unittest

from src.rules.swn_psionics import (
    ATTRIBUTE_FLOOR,
    DISCIPLINES,
    Duration,
    Psychic,
    PsiRulesError,
    TORCHING_TABLE,
)


class TorchingTest(unittest.TestCase):
    def test_the_table_is_a_d6(self):
        self.assertEqual(sorted(TORCHING_TABLE), [1, 2, 3, 4, 5, 6])

    def test_torching_grants_effort_that_may_exceed_the_maximum(self):
        p = Psychic(wisdom=12, constitution=12, disciplines={"Telepathy": 2})
        base = p.capacity
        result = p.torch(die=6, round_number=1)
        self.assertEqual(result["granted"], 1)
        self.assertEqual(result["effect"], "none")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(p.capacity, base + 1)  # over the normal maximum, for the scene
        self.assertGreater(p.free, 0)

    def test_a_burn_costs_the_attribute_the_table_names(self):
        p = Psychic(wisdom=12, constitution=14, disciplines={"Telepathy": 1})
        result = p.torch(die=3, round_number=1)
        self.assertEqual(result["attribute_lost"], "CON")
        self.assertEqual(p.constitution, 13)
        self.assertEqual(result["status"], "ok")

    def test_torching_is_once_per_round(self):
        p = Psychic(12, 12, {"Telepathy": 1})
        p.torch(die=6, round_number=4)
        with self.assertRaises(PsiRulesError):
            p.torch(die=6, round_number=4)
        p.torch(die=6, round_number=5)  # a new round is a new torch

    def test_wisdom_below_the_floor_is_feral_and_constitution_is_death(self):
        p = Psychic(4, 12, {"Telepathy": 1})
        self.assertEqual(p.torch(die=1, round_number=1)["status"], "ok")
        self.assertEqual(p.torch(die=1, round_number=2)["status"], "feral")
        q = Psychic(12, 3, {"Telepathy": 1})
        self.assertEqual(q.torch(die=3, round_number=1)["status"], "dead")
        self.assertEqual(ATTRIBUTE_FLOOR, 3)

    def test_a_choice_result_needs_a_named_attribute(self):
        p = Psychic(12, 12, {"Telepathy": 1})
        with self.assertRaises(PsiRulesError):
            p.torch(die=5, round_number=1)
        result = p.torch(die=5, round_number=1, choice="DEX")
        self.assertEqual(result["attribute_lost"], "DEX")
        self.assertEqual(result["sheet_must_apply"], "DEX")

    def test_the_torched_point_and_its_bonus_end_with_the_scene(self):
        p = Psychic(12, 12, {"Telepathy": 1})
        base = p.capacity
        p.torch(die=6, round_number=1)
        self.assertEqual(p.capacity, base + 1)
        p.end_scene()
        self.assertEqual(p.capacity, base)
        p.torch(die=6, round_number=2)
        p.rest()
        self.assertEqual(p.capacity, base)

    def test_torching_survives_a_snapshot_round_trip(self):
        p = Psychic(12, 12, {"Telepathy": 1}, {"swn_partial_psychic"})
        p.torch(die=1, round_number=3)
        restored = Psychic.from_snapshot(p.snapshot())
        self.assertEqual(restored.snapshot(), p.snapshot())
        self.assertEqual(restored.capacity, p.capacity)


class PackageRestrictionTest(unittest.TestCase):
    def test_an_unrestricted_psychic_may_learn_any_discipline(self):
        p = Psychic(12, 12, {"Telepathy": 1}, {"swn_psychic"})
        for discipline in DISCIPLINES:
            self.assertTrue(p.can_learn(discipline))

    def test_a_partial_psychic_may_master_one_and_no_other(self):
        p = Psychic(12, 12, {"Telepathy": 1}, {"swn_partial_psychic"},
                    restricted_discipline="Telepathy")
        self.assertTrue(p.can_learn("Telepathy"))
        for other in DISCIPLINES:
            if other != "Telepathy":
                self.assertFalse(p.can_learn(other))
        self.assertFalse(p.can_learn("NotADiscipline"))

    def test_a_commitment_still_needs_the_skill_it_names(self):
        p = Psychic(12, 12, {"Telepathy": 1}, {"swn_partial_psychic"},
                    restricted_discipline="Telepathy")
        p.commit("contact", "Telepathy", duration=Duration.SCENE)
        with self.assertRaises(PsiRulesError):
            p.commit("far_sight", "Precognition", duration=Duration.SCENE)


if __name__ == "__main__":
    unittest.main()
