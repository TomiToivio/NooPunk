"""The five live scene types (#1164, #1184).

Astral is postponed and must say so loudly. Action is an arrest, a pursuit, a door or a standoff —
force is the short exception, and the two rules that make it an exception are enforced here.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.rules.cwn_hacking import AlertClock  # noqa: E402
from src.rules.investigation import Case, Clue, ClueKind, Investigator, Scene as CaseScene  # noqa: E402
from src.world.graphs import (  # noqa: E402
    CyberGraph,
    DeviceNode,
    LocationNode,
    PhysicalGraph,
    PhysicalRoute,
)
from src.world.narrative_tags import (  # noqa: E402
    ClueTag,
    PersonalityTag,
    Polarity,
    SocialTag,
    TagBook,
)
from src.world.scenes import (  # noqa: E402
    ACTION_PHASES,
    ActionScene,
    PostponedScene,
    SceneError,
    SceneFrame,
    run_cyber_scene,
    run_exploration_scene,
    run_investigation_scene,
    run_social_scene,
)


def physical() -> PhysicalGraph:
    return PhysicalGraph(
        nodes={
            "loc.street": LocationNode("loc.street", "Kurvi street", "street"),
            "loc.stair": LocationNode("loc.stair", "Stairwell", "room"),
            "loc.flat": LocationNode("loc.flat", "Flat 4B", "room"),
        },
        routes=(
            PhysicalRoute("loc.street", "loc.stair"),
            PhysicalRoute("loc.stair", "loc.flat"),
        ),
    )


class SceneFrameTests(unittest.TestCase):
    def test_the_five_live_types_are_accepted(self):
        for kind in ("Social", "Investigation", "Exploration", "Action", "Cyber"):
            SceneFrame(id=f"scene.{kind}", title=kind, scene_type=kind)

    def test_astral_is_postponed_loudly(self):
        with self.assertRaises(PostponedScene):
            SceneFrame(id="scene.astral", title="Astral", scene_type="Astral")

    def test_combat_is_not_a_scene_type(self):
        with self.assertRaises(SceneError):
            SceneFrame(id="scene.firefight", title="Old word", scene_type="Combat")


class SocialSceneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = SceneFrame(id="scene.chat", title="Front desk", scene_type="Social")

    def test_no_lever_means_no_check(self):
        result = run_social_scene(
            self.frame, TagBook(), holder="npc.clerk", target="pc.rookie",
            approach="ask", actor_total=20, resistance_total=1, method="Persuade")
        self.assertFalse(result.passed)
        self.assertEqual(result.tags_added, ())
        self.assertIn("no lever", result.notes[0])

    def test_a_lever_permits_the_cwn_check_and_records_a_tag(self):
        book = TagBook()
        book.add_social(SocialTag(id="social.1", holder="npc.clerk", target="pc.rookie",
                                  fact="owes a favour", polarity=Polarity.FAVOURABLE))
        result = run_social_scene(
            self.frame, book, holder="npc.clerk", target="pc.rookie",
            approach="ask", actor_total=20, resistance_total=1, method="Persuade")
        self.assertTrue(result.passed)
        (tag,) = result.tags_added
        self.assertEqual(tag.polarity, Polarity.FAVOURABLE)

    def test_coercion_leaves_a_grievance_and_an_unfavourable_tag(self):
        book = TagBook()
        book.add_clue(ClueTag(id="clue.1", clue_id="clue.ledger", holder="pc.rookie",
                              fact="the ledger is his", route="document", reliability="public",
                              bears_on=("npc.clerk",)))
        result = run_social_scene(
            self.frame, book, holder="npc.clerk", target="pc.rookie",
            approach="threaten", actor_total=20, resistance_total=1, method="coerce")
        (tag,) = result.tags_added
        self.assertEqual(tag.polarity, Polarity.UNFAVOURABLE)
        self.assertIn("grievance", tag.fact)


class InvestigationSceneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = SceneFrame(id="scene.warehouse", title="Warehouse", scene_type="Investigation")
        self.case = Case(id="case.1", scenes=(
            CaseScene(id="scene.warehouse", title="Warehouse", clues=(
                Clue(id="clue.log", scene_id="scene.warehouse", kind=ClueKind.CORE,
                     competency="Investigate", fact="A pallet left after midnight"),
            )),
        ))

    def test_a_competent_investigator_gets_the_clue_without_a_roll(self):
        officer = Investigator.from_sheet("rookie", {"Investigate": 0})
        result = run_investigation_scene(self.frame, self.case, officer)
        self.assertTrue(result.passed)
        self.assertEqual(result.facts, ("A pallet left after midnight",))
        (tag,) = result.tags_added
        self.assertEqual(tag.clue_id, "clue.log")
        self.assertEqual(tag.holder, "rookie")

    def test_an_incompetent_investigator_cannot_leave_on_their_own(self):
        officer = Investigator.from_sheet("rookie", {"Shoot": 1})
        result = run_investigation_scene(self.frame, self.case, officer)
        self.assertFalse(result.passed)
        self.assertEqual(result.tags_added, ())

    def test_the_clue_tag_carries_its_route_and_rung(self):
        officer = Investigator.from_sheet("rookie", {"Investigate": 0})
        result = run_investigation_scene(self.frame, self.case, officer,
                                         route="forensic", reliability="authenticated")
        (tag,) = result.tags_added
        self.assertEqual(tag.route, "forensic")
        self.assertEqual(tag.reliability, "authenticated")


class ExplorationSceneTests(unittest.TestCase):
    def test_moving_along_the_graph_returns_what_was_found(self):
        graph = physical()
        graph.enter("pc.rookie", "loc.street")
        frame = SceneFrame(id="scene.walk", title="Up the stairs", scene_type="Exploration")
        result = run_exploration_scene(
            frame, graph, "pc.rookie", ["loc.stair", "loc.flat"],
            discoveries={"loc.flat": "The door is ajar"})
        self.assertTrue(result.passed)
        self.assertEqual(result.facts, ("The door is ajar",))
        self.assertEqual(graph.at("pc.rookie"), "loc.flat")

    def test_an_impassable_route_stops_the_scene(self):
        graph = physical()
        graph.enter("pc.rookie", "loc.street")
        frame = SceneFrame(id="scene.walk", title="Wrong way", scene_type="Exploration")
        result = run_exploration_scene(frame, graph, "pc.rookie", ["loc.flat"])
        self.assertFalse(result.passed)
        self.assertEqual(graph.at("pc.rookie"), "loc.street")


class CyberSceneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = CyberGraph(
            nodes={
                "cyber.camera": DeviceNode("cyber.camera", "Camera", "camera", "loc.street",
                                           ("observe",)),
                "cyber.server": DeviceNode("cyber.server", "Server", "server", "", ("query",)),
            },
            links=(),
        )
        self.frame = SceneFrame(id="scene.hack", title="Camera feed", scene_type="Cyber")

    def test_a_successful_run_program_reports_success(self):
        result = run_cyber_scene(
            self.frame, self.graph, "pc.rookie", "cyber.camera",
            intelligence_score=10, program_skill=1, difficulty=8, dice=(6, 6))
        self.assertTrue(result.passed)

    def test_a_failure_advances_the_alert_clock(self):
        clock = AlertClock()
        result = run_cyber_scene(
            self.frame, self.graph, "pc.rookie", "cyber.camera",
            intelligence_score=3, program_skill=0, difficulty=14, dice=(1, 1), clock=clock)
        self.assertFalse(result.passed)
        self.assertEqual(clock.failures, 1)

    def test_a_device_not_on_the_graph_is_refused(self):
        with self.assertRaises(SceneError):
            run_cyber_scene(self.frame, self.graph, "pc.rookie", "cyber.ghost",
                            intelligence_score=10, program_skill=1, difficulty=8)


class ActionSceneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = physical()
        self.graph.enter("pc.rookie", "loc.street")
        self.graph.enter("npc.suspect", "loc.stair")
        frame = SceneFrame(id="scene.arrest", title="Stairwell arrest", scene_type="Action")
        self.scene = ActionScene(frame=frame, graph=self.graph, actor="pc.rookie",
                                 target="npc.suspect")

    def test_the_phases_are_a_police_problem_not_a_round_structure(self):
        self.assertEqual(ACTION_PHASES, ("approach", "contact", "force", "aftermath"))

    def test_a_firearm_cannot_be_fired_before_it_is_drawn(self):
        self.assertNotIn("fire", self.scene.allowed_verbs())

    def test_escalation_requires_a_recorded_reason(self):
        self.scene.apply("make_contact")
        with self.assertRaises(SceneError):
            self.scene.apply("escalate")
        self.scene.apply("escalate", reason="the subject advanced with a knife")
        self.assertEqual(self.scene.phase, "force")

    def test_drawing_a_firearm_requires_recorded_grounds(self):
        self.scene.apply("make_contact")
        self.scene.apply("escalate", reason="armed subject")
        with self.assertRaises(SceneError):
            self.scene.apply("draw_firearm")
        self.scene.apply("draw_firearm", grounds="immediate threat to a member of the public")
        self.assertIn("fire", self.scene.allowed_verbs())

    def test_a_pursuit_is_a_path_problem(self):
        self.scene.apply("make_contact")
        note = self.scene.apply("pursue")
        self.assertIn("pursuit step", note)
        self.assertEqual(self.graph.at("pc.rookie"), "loc.stair")

    def test_an_arrest_needs_the_subject_in_reach_and_a_lawful_basis(self):
        self.scene.apply("make_contact")
        self.scene.apply("pursue")
        self.assertTrue(self.graph.co_located("pc.rookie", "npc.suspect"))
        with self.assertRaises(SceneError):
            self.scene.apply("arrest")
        note = self.scene.apply("arrest", lawful_basis="caught in the act")
        self.assertIn("caught in the act", note)
        self.assertEqual(self.scene.phase, "aftermath")

    def test_an_arrest_of_someone_out_of_reach_is_refused(self):
        self.graph.move("npc.suspect", "loc.flat")
        with self.assertRaises(SceneError):
            self.scene.apply("arrest", lawful_basis="warrant")


if __name__ == "__main__":
    unittest.main()
