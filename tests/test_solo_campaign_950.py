"""The solo UNSA campaign can be finished end to end, headless, with nobody else (#950).

Written with `unittest`: CI discovers with `unittest` and does not install pytest.

What these tests are really asking: is there a game here, or only a promise of one? The playthrough below goes
from a cold start to a filed case using only text commands, with no LLM, no simulation, no second player, no
Evennia and no Godot.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))

from nopunk_mud.campaign import CampaignEngine, play  # noqa: E402
from nopunk_mud.campaign import content  # noqa: E402

SOLVED = [
    "look", "talk romppainen", "ask romppainen case",
    "go street", "go university", "examine terminal",
    "go street", "go kurvi", "talk witness", "ask witness badge", "examine woman",
    "go street", "go safehouse", "report",
]


class FullPlaythrough(unittest.TestCase):
    def test_a_case_can_be_solved_with_text_commands_only(self):
        engine, transcript = play(SOLVED)
        self.assertEqual(engine.state.ending, "solved")
        self.assertIn("access_log", engine.state.clues)
        self.assertIn("witness_badge", engine.state.clues)
        self.assertIn("Case filed", transcript[-1])

    def test_the_transcript_never_mentions_a_roll_for_a_core_clue(self):
        """The core clue arrives because the player looked, not because the dice agreed."""
        engine, transcript = play(["go street", "go university", "examine terminal"])
        self.assertIn("access_log", engine.state.clues)
        text = transcript[-1]
        self.assertIn("23:40", text)
        self.assertNotIn("miss", text.lower())

    def test_an_optional_clue_may_fail_and_the_case_still_works(self):
        # Seeded so the Notice check fails: the lab note stays out of reach, the core clue does not.
        engine, transcript = play(["go street", "go university", "examine terminal",
                                   "go street", "go kurvi", "talk witness", "ask witness badge",
                                   "examine woman", "go street", "go safehouse", "report"], seed=1)
        self.assertNotIn("lab_note", engine.state.clues)
        self.assertEqual(engine.state.ending, "solved")


class Refusals(unittest.TestCase):
    def test_an_unknown_command_changes_nothing(self):
        engine = CampaignEngine()
        before = engine.state.turns
        text = engine.command("summon demon")
        self.assertIn("not something you can do", text)
        # An unrecognised word costs nothing at all — not a turn, not a position, not a clue.
        self.assertEqual(engine.state.turns, before)
        self.assertEqual(engine.state.location, "safehouse")
        self.assertEqual(engine.state.clues, [])

    def test_you_cannot_walk_through_a_wall(self):
        engine = CampaignEngine()
        text = engine.command("go harbour")
        self.assertIn("cannot go to harbour", text)
        self.assertEqual(engine.state.location, "safehouse")

    def test_a_core_clue_needs_the_conversation_that_frames_it(self):
        engine = CampaignEngine()
        engine.command("go street")
        engine.command("go kurvi")
        text = engine.command("examine woman")
        self.assertIn("Someone would have to tell you", text)
        self.assertEqual(engine.state.clues, [])

    def test_reporting_without_evidence_is_refused_with_a_reason(self):
        engine = CampaignEngine()
        text = engine.command("report")
        self.assertIn("no evidence", text)
        self.assertEqual(engine.state.ending, "")

    def test_attacking_someone_outside_the_case_is_refused(self):
        engine = CampaignEngine()
        engine.command("talk romppainen")
        text = engine.command("attack romppainen")
        self.assertIn("not part of this case", text)


class Combat(unittest.TestCase):
    def test_the_fight_can_kill_and_that_ends_the_case(self):
        engine = CampaignEngine(seed=3)
        engine.command("go street")
        engine.command("go kurvi")
        engine.command("go harbour")
        engine.state.hp = 1
        for _ in range(40):
            engine.command("attack watcher")
            if engine.state.ending:
                break
        self.assertIn(engine.state.ending, {"killed", ""})
        if engine.state.hp == 0:
            self.assertEqual(engine.state.ending, "killed")

    def test_the_fight_can_be_won(self):
        engine = CampaignEngine(seed=5)
        engine.command("go street")
        engine.command("go kurvi")
        engine.command("go harbour")
        engine.state.hp = 40  # this test is about winning, not about surviving
        for _ in range(60):
            engine.command("attack watcher")
            if engine.state.ending == "killed":
                break
            if "van_cleared" in engine.state.flags:
                break
        self.assertIn("van_cleared", engine.state.flags)


class Persistence(unittest.TestCase):
    def test_a_game_survives_a_save_and_a_restart(self):
        engine = CampaignEngine()
        engine.command("go street")
        engine.command("go university")
        engine.command("examine terminal")
        state = engine.to_dict()

        restored = CampaignEngine.from_dict(state)
        self.assertEqual(restored.state.location, "university")
        self.assertIn("access_log", restored.state.clues)

        restored.command("go street")
        restored.command("go kurvi")
        restored.command("talk witness")
        restored.command("ask witness badge")
        restored.command("examine woman")
        restored.command("go street")
        restored.command("go safehouse")
        self.assertIn("Case filed", restored.command("report"))

    def test_a_foreign_save_is_refused(self):
        with self.assertRaises(ValueError):
            CampaignEngine.from_dict({"schema_version": 99})


class NoDependencies(unittest.TestCase):
    def test_the_campaign_imports_no_llm_or_simulation_layer(self):
        package = ROOT / "mud" / "nopunk_mud" / "campaign"
        banned = ("llm_gateway", "sim_bridge", "concordia", "mesa", "evennia", "requests", "openai")
        for path in package.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for name in banned:
                self.assertNotIn(f"import {name}", text, f"{path.name} imports {name}")
                self.assertNotIn(f"from {name}", text, f"{path.name} imports {name}")

    def test_content_covers_every_place_and_ending(self):
        for clue in content.CLUES.values():
            self.assertIn(clue["location"], content.LOCATIONS)
        for place in content.LOCATIONS.values():
            for target in place["exits"].values():
                self.assertIn(target, content.LOCATIONS)
        self.assertEqual(set(content.ENDINGS), {"solved", "incomplete", "killed"})


if __name__ == "__main__":
    unittest.main()
