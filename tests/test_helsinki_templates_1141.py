"""Guards for the four Helsinki worksheets (#1141, Phase 1 rework).

Issue #1141 was reworked after the first drafts: the deliverables are now **prose-led documents Tomi writes in**,
not schema templates. Its acceptance criteria say, in as many words:

    "Remove YAML, JSON, Python, schema-first forms and internal IDs from Tomi-facing writing areas"
    "A human can fill in all four documents by writing descriptive sentences ... No code, YAML, JSON,
     schema keys or database literacy is required."

So these tests enforce a *negative* property, which is the one that will actually decay: no machine syntax in the
author's files. CI discovers tests with `unittest`; do not add a pytest dependency.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"

WORLD = DESIGN / "HELSINKI_WORLD.md"
CITY = DESIGN / "HELSINKI_CITY.md"
FACTIONS = DESIGN / "HELSINKI_FACTIONS.md"
FACES = DESIGN / "HELSINKI_FACES_XENOBESTIARY.md"
ALL = (WORLD, CITY, FACTIONS, FACES)

RELATIVE_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")

#: Anything that looks like a data record rather than a sentence.
SCHEMA_LINE = re.compile(r"^\s{0,4}[a-z][a-z0-9_]{2,}\s*:\s*\S", re.MULTILINE)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TheWorksheetsAreReadableDocuments(unittest.TestCase):
    def test_all_four_documents_exist(self):
        for path in ALL:
            self.assertTrue(path.is_file(), f"missing template: {path.name}")

    def test_each_is_marked_a_worksheet_not_canon(self):
        for path in ALL:
            head = text(path)[:600].lower()
            self.assertIn("not canon", head, path.name)
            self.assertTrue("worksheet" in head or "template" in head,
                            f"{path.name} does not say what it is")
            self.assertIn("phase 1", head, path.name)

    def test_each_uses_the_shared_status_legend(self):
        for path in ALL:
            body = text(path)
            for marker in ("AUTHOR CANON", "REPOSITORY CANON", "EXAMPLE ONLY", "OPEN"):
                self.assertIn(marker, body, f"{path.name} is missing the {marker} status")

    def test_each_has_a_table_of_contents(self):
        for path in ALL:
            self.assertIn("**Contents**", text(path), path.name)

    def test_each_leaves_writing_space_and_decisions_for_the_author(self):
        for path in ALL:
            body = text(path)
            self.assertIn("<!-- Tomi writes below -->", body, path.name)
            self.assertGreaterEqual(body.count("<!-- Tomi writes below -->"), 5,
                                    f"{path.name} does not leave room to write in every section")
            self.assertIn("Unresolved decisions", body, path.name)
            self.assertIn("Record answers here", body, path.name)


class TheWorksheetsContainNoMachineSyntax(unittest.TestCase):
    """The rework's core requirement: Tomi is the writer, not a parser."""

    def test_no_fenced_code_blocks_of_any_kind(self):
        for path in ALL:
            self.assertNotIn("```", text(path), f"{path.name} contains a code fence")

    def test_no_schema_vocabulary_in_the_writing_areas(self):
        """Naming YAML only to say "you will not need it" is fine; a field name is not."""
        for path in ALL:
            body = text(path).lower()
            for word in ("serialization", "schema key", "primary key", "foreign key"):
                self.assertNotIn(word, body, f"{path.name} still talks about {word}")

    def test_no_internal_identifiers(self):
        for path in ALL:
            body = text(path)
            self.assertNotIn("hel_", body, f"{path.name} still carries internal IDs")
            for key in ("site_id", "faction_id", "entity_id", "district_id", "density_access",
                        "transition_rule", "scripted_reveal_gate"):
                self.assertNotIn(key, body, f"{path.name} still carries the field name {key}")

    def test_no_key_value_records(self):
        for path in ALL:
            body = text(path)
            hits = [m.group(0).strip() for m in SCHEMA_LINE.finditer(body)
                    if not m.group(0).strip().startswith(("*", "-", ">", "|"))]
            self.assertEqual(hits, [], f"{path.name} still contains record-style lines: {hits[:4]}")


class TheWorksheetsCoverTheRequestedScope(unittest.TestCase):
    def test_world_covers_its_seven_subjects(self):
        body = text(WORLD).lower()
        for subject in ("theme", "2045", "district", "megacorporation", "gangs", "npc"):
            self.assertIn(subject, body, f"the World worksheet does not cover {subject}")

    def test_city_covers_its_eight_subjects_and_the_three_layers(self):
        body = text(CITY).lower()
        for subject in ("timeline", "megacorporation", "organizations", "ethos", "government",
                        "crime and punishment", "social relationships", "district"):
            self.assertIn(subject, body, f"the City worksheet does not cover {subject}")
        for layer in ("physical", "cyber", "astral"):
            self.assertIn(layer, body, f"the City worksheet does not describe the {layer} layer")

    def test_city_keeps_astral_out_of_the_first_act(self):
        body = text(CITY).lower()
        self.assertIn("first act", body)
        self.assertIn("nothing", body, "the layered example should say plainly that Act I has no astral content")

    def test_factions_name_the_asset_categories_and_a_worked_turn(self):
        body = text(FACTIONS)
        for word in ("Force", "Cunning", "Wealth", "FacCred", "faction turn"):
            self.assertIn(word, body, f"the Factions worksheet is missing {word}")
        self.assertIn("one action", body.lower())

    def test_factions_keep_reputation_out_of_faction_statistics(self):
        body = text(FACTIONS).lower()
        self.assertIn("reputation is not a faction statistic", body)
        self.assertIn("strength", body)

    def test_faces_cover_four_classes_and_ordinary_people(self):
        body = text(FACES)
        for klass in ("Biologics", "Constructs", "Noetics", "Plasmoids", "Ordinary faces"):
            self.assertIn(klass, body, f"the Faces worksheet is missing {klass}")

    def test_faces_keep_the_five_axes_apart(self):
        body = text(FACES).lower()
        for axis in ("body", "ontology", "faction", "density", "layer"):
            self.assertIn(axis, body, f"the Faces worksheet does not separate {axis}")

    def test_psi_does_not_solve_investigations(self):
        body = text(FACES)
        self.assertIn("PSI_INVESTIGATION_BOUNDARY_1105.md", body)
        self.assertIn("never a proof", body.lower(), "telepathy must produce a lead, not evidence")


class EveryRelativeLinkResolves(unittest.TestCase):
    def test_no_template_links_to_a_missing_file(self):
        broken = []
        for path in ALL + (DESIGN / "README.md", ROOT / "docs" / "DOCUMENT_REGISTER.md"):
            for match in RELATIVE_LINK.finditer(text(path)):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [], "broken relative links: " + "; ".join(broken))

    def test_the_design_index_lists_all_four(self):
        body = text(DESIGN / "README.md")
        for path in ALL:
            self.assertIn(path.name, body, f"design/README.md does not list {path.name}")

    def test_the_document_register_names_the_set(self):
        self.assertIn("HELSINKI_CITY.md", text(ROOT / "docs" / "DOCUMENT_REGISTER.md"))


class TheIssueStaysOpen(unittest.TestCase):
    def test_the_documents_never_claim_phase_two_or_three_is_done(self):
        """#1141 closes only when all three phases are finished; Phase 1 must not read as completion."""
        for path in ALL:
            body = text(path).lower()
            self.assertIn("phase 1", body, path.name)
            self.assertIn("tomi", body, path.name)
            self.assertIn("your version", body, path.name)


if __name__ == "__main__":
    unittest.main()
