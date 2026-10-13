"""Executable contracts for the two PSI prototypes (issue #345, acceptance criterion 3).

Code-only, per `AGENTS.md` and issue #271. These exercise the **scenes**: that both resolve on the one
existing engine, that PSI is treated as established mainstream science rather than a debunking puzzle,
that a counter-PSI specialist can genuinely deny access, that the commercial case produces incompatible
accounts and an honest answer to the client, and that the fiction stays quotidian rather than becoming
spellcasting.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_psi_scenes.py"
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game import psi_scenes as ps  # noqa: E402
from strategy_game.map_spec import load_map_spec  # noqa: E402
from strategy_game.rpg.fate import Resolution  # noqa: E402


class EverydayEncounterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scene = ps.everyday_psi_encounter()

    def test_both_checks_resolve_on_the_one_existing_engine(self) -> None:
        self.assertIsInstance(self.scene.noticing, Resolution)
        self.assertIsInstance(self.scene.resistance, Resolution)

    def test_noticing_and_resistance_are_different_actions(self) -> None:
        self.assertEqual(self.scene.noticing.action.value, "overcome")
        self.assertEqual(self.scene.resistance.action.value, "defend")

    def test_the_anomaly_is_ordinary_not_phenomenal(self) -> None:
        """Quotidian surrealism: the unsettling thing is administrative, not a manifestation."""
        text = self.scene.anomaly.lower()
        for banned in ("levitat", "telekine", "fireball", "portal", "apparition", "glowing"):
            self.assertNotIn(banned, text, banned)

    def test_the_scene_refuses_to_prove_anything(self) -> None:
        self.assertTrue(self.scene.what_it_does_not_prove)
        self.assertIn("fit the same evidence", self.scene.what_it_does_not_prove)

    def test_nothing_creates_innate_psi_in_the_witness(self) -> None:
        self.assertEqual(self.scene.witness, "everyday-commuter")

    def test_it_is_deterministic(self) -> None:
        self.assertEqual(ps.everyday_psi_encounter(5).noticing.dice,
                         ps.everyday_psi_encounter(5).noticing.dice)

    def test_the_anomaly_varies_with_the_seed(self) -> None:
        seen = {ps.everyday_psi_encounter(s).anomaly for s in range(len(ps.EVERYDAY_ANOMALIES))}
        self.assertEqual(len(seen), len(ps.EVERYDAY_ANOMALIES))


class CommercialInvestigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scene = ps.commercial_counter_psi_investigation()

    def test_it_declares_a_real_psi_operation(self) -> None:
        self.assertEqual(self.scene["operation"]["id"], "op-harbour-audit")
        self.assertEqual(self.scene["operation"]["approach"], "remote_viewing")

    def test_the_operation_plays_in_canonical_geography(self) -> None:
        self.assertIn(self.scene["operation"]["location_id"], ps.CANONICAL_LOCATIONS)

    def test_the_location_vocabulary_matches_the_validated_map(self) -> None:
        """The scenes must not invent geography the map specification does not know."""
        self.assertEqual(set(ps.CANONICAL_LOCATIONS), set(load_map_spec().node_ids))

    def test_both_readings_resolve_on_the_same_engine(self) -> None:
        self.assertIsInstance(self.scene["access"], Resolution)
        self.assertIsInstance(self.scene["counter_psi"], Resolution)

    def test_a_counter_psi_specialist_can_deny_access(self) -> None:
        """The strongest move must be a refusal of access, so PSI is never unrestricted."""
        across_seeds = [ps.commercial_counter_psi_investigation(s)["access_held"] for s in range(60)]
        self.assertIn(False, across_seeds, "countermeasures must be able to win sometimes")

    def test_access_is_sometimes_held_so_the_mechanic_is_not_degenerate(self) -> None:
        across_seeds = [ps.commercial_counter_psi_investigation(s)["access_held"] for s in range(60)]
        self.assertIn(True, across_seeds)

    def test_the_two_accounts_are_incompatible(self) -> None:
        self.assertFalse(self.scene["accounts_agree"])
        observations = [f["observation"] for f in self.scene["ledger"]["findings"]["op-harbour-audit"]]
        self.assertEqual(len(set(observations)), len(observations))

    def test_every_finding_offers_alternative_explanations(self) -> None:
        findings = self.scene["ledger"]["findings"]["op-harbour-audit"]
        self.assertTrue(findings)
        for finding in findings:
            self.assertTrue(finding["alternative_explanations"], finding["observation"])

    def test_no_finding_claims_corroboration_without_evidence(self) -> None:
        for finding in self.scene["ledger"]["findings"]["op-harbour-audit"]:
            if finding["verification"] == "corroborated":
                self.assertTrue(finding["evidence_refs"])
            self.assertEqual(finding["verification"], "inconclusive")

    def test_the_client_is_told_what_cannot_be_proven(self) -> None:
        self.assertIn("inconclusive", self.scene["client_answer"])
        self.assertIn("Nothing here identifies", self.scene["proves_what"])

    def test_psi_is_never_framed_as_unproven(self) -> None:
        """The mystery is which mechanisms, not whether PSI exists."""
        blob = repr(self.scene).lower()
        for banned in ("whether psi exists", "if psi is real", "prove psi", "debunk"):
            self.assertNotIn(banned, blob, banned)

    def test_consent_and_logging_are_part_of_the_service(self) -> None:
        assets = self.scene["operation"]["asset_ids"]
        self.assertTrue(any("leased" in a or "logged" in a for a in assets))

    def test_it_is_deterministic(self) -> None:
        self.assertEqual(ps.commercial_counter_psi_investigation(4)["access"].dice,
                         ps.commercial_counter_psi_investigation(4)["access"].dice)


class PsiIsEstablishedScienceTests(unittest.TestCase):
    def test_the_module_states_psi_is_established(self) -> None:
        source = Path(ps.__file__).read_text(encoding="utf-8")
        self.assertIn("established mainstream science", source)

    def test_the_module_adds_no_power_and_no_mechanic(self) -> None:
        source = Path(ps.__file__).read_text(encoding="utf-8").split('"""', 2)[-1]
        for banned in ("def cast", "spell", "mana", "fireball", "power_level", "psi_points"):
            self.assertNotIn(banned, source, banned)

    def test_it_reuses_the_existing_psi_seam_rather_than_a_second_one(self) -> None:
        source = Path(ps.__file__).read_text(encoding="utf-8")
        self.assertIn("from .psi_operations import", source)

    def test_it_imports_the_rpg_layer_in_the_permitted_direction(self) -> None:
        """strategy_game -> rpg, never rpg -> strategy_game."""
        source = Path(ps.__file__).read_text(encoding="utf-8")
        self.assertIn("from .rpg import fate", source)
        self.assertNotIn("from ..", source)


class ScopeTests(unittest.TestCase):
    def test_no_optional_dependency_is_required(self) -> None:
        source = Path(ps.__file__).read_text(encoding="utf-8")
        for banned in ("numpy", "pandas", "requests", "ollama", "openai"):
            self.assertNotIn(f"import {banned}", source)

    def test_it_proposes_no_numeric_scale(self) -> None:
        source = Path(ps.__file__).read_text(encoding="utf-8")
        for banned in ("psi_strength", "power_rating", "psi_score", "capability_level"):
            self.assertNotIn(banned, source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
