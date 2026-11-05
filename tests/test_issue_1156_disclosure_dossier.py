"""Guards for the disclosure dossier and the scenario proposal (#1156).

The issue asks for **two separate documents, both explicitly not canon**, with real-world claims
attributed and fictional claims labelled. That separation is the property that decays first: a later
edit merges the files, or promotes the proposal into canon by dropping its banner.

These tests describe the documents as they actually landed, not as anyone imagined them.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs/research/UFO_DISCLOSURE_BACKGROUND_RESEARCH.md"
PROPOSAL = ROOT / "docs/proposals/UFO_DISCLOSURE_NHI_CRISIS_SCENARIO_DRAFT.md"

LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(path: Path) -> str:
    return re.sub(r"\s+", " ", text(path))


class TwoDocumentsTwoJobs(unittest.TestCase):
    def test_both_exist(self):
        self.assertTrue(RESEARCH.is_file(), "the research dossier is missing")
        self.assertTrue(PROPOSAL.is_file(), "the proposal is missing")

    def test_the_proposal_says_it_is_not_canon(self):
        head = text(PROPOSAL)[:900].upper()
        self.assertIn("PROPOSAL", head)
        self.assertIn("NOT CANON", head)

    def test_the_proposal_defers_to_existing_canon(self):
        body = flat(PROPOSAL).lower()
        self.assertIn("nothing here is binding", body)
        self.assertTrue("wins wherever this document disagrees" in body
                        or "existing canon" in body)

    def test_the_research_document_is_marked_as_research_not_canon(self):
        head = text(RESEARCH)[:700].lower()
        self.assertTrue("not canon" in head or "research" in head)


class TheResearchKeepsItsDiscipline(unittest.TestCase):
    def test_it_defines_the_labels_it_uses(self):
        body = text(RESEARCH)
        self.assertIn("## 0. Method", body)
        section = body.split("## 0. Method")[1].split("## 1.")[0]
        self.assertIn("label", section.lower())

    def test_at_least_eight_hypotheses(self):
        body = text(RESEARCH)
        self.assertRegex(body, r"## \d+\. (Eight|Nine|Ten|Eleven|Twelve) explanatory hypotheses")

    def test_species_and_craft_catalogues_exist(self):
        body = text(RESEARCH)
        self.assertIn("## 5. Species and entity catalogue", body)
        self.assertIn("## 6. Craft and phenomenon catalogue", body)

    def test_every_catalogue_row_carries_an_assignment(self):
        """A catalogue without confirmed/suggested/contested/unknown is a bestiary."""
        body = text(RESEARCH)
        section = body.split("## 5. Species and entity catalogue")[1].split("## 6.")[0]
        rows = [line for line in section.splitlines()
                if line.startswith("| **") and line.count("|") >= 6]
        self.assertGreaterEqual(len(rows), 8, "the species catalogue lost its rows")
        for row in rows:
            lowered = row.lower()
            self.assertTrue(any(word in lowered for word in
                                ("confirmed", "suggested", "contested", "unknown")),
                            f"row has no evidence assignment: {row[:70]}")

    def test_finland_is_documented_not_invented(self):
        body = text(RESEARCH)
        for anchor in ("1933", "1946", "1947"):
            self.assertIn(anchor, body, f"Finnish anchor {anchor} is missing")
        section = body.split("## 7. Finland")[1].split("## 8.")[0]
        self.assertIn("documented", section.lower())

    def test_the_three_scholars_are_attributed(self):
        body = text(RESEARCH)
        for name in ("Pasulka", "Wendt", "Duvall", "Dolan"):
            self.assertIn(name, body)

    def test_it_has_a_bibliography_with_sources(self):
        body = text(RESEARCH)
        self.assertIn("## 10. Bibliography", body)
        self.assertGreaterEqual(body.count("http"), 10, "the bibliography is too thin to verify")

    def test_it_records_disputed_evidence(self):
        body = text(RESEARCH)
        self.assertIn("disputed", body.lower())


class TheProposalCoversTheAsks(unittest.TestCase):
    def test_eight_stages(self):
        body = text(PROPOSAL)
        self.assertEqual(len(re.findall(r"### 1\.\d+ Stage", body)), 8,
                         "the eight-stage cascade lost a stage")

    def test_finland_lived_experience(self):
        body = text(PROPOSAL)
        self.assertIn("Finland: the lived crisis", body)
        self.assertIn("First-person timeline", body)
        self.assertIn("Europol case briefing", body)

    def test_helsinki_detail_and_mission_locations(self):
        body = text(PROPOSAL)
        self.assertIn("Helsinki in 2045", body)
        self.assertIn("Locations for specific missions", body)
        for place in ("Kurvi", "Porkkala", "Vuosaari", "Malmi", "Suomenlinna"):
            self.assertIn(place, body, f"{place} is missing from the location list")

    def test_it_names_what_would_have_to_change(self):
        body = text(PROPOSAL)
        for target in ("ALTERNATE_HISTORY_1114.md", "NHI_CRISIS_921.md", "rulebook/7_TIMELINE.md"):
            self.assertIn(target, body, f"the impact map does not mention {target}")

    def test_it_adds_no_rules(self):
        body = flat(PROPOSAL).lower()
        self.assertTrue("no rule" in body or "no cwn" in body or "rules are untouched" in body)


class LinksResolve(unittest.TestCase):
    def test_every_relative_link_resolves(self):
        broken = []
        for path in (RESEARCH, PROPOSAL):
            for match in LINK.finditer(text(path)):
                target = match.group(1)
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.parent.name}/{path.name} -> {target}")
        self.assertEqual(broken, [], "broken links: " + "; ".join(broken))


if __name__ == "__main__":
    unittest.main()
