"""Combat action economy — assertions traced to the CWN SRD action rules."""
import unittest

from src.rules import cwn_combat_actions as act


class TurnBudgetTests(unittest.TestCase):
    def test_one_main_and_one_move_per_round(self) -> None:
        budget = act.TurnBudget()
        budget.take_main()
        budget.take_move()
        self.assertFalse(budget.main_available)
        self.assertEqual(budget.moves_available, 0)

    def test_a_second_main_is_refused(self) -> None:
        budget = act.TurnBudget()
        budget.take_main()
        with self.assertRaises(act.ActionError):
            budget.take_main()

    def test_a_second_move_needs_the_main_action(self) -> None:
        budget = act.TurnBudget()
        budget.take_move()
        with self.assertRaises(act.ActionError):
            budget.take_move()
        budget.convert_main_to_move()
        budget.take_move()
        self.assertEqual(budget.moves_used, 2)
        self.assertEqual(budget.moves_available, 0)

    def test_converting_the_main_after_using_it_is_refused(self) -> None:
        budget = act.TurnBudget()
        budget.take_main()
        with self.assertRaises(act.ActionError):
            budget.convert_main_to_move()


class SnapAttackTests(unittest.TestCase):
    def test_snap_attacks_are_at_minus_four(self) -> None:
        self.assertEqual(act.snap_attack_penalty(main_used=False), -4)

    def test_a_snap_attack_requires_an_unspent_main(self) -> None:
        with self.assertRaises(act.ActionError):
            act.snap_attack_penalty(main_used=True)


class SwarmTests(unittest.TestCase):
    def test_bonuses_scale_per_other_assailant(self) -> None:
        self.assertEqual(act.swarm_bonus(0), act.SwarmBonus(0, 0))
        self.assertEqual(act.swarm_bonus(1), act.SwarmBonus(2, 1))
        self.assertEqual(act.swarm_bonus(2), act.SwarmBonus(4, 2))

    def test_four_attackers_is_the_cap(self) -> None:
        self.assertEqual(act.swarm_bonus(3), act.SwarmBonus(6, 3))
        self.assertEqual(act.swarm_bonus(9), act.SwarmBonus(6, 3))

    def test_negative_attackers_is_an_error(self) -> None:
        with self.assertRaises(act.ActionError):
            act.swarm_bonus(-1)


class ChargeTests(unittest.TestCase):
    def test_a_charge_grants_plus_two_and_costs_two_ac(self) -> None:
        charge = act.charge(5.0)
        self.assertEqual(charge.to_hit_bonus, 2)
        self.assertEqual(charge.ac_penalty, -2)
        self.assertEqual(charge.speed_multiplier, 2)

    def test_less_than_three_metres_cannot_build_momentum(self) -> None:
        with self.assertRaises(act.ActionError):
            act.charge(2.9)
        self.assertEqual(act.charge(3.0).to_hit_bonus, 2)

    def test_a_charge_needs_both_actions(self) -> None:
        spent_main = act.TurnBudget()
        spent_main.take_main()
        with self.assertRaises(act.ActionError):
            act.charge(5.0, budget=spent_main)

        spent_move = act.TurnBudget()
        spent_move.take_move()
        spent_move.convert_main_to_move()
        spent_move.take_move()
        with self.assertRaises(act.ActionError):
            act.charge(5.0, budget=spent_move)


class TotalDefenseTests(unittest.TestCase):
    def test_total_defense_is_plus_two_and_shock_immunity(self) -> None:
        stance = act.total_defense(main_used=False)
        self.assertEqual(stance.ac_bonus, 2)
        self.assertTrue(stance.shock_immune)

    def test_it_cannot_be_taken_after_the_main_action(self) -> None:
        with self.assertRaises(act.ActionError):
            act.total_defense(main_used=True)


class CatalogueTests(unittest.TestCase):
    def test_the_listed_costs_match_the_srd(self) -> None:
        self.assertEqual(act.COMMON_ACTIONS["make_melee_attack"], "main")
        self.assertEqual(act.COMMON_ACTIONS["run"], "move")
        self.assertEqual(act.COMMON_ACTIONS["charge"], "main+move")
        self.assertEqual(act.COMMON_ACTIONS["make_snap_attack"], "instant")
        self.assertEqual(act.COMMON_ACTIONS["total_defense"], "instant")
        self.assertEqual(act.COMMON_ACTIONS["stand_up"], "move")

    def test_on_turn_and_instant_are_not_capped(self) -> None:
        self.assertFalse(act.ON_TURN_LIMITED)
        self.assertFalse(act.INSTANT_LIMITED)


if __name__ == "__main__":
    unittest.main()
