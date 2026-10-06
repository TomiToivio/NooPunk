"""Guards for issues #158 and #162: UNSA academy and default investigation doctrine."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
CYBER = (ROOT / "rulebook" / "5_CYBERNETIC.md").read_text(encoding="utf-8")
ACADEMY = json.loads((ROOT / "data" / "rules" / "unsa_academy.json").read_text(encoding="utf-8"))
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")


class AcademyBaselineTests(unittest.TestCase):
    def test_rating_and_core_training_are_pinned(self) -> None:
        self.assertEqual(ACADEMY["universal_rating"], 3)
        required = {
            "Guns", "Unarmed", "Melee", "Athletics", "Tactics", "First Aid",
            "Investigation", "Forensics", "Perceive", "Research",
            "Intelligence Analysis", "Counterintelligence", "Infosec", "Interface",
            "Psychic Defence", "Talk", "Kinesics", "Know (Law)", "Work (Police Officer)",
        }
        self.assertTrue(required.issubset(set(ACADEMY["universal_training"])))

    def test_universal_psionics_are_defensive_not_full_psi(self) -> None:
        self.assertEqual(ACADEMY["universal_psionics"]["granted"], ["Psychic Defence"])
        for skill in ("ESP", "Telepathy", "Psychokinesis", "Precognition", "Noöspace"):
            self.assertIn(skill, ACADEMY["universal_psionics"]["not_granted"])

    def test_specialist_tracks_remain_deltas(self) -> None:
        self.assertEqual(
            ACADEMY["specialist_tracks"],
            ["UNSA SWAT Academy", "UNSA PSI Academy", "UNSA TECH Academy", "UNSA NHI Academy"],
        )
        self.assertIn("deltas on top of the shared academy baseline", RULEBOOK)


class InvestigationDoctrineTests(unittest.TestCase):
    def test_default_cell_has_four_roles(self) -> None:
        self.assertEqual(len(ACADEMY["default_investigation_cell"]), 4)
        for role in ("player field investigator", "persistent field partner",
                     "remote human controller", "constrained non-AGI forensic AI"):
            self.assertIn(role, ACADEMY["default_investigation_cell"])
            self.assertIn(role, ORG)

    def test_four_evidence_domains_survive(self) -> None:
        self.assertEqual(
            ACADEMY["evidence_domains"],
            ["physical", "cybernetic", "social", "psychic/noospace"],
        )
        for label in ("**Physical**", "**Cybernetic**", "**Social**", "**Psychic / Noöspace**"):
            self.assertIn(label, RULEBOOK)

    def test_ai_is_copilot_not_autopilot(self) -> None:
        self.assertIn("copilot, not an autopilot", RULEBOOK)
        self.assertIn("not an AGI", CYBER)

    def test_voight_kampff_is_probabilistic(self) -> None:
        protocol = ACADEMY["assessment_protocol"]
        self.assertEqual(protocol["colloquial_name"], "Voight-Kampff")
        self.assertIn("probabilistic", protocol["nature"])
        self.assertIn("probabilistic", RULEBOOK)
        self.assertIn("never a truth machine", RULEBOOK)

    def test_force_doctrine_requires_triangulation(self) -> None:
        for statement in (
            "Triangulate reality before acting.",
            "NHI status alone is not grounds for lethal force.",
        ):
            self.assertIn(statement, ACADEMY["doctrine"])
        self.assertIn("triangulate reality before acting", RULEBOOK)
        self.assertIn("NHI status is not itself grounds for lethal", RULEBOOK)

    def test_men_in_black_are_not_unsa(self) -> None:
        self.assertIn("Men in Black are not the player organization", RULEBOOK)
        self.assertIn("Men in Black is not a", RULEBOOK)
        self.assertIn("Orion", RULEBOOK)


class CyberneticBaselineTests(unittest.TestCase):
    def test_tri_layer_sensorium_exists(self) -> None:
        self.assertIn("Physical / Cyber / Astral", CYBER)
        for heading in ("### Physical", "### Cyber", "### Astral / Noetic"):
            self.assertIn(heading, CYBER)

    def test_no_implant_path_is_preserved(self) -> None:
        self.assertIn("Implants are common but not compulsory", CYBER)
        self.assertIn("fully playable", CYBER)

    def test_equipment_is_tiered_without_numeric_stats(self) -> None:
        for heading in ("### Standard worn / carried", "### Mission-issued",
                        "### Restricted / specialist / experimental"):
            self.assertIn(heading, CYBER)
        self.assertIn("does **not** define numeric cyberware statistics", CYBER)


if __name__ == "__main__":
    unittest.main()
