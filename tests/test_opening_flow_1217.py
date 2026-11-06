"""#1217: the built character is the officer who wakes up.

The fixtures are invented — a Background and four Edge names — because this repository carries no
verified CWN Edge catalogue. What is tested is the join: answers -> validated Lifepath -> the canonical
first-day session, with a real Kit, and a save that resumes mid-morning.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.console.first_day import ACTOR, HOME, OFFICE  # noqa: E402
from src.console.play import run_opening, run_opening_command  # noqa: E402
from src.console.opening import (  # noqa: E402
    OPENING_FORMAT,
    Opening,
    OpeningAnswers,
    OpeningError,
    build_opening,
)
from src.rules.cwn_backgrounds import Background  # noqa: E402
from src.rules.cwn_character import ARRAY, ATTRIBUTES  # noqa: E402
from src.rules.cwn_edges_foci import Edge  # noqa: E402

LAW = Background(
    id="Law Enforcement",
    free_skill="Investigate",
    learning=("Connect", "Shoot", "Drive"),
    growth=("Any Stat", "+1 Physical"),
)

CATALOGUE = {
    "Alert": Edge("Alert"),
    "Ghost": Edge("Ghost"),
    "Mutant": Edge("Mutant", is_power=True),
    "Mentalist": Edge("Mentalist", is_power=True),
    "Spellcaster": Edge("Spellcaster", is_power=True),
}

ARRAY_MAP = dict(zip(ATTRIBUTES, ARRAY, strict=True))


def answers(**overrides) -> OpeningAnswers:
    base = dict(path="grunt", attributes=ARRAY_MAP, edges=("Alert", "Ghost"),
                foci=(), learning=("Connect", "Shoot"), personality=())
    base.update(overrides)
    return OpeningAnswers(**base)


def build(**overrides):
    return build_opening(answers(**overrides), background=LAW, edge_catalogue=CATALOGUE)


class BuildTests(unittest.TestCase):
    def test_the_built_character_is_the_one_in_the_session(self):
        opening = build()
        self.assertEqual(opening.session.sheet_for(ACTOR), "sheet.tony.german")
        self.assertEqual(sorted(opening.character()["edges"]), ["Alert", "Ghost"])

    def test_the_kit_is_issued_once_and_worn_kit_starts_active(self):
        opening = build()
        self.assertEqual(len(opening.kit.items), 9)
        self.assertTrue(opening.kit.get("uniform").active)
        self.assertFalse(opening.kit.get("police_radio").active)
        self.assertTrue(opening.kit.get("police_radio").usable)  # carried, just not switched on

    def test_an_edge_id_outside_the_catalogue_is_refused_by_name(self):
        with self.assertRaises(OpeningError) as caught:
            build(edges=("Alert", "Telepath"))
        self.assertIn("Telepath", str(caught.exception))

    def test_an_illegal_edge_combination_is_refused_by_the_existing_validator(self):
        # psi_access forbids Mentalist beside Spellcaster; the builder must not need to know why.
        with self.assertRaises(Exception) as caught:
            build(edges=("Mentalist", "Spellcaster"))
        self.assertIn("Mentalist", str(caught.exception))

    def test_a_save_with_an_unknown_route_is_refused(self):
        with self.assertRaises(OpeningError):
            answers(path="wizard")


class PlayTests(unittest.TestCase):
    def test_the_whole_script_reaches_ratakatu_without_a_roll(self):
        opening = build()
        opening.script()
        self.assertEqual(opening.session.where(ACTOR), OFFICE)
        self.assertEqual(opening.actions(), ())

    def test_connecting_a_device_turns_it_on_in_the_kit(self):
        opening = build()
        opening.act("wake")
        opening.act("uniform")
        for item in ("police_radio", "phone", "computer"):
            opening.act("inspect:" + item)
        opening.act("connect:computer")
        self.assertTrue(opening.kit.get("computer").active)

    def test_dispatch_is_only_offered_once_the_kit_covers_every_required_function(self):
        opening = build()
        opening.act("wake")
        opening.act("uniform")
        for item in ("police_radio", "phone", "computer", "forensic_scanner", "gun", "sword",
                     "romppainen_fujita_device", "body_camera"):
            opening.act("inspect:" + item)
        self.assertNotIn("dispatch", opening.actions())
        # The radio and the phone are inspected, not linked: they are what Dispatch answers on.
        for item in ("computer", "forensic_scanner", "gun", "sword",
                     "romppainen_fujita_device", "body_camera"):
            opening.act("connect:" + item)
        self.assertNotIn("dispatch", opening.actions(), "no line is live yet")
        opening.act("connect:police_radio")
        self.assertIn("dispatch", opening.actions())
        self.assertEqual(opening.equipment()["missing"], [])

    def test_an_out_of_order_action_is_refused_with_the_available_list(self):
        opening = build()
        with self.assertRaises(OpeningError) as caught:
            opening.act("ride")
        self.assertIn("wake", str(caught.exception))


class SaveTests(unittest.TestCase):
    def test_a_half_played_morning_resumes_where_it_stopped(self):
        opening = build()
        opening.act("wake")
        opening.act("uniform")
        saved = opening.save()
        self.assertEqual(saved["format"], OPENING_FORMAT)

        restored = Opening.load(saved)
        self.assertEqual(restored.character(), opening.character())
        self.assertEqual(restored.actions(), opening.actions())
        self.assertTrue(restored.kit.get("uniform").usable)

        restored.script()
        self.assertEqual(restored.session.where(ACTOR), OFFICE)

    def test_a_foreign_save_is_refused(self):
        with self.assertRaises(OpeningError):
            Opening.load({"format": "something.else", "version": 1})

    def test_a_future_version_is_refused_rather_than_guessed(self):
        with self.assertRaises(OpeningError):
            Opening.load({"format": OPENING_FORMAT, "version": 99})

    def test_the_route_survives_a_round_trip(self):
        opening = build(path="geek")
        restored = Opening.load(opening.save())
        self.assertEqual(restored.lifepath.path, "geek")

    def test_the_actor_starts_at_home(self):
        self.assertEqual(build().session.where(ACTOR), HOME)


class FaultTests(unittest.TestCase):
    """Both comms can fail; the authored flow lets Tony restore one without a roll (#1245)."""

    def test_a_faulty_radio_is_not_offered_for_connection(self):
        opening = build()
        opening.session.flags.add("kit.fault:police_radio")
        opening.act("wake")
        opening.act("uniform")
        opening.act("inspect:police_radio")
        opening.act("inspect:phone")
        self.assertNotIn("connect:police_radio", opening.actions())

    def test_restoring_a_failed_line_reaches_dispatch_without_a_roll(self):
        opening = build()
        opening.session.flags.update({"kit.fault:police_radio", "kit.fault:phone"})
        opening.script()
        self.assertEqual(opening.session.where(ACTOR), OFFICE)
        self.assertIn("dispatch.call", opening.kit.coverage())



class InterfaceTests(unittest.TestCase):
    def test_view_reveals_only_current_place_not_hidden_story(self):
        opening = build()
        view = opening.view()
        self.assertEqual(view["actor"], ACTOR)
        self.assertEqual(view["location"]["id"], HOME)
        self.assertEqual(view["actions"], ["wake"])
        self.assertNotIn("graphs", view)
        self.assertNotIn("loc.ratakatu_12", json.dumps(view))
        self.assertEqual(json.loads(json.dumps(view)), view)

    def test_shared_command_rejects_invalid_action_without_mutation(self):
        opening = build()
        before = opening.save()
        keep_going, result = run_opening_command(opening, "ride")
        self.assertTrue(keep_going)
        self.assertIn("refused", result)
        self.assertEqual(before, opening.save())

    def test_console_resume_uses_same_opening_save(self):
        opening = build()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            saved = root / "before.json"
            scripted = root / "commands.txt"
            after = root / "after.json"
            saved.write_text(json.dumps(opening.save()), encoding="utf-8")
            scripted.write_text("wake\nuniform\nstatus\n", encoding="utf-8")
            args = Namespace(load=str(saved), script=str(scripted), save=str(after))
            self.assertEqual(run_opening(args), 0)
            resumed = Opening.load(json.loads(after.read_text(encoding="utf-8")))
            self.assertIn("first_day:uniform", resumed.session.flags)
            self.assertEqual(resumed.session.where(ACTOR), HOME)
            self.assertEqual(resumed.kit.actor, ACTOR)

    def test_console_refuses_to_invent_default_catalogues(self):
        self.assertEqual(run_opening(Namespace(load="", script="", save="")), 2)

if __name__ == "__main__":
    unittest.main()
