"""Documentary consistency checks for issue #1200, without changing CWN rules."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "docs/world/PLATO_EISS_EURONET_1200.md"


class PlatoCanonTests(unittest.TestCase):
    def test_canonical_name_and_no_new_asi(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for term in ("Project Plato", "European Information Security System (EISS)", "Panopticon", "not a single thinking supercomputer"):
            self.assertIn(term, text)
        self.assertIn("AEGIS is not established canon", text)

    def test_separate_networks_and_legal_limits(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for term in ("Old Internet", "EuroNET", "Closed organizational networks", "Physical data couriers", "Finnish police", "Eurodef", "UNSA", "CWN core remains immutable"):
            self.assertIn(term, text)
        self.assertIn("no remote access", text)

    def test_europe_tech_matrix_maintains_qualitative_profile(self):
        matrix = json.loads((ROOT / "data/world/tech_matrix.json").read_text(encoding="utf-8"))
        eu = next(region for region in matrix["regions"] if region["id"] == "european-federation")
        canon = eu["$plato_eiss_canon_1200"]
        self.assertEqual(canon["official_system"], "European Information Security System (EISS)")
        self.assertEqual(canon["public_network"], "EuroNET")
        self.assertEqual(canon["unofficial_critical_nickname"], "Panopticon")
        self.assertEqual(eu["profile"]["ai_autonomy"], "regulated")
        self.assertEqual(eu["profile"]["psionics"], "unassigned")


if __name__ == "__main__":
    unittest.main()
