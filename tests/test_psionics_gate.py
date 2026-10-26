"""Contract tests for #652's incremental psychic-gate implementation."""
import unittest

from src.rules.psionics import Duration, Psychic, PsiRulesError


class PsychicGateTests(unittest.TestCase):
    def test_untrained_operator_cannot_read_minds(self):
        operator = Psychic(14, 10, {"Telepathy": 1})
        with self.assertRaises(PsiRulesError):
            operator.use_technique("read", "surface_read")
        self.assertEqual(operator.free, operator.capacity)

    def test_package_rank_and_effort(self):
        psychic = Psychic(14, 10, {"Telepathy": 0}, {"swn_partial_psychic"})
        psychic.use_technique("read", "surface_read")
        self.assertEqual(psychic.free, psychic.capacity - 1)
        with self.assertRaises(PsiRulesError):
            psychic.use_technique("trace", "empathic_trace")
        with self.assertRaises(PsiRulesError):
            psychic.use_technique("unknown", "source_book_power")
        self.assertEqual(psychic.free, psychic.capacity - 1)
        psychic.end_scene()
        self.assertEqual(psychic.free, psychic.capacity)

    def test_snapshot_rejects_unauthorized_reservations(self):
        p = Psychic(14, 10, {"Telepathy": 0}, {"swn_psychic"})
        p.use_technique("read", "surface_read", duration=Duration.DAY)
        state = p.snapshot()
        self.assertEqual(Psychic.from_snapshot(state).snapshot(), state)
        state["permissions"] = []
        with self.assertRaises(PsiRulesError):
            Psychic.from_snapshot(state)


if __name__ == "__main__":
    unittest.main()
