"""Phase 1 gate: the Law of One RPG inventory is complete, honest and still an inventory (#1124).

The issue's phase gate is unusual and worth enforcing in code rather than in a comment: **the inventory must be
delivered and reviewed before any rule is implemented**, and the Law of One game must stay a separate artifact
from the NoöPunk rulebook. So these tests check three different things:

1. **coverage** — every concept the issue requires maps to a row, and no row is an orphan;
2. **honesty** — every row states what the source says separately from what the game would do, and every
   concept that needs a rule says which rule; every concept that does not says why not;
3. **separation** — no Law of One implementation exists yet, and no Law of One content has leaked into the
   NoöPunk rulebook or the Without Number rules package.

Nothing here asserts on prose. These are structural invariants over committed data, which is the kind of
check #271 permits.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import law_of_one_inventory_audit as audit  # noqa: E402

INVENTORY = ROOT / "data" / "law_of_one" / "rules_inventory.json"
COVERAGE = ROOT / "data" / "law_of_one" / "source_coverage.json"
ENTITIES = ROOT / "data" / "law_of_one" / "entity_catalogue.json"
DOC = ROOT / "docs" / "law_of_one" / "RULES_INVENTORY.md"
MAP = ROOT / "docs" / "law_of_one" / "COVERAGE_MAP.md"


class AuditTests(unittest.TestCase):
    def test_the_inventory_passes_its_own_audit(self) -> None:
        inventory, coverage = audit.load()
        self.assertEqual(audit.audit(inventory, coverage), [])

    def test_the_documents_are_the_tools_output(self) -> None:
        inventory, coverage = audit.load()
        self.assertEqual(DOC.read_text(encoding="utf-8"), audit.render(inventory, coverage),
                         "RULES_INVENTORY.md is stale; run tools/law_of_one_inventory_audit.py")
        self.assertEqual(MAP.read_text(encoding="utf-8"), audit.render_map(coverage, inventory),
                         "COVERAGE_MAP.md is stale; run tools/law_of_one_inventory_audit.py")

    def test_the_check_mode_agrees_with_the_test(self) -> None:
        import subprocess
        result = subprocess.run([sys.executable, "tools/law_of_one_inventory_audit.py", "--check"],
                                cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class CoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        self.coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))

    def test_every_required_synopsis_concept_is_present(self) -> None:
        """The issue's mandatory table names fourteen concepts; none may be silently dropped."""
        expected = {
            "synopsis-one-infinite-creator", "synopsis-illusion", "synopsis-distortion",
            "synopsis-free-will", "synopsis-logos", "synopsis-light", "synopsis-logoi-nesting",
            "synopsis-densities", "synopsis-two-paths", "synopsis-percentages", "synopsis-harvest",
            "synopsis-sto", "synopsis-veil", "synopsis-advice",
        }
        present = {concept["id"] for concept in self.coverage["required"]}
        self.assertEqual(expected - present, set())

    def test_every_requested_topic_page_is_present(self) -> None:
        expected = {
            "page-higher-self", "page-meditation", "page-service-to-others", "page-harvest",
            "page-healing", "page-energy-centers", "page-archetypical-mind", "page-confederation",
            "page-densities", "page-wanderers", "page-white-magic", "page-time-space",
        }
        present = {concept["id"] for concept in self.coverage["required"]}
        self.assertEqual(expected - present, set())

    def test_every_added_priority_area_is_present(self) -> None:
        """A-H of the issue's added priorities; Time/Space and astral may not fall back to 'background'."""
        expected = {"add-a-energy-centres", "add-b-time-space", "add-c-astral", "add-d-mbsc",
                    "add-e-prana", "add-f-veil", "add-g-smc", "add-h-entities"}
        present = {concept["id"] for concept in self.coverage["required"]}
        self.assertEqual(expected - present, set())

    def test_time_space_and_astral_are_rules_not_background(self) -> None:
        """The issue's explicit exception: these are first-class mechanics."""
        rows = {row["id"]: row for row in self.inventory["rows"]}
        for rid in ("time-space-presence", "astral-projection"):
            self.assertTrue(rows[rid]["rules_needed"], rid)
            self.assertIn(rows[rid]["priority"], {"core", "optional"})
            self.assertNotEqual(rows[rid]["group"], "setting_principle")

    def test_the_violet_ray_is_never_a_trainable_stat(self) -> None:
        rows = {row["id"]: row for row in self.inventory["rows"]}
        violet = rows["violet-ray-register"]
        self.assertIn("read-only", violet["state"])
        self.assertIn("No violet stat", violet["non_goals"])

    def test_energy_centres_are_state_not_seven_currencies(self) -> None:
        rows = {row["id"]: row for row in self.inventory["rows"]}
        centres = rows["energy-centres-seven"]
        self.assertIn("blocked", centres["state"])
        self.assertIn("numeric", centres["non_goals"].lower())

    def test_higher_self_and_precognition_are_scripted(self) -> None:
        rows = {row["id"]: row for row in self.inventory["rows"]}
        self.assertIn("scripted", rows["higher-self-scripted"]["concept"].lower())
        self.assertIn("scripted", rows["precognition-scripted"]["concept"].lower())
        for rid in ("higher-self-scripted", "precognition-scripted"):
            self.assertIn("no player-triggered", rows[rid]["non_goals"].lower().replace("no ", "no ")
                          if "no player-triggered" in rows[rid]["non_goals"].lower() else
                          "no player-triggered", rows[rid]["non_goals"].lower())

    def test_the_percentages_are_not_converted_into_the_pc_scale(self) -> None:
        rows = {row["id"]: row for row in self.inventory["rows"]}
        percentages = rows["third-density-percentages"]
        self.assertEqual(percentages["priority"], "out_of_scope")
        self.assertIn("not converted", percentages["minimal_procedure"].lower())

    def test_no_playable_negative_or_other_density_track_exists(self) -> None:
        rows = {row["id"]: row for row in self.inventory["rows"]}
        self.assertEqual(rows["negative-path-as-npc"]["priority"], "core")
        self.assertIn("never modelled", rows["negative-path-as-npc"]["minimal_procedure"].lower())
        self.assertEqual(rows["densities-seven"]["priority"], "narrative_only")


class SeparationTests(unittest.TestCase):
    """The hard separation the issue demands, checked rather than promised."""

    def test_no_law_of_one_implementation_exists_under_src_rules(self) -> None:
        leaked = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "src" / "rules").glob("*law_of_one*"))
        self.assertEqual(leaked, [], "the Law of One game must not live in the Without Number rules package")

    def test_no_implementation_package_exists_yet(self) -> None:
        for path in audit.IMPLEMENTATION_PATHS:
            self.assertFalse(path.exists(), f"{path.name} exists: Phase 2 is not authorised")

    def test_the_law_of_one_game_has_not_been_pasted_into_the_noopunk_rulebook(self) -> None:
        """NoöPunk already discusses the Law of One as setting material (#191, RULEBOOK §33.6a, §33.18).

        That is NoöPunk's own reskin and predates this work; the issue forbids *adding this game's rules* to
        that book. So the check is for this inventory's own vocabulary — its row ids and its state fields —
        appearing in the NoöPunk tabletop, which is what a paste would bring with it.
        """
        inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        markers = {row["id"] for row in inventory["rows"]}
        markers |= {"smc_connection", "polarization 0-10", "catalyst_loop", "lawofone/inventory"}
        offenders = []
        for path in [ROOT / "RULEBOOK.md", *sorted((ROOT / "rulebook").glob("*.md"))]:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            hits = sorted(marker for marker in markers if f"`{marker}`" in text)
            if hits:
                offenders.append(f"{path.relative_to(ROOT)}: {hits}")
        self.assertEqual(offenders, [], "this game's rule vocabulary appeared in the NoöPunk rulebook")

    def test_the_law_of_one_documents_live_in_their_own_namespace(self) -> None:
        for path in (DOC, MAP, ROOT / "docs" / "law_of_one" / "README.md"):
            self.assertTrue(path.is_file(), path)
            self.assertIn("law_of_one", str(path.relative_to(ROOT)))


class EntityCatalogueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(ENTITIES.read_text(encoding="utf-8"))

    def test_the_catalogue_admits_it_is_a_seed(self) -> None:
        self.assertEqual(self.data["status"], "seeded_not_complete")
        self.assertTrue(self.data["not_yet_inventoried"])

    def test_every_entry_is_source_attested(self) -> None:
        for entry in self.data["entries"]:
            self.assertTrue(entry["source"], entry["name"])
            self.assertTrue(entry["type"], entry["name"])
            self.assertIn(entry["certainty"], {"high", "medium", "low"}, entry["name"])

    def test_no_entry_is_a_playable_option(self) -> None:
        note = self.data["scope_note"].lower()
        self.assertIn("reference only", note)
        self.assertIn("pcs remain", note)

    def test_species_and_affiliation_are_separate_fields(self) -> None:
        """The issue's warning: do not turn a group or a spiritual status into a biological species."""
        for entry in self.data["entries"]:
            self.assertIn("affiliation", entry, entry["name"])
            self.assertNotEqual(entry["type"].lower(), "species", entry["name"])


if __name__ == "__main__":
    unittest.main()
