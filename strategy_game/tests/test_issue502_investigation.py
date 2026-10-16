"""Functional tests for the executable investigation slice; no prose/canon assertions."""
import tempfile
import unittest
from pathlib import Path

from strategy_game.rpg.investigation import Investigation, InvestigationError


class InvestigationTests(unittest.TestCase):
    def test_leader_and_agents_and_branching(self):
        a = Investigation()
        self.assertEqual(a.participants, ["leader"])
        a.party(["leader", "agent_2", "agent_3"])
        a.choose("inspect")
        a.choose("preserve")
        a.choose("report")
        self.assertTrue(a.finished)
        self.assertEqual(a.evidence, ["preserve"])
        self.assertEqual([e["choice"] for e in a.events], ["inspect", "preserve", "report"])
        self.assertTrue(all(e["faction_id"] == a.faction_id for e in a.events))

    def test_alternate_route_and_invalid_choice(self):
        a = Investigation()
        with self.assertRaises(InvestigationError):
            a.choose("report")
        a.choose("interview")
        a.choose("protect")
        a.choose("withhold")
        self.assertTrue(a.finished)
        with self.assertRaises(InvestigationError):
            a.choose("inspect")

    def test_roll_replays_and_does_not_choose_for_player(self):
        a = Investigation()
        a.party(["leader", "agent_3"])
        first = a.attempt("agent_3", "WIL", 1, 9)
        second = a.attempt("agent_3", "WIL", 1, 9)
        self.assertEqual(first["dice"], second["dice"])
        self.assertEqual(a.stage, "briefing")
        with self.assertRaises(InvestigationError):
            a.attempt("agent_4", "REF", 1, 9)
        with self.assertRaises(InvestigationError):
            a.attempt("leader", "NotASkill", 1, 9)

    def test_save_load_and_reject_inconsistent_stage(self):
        a = Investigation()
        a.choose("interview")
        a.choose("disclose")
        a.attempt("leader", "SAV", 2, 42)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "subdir" / "case.json"
            a.save(path)
            loaded = Investigation.load(path)
            self.assertEqual(loaded.to_dict(), a.to_dict())
        broken = a.to_dict()
        broken["stage"] = "complete"
        with self.assertRaises(InvestigationError):
            Investigation.from_dict(broken)

    def test_roster_validated(self):
        case = Investigation()
        with self.assertRaises(InvestigationError):
            case.party(["agent_1", "agent_1"])
        with self.assertRaises(InvestigationError):
            case.party(["invented"])


if __name__ == "__main__":
    unittest.main()
