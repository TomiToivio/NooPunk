"""Executable display behavior of the faction council assignment view (#323)."""
import unittest

from strategy_game.council_view import assignment_rows, render_assignment_board
from strategy_game.council import Council, CouncilLeader, MissionDeclaration, load_council


class CouncilViewTests(unittest.TestCase):
    def setUp(self):
        self.model = load_council()
        self.council = self.model.worked_example_council()

    def test_every_leader_visible_even_when_no_mission(self):
        council = Council("demo", leaders=(
            CouncilLeader("a", name="Alpha", portfolio="politics_diplomacy"),
            CouncilLeader("b", name="Beta", portfolio="research_intelligence", status="injured"),
        ), missions=(MissionDeclaration("m", leader_id="a", kind="investigate", target_id="t", location_id="district", quantity="opinion_support", authorised_by="p"),))
        rows = assignment_rows(council)
        self.assertEqual(len(rows), 2)
        self.assertIn("m (investigate at district: t)", rows[0]["assignment"])
        self.assertEqual(rows[1]["assignment"], "no active mission")
        self.assertEqual(rows[1]["status"], "injured")

    def test_invalid_declarations_remain_visible_as_warnings(self):
        council = Council("bad", leaders=(CouncilLeader("a", portfolio="politics_diplomacy"),),
                          missions=(MissionDeclaration("x", leader_id="absent", kind="investigate", target_id="t", location_id="d", quantity="opinion_support", authorised_by="p"),))
        shown = render_assignment_board(council, self.model)
        self.assertIn("Declaration warnings:", shown)
        self.assertIn("absent", shown)

    def test_render_is_repeatable_and_does_not_mutate_council(self):
        before = self.council.to_dict()
        first = render_assignment_board(self.council, self.model)
        self.assertEqual(first, render_assignment_board(self.council, self.model))
        self.assertEqual(before, self.council.to_dict())
        self.assertIn("Unpursued priorities:", first)
        self.assertIn("no outcomes or passive bonuses applied", first)


if __name__ == "__main__":
    unittest.main()
