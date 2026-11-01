"""Initiative and the combat sequence — assertions traced to the CWN SRD (2.4.1 - 2.4.2)."""
import unittest

from src.rules import cwn_initiative as init


class GroupInitiativeTests(unittest.TestCase):
    def test_a_side_adds_its_best_dexterity_modifier(self) -> None:
        # 8 -> +0, 18 -> +2: the side rolls on its best, not its average.
        side = init.Side("crew", [8, 18, 12], is_pc=True)
        self.assertEqual(side.best_modifier(), 2)

    def test_an_npc_side_without_scores_adds_nothing(self) -> None:
        self.assertEqual(init.Side("thugs", []).best_modifier(), 0)

    def test_highest_total_acts_first(self) -> None:
        pc = init.Side("crew", [14], is_pc=True)      # +1
        npc = init.Side("thugs", [], is_pc=False)     # +0
        order = init.order_sides([pc, npc], dice=[3, 7])   # 4 vs 7
        self.assertEqual([entry.side.name for entry in order], ["thugs", "crew"])

    def test_the_player_side_wins_ties(self) -> None:
        pc = init.Side("crew", [8], is_pc=True)       # +0
        npc = init.Side("thugs", [], is_pc=False)     # +0
        order = init.order_sides([npc, pc], dice=[5, 5])
        self.assertEqual([entry.side.name for entry in order], ["crew", "thugs"])

    def test_a_die_outside_the_die_faces_is_refused(self) -> None:
        with self.assertRaises(init.InitiativeError):
            init.initiative_roll(init.Side("crew", [10]), die=9)
        with self.assertRaises(init.InitiativeError):
            init.initiative_roll(init.Side("crew", [10]), die=0)

    def test_a_fight_needs_a_side(self) -> None:
        with self.assertRaises(init.InitiativeError):
            init.order_sides([])

    def test_one_die_per_side(self) -> None:
        sides = [init.Side("a", [10]), init.Side("b", [10])]
        with self.assertRaises(init.InitiativeError):
            init.order_sides(sides, dice=[4])


class IndividualInitiativeTests(unittest.TestCase):
    def test_each_combatant_adds_their_own_modifier(self) -> None:
        rows = init.order_individual([("slow", 8, True), ("quick", 18, False)], dice=[6, 4])
        # 6 + 0 = 6 versus 4 + 2 = 6: the player character wins the tie.
        self.assertEqual(rows[0][0], "slow")

    def test_player_characters_win_ties(self) -> None:
        rows = init.order_individual([("npc", 12, False), ("pc", 12, True)], dice=[5, 5])
        self.assertEqual([name for name, _ in rows], ["pc", "npc"])

    def test_dice_count_must_match_the_combatants(self) -> None:
        with self.assertRaises(init.InitiativeError):
            init.order_individual([("a", 10, True)], dice=[3, 4])


class RoundTests(unittest.TestCase):
    def _round(self):
        pc = init.Side("crew", [18], is_pc=True)
        npc = init.Side("thugs", [], is_pc=False)
        order = init.order_sides([pc, npc], dice=[8, 1])
        return init.CombatRound(order)

    def test_sides_act_once_per_round(self) -> None:
        fight = self._round()
        acted = fight.run_round()
        self.assertEqual(sorted(acted), ["crew", "thugs"])
        self.assertEqual(fight.round_number, 2)

    def test_initiative_is_not_re_rolled_between_rounds(self) -> None:
        fight = self._round()
        first = fight.order[:]
        fight.run_round()
        self.assertEqual(fight.order, first)

    def test_turn_order_wraps_in_the_same_sequence(self) -> None:
        fight = self._round()
        self.assertEqual(fight.current(), "crew")
        self.assertEqual(fight.advance(), "thugs")
        self.assertEqual(fight.advance(), "crew")
        self.assertEqual(fight.round_number, 2)

    def test_automatic_initiative_acts_before_everyone(self) -> None:
        pc = init.Side("crew", [18], is_pc=True)
        npc = init.Side("thugs", [], is_pc=False)
        order = init.order_sides([pc, npc], dice=[8, 1])
        fight = init.CombatRound(order, automatic=["wired"])
        self.assertEqual(fight.order, ["wired", "crew", "thugs"])

    def test_an_empty_order_is_refused(self) -> None:
        with self.assertRaises(init.InitiativeError):
            init.CombatRound([])


class SurpriseTests(unittest.TestCase):
    def test_surprise_grants_the_ready_side_a_free_round(self) -> None:
        self.assertEqual(init.surprise_free_round(["thugs"], ["crew"]), ["crew"])

    def test_surprise_needs_someone_ready(self) -> None:
        with self.assertRaises(init.InitiativeError):
            init.surprise_free_round(["thugs"], [])


if __name__ == "__main__":
    unittest.main()


from src.rules.cwn_initiative import surprise_applies  # noqa: E402


def test_an_anticipating_group_cannot_be_surprised() -> None:
    """SRD 2.4.1: anticipating combat rules out surprise, whatever the GM intended."""
    assert surprise_applies(surprised=True, anticipating=True) is False
    assert surprise_applies(surprised=True, anticipating=False) is True
    assert surprise_applies(surprised=False, anticipating=False) is False
