"""RPG-first acceptance: playable choices persist without running strategy (#516/#482/#502).

Only executable state and seeded Fate outcomes are asserted. No unapproved lore,
difficulty constants, world-politics numbers or visual renderer is pinned.
"""
import tempfile
import unittest
from pathlib import Path

from strategy_game.rpg.investigation import Investigation, InvestigationError
from strategy_game.rpg.skills import INDIVIDUAL_SKILL_NAMES


class RPGFirstVerticalSliceTest(unittest.TestCase):
    def test_noncombat_case_playthrough_and_reload(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "case.json"
            case = Investigation()
            case.party(["leader", "agent_1", "agent_2", "agent_3", "agent_4"])
            self.assertIn("interview", case.available())
            case.choose("interview")
            check = case.attempt("agent_1", "COG", 1, 516)
            self.assertEqual(check["kind"], "rpg_check")
            self.assertEqual(len(check["dice"]), 4)
            self.assertIn(check["outcome"], (
                "failure", "tie", "success", "success_with_style"
            ))
            case.choose("protect")
            case.save(path)
            resumed = Investigation.load(path)
            self.assertEqual(resumed.to_dict(), case.to_dict())
            resumed.choose("report")
            self.assertTrue(resumed.finished)
            self.assertEqual([e["kind"] for e in resumed.events],
                             ["investigation_choice", "rpg_check",
                              "investigation_choice", "investigation_choice"])
            resumed.save(path)
            self.assertEqual(Investigation.load(path).evidence, ["protect"])

    def test_seeded_roll_is_repeatable_without_strategy_engine(self):
        first = Investigation()
        second = Investigation()
        for case in (first, second):
            case.party(["leader", "agent_3"])
        a = first.attempt("agent_3", "WIL", 2, 470)
        b = second.attempt("agent_3", "WIL", 2, 470)
        self.assertEqual(a, b)

    def test_no_seventh_research_discipline_or_unapproved_skill(self):
        self.assertEqual(set(INDIVIDUAL_SKILL_NAMES),
                         {"COG", "INT", "REF", "SAV", "SOM", "WIL"})
        case = Investigation()
        with self.assertRaises(InvestigationError):
            case.attempt("leader", "PARAPSYCHOLOGY", 2, 506)
        self.assertEqual(case.events, [])

    def test_invalid_choice_does_not_advance_narrative(self):
        case = Investigation()
        with self.assertRaises(InvestigationError):
            case.choose("deploy_global_fleet")
        self.assertEqual(case.stage, "briefing")
        self.assertEqual(case.events, [])


if __name__ == "__main__":
    unittest.main()
