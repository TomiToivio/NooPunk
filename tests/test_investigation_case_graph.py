"""The case graph on the real Lakkahaltia case, and the rules the graph depends on (#704).

Two contracts are pinned here, and both are the kind that rot silently:

* **Competence is presence.** The Without Number baseline rates skills 0-4 and untrained is the
  *absence* of rank 0, so `Heal 0` is a trained investigator. A layer that required a positive
  rating would quietly disqualify every starting character.
* **A mystery has more than one reading.** The graph refuses to load unless it carries both a
  mundane and an anomalous hypothesis, so an anomaly can never be presented as already solved.
"""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from src.rules.investigation import (
    Case,
    CaseGraph,
    Clue,
    ClueKind,
    Hypothesis,
    InvestigationError,
    Investigator,
    Scene,
    discover,
    inconspicuous_finder,
    load_case_graph,
)

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "data" / "scenarios" / "lakkahaltia" / "case_graph.json"
CASE = ROOT / "data" / "scenarios" / "lakkahaltia" / "case.json"

#: The case's own sheet: Program 1, Notice 0, Talk 0 (data/scenarios/lakkahaltia/case.json).
ROMPPAINEN = Investigator.from_sheet("Romppainen", {"Program": 1, "Notice": 0, "Talk": 0})


class TheGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = load_case_graph(GRAPH)

    def test_the_real_case_graph_loads_and_validates(self) -> None:
        self.assertEqual(self.graph.case.id, "lakkahaltia")
        self.assertEqual(len(self.graph.case.scenes), 4)
        self.assertEqual(self.graph.source_case, "data/scenarios/lakkahaltia/case.json")

    def test_every_scene_has_a_core_clue(self) -> None:
        for scene in self.graph.case.scenes:
            with self.subTest(scene=scene.id):
                self.assertTrue(scene.core_clues())

    def test_the_case_sheet_can_leave_every_scene(self) -> None:
        """Rank 0 counts: the starting sheet must never meet a scene it cannot pass."""
        for scene in self.graph.case.scenes:
            with self.subTest(scene=scene.id):
                self.assertIn(scene.id, [s.id for s in self.graph.case.scenes])
                found = discover(self.graph.case, scene.id, ROMPPAINEN)
                self.assertTrue(found.can_leave, f"{scene.id} stops the case sheet")

    def test_leads_point_at_real_scenes(self) -> None:
        known = {scene.id for scene in self.graph.case.scenes}
        for scene in self.graph.case.scenes:
            for clue in scene.clues:
                for target in clue.leads_to:
                    with self.subTest(clue=clue.id, target=target):
                        self.assertIn(target, known)

    def test_the_graph_clue_ids_exist_in_the_case_data(self) -> None:
        """The graph is a reading of case.json, not a second case."""
        shipped = set(json.loads(CASE.read_text(encoding="utf-8"))["clues"])
        graph_ids = {clue.id for scene in self.graph.case.scenes for clue in scene.clues}
        self.assertEqual(graph_ids & shipped, shipped)

    def test_both_readings_are_statable_from_the_same_evidence(self) -> None:
        self.assertIn("mundane", self.graph.families())
        self.assertIn("anomalous", self.graph.families())
        self.assertGreaterEqual(len(self.graph.hypotheses), 2)
        for hypothesis in self.graph.hypotheses:
            with self.subTest(hypothesis=hypothesis.id):
                self.assertEqual(hypothesis.confidence, 0, "the model must not pre-judge")

    def test_no_clue_text_names_an_answer(self) -> None:
        """A 'fact' is an observation. If it settles the case, it is not a clue."""
        forbidden = ("proves", "definitely", "must have been", "therefore")
        for scene in self.graph.case.scenes:
            for clue in scene.clues:
                with self.subTest(clue=clue.id):
                    self.assertFalse([word for word in forbidden if word in clue.fact.lower()])


class CompetenceTest(unittest.TestCase):
    def test_rank_zero_is_competent(self) -> None:
        self.assertTrue(Investigator(name="A", ratings={"Heal": 0}).is_competent("Heal"))

    def test_an_absent_competency_is_not(self) -> None:
        self.assertFalse(Investigator(name="A", ratings={"Heal": 0}).is_competent("Program"))

    def test_a_rank_zero_competency_still_gets_the_clue(self) -> None:
        """CWN rank 0 is trained; the clue is never gated behind a positive number."""
        scene = Scene(id="s", title="S", clues=(Clue(id="c", scene_id="s", kind=ClueKind.CORE,
                                                    competency="Heal", fact="..."),))
        found = discover(Case(id="x", scenes=(scene,)), "s", Investigator(name="A", ratings={"Heal": 0}))
        self.assertTrue(found.can_leave)
        self.assertEqual(found.clue_ids, ("c",))

    def test_a_core_clue_is_granted_only_to_the_competency_that_earns_it(self) -> None:
        scene = Scene(id="s", title="S", clues=(
            Clue(id="med", scene_id="s", kind=ClueKind.CORE, competency="Heal", fact="..."),
            Clue(id="net", scene_id="s", kind=ClueKind.CORE, competency="Program", fact="..."),
        ))
        case = Case(id="x", scenes=(scene,))
        doctor = discover(case, "s", Investigator(name="D", ratings={"Heal": 1}))
        self.assertEqual(doctor.clue_ids, ("med",))
        self.assertTrue(doctor.can_leave, "one core clue of their own is enough to leave")
        self.assertTrue(discover(case, "s", Investigator(name="N", ratings={"Program": 1})).clue_ids == ("net",))


class InconspicuousTest(unittest.TestCase):
    def test_the_highest_pool_notices(self) -> None:
        clue = Clue(id="p", scene_id="s", kind=ClueKind.OPTIONAL, competency="Notice",
                    fact="...", passive=True)
        scene = Scene(id="s", title="S", clues=(clue,))
        sharp = Investigator(name="Sharp", ratings={"Notice": 2})
        blunt = Investigator(name="Blunt", ratings={"Notice": 0})
        self.assertIs(inconspicuous_finder(scene, [blunt, sharp]), sharp)

    def test_nobody_competent_notices_nothing(self) -> None:
        clue = Clue(id="p", scene_id="s", kind=ClueKind.OPTIONAL, competency="Notice",
                    fact="...", passive=True)
        scene = Scene(id="s", title="S", clues=(clue,))
        self.assertIsNone(inconspicuous_finder(scene, [Investigator(name="Blind", ratings={"Talk": 1})]))


class BenefitTest(unittest.TestCase):
    """A benefit names a CWN cost. Nothing here charges it, and no skill rank is a pool."""

    def test_a_discovered_benefit_carries_its_cost(self) -> None:
        clue = Clue(id="c", scene_id="s", kind=ClueKind.OPTIONAL, competency="Know", fact="...",
                    benefit="The story names what it wants.", benefit_cost="a Know check, an hour")
        scene = Scene(id="s", title="S", clues=(clue,))
        found = discover(Case(id="x", scenes=(scene,)), "s", Investigator.from_sheet("A", {"Know": 1}))
        self.assertEqual([(b.clue_id, b.cost) for b in found.benefits],
                         [("c", "a Know check, an hour")])

    def test_a_benefit_without_a_cost_is_refused(self) -> None:
        with self.assertRaises(InvestigationError):
            Clue(id="c", scene_id="s", kind=ClueKind.OPTIONAL, competency="Know",
                 fact="...", benefit="free insight")

    def test_the_investigator_has_no_spend_economy(self) -> None:
        """GUMSHOE spends are refused: SWN Effort is the game's one pool (AGENTS.md)."""
        self.assertFalse(hasattr(Investigator, "spend"))
        self.assertFalse(hasattr(Investigator, "pool"))


class MalformedGraphTest(unittest.TestCase):
    def write(self, payload: dict) -> Path:
        directory = tempfile.mkdtemp(prefix="noopunk-graph-")
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        path = Path(directory) / "graph.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def base(self) -> dict:
        return json.loads(GRAPH.read_text(encoding="utf-8"))

    def test_a_file_without_the_format_marker_is_refused(self) -> None:
        payload = self.base()
        del payload["format"]
        with self.assertRaises(InvestigationError):
            load_case_graph(self.write(payload))

    def test_a_single_explanation_case_is_refused(self) -> None:
        payload = self.base()
        payload["hypotheses"] = [h for h in payload["hypotheses"] if h["family"] == "anomalous"]
        with self.assertRaises(InvestigationError):
            load_case_graph(self.write(payload))

    def test_a_case_without_a_mundane_reading_is_refused(self) -> None:
        payload = self.base()
        payload["hypotheses"] = [h for h in payload["hypotheses"] if h["family"] != "mundane"]
        with self.assertRaises(InvestigationError):
            load_case_graph(self.write(payload))

    def test_a_scene_without_a_core_clue_is_refused(self) -> None:
        payload = self.base()
        payload["scenes"][0]["clues"] = [c for c in payload["scenes"][0]["clues"] if c["kind"] != "core"]
        with self.assertRaises(InvestigationError):
            load_case_graph(self.write(payload))


class ModelCannotSolveItTest(unittest.TestCase):
    def test_no_function_returns_a_verdict(self) -> None:
        graph = load_case_graph(GRAPH)
        self.assertTrue(isinstance(graph, CaseGraph))
        for hypothesis in graph.hypotheses:
            with self.subTest(hypothesis=hypothesis.id):
                self.assertIsInstance(hypothesis, Hypothesis)
                self.assertEqual(hypothesis.confidence, 0)


if __name__ == "__main__":
    unittest.main()
