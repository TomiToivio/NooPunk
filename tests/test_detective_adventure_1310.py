"""Issue #1310: one finite detective investigation, no full-RPG dependency."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "NooPunk-Simulator" / "Code" / "adventure.py"
spec = importlib.util.spec_from_file_location("detective_adventure_1310", PATH)
adventure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adventure)


class DetectiveAdventureTests(unittest.TestCase):
    def setUp(self):
        self.case = adventure.load_case()
        self.game = adventure.Adventure(self.case)

    def step(self, label):
        choices = self.game.choices()
        matches = [i for i, c in enumerate(choices, 1) if c["label"] == label]
        self.assertEqual(len(matches), 1, label)
        self.game.choose(matches[0])

    def reach_decision(self, first="Read the missing-person report and public event register"):
        self.step(first)
        if first.startswith("Read"):
            self.step("Speak with the witness")
        else:
            self.step("Check the event register")
        self.step("Review the voluntarily provided message")
        self.step("Review all leads and decide how to proceed")
        self.assertEqual(self.game.state["scene"], "decision")

    def test_three_distinct_endings(self):
        for index, ending in enumerate(("private_end", "review_end", "public_end"), 1):
            with self.subTest(ending=ending):
                self.setUp()
                self.reach_decision()
                self.game.choose(index)
                self.assertEqual(self.game.state["scene"], ending)
                self.assertTrue(self.game.state["finished"])
                self.assertEqual(self.game.choices(), [])

    def test_alternate_investigation_order_is_playable(self):
        self.reach_decision(first="Interview a witness from the meeting")
        self.assertEqual(set(self.game.state["clues"]),
                         {"missing", "roster", "witness", "message"})

    def test_no_shortcut_or_softlock(self):
        self.step("Interview a witness from the meeting")
        self.step("Review the voluntarily provided message")
        self.assertFalse(any(c["to"] == "decision" for c in self.game.choices()))
        self.assertTrue(any(c["to"] == "records" for c in self.game.choices()))
        self.step("Recheck records")
        self.step("Review the voluntarily provided message")
        self.assertTrue(any(c["to"] == "decision" for c in self.game.choices()))

    def test_save_load_roundtrip_and_log(self):
        self.step("Read the missing-person report and public event register")
        with tempfile.TemporaryDirectory() as directory:
            save = Path(directory) / "case.json"
            self.game.save(save)
            restored = adventure.Adventure.restore(self.case, save)
        self.assertEqual(restored.state, self.game.state)
        self.assertIn("event register", restored.notebook())
        self.assertEqual(len(restored.state["history"]), 1)

    def test_bad_save_rejected(self):
        data = dict(self.game.state, case_id="different_case")
        with self.assertRaises(ValueError):
            adventure.Adventure(self.case, data)

    def test_fixture_marked_synthetic_not_canon(self):
        self.assertEqual(self.case["source"]["kind"], "synthetic_development_fixture")
        self.assertFalse(self.case["source"]["canon"])
        self.assertIsNone(self.case["source"]["story_manuscript"])

    def test_broken_scene_reference_rejected(self):
        changed = json.loads(json.dumps(self.case))
        changed["scenes"]["briefing"]["choices"][0]["to"] = "unknown"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.json"
            path.write_text(json.dumps(changed), encoding="utf-8")
            with self.assertRaises(ValueError):
                adventure.load_case(path)

    def test_hypotheses_are_gated_by_evidence(self):
        """A hypothesis is something you can hold once the evidence exists — not a fact of the case."""
        self.assertEqual(self.game.available_hypotheses(), [])
        with self.assertRaises(ValueError):
            self.game.consider("h1")
        self.reach_decision()
        available = dict(self.game.available_hypotheses())
        self.assertIn("h1", available)
        self.assertIn("cannot both be right", available["h1"])

    def test_the_detective_records_and_sets_aside_hypotheses(self):
        self.reach_decision()
        self.game.consider("h1")
        self.game.dismiss("h2")
        self.assertEqual(self.game.state["hypotheses"], {"h1": "considered", "h2": "dismissed"})
        notebook = self.game.notebook()
        self.assertIn("Recorded by you:", notebook)
        self.assertIn("Set aside:", notebook)
        with self.assertRaises(ValueError):
            self.game.consider("h99")

    def test_contradictions_surface_only_when_both_records_are_held(self):
        self.step("Read the missing-person report and public event register")
        self.assertEqual(self.game.contradictions(), [])
        self.step("Speak with the witness")
        self.assertEqual([cid for cid, _ in self.game.contradictions()], ["c1"])
        self.assertIn("only one group present", self.game.notebook())

    def test_open_leads_are_places_not_yet_visited(self):
        self.step("Read the missing-person report and public event register")
        leads = dict(self.game.leads())
        self.assertIn("witness", leads)
        self.assertNotIn("records", leads, "the scene you are standing in is not a lead")
        self.step("Speak with the witness")
        self.assertNotIn("witness", dict(self.game.leads()))

    def test_reasoning_and_disposition_survive_save_and_load(self):
        self.reach_decision()
        self.game.consider("h1")
        self.game.choose(2)
        with tempfile.TemporaryDirectory() as directory:
            save = Path(directory) / "case.json"
            self.game.save(save)
            restored = adventure.Adventure.restore(self.case, save)
        self.assertEqual(restored.state, self.game.state)
        self.assertIn("Recorded by you:", restored.notebook())
        self.assertIn("Disposition: formal_review", restored.notebook())

    def test_a_save_from_before_the_reasoning_layer_still_loads(self):
        legacy = dict(self.game.state)
        del legacy["hypotheses"]
        restored = adventure.Adventure(self.case, legacy)
        self.assertEqual(restored.state["hypotheses"], {})
        self.assertIn("CASE NOTEBOOK", restored.notebook())

    def test_a_save_with_an_unknown_hypothesis_is_rejected(self):
        with self.assertRaises(ValueError):
            adventure.Adventure(self.case, dict(self.game.state, hypotheses={"h99": "considered"}))
        with self.assertRaises(ValueError):
            adventure.Adventure(self.case, dict(self.game.state, hypotheses={"h1": "certain"}))

    def test_no_rpg_imports(self):
        contents = PATH.read_text(encoding="utf-8")
        for forbidden in ("src.rules", "src.text_game", "from rules", "from world", "evennia"):
            self.assertNotIn(forbidden, contents)


if __name__ == "__main__":
    unittest.main()
