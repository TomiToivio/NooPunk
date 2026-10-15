"""Executable contracts for issue #482 (no political/strategic effects)."""
import unittest
from random import Random

from strategy_game.rpg.fate import Action, Character, ResourceError
from strategy_game.rpg.dual_layer import (
    INDIVIDUAL_SKILLS, Scale, DualLayerCharacter, StrategicOrder, CouncilTurn,
)


def operative(identifier: str) -> DualLayerCharacter:
    return DualLayerCharacter(
        Character(identifier, identifier, ["Careful Analyst"], fate_points=2),
        {key: (3 if key == "COG" else 0) for key in INDIVIDUAL_SKILLS},
        {"Science": 1, "Espionage": 2},
        frozenset({"netrunner"}) if identifier == "leader" else frozenset(),
    )


class DualLayerTests(unittest.TestCase):
    def test_six_exact_skills_required(self):
        member = operative("x")
        self.assertEqual(set(member.individual_skills), set(INDIVIDUAL_SKILLS))
        with self.assertRaises(ResourceError):
            DualLayerCharacter(member.character, {"COG": 3}, {})

    def test_skill_domains_not_interchangeable(self):
        member = operative("x")
        self.assertEqual(member.rating(Scale.RPG, "COG"), 3)
        self.assertEqual(member.rating(Scale.STRATEGY, "Science"), 1)
        with self.assertRaises(ResourceError):
            member.rating(Scale.STRATEGY, "COG")
        with self.assertRaises(ResourceError):
            member.rating(Scale.RPG, "Science")

    def test_same_fate_dice_engine(self):
        member = operative("x")
        a = member.act(Scale.RPG, Action.OVERCOME, "COG", 2, rng=Random(11))
        b = member.act(Scale.STRATEGY, Action.OVERCOME, "Science", 2, rng=Random(11))
        self.assertEqual(a.resolution.dice, b.resolution.dice)
        self.assertEqual(a.resolution.total - b.resolution.total, 2)

    def test_invocation_consumes_real_character_resource(self):
        member = operative("x")
        member.act(Scale.RPG, Action.OVERCOME, "COG", 2,
                   rng=Random(5), invocation="Careful Analyst")
        self.assertEqual(member.character.fate_points, 1)
        with self.assertRaises(ResourceError):
            member.act(Scale.RPG, Action.OVERCOME, "COG", 2,
                       rng=Random(5), invocation="Nonexistent")

    def test_special_action_gate(self):
        with self.assertRaises(ResourceError):
            operative("agent").act(Scale.RPG, Action.OVERCOME, "COG", 1,
                                    rng=Random(1), required_capability="netrunner")
        operative("leader").act(Scale.RPG, Action.OVERCOME, "COG", 1,
                                rng=Random(1), required_capability="netrunner")

    def test_five_agents_and_one_order_each(self):
        council = CouncilTurn(operative("leader"), tuple(operative(str(i)) for i in range(4)))
        for identifier in ("leader", "0", "1", "2", "3"):
            council.assign(StrategicOrder(identifier, Action.OVERCOME, "Science", 2))
        with self.assertRaises(ResourceError):
            council.assign(StrategicOrder("leader", Action.OVERCOME, "Science", 2))
        results = council.resolve_orders(rng=Random(17))
        self.assertEqual(len(results), 5)
        council.next_turn()
        self.assertEqual(len(council.orders), 0)

    def test_invalid_orders_do_not_consume_slot(self):
        council = CouncilTurn(operative("leader"), tuple(operative(str(i)) for i in range(4)))
        with self.assertRaises(ResourceError):
            council.assign(StrategicOrder("0", Action.OVERCOME, "Espionage", 2,
                                           "netrunner"))
        self.assertFalse(council.orders)

    def test_no_extra_council_members(self):
        with self.assertRaises(ResourceError):
            CouncilTurn(operative("leader"), (operative("a"),))


if __name__ == "__main__":
    unittest.main()
