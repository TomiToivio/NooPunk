"""The shipped case graph obeys the same contract the table does (#718).

No Godot runtime is needed for this: the point of #718 is that the *data contract* is shared, so the
contract can be checked where the data lives. If this test passes and the Godot adapter only reads the
same file, the slice cannot drift from the table without something failing here first.

What it proves, and nothing more:
  * the graph loads and validates under the repository's own loader;
  * every competency named in the graph exists in the WN baseline's skill list;
  * every scene is reachable from the entrance, so no content is orphaned;
  * a competent investigator gets the clue and an incompetent one does not — the discovery rule is
    automatic, not a local Godot behaviour.

It does **not** prove the GDScript adapter runs; that needs a Godot binary, which this host does not have.

Stdlib unittest only — NoöPunk's CI has no pytest.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.rules.investigation import (
    ClueKind,
    Investigator,
    discover,
    load_case_graph,
)

ROOT = Path(__file__).resolve().parents[1]
CASE_GRAPH = ROOT / "data" / "scenarios" / "lakkahaltia" / "case_graph.json"
WN_BASELINE = ROOT / "data" / "rules" / "without_number.json"


def graph():
    return load_case_graph(CASE_GRAPH)


class TestTheGraphLoads(unittest.TestCase):
    def test_it_is_the_noopunk_case_graph_format(self):
        raw = json.loads(CASE_GRAPH.read_text(encoding="utf-8"))
        self.assertEqual(raw["format"], "noopunk-case-graph")
        self.assertEqual(raw["case_id"], "lakkahaltia")

    def test_it_validates(self):
        graph().validate()

    def test_it_carries_both_readings(self):
        families = graph().families()
        self.assertIn("mundane", families)
        self.assertIn("anomalous", families)


class TestCompetenciesAreReal(unittest.TestCase):
    def test_every_competency_named_in_the_graph_exists_in_the_baseline(self):
        known = set(json.loads(WN_BASELINE.read_text(encoding="utf-8"))["skills"]["names"])
        named = {
            clue.competency
            for scene in graph().case.scenes
            for clue in scene.clues
        }
        self.assertTrue(named, "the graph names no competencies at all")
        self.assertEqual(named - known, set(), f"graph names unknown competencies: {named - known}")


class TestEverySceneIsReachable(unittest.TestCase):
    def test_no_orphaned_scene(self):
        case = graph().case
        start = case.scenes[0].id
        edges: dict[str, set[str]] = {s.id: set() for s in case.scenes}
        for scene in case.scenes:
            for clue in scene.clues:
                edges[scene.id].update(clue.leads_to)

        seen, queue = {start}, [start]
        while queue:
            for nxt in edges[queue.pop()]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)

        self.assertEqual(set(edges) - seen, set(), "unreachable scenes")

    def test_no_dangling_lead(self):
        case = graph().case
        ids = {s.id for s in case.scenes}
        for scene in case.scenes:
            for clue in scene.clues:
                self.assertTrue(set(clue.leads_to) <= ids, f"{clue.id} leads nowhere real")


class TestDiscoveryIsAutomatic(unittest.TestCase):
    def test_a_competent_investigator_gets_the_core_clue_without_a_check(self):
        case = graph().case
        scene = case.scenes[0]
        core = [c for c in scene.clues if c.kind is ClueKind.CORE]
        self.assertTrue(core)
        expert = Investigator(name="expert", ratings={core[0].competency: 0})  # rank 0 is trained
        found = discover(case, scene.id, expert)
        self.assertIn(core[0].id, found.clue_ids)
        self.assertTrue(found.can_leave)

    def test_an_incompetent_investigator_gets_nothing_for_free(self):
        case = graph().case
        scene = case.scenes[0]
        novice = Investigator(name="novice", ratings={})
        found = discover(case, scene.id, novice)
        self.assertEqual(found.clue_ids, ())
        self.assertFalse(found.can_leave)


if __name__ == "__main__":
    unittest.main()
