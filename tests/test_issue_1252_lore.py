"""#1252: the political lore exists, is cross-referenced, and does not settle what the author left open.

The dangerous failure mode for a lore brief of this size is not a typo. It is an agent **finishing the
sentence**: deciding who caused the NHI Crisis, merging two factions that were left separate, or
turning a deliberate gap into a date. These tests exist to fail when that happens.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.world.graphs import WorldGraphs  # noqa: E402

DOC = ROOT / "docs/world/POLITICS_1252.md"
GRAPH = ROOT / "data/world/politics_1252_graph.json"

#: The six groupings the author named. If one disappears, the taxonomy has been rewritten by accident.
SIX_GROUPINGS = ("nhi.noetics", "nhi.biologics", "nhi.sirians", "nhi.confederacy",
                 "nhi.orion", "nhi.machine")


class DocumentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = DOC.read_text(encoding="utf-8")

    def test_the_document_exists_and_carries_the_author_direction_banner(self):
        self.assertIn("author-directed", self.text)
        self.assertIn("#1252", self.text)

    def test_the_three_governments_are_all_present_with_their_directions(self):
        for phrase in ("EU / federal", "Finland / state", "Greater Helsinki / city",
                       "decelerationist", "Accelerationist"):
            self.assertIn(phrase, self.text, phrase)

    def test_the_three_lawful_instructions_rule_is_stated(self):
        self.assertIn("three lawful instructions", self.text)

    def test_sampo_is_not_written_as_a_rogue_deep_state(self):
        self.assertIn("not a rogue deep state", self.text)

    def test_the_soviet_contact_history_is_dated_against_the_1991_collapse(self):
        self.assertIn("1991", self.text)
        self.assertIn("pre-1991", self.text)

    def test_every_cross_reference_the_issue_named_is_present(self):
        for issue in ("#1121", "#1005", "#1156", "#1236", "#922", "#921", "#1255"):
            self.assertIn(issue, self.text, issue)

    def test_the_timeline_marks_unfixed_dates_instead_of_inventing_them(self):
        self.assertGreaterEqual(self.text.count("TBD"), 10,
                                "the brief leaves many dates open; a filled-in calendar is a canon decision")

    def test_the_document_declares_that_it_adds_no_mechanics(self):
        self.assertIn("no mechanics", self.text)
        self.assertIn("CWN remains the immutable core", self.text)


class CulpabilityTests(unittest.TestCase):
    """The author's account ended mid-sentence after 'although'. It must stay unfinished."""

    def setUp(self) -> None:
        self.text = DOC.read_text(encoding="utf-8").lower()

    def test_the_culpability_is_explicitly_unresolved(self):
        self.assertIn("culpability is unresolved", self.text)

    def test_no_agent_has_finished_the_sentence(self):
        for claim in ("eldrich caused", "eros caused", "eldrich is responsible for the nhi crisis",
                      "eros is responsible for the nhi crisis"):
            self.assertNotIn(claim, self.text, f"the document settles what the author left open: {claim}")

    def test_the_document_says_accusation_is_not_verdict(self):
        self.assertIn("accusation, not verdict", self.text)


class GraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(GRAPH.read_text(encoding="utf-8"))
        self.graphs = WorldGraphs.from_dict(self.payload)

    def test_the_political_graph_loads_through_the_existing_loader(self):
        self.assertIn("social", self.payload)
        self.assertTrue(self.graphs.social.nodes)

    def test_all_six_groupings_are_nodes(self):
        for node in SIX_GROUPINGS:
            self.assertIn(node, self.graphs.social.nodes, node)

    def test_the_three_governments_and_sampo_are_nodes(self):
        for node in ("gov.eu", "gov.finland", "gov.helsinki", "org.sampo"):
            self.assertIn(node, self.graphs.social.nodes, node)

    def test_every_edge_connects_known_nodes(self):
        for edge in self.payload["social"]["edges"]:
            self.assertIn(edge["source"], self.graphs.social.nodes)
            self.assertIn(edge["target"], self.graphs.social.nodes)

    def test_the_relationship_scores_stay_inside_the_existing_band(self):
        for edge in self.payload["social"]["edges"]:
            self.assertGreaterEqual(edge["score"], -4)
            self.assertLessEqual(edge["score"], 4)

    def test_the_zones_are_physical_nodes(self):
        for node in ("loc.zone_karjala", "loc.zone_kainuu", "loc.zone_lappi",
                     "loc.eez_vantaa", "loc.eez_espoo"):
            self.assertIn(node, self.graphs.physical.nodes, node)

    def test_the_diplomatic_island_is_a_placeholder_not_an_invented_location(self):
        node = self.graphs.physical.nodes["loc.diplomatic_island"]
        self.assertIn("TBD", node.label)


class ReconciliationTests(unittest.TestCase):
    def test_the_older_faction_taxonomy_is_pointed_at_rather_than_rewritten(self):
        old = (ROOT / "docs/world/NHI_FACTIONS_922.md").read_text(encoding="utf-8")
        self.assertIn("#1252", old)
        self.assertIn("Zookeepers", old)

    def test_the_zookeeper_question_is_resolved_by_1254(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Zookeepers", text)
        self.assertIn("#1254 resolves the former TBD", text)
        self.assertIn("are distinct entities", text)


if __name__ == "__main__":
    unittest.main()
