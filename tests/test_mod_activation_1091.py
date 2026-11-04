"""Regression tests for the canonical mod activation contract (#1091)."""
import copy
import json
import unittest
from pathlib import Path

from src.rules.mod_boundary import BaselineViolation, validate_registry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/mods/registry.json"


class ActivationContractTests(unittest.TestCase):
    def setUp(self):
        self.mods = json.loads(REGISTRY.read_text(encoding="utf-8"))["mods"]

    def reject(self, mutate):
        records = copy.deepcopy(self.mods)
        mutate(records[0])
        with self.assertRaises(BaselineViolation):
            validate_registry(records)

    def test_every_real_module_has_valid_metadata(self):
        """The count is the registry's, not a literal: a new mod must not need this test edited."""
        accepted = validate_registry(self.mods)
        self.assertEqual(sorted(accepted), sorted(mod["name"] for mod in self.mods))
        self.assertGreaterEqual(len(accepted), 6)

    def test_missing_hooks_fail(self):
        self.reject(lambda mod: mod.pop("hooks"))

    def test_nonexistent_function_fails(self):
        self.reject(lambda mod: mod["hooks"].append({"path": mod["implementation"][0], "symbol": "imaginary_hook_1091"}))

    def test_unregistered_hook_file_fails(self):
        self.reject(lambda mod: mod["hooks"].append({"path": "README.md", "symbol": "fake"}))

    def test_missing_state_fails(self):
        self.reject(lambda mod: mod.pop("state"))

    def test_unknown_dependency_fails(self):
        self.reject(lambda mod: mod["dependencies"].append("nonexistent_mod"))

    def test_missing_off_switch_fails(self):
        self.reject(lambda mod: mod.pop("off_switch"))

    def test_missing_tabletop_path_fails(self):
        self.reject(lambda mod: mod.update(tabletop_procedure="docs/NO_SUCH_FILE_1091.md"))

    def test_missing_tabletop_gap_fails(self):
        self.reject(lambda mod: mod.update(tabletop_procedure=None, tabletop_gap=None))

    def test_unimplemented_mod_cannot_claim_hooks(self):
        records = copy.deepcopy(self.mods)
        empty = next(m for m in records if m["name"] == "vices_temptations")
        empty["hooks"] = [{"path": "README.md", "symbol": "fake"}]
        with self.assertRaises(BaselineViolation):
            validate_registry(records)

    def test_published_cwn_is_still_separate(self):
        for mod in self.mods:
            self.assertFalse(mod["changes_core_mechanics"])
            self.assertFalse(mod["off_switch"]["default_enabled"])


if __name__ == "__main__":
    unittest.main()
