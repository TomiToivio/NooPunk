"""Regression tests for malformed council declarations (#323)."""
import unittest

from strategy_game.council import council_from_dict, load_council


class CouncilMissingIdentifierTests(unittest.TestCase):
    def test_missing_leader_id_reaches_validator(self):
        council = council_from_dict({
            "id": "player",
            "leaders": [{"name": "Anonymous", "portfolio": "politics_diplomacy"}],
        })
        self.assertEqual(len(council.leaders), 1)
        problems = load_council().structural_problems(council)
        self.assertTrue(any("leader has no identifier" in p for p in problems))

    def test_missing_mission_id_reaches_validator(self):
        council = council_from_dict({
            "id": "player",
            "missions": [{
                "leader_id": "", "kind": "campaign", "target_id": "target",
                "location_id": "district", "quantity": "public_opinion",
                "authorised_by": "player",
            }],
        })
        self.assertEqual(len(council.missions), 1)
        problems = load_council().structural_problems(council)
        self.assertTrue(any("mission has no identifier" in p for p in problems))
        self.assertTrue(any("leaderless" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
