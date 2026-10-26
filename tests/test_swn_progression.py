"""SWN psychic progression regression tests; no proprietary powers."""
import unittest

from src.rules.swn_progression import PsychicTraining
from src.rules.swn_psionics import PsiRulesError


class PsychicProgressionTests(unittest.TestCase):
    def test_full_psychic_may_expand_disciplines(self):
        p = PsychicTraining("swn_psychic")
        p.learn_discipline("Telepathy")
        p.learn_discipline("Precognition")
        self.assertEqual(p.advance("Telepathy"), 1)
        p.learn_technique("noo_sense", "Telepathy", 1)
        self.assertTrue(p.technique_access("noo_sense"))
        self.assertEqual(PsychicTraining.from_snapshot(p.snapshot()).snapshot(), p.snapshot())

    def test_partial_psychic_single_discipline(self):
        p = PsychicTraining("swn_partial_psychic", {"Telepathy": 0})
        with self.assertRaises(PsiRulesError):
            p.learn_discipline("Teleportation")
        with self.assertRaises(PsiRulesError):
            PsychicTraining("swn_partial_psychic", {"Telepathy": 0, "Teleportation": 0})

    def test_technique_requires_trained_rank(self):
        p = PsychicTraining("swn_psychic", {"Biopsionics": 0})
        with self.assertRaises(PsiRulesError):
            p.learn_technique("noo_heal", "Biopsionics", 2)
        p.advance("Biopsionics")
        p.advance("Biopsionics")
        p.learn_technique("noo_heal", "Biopsionics", 2)
        self.assertTrue(p.technique_access("noo_heal"))

    def test_invalid_snapshots_rejected(self):
        for state in [
            {"package": "warrior", "skills": {}},
            {"package": "swn_psychic", "skills": {"Telepathy": 5}},
            {"package": "swn_psychic", "skills": {}, "techniques": {"broken": ["Telepathy", 0]}},
            {"package": "swn_psychic", "skills": {"Telepathy": 0}, "techniques": {"bad": [1]}},
        ]:
            with self.subTest(state=state), self.assertRaises(PsiRulesError):
                PsychicTraining.from_snapshot(state)


if __name__ == "__main__":
    unittest.main()
