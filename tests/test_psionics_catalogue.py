"""The authored technique catalogue and its training gate (#652).

`TECHNIQUES` in ``rules/psionics.py`` answers "is this id authorized by the psychic package". The
catalogue answers the next question: "what does playing it cost, and what does it do". These tests keep
the second from becoming dead data, and keep the gate a *permission* rather than a difficulty.
"""
import unittest

from src.rules.psionics import (
    DISCIPLINES,
    effort_duration,
    load_catalogue,
    may_use,
)


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = load_catalogue()

    def test_every_discipline_has_exactly_one_core(self):
        cores = {entry["discipline"] for entry in self.catalogue.values() if entry.get("core")}
        self.assertEqual(cores, set(DISCIPLINES))

    def test_there_are_techniques_beyond_the_cores(self):
        learned = [entry for entry in self.catalogue.values() if not entry.get("core")]
        self.assertGreaterEqual(len(learned), 18)
        for entry in learned:
            with self.subTest(technique=entry["id"]):
                self.assertIn(entry["discipline"], DISCIPLINES)
                # Rank 0 is legal for a learned pick (premonition is one); the *core* of a discipline
                # is simply the pick nobody has to choose.
                self.assertTrue(0 <= int(entry["min_skill"]) <= 4)
                self.assertTrue(str(entry["effect"]).strip())

    def test_the_catalogue_covers_every_authorized_id(self):
        from src.rules.psionics import TECHNIQUES
        for technique_id in TECHNIQUES:
            with self.subTest(technique=technique_id):
                self.assertIn(technique_id, self.catalogue)


class GateTests(unittest.TestCase):
    def test_untaught_is_a_permission_failure(self):
        self.assertFalse(may_use({"Biopsionics": 0}, "purge"))     # needs Biopsionics-2
        self.assertFalse(may_use({}, "surface_read"))
        self.assertFalse(may_use({"Telepathy": 1}, "no_such_technique"))

    def test_trained_clears_the_gate(self):
        self.assertTrue(may_use({"Telepathy": 0}, "surface_read"))
        self.assertTrue(may_use({"Telepathy": 1}, "thread"))
        self.assertTrue(may_use({"Biopsionics": 3}, "purge"))


class CostTests(unittest.TestCase):
    def test_a_core_costs_nothing_and_a_committed_power_names_its_duration(self):
        self.assertEqual(effort_duration("surface_read"), "none")
        self.assertEqual(effort_duration("thread"), "scene")
        self.assertEqual(effort_duration("command"), "day")
        self.assertEqual(effort_duration("no_such_technique"), "none")


if __name__ == "__main__":
    unittest.main()
