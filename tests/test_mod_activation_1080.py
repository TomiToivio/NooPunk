"""The registry is readable by a machine (#1080 item 6), now that #1091 gave it a contract.

Kept deliberately thin: the contract itself is tested in `test_mod_contract_1091.py`, and this file
only checks the part #1080 asked for — that the registry is a working data file with a tool behind it,
not a paragraph of prose that happens to be JSON.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import check_mod_activation as tool  # noqa: E402
from rules.mod_boundary import validate_registry  # noqa: E402

REGISTRY = ROOT / "data" / "mods" / "registry.json"


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_the_registry_is_schema_three(self):
        self.assertEqual(self.data["schema"], 3)

    def test_the_registry_validates(self):
        self.assertTrue(validate_registry(self.data["mods"], root=ROOT))

    def test_every_mod_carries_an_implementation_list(self):
        for mod in self.data["mods"]:
            with self.subTest(mod=mod["name"]):
                self.assertIsInstance(mod.get("implementation"), list)

    def test_the_tool_prints_a_table(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/check_mod_activation.py")],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("off-switch", result.stdout)
        self.assertIn("implemented", result.stdout)

    def test_the_rows_match_the_registry(self):
        table = tool.rows(self.data, tool.test_corpus())
        self.assertEqual([r["name"] for r in table], [m["name"] for m in self.data["mods"]])


if __name__ == "__main__":
    unittest.main()
