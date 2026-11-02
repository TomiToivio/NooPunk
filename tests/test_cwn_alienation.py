"""Cyber Alienation, chrome syndromes and cyber-induced psychosis (#1068).

Source: CWN Deluxe printed pp. 226–231. The rules are optional, so the tests check both halves of that
claim: the mechanics match the book, and importing this module changes nothing about default cyberware
behaviour (it imports only the standard library).
"""
import unittest

from src.rules.cwn_alienation import (
    SYNDROMES,
    THERAPY_COST,
    Alienation,
    AlienationError,
    rescue_from_psychosis,
    system_cost,
)


class SystemCostTests(unittest.TestCase):
    def test_strain_rounds_up_and_nerveware_adds_two(self):
        self.assertEqual(system_cost(0.5), 1, "half a point of strain still costs a point")
        self.assertEqual(system_cost(2), 2)
        self.assertEqual(system_cost(1, nerve=True), 3, "Nerveware is +2 on top of its own cost")

    def test_discounted_sense_mods_still_cost_one(self):
        self.assertEqual(system_cost(0, discounted_sense=True), 1)
        self.assertEqual(system_cost(0.5, discounted_sense=True), 1)

    def test_a_negative_cost_is_refused(self):
        with self.assertRaises(AlienationError):
            system_cost(-1)


class ScoreAndCeilingTests(unittest.TestCase):
    def test_ceiling_is_wisdom_plus_syndromes(self):
        person = Alienation(wisdom=12)
        self.assertEqual(person.maximum, 12)
        person.take_syndrome("distant")
        self.assertEqual(person.maximum, 15, "Distant adds 3 to the allowed maximum")

    def test_score_above_the_ceiling_is_psychosis(self):
        person = Alienation(wisdom=3)
        person.install(2)
        person.install(2)
        self.assertTrue(person.broken)

    def test_installing_chrome_raises_both_score_and_floor(self):
        person = Alienation(wisdom=10)
        person.install(2)
        self.assertEqual((person.score, person.floor), (2, 2))

    def test_removing_chrome_lowers_the_floor_and_never_leaves_it_above_the_score(self):
        person = Alienation(wisdom=10)
        person.install(3)
        person.score += 2  # gained through failed checks
        person.uninstall(3)
        self.assertEqual(person.floor, 0)
        self.assertEqual(person.score, 2, "relief cannot take the score below the new floor")

    def test_a_syndrome_cannot_be_taken_twice(self):
        person = Alienation(wisdom=10, syndromes=["brutal"])
        with self.assertRaises(AlienationError):
            person.take_syndrome("brutal")

    def test_unknown_syndromes_are_refused(self):
        with self.assertRaises(AlienationError):
            Alienation(wisdom=10, syndromes=["impossible"])
        with self.assertRaises(AlienationError):
            Alienation(wisdom=10).take_syndrome("impossible")


class CheckTests(unittest.TestCase):
    def test_rolling_at_or_under_the_score_gains_a_point(self):
        person = Alienation(wisdom=14, score=5)
        self.assertEqual(person.check(5)["gained"], 1, "equal to the score still counts")
        self.assertEqual(person.score, 6)

    def test_rolling_over_the_score_gains_nothing(self):
        person = Alienation(wisdom=14, score=5)
        self.assertEqual(person.check(6)["gained"], 0)
        self.assertEqual(person.score, 5)

    def test_crossing_the_ceiling_asks_for_a_mental_save(self):
        person = Alienation(wisdom=2, score=2)
        result = person.check(1)
        self.assertTrue(result["mental_save"])
        self.assertEqual(person.mental_save(success=True), "syndrome")
        self.assertEqual(person.mental_save(success=False), "psychosis")

    def test_a_save_is_only_called_for_past_the_ceiling(self):
        person = Alienation(wisdom=14, score=1)
        with self.assertRaises(AlienationError):
            person.mental_save(success=True)

    def test_a_roll_outside_the_d20_is_refused(self):
        with self.assertRaises(AlienationError):
            Alienation(wisdom=10).check(0)
        with self.assertRaises(AlienationError):
            Alienation(wisdom=10).check(21)


class TherapyTests(unittest.TestCase):
    def test_a_week_costs_two_thousand_and_drops_one_point(self):
        person = Alienation(wisdom=10, score=4)
        result = person.therapy_week()
        self.assertEqual(result, {"dropped": 1, "score": 3, "cost": THERAPY_COST})

    def test_therapy_cannot_undo_what_the_chrome_costs(self):
        person = Alienation(wisdom=10)
        person.install(2)
        self.assertEqual(person.therapy_week(), {"dropped": 0, "score": 2, "cost": 0})

    def test_therapy_stops_at_the_floor_and_not_at_zero(self):
        person = Alienation(wisdom=10)
        person.install(1)
        person.score = 3
        self.assertEqual(person.therapy_week()["score"], 2)
        self.assertEqual(person.therapy_week()["score"], 1)
        self.assertEqual(person.therapy_week()["dropped"], 0)


class RescueTests(unittest.TestCase):
    def test_chrome_must_come_out_first(self):
        result = rescue_from_psychosis(wisdom=12, score=5, chrome_removed=False,
                                       therapist_skill=2, die=18)
        self.assertFalse(result["rescued"])
        self.assertIn("chrome", result["reason"])

    def test_alienation_must_be_below_wisdom_first(self):
        result = rescue_from_psychosis(wisdom=12, score=12, chrome_removed=True,
                                       therapist_skill=2, die=18)
        self.assertFalse(result["rescued"])

    def test_therapist_skill_is_the_bonus_on_a_mental_save(self):
        weak = rescue_from_psychosis(wisdom=12, score=4, chrome_removed=True, therapist_skill=1, die=13)
        strong = rescue_from_psychosis(wisdom=12, score=4, chrome_removed=True, therapist_skill=2, die=13)
        self.assertFalse(weak["rescued"], "14 falls short of the 15 Mental save")
        self.assertTrue(strong["rescued"], "15 succeeds")


class SyndromeTableTests(unittest.TestCase):
    def test_the_book_table_is_complete(self):
        expected = {"brutal": 4, "candid": 3, "cold": 4, "distant": 3, "exultant": 3, "fearless": 4,
                    "hypervigilant": 3, "murderous": 6, "ravenous": 4, "savage": 5, "secretive": 3,
                    "stressed": 3}
        self.assertEqual({name: data["max_bonus"] for name, data in SYNDROMES.items()}, expected)
        for name, data in SYNDROMES.items():
            self.assertTrue(data["effect"], f"{name} must say what it does")

    def test_the_module_is_optional_and_dependency_free(self):
        import inspect

        import src.rules.cwn_alienation as module

        source = inspect.getsource(module)
        for import_line in ("import src.rules.cwn_cyberware", "from .cwn_cyberware",
                            "from src.rules.cwn_cyberware"):
            self.assertNotIn(import_line, source,
                             "Alienation must not attach itself to the default cyberware rules")


if __name__ == "__main__":
    unittest.main()
