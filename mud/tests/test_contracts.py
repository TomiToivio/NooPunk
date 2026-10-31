import unittest
from systems.cwn import skill_check
from systems.agents import Intent, validate_npc_intent, OfflineGM
from systems.simulation import SupplyProposal, validate_proposal

class FixedDice:
    def randint(self, a, b):
        return 4

class ContractsTest(unittest.TestCase):
    def test_cwn_check_and_input(self):
        outcome = skill_check(1, 1, 8, FixedDice())
        self.assertEqual(outcome.total, 10)
        self.assertTrue(outcome.success)
        with self.assertRaises(ValueError):
            skill_check(99, 0)
    def test_ai_cannot_mutate_or_act_as_player(self):
        self.assertTrue(validate_npc_intent(Intent("npc1", "say", text="Hello"), {"npc1"}, {"Kurvi"}))
        self.assertFalse(validate_npc_intent(Intent("pc1", "say"), {"npc1"}, {"Kurvi"}))
        self.assertFalse(validate_npc_intent(Intent("npc1", "give_resources"), {"npc1"}, {"Kurvi"}))
        self.assertFalse(validate_npc_intent(Intent("npc1", "move", "Moon"), {"npc1"}, {"Kurvi"}))
        self.assertIn("quiet", OfflineGM().narrate("Kurvi", []))
    def test_mesa_proposals_are_bounded(self):
        self.assertTrue(validate_proposal(SupplyProposal("Kurvi", -1, "consumption"), {"Kurvi"}))
        self.assertFalse(validate_proposal(SupplyProposal("Kurvi", 999, "mint"), {"Kurvi"}))

if __name__ == "__main__":
    unittest.main()
