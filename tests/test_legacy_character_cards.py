"""Stdlib tests for NoöPunk character cards."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from character_cards import load_cards, instantiate, view

class CharacterCardsTest(unittest.TestCase):
    def test_catalogue_and_four_nhi(self):
        cards = load_cards()
        self.assertEqual(len({c["id"] for c in cards}), len(cards))
        self.assertEqual({c["nhi"]["ontology"] for c in cards if c["card_type"] == "nhi"},
                         {"Biologics", "Constructs", "Noetics", "Plasmoids"})
    def test_privacy(self):
        leader = next(c for c in load_cards() if c["card_type"] == "canonical")
        self.assertNotIn("Leave specific hidden interests", view(leader))
        self.assertIn("Leave specific hidden interests", view(leader, True))
    def test_template_instance(self):
        archetype = next(c for c in load_cards() if c["card_type"] == "archetype")
        inst = instantiate(archetype, "npc.guard.01", "Arja", "Example faction")
        self.assertEqual(inst["template_id"], archetype["id"])
        self.assertEqual(inst["factions"], ["Example faction"])
        self.assertNotIn("instance_id", archetype)
    def test_no_duplicate_canon(self):
        leader = next(c for c in load_cards() if c["card_type"] == "canonical")
        with self.assertRaises(ValueError):
            instantiate(leader, "copy")

if __name__ == "__main__":
    unittest.main()
