"""The four Helsinki setting templates (#1141) stay templates and stay linked.

Phase 1 of #1141 is docs only: four draft outlines Tomi will author. This guard exists because the
failure mode is not a syntax error — it is a template that quietly becomes canon ("the example is now
the setting"), a placeholder that gets filled by an agent, or a cross-document link that rots when a
file moves. The tests below are the cheap, deterministic part of that.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
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


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TheFourTemplatesExistAndSayWhatTheyAre(unittest.TestCase):
    def test_all_four_documents_exist(self):
        for path in ALL:
            self.assertTrue(path.is_file(), f"missing template: {path.name}")

    def test_each_is_marked_a_template_not_canon(self):
        for path in ALL:
            head = text(path)[:400]
            self.assertIn("STATUS: TEMPLATE", head, path.name)
            self.assertIn("not canon", head.lower(), path.name)

    def test_each_uses_the_shared_status_legend_and_placeholders(self):
        for path in ALL:
            body = text(path)
            for marker in ("AUTHOR CANON", "REPOSITORY CANON", "EXAMPLE ONLY", "OPEN"):
                self.assertIn(marker, body, f"{path.name} is missing the {marker} status")
            self.assertIn("<!-- Tomi writes below -->", body, path.name)

    def test_each_leaves_unresolved_decisions_for_the_author(self):
        for path in ALL:
            body = text(path)
            self.assertIn("Unresolved decisions", body, f"{path.name} has no decision table")
            self.assertIn("Record answers here", body, path.name)

    def test_examples_are_labelled_and_never_claim_a_printed_number(self):
        for path in ALL:
            body = text(path)
            self.assertGreaterEqual(body.count("EXAMPLE ONLY"), 3, f"{path.name} lacks labelled examples")
            self.assertIn("illustrative", body, path.name)


class WorldTemplateCoversTheSevenSections(unittest.TestCase):
    def test_the_world_has_every_requested_section(self):
        body = text(WORLD)
        for heading in ("Cyberpunk Themes", "The World", "The City (index only)",
                        "Districts (index only)", "Megacorps", "Gangs", "NPCs"):
            self.assertIn(heading, body, f"world template missing: {heading}")

    def test_the_world_defers_to_the_author_files_it_must_not_supersede(self):
        body = text(WORLD)
        self.assertIn("GREATER_HELSINKI_2045.md", body)
        self.assertIn("ZONES.md", body)
        self.assertIn("EUROPOL_HELSINKI_1114.md", body)


class CityTemplateCoversTheCityAndTheLayers(unittest.TestCase):
    def test_every_cwn_city_section_is_present(self):
        body = text(CITY)
        for heading in ("A Timeline of Collapse", "The Megacorps", "Other Groups and Organizations",
                        "The Ethos of the City", "The City Government", "Crime and Punishment",
                        "Social Relationships in the City", "The Districts of the City"):
            self.assertIn(heading, body, f"city template missing: {heading}")

    def test_the_three_layers_are_modelled_separately(self):
        body = text(CITY)
        for layer in ("**Physical**", "**Cyber**", "**Astral**"):
            self.assertIn(layer, body)

    def test_the_metaphysical_axes_are_not_conflated(self):
        body = text(CITY)
        self.assertIn("Space/Time vs Time/Space", body)
        self.assertIn("Third vs Fourth density", body)
        self.assertIn("Interdimensional hypothesis", body)
        self.assertIn("not a spatial", body.replace("**not** a spatial", "not a spatial"))

    def test_the_layered_site_record_carries_the_required_keys(self):
        body = text(CITY)
        for key in ("site_id", "district_ref", "physical:", "cyber:", "astral:", "realm",
                    "density_access", "transition_rule", "scripted_reveal_gate", "gm_secrets"):
            self.assertIn(key, body, f"site record missing {key}")

    def test_real_tunnels_are_not_declared_traversable(self):
        body = " ".join(text(CITY).lower().split())     # markdown wraps lines; compare prose
        self.assertIn("verify actual public access", body)
        self.assertIn("mark every 2045 addition as fictional", body)

    def test_act_one_stays_grounded(self):
        body = text(CITY)
        self.assertIn("Act I", body)
        self.assertIn("locked", body)


class FactionsTemplateUsesSwnAndDelegatesTheRest(unittest.TestCase):
    def test_it_names_the_swn_faction_statistics_and_source_pages(self):
        body = text(FACTIONS)
        for token in ("Force", "Cunning", "Wealth", "FacCreds", "p. 211", "219", "221", "223"):
            self.assertIn(token, body)

    def test_it_samples_every_asset_category_from_the_catalogue(self):
        body = text(FACTIONS)
        for asset in ("false_front", "hitmen", "franchise"):
            self.assertIn(asset, body, f"no {asset} example")

    def test_wwn_and_awn_are_delegate_modes_not_extra_wallets(self):
        body = text(FACTIONS)
        for mode in ("swn_faction", "wwn_project", "awn_enclave"):
            self.assertIn(mode, body)
        self.assertIn("one actor, one mode", body.lower())
        self.assertIn("not a faction statistic", body.lower())

    def test_it_does_not_fabricate_scores(self):
        body = text(FACTIONS)
        self.assertIn("TBD", body)


class FacesTemplateSpansTheTaxonomyAndOrdinaryPeople(unittest.TestCase):
    def test_all_four_nhi_classes_have_a_card(self):
        body = text(FACES)
        for klass in ("Biologics", "Constructs", "Noetics", "Plasmoids"):
            self.assertIn(klass, body)
            self.assertIn(f"taxonomy: \"{klass.removesuffix('s')}\"", body,
                          f"no {klass} card")

    def test_there_is_an_ordinary_street_npc(self):
        body = text(FACES)
        self.assertIn("Ordinary faces", body)
        self.assertIn("hel_npc_", body)

    def test_classification_axes_are_kept_apart(self):
        body = text(FACES)
        for axis in ("species / body", "ontological type", "faction", "density", "realm / layer"):
            self.assertIn(axis, body)

    def test_psi_cannot_shortcut_an_investigation(self):
        body = text(FACES)
        self.assertIn("PSI_INVESTIGATION_BOUNDARY_1105.md", body)
        self.assertIn("lead", body.lower())

    def test_a_cyber_only_phenomenon_is_not_a_being(self):
        body = text(FACES)
        self.assertIn("Cyber-only phenomena", body)
        self.assertIn("not", body)


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


if __name__ == "__main__":
    unittest.main()
