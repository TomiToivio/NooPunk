"""Regression guards for EU technology lore (#1236), reconciled with main."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/lore/eu_technology_bureaucracy.md"
REGISTER = ROOT / "docs/DOCUMENT_REGISTER.md"
HISTORY = ROOT / "docs/world/ALTERNATE_HISTORY_1114.md"

class EUTechnologyLoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")
    def test_document_and_register(self):
        self.assertGreater(len(self.text), 10000)
        self.assertIn("lore/eu_technology_bureaucracy.md", REGISTER.read_text(encoding="utf-8"))
    def test_war_treated_as_fiction_with_disputed_testimony(self):
        for term in ("Medvedev", "Putin", "VDV", "World War Three", "[CONTESTED]", "Mandela Effect"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.text.lower())
    def test_technology_and_ai_constraints(self):
        for term in ("New European Idealism", "Spinoza", "Kant", "Hegel", "Gemma 4 31B", "Mistral", "GOFAI", "Prolog", "EMP", "firebreak"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.text.lower())
    def test_field_operations_and_evidence(self):
        for term in ("Tony German", "Laura Wendt", "Salla Sotavaara", "PoliisiSanomalaite", "RFOAS", "cyberdeck", "Plato", "Eurodef", "Clue"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.text.lower())
    def test_open_decisions_and_mechanical_boundary(self):
        self.assertIn("## 9. Open decisions", self.text)
        self.assertIn("## 10. What this document does not do", self.text)
    def test_history_cross_reference(self):
        self.assertIn("eu_technology_bureaucracy.md", HISTORY.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
