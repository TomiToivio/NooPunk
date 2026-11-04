"""The four Helsinki author worksheets (#1141) stay worksheets, and stay link-correct.

Phase 1 of #1141 is documentation: four author-first templates. The failure mode is not a syntax error —
it is a worksheet that quietly turns into canon (an example promoted to setting), a placeholder filled in
by an agent, a rule citation that drifts from the catalogue the repository actually verified, or a
cross-link that rots. These tests are the deterministic part of that.

They test the **documents**, not a rules engine: #1141 authorizes no implementation.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import json
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


def flat(path: Path) -> str:
    """The document as one line of prose, so wrapped markdown still matches."""
    return " ".join(path.read_text(encoding="utf-8").split())


def raw(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TheFourWorksheetsExist(unittest.TestCase):
    def test_all_four_documents_exist_where_the_issue_asked(self):
        for path in ALL:
            self.assertTrue(path.is_file(), f"missing worksheet: {path.name}")

    def test_each_declares_itself_a_draft_and_not_canon(self):
        for path in ALL:
            head = raw(path)[:600]
            self.assertIn("DRAFT", head, path.name)
            self.assertIn("NOT CANON", head, path.name)
            self.assertIn("1141", head, path.name)

    def test_each_carries_the_shared_status_legend(self):
        for path in ALL:
            body = raw(path)
            for status in ("AUTHOR CANON", "REPOSITORY CANON", "EXAMPLE ONLY", "OPEN"):
                self.assertIn(status, body, f"{path.name} lacks the {status} status")

    def test_each_leaves_writing_space_for_the_author(self):
        for path in ALL:
            self.assertIn("<!-- Tomi writes below -->", raw(path), path.name)


class WorldWorksheet(unittest.TestCase):
    def test_all_seven_sections_are_present(self):
        body = raw(WORLD)
        for heading in ("Cyberpunk Themes", "The World", "The City", "Districts",
                        "Megacorps", "Gangs", "NPCs"):
            self.assertIn(heading, body, f"world worksheet missing: {heading}")

    def test_it_defers_governance_to_the_author_files(self):
        body = raw(WORLD)
        self.assertIn("GREATER_HELSINKI_2045.md", body)
        self.assertIn("ZONES.md", body)


class CityWorksheet(unittest.TestCase):
    def test_every_cwn_city_section_is_present(self):
        body = raw(CITY)
        for heading in ("A Timeline of Collapse", "The Megacorps", "Other Groups and Organizations",
                        "The Ethos of the City", "The City Government", "Crime and Punishment",
                        "Social Relationships in the City", "The Districts of the City"):
            self.assertIn(heading, body, f"city worksheet missing: {heading}")

    def test_the_three_layers_are_modelled_separately(self):
        body = flat(CITY)
        for layer in ("Physical", "Cyber", "Astral"):
            self.assertIn(layer, body)

    def test_the_metaphysical_axes_are_not_conflated(self):
        body = flat(CITY)
        self.assertIn("Space/Time versus Time/Space", body)
        self.assertIn("Third/Fourth Density", body)
        self.assertIn("Interdimensional Hypothesis", body)
        self.assertIn("not another map axis", body)

    def test_the_layered_site_record_carries_the_required_keys(self):
        body = raw(CITY)
        for key in ("site_id", "district_id", "physical_site", "cyber_site", "astral_site", "realm",
                    "density_access", "transition_rule", "scripted_reveal_gate", "GM_secrets",
                    "known_tunnels"):
            self.assertIn(key, body, f"site record missing {key}")

    def test_real_tunnels_are_not_declared_traversable(self):
        body = flat(CITY)
        self.assertIn("No real restricted route is declared public or traversable", body)
        self.assertIn("fictional_2045", body)

    def test_act_one_keeps_the_astral_layer_out_of_play(self):
        body = flat(CITY)
        self.assertIn("Act I", body)
        self.assertIn("gm_only: true", body)


class FactionsWorksheet(unittest.TestCase):
    def test_it_names_the_swn_statistics(self):
        body = flat(FACTIONS)
        for token in ("Force", "Cunning", "Wealth", "FacCreds"):
            self.assertIn(token, body)

    def test_it_samples_a_verified_row_for_every_asset_category(self):
        """The sample ids and values must match the repository's extracted catalogue, not memory."""
        # Loaded by glob, not by literal name: the CWN parity audit treats a test that *mentions* an
        # implementation module as evidence that the section is tested, and a documentation guard is not
        # evidence for any rule. Keeping the stem out of this file keeps the matrix honest.
        catalogue_path = next((ROOT / "data" / "rules").glob("*faction_asset*.json"))
        catalogue = {
            asset["id"]: asset
            for asset in json.loads(catalogue_path.read_text(encoding="utf-8"))["assets"]
        }
        body = raw(FACTIONS)
        for asset_id, category in (("false_front", "Cunning"), ("hitmen", "Force"),
                                   ("franchise", "Wealth")):
            self.assertIn(asset_id, body, f"no {category} sample row")
            row = catalogue[asset_id]
            self.assertIn(str(row["cost"]), body)
            self.assertIn(str(row["hp"]), body)

    def test_it_does_not_fabricate_scores(self):
        body = raw(FACTIONS)
        self.assertIn("TBD", body)

    def test_wwn_and_awn_are_delegate_modes(self):
        body = flat(FACTIONS)
        for mode in ("swn_faction", "wwn_project", "awn_enclave"):
            self.assertIn(mode, body)

    def test_it_keeps_character_reputation_out_of_faction_statistics(self):
        body = flat(FACTIONS)
        self.assertIn("1137", body)
        self.assertIn("NOT faction rating", body)

    def test_the_page_number_discrepancy_is_recorded_not_hidden(self):
        """The worksheet cites 218/220/222; the extracted catalogue records 219/221/223."""
        body = flat(FACTIONS)
        self.assertIn("page numbering must be reconciled", body.lower())


class FacesWorksheet(unittest.TestCase):
    def test_all_four_nhi_classes_have_a_card(self):
        body = raw(FACES)
        for klass in ("Biologics", "Constructs", "Noetics", "Plasmoids"):
            self.assertIn(klass, body, f"no {klass} card")

    def test_an_ordinary_street_face_is_present(self):
        body = raw(FACES)
        self.assertIn("Ordinary CWN street face", body)
        self.assertIn("ordinary human", body)

    def test_the_classification_axes_are_distinct_fields(self):
        body = flat(FACES)
        for field in ("body_type", "ontology_claim", "faction_ref", "density", "realm",
                      "encounter_layers"):
            self.assertIn(field, body)

    def test_a_cyber_only_process_is_not_a_being(self):
        body = flat(FACES)
        self.assertIn("cyber-only script", body)
        self.assertIn("not a Construct or a Noetic", body)

    def test_no_invented_alien_stat_blocks(self):
        body = raw(FACES)
        self.assertIn("TBD", body)
        self.assertIn("Xenobestiary", body)


class LinksAndIndexes(unittest.TestCase):
    def test_no_worksheet_links_to_a_missing_file(self):
        broken = []
        for path in ALL + (DESIGN / "README.md",):
            for match in RELATIVE_LINK.finditer(raw(path)):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [], "broken relative links: " + "; ".join(broken))

    def test_the_design_index_points_at_the_worksheets(self):
        body = raw(DESIGN / "README.md")
        for path in ALL:
            self.assertIn(path.name, body, f"design/README.md does not list {path.name}")

    def test_the_document_register_names_the_set(self):
        self.assertIn("HELSINKI_CITY.md", raw(ROOT / "docs" / "DOCUMENT_REGISTER.md"))


if __name__ == "__main__":
    unittest.main()
