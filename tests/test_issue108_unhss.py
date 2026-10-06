"""Acceptance guard for issue #108: UNSA / Firewall campaign canon."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
FACTIONS = (ROOT / "FACTIONS.md").read_text(encoding="utf-8")
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")


class Issue108UNSATests(unittest.TestCase):
    def test_name_and_aliases(self):
        for phrase in (
            "United Nations Security Agency (UNSA)",
            "United Nations X-Risk and NHI Organization",
            "UN X-Risk Agency", "UN NHI Agency",
            "X-Com", "X-Cops", "X-Files", "Men in Black",
        ):
            self.assertIn(phrase, BOOK)

    def test_default_pc_dual_affiliation(self):
        self.assertIn("Player characters are UNSA field agents", BOOK)
        self.assertIn("personal faction identity + UNSA mission", BOOK)
        self.assertIn("UNSA", FACTIONS)

    def test_three_function_hybrid_and_forces(self):
        for phrase in (
            "Civilian / scientific / diplomatic branch",
            "UNSA Police",
            "Tactical / military component",
            "Earth Special Operations Regiment",
            "Solar-System Space Marine Regiment",
            "strike fleet",
            "deep-space scouts",
        ):
            self.assertIn(phrase, BOOK)

    def test_federal_un_and_wallfacers(self):
        for phrase in (
            "UN President", "UN Prime Minister", "UN Parliament",
            "four years", "four Wallfacers",
            "Minister of Human Security and Survival",
        ):
            self.assertIn(phrase, BOOK)

    def test_machine_readable_model(self):
        for phrase in ("canonical_name:", "wallfacers: 4", "dual_affiliation: true"):
            self.assertIn(phrase, ORG)


if __name__ == "__main__":
    unittest.main()
